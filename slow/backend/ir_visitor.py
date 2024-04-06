from slow.ast.assign import AssignNode
from slow.node import NodeVisitor
from slow.ast.binary import BinaryNode, BinaryOperator
from slow.ast.literal import LiteralIntegerNode
from slow.ast.identifier import IdentifierNode
from slow.ast.let import LetAssignmentNode, LetDeclarationNode
from slow.ast.program import ProgramNode


class IRVisitor(NodeVisitor):
    def __init__(self) -> None:
        self.temporary_counter = 0
        self.literal_integer_temporary_cache: dict[int, int] = {}
        self.identifier_counter: dict[IdentifierNode, int] = {}
        self.binary_temporary_cache: dict[tuple[BinaryOperator, str, str], int] = {}
        self.temporary_stack: list[str] = []

    def _clear(self) -> None:
        self.temporary_counter = 1
        self.literal_integer_temporary_cache = {}
        self.identifier_counter = {}
        self.binary_temporary_cache = {}
        self.temporary_stack = []

    def visit_literal_integer(self, node: LiteralIntegerNode) -> None:
        self.temporary_stack.append(f"{node.value}")

    def visit_identifier(self, node: IdentifierNode) -> None:
        assert node in self.identifier_counter # At this stage, all identifiers should be declared (parser responsibility)
        self.temporary_stack.append(f"{node.name}{self.identifier_counter[node]}")

    def visit_binary(self, node: BinaryNode) -> None:
        node.lhs.accept(self)
        node.rhs.accept(self)

        rhs = self.temporary_stack.pop()
        lhs = self.temporary_stack.pop()

        key = (node.op, lhs, rhs)
        if key in self.binary_temporary_cache:
            self.temporary_stack.append(f"t{self.binary_temporary_cache[key]}")
        else:
            print(f"t{self.temporary_counter} = {lhs} {node.op} {rhs}")
            self.binary_temporary_cache[key] = self.temporary_counter
            self.temporary_stack.append(f"t{self.temporary_counter}")
            self.temporary_counter += 1

    def visit_let_declaration(self, node: LetDeclarationNode) -> None:
        # TODO: How to handle let declarations in SSA form?
        return

    def visit_let_assignment(self, node: LetAssignmentNode) -> None:
        id_counter = self.identifier_counter.get(node.identifier, 0)
        self.identifier_counter[node.identifier] = id_counter + 1

        node.expression.accept(self)
        expression = self.temporary_stack.pop()
        print(f"{node.identifier.name}{id_counter + 1} = {expression}")

    def visit_assign(self, node: AssignNode) -> None:
        node.expression.accept(self)
        expression = self.temporary_stack.pop()

        self.identifier_counter[node.identifier] += 1
        print(f"{node.identifier.name}{self.identifier_counter[node.identifier]} = {expression}")

    def visit_program(self, node: ProgramNode) -> None:
        for statement in node.statements:
            statement.accept(self)
