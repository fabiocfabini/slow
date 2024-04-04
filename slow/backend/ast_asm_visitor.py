from slow.node import NodeVisitor
from slow.ast.binary import BinaryNode
from slow.ast.literal import LiteralIntegerNode


class AstAsmVisitor(NodeVisitor):
    def visit_literal_integer(self, node: LiteralIntegerNode) -> None:
        print(f"push {node.value}")

    def visit_binary(self, node: BinaryNode) -> None:
        node.lhs.accept(self)
        node.rhs.accept(self)
        print("pop rdi")
        print("pop rax")
        print(f"{node.op.to_asm()} rax, rdi")
        print("push rax")
