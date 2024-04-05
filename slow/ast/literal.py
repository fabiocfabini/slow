from dataclasses import dataclass

from ..node import ExpressionNode, NodeVisitor


@dataclass
class LiteralIntegerNode(ExpressionNode):
    value: int
    line: int

    def accept(self, visitor: NodeVisitor) -> None:
        visitor.visit_literal_integer(self)

    def __str__(self) -> str:
        return f"{self.value}"
