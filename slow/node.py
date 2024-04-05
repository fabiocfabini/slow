from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Protocol, TYPE_CHECKING


if TYPE_CHECKING:
    from slow.ast.binary import BinaryNode
    from slow.ast.literal import LiteralIntegerNode
    from slow.ast.identifier import IdentifierNode
    from slow.ast.let import LetDeclarationNode, LetAssignmentNode
    from slow.ast.program import ProgramNode


class Node(ABC):
    @abstractmethod
    def accept(self, visitor: NodeVisitor) -> None:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

class ExpressionNode(Node):
    pass

class StatementNode(Node):
    pass

class NodeVisitor(Protocol):
    def visit_literal_integer(self, node: LiteralIntegerNode) -> None:
        pass

    def visit_binary(self, node: BinaryNode) -> None:
        pass

    def visit_identifier(self, node: IdentifierNode) -> None:
        pass

    def visit_let_declaration(self, node: LetDeclarationNode) -> None:
        pass

    def visit_let_assignment(self, node: LetAssignmentNode) -> None:
        pass

    def visit_program(self, node: ProgramNode) -> None:
        pass
