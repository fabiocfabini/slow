from slow.frontend.parser import Parser

from slow.ast.literal import LiteralIntegerNode
from slow.ast.grouping import GroupingNode
from slow.ast.binary import BinaryNode, BinaryOperator

def test_expression() -> None:
    parser = Parser()

    ast = None

    assert parser.parse("(1 + 2) *\n ") == ast