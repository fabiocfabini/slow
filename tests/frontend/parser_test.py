from slow.frontend.parser import Parser

from slow.ast.literal import LiteralIntegerNode
from slow.ast.binary import BinaryNode, BinaryOperator

def test_expression() -> None:
    parser = Parser()

    ast = BinaryNode(
        BinaryNode(
            LiteralIntegerNode(1, 1),
            LiteralIntegerNode(2, 1),
            BinaryOperator.ADD,
        ),
        LiteralIntegerNode(2, 1),
        BinaryOperator.MUL,
    )

    assert parser.parse("(1 + 2) * 2 ") == ast