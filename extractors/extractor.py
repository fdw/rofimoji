from typing import Dict, List

import requests


class Extractor(object):

    def __init__(self):
        self.names = self.__fetch_names()

    def extract(self):
        pass

    def __fetch_names(self) -> Dict[chr, str]:
        print("Fetching all names")

        response = requests.get(
            'https://unicode.org/Public/UNIDATA/UnicodeData.txt',
            timeout=60
        )  # type: requests.Response

        lines = response.content.decode(response.encoding).split('\n')
        characters = {}

        for line in lines:
            if len(line) == 0:
                continue
            fields = line.split(';')
            characters[chr(int(fields[0], 16))] = fields[1].title()

        return characters

    def resolve_character_range(self, line: str) -> List[str]:
        try:
            (start, end) = line.split('..')
            symbols = []
            for char in range(int(start, 16), int(end, 16) + 1):
                symbols.append(chr(char))
            return symbols
        except ValueError:
            return [self.resolve_character(line)]

    def resolve_character(self, string: str) -> str:
        result = []
        for character in string.split(' '):
            result.append(chr(int(character, 16)))

        return "".join(result)


if __name__ == "__main__":
    from extractors.extract_emojis import EmojiExtractor
    from extractors.extract_maths_symbols import MathExtractor
    from extractors.extract_scripts import ScriptsExtractor

    EmojiExtractor().extract()
    ScriptsExtractor().extract()
    MathExtractor().extract()
