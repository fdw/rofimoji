import html
from pathlib import Path
from typing import List

import requests

from .characterfactory import CharacterFactory, Character
from .extractor import Extractor


class MathExtractor(Extractor):
    __char_factory: CharacterFactory
    __characters: List[Character]

    def __init__(self, character_factory: CharacterFactory):
        self.__char_factory = character_factory
        self.__characters = []

    def __fetch_math_symbols(self) -> None:
        data = requests.get(
            'https://unicode.org/Public/math/latest/MathClassEx-15.txt',
            timeout=60
        )  # type: requests.Response

        characters = []
        for line in data.text.split('\n'):
            if line and not line.startswith('#'):
                fields = line.split(';')
                symbols = self.__resolve_character_range(fields[0].strip())
                for symbol in symbols:
                    characters.append(self.__char_factory.get_character(symbol))

        self.__characters = characters

    def __resolve_character_range(self, line: str) -> List[int]:
        try:
            (start, end) = line.split('..')
            return list(range(int(start, 16), int(end, 16) + 1))
        except ValueError:
            return [int(line, 16)]

    def __write_file(self, target: Path) -> None:
        with (target / 'math.csv').open('w') as symbol_file:
            for character in self.__characters:
                symbol_file.write(f"{character.char} {character.title_case_name}\n")

    def extract_to(self, target: Path) -> None:
        self.__fetch_math_symbols()
        self.__write_file(target)
