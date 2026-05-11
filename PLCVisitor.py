# Generated from PLC.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .PLCParser import PLCParser
else:
    from PLCParser import PLCParser

# This class defines a complete generic visitor for a parse tree produced by PLCParser.

class PLCVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by PLCParser#program.
    def visitProgram(self, ctx:PLCParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLCParser#EmptyStmt.
    def visitEmptyStmt(self, ctx:PLCParser.EmptyStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLCParser#VarDeclStmt.
    def visitVarDeclStmt(self, ctx:PLCParser.VarDeclStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLCParser#ExprStmt.
    def visitExprStmt(self, ctx:PLCParser.ExprStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLCParser#ReadStmt.
    def visitReadStmt(self, ctx:PLCParser.ReadStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLCParser#WriteStmt.
    def visitWriteStmt(self, ctx:PLCParser.WriteStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLCParser#BlockStmt.
    def visitBlockStmt(self, ctx:PLCParser.BlockStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLCParser#IfStmt.
    def visitIfStmt(self, ctx:PLCParser.IfStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLCParser#WhileStmt.
    def visitWhileStmt(self, ctx:PLCParser.WhileStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLCParser#MulExpr.
    def visitMulExpr(self, ctx:PLCParser.MulExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLCParser#AndExpr.
    def visitAndExpr(self, ctx:PLCParser.AndExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLCParser#BoolLitExpr.
    def visitBoolLitExpr(self, ctx:PLCParser.BoolLitExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLCParser#RelExpr.
    def visitRelExpr(self, ctx:PLCParser.RelExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLCParser#StringLitExpr.
    def visitStringLitExpr(self, ctx:PLCParser.StringLitExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLCParser#AddExpr.
    def visitAddExpr(self, ctx:PLCParser.AddExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLCParser#OrExpr.
    def visitOrExpr(self, ctx:PLCParser.OrExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLCParser#AssignExpr.
    def visitAssignExpr(self, ctx:PLCParser.AssignExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLCParser#IntLitExpr.
    def visitIntLitExpr(self, ctx:PLCParser.IntLitExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLCParser#EqExpr.
    def visitEqExpr(self, ctx:PLCParser.EqExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLCParser#FloatLitExpr.
    def visitFloatLitExpr(self, ctx:PLCParser.FloatLitExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLCParser#VarExpr.
    def visitVarExpr(self, ctx:PLCParser.VarExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLCParser#NotExpr.
    def visitNotExpr(self, ctx:PLCParser.NotExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLCParser#UminusExpr.
    def visitUminusExpr(self, ctx:PLCParser.UminusExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLCParser#ParenExpr.
    def visitParenExpr(self, ctx:PLCParser.ParenExprContext):
        return self.visitChildren(ctx)



del PLCParser