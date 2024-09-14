from operator import rshift
from pathlib import Path
from typing import List

import aiofiles
import aiohttp

from .characterfactory import Character
from .extractor import Extractor


class NerdFontExtractor(Extractor):
    __icons: List[Character]

    def __init__(self):
        self.__icons = []

    async def extract_to(self, target: Path) -> None:
        await self.__fetch_icons()
        await self.__write_to_file(target)
        print("Finished NerdFont")

    async def __fetch_icons(self) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://raw.githubusercontent.com/ryanoasis/nerd-fonts/master/glyphnames.json") as response:
                for key, value in (await response.json(content_type=None)).items():
                    if key == "METADATA":
                        continue
                    icon = int(value['code'], 16)
                    self.__icons.append(Character(icon, key))

    async def __write_to_file(self, target: Path) -> None:
        async with aiofiles.open(target / "nerd_font.csv", mode="w") as character_file:
            for icon in self.__icons:
                await character_file.write(f"{icon.directional_char} {icon.lower_case_name}\n")
