from dataclasses import dataclass

from ..node import Node, StatementNode, NodeVisitor


@dataclass
class ProgramNode(Node):
    statements: list[StatementNode]

    def accept(self, visitor: NodeVisitor) -> None:
        visitor.visit_program(self)

    def __str__(self) -> str:
        return "\n".join(str(statement) for statement in self.statements)
