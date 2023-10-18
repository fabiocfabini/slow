import pytest

from slow.frontend.parser import Parser

from slow.ast.node import Node
from slow.ast.literal import LiteralIntegerNode
from slow.ast.binary import BinaryNode, BinaryOperator
from slow._exceptions import ParserError, LexerError


class TestLexerError:
    @pytest.mark.xfail()
    @pytest.mark.parametrize("expression, expected_error_message", [
        ("1 + º", "Unexpected character: 'º'"),
        ("1 + 2 º", "Unexpected character: 'º'"),
        ("1 + 2 * º", "Unexpected character: 'º'"),
    ])
    def test_expected_integer_fail(self, expression: str, expected_error_message: str) -> None:
        with pytest.raises(LexerError) as excinfo:
            Parser(True).parse(expression)

        assert expected_error_message == str(excinfo.value)


class TestParserError:
    @pytest.mark.xfail()
    def test_missing_rparen_fail(self) -> None:
        with pytest.raises(ParserError) as excinfo:
            Parser(True).parse("1 + (2")

        assert "Expected ')' after expression. Got ''" == str(excinfo.value)

    @pytest.mark.xfail()
    @pytest.mark.parametrize("expression, expected_error_message", [
        ("1 +", "Expected expression. Got ''"),
        ("1 + -", "Expected expression. Got '-'"),
    ])
    def test_expected_expression_fail(self, expression: str, expected_error_message: str) -> None:
        with pytest.raises(ParserError) as excinfo:
            Parser(True).parse(expression)

        assert expected_error_message == str(excinfo.value)


class TestParserExpression:
    @pytest.mark.parametrize("expression, expected", [
        (
            "1", 
            LiteralIntegerNode(1, 1)
        ),
    ])
    def test_primary_expression(self, expression: str, expected: Node) -> None:
        assert expected == Parser(True).parse(expression)

    @pytest.mark.parametrize("expression, expected", [
        (
            "1 + 2",
            BinaryNode(
                LiteralIntegerNode(1, 1), 
                LiteralIntegerNode(2, 1), 
                BinaryOperator.ADD
            )
        ),
        (
            "1 + 2 * 2",
            BinaryNode(
                LiteralIntegerNode(1, 1),
                BinaryNode(
                    LiteralIntegerNode(2, 1), 
                    LiteralIntegerNode(2, 1),
                    BinaryOperator.MUL
                ),
                BinaryOperator.ADD
            )
        ),
        (
            "(1 + 2) * 2",
            BinaryNode(
                BinaryNode(
                    LiteralIntegerNode(1, 1),
                    LiteralIntegerNode(2, 1),
                    BinaryOperator.ADD
                ),
                LiteralIntegerNode(2, 1),
                BinaryOperator.MUL
            )
        ),
    ])
    def test_binary_expression(self, expression: str, expected: Node) -> None:
        assert expected == Parser(True).parse(expression)
