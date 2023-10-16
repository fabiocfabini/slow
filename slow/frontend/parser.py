from __future__ import annotations

from typing import Optional, Callable, ClassVar, Dict
from dataclasses import dataclass
from enum import Enum, auto

from ..ast.node import Node
from ..ast.literal import LiteralIntegerNode
from ..ast.binary import BinaryNode
from ..ast.grouping import GroupingNode
from .lexer import Lexer
from .lexeme import Token, TokenKind


class Precedence(Enum):
    NO_PRECEDENCE   = auto()
    ASSIGNMENT      = auto() # =
    # TERNARY         = auto() # ? :
    # OR              = auto() # or
    # AND             = auto() # and
    # EQUALITY        = auto() # == !=
    # COMPARISON      = auto() # < > <= >=
    TERM            = auto() # + -
    FACTOR          = auto() # * /
    # MOD             = auto() # %
    # UNARY           = auto() # not -
    # CALL            = auto() # . ()
    PRIMARY         = auto()


@dataclass
class ExpressionParseRule:
    prefix: Optional[Callable[[Parser], Optional[Node]]]
    infix: Optional[Callable[[Parser, Node], Optional[Node]]]
    precedence: Precedence


@dataclass
class Parser:
    lexer: Optional[Lexer] = None
    current: Optional[Token] = None
    previous: Optional[Token] = None
    had_error: bool = False
    panic_mode: bool = False

    expression_rule_table: ClassVar[Dict[TokenKind, ExpressionParseRule]]

# pylint: disable=C0301
    def __post_init__(self) -> None:
        Parser.expression_rule_table = {
            TokenKind.EOF       : ExpressionParseRule(            None,           None, Precedence.NO_PRECEDENCE),
            TokenKind.ERROR     : ExpressionParseRule(            None,           None, Precedence.NO_PRECEDENCE),
            TokenKind.LPAREN    : ExpressionParseRule(Parser._grouping,           None, Precedence.NO_PRECEDENCE),
            TokenKind.RPAREN    : ExpressionParseRule(            None,           None, Precedence.NO_PRECEDENCE),
            TokenKind.INTEGER   : ExpressionParseRule( Parser._integer,           None, Precedence.NO_PRECEDENCE),
            TokenKind.ADD       : ExpressionParseRule(            None, Parser._binary, Precedence.TERM         ),
            TokenKind.SUB       : ExpressionParseRule(            None, Parser._binary, Precedence.TERM         ),
            TokenKind.MUL       : ExpressionParseRule(            None, Parser._binary, Precedence.FACTOR       ),
            TokenKind.DIV       : ExpressionParseRule(            None, Parser._binary, Precedence.FACTOR       ),
        }
# pylint: enable=C0301

    def parse(self, source: str) -> Optional[Node]:
        self._reset()
        self.lexer = Lexer(source)

        self._advance()

        return self._expression()

    def _reset(self) -> None:
        pass

    def _advance(self) -> None:
        self.previous = self.current

        while True:
            self.current = self.lexer.next()

            if self.current.kind != TokenKind.ERROR:
                break

            self._lexer_error()

    def _lexer_error(self) -> None:
        if self.panic_mode:
            return

        self.had_error = True
        self.panic_mode = True

        assert self.current is not None
        if self.current.kind == TokenKind.ERROR:
            print(f"Lexer error: {self.current.value}")

    def _parser_error(self, message: str) -> None:
        if self.panic_mode:
            return

        self.had_error = True
        self.panic_mode = True

        print(f"Parser error: {message}")

    def _match(self, kind: TokenKind) -> bool:
        assert self.current is not None
        if self.current.kind == kind:
            self._advance()
            return True

        return False

    def _integer(self) -> Optional[Node]:
        assert self.previous is not None
        assert isinstance(self.previous.value, int)
        return LiteralIntegerNode(self.previous.value, self.previous.line)

    def _grouping(self) -> Optional[Node]:
        expression = self._expression()

        if self._match(TokenKind.RPAREN):
            assert expression is not None
            return GroupingNode(expression)

        self._parser_error(f"Expected ')' after expression. Got {self.current.value}")
        return None

    def _binary(self, lhs: Node) -> Optional[Node]:
        tok_op = self.previous

        assert tok_op is not None
        rhs = self._parse_precedence(Parser.expression_rule_table[tok_op.kind].precedence)

        if not self.panic_mode:
            assert rhs is not None
            return BinaryNode(lhs, rhs, tok_op.to_binary_operator())

        return None

    def _expression(self) -> Optional[Node]:
        return self._parse_precedence(Precedence.ASSIGNMENT)

    def _parse_precedence(self, precedence: Precedence) -> Optional[Node]:
        self._advance()

        assert self.previous is not None
        prefix_rule =  Parser.expression_rule_table[self.previous.kind].prefix

        if prefix_rule is None:
            self._parser_error(f"Expected expression. Got {self.previous.value}")
            return None

        lhs = prefix_rule(self)

        rule: ExpressionParseRule
        assert self.current is not None
        while precedence.value <= (rule := Parser.expression_rule_table[self.current.kind]).precedence.value:  # pylint: disable=C0301
            self._advance()
            infix_rule = rule.infix

            if infix_rule is None:
                self._parser_error(f"Expected binary operator. Got {self.current.value}")
                return None

            assert lhs is not None
            lhs = infix_rule(self, lhs)

        return lhs
