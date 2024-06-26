from enum import Enum, auto
from typing import Union
from dataclasses import dataclass

from slow.ast.binary import BinaryOperator

class TokenKind(Enum):
    # Special
    EOF = auto()
    ERROR = auto()
    ID = auto()

    # Single-character
    SEMICOLON = auto()
    ASSIGN = auto()
    LPAREN = auto()
    RPAREN = auto()

    # Values
    INTEGER = auto()
    TRUE = auto()
    FALSE = auto()

    # Arithmetic operators
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()

    # Keywords
    LET = auto()


TokenValue = Union[int, str, None]

@dataclass(slots=True, frozen=True)
class Token:
    kind: TokenKind
    value: TokenValue
    line: int
    span: slice

    def to_binary_operator(self) -> BinaryOperator:
        match self.kind:
            case TokenKind.ADD:
                return BinaryOperator.ADD
            case TokenKind.SUB:
                return BinaryOperator.SUB
            case TokenKind.MUL:
                return BinaryOperator.MUL
            case TokenKind.DIV:
                return BinaryOperator.DIV
            case _:
                raise ValueError(f"Token {self} is not a binary operator")
