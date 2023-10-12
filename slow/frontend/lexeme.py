from enum import Enum, auto
from typing import Union
from dataclasses import dataclass


class TokenKind(Enum):
    # Special
    EOF = auto()
    ERROR = auto()

    # Values
    INTEGER = auto()

    # ARITHMETIC OPERATORS
    ADD = auto()
    SUB = auto()


TokenValue = Union[int, str, None]

@dataclass(slots=True, frozen=True)
class Token:
    kind: TokenKind
    value: TokenValue
    line: int

    def __repr__(self) -> str:
        return f"Token({self.kind}, {self.value}, {self.line})"

    def __str__(self) -> str:
        return self.__repr__()

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
