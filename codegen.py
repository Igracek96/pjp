"""Code generator: typed AST -> stack machine instructions (list of strings)."""

from ast_nodes import (
    Program, VarDecl, Assign, BinOp, UnaryOp, IntToFloat, If, While,
    Block, Read, Write, Var, IntLit, FloatLit, BoolLit, StrLit, Empty, ExprStmt,
)

TYPE_SUFFIX = {"int": "I", "float": "F", "bool": "B", "string": "S"}

# Default push instruction for each type (strings use quoted empty string)
DEFAULTS = {
    "int":    "push I 0",
    "float":  "push F 0.0",
    "bool":   "push B false",
    "string": 'push S ""',
}


def _escape_str(s: str) -> str:
    """Escape a Python string for use in instruction format: push S "..."."""
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\t", "\\t")


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
            self.emit(DEFAULTS[node.var_type])
            self.emit(f"save {name}")

    def visit_Block(self, node: Block):
        for stmt in node.statements:
            self.visit(stmt)

    def visit_If(self, node: If):
        # Always generate both labels (else + end), even if there is no else branch.
        # This matches the expected instruction format from the assignment.
        else_label = self.new_label()
        end_label  = self.new_label()
        self.visit(node.condition)
        self.emit(f"fjmp {else_label}")
        self.visit(node.then_stmt)
        self.emit(f"jmp {end_label}")
        self.emit(f"label {else_label}")
        if node.else_stmt is not None:
            self.visit(node.else_stmt)
        self.emit(f"label {end_label}")

    def visit_While(self, node: While):
        start_label = self.new_label()
        end_label   = self.new_label()
        self.emit(f"label {start_label}")
        self.visit(node.condition)
        self.emit(f"fjmp {end_label}")
        self.visit(node.body)
        self.emit(f"jmp {start_label}")
        self.emit(f"label {end_label}")

    def visit_Read(self, node: Read):
        for var in node.variables:
            self.emit(f"read {TYPE_SUFFIX[var.type]}")
            self.emit(f"save {var.name}")

    def visit_Write(self, node: Write):
        for expr in node.expressions:
            self.visit(expr)
        self.emit(f"print {len(node.expressions)}")

    def visit_Assign(self, node: Assign):
        self.visit(node.value)
        self.emit(f"save {node.target.name}")
        self.emit(f"load {node.target.name}")   # assignment is an expression – leave value on stack

    def visit_BinOp(self, node: BinOp):
        self.visit(node.left)
        self.visit(node.right)
        op = node.op
        t  = node.type

        if op == "+":    self.emit(f"add {TYPE_SUFFIX[t]}")
        elif op == "-":  self.emit(f"sub {TYPE_SUFFIX[t]}")
        elif op == "*":  self.emit(f"mul {TYPE_SUFFIX[t]}")
        elif op == "/":  self.emit(f"div {TYPE_SUFFIX[t]}")
        elif op == "%":  self.emit("mod")
        elif op == ".":  self.emit("concat")
        elif op == "&&": self.emit("and")
        elif op == "||": self.emit("or")
        elif op == "<":
            self.emit(f"lt {TYPE_SUFFIX[node.left.type]}")
        elif op == ">":
            self.emit(f"gt {TYPE_SUFFIX[node.left.type]}")
        elif op == "==":
            self.emit(f"eq {TYPE_SUFFIX[node.left.type]}")
        elif op == "!=":
            self.emit(f"eq {TYPE_SUFFIX[node.left.type]}")
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
        self.emit(f'push S "{_escape_str(node.value)}"')
