from dataclasses import dataclass
from enum import Enum


class Action(Enum):
    TYPE = "type"
    COPY = "copy"
    CLIPBOARD = "clipboard"
    UNICODE = "unicode"
    COPY_UNICODE = "copy-unicode"
    STDOUT = "print"
    MENU = "menu"

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value


class CANCEL:
    def __eq__(self, other):
        return isinstance(other, CANCEL)


class DEFAULT:
    def __eq__(self, other):
        return isinstance(other, DEFAULT)


@dataclass
class Shortcut:
    index: int
