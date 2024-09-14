import html
from dataclasses import dataclass
from pathlib import Path
from typing import List

import aiofiles
import aiohttp

from .extractor import Extractor


@dataclass
class Kaomoji:
    string: str
    description: str


class KaomojiExtractor(Extractor):
    __kaomojis: List[Kaomoji]

    def __init__(self):
        self.__kaomojis = []

    async def extract_to(self, target: Path) -> None:
        await self.__fetch_icons()
        await self.__write_to_file(target)
        print("Finished Kaomoji")

    async def __fetch_icons(self) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://raw.githubusercontent.com/w33ble/emoticon-data/master/emoticons.json"
            ) as response:
                """
                {
                  "tags": [
                    "hide"
                  ],
                  "string": "(⊃‿⊂)",
                  "id": "f73741a5-13f9-44a3-9dfe-4bce15c44cda"
                }
                """
                for kaomoji in (await response.json(content_type=None))["emoticons"]:
                    self.__kaomojis.append(Kaomoji(kaomoji["string"].replace(" ", " "), ", ".join(kaomoji["tags"])))

    async def __write_to_file(self, target: Path) -> None:
        async with aiofiles.open(target / "kaomoji.csv", mode="w") as character_file:
            for kaomoji in self.__kaomojis:
                await character_file.write(f"{kaomoji.string} {html.escape(kaomoji.description.lower())}\n")
