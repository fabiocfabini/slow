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

    assert lexer.next() == Token(TokenKind.INTEGER, 1, 2, (9, 11))
    assert lexer.next() == Token(TokenKind.INTEGER, 12, 3, (40, 43))
    assert lexer.next() == Token(TokenKind.INTEGER, 123, 4, (78, 82))

def test_whitespace() -> None:
    lexer = Lexer("     ")

    for _ in range(10):
        assert lexer.next().kind == TokenKind.EOF

@pytest.mark.parametrize("text,token", [
    ("// This is a comment", Token(TokenKind.EOF, None, 1, (20, 21))),
    ("(", Token(TokenKind.LPAREN, None, 1, (0, 1))),
    (")", Token(TokenKind.RPAREN, None, 1, (0, 1))),
    ("123", Token(TokenKind.INTEGER, 123, 1, (0, 4))),
    ("+", Token(TokenKind.ADD, None, 1, (0, 1))),
    ("-", Token(TokenKind.SUB, None, 1, (0, 1))),
    ("*", Token(TokenKind.MUL, None, 1, (0, 1))),
    ("/", Token(TokenKind.DIV, None, 1, (0, 1))),
])
def test_single(text: str, token: Token) -> None:
    lexer = Lexer(text)

    assert lexer.next() == token