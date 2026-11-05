import html
from dataclasses import dataclass
from itertools import groupby
from pathlib import Path

import aiofiles
import aiohttp

from .extractor import Extractor


@dataclass(slots=True)
class Kaomoji:
    string: str
    group: str
    description: str


class KaomojiExtractor(Extractor):
    __kaomojis: list[Kaomoji]

    def __init__(self):
        self.__kaomojis = []

    async def extract_to(self, target: Path) -> None:
        await self.__fetch_icons()
        await self.__write_to_file(target)
        print("Finished Kaomoji")

    async def __fetch_icons(self) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://raw.githubusercontent.com/Funovate-Technology/fontvibe-kaomoji/v1.0.9/data/picker.json"
            ) as response:
                """
                {
                  "text": "(⊃‿⊂)",
                  "group": "shy",
                  "keywords": [
                    "shy",
                    "hide"
                  ]
                }
                """
                for kaomoji in await response.json(content_type=None):
                    self.__kaomojis.append(
                        Kaomoji(kaomoji["text"].replace(" ", " "), kaomoji["group"], ", ".join(kaomoji["keywords"]))
                    )

    async def __write_to_file(self, target: Path) -> None:
        by_group = sorted(self.__kaomojis, key=lambda kaomoji: kaomoji.group)
        for group, kaomojis in groupby(by_group, key=lambda kaomoji: kaomoji.group):
            async with aiofiles.open(target / f"kaomoji_{group}.csv", mode="w") as character_file:
                for kaomoji in kaomojis:
                    await character_file.write(
                        f"{html.escape(kaomoji.string)} {html.escape(kaomoji.description.lower())}\n"
                    )
