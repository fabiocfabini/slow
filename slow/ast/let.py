from dataclasses import dataclass

from ..node import StatementNode, ExpressionNode, NodeVisitor
from .identifier import IdentifierNode


@dataclass
class LetDeclarationNode(StatementNode):
    identifier: IdentifierNode

    def accept(self, visitor: NodeVisitor) -> None:
        visitor.visit_let_declaration(self)

    def __str__(self) -> str:
        return f"let {self.identifier};"


@dataclass
class LetAssignmentNode(StatementNode):
    identifier: IdentifierNode
    expression: ExpressionNode

    def accept(self, visitor: NodeVisitor) -> None:
        visitor.visit_let_assignment(self)

    def __str__(self) -> str:
        return f"let {self.identifier} = {self.expression};"
