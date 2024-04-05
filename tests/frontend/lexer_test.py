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

    assert lexer.next() == Token(TokenKind.INTEGER, 1, 2, slice(9, 10))
    assert lexer.next() == Token(TokenKind.INTEGER, 12, 3, slice(40, 42))
    assert lexer.next() == Token(TokenKind.INTEGER, 123, 4, slice(78, 81))

def test_whitespace() -> None:
    lexer = Lexer("     ")

    for _ in range(10):
        assert lexer.next().kind == TokenKind.EOF

@pytest.mark.parametrize("text,token", [
    ("// This is a comment", Token(TokenKind.EOF, None, 1, slice(20, 20))),
    ("(", Token(TokenKind.LPAREN, None, 1, slice(0, 1))),
    (")", Token(TokenKind.RPAREN, None, 1, slice(0, 1))),
    ("123", Token(TokenKind.INTEGER, 123, 1, slice(0, 3))),
    ("+", Token(TokenKind.ADD, None, 1, slice(0, 1))),
    ("-", Token(TokenKind.SUB, None, 1, slice(0, 1))),
    ("*", Token(TokenKind.MUL, None, 1, slice(0, 1))),
    ("/", Token(TokenKind.DIV, None, 1, slice(0, 1))),
    ("true", Token(TokenKind.TRUE, None, 1, slice(0, 4))),
    ("false", Token(TokenKind.FALSE, None, 1, slice(0, 5))),
    ("x", Token(TokenKind.ID, "x", 1, slice(0, 1))),
    ("_m12m12_12", Token(TokenKind.ID, "_m12m12_12", 1, slice(0, 10))),
])
def test_single(text: str, token: Token) -> None:
    lexer = Lexer(text)

    assert lexer.next() == token


@pytest.mark.parametrize("text,tokens", [
    ("+-*/()1true false _m12m12_12", [
        Token(TokenKind.ADD, None, 1, slice(0, 1)),
        Token(TokenKind.SUB, None, 1, slice(1, 2)),
        Token(TokenKind.MUL, None, 1, slice(2, 3)),
        Token(TokenKind.DIV, None, 1, slice(3, 4)),
        Token(TokenKind.LPAREN, None, 1, slice(4, 5)),
        Token(TokenKind.RPAREN, None, 1, slice(5, 6)),
        Token(TokenKind.INTEGER, 1, 1, slice(6, 7)),
        Token(TokenKind.TRUE, None, 1, slice(7, 11)),
        Token(TokenKind.FALSE, None, 1, slice(12, 17)),
        Token(TokenKind.ID, "_m12m12_12", 1, slice(18, 28)),
    ]),
])
def test_multiple(text: str, tokens: list[Token]) -> None:
    lexer = Lexer(text)

    for token in tokens:
        assert lexer.next() == token
