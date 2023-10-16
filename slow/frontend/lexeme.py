from enum import Enum, auto
from typing import Union
from dataclasses import dataclass

from ..ast.binary import BinaryOperator

class TokenKind(Enum):
    # Special
    EOF = auto()
    ERROR = auto()

    # Single-character
    LPAREN = auto()
    RPAREN = auto()

    # Values
    INTEGER = auto()

    # Arithmetic operators
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()


TokenValue = Union[int, str, None]

@dataclass(slots=True, frozen=True)
class Token:
    kind: TokenKind
    value: TokenValue
    line: int

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

    def __format__(self, __format_spec: str) -> str:
        match __format_spec:
            case "kind":
                return str(self.kind)
            case "value":
                return str(self.value)
            case "line":
                return str(self.line)
            case _:
                return self.__repr__()
