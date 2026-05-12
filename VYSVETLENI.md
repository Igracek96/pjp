# Jak funguje celý kompilátor – vysvětlení na příkladu

Ukážeme si, co se děje s tímto programem:

```
int a;
a = 3 + 4 * 2;
write a;
```

Program deklaruje proměnnou `a`, spočítá `3 + 4 * 2 = 11` a vypíše `11`.

Kód projde **6 fází**. Každá fáze vezme výstup předchozí a předá ho dál:

```
zdrojový text
    ↓  (main.py)
[1] ANTLR Lexer     →  tokeny (kousky textu)
    ↓
[2] ANTLR Parser    →  parse tree (strom podle gramatiky)
    ↓
[3] ASTBuilder      →  AST (náš vlastní strom)
    ↓
[4] TypeChecker     →  AST s doplněnými typy
    ↓
[5] CodeGen         →  instrukce zásobníkového stroje
    ↓
[6] Interpreter     →  výstup programu: 11
```

---

## Fáze 1 – ANTLR Lexer (PLCLexer.py)

**Co dělá:** Rozseká text na tokeny (= nejmenší kousky s významem).

**Vstup:** text `int a;\na = 3 + 4 * 2;\nwrite a;\n`

**Výstup:** seznam tokenů:

```
Token  1:  type=int       text="int"
Token  2:  type=ID        text="a"
Token  3:  type=;         text=";"
Token  4:  type=ID        text="a"
Token  5:  type==         text="="
Token  6:  type=INT       text="3"
Token  7:  type=+         text="+"
Token  8:  type=INT       text="4"
Token  9:  type=*         text="*"
Token 10:  type=INT       text="2"
Token 11:  type=;         text=";"
Token 12:  type=write     text="write"
Token 13:  type=ID        text="a"
Token 14:  type=;         text=";"
Token 15:  type=EOF       text=""
```

Mezery a konce řádků se zahodí (pravidlo `WS : [ \t\r\n]+ -> skip` v PLC.g4).

**Kde v kódu:**

```
main.py řádek 42-43:
    input_stream = InputStream(source)
    lexer = PLCLexer(input_stream)
```

PLCLexer je vygenerovaný ANTLR. Pravidla podle kterých rozpoznává tokeny
jsou v PLC.g4 (lexerová pravidla = VELKÁ PÍSMENA):

```
INT    : [0-9]+ ;              ← "3", "4", "2"
ID     : [a-zA-Z] [a-zA-Z0-9]* ;   ← "a"
WS     : [ \t\r\n]+ -> skip ;      ← mezery se zahodí
```

Klíčová slova (`int`, `write`) se rozpoznávají automaticky – ANTLR je
porovná s doslovnými řetězci v gramatice (`'int'`, `'write'`).

---

## Fáze 2 – ANTLR Parser (PLCParser.py)

**Co dělá:** Z tokenů postaví parse tree (strom) podle gramatiky.

**Vstup:** tokeny z fáze 1

**Výstup:** parse tree:

```
Program
├── VarDeclStmt: "int" "a" ";"
├── ExprStmt: expr ";"
│   └── AssignExpr: expr "=" expr
│       ├── VarExpr: "a"
│       └── AddExpr: expr "+" expr
│           ├── IntLitExpr: "3"
│           └── MulExpr: expr "*" expr
│               ├── IntLitExpr: "4"
│               └── IntLitExpr: "2"
└── WriteStmt: "write" expr ";"
    └── VarExpr: "a"
```

**Klíčový moment – precedence (priorita operátorů):**

Výraz `3 + 4 * 2` by se mohl parsovat dvěma způsoby:
- `(3 + 4) * 2 = 14`  ← ŠPATNĚ
- `3 + (4 * 2) = 11`  ← SPRÁVNĚ

Parser to řeší díky pořadí alternativ v PLC.g4:

```
expr
    : expr op=('*'|'/'|'%') expr     # MulExpr    ← 1. = NEJVYŠŠÍ priorita
    | expr op=('+'|'-'|'.') expr     # AddExpr    ← 2. = nižší priorita
    | ...
```

V ANTLR4 platí: **alternativa uvedená DŘÍVE má VYŠŠÍ precedenci**.
`MulExpr` je před `AddExpr`, takže `*` se "váže těsněji" než `+`.

Proto se `3 + 4 * 2` parsuje jako `3 + (4 * 2)`:
- Nejdřív se `4 * 2` spojí do MulExpr
- Pak se `3 + [MulExpr]` spojí do AddExpr

**Kde v kódu:**

```
main.py řádek 48-54:
    token_stream = CommonTokenStream(lexer)
    parser = PLCParser(token_stream)
    tree = parser.program()
```

---

## Fáze 3 – ASTBuilder (ast_builder.py)

**Co dělá:** Projde parse tree a vytvoří náš vlastní AST
(jednodušší strom bez středníků, závorek, klíčových slov).

**Vstup:** parse tree z fáze 2

**Výstup:** náš AST:

```
Program(statements=[
    VarDecl(var_type="int", names=["a"]),
    ExprStmt(expr=
        Assign(target=Var("a"), value=
            BinOp(op="+",
                left=IntLit(3),
                right=BinOp(op="*",
                    left=IntLit(4),
                    right=IntLit(2)
                )
            )
        )
    ),
    Write(expressions=[Var("a")])
])
```

**Jak to funguje krok za krokem:**

1. ANTLR zavolá `visitProgram` – ten projde všechny statement poduzly:

```python
def visitProgram(self, ctx):
    stmts = [self.visit(s) for s in ctx.statement()]
    return Program(stmts)
```

`ctx.statement()` vrátí seznam 3 statement kontextů.
`self.visit(s)` pro každý zavolá správný `visitXxx`.

2. Pro `int a;` se zavolá `visitVarDeclStmt`:

```python
def visitVarDeclStmt(self, ctx):
    var_type = ctx.varType.text       # → "int"
    names = [tok.getText() for tok in ctx.ID()]   # → ["a"]
    return VarDecl("int", ["a"])
```

3. Pro `a = 3 + 4 * 2;` se zavolá `visitExprStmt`, který zavolá
   `visitAssignExpr`:

```python
def visitAssignExpr(self, ctx):
    target = self.visit(ctx.expr(0))   # → Var("a")
    value = self.visit(ctx.expr(1))    # → BinOp("+", IntLit(3), BinOp("*", ...))
    return Assign(target, value)
```

Při zpracování pravé strany se rekurzivně zavolá:
- `visitAddExpr` → `BinOp("+", left, right)`
  - left: `visitIntLitExpr` → `IntLit(3)`
  - right: `visitMulExpr` → `BinOp("*", left, right)`
    - left: `visitIntLitExpr` → `IntLit(4)`
    - right: `visitIntLitExpr` → `IntLit(2)`

4. Pro `write a;` se zavolá `visitWriteStmt`:

```python
def visitWriteStmt(self, ctx):
    exprs = [self.visit(e) for e in ctx.expr()]   # → [Var("a")]
    return Write(exprs)
```

**Kde v kódu:**

```
main.py řádek 64:
    ast = ASTBuilder().visit(tree)
```

---

## Fáze 4 – TypeChecker (typechecker.py)

**Co dělá:**
1. Zkontroluje, že typy dávají smysl
2. Doplní `.type` na každý uzel AST
3. Vloží `IntToFloat` uzly kde je potřeba konverze

**Vstup:** AST z fáze 3 (bez typů)

**Výstup:** stejný AST, ale s doplněnými typy:

```
Program(statements=[
    VarDecl(var_type="int", names=["a"]),
    ExprStmt(expr=
        Assign(target=Var("a", type="int"), value=
            BinOp(op="+", type="int",
                left=IntLit(3, type="int"),
                right=BinOp(op="*", type="int",
                    left=IntLit(4, type="int"),
                    right=IntLit(2, type="int")
                )
            ),
            type="int"
        )
    ),
    Write(expressions=[Var("a", type="int")])
])
```

**Jak to funguje krok za krokem:**

1. `visit_VarDecl` – zaregistruje proměnnou `a` jako `int` v ScopeManageru:

```python
def visit_VarDecl(self, node):
    for name in node.names:
        self.scope.declare(name, node.var_type)
        # ScopeManager.scopes = [{"a": "int"}]
```

2. `visit_Assign` – zkontroluje přiřazení:

```python
def visit_Assign(self, node):
    # Ověří, že levá strana je proměnná
    target_type = self.scope.lookup("a")     # → "int"
    node.target.type = "int"

    # Rekurzivně zkontroluje pravou stranu
    val_type = self.visit(node.value)        # → "int" (viz níže)

    # Zkontroluje, že typy jsou kompatibilní
    # "int" == "int" → OK
    node.type = "int"
```

3. Kontrola pravé strany `3 + 4 * 2` – rekurze zespodu nahoru:

```
visit_BinOp(op="+")
    ├── visit(left) → visit_IntLit(3) → vrátí "int"
    ├── visit(right) → visit_BinOp(op="*")
    │       ├── visit(left) → visit_IntLit(4) → vrátí "int"
    │       ├── visit(right) → visit_IntLit(2) → vrátí "int"
    │       └── "int" + "int" → node.type = "int", vrátí "int"
    └── "int" + "int" → node.type = "int", vrátí "int"
```

Každý `visit_IntLit` vrátí `"int"`.
`visit_BinOp` pro `*`: oba operandy jsou `"int"` → výsledek je `"int"`.
`visit_BinOp` pro `+`: oba operandy jsou `"int"` → výsledek je `"int"`.

Kdybychom měli `3 + 4.0 * 2`, TypeChecker by:
- Zjistil, že `4.0` je float a `2` je int
- Vložil `IntToFloat(IntLit(2))` místo `IntLit(2)`
- Výsledek `*` by byl float, pak by vložil `IntToFloat(IntLit(3))` v `+`

**Kde v kódu:**

```
main.py řádek 67:
    TypeChecker().check(ast)
```

---

## Fáze 5 – CodeGen (codegen.py)

**Co dělá:** Projde typovaný AST a vygeneruje instrukce zásobníkového stroje.

**Vstup:** typovaný AST z fáze 4

**Výstup:** seznam instrukcí (stringů):

```
push I 0       ← [1] deklarace: int a;
save a         ← [1]
push I 3       ← [2] pravá strana přiřazení: 3 + 4 * 2
push I 4       ← [2]
push I 2       ← [2]
mul I          ← [2] 4 * 2
add I          ← [2] 3 + (výsledek)
save a         ← [2] uloží výsledek do a
load a         ← [2] znovu načte (= je výraz, vrací hodnotu)
pop            ← [2] ExprStmt: zahodí hodnotu
load a         ← [3] write a;
print 1        ← [3]
```

**Jak to funguje krok za krokem:**

1. `visit_VarDecl("int", ["a"])` – pushne výchozí hodnotu a uloží:

```python
def visit_VarDecl(self, node):
    for name in node.names:
        self.emit(DEFAULTS[node.var_type])   # → "push I 0"
        self.emit(f"save {name}")            # → "save a"
```

2. `visit_ExprStmt` – zpracuje výraz a zahodí výsledek:

```python
def visit_ExprStmt(self, node):
    self.visit(node.expr)    # vygeneruje kód pro přiřazení
    self.emit("pop")         # zahodí výsledek (přiřazení vrací hodnotu)
```

3. `visit_Assign` – uloží hodnotu a nechá ji na zásobníku:

```python
def visit_Assign(self, node):
    self.visit(node.value)                # vygeneruje kód pro 3 + 4 * 2
    self.emit(f"save {node.target.name}") # → "save a"
    self.emit(f"load {node.target.name}") # → "load a" (= je výraz!)
```

Proč `save` a hned `load`? Protože `=` je **výraz** – vrací hodnotu.
To umožňuje řetězení: `a = b = 5` (vnitřní `b = 5` nechá 5 na zásobníku).
`ExprStmt` pak přidá `pop`, protože jako příkaz tu hodnotu nepotřebujeme.

4. Generování kódu pro `3 + 4 * 2` – rekurze:

```python
visit_BinOp(op="+")                    # AddExpr
    visit(left) → visit_IntLit(3)     # emit: "push I 3"
    visit(right) → visit_BinOp(op="*") # MulExpr
        visit(left) → visit_IntLit(4)  # emit: "push I 4"
        visit(right) → visit_IntLit(2) # emit: "push I 2"
        emit: "mul I"                  # ← 4 * 2
    emit: "add I"                      # ← 3 + (výsledek mul)
```

Pořadí je důležité! Nejdřív se vygeneruje kód pro **listy stromu**
(IntLit uzly), pak operace nad nimi. Strom se prochází **do hloubky**:

```
            +           Výsledné instrukce (v pořadí generování):
           / \
          3   *         1. push I 3     (navštíví levý list +)
             / \        2. push I 4     (navštíví levý list *)
            4   2       3. push I 2     (navštíví pravý list *)
                        4. mul I        (vrátí se do *)
                        5. add I        (vrátí se do +)
```

5. `visit_Write` – pushne hodnoty a vytiskne:

```python
def visit_Write(self, node):
    for expr in node.expressions:
        self.visit(expr)                          # → "load a"
    self.emit(f"print {len(node.expressions)}")   # → "print 1"
```

**Kde v kódu:**

```
main.py řádek 70:
    return CodeGen().generate(ast)
```

---

## Fáze 6 – Interpreter (interpreter.py)

**Co dělá:** Simuluje zásobníkový stroj – vykonává instrukce jednu po druhé.

**Vstup:** instrukce z fáze 5

**Simulace krok za krokem:**

Zásobník začíná prázdný `[]`, proměnné prázdné `{}`.

```
Instrukce      │ Zásobník      │ Proměnné    │ Co se děje
───────────────┼───────────────┼─────────────┼──────────────────────
push I 0       │ [0]           │ {}          │ pushne 0 (int)
save a         │ []            │ {a: 0}      │ popne 0, uloží do a
push I 3       │ [3]           │ {a: 0}      │ pushne 3
push I 4       │ [3, 4]        │ {a: 0}      │ pushne 4
push I 2       │ [3, 4, 2]     │ {a: 0}      │ pushne 2
mul I          │ [3, 8]        │ {a: 0}      │ popne 2 a 4, pushne 4*2=8
add I          │ [11]          │ {a: 0}      │ popne 8 a 3, pushne 3+8=11
save a         │ []            │ {a: 11}     │ popne 11, uloží do a
load a         │ [11]          │ {a: 11}     │ pushne hodnotu a (11)
pop            │ []            │ {a: 11}     │ zahodí 11 (ExprStmt)
load a         │ [11]          │ {a: 11}     │ pushne hodnotu a (11)
print 1        │ []            │ {a: 11}     │ popne 1 hodnotu, vytiskne: 11
```

**Výstup programu:** `11`

**Klíčové detaily:**

`mul I` – vezme DVĚ hodnoty ze zásobníku:
```python
b, a = self.stack.pop(), self.stack.pop()   # b=2, a=4
self.stack.append(a * b)                    # 4 * 2 = 8
```
`b` (navrchu) přišlo jako **druhé** (push 2 po push 4).
Pořadí `b, a = pop(), pop()` je důležité pro `sub` a `div` (není komutativní).

`save a` – popne hodnotu a uloží do slovníku:
```python
self.variables["a"] = self.stack.pop()
```

`print 1` – vezme posledních N hodnot a vytiskne:
```python
n = 1
values = self.stack[-1:]    # [11]
del self.stack[-1:]          # zásobník prázdný
for val in values:
    self._print_value(val)   # vytiskne "11"
print()                      # newline na konci
```

**Kde v kódu:**

```
main.py řádek 101:
    Interpreter(instructions).run()
```

---

## Shrnutí celé cesty

```
"int a;\na = 3 + 4 * 2;\nwrite a;\n"

  [Lexer]   →  int  a  ;  a  =  3  +  4  *  2  ;  write  a  ;  EOF

  [Parser]  →  Program
               ├── VarDeclStmt(int, a)
               ├── ExprStmt(AssignExpr(a, AddExpr(3, MulExpr(4, 2))))
               └── WriteStmt(a)

  [ASTBuilder] → Program
                  ├── VarDecl("int", ["a"])
                  ├── ExprStmt(Assign(Var("a"), BinOp("+", 3, BinOp("*", 4, 2))))
                  └── Write([Var("a")])

  [TypeChecker] → (stejný strom, ale .type="int" na všech uzlech)

  [CodeGen]  →  push I 0 / save a / push I 3 / push I 4 / push I 2 /
                mul I / add I / save a / load a / pop / load a / print 1

  [Interpreter] →  11
```

---

## Bonusový příklad – co by se změnilo s float?

Kdyby program byl `float a; a = 3 + 4.0 * 2;`:

**TypeChecker** by zjistil:
- `4.0` je float, `2` je int → vloží `IntToFloat(IntLit(2))`, výsledek `*` je float
- `3` je int, výsledek `*` je float → vloží `IntToFloat(IntLit(3))`, výsledek `+` je float

**CodeGen** by vygeneroval:
```
push F 0.0     ← float default
save a
push I 3
itof           ← IntToFloat: převede 3 na 3.0
push F 4.0
push I 2
itof           ← IntToFloat: převede 2 na 2.0
mul F          ← float násobení: 4.0 * 2.0 = 8.0
add F          ← float sčítání: 3.0 + 8.0 = 11.0
save a
load a
pop
load a
print 1
```

**Výstup:** `11.0`

`itof` je instrukce interpretu, která popne int a pushne float:
```python
elif op == "itof":
    self.stack.append(float(self.stack.pop()))   # int → float
```
