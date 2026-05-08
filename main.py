"""PLC Compiler - main entry point."""

import sys
from lexer import Lexer
from parser import Parser
from typechecker import TypeChecker
from codegen import CodeGen
from interpreter import Interpreter


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <source_file>", file=sys.stderr)
        sys.exit(1)

    source = open(sys.argv[1]).read()

    try:
        tokens = Lexer(source).tokenize()
        ast = Parser(tokens).parse()
        TypeChecker().check(ast)
        instructions = CodeGen().generate(ast)
        Interpreter(instructions).run()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
