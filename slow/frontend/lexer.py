from dataclasses import dataclass

from .lexeme import Token, TokenKind, TokenValue


@dataclass(slots=True)
class Lexer:
    source: str
    start: int = 0
    current: int = 0
    line: int = 1

    def next(self) -> Token:
        self._skip_whitespace()

        token: Token
        if self._is_at_end():
            return self._make_token(TokenKind.EOF)
        char: str = self._peek()
        if char.isdigit():
            return self._number()

        match char:
            case "+":
                token = self._make_token(TokenKind.ADD)
                self._advance()
            case "-":
                token = self._make_token(TokenKind.SUB)
                self._advance()
            case _:
                token = self._make_error(f"Unexpected character: {char}")
                self._advance()

        self._rebase()
        return token

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
                    if self._peek() == "/":
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
        return Token(kind, value, self.line)

    def _make_error(self, msg: str) -> Token:
        # TODO: Improve reporting (file:line:column lex error: msg)
        return self._make_token(TokenKind.ERROR, f"{msg} at line {self.line}")

    def _number(self) -> Token:
        while not self._is_at_end() and self._peek().isdigit():
            self._advance()

        value: int = int(self.source[self.start : self.current])
        self._rebase()

        return self._make_token(TokenKind.INTEGER, value)


if __name__ == "__main__":
    lexer = Lexer("1-12+123")

    while (tok := lexer.next()).kind != TokenKind.EOF:
        print(tok)

    print(tok)
