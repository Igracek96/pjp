# Generated from PLC.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,36,117,2,0,7,0,2,1,7,1,2,2,7,2,1,0,5,0,8,8,0,10,0,12,0,11,9,
        0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,5,1,20,8,1,10,1,12,1,23,9,1,1,1,1,
        1,1,1,1,1,1,1,1,1,1,1,1,1,5,1,33,8,1,10,1,12,1,36,9,1,1,1,1,1,1,
        1,1,1,1,1,5,1,43,8,1,10,1,12,1,46,9,1,1,1,1,1,1,1,1,1,5,1,52,8,1,
        10,1,12,1,55,9,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,1,65,8,1,1,1,
        1,1,1,1,1,1,1,1,1,1,3,1,73,8,1,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,
        2,1,2,1,2,1,2,1,2,1,2,3,2,89,8,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,
        1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,5,2,112,8,2,
        10,2,12,2,115,9,2,1,2,0,1,4,3,0,2,4,0,5,1,0,2,5,1,0,16,18,1,0,19,
        21,1,0,22,23,1,0,24,25,140,0,9,1,0,0,0,2,72,1,0,0,0,4,88,1,0,0,0,
        6,8,3,2,1,0,7,6,1,0,0,0,8,11,1,0,0,0,9,7,1,0,0,0,9,10,1,0,0,0,10,
        12,1,0,0,0,11,9,1,0,0,0,12,13,5,0,0,1,13,1,1,0,0,0,14,73,5,1,0,0,
        15,16,7,0,0,0,16,21,5,34,0,0,17,18,5,6,0,0,18,20,5,34,0,0,19,17,
        1,0,0,0,20,23,1,0,0,0,21,19,1,0,0,0,21,22,1,0,0,0,22,24,1,0,0,0,
        23,21,1,0,0,0,24,73,5,1,0,0,25,26,3,4,2,0,26,27,5,1,0,0,27,73,1,
        0,0,0,28,29,5,7,0,0,29,34,5,34,0,0,30,31,5,6,0,0,31,33,5,34,0,0,
        32,30,1,0,0,0,33,36,1,0,0,0,34,32,1,0,0,0,34,35,1,0,0,0,35,37,1,
        0,0,0,36,34,1,0,0,0,37,73,5,1,0,0,38,39,5,8,0,0,39,44,3,4,2,0,40,
        41,5,6,0,0,41,43,3,4,2,0,42,40,1,0,0,0,43,46,1,0,0,0,44,42,1,0,0,
        0,44,45,1,0,0,0,45,47,1,0,0,0,46,44,1,0,0,0,47,48,5,1,0,0,48,73,
        1,0,0,0,49,53,5,9,0,0,50,52,3,2,1,0,51,50,1,0,0,0,52,55,1,0,0,0,
        53,51,1,0,0,0,53,54,1,0,0,0,54,56,1,0,0,0,55,53,1,0,0,0,56,73,5,
        10,0,0,57,58,5,11,0,0,58,59,5,12,0,0,59,60,3,4,2,0,60,61,5,13,0,
        0,61,64,3,2,1,0,62,63,5,14,0,0,63,65,3,2,1,0,64,62,1,0,0,0,64,65,
        1,0,0,0,65,73,1,0,0,0,66,67,5,15,0,0,67,68,5,12,0,0,68,69,3,4,2,
        0,69,70,5,13,0,0,70,71,3,2,1,0,71,73,1,0,0,0,72,14,1,0,0,0,72,15,
        1,0,0,0,72,25,1,0,0,0,72,28,1,0,0,0,72,38,1,0,0,0,72,49,1,0,0,0,
        72,57,1,0,0,0,72,66,1,0,0,0,73,3,1,0,0,0,74,75,6,2,-1,0,75,76,5,
        29,0,0,76,89,3,4,2,8,77,78,5,20,0,0,78,89,3,4,2,7,79,80,5,12,0,0,
        80,81,3,4,2,0,81,82,5,13,0,0,82,89,1,0,0,0,83,89,5,32,0,0,84,89,
        5,31,0,0,85,89,5,30,0,0,86,89,5,33,0,0,87,89,5,34,0,0,88,74,1,0,
        0,0,88,77,1,0,0,0,88,79,1,0,0,0,88,83,1,0,0,0,88,84,1,0,0,0,88,85,
        1,0,0,0,88,86,1,0,0,0,88,87,1,0,0,0,89,113,1,0,0,0,90,91,10,15,0,
        0,91,92,7,1,0,0,92,112,3,4,2,16,93,94,10,14,0,0,94,95,7,2,0,0,95,
        112,3,4,2,15,96,97,10,13,0,0,97,98,7,3,0,0,98,112,3,4,2,14,99,100,
        10,12,0,0,100,101,7,4,0,0,101,112,3,4,2,13,102,103,10,11,0,0,103,
        104,5,26,0,0,104,112,3,4,2,12,105,106,10,10,0,0,106,107,5,27,0,0,
        107,112,3,4,2,11,108,109,10,9,0,0,109,110,5,28,0,0,110,112,3,4,2,
        9,111,90,1,0,0,0,111,93,1,0,0,0,111,96,1,0,0,0,111,99,1,0,0,0,111,
        102,1,0,0,0,111,105,1,0,0,0,111,108,1,0,0,0,112,115,1,0,0,0,113,
        111,1,0,0,0,113,114,1,0,0,0,114,5,1,0,0,0,115,113,1,0,0,0,10,9,21,
        34,44,53,64,72,88,111,113
    ]

class PLCParser ( Parser ):

    grammarFileName = "PLC.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "';'", "'int'", "'float'", "'bool'", "'string'", 
                     "','", "'read'", "'write'", "'{'", "'}'", "'if'", "'('", 
                     "')'", "'else'", "'while'", "'*'", "'/'", "'%'", "'+'", 
                     "'-'", "'.'", "'<'", "'>'", "'=='", "'!='", "'&&'", 
                     "'||'", "'='", "'!'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "BOOL", "FLOAT", "INT", 
                      "STRING", "ID", "COMMENT", "WS" ]

    RULE_program = 0
    RULE_statement = 1
    RULE_expr = 2

    ruleNames =  [ "program", "statement", "expr" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    T__9=10
    T__10=11
    T__11=12
    T__12=13
    T__13=14
    T__14=15
    T__15=16
    T__16=17
    T__17=18
    T__18=19
    T__19=20
    T__20=21
    T__21=22
    T__22=23
    T__23=24
    T__24=25
    T__25=26
    T__26=27
    T__27=28
    T__28=29
    BOOL=30
    FLOAT=31
    INT=32
    STRING=33
    ID=34
    COMMENT=35
    WS=36

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(PLCParser.EOF, 0)

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PLCParser.StatementContext)
            else:
                return self.getTypedRuleContext(PLCParser.StatementContext,i)


        def getRuleIndex(self):
            return PLCParser.RULE_program

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProgram" ):
                return visitor.visitProgram(self)
            else:
                return visitor.visitChildren(self)




    def program(self):

        localctx = PLCParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 9
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 33823955902) != 0):
                self.state = 6
                self.statement()
                self.state = 11
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 12
            self.match(PLCParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return PLCParser.RULE_statement

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class IfStmtContext(StatementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PLCParser.StatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(PLCParser.ExprContext,0)

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PLCParser.StatementContext)
            else:
                return self.getTypedRuleContext(PLCParser.StatementContext,i)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIfStmt" ):
                return visitor.visitIfStmt(self)
            else:
                return visitor.visitChildren(self)


    class ExprStmtContext(StatementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PLCParser.StatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(PLCParser.ExprContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExprStmt" ):
                return visitor.visitExprStmt(self)
            else:
                return visitor.visitChildren(self)


    class WhileStmtContext(StatementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PLCParser.StatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(PLCParser.ExprContext,0)

        def statement(self):
            return self.getTypedRuleContext(PLCParser.StatementContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWhileStmt" ):
                return visitor.visitWhileStmt(self)
            else:
                return visitor.visitChildren(self)


    class VarDeclStmtContext(StatementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PLCParser.StatementContext
            super().__init__(parser)
            self.varType = None # Token
            self.copyFrom(ctx)

        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(PLCParser.ID)
            else:
                return self.getToken(PLCParser.ID, i)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVarDeclStmt" ):
                return visitor.visitVarDeclStmt(self)
            else:
                return visitor.visitChildren(self)


    class BlockStmtContext(StatementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PLCParser.StatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PLCParser.StatementContext)
            else:
                return self.getTypedRuleContext(PLCParser.StatementContext,i)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBlockStmt" ):
                return visitor.visitBlockStmt(self)
            else:
                return visitor.visitChildren(self)


    class WriteStmtContext(StatementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PLCParser.StatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PLCParser.ExprContext)
            else:
                return self.getTypedRuleContext(PLCParser.ExprContext,i)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWriteStmt" ):
                return visitor.visitWriteStmt(self)
            else:
                return visitor.visitChildren(self)


    class ReadStmtContext(StatementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PLCParser.StatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(PLCParser.ID)
            else:
                return self.getToken(PLCParser.ID, i)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReadStmt" ):
                return visitor.visitReadStmt(self)
            else:
                return visitor.visitChildren(self)


    class EmptyStmtContext(StatementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PLCParser.StatementContext
            super().__init__(parser)
            self.copyFrom(ctx)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEmptyStmt" ):
                return visitor.visitEmptyStmt(self)
            else:
                return visitor.visitChildren(self)



    def statement(self):

        localctx = PLCParser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_statement)
        self._la = 0 # Token type
        try:
            self.state = 72
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1]:
                localctx = PLCParser.EmptyStmtContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 14
                self.match(PLCParser.T__0)
                pass
            elif token in [2, 3, 4, 5]:
                localctx = PLCParser.VarDeclStmtContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 15
                localctx.varType = self._input.LT(1)
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 60) != 0)):
                    localctx.varType = self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 16
                self.match(PLCParser.ID)
                self.state = 21
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==6:
                    self.state = 17
                    self.match(PLCParser.T__5)
                    self.state = 18
                    self.match(PLCParser.ID)
                    self.state = 23
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 24
                self.match(PLCParser.T__0)
                pass
            elif token in [12, 20, 29, 30, 31, 32, 33, 34]:
                localctx = PLCParser.ExprStmtContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 25
                self.expr(0)
                self.state = 26
                self.match(PLCParser.T__0)
                pass
            elif token in [7]:
                localctx = PLCParser.ReadStmtContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 28
                self.match(PLCParser.T__6)
                self.state = 29
                self.match(PLCParser.ID)
                self.state = 34
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==6:
                    self.state = 30
                    self.match(PLCParser.T__5)
                    self.state = 31
                    self.match(PLCParser.ID)
                    self.state = 36
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 37
                self.match(PLCParser.T__0)
                pass
            elif token in [8]:
                localctx = PLCParser.WriteStmtContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 38
                self.match(PLCParser.T__7)
                self.state = 39
                self.expr(0)
                self.state = 44
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==6:
                    self.state = 40
                    self.match(PLCParser.T__5)
                    self.state = 41
                    self.expr(0)
                    self.state = 46
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 47
                self.match(PLCParser.T__0)
                pass
            elif token in [9]:
                localctx = PLCParser.BlockStmtContext(self, localctx)
                self.enterOuterAlt(localctx, 6)
                self.state = 49
                self.match(PLCParser.T__8)
                self.state = 53
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while (((_la) & ~0x3f) == 0 and ((1 << _la) & 33823955902) != 0):
                    self.state = 50
                    self.statement()
                    self.state = 55
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 56
                self.match(PLCParser.T__9)
                pass
            elif token in [11]:
                localctx = PLCParser.IfStmtContext(self, localctx)
                self.enterOuterAlt(localctx, 7)
                self.state = 57
                self.match(PLCParser.T__10)
                self.state = 58
                self.match(PLCParser.T__11)
                self.state = 59
                self.expr(0)
                self.state = 60
                self.match(PLCParser.T__12)
                self.state = 61
                self.statement()
                self.state = 64
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,5,self._ctx)
                if la_ == 1:
                    self.state = 62
                    self.match(PLCParser.T__13)
                    self.state = 63
                    self.statement()


                pass
            elif token in [15]:
                localctx = PLCParser.WhileStmtContext(self, localctx)
                self.enterOuterAlt(localctx, 8)
                self.state = 66
                self.match(PLCParser.T__14)
                self.state = 67
                self.match(PLCParser.T__11)
                self.state = 68
                self.expr(0)
                self.state = 69
                self.match(PLCParser.T__12)
                self.state = 70
                self.statement()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return PLCParser.RULE_expr

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class MulExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PLCParser.ExprContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PLCParser.ExprContext)
            else:
                return self.getTypedRuleContext(PLCParser.ExprContext,i)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMulExpr" ):
                return visitor.visitMulExpr(self)
            else:
                return visitor.visitChildren(self)


    class AndExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PLCParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PLCParser.ExprContext)
            else:
                return self.getTypedRuleContext(PLCParser.ExprContext,i)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAndExpr" ):
                return visitor.visitAndExpr(self)
            else:
                return visitor.visitChildren(self)


    class BoolLitExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PLCParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def BOOL(self):
            return self.getToken(PLCParser.BOOL, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBoolLitExpr" ):
                return visitor.visitBoolLitExpr(self)
            else:
                return visitor.visitChildren(self)


    class RelExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PLCParser.ExprContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PLCParser.ExprContext)
            else:
                return self.getTypedRuleContext(PLCParser.ExprContext,i)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRelExpr" ):
                return visitor.visitRelExpr(self)
            else:
                return visitor.visitChildren(self)


    class StringLitExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PLCParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def STRING(self):
            return self.getToken(PLCParser.STRING, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStringLitExpr" ):
                return visitor.visitStringLitExpr(self)
            else:
                return visitor.visitChildren(self)


    class AddExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PLCParser.ExprContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PLCParser.ExprContext)
            else:
                return self.getTypedRuleContext(PLCParser.ExprContext,i)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAddExpr" ):
                return visitor.visitAddExpr(self)
            else:
                return visitor.visitChildren(self)


    class OrExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PLCParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PLCParser.ExprContext)
            else:
                return self.getTypedRuleContext(PLCParser.ExprContext,i)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOrExpr" ):
                return visitor.visitOrExpr(self)
            else:
                return visitor.visitChildren(self)


    class AssignExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PLCParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PLCParser.ExprContext)
            else:
                return self.getTypedRuleContext(PLCParser.ExprContext,i)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAssignExpr" ):
                return visitor.visitAssignExpr(self)
            else:
                return visitor.visitChildren(self)


    class IntLitExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PLCParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def INT(self):
            return self.getToken(PLCParser.INT, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIntLitExpr" ):
                return visitor.visitIntLitExpr(self)
            else:
                return visitor.visitChildren(self)


    class EqExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PLCParser.ExprContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PLCParser.ExprContext)
            else:
                return self.getTypedRuleContext(PLCParser.ExprContext,i)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEqExpr" ):
                return visitor.visitEqExpr(self)
            else:
                return visitor.visitChildren(self)


    class FloatLitExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PLCParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def FLOAT(self):
            return self.getToken(PLCParser.FLOAT, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFloatLitExpr" ):
                return visitor.visitFloatLitExpr(self)
            else:
                return visitor.visitChildren(self)


    class VarExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PLCParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(PLCParser.ID, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVarExpr" ):
                return visitor.visitVarExpr(self)
            else:
                return visitor.visitChildren(self)


    class NotExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PLCParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(PLCParser.ExprContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNotExpr" ):
                return visitor.visitNotExpr(self)
            else:
                return visitor.visitChildren(self)


    class UminusExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PLCParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(PLCParser.ExprContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUminusExpr" ):
                return visitor.visitUminusExpr(self)
            else:
                return visitor.visitChildren(self)


    class ParenExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PLCParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(PLCParser.ExprContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParenExpr" ):
                return visitor.visitParenExpr(self)
            else:
                return visitor.visitChildren(self)



    def expr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = PLCParser.ExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 4
        self.enterRecursionRule(localctx, 4, self.RULE_expr, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 88
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [29]:
                localctx = PLCParser.NotExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 75
                self.match(PLCParser.T__28)
                self.state = 76
                self.expr(8)
                pass
            elif token in [20]:
                localctx = PLCParser.UminusExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 77
                self.match(PLCParser.T__19)
                self.state = 78
                self.expr(7)
                pass
            elif token in [12]:
                localctx = PLCParser.ParenExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 79
                self.match(PLCParser.T__11)
                self.state = 80
                self.expr(0)
                self.state = 81
                self.match(PLCParser.T__12)
                pass
            elif token in [32]:
                localctx = PLCParser.IntLitExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 83
                self.match(PLCParser.INT)
                pass
            elif token in [31]:
                localctx = PLCParser.FloatLitExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 84
                self.match(PLCParser.FLOAT)
                pass
            elif token in [30]:
                localctx = PLCParser.BoolLitExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 85
                self.match(PLCParser.BOOL)
                pass
            elif token in [33]:
                localctx = PLCParser.StringLitExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 86
                self.match(PLCParser.STRING)
                pass
            elif token in [34]:
                localctx = PLCParser.VarExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 87
                self.match(PLCParser.ID)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 113
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,9,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 111
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,8,self._ctx)
                    if la_ == 1:
                        localctx = PLCParser.MulExprContext(self, PLCParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 90
                        if not self.precpred(self._ctx, 15):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 15)")
                        self.state = 91
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 458752) != 0)):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 92
                        self.expr(16)
                        pass

                    elif la_ == 2:
                        localctx = PLCParser.AddExprContext(self, PLCParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 93
                        if not self.precpred(self._ctx, 14):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 14)")
                        self.state = 94
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 3670016) != 0)):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 95
                        self.expr(15)
                        pass

                    elif la_ == 3:
                        localctx = PLCParser.RelExprContext(self, PLCParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 96
                        if not self.precpred(self._ctx, 13):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 13)")
                        self.state = 97
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==22 or _la==23):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 98
                        self.expr(14)
                        pass

                    elif la_ == 4:
                        localctx = PLCParser.EqExprContext(self, PLCParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 99
                        if not self.precpred(self._ctx, 12):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 12)")
                        self.state = 100
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==24 or _la==25):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 101
                        self.expr(13)
                        pass

                    elif la_ == 5:
                        localctx = PLCParser.AndExprContext(self, PLCParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 102
                        if not self.precpred(self._ctx, 11):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 11)")
                        self.state = 103
                        self.match(PLCParser.T__25)
                        self.state = 104
                        self.expr(12)
                        pass

                    elif la_ == 6:
                        localctx = PLCParser.OrExprContext(self, PLCParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 105
                        if not self.precpred(self._ctx, 10):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 10)")
                        self.state = 106
                        self.match(PLCParser.T__26)
                        self.state = 107
                        self.expr(11)
                        pass

                    elif la_ == 7:
                        localctx = PLCParser.AssignExprContext(self, PLCParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 108
                        if not self.precpred(self._ctx, 9):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 9)")
                        self.state = 109
                        self.match(PLCParser.T__27)
                        self.state = 110
                        self.expr(9)
                        pass

             
                self.state = 115
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,9,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[2] = self.expr_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expr_sempred(self, localctx:ExprContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 15)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 14)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 13)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 12)
         

            if predIndex == 4:
                return self.precpred(self._ctx, 11)
         

            if predIndex == 5:
                return self.precpred(self._ctx, 10)
         

            if predIndex == 6:
                return self.precpred(self._ctx, 9)
         




