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

    def resolve_character_range(self, line: str) -> List[chr]:
        try:
            (start, end) = line.split('..')
            symbols = []
            for char in range(int(start, 16), int(end, 16) + 1):
                symbols.append(chr(char))
            return symbols
        except ValueError:
            return [chr(int(line, 16))]
