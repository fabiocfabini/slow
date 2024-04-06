from dataclasses import dataclass

from ..node import StatementNode, ExpressionNode, NodeVisitor
from .identifier import IdentifierNode


@dataclass
class AssignNode(StatementNode):
    identifier: IdentifierNode
    expression: ExpressionNode

    def accept(self, visitor: NodeVisitor) -> None:
        visitor.visit_assign(self)

    def __str__(self) -> str:
        return f"{self.identifier} = {self.expression};"
