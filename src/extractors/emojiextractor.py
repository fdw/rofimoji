import asyncio
import html
from pathlib import Path
from typing import Dict, List

import aiofiles
import aiohttp
from aiohttp import ClientSession, ClientTimeout
from bs4 import BeautifulSoup
from lxml import etree
from lxml.etree import XPath

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

    async def extract_to(self, target: Path) -> None:
        await self.__fetch_data()
        await self.__write_character_file(target)
        await self.__write_metadata_file(target)
        print("Finished Emoji")

    async def __fetch_data(self) -> None:
        async with aiohttp.ClientSession(timeout=ClientTimeout(sock_read=120)) as session:
            await asyncio.gather(
                self.__fetch_emoji_list(session),
                self.__fetch_annotations(session),
                self.__fetch_additional_data(session),
            )

    async def __fetch_emoji_list(self, session: ClientSession) -> None:
        async with session.get("https://unicode.org/emoji/charts-17.0/full-emoji-list.html") as data:
            html_content = BeautifulSoup(await data.text(), "lxml")

            current_title = None
            current_emojis: List[Character] = []
            for row in html_content.find("table").find_all("tr"):
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

    async def __fetch_annotations(self, session: ClientSession) -> None:
        async with session.get(
            "https://raw.githubusercontent.com/unicode-org/cldr/latest/common/annotations/en.xml"
        ) as data:
            xpath = XPath('./annotations/annotation[not(@type="tts")]')
            for element in xpath(etree.fromstring(await data.read())):
                self.__annotations[element.get("cp")] = element.text.split(" | ")

    async def __fetch_additional_data(self, session: ClientSession) -> None:
        def __extract_ep_emojis(emoji_data: List[str]) -> None:
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

        def __extract_base_emojis(emoji_data: List[str]) -> None:
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

        async with session.get("https://unicode.org/Public/17.0.0/ucd/emoji/emoji-data.txt") as data:
            emoji_data = (await data.text()).split("\n")
            __extract_ep_emojis(emoji_data)
            __extract_base_emojis(emoji_data)

    def __resolve_character_range(self, line: str) -> List[str]:
        try:
            (start, end) = line.split("..")
            return [chr(char) for char in range(int(start, 16), int(end, 16) + 1)]
        except ValueError:
            return [self.__resolve_character(line)]

    def __resolve_character(self, string: str) -> str:
        return "".join(chr(int(character, 16)) for character in string.split(" "))

    async def __write_character_file(self, target: Path) -> None:
        for block in self.__all_blocks:
            async with aiofiles.open(
                target / f"emojis_{block.name.lower().replace(' ', '').replace('&', '_')}.csv", mode="w"
            ) as character_file:
                for entry in self.__compile_entries(block):
                    await character_file.write(entry + "\n")

    def __compile_entries(self, block: Block) -> List[str]:
        annotated_emojis = []
        for emoji in block.characters:
            entry = f"{emoji.char} {html.escape(emoji.name)}"
            if emoji.descriptions:
                entry += f" <small>({html.escape(', '.join(emoji.descriptions))})</small>"
            annotated_emojis.append(entry)
        return annotated_emojis

    async def __write_metadata_file(self, target: Path) -> None:
        async with aiofiles.open(target / "copyme.py", mode="w") as metadata_file:
            await metadata_file.write("skin_tone_selectable_emojis={'")
            await metadata_file.write("', '".join(self.__base_emojis))
            await metadata_file.write("'}\n")
