from dataclasses import dataclass

from .node import Node, NodeVisitor


@dataclass
class GroupingNode(Node):
    expression: Node

    def accept(self, visitor: NodeVisitor) -> None:
        visitor.visit_literal_integer(self)
