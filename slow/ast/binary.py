from dataclasses import dataclass
from enum import Enum, auto

from .node import Node, NodeVisitor


class BinaryOperator(Enum):
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()


@dataclass
class BinaryNode(Node):
    lhs: Node
    rhs: Node
    op: BinaryOperator

    def accept(self, visitor: NodeVisitor) -> None:
        visitor.visit_binary(self)
