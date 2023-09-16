from pathlib import Path
from typing import List

import requests
from bs4 import BeautifulSoup

from .characterfactory import Character
from .extractor import Extractor


class NerdFontExtractor(Extractor):
    __icons: List[Character]

    def __init__(self):
        self.__icons = []

    def __fetch_icons(self) -> None:
        response = requests.get("https://www.nerdfonts.com/cheat-sheet")

        characters = BeautifulSoup(response.text, "html.parser").find(id="glyphCheatSheet").find_all(class_="column")
        for c in characters:
            icon = int(c.find(class_="codepoint").string, 16)
            name = c.find(class_="class-name").string
            self.__icons.append(Character(icon, name))

    def __write_to_file(self, target: Path) -> None:
        if len(self.__icons) == 0:
            return

        with (target / "nerd_font.csv").open("w") as symbol_file:
            for icon in self.__icons:
                symbol_file.write(f"{icon.directional_char} {icon.lower_case_name}\n")

    def extract_to(self, target: Path) -> None:
        self.__fetch_icons()
        self.__write_to_file(target)
