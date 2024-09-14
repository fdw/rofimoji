from pathlib import Path
from typing import List

import aiofiles
import aiohttp

from .characterfactory import Character
from .extractor import Extractor


class GitmojiExtractor(Extractor):
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
                "https://raw.githubusercontent.com/carloscuesta/gitmoji/master/packages/gitmojis/src/gitmojis.json"
            ) as response:
                """
                {
                    'emoji': '🎨',
                    'entity': '&#x1f3a8;',
                    'code': ':art:',
                    'description': 'Improve structure / format of the code.',
                    'name': 'art',
                    'semver': None
                }
                """
                for char in (await response.json(content_type=None))["gitmojis"]:
                    icon = ord(char["emoji"][0])
                    name = char["description"]
                    self.__icons.append(Character(icon, name))

    async def __write_to_file(self, target: Path) -> None:
        async with aiofiles.open(target / "gitmoji.csv", mode="w") as character_file:
            for icon in self.__icons:
                await character_file.write(f"{icon.directional_char} {icon.lower_case_name}\n")
