from pathlib import Path
from typing import List

import aiofiles
import aiohttp

from .characterfactory import Character
from .extractor import Extractor


class FontAwesome6Extractor(Extractor):
    __icons: List[Character]

    def __init__(self):
        self.__icons = []

    async def extract_to(self, target: Path) -> None:
        await self.__fetch_icons()
        await self.__write_to_file(target)
        print("Finished FontAwesome 6")

    async def __fetch_icons(self) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/metadata/icons.json"
            ) as response:
                for name, data in (await response.json(content_type=None)).items():
                    icon = int(data["unicode"], 16)
                    name = f"fa-{name}"
                    char = Character(icon, name)
                    try:
                        for alias in data["aliases"]["names"]:
                            char.add_description(f"fa-{alias}")
                    except KeyError:
                        pass
                    self.__icons.append(char)

    async def __write_to_file(self, target: Path) -> None:
        async with aiofiles.open(target / "fontawesome6.csv", mode="w") as character_file:
            for icon in self.__icons:
                aliases = f" <small>({', '.join(icon.descriptions)})</small>"
                line = f'{icon.directional_char} {icon.lower_case_name}{aliases if icon.descriptions else ""}\n'
                await character_file.write(line)
