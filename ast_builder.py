"""Converts ANTLR parse tree into our AST nodes (from ast_nodes.py).

ANTLR generates a generic parse tree. This visitor walks it and builds
our AST, which the rest of the pipeline (typechecker, codegen, interpreter) uses.
"""

from PLCParser import PLCParser
from PLCVisitor import PLCVisitor
from ast_nodes import (
    Program, VarDecl, Assign, BinOp, UnaryOp, If, While,
    Block, Read, Write, Var, IntLit, FloatLit, BoolLit, StrLit, Empty, ExprStmt,
)


class ASTBuilder(PLCVisitor):

    # ---- Program ----

    def visitProgram(self, ctx: PLCParser.ProgramContext):
        stmts = [self.visit(s) for s in ctx.statement()]
        return Program(stmts)

    # ---- Statements ----

    def visitEmptyStmt(self, ctx):
        return Empty()

    def visitVarDeclStmt(self, ctx):
        var_type = ctx.varType.text
        names = [tok.getText() for tok in ctx.ID()]
        return VarDecl(var_type, names)

    def visitExprStmt(self, ctx):
        return ExprStmt(self.visit(ctx.expr()))

    def visitReadStmt(self, ctx):
        variables = [Var(tok.getText()) for tok in ctx.ID()]
        return Read(variables)

    def visitWriteStmt(self, ctx):
        exprs = [self.visit(e) for e in ctx.expr()]
        return Write(exprs)

    def visitBlockStmt(self, ctx):
        stmts = [self.visit(s) for s in ctx.statement()]
        return Block(stmts)

    def visitIfStmt(self, ctx):
        cond = self.visit(ctx.expr())
        stmts = ctx.statement()
        then_stmt = self.visit(stmts[0])
        else_stmt = self.visit(stmts[1]) if len(stmts) > 1 else None
        return If(cond, then_stmt, else_stmt)

    def visitWhileStmt(self, ctx):
        cond = self.visit(ctx.expr())
        body = self.visit(ctx.statement())
        return While(cond, body)

    # ---- Expressions ----

    def visitAssignExpr(self, ctx):
        target = self.visit(ctx.expr(0))
        value = self.visit(ctx.expr(1))
        return Assign(target, value)

    def visitOrExpr(self, ctx):
        return BinOp("||", self.visit(ctx.expr(0)), self.visit(ctx.expr(1)))

    def visitAndExpr(self, ctx):
        return BinOp("&&", self.visit(ctx.expr(0)), self.visit(ctx.expr(1)))

    def visitEqExpr(self, ctx):
        return BinOp(ctx.op.text, self.visit(ctx.expr(0)), self.visit(ctx.expr(1)))

    def visitRelExpr(self, ctx):
        return BinOp(ctx.op.text, self.visit(ctx.expr(0)), self.visit(ctx.expr(1)))

    def visitAddExpr(self, ctx):
        return BinOp(ctx.op.text, self.visit(ctx.expr(0)), self.visit(ctx.expr(1)))

    def visitMulExpr(self, ctx):
        return BinOp(ctx.op.text, self.visit(ctx.expr(0)), self.visit(ctx.expr(1)))

    def visitNotExpr(self, ctx):
        return UnaryOp("!", self.visit(ctx.expr()))

    def visitUminusExpr(self, ctx):
        return UnaryOp("-", self.visit(ctx.expr()))

    def visitParenExpr(self, ctx):
        return self.visit(ctx.expr())

    # ---- Literals ----

    def visitIntLitExpr(self, ctx):
        return IntLit(int(ctx.INT().getText()))

    def visitFloatLitExpr(self, ctx):
        return FloatLit(float(ctx.FLOAT().getText()))

    def visitBoolLitExpr(self, ctx):
        return BoolLit(ctx.BOOL().getText() == "true")

    def visitStringLitExpr(self, ctx):
        raw = ctx.STRING().getText()
        # Strip surrounding quotes and process escape sequences
        s = raw[1:-1]
        s = s.replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"').replace('\\\\', '\\')
        return StrLit(s)

    def visitVarExpr(self, ctx):
        return Var(ctx.ID().getText())
