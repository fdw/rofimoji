import html
from collections import namedtuple
from pathlib import Path
from typing import Dict, List

import requests
from bs4 import BeautifulSoup
from lxml import etree
from lxml.etree import XPath
from tqdm import tqdm

from .extractor import Extractor

Emoji = namedtuple("Emoji", "char name")


class EmojiExtractor(Extractor):
    __all_emojis: List[Emoji]
    __annotations: Dict[chr, List[str]]
    __base_emojis: List[chr]

    def __init__(self):
        self.__all_emojis = []
        self.__annotations = {}
        self.__base_emojis = []

    def __fetch_data(self) -> None:
        with tqdm(total=3) as progress:
            progress.set_description("Downloading list of all emojis")
            self.__all_emojis = self.__fetch_emoji_list()
            progress.update(1)

            progress.set_description("Downloading annotations")
            self.__annotations = self.__fetch_annotations()
            progress.update(1)

            progress.set_description("Downloading list of human emojis")
            self.__base_emojis = self.__fetch_base_emojis()
            progress.update(1)

    def __fetch_emoji_list(self) -> List[Emoji]:
        data: requests.Response = requests.get(
            "https://unicode.org/emoji/charts-14.0/full-emoji-list.html", timeout=120
        )

        html = BeautifulSoup(data.text, "lxml")

        emojis = []
        for row in html.find("table").find_all("tr"):
            if not row.th:
                emoji = row.find("td", {"class": "chars"}).string
                description = row.find("td", {"class": "name"}).string.replace("⊛ ", "")
                emojis.append(Emoji(emoji, description))

        return emojis

    def __fetch_annotations(self) -> Dict[chr, List[str]]:
        data: requests.Response = requests.get(
            "https://raw.githubusercontent.com/unicode-org/cldr/latest/common/annotations/en.xml", timeout=60
        )

        xpath = XPath('./annotations/annotation[not(@type="tts")]')
        return {element.get("cp"): element.text.split(" | ") for element in xpath(etree.fromstring(data.content))}

    def __fetch_base_emojis(self) -> List[chr]:
        data: requests.Response = requests.get("https://unicode.org/Public/14.0.0/ucd/emoji/emoji-data.txt", timeout=60)

        started = False
        emojis = []
        for line in data.text.split("\n"):
            if not started and line != "# All omitted code points have Emoji_Modifier_Base=No ":
                continue
            started = True
            if line == "# Total elements: 132":
                break
            if line and not line.startswith("#"):
                emojis.extend(self.__resolve_character_range(line.split(";")[0].strip()))

        return emojis

    def __resolve_character_range(self, line: str) -> List[str]:
        try:
            (start, end) = line.split("..")
            return [chr(char) for char in range(int(start, 16), int(end, 16) + 1)]
        except ValueError:
            return [self.__resolve_character(line)]

    def __resolve_character(self, string: str) -> str:
        return "".join(chr(int(character, 16)) for character in string.split(" "))

    def __write_symbol_file(self, target: Path) -> None:
        with (target / "emojis.csv").open("w") as symbol_file:
            for entry in self.__compile_entries(self.__all_emojis):
                symbol_file.write(entry + "\n")

    def __compile_entries(self, emojis: List[Emoji]) -> List[str]:
        annotated_emojis = []
        for emoji in emojis:
            entry = f"{emoji.char} {html.escape(emoji.name)}"
            if emoji.char in self.__annotations:
                entry += f" <small>({html.escape(', '.join([annotation for annotation in self.__annotations[emoji.char] if annotation != emoji.name]))})</small>"
            annotated_emojis.append(entry)
        return annotated_emojis

    def __write_metadata_file(self, target: Path) -> None:
        with (target / "copyme.py").open("w") as metadata_file:
            metadata_file.write("skin_tone_selectable_emojis={'")
            metadata_file.write("', '".join(self.__base_emojis))
            metadata_file.write("'}\n")

    def extract_to(self, target: Path) -> None:
        self.__fetch_data()
        self.__write_symbol_file(target)
        self.__write_metadata_file(target)
