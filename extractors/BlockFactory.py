from dataclasses import dataclass
from typing import List

from extractors.CharacterFactory import Character, CharacterFactory


@dataclass
class Block(object):
    name: str
    start: int
    end: int
    characters: List[Character]


class BlockFactory(object):
    def __init__(self: 'BlockFactory', character_factory: CharacterFactory):
        self.__char_factory = character_factory

    def build_block_from_range(self: 'BlockFactory', name: str, range: str) -> Block:
        (start, end) = range.split('..')
        return self.build_block(name, int(start.strip(), 16), int(end.strip(), 16))

    def build_block(self: 'BlockFactory', name: str, start: int, end: int) -> Block:
        return Block(name.strip().title(), start, end, self.__fill_characters(start, end))

    def __fill_characters(self: 'BlockFactory', start: int, end: int) -> List[Character]:
        return [char
                for char in (self.__char_factory.get_character(pos) for pos in range(start, end + 1))
                if char is not None]
