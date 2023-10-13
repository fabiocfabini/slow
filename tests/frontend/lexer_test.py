from slow.frontend.lexer import Lexer
from slow.frontend.lexeme import TokenKind, Token

def test_empty() -> None:
    lexer = Lexer("")

    for _ in range(10):
        assert lexer.next().kind == TokenKind.EOF

def test_whitespace() -> None:
    lexer = Lexer("     ")

    for _ in range(10):
        assert lexer.next().kind == TokenKind.EOF

def test_seperated_tokens() -> None:
    lexer = Lexer("1 12 123 + -")

    assert lexer.next() == Token(TokenKind.INTEGER, 1, 0)
    assert lexer.next() == Token(TokenKind.INTEGER, 12, 0)
    assert lexer.next() == Token(TokenKind.INTEGER, 123, 0)
    assert lexer.next() == Token(TokenKind.ADD, None, 0)
    assert lexer.next() == Token(TokenKind.SUB, None, 0)

    for _ in range(10):
        assert lexer.next().kind == TokenKind.EOF

def test_non_seperated_tokens() -> None:
    lexer = Lexer("1-12+123")

    assert lexer.next() == Token(TokenKind.INTEGER, 1, 0)
    assert lexer.next() == Token(TokenKind.SUB, None, 0)
    assert lexer.next() == Token(TokenKind.INTEGER, 12, 0)
    assert lexer.next() == Token(TokenKind.ADD, None, 0)
    assert lexer.next() == Token(TokenKind.INTEGER, 123, 0)

    for _ in range(10):
        assert lexer.next().kind == TokenKind.EOF
