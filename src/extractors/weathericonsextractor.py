from pathlib import Path
from typing import List

import aiofiles
import aiohttp
from bs4 import BeautifulSoup

from .characterfactory import Character
from .extractor import Extractor


class WeatherIconsExtractor(Extractor):
    __icons: List[Character]

    def __init__(self):
        self.__icons = []

    async def extract_to(self, target: Path) -> None:
        await self.__fetch_icons()
        await self.__write_to_file(target)
        print("Finished Weather Icons")

    async def __fetch_icons(self) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://raw.githubusercontent.com/erikflowers/weather-icons/refs/heads/master/values/weathericons.xml"
            ) as response:
                html_content = BeautifulSoup(await response.text(), "xml")

                for row in html_content.find("resources").find_all("string"):
                    self.__icons.append(Character(row.string, row["name"]))

    async def __write_to_file(self, target: Path) -> None:
        async with aiofiles.open(target / "weathericons.csv", mode="w") as character_file:
            for icon in self.__icons:
                await character_file.write(f"{icon.directional_char} {icon.lower_case_name}\n")
