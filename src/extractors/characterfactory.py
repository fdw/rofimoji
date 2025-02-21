import html
from typing import Dict, List, Optional, Union
from unicodedata import bidirectional

import aiohttp


class Character:
    ltr_mark: str = "\u200e"

    char: str
    name: str
    force_ltr: bool
    descriptions: List[str]

    def __init__(
        self,
        char: Union[int, str],
        name: str,
        bidi_class: Optional[str] = None,
        descriptions: Optional[List[str]] = None,
    ):
        self.char = chr(char) if isinstance(char, int) else char
        self.name = name.strip()
        if not bidi_class:
            bidi_class = bidirectional(self.char)
        self.force_ltr = bidi_class in ("AL", "AN", "R", "RLE", "RLI", "RLO")
        if descriptions:
            self.descriptions = descriptions
        else:
            self.descriptions = []

    @property
    def directional_char(self) -> str:
        return f"{self.ltr_mark if self.force_ltr else ''}{self.char}"

    @property
    def title_case_name(self) -> str:
        return html.escape(self.name.title())

    @property
    def lower_case_name(self) -> str:
        return html.escape(self.name.lower())

    def add_description(self, description: str) -> None:
        if description not in self.descriptions and description != self.name and description != self.char:
            self.descriptions.append(description)

    def add_descriptions(self, descriptions: List[str]) -> None:
        for description in descriptions:
            self.add_description(description)


class CharacterFactory:
    __characters: Dict[str, Character]

    def __init__(self):
        self.__characters = {}

    async def fetch_characters(self) -> None:
        INDEX_CODEPOINT = 0
        INDEX_NAME = 1
        INDEX_CATEGORY = 2
        INDEX_BIDI_CLASS = 4

        async with aiohttp.ClientSession() as session:
            async with session.get("https://unicode.org/Public/UNIDATA/UnicodeData.txt") as response:
                lines = (await response.text()).split("\n")

                for line in lines:
                    fields = line.split(";")
                    if (
                        len(fields) >= 2
                        and fields[INDEX_CATEGORY] not in ("Cc", "Co", "Cs")
                        and not (fields[INDEX_NAME].startswith("<") and fields[INDEX_NAME].endswith(">"))
                    ):
                        character = Character(
                            int(fields[INDEX_CODEPOINT], 16), fields[INDEX_NAME], fields[INDEX_BIDI_CLASS]
                        )
                        self.__characters[character.char] = character

    def get_character(self, char: int) -> Optional[Character]:
        return self.__characters.get(chr(char))
