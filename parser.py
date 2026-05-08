"""Recursive descent parser: tokens -> AST."""

from typing import List
from lexer import Token
from ast_nodes import (
    Program, VarDecl, Assign, BinOp, UnaryOp, If, While,
    Block, Read, Write, Var, IntLit, FloatLit, BoolLit, StrLit, Empty, ExprStmt,
)


class ParseError(Exception):
    pass


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    # -- Helpers --

    def _current(self) -> Token:
        return self.tokens[self.pos]

    def _peek(self, token_type: str) -> bool:
        return self._current().type == token_type

    def _match(self, token_type: str) -> Token:
        tok = self._current()
        if tok.type != token_type:
            raise ParseError(
                f"Line {tok.line}: expected '{token_type}', got '{tok.type}' ('{tok.value}')")
        self.pos += 1
        return tok

    def _at_type_keyword(self) -> bool:
        return self._current().type in ("int", "float", "bool", "string")

    # -- Entry point --

    def parse(self) -> Program:
        stmts = []
        while not self._peek("EOF"):
            stmts.append(self._statement())
        return Program(stmts)

    # -- Statements --

    def _statement(self):
        tok = self._current()

        # Empty statement
        if tok.type == ";":
            self._match(";")
            return Empty()

        # Variable declaration: type id (',' id)* ';'
        if self._at_type_keyword():
            return self._var_decl()

        # Block
        if tok.type == "{":
            return self._block()

        # If
        if tok.type == "if":
            return self._if_stmt()

        # While
        if tok.type == "while":
            return self._while_stmt()

        # Read
        if tok.type == "read":
            return self._read_stmt()

        # Write
        if tok.type == "write":
            return self._write_stmt()

        # Expression statement
        return self._expr_stmt()

    def _var_decl(self):
        var_type = self._current().value
        self._match(self._current().type)  # consume the type keyword
        names = [self._match("ID").value]
        while self._peek(","):
            self._match(",")
            names.append(self._match("ID").value)
        self._match(";")
        return VarDecl(var_type, names)

    def _block(self):
        self._match("{")
        stmts = []
        while not self._peek("}"):
            stmts.append(self._statement())
        self._match("}")
        return Block(stmts)

    def _if_stmt(self):
        self._match("if")
        self._match("(")
        cond = self._expr()
        self._match(")")
        then_stmt = self._statement()
        else_stmt = None
        if self._peek("else"):
            self._match("else")
            else_stmt = self._statement()
        return If(cond, then_stmt, else_stmt)

    def _while_stmt(self):
        self._match("while")
        self._match("(")
        cond = self._expr()
        self._match(")")
        body = self._statement()
        return While(cond, body)

    def _read_stmt(self):
        self._match("read")
        variables = [Var(self._match("ID").value)]
        while self._peek(","):
            self._match(",")
            variables.append(Var(self._match("ID").value))
        self._match(";")
        return Read(variables)

    def _write_stmt(self):
        self._match("write")
        exprs = [self._expr()]
        while self._peek(","):
            self._match(",")
            exprs.append(self._expr())
        self._match(";")
        return Write(exprs)

    def _expr_stmt(self):
        expr = self._expr()
        self._match(";")
        return ExprStmt(expr)

    # -- Expressions (precedence climbing) --

    def _expr(self):
        return self._assignment()

    def _assignment(self):
        left = self._or_expr()
        if self._peek("="):
            self._match("=")
            right = self._assignment()  # right-associative
            return Assign(left, right)
        return left

    def _or_expr(self):
        left = self._and_expr()
        while self._peek("||"):
            self._match("||")
            right = self._and_expr()
            left = BinOp("||", left, right)
        return left

    def _and_expr(self):
        left = self._eq_expr()
        while self._peek("&&"):
            self._match("&&")
            right = self._eq_expr()
            left = BinOp("&&", left, right)
        return left

    def _eq_expr(self):
        left = self._rel_expr()
        while self._current().type in ("==", "!="):
            op = self._match(self._current().type).value
            right = self._rel_expr()
            left = BinOp(op, left, right)
        return left

    def _rel_expr(self):
        left = self._add_expr()
        while self._current().type in ("<", ">"):
            op = self._match(self._current().type).value
            right = self._add_expr()
            left = BinOp(op, left, right)
        return left

    def _add_expr(self):
        left = self._mul_expr()
        while self._current().type in ("+", "-", "."):
            op = self._match(self._current().type).value
            right = self._mul_expr()
            left = BinOp(op, left, right)
        return left

    def _mul_expr(self):
        left = self._unary()
        while self._current().type in ("*", "/", "%"):
            op = self._match(self._current().type).value
            right = self._unary()
            left = BinOp(op, left, right)
        return left

    def _unary(self):
        if self._peek("!"):
            self._match("!")
            operand = self._unary()
            return UnaryOp("!", operand)
        if self._peek("-"):
            self._match("-")
            operand = self._unary()
            return UnaryOp("-", operand)
        return self._primary()

    def _primary(self):
        tok = self._current()

        if tok.type == "INT":
            self._match("INT")
            return IntLit(int(tok.value))

        if tok.type == "FLOAT":
            self._match("FLOAT")
            return FloatLit(float(tok.value))

        if tok.type == "STRING":
            self._match("STRING")
            return StrLit(tok.value)

        if tok.type == "true":
            self._match("true")
            return BoolLit(True)

        if tok.type == "false":
            self._match("false")
            return BoolLit(False)

        if tok.type == "ID":
            self._match("ID")
            return Var(tok.value)

        if tok.type == "(":
            self._match("(")
            expr = self._expr()
            self._match(")")
            return expr

        raise ParseError(
            f"Line {tok.line}: unexpected token '{tok.value}' in expression")
