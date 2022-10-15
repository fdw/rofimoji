from dataclasses import dataclass
from typing import List

from .characterfactory import Character, CharacterFactory


@dataclass
class Block:
    name: str
    characters: List[Character]


class BlockFactory:
    __char_factory: CharacterFactory

    def __init__(self, character_factory: CharacterFactory):
        self.__char_factory = character_factory

    def build_block_from_range(self, name: str, range: str) -> Block:
        (start, end) = range.split("..")
        return self.__build_block(name, int(start.strip(), 16), int(end.strip(), 16))

    def __build_block(self, name: str, start: int, end: int) -> Block:
        return Block(name.strip().title(), self.__fill_characters(start, end))

    def __fill_characters(self, start: int, end: int) -> List[Character]:
        return [
            char
            for char in (self.__char_factory.get_character(pos) for pos in range(start, end + 1))
            if char is not None
        ]
