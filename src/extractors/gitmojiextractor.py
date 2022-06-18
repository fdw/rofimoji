import html
from pathlib import Path
from typing import List

import requests

from .characterfactory import Character
from .extractor import Extractor


class GitmojiExtractor(Extractor):
    __icons: List[Character]

    def __init__(self):
        self.__icons = []

    def __fetch_icons(self) -> None:
        response = requests.get(
            "https://raw.githubusercontent.com/carloscuesta/gitmoji/master/src/data/gitmojis.json",
            timeout=60
        )
        """
        {
            'emoji': '🎨',
            'entity': '&#x1f3a8;',
            'code': ':art:',
            'description': 'Improve structure / format of the code.',
            'name': 'art',
            'semver': None
        }
        """
        for char in response.json()["gitmojis"]:
            icon = ord(char["emoji"][0])
            name = char["description"]
            self.__icons.append(Character(icon, name))

    def __write_to_file(self, target: Path) -> None:
        with (target / 'gitmoji.csv').open('w') as symbol_file:
            for icon in self.__icons:
                symbol_file.write(f"{icon.directional_char} {icon.lower_case_name}\n")

    def extract_to(self, target: Path) -> None:
        self.__fetch_icons()
        self.__write_to_file(target)
