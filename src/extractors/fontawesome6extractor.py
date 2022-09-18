from pathlib import Path
from typing import List

import requests

from .characterfactory import Character
from .extractor import Extractor


class FontAwesome6Extractor(Extractor):
    __icons: List[Character]

    def __init__(self):
        self.__icons = []

    def __fetch_icons(self) -> None:
        response: requests.Response = requests.get(
            "https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/metadata/icons.json"
        )
        for (name, data) in response.json().items():
            icon = int(data["unicode"], 16)
            name = f"fa-{name}"
            char = Character(icon, name)
            try:
                for alias in data["aliases"]["names"]:
                    char.add_description(f"fa-{alias}")
            except KeyError:
                pass
            self.__icons.append(char)

    def __write_to_file(self, target: Path) -> None:
        if len(self.__icons) == 0:
            return

        with (target / "fontawesome6.csv").open("w") as symbol_file:
            for icon in self.__icons:
                aliases = f" <small>({', '.join(icon.descriptions)})</small>"
                line = f'{icon.directional_char} {icon.lower_case_name}{aliases if icon.descriptions else ""}\n'
                symbol_file.write(line)

    def extract_to(self, target: Path) -> None:
        self.__fetch_icons()
        self.__write_to_file(target)
