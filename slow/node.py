from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Protocol, TYPE_CHECKING


if TYPE_CHECKING:
    from slow.ast.binary import BinaryNode
    from slow.ast.literal import LiteralIntegerNode
    from slow.ast.identifier import IdentifierNode


class Node(ABC):
    @abstractmethod
    def accept(self, visitor: NodeVisitor) -> None:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass


class NodeVisitor(Protocol):
    @abstractmethod
    def visit_literal_integer(self, node: LiteralIntegerNode) -> None:
        pass

    @abstractmethod
    def visit_binary(self, node: BinaryNode) -> None:
        pass

    @abstractmethod
    def visit_identifier(self, node: IdentifierNode) -> None:
        pass
