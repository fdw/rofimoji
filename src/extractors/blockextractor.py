import html
from pathlib import Path

import requests

from .blockfactory import BlockFactory
from .characterfactory import CharacterFactory
from .extractor import Extractor


class BlockExtractor(Extractor):
    def __init__(self, character_factory: CharacterFactory):
        super().__init__()
        self.__blocks = []
        self.__block_factory = BlockFactory(character_factory)

    def __fetch_blocks(self):
        print('Downloading list of all blocks')

        response = requests.get(
            'https://www.unicode.org/Public/14.0.0/ucd/Blocks.txt',
            timeout=60
        )  # type: requests.Response

        lines = response.text.split('\n')

        for line in lines:
            if not line or line.startswith(('#', '@')):
                continue
            key, _, value = line.partition(';')
            self.__blocks.append(self.__block_factory.build_block_from_range(value.strip(), key.strip()))

    def __write_to_files(self, target: Path):
        for block in self.__blocks:
            if not block.characters:
                continue

            with (target / f'{block.name.lower().replace(" ", "_")}.csv').open('w') as symbol_file:
                for character in block.characters:
                    symbol_file.write(f'{character.directional_char} {html.escape(character.name)}\n')

    def extract_to(self, target: Path):
        self.__fetch_blocks()
        self.__write_to_files(target)
