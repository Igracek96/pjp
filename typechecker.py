"""Type checker: walks the AST, resolves types, inserts int->float conversions.
Also mangles variable names to handle nested scopes (e.g. y -> y$1)."""

from ast_nodes import (
    Program, VarDecl, Assign, BinOp, UnaryOp, IntToFloat, If, While,
    Block, Read, Write, Var, IntLit, FloatLit, BoolLit, StrLit, Empty, ExprStmt,
)


class TypeError_(Exception):
    """Named with underscore to avoid shadowing builtin TypeError."""
    pass


class ScopeManager:
    """Manages nested variable scopes with unique name mangling."""

    def __init__(self):
        self.scopes = [{}]        # each scope: name -> (mangled_name, type)
        self.var_counter = 0      # for generating unique mangled names

    def enter(self):
        self.scopes.append({})

    def exit(self):
        self.scopes.pop()

    def declare(self, name: str, var_type: str) -> str:
        """Declare variable, return its mangled name."""
        current = self.scopes[-1]
        if name in current:
            raise TypeError_(f"Variable '{name}' already declared in this scope")
        mangled = f"{name}${self.var_counter}"
        self.var_counter += 1
        current[name] = (mangled, var_type)
        return mangled

    def lookup(self, name: str):
        """Returns (mangled_name, type). Searches from innermost scope."""
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        raise TypeError_(f"Undeclared variable '{name}'")


class TypeChecker:
    def __init__(self):
        self.scope = ScopeManager()

    def check(self, node: Program):
        self.visit(node)

    def visit(self, node):
        method = f"visit_{type(node).__name__}"
        visitor = getattr(self, method, None)
        if visitor is None:
            raise TypeError_(f"No visitor for {type(node).__name__}")
        return visitor(node)

    def visit_Program(self, node: Program):
        for stmt in node.statements:
            self.visit(stmt)

    def visit_ExprStmt(self, node: ExprStmt):
        self.visit(node.expr)

    def visit_Empty(self, node: Empty):
        pass

    def visit_VarDecl(self, node: VarDecl):
        # Replace original names with mangled names in the AST
        mangled_names = []
        for name in node.names:
            mangled = self.scope.declare(name, node.var_type)
            mangled_names.append(mangled)
        node.names = mangled_names

    def visit_Block(self, node: Block):
        self.scope.enter()
        for stmt in node.statements:
            self.visit(stmt)
        self.scope.exit()

    def visit_If(self, node: If):
        cond_type = self.visit(node.condition)
        if cond_type != "bool":
            raise TypeError_(f"If condition must be bool, got '{cond_type}'")
        self.visit(node.then_stmt)
        if node.else_stmt is not None:
            self.visit(node.else_stmt)

    def visit_While(self, node: While):
        cond_type = self.visit(node.condition)
        if cond_type != "bool":
            raise TypeError_(f"While condition must be bool, got '{cond_type}'")
        self.visit(node.body)

    def visit_Read(self, node: Read):
        for var in node.variables:
            mangled, var_type = self.scope.lookup(var.name)
            var.name = mangled
            var.type = var_type

    def visit_Write(self, node: Write):
        for expr in node.expressions:
            self.visit(expr)

    def visit_Assign(self, node: Assign):
        if not isinstance(node.target, Var):
            raise TypeError_("Left side of assignment must be a variable")
        mangled, target_type = self.scope.lookup(node.target.name)
        node.target.name = mangled
        node.target.type = target_type
        val_type = self.visit(node.value)

        # Allow int -> float implicit conversion
        if target_type == "float" and val_type == "int":
            node.value = IntToFloat(node.value)
            val_type = "float"

        if target_type != val_type:
            raise TypeError_(
                f"Cannot assign '{val_type}' to variable of type '{target_type}'")
        node.type = target_type
        return target_type

    def visit_BinOp(self, node: BinOp):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        op = node.op

        # Boolean operators
        if op in ("||", "&&"):
            if left_type != "bool" or right_type != "bool":
                raise TypeError_(f"Operator '{op}' requires bool operands, got '{left_type}' and '{right_type}'")
            node.type = "bool"
            return "bool"

        # Concatenation
        if op == ".":
            if left_type != "string" or right_type != "string":
                raise TypeError_(f"Operator '.' requires string operands, got '{left_type}' and '{right_type}'")
            node.type = "string"
            return "string"

        # Modulo - int only
        if op == "%":
            if left_type != "int" or right_type != "int":
                raise TypeError_(f"Operator '%' requires int operands, got '{left_type}' and '{right_type}'")
            node.type = "int"
            return "int"

        # Implicit int->float promotion for mixed arithmetic
        if {left_type, right_type} == {"int", "float"}:
            if left_type == "int":
                node.left = IntToFloat(node.left)
                left_type = "float"
            else:
                node.right = IntToFloat(node.right)
                right_type = "float"

        # Arithmetic: +, -, *, /
        if op in ("+", "-", "*", "/"):
            if left_type not in ("int", "float") or right_type not in ("int", "float"):
                raise TypeError_(f"Operator '{op}' requires numeric operands, got '{left_type}' and '{right_type}'")
            if left_type != right_type:
                raise TypeError_(f"Type mismatch for '{op}': '{left_type}' and '{right_type}'")
            node.type = left_type
            return left_type

        # Relational: <, >
        if op in ("<", ">"):
            if left_type not in ("int", "float") or right_type not in ("int", "float"):
                raise TypeError_(f"Operator '{op}' requires numeric operands, got '{left_type}' and '{right_type}'")
            if left_type != right_type:
                raise TypeError_(f"Type mismatch for '{op}': '{left_type}' and '{right_type}'")
            node.type = "bool"
            return "bool"

        # Equality: ==, !=
        if op in ("==", "!="):
            if left_type == "bool" or right_type == "bool":
                raise TypeError_(f"Operator '{op}' cannot be used with bool operands")
            if left_type not in ("int", "float", "string") or right_type not in ("int", "float", "string"):
                raise TypeError_(f"Operator '{op}' requires int, float, or string operands")
            if left_type != right_type:
                raise TypeError_(f"Type mismatch for '{op}': '{left_type}' and '{right_type}'")
            node.type = "bool"
            return "bool"

        raise TypeError_(f"Unknown binary operator '{op}'")

    def visit_UnaryOp(self, node: UnaryOp):
        operand_type = self.visit(node.operand)
        if node.op == "!":
            if operand_type != "bool":
                raise TypeError_(f"Operator '!' requires bool operand, got '{operand_type}'")
            node.type = "bool"
            return "bool"
        if node.op == "-":
            if operand_type not in ("int", "float"):
                raise TypeError_(f"Unary '-' requires numeric operand, got '{operand_type}'")
            node.type = operand_type
            return operand_type
        raise TypeError_(f"Unknown unary operator '{node.op}'")

    def visit_Var(self, node: Var):
        mangled, var_type = self.scope.lookup(node.name)
        node.name = mangled
        node.type = var_type
        return var_type

    def visit_IntLit(self, node):
        return "int"

    def visit_FloatLit(self, node):
        return "float"

    def visit_BoolLit(self, node):
        return "bool"

    def visit_StrLit(self, node):
        return "string"

    def visit_IntToFloat(self, node):
        return "float"
