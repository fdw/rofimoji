from pathlib import Path
from typing import List

import aiofiles
import aiohttp

from .characterfactory import Character, CharacterFactory
from .extractor import Extractor


class MathExtractor(Extractor):
    __char_factory: CharacterFactory
    __characters: List[Character]

    def __init__(self, character_factory: CharacterFactory):
        self.__char_factory = character_factory
        self.__characters = []

    async def extract_to(self, target: Path) -> None:
        await self.__fetch_math_symbols()
        await self.__write_file(target)
        print("Finished Math characters")

    async def __fetch_math_symbols(self) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://unicode.org/Public/math/latest/MathClassEx-15.txt") as response:
                characters = []
                for line in (await response.text()).split("\n"):
                    if line and not line.startswith("#"):
                        fields = line.split(";")
                        symbols = self.__resolve_character_range(fields[0].strip())
                        for symbol in symbols:
                            characters.append(self.__char_factory.get_character(symbol))

                self.__characters = [character for character in characters if character is not None]

    def __resolve_character_range(self, line: str) -> List[int]:
        try:
            (start, end) = line.split("..")
            return list(range(int(start, 16), int(end, 16) + 1))
        except ValueError:
            return [int(line, 16)]

    async def __write_file(self, target: Path) -> None:
        async with aiofiles.open(target / "math.csv", mode="w") as character_file:
            for character in self.__characters:
                await character_file.write(f"{character.char} {character.title_case_name}\n")
