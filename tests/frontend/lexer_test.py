import pytest

from slow.frontend.lexer import Lexer
from slow.frontend.lexeme import TokenKind, Token


def test_empty() -> None:
    lexer = Lexer("")

    for _ in range(10):
        assert lexer.next().kind == TokenKind.EOF

def test_lines() -> None:
    lexer = Lexer("""
        1
        12
        123
    """)

    assert lexer.next() == Token(TokenKind.INTEGER, 1, 1)
    assert lexer.next() == Token(TokenKind.INTEGER, 12, 2)
    assert lexer.next() == Token(TokenKind.INTEGER, 123, 3)

def test_whitespace() -> None:
    lexer = Lexer("     ")

    for _ in range(10):
        assert lexer.next().kind == TokenKind.EOF

@pytest.mark.parametrize("text,token", [
    ("123", Token(TokenKind.INTEGER, 123, 0)),
    ("+", Token(TokenKind.ADD, None, 0)),
    ("-", Token(TokenKind.SUB, None, 0)),
])
def test_single(text: str, token: Token) -> None:
    lexer = Lexer(text)

    assert lexer.next() == token