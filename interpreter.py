"""Stack machine interpreter: executes generated instructions.
Can run from a list of instructions (in-memory) or from a .ins text file."""

import sys


class RuntimeError_(Exception):
    pass


def load_instructions(path: str) -> list:
    """Read an instruction file and return a list of instruction strings."""
    with open(path) as f:
        return [line.rstrip("\n") for line in f if line.strip()]


class Interpreter:
    def __init__(self, instructions: list):
        self.instructions = instructions
        self.stack = []
        self.variables = {}
        self.labels = {}    # label number -> instruction index
        self.pc = 0

        # Pre-scan for labels so jmp/fjmp can jump forward
        for i, instr in enumerate(self.instructions):
            if instr.startswith("label "):
                label_num = int(instr.split()[1])
                self.labels[label_num] = i

    def run(self):
        while self.pc < len(self.instructions):
            instr = self.instructions[self.pc]
            self.pc += 1
            self._execute(instr)

    def _execute(self, instr: str):
        # Split into at most 3 parts so "push S hello world" keeps the string intact
        parts = instr.split(" ", 2)
        op = parts[0]

        if op == "push":
            self._push(parts[1], parts[2] if len(parts) > 2 else "")
        elif op == "pop":
            self.stack.pop()
        elif op == "load":
            name = parts[1]
            if name not in self.variables:
                raise RuntimeError_(f"Undefined variable '{name}'")
            self.stack.append(self.variables[name])
        elif op == "save":
            self.variables[parts[1]] = self.stack.pop()
        elif op == "add":
            b, a = self.stack.pop(), self.stack.pop()
            self.stack.append(a + b)
        elif op == "sub":
            b, a = self.stack.pop(), self.stack.pop()
            self.stack.append(a - b)
        elif op == "mul":
            b, a = self.stack.pop(), self.stack.pop()
            self.stack.append(a * b)
        elif op == "div":
            b, a = self.stack.pop(), self.stack.pop()
            if b == 0 or b == 0.0:
                raise RuntimeError_("Division by zero")
            if parts[1] == "I":
                self.stack.append(int(a // b))
            else:
                self.stack.append(a / b)
        elif op == "mod":
            b, a = self.stack.pop(), self.stack.pop()
            if b == 0:
                raise RuntimeError_("Modulo by zero")
            self.stack.append(a % b)
        elif op == "uminus":
            self.stack.append(-self.stack.pop())
        elif op == "concat":
            b, a = self.stack.pop(), self.stack.pop()
            self.stack.append(a + b)
        elif op == "and":
            b, a = self.stack.pop(), self.stack.pop()
            self.stack.append(a and b)
        elif op == "or":
            b, a = self.stack.pop(), self.stack.pop()
            self.stack.append(a or b)
        elif op == "not":
            self.stack.append(not self.stack.pop())
        elif op == "gt":
            b, a = self.stack.pop(), self.stack.pop()
            self.stack.append(a > b)
        elif op == "lt":
            b, a = self.stack.pop(), self.stack.pop()
            self.stack.append(a < b)
        elif op == "eq":
            b, a = self.stack.pop(), self.stack.pop()
            self.stack.append(a == b)
        elif op == "itof":
            self.stack.append(float(self.stack.pop()))
        elif op == "label":
            pass    # labels already pre-scanned
        elif op == "jmp":
            self.pc = self.labels[int(parts[1])]
        elif op == "fjmp":
            val = self.stack.pop()
            if not val:
                self.pc = self.labels[int(parts[1])]
        elif op == "print":
            n = int(parts[1])
            values = self.stack[-n:]
            del self.stack[-n:]
            for val in values:
                self._print_value(val)
            print()     # trailing newline after last value
        elif op == "read":
            raw = input()
            self.stack.append(self._parse_input(parts[1], raw))
        else:
            raise RuntimeError_(f"Unknown instruction: {instr}")

    def _push(self, type_suffix: str, raw_value: str):
        if type_suffix == "I":
            self.stack.append(int(raw_value))
        elif type_suffix == "F":
            self.stack.append(float(raw_value))
        elif type_suffix == "B":
            self.stack.append(raw_value == "true")
        elif type_suffix == "S":
            # Strings in instruction files are quoted: "hello world"
            # Strip surrounding quotes and unescape sequences.
            if len(raw_value) >= 2 and raw_value[0] == '"' and raw_value[-1] == '"':
                s = raw_value[1:-1]
                s = s.replace('\\"', '"').replace('\\n', '\n').replace('\\t', '\t').replace('\\\\', '\\')
                self.stack.append(s)
            else:
                self.stack.append(raw_value)    # fallback: unquoted (shouldn't happen)
        else:
            raise RuntimeError_(f"Unknown type suffix '{type_suffix}'")

    def _parse_input(self, type_suffix: str, raw: str):
        try:
            if type_suffix == "I":   return int(raw)
            elif type_suffix == "F": return float(raw)
            elif type_suffix == "B":
                if raw.strip().lower() == "true":  return True
                if raw.strip().lower() == "false": return False
                raise ValueError
            elif type_suffix == "S": return raw
        except ValueError:
            raise RuntimeError_(f"Cannot parse '{raw}' as type {type_suffix}")

    def _print_value(self, val):
        if isinstance(val, bool):
            # bool must be checked before int (bool is a subclass of int in Python)
            print("true" if val else "false", end="")
        elif isinstance(val, float):
            formatted = f"{val:.10f}".rstrip("0")
            if formatted.endswith("."):
                formatted += "0"
            print(formatted, end="")
        else:
            print(val, end="")
