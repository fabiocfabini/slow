from slow.node import NodeVisitor
from slow.ast.binary import BinaryNode, BinaryOperator
from slow.ast.literal import LiteralIntegerNode


class IRVisitor(NodeVisitor):
    temporary_counter = 0
    literal_integer_temporary_cache: dict[int, int] = {}
    binary_temporary_cache: dict[tuple[BinaryOperator, int, int], int] = {}
    temporary_stack: list[int] = []

    def _clear(self) -> None:
        IRVisitor.temporary_counter = 0
        IRVisitor.literal_integer_temporary_cache = {}
        IRVisitor.binary_temporary_cache = {}
        IRVisitor.temporary_stack = []

    def visit_literal_integer(self, node: LiteralIntegerNode) -> None:
        if node.value in IRVisitor.literal_integer_temporary_cache:
            IRVisitor.temporary_stack.append(IRVisitor.literal_integer_temporary_cache[node.value])
        else:
            print(f"t{IRVisitor.temporary_counter} = {node.value}")
            IRVisitor.literal_integer_temporary_cache[node.value] = IRVisitor.temporary_counter
            IRVisitor.temporary_stack.append(IRVisitor.temporary_counter)
            IRVisitor.temporary_counter += 1

    def visit_binary(self, node: BinaryNode) -> None:
        node.lhs.accept(self)
        node.rhs.accept(self)

        rhs = IRVisitor.temporary_stack.pop()
        lhs = IRVisitor.temporary_stack.pop()

        key = (node.op, lhs, rhs)
        if key in IRVisitor.binary_temporary_cache:
            IRVisitor.temporary_stack.append(IRVisitor.binary_temporary_cache[key])
        else:
            print(f"t{IRVisitor.temporary_counter} = t{lhs} {node.op} t{rhs}")
            IRVisitor.binary_temporary_cache[key] = IRVisitor.temporary_counter
            IRVisitor.temporary_stack.append(IRVisitor.temporary_counter)
            IRVisitor.temporary_counter += 1
