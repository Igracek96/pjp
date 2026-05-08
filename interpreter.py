"""Stack machine interpreter: executes generated instructions."""

import sys


class RuntimeError_(Exception):
    pass


class Interpreter:
    def __init__(self, instructions: list):
        self.instructions = instructions
        self.stack = []
        self.variables = {}
        self.labels = {}    # label number -> instruction index
        self.pc = 0         # program counter

        # Pre-scan for labels
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
            name = parts[1]
            self.variables[name] = self.stack.pop()
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
            if parts[1] == "I":
                if b == 0:
                    raise RuntimeError_("Division by zero")
                self.stack.append(int(a // b))
            else:
                if b == 0.0:
                    raise RuntimeError_("Division by zero")
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
            pass  # labels are pre-scanned
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
            print()  # trailing newline
        elif op == "read":
            type_suffix = parts[1]
            raw = input()
            self.stack.append(self._parse_input(type_suffix, raw))
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
            self.stack.append(raw_value)
        else:
            raise RuntimeError_(f"Unknown type suffix '{type_suffix}'")

    def _parse_input(self, type_suffix: str, raw: str):
        try:
            if type_suffix == "I":
                return int(raw)
            elif type_suffix == "F":
                return float(raw)
            elif type_suffix == "B":
                if raw.strip().lower() == "true":
                    return True
                elif raw.strip().lower() == "false":
                    return False
                raise ValueError
            elif type_suffix == "S":
                return raw
        except ValueError:
            raise RuntimeError_(f"Cannot parse '{raw}' as {type_suffix}")

    def _print_value(self, val):
        if isinstance(val, bool):
            print("true" if val else "false", end="")
        elif isinstance(val, float):
            # Print without trailing zeros but keep at least one decimal
            formatted = f"{val:.10f}".rstrip("0")
            if formatted.endswith("."):
                formatted += "0"
            print(formatted, end="")
        else:
            print(val, end="")
