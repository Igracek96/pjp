grammar PLC;

// ---- Parser rules ----

program : statement* EOF ;

statement
    : ';'                                                              # EmptyStmt
    | varType=('int'|'float'|'bool'|'string') ID (',' ID)* ';'        # VarDeclStmt
    | expr ';'                                                         # ExprStmt
    | 'read' ID (',' ID)* ';'                                         # ReadStmt
    | 'write' expr (',' expr)* ';'                                    # WriteStmt
    | '{' statement* '}'                                               # BlockStmt
    | 'if' '(' expr ')' statement ('else' statement)?                  # IfStmt
    | 'while' '(' expr ')' statement                                   # WhileStmt
    ;

// In ANTLR4, alternatives listed FIRST have the HIGHEST precedence.
// Binary operators are ordered from highest to lowest precedence.
// Non-left-recursive alternatives (unary, atoms) are the base case
// and always have the highest effective precedence.
expr
    : expr op=('*'|'/'|'%') expr        # MulExpr
    | expr op=('+'|'-'|'.') expr        # AddExpr
    | expr op=('<'|'>') expr            # RelExpr
    | expr op=('=='|'!=') expr          # EqExpr
    | expr '&&' expr                    # AndExpr
    | expr '||' expr                    # OrExpr
    | <assoc=right> expr '=' expr       # AssignExpr
    | '!' expr                          # NotExpr
    | '-' expr                          # UminusExpr
    | '(' expr ')'                      # ParenExpr
    | INT                               # IntLitExpr
    | FLOAT                             # FloatLitExpr
    | BOOL                              # BoolLitExpr
    | STRING                            # StringLitExpr
    | ID                                # VarExpr
    ;

// ---- Lexer rules ----

BOOL   : 'true' | 'false' ;
FLOAT  : [0-9]+ '.' [0-9]+ ;
INT    : [0-9]+ ;
STRING : '"' ( '\\' . | ~["\\\r\n] )* '"' ;
ID     : [a-zA-Z] [a-zA-Z0-9]* ;

COMMENT : '//' ~[\r\n]* -> skip ;
WS      : [ \t\r\n]+ -> skip ;
