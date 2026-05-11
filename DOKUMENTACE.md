# PLC Compiler – Kompletní dokumentace

Tento dokument vysvětluje celý zdrojový kód projektu od základů.
Je určen pro toho, kdo kód neviděl a nemá hluboké programátorské zkušenosti.

---

## Co projekt dělá

Projekt implementuje **překladač a interpret** jednoduchého programovacího jazyka.
Vezme zdrojový kód (textový soubor) a vykoná ho – vypíše výsledky, načte vstupy atd.

Spuštění:
```
python3 main.py program.plc              # kompilace + spuštění
python3 main.py --compile program.plc    # pouze kompilace → program.ins
python3 main.py --run program.ins        # spuštění souboru instrukcí
```

---

## Jak celý program funguje – výrobní linka

Vstupní text se zpracovává v 5 krocích. Každý krok dělá jednu věc a předá výsledek dalšímu:

```
"write 5+3;"
      ↓
  1. ANTLR LEXER    →  [WRITE] [5] [+] [3] [;]
      ↓               (tokeny – kousky textu s označením)
  2. ANTLR PARSER   →  (write (+ 5 3))
      ↓               (parse tree – strom od ANTLR)
  3. AST BUILDER    →  Write( BinOp(+, 5, 3) )
      ↓               (AST – náš vlastní strom)
  4. TYPECHECKER    →  Write( BinOp(+:int, 5:int, 3:int) )
      ↓               (typy doplněny, chyby odhaleny)
  5. CODEGEN        →  push I 5 / push I 3 / add I / print 1
      ↓               (instrukce zásobníkového stroje)
  6. INTERPRETER    →  8
                      (výstup programu)
```

Každý krok je v samostatném souboru. Tím je kód přehledný a každou část
lze měnit bez dotknutí ostatních.

---

## Jazyk – co umí

### Datové typy
| Typ | Příklad | Výchozí hodnota |
|---|---|---|
| `int` | `42`, `-7` | `0` |
| `float` | `3.14`, `1.5` | `0.0` |
| `bool` | `true`, `false` | `false` |
| `string` | `"hello"` | `""` |

### Příkazy
```
;                          prázdný příkaz
int a, b;                  deklarace proměnných
a = 5;                     přiřazení (výraz jako příkaz)
read a, b;                 čtení ze stdin
write "x=", a;             výpis na stdout (newline za posledním)
{ ... }                    blok příkazů (vlastní scope)
if (podmínka) stmt         podmíněný příkaz
if (podmínka) stmt else s  podmínka s else větví
while (podmínka) stmt      smyčka
```

### Operátory (od nejnižší priority)
| Priorita | Operátor | Typy | Výsledek |
|---|---|---|---|
| 1 (nejnižší) | `=` | pravá asociativita | přiřazení |
| 2 | `\|\|` | bool × bool | bool |
| 3 | `&&` | bool × bool | bool |
| 4 | `==`, `!=` | int/float/string | bool |
| 5 | `<`, `>` | int/float | bool |
| 6 | `+`, `-` | int/float | int/float |
| 6 | `.` | string × string | string |
| 7 | `*`, `/` | int/float | int/float |
| 7 | `%` | int × int | int |
| 8 | `!` | bool | bool |
| 9 (nejvyšší) | unární `-` | int/float | int/float |

### Typová pravidla
- Automatická konverze `int → float` je povolena (např. `1.5 + 3` = `4.5`)
- Konverze `float → int` **není** povolena
- `%` pouze pro int
- `.` (konkatenace) pouze pro string
- `<`, `>` pouze pro int nebo float (ne string, ne bool)
- `==`, `!=` pro int, float, string (ne bool)
- `&&`, `||`, `!` pouze pro bool
- Levá strana `=` musí být proměnná

---

## Zásobníkové instrukce

Překladač generuje instrukce pro zásobníkový stroj. Zásobník funguje jako hromada talířů – vždy přidáváš nebo bereš ze vrchu.

```
push I 3   →  zásobník: [3]
push I 4   →  zásobník: [3, 4]
add I      →  zásobník: [7]        (vezme 3 a 4, pushne 7)
push I 2   →  zásobník: [7, 2]
mul I      →  zásobník: [14]       (vezme 7 a 2, pushne 14)
```

### Přehled instrukcí
| Instrukce | Co dělá |
|---|---|
| `push T x` | Pushne hodnotu x typu T (I/F/B/S) |
| `pop` | Zahodí vrchol zásobníku |
| `load id` | Pushne hodnotu proměnné id |
| `save id` | Popne vrchol a uloží do proměnné id |
| `add T` / `sub T` / `mul T` / `div T` | Aritmetika (T = I nebo F) |
| `mod` | Modulo (int) |
| `uminus T` | Unární mínus |
| `concat` | Konkatenace stringů |
| `and` / `or` / `not` | Boolean operace |
| `gt T` / `lt T` | Větší/menší než |
| `eq T` | Rovnost |
| `itof` | Převod int → float |
| `label n` | Označí pozici číslem n |
| `jmp n` | Nepodmíněný skok na label n |
| `fjmp n` | Skok na label n pokud je vrchol false (a popne ho) |
| `print n` | Vytiskne n hodnot ze zásobníku + newline |
| `read T` | Čte hodnotu typu T ze stdin, pushne |

---

# Soubor `PLC.g4` – ANTLR gramatika

## Co je ANTLR?

ANTLR (ANother Tool for Language Recognition) je generátor parserů. Napíšeme gramatiku
(pravidla jazyka) a ANTLR z ní automaticky vygeneruje lexer a parser v Pythonu.

Výhody oproti ručně psanému lexeru/parseru:
- Gramatika je čitelná a kompaktní
- Změna syntaxe = úprava jednoho souboru (PLC.g4)
- ANTLR řeší precedenci operátorů automaticky

## Struktura gramatiky

Soubor `PLC.g4` je **combined grammar** – obsahuje lexerová i parserová pravidla.

### Parser pravidla (malá písmena)

```
program : statement* EOF ;
```
Program je nula nebo více příkazů, následovaných koncem souboru.

```
statement
    : ';'                                                    # EmptyStmt
    | varType=('int'|'float'|'bool'|'string') ID (',' ID)* ';'  # VarDeclStmt
    | expr ';'                                               # ExprStmt
    | 'read' ID (',' ID)* ';'                                # ReadStmt
    | 'write' expr (',' expr)* ';'                           # WriteStmt
    | '{' statement* '}'                                     # BlockStmt
    | 'if' '(' expr ')' statement ('else' statement)?        # IfStmt
    | 'while' '(' expr ')' statement                         # WhileStmt
    ;
```

Každá alternativa má **label** (text za `#`). ANTLR podle něj vygeneruje
samostatnou visitor metodu – např. `visitVarDeclStmt`, `visitIfStmt` atd.

### Pravidlo pro výrazy – precedence

```
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
```

**Klíčové pravidlo ANTLR4:** alternativa uvedená **dříve** (výše) má **vyšší precedenci**.
Proto `*`/`/`/`%` je na prvním místě (nejvyšší priorita) a `=` přiřazení je poslední
z binárních operátorů (nejnižší priorita).

`<assoc=right>` u přiřazení říká, že `a = b = 5` se parsuje jako `a = (b = 5)`.

Unární operátory (`!`, `-`) a atomy (literály, závorky, proměnné) nejsou
rekurzivní zleva, takže mají vždy nejvyšší efektivní precedenci.

### Lexerová pravidla (velká písmena)

```
BOOL   : 'true' | 'false' ;
FLOAT  : [0-9]+ '.' [0-9]+ ;
INT    : [0-9]+ ;
STRING : '"' ( '\\' . | ~["\\\r\n] )* '"' ;
ID     : [a-zA-Z] [a-zA-Z0-9]* ;
COMMENT : '//' ~[\r\n]* -> skip ;
WS      : [ \t\r\n]+ -> skip ;
```

Pořadí je důležité i u lexeru:
- `BOOL` před `ID` – aby `true`/`false` nebyly rozpoznány jako identifikátory
- `FLOAT` před `INT` – aby `3.14` byl float, ne int `3` + `.` + int `14`
- `-> skip` = tokeny bílých znaků a komentářů se zahodí

### Regenerace

Po úpravě PLC.g4 je nutné znovu vygenerovat Python soubory:
```bash
java -jar antlr-4.13.2-complete.jar -Dlanguage=Python3 -visitor -no-listener PLC.g4
```

Toto vytvoří soubory `PLCLexer.py`, `PLCParser.py` a `PLCVisitor.py`.
Tyto soubory se **needitují ručně** – jsou auto-generované.

---

# Soubor `ast_builder.py` – parse tree → AST

## Proč potřebujeme ASTBuilder?

ANTLR vygeneruje **parse tree** – generický strom, který přesně kopíruje gramatiku.
My ale chceme pracovat s **naším vlastním AST** (definovaným v `ast_nodes.py`),
protože:
1. AST je jednodušší (žádné závorky, středníky, klíčová slova)
2. Zbytek pipeline (typechecker, codegen) pracuje s naším AST
3. Přidání nového příkazu = přidání visitor metody sem + AST uzel

`ASTBuilder` dědí z `PLCVisitor` (vygenerovaný ANTLR) a implementuje
metody pro každý label v gramatice.

## Jak to funguje

ANTLR Visitor pattern: pro každý label v gramatice (např. `#IfStmt`) existuje
metoda `visitIfStmt`. Implementujeme ji tak, aby vrátila odpovídající AST uzel.

```python
class ASTBuilder(PLCVisitor):

    def visitProgram(self, ctx):
        stmts = [self.visit(s) for s in ctx.statement()]
        return Program(stmts)
```

`ctx` je kontext od ANTLR – obsahuje poduzly parse tree.
`ctx.statement()` vrátí seznam všech `statement` poduzlů.
`self.visit(s)` rekurzivně zavolá správný `visitXxx` pro každý podstrom.

## Příkazy

```python
def visitVarDeclStmt(self, ctx):
    var_type = ctx.varType.text          # "int", "float" atd. (pojmenovaný token z gramatiky)
    names = [tok.getText() for tok in ctx.ID()]   # seznam všech ID tokenů
    return VarDecl(var_type, names)
```

`ctx.varType` odpovídá `varType=('int'|'float'|'bool'|'string')` z gramatiky.

```python
def visitIfStmt(self, ctx):
    cond = self.visit(ctx.expr())
    stmts = ctx.statement()              # seznam statement poduzlů (1 nebo 2)
    then_stmt = self.visit(stmts[0])
    else_stmt = self.visit(stmts[1]) if len(stmts) > 1 else None
    return If(cond, then_stmt, else_stmt)
```

If má vždy podmínku (`ctx.expr()`) a 1–2 příkazy (`ctx.statement()` vrací seznam).
Pokud je seznam delší než 1, druhý příkaz je else větev.

```python
def visitWhileStmt(self, ctx):
    cond = self.visit(ctx.expr())
    body = self.visit(ctx.statement())   # jen jeden statement → vrátí kontext přímo
    return While(cond, body)
```

While má jen jeden statement, proto `ctx.statement()` vrátí kontext přímo (ne seznam).

## Výrazy

```python
def visitAssignExpr(self, ctx):
    target = self.visit(ctx.expr(0))     # levá strana (index 0)
    value = self.visit(ctx.expr(1))      # pravá strana (index 1)
    return Assign(target, value)

def visitOrExpr(self, ctx):
    return BinOp("||", self.visit(ctx.expr(0)), self.visit(ctx.expr(1)))

def visitMulExpr(self, ctx):
    return BinOp(ctx.op.text, self.visit(ctx.expr(0)), self.visit(ctx.expr(1)))
```

`ctx.expr(0)` a `ctx.expr(1)` jsou levý a pravý operand.
`ctx.op.text` je text operátoru (díky `op=` pojmenování v gramatice).

## Literály

```python
def visitIntLitExpr(self, ctx):
    return IntLit(int(ctx.INT().getText()))

def visitStringLitExpr(self, ctx):
    raw = ctx.STRING().getText()
    s = raw[1:-1]      # odstraní uvozovky
    s = s.replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"').replace('\\\\', '\\')
    return StrLit(s)
```

ANTLR vrací string **včetně uvozovek** (`"hello"` → `'"hello"'`).
Proto je stripujeme (`raw[1:-1]`) a zpracujeme escape sekvence.

---

# Soubor `ast_nodes.py` – datové kontejnery

## Co je to AST?

AST (Abstract Syntax Tree) je způsob jak uložit **strukturu programu** do paměti.
Kód nelze uložit jen jako text – potřebujeme vědět, co je přiřazení, co je sčítání atd.

Příklad: kód `a = 5 + 3;` se uloží jako strom:
```
Assign
├── target: Var("a")
└── value: BinOp(op="+")
           ├── left:  IntLit(5)
           └── right: IntLit(3)
```

Každý uzel stromu je jedna Python třída v tomto souboru.
Třídy jsou **jen obálky na data** – žádná logika, žádné výpočty.

## Technická poznámka: `@dataclass`

Normálně při vytváření třídy musíš napsat spoustu kódu (`__init__`, `__repr__` atd.).
Dekorátor `@dataclass` to vygeneruje automaticky z deklarace atributů.

```python
@dataclass
class BinOp:
    op: str        # název atributu: typ
    left: Any
    right: Any
    type: Optional[str] = None   # = None znamená: výchozí hodnota je None
```

`Optional[str]` = buď string, nebo `None`. `Any` = cokoliv (libovolný AST uzel).

## Uzly pro celý program a bloky

```python
@dataclass
class Program:
    statements: List[Any]
```
Kořen celého stromu. `statements` = seznam všech příkazů programu.

```python
@dataclass
class Block:
    statements: List[Any]
```
Blok příkazů v složených závorkách `{ ... }`. Vytváří
vlastní **scope** – proměnné deklarované uvnitř zaniknou po opuštění bloku.

```python
@dataclass
class Empty:
    pass
```
Prázdný příkaz – jen samotný středník `;`.

## Uzly pro příkazy

- **VarDecl(var_type, names)** – deklarace: `int a, b;` → `VarDecl("int", ["a", "b"])`
- **If(condition, then_stmt, else_stmt)** – podmíněný příkaz, `else_stmt` je `None` pokud chybí
- **While(condition, body)** – smyčka
- **Read(variables)** – čtení ze stdin: `read a, b;` → `Read([Var("a"), Var("b")])`
- **Write(expressions)** – výpis
- **ExprStmt(expr)** – výraz jako příkaz; CodeGen přidá `pop` po vykonání

## Uzly pro výrazy

- **Assign(target, value)** – přiřazení, `type` doplní TypeChecker
- **BinOp(op, left, right)** – binární operace
- **UnaryOp(op, operand)** – unární `!` nebo `-`
- **IntToFloat(expr)** – vložen TypeCheckerem pro automatickou konverzi int → float
- **Var(name)** – odkaz na proměnnou

## Literály

- **IntLit(value)** – `type = "int"`
- **FloatLit(value)** – `type = "float"`
- **BoolLit(value)** – `type = "bool"`
- **StrLit(value)** – `type = "string"`

Mají `type` nastavený rovnou, protože ho známe z hodnoty.

---

# Soubor `typechecker.py` – kontrola typů

## Co TypeChecker dělá

1. Projde celý AST strom
2. Ke každému výrazu zjistí a uloží jeho typ (nastaví `.type` na uzlech)
3. Zkontroluje, že typy dávají smysl
4. Vloží `IntToFloat` uzly kde je potřeba automatická konverze
5. Nahlásí **všechny** typové chyby (nezastaví se na první)

## ScopeManager – správa rozsahu platnosti proměnných

### Proč scopy?

V jazycích s bloky (`{ ... }`) proměnné deklarované uvnitř bloku existují
jen v tomto bloku a zanikají po jeho opuštění:

```
int x;        ← x existuje v celém programu
{
    int y;    ← y existuje jen uvnitř tohoto bloku
    x = 5;   ← OK, x je viditelné
}
y = 3;        ← CHYBA: y zde neexistuje
```

### Jak ScopeManager funguje

```python
class ScopeManager:
    def __init__(self):
        self.scopes = [{}]    # zásobník slovníků, začínáme s globálním scope
```

`scopes` je zásobník slovníků. Každý slovník = jeden scope (name → type).

```
Začátek:      scopes = [{}]                ← globální scope
int x; →      scopes = [{"x": "int"}]
{  →          scopes = [{"x": "int"}, {}]    ← nový scope pro blok
  int y; →    scopes = [{"x": "int"}, {"y": "int"}]
}  →          scopes = [{"x": "int"}]        ← y zaniklo!
```

**Shadowing je zakázaný** – `declare()` kontroluje **všechny** aktivní scopy.
Pokud proměnná stejného jména existuje kdekoliv, je to chyba.

```python
def declare(self, name, var_type):
    for scope in self.scopes:
        if name in scope:
            raise TypeError_("Variable already declared")
    self.scopes[-1][name] = var_type

def lookup(self, name):
    for scope in reversed(self.scopes):   # hledá od nejbližšího scope
        if name in scope:
            return scope[name]
    raise TypeError_("Undeclared variable")
```

## Visitor pattern

```python
def visit(self, node):
    method = f"visit_{type(node).__name__}"   # zjistí název třídy uzlu
    visitor = getattr(self, method, None)      # najde metodu tohoto jména
    return visitor(node)
```

Pro každý typ AST uzlu existuje metoda `visit_BinOp`, `visit_If` atd.
Přidat podporu pro nový uzel = přidat novou metodu. Nic jiného se nezmění.

## Sběr všech chyb

TypeChecker **nezastaví se na první chybě**. Používá `_safe_visit()`:

```python
def _safe_visit(self, node):
    try:
        return self.visit(node)
    except TypeError_ as e:
        self.errors.append(str(e))
        return None
```

Chyba se uloží do seznamu a kontrola pokračuje dál. Na konci se všechny chyby
vypíší najednou.

## Klíčové visit metody

### Binární operace

```python
def visit_BinOp(self, node):
    left_type = self.visit(node.left)     # zjisti typ levého operandu
    right_type = self.visit(node.right)   # zjisti typ pravého operandu
```

Každý operátor má svá pravidla. Příklad – logické operátory:
```python
    if op in ("||", "&&"):
        if left_type != "bool" or right_type != "bool":
            raise TypeError_(...)
        node.type = "bool"
        return "bool"
```

### Automatická konverze int → float

```python
    if {left_type, right_type} == {"int", "float"}:
        if left_type == "int":
            node.left = IntToFloat(node.left)    # vloží konverzní uzel do AST
        else:
            node.right = IntToFloat(node.right)
```

Přímo modifikuje AST – CodeGen pak uvidí `IntToFloat` a vygeneruje instrukci `itof`.

### Přiřazení

```python
def visit_Assign(self, node):
    if not isinstance(node.target, Var):
        raise TypeError_("Left side must be a variable")
    target_type = self.scope.lookup(node.target.name)
    val_type = self.visit(node.value)
    # Konverze int → float pokud přiřazujeme int do float proměnné
    if target_type == "float" and val_type == "int":
        node.value = IntToFloat(node.value)
```

---

# Soubor `codegen.py` – AST → instrukce

## Co CodeGen dělá

Prochází typovaný AST (po TypeCheckeru) a pro každý uzel emituje instrukce
zásobníkového stroje. Výsledkem je seznam stringů.

## Základní struktura

```python
TYPE_SUFFIX = {"int": "I", "float": "F", "bool": "B", "string": "S"}
DEFAULTS = {"int": "push I 0", "float": "push F 0.0", "bool": "push B false", "string": 'push S ""'}
```

`new_label()` generuje unikátní čísla pro labely (skoky). Každý `if` a `while`
potřebuje vlastní labely.

## Deklarace proměnné

```python
def visit_VarDecl(self, node):
    for name in node.names:
        self.emit(DEFAULTS[node.var_type])   # pushne výchozí hodnotu
        self.emit(f"save {name}")            # uloží do proměnné
```

`int a;` → `push I 0` / `save a`.

## Přiřazení

```python
def visit_Assign(self, node):
    self.visit(node.value)                   # hodnota na zásobník
    self.emit(f"save {node.target.name}")    # uloží do proměnné
    self.emit(f"load {node.target.name}")    # znovu načte na zásobník
```

Proč `save` + `load`? Protože `=` je **výraz** (vrací hodnotu).
`a = b = 5` musí fungovat: vnitřní přiřazení nechá 5 na zásobníku pro vnější.
`ExprStmt` pak přidá `pop` a zahodí výsledek, když přiřazení stojí samo jako příkaz.

## If příkaz

```python
def visit_If(self, node):
    else_label = self.new_label()
    end_label  = self.new_label()
    self.visit(node.condition)       # podmínka → bool na zásobníku
    self.emit(f"fjmp {else_label}")  # pokud false, skoč na else
    self.visit(node.then_stmt)       # kód then větve
    self.emit(f"jmp {end_label}")    # přeskočí else větev
    self.emit(f"label {else_label}") # začátek else
    if node.else_stmt is not None:
        self.visit(node.else_stmt)
    self.emit(f"label {end_label}")  # konec
```

Vždy generuje oba labely (else + end), i když else větev chybí.
To odpovídá očekávanému formátu ze zadání.

## While smyčka

```python
def visit_While(self, node):
    start_label = self.new_label()
    end_label   = self.new_label()
    self.emit(f"label {start_label}")    # START
    self.visit(node.condition)
    self.emit(f"fjmp {end_label}")       # pokud false, konec smyčky
    self.visit(node.body)
    self.emit(f"jmp {start_label}")      # zpět na START
    self.emit(f"label {end_label}")      # END
```

## Binární operace

```python
def visit_BinOp(self, node):
    self.visit(node.left)     # levý operand → zásobník
    self.visit(node.right)    # pravý operand → zásobník
    # instrukce vezme dvě hodnoty a pushne výsledek
```

Speciální případ: `!=` neexistuje jako instrukce → generuje se `eq` + `not`.

Pro porovnávací operátory (`<`, `>`, `==`) se typ bere z operandů (`node.left.type`),
ne z výsledku (ten je vždy `bool`).

---

# Soubor `interpreter.py` – vykonání instrukcí

## Jak zásobníkový stroj funguje

```
push I 3   →  zásobník: [3]
push I 4   →  zásobník: [3, 4]    (4 je navrchu)
add I      →  zásobník: [7]       (vezme 4 a 3, pushne 7)
save x     →  zásobník: []        (popne 7, uloží do proměnné x)
```

## Inicializace

```python
class Interpreter:
    def __init__(self, instructions):
        self.instructions = instructions
        self.stack = []
        self.variables = {}
        self.labels = {}    # číslo labelu → index instrukce
        self.pc = 0         # program counter

        # Před-sken labelů
        for i, instr in enumerate(self.instructions):
            if instr.startswith("label "):
                self.labels[int(instr.split()[1])] = i
```

**Proč přeskenovat labely předem?**
`fjmp 5` potřebuje vědět kde je `label 5`, ale ten může být kdekoliv –
i za aktuální pozicí. Sken předem umožňuje skákat dopředu i dozadu.

## Hlavní smyčka

```python
def run(self):
    while self.pc < len(self.instructions):
        instr = self.instructions[self.pc]
        self.pc += 1                   # posune PŘED vykonáním!
        self._execute(instr)
```

`pc` se zvýší **před** `_execute`, protože `jmp` nastavuje `pc` přímo.

## Klíčové instrukce

### Push – převod ze stringu na Python typ

```python
def _push(self, type_suffix, raw_value):
    if type_suffix == "I":   self.stack.append(int(raw_value))
    elif type_suffix == "F": self.stack.append(float(raw_value))
    elif type_suffix == "B": self.stack.append(raw_value == "true")
    elif type_suffix == "S":
        # Stringy v instrukcích jsou v uvozovkách: "hello world"
        s = raw_value[1:-1]     # odstraní uvozovky
        s = s.replace('\\"', '"').replace('\\n', '\n')...
        self.stack.append(s)
```

### Aritmetika – pozor na pořadí

```python
b, a = self.stack.pop(), self.stack.pop()   # b je navrchu
self.stack.append(a + b)
```

`b` (navrchu) přišlo druhé. Pro `sub`/`div`/`lt`/`gt` záleží na pořadí.

### Skoky

```python
elif op == "jmp":
    self.pc = self.labels[int(parts[1])]

elif op == "fjmp":
    val = self.stack.pop()           # vezmi bool
    if not val:
        self.pc = self.labels[int(parts[1])]    # skoč jen pokud false
```

### Print

```python
elif op == "print":
    n = int(parts[1])
    values = self.stack[-n:]    # posledních n hodnot
    del self.stack[-n:]
    for val in values:
        self._print_value(val)
    print()     # newline na konci
```

### Výpis hodnot

```python
def _print_value(self, val):
    if isinstance(val, bool):           # bool PŘED int (bool je podtřída int)
        print("true" if val else "false", end="")
    elif isinstance(val, float):
        formatted = f"{val:.10f}".rstrip("0")   # odstraní nuly na konci
        if formatted.endswith("."):
            formatted += "0"                    # ale aspoň jedno des. místo
        print(formatted, end="")
    else:
        print(val, end="")
```

## Načtení instrukcí ze souboru

```python
def load_instructions(path):
    with open(path) as f:
        return [line.rstrip("\n") for line in f if line.strip()]
```

---

# Soubor `main.py` – vstupní bod

```python
from antlr4 import CommonTokenStream, InputStream
from PLCLexer import PLCLexer
from PLCParser import PLCParser
from ast_builder import ASTBuilder
from typechecker import TypeChecker
from codegen import CodeGen
from interpreter import Interpreter

def compile_source(source_path):
    source = open(source_path).read()

    # 1. ANTLR lexing + parsing
    lexer = PLCLexer(InputStream(source))
    parser = PLCParser(CommonTokenStream(lexer))
    tree = parser.program()

    # 2. Parse tree → AST
    ast = ASTBuilder().visit(tree)

    # 3. Type checking
    TypeChecker().check(ast)

    # 4. Code generation
    return CodeGen().generate(ast)
```

Tři režimy spuštění:
- `python3 main.py program.plc` – kompilace + spuštění
- `python3 main.py --compile program.plc` – jen kompilace (→ .ins soubor)
- `python3 main.py --run program.ins` – spuštění .ins souboru

`SyntaxErrorCollector` nahrazuje výchozí ANTLR error listener a sbírá
všechny syntaktické chyby (ne jen první).

---

# Jak přidat novou funkci

## Příklad: přidání `for` cyklu

Syntaxe: `for (int i = 0; i < 10; i = i + 1) { ... }`

### 1. `PLC.g4` – nové pravidlo v gramatice
```
statement
    : ...
    | 'for' '(' statement expr ';' expr ')' statement  # ForStmt
    ;
```
Po úpravě znovu vygenerovat ANTLR soubory.

### 2. `ast_nodes.py` – nový uzel
```python
@dataclass
class For:
    init: Any        # inicializační příkaz
    condition: Any   # podmínka
    step: Any        # krok
    body: Any        # tělo smyčky
```

### 3. `ast_builder.py` – nová visitor metoda
```python
def visitForStmt(self, ctx):
    init = self.visit(ctx.statement(0))
    cond = self.visit(ctx.expr(0))
    step = self.visit(ctx.expr(1))
    body = self.visit(ctx.statement(1))
    return For(init, cond, step, body)
```

### 4. `typechecker.py` – typová kontrola
```python
def visit_For(self, node):
    self.scope.enter()
    self.visit(node.init)
    cond_type = self.visit(node.condition)
    if cond_type != "bool":
        raise TypeError_("For condition must be bool")
    self.visit(node.step)
    self.visit(node.body)
    self.scope.exit()
```

### 5. `codegen.py` – generování kódu
```python
def visit_For(self, node):
    self.visit(node.init)
    start = self.new_label()
    end = self.new_label()
    self.emit(f"label {start}")
    self.visit(node.condition)
    self.emit(f"fjmp {end}")
    self.visit(node.body)
    self.visit(node.step)
    self.emit("pop")          # step je výraz → zahodit výsledek
    self.emit(f"jmp {start}")
    self.emit(f"label {end}")
```

**Nic jiného se nemění.** To je síla modulární architektury.

## Přehled: kde co měnit

| Chci přidat... | Kde upravit |
|---|---|
| Nový příkaz (`for`, `do-while`...) | `PLC.g4` + `ast_nodes.py` + `ast_builder.py` + `typechecker.py` + `codegen.py` |
| Nový operátor | `PLC.g4` (správná pozice = priorita) + `visit_BinOp` v typecheckeru a codegenu |
| Nový typ (`char`...) | `PLC.g4` lexer + `ast_nodes.py` literál + `TYPE_SUFFIX`/`DEFAULTS` v codegenu + `_push`/`_parse_input` v interpretu |
| Změna scopingu | Jen `ScopeManager` v `typechecker.py` |
