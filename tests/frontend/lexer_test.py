from slow.frontend.lexer import Lexer
from slow.frontend.lexeme import TokenKind

def test_empty() -> None:
    lexer = Lexer("")

    for _ in range(10):
        assert lexer.next().kind == TokenKind.EOF

def test_whitespace() -> None:
    lexer = Lexer("     ")

    for _ in range(10):
        assert lexer.next().kind == TokenKind.EOF

def test_expression() -> None:
    lexer = Lexer("1 + 2")

    assert lexer.next().kind == TokenKind.INTEGER
    assert lexer.next().kind == TokenKind.ADD
    assert lexer.next().kind == TokenKind.INTEGER

    for _ in range(10):
        assert lexer.next().kind == TokenKind.EOF
