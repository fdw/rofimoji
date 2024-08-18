import json
from dataclasses import dataclass
from pathlib import Path
from typing import List

import requests

from .extractor import Extractor


@dataclass
class HtmlCharacter:
    string: str
    name: str


class HtmlCharacterExtractor(Extractor):
    __characters: List[HtmlCharacter]

    def __init__(self):
        self.__characters = []

    def __fetch_data(self) -> None:
        response: requests.Response = requests.get("https://html.spec.whatwg.org/entities.json", timeout=120)
        entities = json.loads(response.text)
        for key in entities:
            if key.endswith(";") and key != "&NewLine;":
                name = key[1:-1]
                char = "".join(list(map(chr, entities[key]["codepoints"])))
                self.__characters.append(HtmlCharacter(char, name))

    def __write_to_file(self, target: Path) -> None:
        with (target / "html_characters.csv").open("w") as symbol_file:
            for character in self.__characters:
                symbol_file.write(f"{character.string} {character.name}\n")

    def extract_to(self, target: Path) -> None:
        self.__fetch_data()
        self.__write_to_file(target)
