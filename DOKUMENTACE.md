# PLC Compiler – Kompletní dokumentace

Tento dokument vysvětluje celý zdrojový kód projektu od základů.
Je určen pro toho, kdo kód neviděl a nemá hluboké programátorské zkušenosti.

---

## Co projekt dělá

Projekt implementuje **překladač a interpret** jednoduchého programovacího jazyka.
Vezme zdrojový kód (textový soubor) a vykoná ho – vypíše výsledky, načte vstupy atd.

Spuštění:
```
python3 main.py program.txt
```

---

## Jak celý program funguje – výrobní linka

Vstupní text se zpracovává v 5 krocích. Každý krok dělá jednu věc a předá výsledek dalšímu:

```
"write 5+3;"
      ↓
  1. LEXER        →  [WRITE] [5] [+] [3] [;]
      ↓               (tokeny – kousky textu s označením)
  2. PARSER       →  Write( BinOp(+, 5, 3) )
      ↓               (AST – strom struktury programu)
  3. TYPECHECKER  →  Write( BinOp(+:int, 5:int, 3:int) )
      ↓               (typy doplněny, chyby odhaleny)
  4. CODEGEN      →  push I 5 / push I 3 / add I / print 1
      ↓               (instrukce zásobníkového stroje)
  5. INTERPRETER  →  8
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
Příklad: program se třemi příkazy → `Program(statements=[stmt1, stmt2, stmt3])`.

```python
@dataclass
class Block:
    statements: List[Any]
```
Blok příkazů v složených závorkách `{ ... }`. Důležitý proto, že vytváří
vlastní **scope** – proměnné deklarované uvnitř zaniknou po opuštění bloku.

```python
@dataclass
class Empty:
    pass
```
Prázdný příkaz – jen samotný středník `;`. Neobsahuje nic, nic nedělá.

## Uzly pro příkazy

```python
@dataclass
class VarDecl:
    var_type: str       # "int", "float", "bool", "string"
    names: List[str]
```
Deklarace proměnné: `int a, b;` → `VarDecl(var_type="int", names=["a", "b"])`.
Poznámka: `names` TypeChecker přejmenuje na "mangled" verze jako `a$0`, `b$1`
(důvod viz sekce TypeChecker).

```python
@dataclass
class If:
    condition: Any
    then_stmt: Any
    else_stmt: Optional[Any] = None
```
Podmíněný příkaz. `else_stmt` je `None` pokud větev `else` chybí.
Příklad: `if (a > 0) write a;` → `If(condition=BinOp(">", ...), then_stmt=Write(...), else_stmt=None)`.

```python
@dataclass
class While:
    condition: Any
    body: Any
```
Smyčka: `while (i < 10) { ... }` → `While(condition=BinOp("<", ...), body=Block(...))`.

```python
@dataclass
class Read:
    variables: List[Any]   # seznam Var uzlů
```
Čtení ze stdin: `read a, b;` → `Read(variables=[Var("a"), Var("b")])`.

```python
@dataclass
class Write:
    expressions: List[Any]
```
Výpis: `write "x=", a;` → `Write(expressions=[StrLit("x="), Var("a")])`.

```python
@dataclass
class ExprStmt:
    expr: Any
```
Výraz použitý jako příkaz. V jazyce je `=` výraz (vrací hodnotu), ale `a = 5;`
je příkaz – výsledek se zahodí. `ExprStmt` říká CodeGenu: "po vykonání výrazu přidej `pop`".

## Uzly pro výrazy

```python
@dataclass
class Assign:
    target: Any            # Var uzel (levá strana)
    value: Any             # libovolný výraz (pravá strana)
    type: Optional[str] = None
```
Přiřazení: `a = 5` → `Assign(target=Var("a"), value=IntLit(5))`.
`type` doplní TypeChecker (bude `"int"`).

```python
@dataclass
class BinOp:
    op: str                # "+", "-", "*", "/", "%", ".", "<", ">", "==", "!=", "&&", "||"
    left: Any
    right: Any
    type: Optional[str] = None
```
Binární operace (dva operandy): `5 + 3` → `BinOp(op="+", left=IntLit(5), right=IntLit(3))`.

```python
@dataclass
class UnaryOp:
    op: str                # "!" nebo "-"
    operand: Any
    type: Optional[str] = None
```
Unární operace (jeden operand): `-5` → `UnaryOp(op="-", operand=IntLit(5))`.

```python
@dataclass
class IntToFloat:
    expr: Any
    type: str = "float"
```
Tento uzel **nevytváří parser** – přidává ho TypeChecker sám, když vidí situaci jako
`1.5 + 3` (int `3` se musí převést na float před sčítáním). Jde o "neviditelnou"
konverzi vloženou přímo do stromu.

```python
@dataclass
class Var:
    name: str
    type: Optional[str] = None
```
Odkaz na proměnnou: `a` v kódu → `Var(name="a")`.
TypeChecker doplní `type` a přejmenuje `name` na mangled verzi (např. `a$0`).

## Literály

```python
@dataclass
class IntLit:
    value: int
    type: str = "int"       # typ je pevně daný – vždy "int"

@dataclass
class FloatLit:
    value: float
    type: str = "float"

@dataclass
class BoolLit:
    value: bool
    type: str = "bool"

@dataclass
class StrLit:
    value: str
    type: str = "string"
```
Konkrétní hodnoty v kódu. Mají `type` nastavený rovnou, protože ho známe
z hodnoty (číslo je vždy int nebo float, text je vždy string atd.).

---

# Soubor `lexer.py` – text → tokeny

## Co je token?

Token = nejmenší smysluplná část kódu. Lexer rozloží vstupní text na seznam tokenů.

Příklad: `write "hello", x + 3;` se rozloží na:
```
Token(type="write",  value="write")
Token(type="STRING", value="hello")
Token(type=",",      value=",")
Token(type="ID",     value="x")
Token(type="+",      value="+")
Token(type="INT",    value="3")
Token(type=";",      value=";")
```

Každý token má:
- `type` – kategorie (co to je: klíčové slovo, číslo, operátor...)
- `value` – přesný text ze zdrojového kódu
- `line` – číslo řádku (pro chybové hlášky)

## Struktura třídy Lexer

```python
class Lexer:
    def __init__(self, source: str):
        self.source = source  # celý zdrojový kód jako jeden velký string
        self.pos = 0          # aktuální pozice – index znaku v source
        self.line = 1         # číslo aktuálního řádku (začínáme od 1)
```

Lexer si pamatuje kde v textu právě je (`pos`) a na kterém řádku (`line`).
Oba se průběžně aktualizují při čtení textu.

## Hlavní smyčka `tokenize()`

```python
def tokenize(self) -> List[Token]:
    tokens = []
    while self.pos < len(self.source):
        ch = self.source[self.pos]   # aktuální znak
        ...
    tokens.append(Token("EOF", "", self.line))  # konec souboru
    return tokens
```

Prochází text znak po znaku. Pro každý znak rozhodne, o co jde, a vytvoří token
(nebo přeskočí, pokud je to mezera/komentář). Na konec přidá speciální token `EOF`
(End Of File) – parser ho použije jako signál konce.

## Co se zpracovává a v jakém pořadí

**1. Mezery a konce řádků** – přeskočí se:
```python
if ch in " \t\r":
    self.pos += 1
    continue
if ch == "\n":
    self.line += 1   # zvýší počítadlo řádků
    self.pos += 1
    continue
```

**2. Komentář `//`** – přeskočí vše do konce řádku:
```python
if ch == "/" and self.source[self.pos + 1] == "/":
    while self.pos < len(self.source) and self.source[self.pos] != "\n":
        self.pos += 1
    continue
```

**3. Blokový komentář `/* ... */`** – přeskočí vše do `*/`:
```python
if ch == "/" and self.source[self.pos + 1] == "*":
    self.pos += 2             # přeskočí /*
    while self.pos + 1 < len(self.source):
        if self.source[self.pos] == "\n":
            self.line += 1    # počítáme řádky i uvnitř komentáře
        if self.source[self.pos] == "*" and self.source[self.pos + 1] == "/":
            self.pos += 2     # přeskočí */
            break
        self.pos += 1
```

**4. String literál** – zahájí čtení stringu metodou `_read_string()`:
```python
if ch == '"':
    tokens.append(self._read_string())
    continue
```

**5. Číslo** – zahájí čtení čísla metodou `_read_number()`:
```python
if ch.isdigit():
    tokens.append(self._read_number())
    continue
```

**6. Identifikátor nebo klíčové slovo**:
```python
if ch.isalpha() or ch == "_":
    tokens.append(self._read_ident())
    continue
```

**7. Dvoumístné operátory** – musí být před jednomístnými!
Jinak by `==` bylo rozpoznáno jako dvě `=`:
```python
two = self.source[self.pos:self.pos + 2]
if two in TWO_CHAR_OPS:   # {"==", "!=", "||", "&&"}
    tokens.append(Token(two, two, self.line))
    self.pos += 2
    continue
```

**8. Jednomístné operátory a interpunkce**:
```python
if ch in ONE_CHAR_OPS:
    tokens.append(Token(ch, ch, self.line))
    self.pos += 1
    continue
```

## Čtení stringu `_read_string()`

```python
def _read_string(self) -> Token:
    line = self.line
    self.pos += 1      # přeskočí otevírací uvozovku "
    result = []
    while self.pos < len(self.source) and self.source[self.pos] != '"':
        if self.source[self.pos] == "\\":   # zpětné lomítko = escape sekvence
            self.pos += 1
            esc = self.source[self.pos]
            if esc == "n":    result.append("\n")   # \n → nový řádek
            elif esc == "t":  result.append("\t")   # \t → tabulátor
            elif esc == "\\": result.append("\\")   # \\ → zpětné lomítko
            elif esc == '"':  result.append('"')    # \" → uvozovka
            else:             result.append(esc)    # ostatní: zachovat
        else:
            if self.source[self.pos] == "\n":
                self.line += 1          # string může být víceřádkový
            result.append(self.source[self.pos])
        self.pos += 1
    if self.pos >= len(self.source):
        raise LexerError(f"Line {line}: unterminated string")
    self.pos += 1   # přeskočí zavírací uvozovku "
    return Token("STRING", "".join(result), line)
```

Čte znak po znaku. `result` je seznam znaků, na konci se spojí do stringu pomocí `"".join(result)`.

## Čtení čísla `_read_number()`

```python
def _read_number(self) -> Token:
    start = self.pos
    while self.pos < len(self.source) and self.source[self.pos].isdigit():
        self.pos += 1
    # Zkontroluj, zda jde o float (tečka následovaná číslicí)
    if self.pos < len(self.source) and self.source[self.pos] == ".":
        if self.pos + 1 < len(self.source) and self.source[self.pos + 1].isdigit():
            self.pos += 1   # přeskočí tečku
            while self.pos < len(self.source) and self.source[self.pos].isdigit():
                self.pos += 1
            return Token("FLOAT", self.source[start:self.pos], line)
    return Token("INT", self.source[start:self.pos], line)
```

Proč kontrolujeme co je za tečkou? Protože `3.14` je float, ale `a.b` je proměnná,
tečka (operátor konkatenace), proměnná. Kdybychom nekontrolovali, `a.b` by se
rozpoznalo špatně.

## Čtení identifikátoru `_read_ident()`

```python
def _read_ident(self) -> Token:
    start = self.pos
    while self.pos < len(self.source) and (self.source[self.pos].isalnum() or self.source[self.pos] == "_"):
        self.pos += 1
    word = self.source[start:self.pos]
    if word in KEYWORDS:
        return Token(word, word, line)   # klíčové slovo: type = "if", "while"...
    return Token("ID", word, line)       # identifikátor: type = "ID"
```

Klíčové slovo a identifikátor vypadají stejně – jsou to písmena. Rozdíl je v tom,
zda se slovo nachází v množině `KEYWORDS`. Pokud ano, je to klíčové slovo s `type`
rovným samotnému slovu (`"if"`, `"while"` atd.). Pokud ne, je to identifikátor s `type = "ID"`.

---

# Soubor `parser.py` – tokeny → AST

## Co je recursive descent parser?

Parser bere seznam tokenů a staví z nich AST strom.
"Recursive descent" = každé jazykové pravidlo je jedna metoda, která může volat jiné metody.

**Klíčová myšlenka:** priorita operátorů je zakódována ve struktuře volání.
Metoda pro `+` volá metodu pro `*` – tím se `*` zpracuje "hlouběji" a tedy dříve,
což odpovídá vyšší prioritě.

```
_expr()
  └─ _assignment()       ← = (pravá asociativita)
       └─ _or_expr()     ← ||
            └─ _and_expr()  ← &&
                 └─ _eq_expr()   ← ==, !=
                      └─ _rel_expr()   ← <, >
                           └─ _add_expr()   ← +, -, .
                                └─ _mul_expr()   ← *, /, %
                                     └─ _unary()   ← !, unární -
                                          └─ _primary()  ← literály, ID, (expr)
```

## Pomocné metody

```python
def _current(self) -> Token:
    return self.tokens[self.pos]       # aktuální token (neposunuje se)

def _peek(self, token_type: str) -> bool:
    return self._current().type == token_type   # je aktuální token tohoto typu?

def _match(self, token_type: str) -> Token:
    tok = self._current()
    if tok.type != token_type:
        raise ParseError(f"Line {tok.line}: expected '{token_type}', got '{tok.value}'")
    self.pos += 1    # posune se na další token
    return tok       # vrátí spotřebovaný token
```

`_match` je základ parseru:
- Zkontroluje, že aktuální token je správného typu
- Posune `pos` na další token
- Vrátí token (pro přístup k hodnotě)
- Pokud token nesedí, vyhodí chybu

## Parsování příkazů

```python
def _statement(self):
    tok = self._current()

    if tok.type == ";":           return Empty po _match(";")
    if self._at_type_keyword():   return self._var_decl()
    if tok.type == "{":           return self._block()
    if tok.type == "if":          return self._if_stmt()
    if tok.type == "while":       return self._while_stmt()
    if tok.type == "read":        return self._read_stmt()
    if tok.type == "write":       return self._write_stmt()
    return self._expr_stmt()      # výchozí: výraz jako příkaz
```

Podívá se na aktuální token a rozhodne, jaký příkaz parsovat – funguje jako rozcestník.

## Deklarace proměnné

```python
def _var_decl(self):
    var_type = self._current().value      # "int", "float" atd.
    self._match(self._current().type)     # spotřebuje klíčové slovo
    names = [self._match("ID").value]     # první jméno (povinné)
    while self._peek(","):                # dokud jsou čárky, čti další jména
        self._match(",")
        names.append(self._match("ID").value)
    self._match(";")
    return VarDecl(var_type, names)
```

Parsuje `int a, b, c;` → `VarDecl("int", ["a", "b", "c"])`.

## If příkaz

```python
def _if_stmt(self):
    self._match("if")
    self._match("(")
    cond = self._expr()               # parsuje podmínku
    self._match(")")
    then_stmt = self._statement()     # parsuje then větev (příkaz nebo blok)
    else_stmt = None
    if self._peek("else"):            # else je volitelné
        self._match("else")
        else_stmt = self._statement()
    return If(cond, then_stmt, else_stmt)
```

## Výrazy – přiřazení (pravá asociativita)

```python
def _assignment(self):
    left = self._or_expr()       # nejdřív parsuj vyšší prioritu
    if self._peek("="):
        self._match("=")
        right = self._assignment()   # ← REKURZE: volá SEBE (ne _or_expr)
        return Assign(left, right)
    return left
```

Pravá asociativita je elegantně vyřešena rekurzí. `a = b = 5`:
1. `left = a` (parsuje `_or_expr` → Var("a"))
2. Vidí `=`, parsuje pravou stranu jako `_assignment` znovu
3. Pravá strana: `left = b`, vidí `=`, parsuje `5` → `Assign(b, 5)`
4. Výsledek: `Assign(a, Assign(b, 5))`

## Výrazy – levá asociativita (`||`, `&&`, `+`, `*` atd.)

```python
def _or_expr(self):
    left = self._and_expr()
    while self._peek("||"):        # while = levá asociativita
        self._match("||")
        right = self._and_expr()
        left = BinOp("||", left, right)   # "obaluje" předchozí výsledek
    return left
```

`a || b || c` se parsuje jako `(a || b) || c`:
1. `left = a`
2. Vidí `||`, `left = BinOp(||, a, b)`
3. Vidí `||`, `left = BinOp(||, BinOp(||, a, b), c)`

Stejný vzor mají `_and_expr`, `_eq_expr`, `_rel_expr`, `_add_expr`, `_mul_expr`.

## Unární operátory

```python
def _unary(self):
    if self._peek("!"):
        self._match("!")
        operand = self._unary()    # rekurzivní: !!true je OK
        return UnaryOp("!", operand)
    if self._peek("-"):
        self._match("-")
        operand = self._unary()    # rekurzivní: --5 je OK
        return UnaryOp("-", operand)
    return self._primary()
```

Unární operátory volají sebe rekurzivně → `!!true` = `UnaryOp(!, UnaryOp(!, true))`.

## Primární výrazy

```python
def _primary(self):
    tok = self._current()

    if tok.type == "INT":     return IntLit(int(tok.value))      # "42" → 42
    if tok.type == "FLOAT":   return FloatLit(float(tok.value))  # "3.14" → 3.14
    if tok.type == "STRING":  return StrLit(tok.value)
    if tok.type == "true":    return BoolLit(True)
    if tok.type == "false":   return BoolLit(False)
    if tok.type == "ID":      return Var(tok.value)

    if tok.type == "(":
        self._match("(")
        expr = self._expr()    # obsah závorek = celý výraz znovu od začátku
        self._match(")")
        return expr            # závorky jsou "transparentní" – vrátíme obsah
```

"Listové" uzly stromu. Závorky jsou transparentní – parser je spolkne
a vrátí obsah, prioritu zajistí fakt, že se expr parsuje celý znovu.

---

# Soubor `typechecker.py` – kontrola typů

## Co TypeChecker dělá

1. Projde celý AST strom
2. Ke každému výrazu zjistí a uloží jeho typ (nastaví `.type` na uzlech)
3. Zkontroluje, že typy dávají smysl
4. Přejmenuje proměnné na unikátní "mangled" jména
5. Vloží `IntToFloat` uzly kde je potřeba automatická konverze

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

`ScopeManager` implementuje toto chování.

### Jak ScopeManager funguje

```python
class ScopeManager:
    def __init__(self):
        self.scopes = [{}]    # zásobník slovníků, začínáme s globálním scope
        self.var_counter = 0  # počítadlo pro unikátní jména
```

`scopes` je zásobník slovníků. Každý slovník = jeden scope.
Vizualizace při vstupu/výstupu z bloku:

```
Začátek:      scopes = [{}]                ← globální scope
int x; →      scopes = [{"x": ("x$0","int")}]
{  →          scopes = [{"x": ...}, {}]    ← nový scope pro blok
  int y; →    scopes = [{"x": ...}, {"y": ("y$1","int")}]
}  →          scopes = [{"x": ...}]        ← y zaniklo!
```

```python
def declare(self, name: str, var_type: str) -> str:
    current = self.scopes[-1]      # aktuální (nejhloubnější) scope
    if name in current:
        raise TypeError_("Variable already declared in this scope")
    mangled = f"{name}${self.var_counter}"   # "x" → "x$0", "y" → "y$1"
    self.var_counter += 1
    current[name] = (mangled, var_type)
    return mangled
```

### Proč "mangling" (přejmenování)?

Dvě proměnné stejného jména v různých scopech musí mít různá jména v interpretu,
protože interpret používá jeden slovník proměnných:

```
{
    int x;    → přejmenováno na x$0
    {
        int x;    → přejmenováno na x$1 (jiná proměnná!)
        write x;  → generuje: load x$1
    }
    write x;  → generuje: load x$0
}
```

```python
def lookup(self, name: str):
    for scope in reversed(self.scopes):   # hledá od nejbližšího scope
        if name in scope:
            return scope[name]
    raise TypeError_("Undeclared variable")
```

`reversed` = hledá od nejhloubnějšího scope směrem ven. Vnitřní `x` tak zastíní vnější `x`.

## Visitor pattern

```python
def visit(self, node):
    method = f"visit_{type(node).__name__}"   # zjistí název třídy uzlu
    visitor = getattr(self, method, None)      # najde metodu tohoto jména
    if visitor is None:
        raise TypeError_(f"No visitor for {type(node).__name__}")
    return visitor(node)
```

Místo dlouhého `if isinstance(node, BinOp): ... elif isinstance(node, If): ...`
se použije reflexe. `type(node).__name__` vrátí název třídy jako string
(`"BinOp"`, `"If"` atd.), pak se najde metoda `visit_BinOp`, `visit_If` atd.

Přidat podporu pro nový AST uzel = přidat metodu `visit_NovýUzel`. Nic jiného se nezmění.

## Klíčové visit metody

### Blok

```python
def visit_Block(self, node: Block):
    self.scope.enter()           # vstup do nového scope
    for stmt in node.statements:
        self.visit(stmt)
    self.scope.exit()            # výstup – proměnné z bloku zaniknou
```

### Binární operace – ukázka logiky

```python
def visit_BinOp(self, node: BinOp):
    left_type = self.visit(node.left)     # zjisti typ levého operandu (rekurzivně)
    right_type = self.visit(node.right)   # zjisti typ pravého operandu

    op = node.op

    if op in ("||", "&&"):
        if left_type != "bool" or right_type != "bool":
            raise TypeError_(f"Operator '{op}' requires bool operands")
        node.type = "bool"
        return "bool"
```

Každý operátor má svá pravidla. Metoda:
1. Rekurzivně zjistí typy operandů
2. Zkontroluje pravidla
3. Nastaví `node.type` = výsledný typ
4. Vrátí výsledný typ (pro použití v nadřazeném uzlu)

### Automatická konverze int → float

```python
    # Pokud jsou operandy int a float, převeď int na float
    if {left_type, right_type} == {"int", "float"}:
        if left_type == "int":
            node.left = IntToFloat(node.left)    # vloží konverzní uzel do AST!
            left_type = "float"
        else:
            node.right = IntToFloat(node.right)
            right_type = "float"
```

Toto přímo modifikuje AST strom – vloží `IntToFloat` uzel.
CodeGen pak uvidí `IntToFloat` a vygeneruje instrukci `itof`.

### Přiřazení

```python
def visit_Assign(self, node: Assign):
    if not isinstance(node.target, Var):
        raise TypeError_("Left side of assignment must be a variable")
    mangled, target_type = self.scope.lookup(node.target.name)
    node.target.name = mangled      # přejmenuje proměnnou na mangled verzi
    node.target.type = target_type
    val_type = self.visit(node.value)

    # Konverze int → float pokud přiřazujeme int do float proměnné
    if target_type == "float" and val_type == "int":
        node.value = IntToFloat(node.value)
        val_type = "float"

    if target_type != val_type:
        raise TypeError_(f"Cannot assign '{val_type}' to '{target_type}'")
    node.type = target_type
    return target_type
```

---

# Soubor `codegen.py` – AST → instrukce

## Co CodeGen dělá

Prochází typovaný AST (po TypeCheckeru) a pro každý uzel emituje instrukce
zásobníkového stroje. Výsledkem je seznam stringů jako:
```
push I 5
push I 3
add I
print 1
```

## Základní struktura

```python
TYPE_SUFFIX = {"int": "I", "float": "F", "bool": "B", "string": "S"}
DEFAULTS    = {"int": ("I", 0), "float": ("F", 0.0), "bool": ("B", "false"), "string": ("S", "")}
```

`TYPE_SUFFIX` mapuje typy jazyka na jednopísmenné zkratky pro instrukce.
`DEFAULTS` obsahuje výchozí hodnoty pro každý typ (int → 0, string → "" atd.).

```python
def new_label(self) -> int:
    n = self.label_counter
    self.label_counter += 1
    return n    # vrátí 0, pak 1, pak 2, pak 3...

def emit(self, instr: str):
    self.instructions.append(instr)   # přidá instrukci do výsledného seznamu
```

`new_label()` generuje unikátní čísla pro labely (skoky). Každý `if` a `while`
potřebuje vlastní labely, jinak by se skoky pletly.

## Deklarace proměnné

```python
def visit_VarDecl(self, node: VarDecl):
    for name in node.names:
        suffix, default = DEFAULTS[node.var_type]
        self.emit(f"push {suffix} {default}")   # pushne výchozí hodnotu
        self.emit(f"save {name}")               # uloží do proměnné
```

`int a;` → `push I 0` / `save a$0`. Proměnná "vznikne" jako výchozí hodnota.

## Přiřazení

```python
def visit_Assign(self, node: Assign):
    self.visit(node.value)                    # kód pravé strany → hodnota na zásobníku
    self.emit(f"save {node.target.name}")     # uloží do proměnné (popne zásobník)
    self.emit(f"load {node.target.name}")     # znovu načte na zásobník
```

Proč `save` a pak hned `load`? Protože `=` je **výraz** (vrací hodnotu).
`a = b = 5` musí fungovat takto:
1. Zpracuje `b = 5`: pushne 5, save do b, load z b (5 zůstane na zásobníku)
2. Zpracuje `a = [výsledek]`: vezme 5 ze zásobníku, save do a, load z a

`ExprStmt` pak přidá `pop` a zahodí zbývající hodnotu (výsledek přiřazení nepotřebujeme).

## If příkaz

```python
def visit_If(self, node: If):
    if node.else_stmt is not None:
        else_label = self.new_label()
        end_label  = self.new_label()
        self.visit(node.condition)       # podmínka → bool na zásobníku
        self.emit(f"fjmp {else_label}")  # pokud false, skoč na else
        self.visit(node.then_stmt)       # kód then větve
        self.emit(f"jmp {end_label}")    # přeskočí else větev
        self.emit(f"label {else_label}") # začátek else
        self.visit(node.else_stmt)
        self.emit(f"label {end_label}")  # konec
    else:
        end_label = self.new_label()
        self.visit(node.condition)
        self.emit(f"fjmp {end_label}")
        self.visit(node.then_stmt)
        self.emit(f"label {end_label}")
```

Vizualizace vygenerovaného kódu pro `if (a > 0) write a; else write 0;`:
```
load a$0
push I 0
gt I
fjmp 1         ← skoč na ELSE pokud false
load a$0
print 1        ← then větev
jmp 2          ← přeskoč else
label 1        ← ELSE
push I 0
print 1        ← else větev
label 2        ← END
```

## While smyčka

```python
def visit_While(self, node: While):
    start_label = self.new_label()
    end_label   = self.new_label()
    self.emit(f"label {start_label}")    # START: sem se skáče zpět
    self.visit(node.condition)
    self.emit(f"fjmp {end_label}")       # pokud false, konec smyčky
    self.visit(node.body)
    self.emit(f"jmp {start_label}")      # zpět na START
    self.emit(f"label {end_label}")      # END
```

Vizualizace pro `while (i < 10) { i = i + 1; }`:
```
label 0        ← START
load i$0
push I 10
lt I
fjmp 1         ← konec pokud i >= 10
load i$0
push I 1
add I
save i$0
load i$0
pop            ← ExprStmt: zahoď výsledek přiřazení
jmp 0          ← zpět na START
label 1        ← END
```

## Write a Read

```python
def visit_Write(self, node: Write):
    for expr in node.expressions:
        self.visit(expr)                          # každý výraz pushne hodnotu
    self.emit(f"print {len(node.expressions)}")   # vytiskni N hodnot najednou

def visit_Read(self, node: Read):
    for var in node.variables:
        suffix = TYPE_SUFFIX[var.type]
        self.emit(f"read {suffix}")      # čti hodnotu ze stdin, push na zásobník
        self.emit(f"save {var.name}")    # ulož do proměnné
```

## Binární operace

```python
def visit_BinOp(self, node: BinOp):
    self.visit(node.left)     # levý operand → na zásobník
    self.visit(node.right)    # pravý operand → na zásobník
    # teď jsou na zásobníku dvě hodnoty, instrukce je vezme a pushne výsledek

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
        operand_type = node.left.type    # lt potřebuje typ operandů, ne výsledku
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
        self.emit("not")       # != neexistuje jako instrukce → eq + not
```

## IntToFloat konverze

```python
def visit_IntToFloat(self, node: IntToFloat):
    self.visit(node.expr)    # vygeneruj kód pro int výraz
    self.emit("itof")        # přidej konverzi
```

---

# Soubor `interpreter.py` – vykonání instrukcí

## Jak zásobníkový stroj funguje

Zásobník = hromada talířů. Vždy přidáváš nebo bereš ze vrchu.

```
push I 3   →  zásobník: [3]
push I 4   →  zásobník: [3, 4]    (4 je navrchu)
add I      →  zásobník: [7]       (vezme 4 a 3, pushne 7)
push I 2   →  zásobník: [7, 2]
mul I      →  zásobník: [14]      (vezme 2 a 7, pushne 14)
save x     →  zásobník: []        (popne 14, uloží do proměnné x)
```

## Inicializace

```python
class Interpreter:
    def __init__(self, instructions: list):
        self.instructions = instructions
        self.stack = []         # zásobník (Python seznam, vrch = poslední prvek)
        self.variables = {}     # slovník: mangled_jméno → hodnota
        self.labels = {}        # slovník: číslo_labelu → index_instrukce
        self.pc = 0             # program counter: index aktuální instrukce

        # Před spuštěním projdi instrukce a zapamatuj si pozice labelů
        for i, instr in enumerate(self.instructions):
            if instr.startswith("label "):
                label_num = int(instr.split()[1])
                self.labels[label_num] = i
```

**Proč přeskenovat labely předem?**
`fjmp 5` potřebuje vědět kde je `label 5`, ale `label 5` může být kdekoliv v kódu –
i za aktuální pozicí. Kdybychom labely nehledali předem, museli bychom prohledávat
seznam pokaždé, nebo labely musely být jen dopředu.

## Hlavní smyčka

```python
def run(self):
    while self.pc < len(self.instructions):
        instr = self.instructions[self.pc]
        self.pc += 1                   # posune PŘED vykonáním instrukce!
        self._execute(instr)
```

`pc` se zvýší **před** `_execute`. Proč? Protože `jmp` nastavuje `pc` přímo.
Kdyby se `pc` zvyšovalo po `_execute`, `jmp` by fungoval o 1 instrukci dál.

## Vykonání instrukcí `_execute()`

```python
def _execute(self, instr: str):
    parts = instr.split(" ", 2)   # "push I 42" → ["push", "I", "42"]
    op = parts[0]
```

`split(" ", 2)` rozdělí na **maximálně 3 části**. String `"push S hello world"` se rozdělí
na `["push", "S", "hello world"]` – třetí část je celý zbytek, bez dalšího dělení.

### Push

```python
if op == "push":
    self._push(parts[1], parts[2] if len(parts) > 2 else "")
```

```python
def _push(self, type_suffix: str, raw_value: str):
    if type_suffix == "I":   self.stack.append(int(raw_value))
    elif type_suffix == "F": self.stack.append(float(raw_value))
    elif type_suffix == "B": self.stack.append(raw_value == "true")  # string → bool
    elif type_suffix == "S": self.stack.append(raw_value)            # string zůstane
```

Hodnoty ze instrukčního stringu se převedou na správné Python typy.

### Aritmetika

```python
elif op == "add":
    b, a = self.stack.pop(), self.stack.pop()   # b je navrchu (přišlo druhé)
    self.stack.append(a + b)
```

**Pozor na pořadí!** Zásobník: `[3, 5]` (5 navrchu). `b=5`, `a=3`. Pro `add` je pořadí jedno,
ale pro `sub`, `div`, `lt`, `gt` záleží: `3 - 5 ≠ 5 - 3`.

```python
elif op == "div":
    b, a = self.stack.pop(), self.stack.pop()
    if parts[1] == "I":                    # celočíselné dělení
        if b == 0: raise RuntimeError_("Division by zero")
        self.stack.append(int(a // b))     # // = celočíselné dělení v Pythonu
    else:                                  # float dělení
        if b == 0.0: raise RuntimeError_("Division by zero")
        self.stack.append(a / b)
```

### Skoky

```python
elif op == "jmp":
    self.pc = self.labels[int(parts[1])]    # nastav pc na index labelu

elif op == "fjmp":
    val = self.stack.pop()                   # vezmi bool ze zásobníku (a spotřebuj ho)
    if not val:
        self.pc = self.labels[int(parts[1])]  # skoč jen pokud false
```

`fjmp` = "false jump" – skočí jen pokud je vrchol zásobníku `False`.
Vždy popne hodnotu ze zásobníku (ať skočí nebo ne).

### Print

```python
elif op == "print":
    n = int(parts[1])
    values = self.stack[-n:]    # posledních n hodnot (nejstarší první)
    del self.stack[-n:]         # odeber je ze zásobníku
    for val in values:
        self._print_value(val)
    print()                     # newline na konci
```

`self.stack[-n:]` je Python "slice" – vezme posledních n prvků.
Pořadí je správné: nejdřív pushnutá hodnota je na indexu `[-n]`, tedy vytiskne se první.

### Výpis hodnot

```python
def _print_value(self, val):
    if isinstance(val, bool):
        print("true" if val else "false", end="")   # Python tiskne True/False s velkým
    elif isinstance(val, float):
        formatted = f"{val:.10f}".rstrip("0")       # odstraní nuly na konci
        if formatted.endswith("."):
            formatted += "0"                        # ale aspoň jedno des. místo
        print(formatted, end="")
    else:
        print(val, end="")   # int a string přímo
```

`end=""` = netiskni newline za každou hodnotou.
Proč kontrolujeme bool před float? Protože v Pythonu je `bool` podtřídou `int`
(`isinstance(True, int)` je `True`), takže musíme bool zkontrolovat jako první.

### Read

```python
elif op == "read":
    type_suffix = parts[1]
    raw = input()                                  # čte řádek ze stdin
    self.stack.append(self._parse_input(type_suffix, raw))

def _parse_input(self, type_suffix: str, raw: str):
    try:
        if type_suffix == "I":   return int(raw)
        elif type_suffix == "F": return float(raw)
        elif type_suffix == "B":
            if raw.strip().lower() == "true":  return True
            elif raw.strip().lower() == "false": return False
            raise ValueError
        elif type_suffix == "S": return raw    # string = celý řádek
    except ValueError:
        raise RuntimeError_(f"Cannot parse '{raw}' as {type_suffix}")
```

---

# Soubor `main.py` – vstupní bod

```python
import sys
from lexer import Lexer
from parser import Parser
from typechecker import TypeChecker
from codegen import CodeGen
from interpreter import Interpreter

def main():
    source = open(sys.argv[1]).read()         # přečte soubor ze CLI argumentu
    tokens = Lexer(source).tokenize()         # text → tokeny
    ast = Parser(tokens).parse()              # tokeny → AST
    TypeChecker().check(ast)                  # kontrola typů (modifikuje AST!)
    instructions = CodeGen().generate(ast)    # AST → instrukce
    Interpreter(instructions).run()           # vykonání

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
```

`sys.argv[1]` = první argument z příkazové řádky (název souboru).
`try/except` zachytí všechny chyby z libovolné fáze a vytiskne je čitelně.
`file=sys.stderr` = chyby jdou do stderr (standardní chybový výstup), ne stdout.

---

# Jak přidat novou funkci

## Příklad: přidání `for` cyklu

Syntaxe: `for (int i = 0; i < 10; i = i + 1) { ... }`

### 1. `ast_nodes.py` – nový uzel
```python
@dataclass
class For:
    init: Any        # inicializační příkaz (int i = 0)
    condition: Any   # podmínka (i < 10)
    step: Any        # krok (i = i + 1)
    body: Any        # tělo smyčky
```

### 2. `parser.py` – nové parsování
```python
# V _statement():
if tok.type == "for":
    return self._for_stmt()

def _for_stmt(self):
    self._match("for")
    self._match("(")
    init = self._statement()      # int i = 0;
    cond = self._expr()
    self._match(";")
    step = self._expr()
    self._match(")")
    body = self._statement()
    return For(init, cond, step, body)
```

### 3. `typechecker.py` – typová kontrola
```python
def visit_For(self, node: For):
    self.scope.enter()           # for má vlastní scope
    self.visit(node.init)
    cond_type = self.visit(node.condition)
    if cond_type != "bool":
        raise TypeError_("For condition must be bool")
    self.visit(node.step)
    self.visit(node.body)
    self.scope.exit()
```

### 4. `codegen.py` – generování kódu
```python
def visit_For(self, node: For):
    self.visit(node.init)              # inicializace
    start = self.new_label()
    end   = self.new_label()
    self.emit(f"label {start}")
    self.visit(node.condition)
    self.emit(f"fjmp {end}")
    self.visit(node.body)
    self.visit(node.step)              # krok
    self.emit(f"jmp {start}")
    self.emit(f"label {end}")
```

**Nic jiného se nemění.** To je síla visitor patternu.

## Přehled: kde co měnit

| Chci přidat... | Kde upravit |
|---|---|
| Nový příkaz (`for`, `do-while`...) | `ast_nodes.py` + `parser.py` + `visit_X` v TypeCheckeru a CodeGenu |
| Nový operátor | `lexer.py` + správná priorita v `parser.py` + `visit_BinOp` v TypeCheckeru a CodeGenu |
| Nový typ (`char`...) | `ast_nodes.py` literál + `lexer.py` + `TYPE_SUFFIX` v CodeGenu + `_push`/`_parse_input` v Interpretu |
| Změna scopingu | Jen `ScopeManager.exit()` v `typechecker.py` |
| Procedury (label/jmp) | `ast_nodes.py` uzly + vše ostatní; CodeGen generuje label/jmp místo call/return |
