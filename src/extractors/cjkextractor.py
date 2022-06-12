import html
import io
import re
import zipfile
from pathlib import Path
from typing import Dict, List

import requests

from .characterfactory import Character


class CjkExtractor(object):
    def __init__(self):
        self.__characters = self.fetch_characters()

    def fetch_characters(self: 'CjkExtractor') -> Dict[str, List[Character]]:
        INDEX_CODEPOINT = 0
        INDEX_LANGUAGE = 1
        INDEX_DESCRIPTION = 2

        response = requests.get(
            'https://unicode.org/Public/UNIDATA/Unihan.zip',
            timeout=60
        )  # type: requests.Response

        characters = {}
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip:
            with io.TextIOWrapper(zip.open('Unihan_Readings.txt'), encoding='utf-8') as file:
                for line in file.read().split('\n'):
                    if not line or line.startswith('#'):
                        continue

                    fields = line.split('\t')
                    character = Character(
                        int(fields[INDEX_CODEPOINT][2:], 16),
                        fields[INDEX_DESCRIPTION],
                        'L'
                    )
                    language = fields[INDEX_LANGUAGE][1:]
                    if language not in characters:
                        characters[language] = []
                    characters[language].append(character)

        return characters

    def write_to_file(self: 'CjkExtractor', language: str, characters: List[Character]):
        with (Path(__file__).parent.parent / 'picker' / 'data' / f'cjk_{language.lower()}.csv').open('w') as symbol_file:
            for character in characters:
                symbol_file.write(f'{character.directional_char} {html.escape(character.name)}\n')

    def extract(self):
        for language in ('Cantonese', 'Mandarin', 'Vietnamese', 'Tang', 'JapaneseKun', 'JapaneseOn', 'Korean'):
            self.write_to_file(re.sub(r'(?!^)(?=[A-Z])', '_', language).lower(), self.__characters[language])
