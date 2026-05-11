"""Type checker: walks the AST, resolves types, inserts int->float conversions.
Reports ALL type errors (does not stop at first)."""

import sys
from ast_nodes import (
    Program, VarDecl, Assign, BinOp, UnaryOp, IntToFloat, If, While,
    Block, Read, Write, Var, IntLit, FloatLit, BoolLit, StrLit, Empty, ExprStmt,
)


class TypeError_(Exception):
    pass


class ScopeManager:
    """Manages nested variable scopes. Shadowing (redeclaration in any scope) is forbidden."""

    def __init__(self):
        self.scopes = [{}]    # stack of dicts: name -> type

    def enter(self):
        self.scopes.append({})

    def exit(self):
        self.scopes.pop()

    def declare(self, name: str, var_type: str):
        # Redeclaration in ANY active scope is an error
        for scope in self.scopes:
            if name in scope:
                raise TypeError_(f"Variable '{name}' already declared")
        self.scopes[-1][name] = var_type

    def lookup(self, name: str) -> str:
        """Returns type. Searches from innermost scope outward."""
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        raise TypeError_(f"Undeclared variable '{name}'")


class TypeChecker:
    def __init__(self):
        self.scope = ScopeManager()
        self.errors = []

    def check(self, node: Program):
        self.visit(node)
        if self.errors:
            for err in self.errors:
                print(f"Type error: {err}", file=sys.stderr)
            raise TypeError_("Type checking failed")

    def visit(self, node):
        method = f"visit_{type(node).__name__}"
        visitor = getattr(self, method, None)
        if visitor is None:
            raise TypeError_(f"No visitor for {type(node).__name__}")
        return visitor(node)

    def _safe_visit(self, node):
        """Visit a node, catching TypeError_ and collecting it instead of propagating."""
        try:
            return self.visit(node)
        except TypeError_ as e:
            self.errors.append(str(e))
            return None

    def visit_Program(self, node: Program):
        for stmt in node.statements:
            self._safe_visit(stmt)

    def visit_ExprStmt(self, node: ExprStmt):
        self._safe_visit(node.expr)

    def visit_Empty(self, node: Empty):
        pass

    def visit_VarDecl(self, node: VarDecl):
        for name in node.names:
            try:
                self.scope.declare(name, node.var_type)
            except TypeError_ as e:
                self.errors.append(str(e))

    def visit_Block(self, node: Block):
        self.scope.enter()
        for stmt in node.statements:
            self._safe_visit(stmt)
        self.scope.exit()

    def visit_If(self, node: If):
        cond_type = self._safe_visit(node.condition)
        if cond_type is not None and cond_type != "bool":
            self.errors.append(f"If condition must be bool, got '{cond_type}'")
        self._safe_visit(node.then_stmt)
        if node.else_stmt is not None:
            self._safe_visit(node.else_stmt)

    def visit_While(self, node: While):
        cond_type = self._safe_visit(node.condition)
        if cond_type is not None and cond_type != "bool":
            self.errors.append(f"While condition must be bool, got '{cond_type}'")
        self._safe_visit(node.body)

    def visit_Read(self, node: Read):
        for var in node.variables:
            try:
                var_type = self.scope.lookup(var.name)
                var.type = var_type
            except TypeError_ as e:
                self.errors.append(str(e))

    def visit_Write(self, node: Write):
        for expr in node.expressions:
            self._safe_visit(expr)

    def visit_Assign(self, node: Assign):
        if not isinstance(node.target, Var):
            raise TypeError_("Left side of assignment must be a variable")
        target_type = self.scope.lookup(node.target.name)
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

        if op in ("||", "&&"):
            if left_type != "bool" or right_type != "bool":
                raise TypeError_(f"Operator '{op}' requires bool operands, got '{left_type}' and '{right_type}'")
            node.type = "bool"
            return "bool"

        if op == ".":
            if left_type != "string" or right_type != "string":
                raise TypeError_(f"Operator '.' requires string operands, got '{left_type}' and '{right_type}'")
            node.type = "string"
            return "string"

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

        if op in ("+", "-", "*", "/"):
            if left_type not in ("int", "float") or left_type != right_type:
                raise TypeError_(f"Operator '{op}' requires matching numeric operands, got '{left_type}' and '{right_type}'")
            node.type = left_type
            return left_type

        if op in ("<", ">"):
            if left_type not in ("int", "float") or left_type != right_type:
                raise TypeError_(f"Operator '{op}' requires matching numeric operands, got '{left_type}' and '{right_type}'")
            node.type = "bool"
            return "bool"

        if op in ("==", "!="):
            if left_type == "bool" or right_type == "bool":
                raise TypeError_(f"Operator '{op}' cannot be used with bool operands")
            if left_type not in ("int", "float", "string") or left_type != right_type:
                raise TypeError_(f"Operator '{op}' requires matching operands, got '{left_type}' and '{right_type}'")
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
        var_type = self.scope.lookup(node.name)
        node.type = var_type
        return var_type

    def visit_IntLit(self, node):   return "int"
    def visit_FloatLit(self, node): return "float"
    def visit_BoolLit(self, node):  return "bool"
    def visit_StrLit(self, node):   return "string"

    def visit_IntToFloat(self, node):
        return "float"
