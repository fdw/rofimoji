import html
from dataclasses import dataclass
from enum import Enum


class Action(Enum):
    TYPE = "type"
    COPY = "copy"
    CLIPBOARD = "clipboard"
    TYPE_NUMERICAL = "type-numerical"
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


@dataclass(slots=True)
class Shortcut:
    index: int


@dataclass(slots=True)
class CharacterEntry:
    character_html: str
    description_html: str | None = None

    @property
    def character(self) -> str:
        return html.unescape(self.character_html)

    @property
    def description(self) -> str | None:
        if self.description_html is None:
            return None
        return html.unescape(self.description_html.replace("<small>", "").replace("</small>", ""))

    def merge(self, other: "CharacterEntry"):
        if self == other:
            return self

        if self.character != other.character:
            raise Exception("Cannot merge different characters")

        if other.description_html:
            if self.description_html:
                self.description_html = f"{self.description_html}, {other.description_html}"
            else:
                self.description_html = other.description_html
