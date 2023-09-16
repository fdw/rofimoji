import html
from pathlib import Path
from typing import Dict, List

import requests
from bs4 import BeautifulSoup
from lxml import etree
from lxml.etree import XPath
from tqdm import tqdm

from .blockfactory import Block
from .characterfactory import Character
from .extractor import Extractor


class EmojiExtractor(Extractor):
    __all_blocks: List[Block]
    __annotations: Dict[str, List[str]]
    __base_emojis: List[str]

    def __init__(self):
        self.__annotations = {}
        self.__all_blocks = []
        self.__ep_emojis = []
        self.__base_emojis = []

    def __fetch_data(self) -> None:
        with tqdm(total=3) as progress:
            progress.set_description("Downloading annotations")
            self.__fetch_annotations()
            progress.update(1)

            progress.set_description("Downloading list of additional emoji data")
            self.__fetch_additional_data()
            progress.update(1)

            progress.set_description("Downloading list of all emojis")
            self.__fetch_emoji_list()
            progress.update(1)

    def __fetch_emoji_list(self) -> None:
        data: requests.Response = requests.get(
            "https://unicode.org/emoji/charts-15.1/full-emoji-list.html", timeout=120
        )

        html = BeautifulSoup(data.text, "lxml")

        current_title = None
        current_emojis: List[Character] = []
        for row in html.find("table").find_all("tr"):
            if row.th and "bighead" in row.th["class"]:
                if current_title:
                    self.__all_blocks.append(Block(current_title, current_emojis))
                current_title = row.a.string
                current_emojis = []
            elif not row.th:
                emoji = row.find("td", {"class": "chars"}).string
                description = row.find("td", {"class": "name"}).string.replace("⊛ ", "")
                current_emojis.append(
                    Character(
                        emoji if emoji in self.__ep_emojis or len(emoji) > 1 else f"{emoji}️",
                        description,
                        "L",
                        self.__annotations.get(emoji, None),
                    )
                )

        self.__all_blocks.append(Block(current_title, current_emojis))

    def __fetch_annotations(self) -> None:
        data: requests.Response = requests.get(
            "https://raw.githubusercontent.com/unicode-org/cldr/latest/common/annotations/en.xml", timeout=60
        )

        xpath = XPath('./annotations/annotation[not(@type="tts")]')
        for element in xpath(etree.fromstring(data.content)):
            self.__annotations[element.get("cp")] = element.text.split(" | ")

    def __fetch_additional_data(self) -> None:
        def __extract_ep_emojis() -> None:
            started = False
            emojis = []
            for line in emoji_data:
                if not started and not line.startswith("# All omitted code points have Emoji_Presentation=No"):
                    continue
                else:
                    started = True
                if line.startswith("# Total elements:"):
                    break
                if line and not line.startswith("#"):
                    emojis.extend(self.__resolve_character_range(line.split(";")[0].strip()))

            self.__ep_emojis = emojis

        def __extract_base_emojis() -> None:
            started = False
            emojis = []
            for line in emoji_data:
                if not started and not line.startswith("# All omitted code points have Emoji_Modifier_Base=No"):
                    continue
                else:
                    started = True
                if line.startswith("# Total elements:"):
                    break
                if line and not line.startswith("#"):
                    emojis.extend(self.__resolve_character_range(line.split(";")[0].strip()))

            self.__base_emojis = emojis

        data: requests.Response = requests.get("https://unicode.org/Public/15.1.0/ucd/emoji/emoji-data.txt", timeout=60)
        emoji_data = data.text.split("\n")
        __extract_ep_emojis()
        __extract_base_emojis()

    def __resolve_character_range(self, line: str) -> List[str]:
        try:
            (start, end) = line.split("..")
            return [chr(char) for char in range(int(start, 16), int(end, 16) + 1)]
        except ValueError:
            return [self.__resolve_character(line)]

    def __resolve_character(self, string: str) -> str:
        return "".join(chr(int(character, 16)) for character in string.split(" "))

    def __write_symbol_file(self, target: Path) -> None:
        for block in self.__all_blocks:
            with (target / f"emojis_{block.name.lower().replace(' ', '').replace('&', '_')}.csv").open(
                "w"
            ) as symbol_file:
                for entry in self.__compile_entries(block):
                    symbol_file.write(entry + "\n")

    def __compile_entries(self, block: Block) -> List[str]:
        annotated_emojis = []
        for emoji in block.characters:
            entry = f"{emoji.char} {html.escape(emoji.name)}"
            if emoji.descriptions:
                entry += f" <small>({html.escape(', '.join(emoji.descriptions))})</small>"
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
