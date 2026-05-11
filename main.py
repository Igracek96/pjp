"""
PLC Compiler & Interpreter (ANTLR-based)

Usage:
  python3 main.py source.plc              compile and run immediately
  python3 main.py --compile source.plc    compile to source.ins (instruction file)
  python3 main.py --run source.ins        run an instruction file
"""

import sys
from antlr4 import CommonTokenStream, InputStream
from antlr4.error.ErrorListener import ErrorListener

from PLCLexer import PLCLexer
from PLCParser import PLCParser
from ast_builder import ASTBuilder
from typechecker import TypeChecker, TypeError_
from codegen import CodeGen
from interpreter import Interpreter, load_instructions


class SyntaxErrorCollector(ErrorListener):
    """Collects all ANTLR syntax errors instead of printing them immediately."""

    def __init__(self):
        super().__init__()
        self.errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.errors.append(f"Line {line}:{column} {msg}")


def compile_source(source_path: str) -> list:
    """Compile a source file to a list of instructions."""
    source = open(source_path).read()

    # Strip BOM if present
    if source.startswith('\ufeff'):
        source = source[1:]

    # 1. Lexing + Parsing (ANTLR)
    input_stream = InputStream(source)
    lexer = PLCLexer(input_stream)
    lexer.removeErrorListeners()
    lex_errors = SyntaxErrorCollector()
    lexer.addErrorListener(lex_errors)

    token_stream = CommonTokenStream(lexer)
    parser = PLCParser(token_stream)
    parser.removeErrorListeners()
    parse_errors = SyntaxErrorCollector()
    parser.addErrorListener(parse_errors)

    tree = parser.program()

    # Report syntax errors and stop
    all_syntax_errors = lex_errors.errors + parse_errors.errors
    if all_syntax_errors:
        for err in all_syntax_errors:
            print(f"Syntax error: {err}", file=sys.stderr)
        sys.exit(1)

    # 2. Build AST from parse tree
    ast = ASTBuilder().visit(tree)

    # 3. Type checking (reports ALL type errors, then raises TypeError_)
    TypeChecker().check(ast)

    # 4. Code generation
    return CodeGen().generate(ast)


def main():
    args = sys.argv[1:]

    if not args:
        print(__doc__)
        sys.exit(1)

    if args[0] == "--compile":
        if len(args) < 2:
            print("Usage: python3 main.py --compile source.plc", file=sys.stderr)
            sys.exit(1)
        source_path = args[1]
        out_path = source_path.rsplit(".", 1)[0] + ".ins"
        instructions = compile_source(source_path)
        with open(out_path, "w") as f:
            f.write("\n".join(instructions) + "\n")
        print(f"Compiled to {out_path}")

    elif args[0] == "--run":
        if len(args) < 2:
            print("Usage: python3 main.py --run source.ins", file=sys.stderr)
            sys.exit(1)
        instructions = load_instructions(args[1])
        Interpreter(instructions).run()

    else:
        # Default: compile and run
        instructions = compile_source(args[0])
        Interpreter(instructions).run()


if __name__ == "__main__":
    try:
        main()
    except TypeError_:
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
