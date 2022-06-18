import io
import re
import zipfile
from pathlib import Path
from typing import Dict, List

import requests

from .characterfactory import Character
from .extractor import Extractor


class CjkExtractor(Extractor):
    __characters: Dict[str, List[Character]]

    def __init__(self):
        self.__characters = {}

    def __fetch_characters(self) -> None:
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

        self.__characters = characters

    def __write_to_file(self, target: Path, language: str, characters: List[Character]) -> None:
        filename = f'cjk_{re.sub(r"(?!^)(?=[A-Z])", "_", language).lower()}.csv'
        with (target / filename).open('w') as symbol_file:
            for character in characters:
                symbol_file.write(f'{character.directional_char} {character.title_case_name}\n')

    def extract_to(self, target: Path) -> None:
        self.__fetch_characters()
        for language in ('Cantonese', 'Mandarin', 'Vietnamese', 'Tang', 'JapaneseKun', 'JapaneseOn', 'Korean'):
            self.__write_to_file(target, language, self.__characters[language])
