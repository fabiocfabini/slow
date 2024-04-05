from typing import ClassVar
from dataclasses import dataclass, field
from string import ascii_letters

from .lexeme import Token, TokenKind, TokenValue


@dataclass(slots=True)
class Lexer:
    source: str
    start: int = 0
    current: int = 0
    line: int = 1
    _head_identifier_chars: ClassVar[set[str]] = field(init=False, default=set(ascii_letters) | {"_"})
    _tail_identifier_chars: ClassVar[set[str]] = field(init=False, default=set(ascii_letters) | set("0123456789") | {"_"})

    def next(self) -> Token:
        self._skip_whitespace()

        token: Token
        if self._is_at_end():
            return self._make_token(TokenKind.EOF)
        char = self._peek()
        if char.isdigit():
            return self._number()
        if char in self._head_identifier_chars:
            return self._identifier()

        match char:
            case "(":
                self._advance()
                token = self._make_token(TokenKind.LPAREN)
            case ")":
                self._advance()
                token = self._make_token(TokenKind.RPAREN)
            case "+":
                self._advance()
                token = self._make_token(TokenKind.ADD)
            case "-":
                self._advance()
                token = self._make_token(TokenKind.SUB)
            case "*":
                self._advance()
                token = self._make_token(TokenKind.MUL)
            case "/":
                self._advance()
                token = self._make_token(TokenKind.DIV)
            case _:
                self._advance()
                token = self._make_error(f"Unexpected character: {char}")

        self._rebase()
        return token

    def lexeme_at_token(self, token: Token) -> str:
        return self.source[token.span]

    def _is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def _rebase(self) -> None:
        self.start = self.current

    def _advance(self) -> None:
        self.current += 1

    def _regress(self) -> None:
        self.current -= 1

    def _peek(self) -> str:
        return self.source[self.current]

    def _peek_next(self) -> str:
        return self.source[self.current + 1]

    def _peek_offset(self, offset: int) -> str:
        return self.source[self.start + offset]

    def _skip_whitespace(self) -> None:
        while not self._is_at_end():
            match self._peek():
                case " " | "\r" | "\t":
                    self._advance()
                case "\n":
                    self.line += 1
                    self._advance()
                case "/":
                    self._advance()
                    if not self._is_at_end() and self._peek() == "/":
                        self._advance()
                        while not self._is_at_end() and self._peek() != "\n":
                            self._advance()
                    else:
                        self._regress()
                        return
                case _:
                    break

        self._rebase()

    def _make_token(self, kind: TokenKind, value: TokenValue = None) -> Token:
        return Token(kind, value, self.line, slice(self.start, self.current))

    def _make_error(self, msg: str) -> Token:
        # TODO: Improve reporting (file:line:column lex error: msg)
        return self._make_token(TokenKind.ERROR, f"{msg}")

    def _number(self) -> Token:
        while not self._is_at_end() and self._peek().isdigit():
            self._advance()

        value: int = int(self.source[self.start : self.current])
        token = self._make_token(TokenKind.INTEGER, value)

        self._rebase()
        return token

    def _make_id_or_keyword(self, value: str) -> Token:
        match value:
            case "true":
                return self._make_token(TokenKind.TRUE)
            case "false":
                return self._make_token(TokenKind.FALSE)
            case _:
                return self._make_token(TokenKind.ID, value)

    def _identifier(self) -> Token:
        while not self._is_at_end() and self._peek() in self._tail_identifier_chars:
            self._advance()

        value: str = self.source[self.start : self.current]
        token = self._make_id_or_keyword(value)

        self._rebase()
        return token
