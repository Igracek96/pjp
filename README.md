# PLC Compiler

Překladač a interpret jednoduchého programovacího jazyka implementovaný v Pythonu.
Školní projekt na VŠB-TUO, předmět Překladače (PLC).

## Spuštění

```bash
python3 main.py program.txt
```

## Architektura

```
zdrojový kód
      ↓
  lexer.py       – text → tokeny
      ↓
  parser.py      – tokeny → AST (strom programu)
      ↓
  typechecker.py – kontrola typů, přejmenování proměnných
      ↓
  codegen.py     – AST → instrukce zásobníkového stroje
      ↓
  interpreter.py – vykonání instrukcí
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

**Operátory:**
- Aritmetické: `+`, `-`, `*`, `/`, `%`
- Řetězcové: `.` (konkatenace)
- Porovnávací: `<`, `>`, `==`, `!=`
- Logické: `&&`, `||`, `!`
- Přiřazení: `=` (pravá asociativita, řetězení: `a = b = 5`)

**Typová pravidla:**
- Automatická konverze `int → float` (např. `1.5 + 3` = `4.5`)
- Konverze `float → int` není povolena

## Příklad programu

```
int i;
while (i < 5) {
    write "i = ", i;
    i = i + 1;
}
```

Výstup:
```
i = 0
i = 1
i = 2
i = 3
i = 4
```

## Soubory

| Soubor | Popis |
|---|---|
| `main.py` | Vstupní bod, pipeline |
| `lexer.py` | Lexer – text na tokeny |
| `parser.py` | Recursive descent parser |
| `ast_nodes.py` | Definice uzlů AST stromu |
| `typechecker.py` | Typová kontrola + správa scopů |
| `codegen.py` | Generátor instrukcí |
| `interpreter.py` | Zásobníkový stroj |
| `DOKUMENTACE.md` | Detailní vysvětlení celého kódu |

## Testování

```bash
python3 main.py test1.in          # konstanty, výrazy, vstup/výstup
python3 main.py test2.in          # relační a logické operátory
echo "3" | python3 main.py test3.in   # if/else, while
python3 main.py test_errors.in    # typové chyby
```
