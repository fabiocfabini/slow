from dataclasses import dataclass
from enum import Enum, auto

from slow.node import Node, NodeVisitor


class BinaryOperator(Enum):
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()

    def to_asm(self) -> str:
        match self:
            case BinaryOperator.ADD:
                return "add"
            case BinaryOperator.SUB:
                return "sub"
            case BinaryOperator.MUL:
                return "mul"
            case BinaryOperator.DIV:
                return "div"
            case _:
                raise ValueError(f"Binary operator {self} is not supported")

    def __str__(self) -> str:
        match self:
            case BinaryOperator.ADD:
                return "+"
            case BinaryOperator.SUB:
                return "-"
            case BinaryOperator.MUL:
                return "*"
            case BinaryOperator.DIV:
                return "/"
            case _:
                raise ValueError(f"Binary operator {self} is not supported")


@dataclass
class BinaryNode(Node):
    lhs: Node
    rhs: Node
    op: BinaryOperator

    def accept(self, visitor: NodeVisitor) -> None:
        visitor.visit_binary(self)

    def __str__(self) -> str:
        return f"({self.lhs} {self.op} {self.rhs})"

    def __hash__(self) -> int:
        return hash((self.lhs, self.rhs, self.op))
