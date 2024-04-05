from dataclasses import dataclass

from ..node import Node, NodeVisitor


@dataclass
class IdentifierNode(Node):
    name: str
    # NOTE: Only supports integer types

    def accept(self, visitor: NodeVisitor) -> None:
        visitor.visit_identifier(self)

    def __str__(self) -> str:
        return self.name

    def __hash__(self) -> int:
        return hash(self.name)
