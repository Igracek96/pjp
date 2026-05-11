"""
PLC Compiler & Interpreter

Usage:
  python3 main.py source.plc              compile and run immediately
  python3 main.py --compile source.plc    compile to source.ins (instruction file)
  python3 main.py --run source.ins        run an instruction file
"""

import sys
from lexer import Lexer
from parser import Parser
from typechecker import TypeChecker, TypeError_
from codegen import CodeGen
from interpreter import Interpreter, load_instructions


def compile_source(source_path: str) -> list:
    """Compile a source file to a list of instructions."""
    source = open(source_path).read()
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    TypeChecker().check(ast)          # prints all type errors, then raises TypeError_
    return CodeGen().generate(ast)


def main():
    args = sys.argv[1:]

    if not args:
        print(__doc__)
        sys.exit(1)

    if args[0] == "--compile":
        # Compile source to instruction file (.ins)
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
        # Run an instruction file directly
        if len(args) < 2:
            print("Usage: python3 main.py --run source.ins", file=sys.stderr)
            sys.exit(1)
        instructions = load_instructions(args[1])
        Interpreter(instructions).run()

    else:
        # Default: compile source and run immediately (in memory)
        instructions = compile_source(args[0])
        Interpreter(instructions).run()


if __name__ == "__main__":
    try:
        main()
    except TypeError_:
        sys.exit(1)     # errors already printed by TypeChecker.check()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
