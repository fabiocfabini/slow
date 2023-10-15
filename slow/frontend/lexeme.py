from enum import Enum, auto
from typing import Union
from dataclasses import dataclass


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
