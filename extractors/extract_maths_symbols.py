import html
from collections import namedtuple
from typing import List

import requests

from extractors.extractor import Extractor

Character = namedtuple('Character', 'char name')


class MathExtractor(Extractor):

    def fetch_math_symbols(self: 'MathExtractor') -> List[Character]:
        print('Downloading list of maths symbols...')

        data = requests.get(
            'https://unicode.org/Public/math/latest/MathClassEx-15.txt',
            timeout=60
        )  # type: requests.Response

        characters = []
        for line in data.content.decode(data.encoding).split('\n'):
            if line.startswith('#') or len(line) == 0:
                continue

            fields = line.split(';')

            symbols = self.resolve_character_range(fields[0].strip())

            for symbol in symbols:
                characters.append(Character(symbol, self.names[symbol]))

        return characters

    def write_file(self: 'MathExtractor', symbols: List[Character]):
        symbol_file = open(f"../picker/data/math.csv", 'w')

        for character in symbols:
            symbol_file.write(f"{character.char} {html.escape(character.name)}\n")

        symbol_file.close()

    def extract(self):
        self.write_file(self.fetch_math_symbols())
