from __future__ import annotations

from abc import ABC, abstractmethod


class Node(ABC):
    @abstractmethod
    def accept(self, visitor: NodeVisitor) -> None:
        pass


class NodeVisitor(ABC):
    @abstractmethod
    def visit_literal_integer(self, node: Node) -> None:
        pass

    @abstractmethod
    def visit_grouping(self, node: Node) -> None:
        pass

    @abstractmethod
    def visit_binary(self, node: Node) -> None:
        pass
