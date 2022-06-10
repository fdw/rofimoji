import html
from pathlib import Path
from typing import List

import requests

from .characterfactory import Character
from .extractor import Extractor


class FontAwesome6Extractor(Extractor):
    __icons: List[Character]

    def __init__(self):
        self.__icons = []

    def __fetch_icons(self: 'FontAwesome6Extractor'):
        response = requests.get(
            'https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/metadata/icons.json',
            timeout=60
        )
        for (name, data) in response.json().items():
            icon = int(data['unicode'], 16)
            name = f'fa-{name}'
            char = Character(icon, name)
            char.aliases: List[str] = []
            try:
                for alias in data['aliases']['names']:
                    char.aliases.append(f'fa-{alias}')
            except KeyError:
                pass
            self.__icons.append(char)

    def __write_to_file(self, target: Path):
        if len(self.__icons) == 0:
            return

        with (target / 'fontawesome6.csv').open('w') as symbol_file:
            for icon in self.__icons:
                line=f'{icon.directional_char} {html.escape(icon.name.lower())}'
                if len(icon.aliases) > 0:
                    line += f" <small>({', '.join(icon.aliases)})</small>\n"
                else:
                    line += '\n'
                symbol_file.write(line)


    def extract_to(self, target: Path):
        self.__fetch_icons()
        self.__write_to_file(target)
