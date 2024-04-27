import html
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import requests

from .characterfactory import Character
from .extractor import Extractor


@dataclass
class Kaomoji:
    string: str
    description: str


class KaomojiExtractor(Extractor):
    __kaomojis: List[Kaomoji]

    def __init__(self):
        self.__kaomojis = []

    def __fetch_icons(self) -> None:
        response = requests.get("https://raw.githubusercontent.com/w33ble/emoticon-data/master/emoticons.json")
        """
        {
          "tags": [
            "hide"
          ],
          "string": "(⊃‿⊂)",
          "id": "f73741a5-13f9-44a3-9dfe-4bce15c44cda"
        }
        """
        for kaomoji in response.json()["emoticons"]:
            self.__kaomojis.append(Kaomoji(kaomoji["string"].replace(" ", " "), ", ".join(kaomoji["tags"])))

    def __write_to_file(self, target: Path) -> None:
        with (target / "kaomoji.csv").open("w") as symbol_file:
            for kaomoji in self.__kaomojis:
                symbol_file.write(f"{kaomoji.string} {html.escape(kaomoji.description.lower())}\n")

    def extract_to(self, target: Path) -> None:
        self.__fetch_icons()
        self.__write_to_file(target)
