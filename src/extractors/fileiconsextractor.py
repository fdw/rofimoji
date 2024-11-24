from pathlib import Path
from typing import List

import aiofiles
import aiohttp
from bs4 import BeautifulSoup

from .characterfactory import Character
from .extractor import Extractor


class FileIconsExtractor(Extractor):
    __icons: List[Character]

    def __init__(self):
        self.__icons = []

    async def extract_to(self, target: Path) -> None:
        await self.__fetch_icons()
        await self.__write_to_file(target)
        print("Finished Gitmoji")

    async def __fetch_icons(self) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://raw.githubusercontent.com/file-icons/icons/refs/heads/master/charmap.md"
            ) as response:
                for line in (await response.text()).split("\n"):
                    if line and line.strip().startswith("<tbody>"):
                        html = BeautifulSoup(line, "lxml")
                        name = html.find_all("td")[1].string
                        codepoint = int(html.find_all("td")[2].code.string[1:], 16)
                        self.__icons.append(
                            Character(
                                codepoint,
                                name,
                            )
                        )

    async def __write_to_file(self, target: Path) -> None:
        async with aiofiles.open(target / "fileicons.csv", mode="w") as character_file:
            for icon in self.__icons:
                await character_file.write(f"{icon.directional_char} {icon.lower_case_name}\n")
