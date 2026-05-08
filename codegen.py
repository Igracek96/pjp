"""Code generator: typed AST -> stack machine instructions."""

from ast_nodes import (
    Program, VarDecl, Assign, BinOp, UnaryOp, IntToFloat, If, While,
    Block, Read, Write, Var, IntLit, FloatLit, BoolLit, StrLit, Empty, ExprStmt,
)

# Map PLC types to instruction type suffixes
TYPE_SUFFIX = {"int": "I", "float": "F", "bool": "B", "string": "S"}

# Default values for variable declarations
DEFAULTS = {"int": ("I", 0), "float": ("F", 0.0), "bool": ("B", "false"), "string": ("S", "")}


class CodeGen:
    def __init__(self):
        self.instructions = []
        self.label_counter = 0

    def new_label(self) -> int:
        n = self.label_counter
        self.label_counter += 1
        return n

    def emit(self, instr: str):
        self.instructions.append(instr)

    def generate(self, node: Program) -> list:
        self.visit(node)
        return self.instructions

    def visit(self, node):
        method = f"visit_{type(node).__name__}"
        return getattr(self, method)(node)

    def visit_Program(self, node: Program):
        for stmt in node.statements:
            self.visit(stmt)

    def visit_ExprStmt(self, node):
        self.visit(node.expr)
        self.emit("pop")

    def visit_Empty(self, node):
        pass

    def visit_VarDecl(self, node: VarDecl):
        for name in node.names:
            suffix, default = DEFAULTS[node.var_type]
            self.emit(f"push {suffix} {default}")
            self.emit(f"save {name}")

    def visit_Block(self, node: Block):
        for stmt in node.statements:
            self.visit(stmt)

    def visit_If(self, node: If):
        if node.else_stmt is not None:
            else_label = self.new_label()
            end_label = self.new_label()
            self.visit(node.condition)
            self.emit(f"fjmp {else_label}")
            self.visit(node.then_stmt)
            self.emit(f"jmp {end_label}")
            self.emit(f"label {else_label}")
            self.visit(node.else_stmt)
            self.emit(f"label {end_label}")
        else:
            end_label = self.new_label()
            self.visit(node.condition)
            self.emit(f"fjmp {end_label}")
            self.visit(node.then_stmt)
            self.emit(f"label {end_label}")

    def visit_While(self, node: While):
        start_label = self.new_label()
        end_label = self.new_label()
        self.emit(f"label {start_label}")
        self.visit(node.condition)
        self.emit(f"fjmp {end_label}")
        self.visit(node.body)
        self.emit(f"jmp {start_label}")
        self.emit(f"label {end_label}")

    def visit_Read(self, node: Read):
        for var in node.variables:
            suffix = TYPE_SUFFIX[var.type]
            self.emit(f"read {suffix}")
            self.emit(f"save {var.name}")

    def visit_Write(self, node: Write):
        for expr in node.expressions:
            self.visit(expr)
        self.emit(f"print {len(node.expressions)}")

    def visit_Assign(self, node: Assign):
        self.visit(node.value)
        self.emit(f"save {node.target.name}")
        self.emit(f"load {node.target.name}")  # assignment is an expression; leave value on stack

    def visit_BinOp(self, node: BinOp):
        self.visit(node.left)
        self.visit(node.right)
        op = node.op
        t = node.type

        if op == "+":
            self.emit(f"add {TYPE_SUFFIX[t]}")
        elif op == "-":
            self.emit(f"sub {TYPE_SUFFIX[t]}")
        elif op == "*":
            self.emit(f"mul {TYPE_SUFFIX[t]}")
        elif op == "/":
            self.emit(f"div {TYPE_SUFFIX[t]}")
        elif op == "%":
            self.emit("mod")
        elif op == ".":
            self.emit("concat")
        elif op == "&&":
            self.emit("and")
        elif op == "||":
            self.emit("or")
        elif op == "<":
            # Result type is bool, but instruction needs the operand type
            operand_type = node.left.type
            self.emit(f"lt {TYPE_SUFFIX[operand_type]}")
        elif op == ">":
            operand_type = node.left.type
            self.emit(f"gt {TYPE_SUFFIX[operand_type]}")
        elif op == "==":
            operand_type = node.left.type
            self.emit(f"eq {TYPE_SUFFIX[operand_type]}")
        elif op == "!=":
            operand_type = node.left.type
            self.emit(f"eq {TYPE_SUFFIX[operand_type]}")
            self.emit("not")

    def visit_UnaryOp(self, node: UnaryOp):
        self.visit(node.operand)
        if node.op == "-":
            self.emit(f"uminus {TYPE_SUFFIX[node.type]}")
        elif node.op == "!":
            self.emit("not")

    def visit_IntToFloat(self, node: IntToFloat):
        self.visit(node.expr)
        self.emit("itof")

    def visit_Var(self, node: Var):
        self.emit(f"load {node.name}")

    def visit_IntLit(self, node: IntLit):
        self.emit(f"push I {node.value}")

    def visit_FloatLit(self, node: FloatLit):
        self.emit(f"push F {node.value}")

    def visit_BoolLit(self, node: BoolLit):
        self.emit(f"push B {'true' if node.value else 'false'}")

    def visit_StrLit(self, node: StrLit):
        self.emit(f"push S {node.value}")
