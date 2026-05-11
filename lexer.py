"""Lexer: source code -> list of tokens."""

from dataclasses import dataclass
from typing import List


@dataclass
class Token:
    type: str
    value: str
    line: int = 0


KEYWORDS = {"int", "float", "bool", "string", "true", "false",
            "if", "else", "while", "read", "write"}

# Two-character operators must be checked before single-character ones
TWO_CHAR_OPS = {"==", "!=", "||", "&&"}
ONE_CHAR_OPS = {"+", "-", "*", "/", "%", ".", "!", "<", ">", "=",
                "(", ")", "{", "}", ",", ";"}


class LexerError(Exception):
    pass


class Lexer:
    def __init__(self, source: str):
        # Strip BOM if present (some editors add it to UTF-8 files)
        self.source = source.lstrip('\ufeff')
        self.pos = 0
        self.line = 1

    def tokenize(self) -> List[Token]:
        tokens = []
        while self.pos < len(self.source):
            ch = self.source[self.pos]

            # Whitespace
            if ch in " \t\r":
                self.pos += 1
                continue
            if ch == "\n":
                self.line += 1
                self.pos += 1
                continue

            # Single-line comment //
            if ch == "/" and self.pos + 1 < len(self.source) and self.source[self.pos + 1] == "/":
                while self.pos < len(self.source) and self.source[self.pos] != "\n":
                    self.pos += 1
                continue

            # String literal
            if ch == '"':
                tokens.append(self._read_string())
                continue

            # Number literal (int or float)
            if ch.isdigit():
                tokens.append(self._read_number())
                continue

            # Identifier or keyword (letters and digits only, must start with letter)
            if ch.isalpha():
                tokens.append(self._read_ident())
                continue

            # Two-character operators
            if self.pos + 1 < len(self.source):
                two = self.source[self.pos:self.pos + 2]
                if two in TWO_CHAR_OPS:
                    tokens.append(Token(two, two, self.line))
                    self.pos += 2
                    continue

            # Single-character operators/punctuation
            if ch in ONE_CHAR_OPS:
                tokens.append(Token(ch, ch, self.line))
                self.pos += 1
                continue

            raise LexerError(f"Line {self.line}: unexpected character '{ch}'")

        tokens.append(Token("EOF", "", self.line))
        return tokens

    def _read_string(self) -> Token:
        line = self.line
        self.pos += 1  # skip opening quote
        start = self.pos
        result = []
        while self.pos < len(self.source) and self.source[self.pos] != '"':
            if self.source[self.pos] == "\\":
                self.pos += 1
                if self.pos >= len(self.source):
                    raise LexerError(f"Line {line}: unterminated string")
                esc = self.source[self.pos]
                if esc == "n":
                    result.append("\n")
                elif esc == "t":
                    result.append("\t")
                elif esc == "\\":
                    result.append("\\")
                elif esc == '"':
                    result.append('"')
                else:
                    result.append(esc)
            else:
                if self.source[self.pos] == "\n":
                    self.line += 1
                result.append(self.source[self.pos])
            self.pos += 1
        if self.pos >= len(self.source):
            raise LexerError(f"Line {line}: unterminated string")
        self.pos += 1  # skip closing quote
        return Token("STRING", "".join(result), line)

    def _read_number(self) -> Token:
        line = self.line
        start = self.pos
        while self.pos < len(self.source) and self.source[self.pos].isdigit():
            self.pos += 1
        if self.pos < len(self.source) and self.source[self.pos] == ".":
            # Check it's not the concat operator after an int (e.g. 3.14 vs expression)
            if self.pos + 1 < len(self.source) and self.source[self.pos + 1].isdigit():
                self.pos += 1  # skip dot
                while self.pos < len(self.source) and self.source[self.pos].isdigit():
                    self.pos += 1
                return Token("FLOAT", self.source[start:self.pos], line)
        return Token("INT", self.source[start:self.pos], line)

    def _read_ident(self) -> Token:
        line = self.line
        start = self.pos
        while self.pos < len(self.source) and self.source[self.pos].isalnum():
            self.pos += 1
        word = self.source[start:self.pos]
        if word in KEYWORDS:
            return Token(word, word, line)
        return Token("ID", word, line)
