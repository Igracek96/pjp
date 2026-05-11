# PLC Compiler

Překladač a interpret jednoduchého programovacího jazyka implementovaný v Pythonu s použitím ANTLR4.
Školní projekt na VŠB-TUO, předmět Překladače (PLC).

## Požadavky

- Python 3.x
- `antlr4-python3-runtime` (`pip install antlr4-python3-runtime`)
- Java + ANTLR4 JAR (pouze pro regeneraci gramatiky)

## Spuštění

```bash
# Kompilace a okamžité spuštění
python3 main.py program.plc

# Pouze kompilace do souboru instrukcí
python3 main.py --compile program.plc    # → program.ins

# Spuštění existujícího souboru instrukcí
python3 main.py --run program.ins
```

## Regenerace ANTLR souborů

```bash
java -jar antlr-4.13.2-complete.jar -Dlanguage=Python3 -visitor -no-listener PLC.g4
```

## Architektura

```
zdrojový kód (.plc)
      ↓
  ANTLR4 (PLCLexer + PLCParser)  – text → parse tree
      ↓
  ast_builder.py   – parse tree → AST (náš strom)
      ↓
  typechecker.py   – kontrola typů, konverze int→float
      ↓
  codegen.py       – AST → instrukce zásobníkového stroje
      ↓
  interpreter.py   – vykonání instrukcí
```

## Podporovaný jazyk

**Datové typy:** `int`, `float`, `bool`, `string`

**Příkazy:**
```
int a, b;              // deklarace proměnných
a = 5;                 // přiřazení
write "výsledek:", a;  // výpis
read a;                // čtení ze stdin
if (a > 0) { ... }    // podmínka
while (a < 10) { ... } // smyčka
{ ... }                // blok (vlastní scope)
```

**Operátory (od nejvyšší priority):**
- `*`, `/`, `%` – násobení, dělení, modulo
- `+`, `-`, `.` – sčítání, odčítání, konkatenace
- `<`, `>` – porovnání
- `==`, `!=` – rovnost
- `&&` – logický AND
- `||` – logický OR
- `=` – přiřazení (pravá asociativita)

**Typová pravidla:**
- Automatická konverze `int → float` (např. `1.5 + 3` = `4.5`)
- Konverze `float → int` není povolena

## Soubory

| Soubor | Popis |
|---|---|
| `PLC.g4` | ANTLR4 gramatika (lexer + parser) |
| `PLCLexer.py` | Vygenerovaný lexer (ANTLR) |
| `PLCParser.py` | Vygenerovaný parser (ANTLR) |
| `PLCVisitor.py` | Vygenerovaný visitor (ANTLR) |
| `ast_builder.py` | Převod parse tree → AST |
| `ast_nodes.py` | Definice uzlů AST stromu |
| `typechecker.py` | Typová kontrola + správa scopů |
| `codegen.py` | Generátor instrukcí |
| `interpreter.py` | Zásobníkový stroj |
| `main.py` | Vstupní bod, pipeline |
| `DOKUMENTACE.md` | Detailní vysvětlení celého kódu |

## Testování

```bash
python3 main.py test1.in          # konstanty, výrazy, vstup/výstup
python3 main.py test2.in          # relační a logické operátory
echo "3" | python3 main.py test3.in   # if/else, while
python3 main.py test_errors.in    # typové chyby
```
