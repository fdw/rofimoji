from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List


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


@dataclass
class CharacterEntry:
    character: str
    description: str

    def __init__(self, character: str, description: str | None = None):
        self.character = character
        self.description = description if description else ""

    def merge(self, other: "CharacterEntry"):
        if self.character != other.character:
            raise Exception("Cannot merge different characters")

        if len(other.description) > 0:
            if len(self.description) > 0:
                self.description = f"{self.description}, {other.description}"
            else:
                self.description = other.description
