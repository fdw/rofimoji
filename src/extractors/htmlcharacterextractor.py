from dataclasses import dataclass
from pathlib import Path
from typing import List

import aiofiles
import aiohttp

from .extractor import Extractor


@dataclass
class HtmlCharacter:
    string: str
    name: str


class HtmlCharacterExtractor(Extractor):
    __characters: List[HtmlCharacter]

    def __init__(self):
        self.__characters = []

    async def extract_to(self, target: Path) -> None:
        await self.__fetch_data()
        await self.__write_to_file(target)
        print("Finished HtmlCharacters")

    async def __fetch_data(self) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://html.spec.whatwg.org/entities.json") as response:
                entities = await response.json()
                for key in entities:
                    if key.endswith(";") and key != "&NewLine;":
                        name = key[1:-1]
                        char = "".join(list(map(chr, entities[key]["codepoints"])))
                        self.__characters.append(HtmlCharacter(char, name))

    async def __write_to_file(self, target: Path) -> None:
        async with aiofiles.open(target / "html_characters.csv", mode="w") as character_file:
            for character in self.__characters:
                await character_file.write(f"{character.string} {character.name}\n")
