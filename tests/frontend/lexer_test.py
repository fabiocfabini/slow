import pytest

from slow.frontend.lexer import Lexer
from slow.frontend.lexeme import TokenKind, Token


def test_empty() -> None:
    lexer = Lexer("")

    for _ in range(10):
        assert lexer.next().kind == TokenKind.EOF

def test_lines() -> None:
    lexer = Lexer("""
        1 // This is a comment
        12 // This is another comment
        123 // This is a third comment
    """)

    assert lexer.next() == Token(TokenKind.INTEGER, 1, 2)
    assert lexer.next() == Token(TokenKind.INTEGER, 12, 3)
    assert lexer.next() == Token(TokenKind.INTEGER, 123, 4)

def test_whitespace() -> None:
    lexer = Lexer("     ")

    for _ in range(10):
        assert lexer.next().kind == TokenKind.EOF

@pytest.mark.parametrize("text,token", [
    ("// This is a comment", Token(TokenKind.EOF, None, 1)),
    ("123", Token(TokenKind.INTEGER, 123, 1)),
    ("+", Token(TokenKind.ADD, None, 1)),
    ("-", Token(TokenKind.SUB, None, 1)),
])
def test_single(text: str, token: Token) -> None:
    lexer = Lexer(text)

    assert lexer.next() == token