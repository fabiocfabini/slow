from __future__ import annotations

from typing import Optional, Callable, ClassVar, Dict
from dataclasses import dataclass, field
from enum import Enum, auto

from slow._exceptions import ParserError, LexerError
from slow.node import Node
from slow.ast.literal import LiteralIntegerNode
from slow.ast.binary import BinaryNode
from slow.ast.identifier import IdentifierNode
from .lexeme import Token, TokenKind
from .lexer import Lexer

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
    test_mode: bool = False

    _identifier_table: set[IdentifierNode] = field(default_factory=set)

    _lexer: Lexer = field(init=False, repr=False)
    _current: Optional[Token] = field(init=False, default=None)
    _previous: Optional[Token] = field(init=False, default=None)
    _had_error: bool = field(init=False, default=False)
    _panic_mode: bool = field(init=False, default=False)


    _expression_rule_table: ClassVar[Dict[TokenKind, ExpressionParseRule]]

# pylint: disable=C0301
    def __post_init__(self) -> None:
        Parser._expression_rule_table = {
            TokenKind.EOF       : ExpressionParseRule(            None,           None, Precedence.NO_PRECEDENCE),
            TokenKind.ERROR     : ExpressionParseRule(            None,           None, Precedence.NO_PRECEDENCE),
            TokenKind.ID        : ExpressionParseRule(      Parser._id,           None, Precedence.NO_PRECEDENCE),
            TokenKind.LPAREN    : ExpressionParseRule(Parser._grouping,           None, Precedence.NO_PRECEDENCE),
            TokenKind.RPAREN    : ExpressionParseRule(            None,           None, Precedence.NO_PRECEDENCE),
            TokenKind.INTEGER   : ExpressionParseRule( Parser._integer,           None, Precedence.NO_PRECEDENCE),
            TokenKind.TRUE      : ExpressionParseRule(    Parser._true,           None, Precedence.NO_PRECEDENCE),
            TokenKind.FALSE     : ExpressionParseRule(   Parser._false,           None, Precedence.NO_PRECEDENCE),
            TokenKind.ADD       : ExpressionParseRule(            None, Parser._binary, Precedence.TERM         ),
            TokenKind.SUB       : ExpressionParseRule(            None, Parser._binary, Precedence.TERM         ),
            TokenKind.MUL       : ExpressionParseRule(            None, Parser._binary, Precedence.FACTOR       ),
            TokenKind.DIV       : ExpressionParseRule(            None, Parser._binary, Precedence.FACTOR       ),
        }
# pylint: enable=C0301

    def parse(self, source: str) -> Optional[Node]:
        self._reset(source)

        self._advance()

        return self._expression()

    def _reset(self, source: str) -> None:
        self._lexer = Lexer(source)
        self._current = None
        self._previous = None
        self._had_error = False
        self._panic_mode = False

    def _advance(self) -> None:
        self._previous = self._current

        while True:
            assert self._lexer is not None
            self._current = self._lexer.next()

            if self._current.kind != TokenKind.ERROR:
                break

            self._lexer_error()

    def _lexer_error(self) -> None:
        if self._panic_mode:
            return

        self._had_error = True
        self._panic_mode = True

        assert self._current is not None
        if self._current.kind == TokenKind.ERROR:
            assert self._lexer is not None

            if self.test_mode:
                raise LexerError(str(self._current.value))

            print(f"Lexer error: {self._current.value}")

    def _parser_error(self, message: str) -> None:
        if self._panic_mode:
            return

        self._had_error = True
        self._panic_mode = True

        if self.test_mode:
            raise ParserError(message)

        print(f"Parser error: {message}")

    def _match(self, kind: TokenKind) -> bool:
        assert self._current is not None
        if self._current.kind == kind:
            self._advance()
            return True

        return False

    # NOTE: Booleans are glorified integers
    def _true(self) -> Optional[Node]:
        assert self._previous is not None

        return LiteralIntegerNode(1, self._previous.line)

    def _false(self) -> Optional[Node]:
        assert self._previous is not None

        return LiteralIntegerNode(0, self._previous.line)

    def _integer(self) -> Optional[Node]:
        assert self._previous is not None
        assert isinstance(self._previous.value, int)

        return LiteralIntegerNode(self._previous.value, self._previous.line)

    def _id(self) -> Optional[Node]:
        assert self._previous is not None
        assert isinstance(self._previous.value, str)

        node = IdentifierNode(self._previous.value)
        if node in self._identifier_table:
            return node

        self._parser_error(f"Undefined identifier '{node}'")
        return None

    def _grouping(self) -> Optional[Node]:
        expression = self._expression()

        if self._match(TokenKind.RPAREN):
            assert expression is not None
            return expression

        assert self._lexer is not None
        assert self._current is not None
        self._parser_error(f"Expected ')' after expression. Got '{self._lexer.lexeme_at_token(self._current)}'")
        return None

    def _binary(self, lhs: Node) -> Optional[Node]:
        tok_op = self._previous

        assert tok_op is not None
        rhs = self._parse_precedence(Parser._expression_rule_table[tok_op.kind].precedence)

        if not self._panic_mode:
            assert rhs is not None
            return BinaryNode(lhs, rhs, tok_op.to_binary_operator())

        return None

    def _parse_precedence(self, precedence: Precedence) -> Optional[Node]:
        self._advance()

        assert self._previous is not None
        prefix_rule =  Parser._expression_rule_table[self._previous.kind].prefix

        if prefix_rule is None:
            assert self._lexer is not None
            assert self._current is not None
            self._parser_error(f"Expected expression. Got '{self._lexer.lexeme_at_token(self._previous)}'")
            return None

        lhs = prefix_rule(self)

        rule: ExpressionParseRule
        assert self._current is not None
        while precedence.value <= (rule := Parser._expression_rule_table[self._current.kind]).precedence.value:
            self._advance()
            infix_rule = rule.infix

            if infix_rule is None:
                assert self._lexer is not None
                assert self._current is not None
                self._parser_error(f"Expected binary operator. Got '{self._lexer.lexeme_at_token(self._previous)}'")
                return None

            if lhs is not None:
                lhs = infix_rule(self, lhs)
            else:
                return None

        return lhs

    def _expression(self) -> Optional[Node]:
        return self._parse_precedence(Precedence.ASSIGNMENT)
