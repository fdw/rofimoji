import typing
from pathlib import Path

import aiofiles
import aiohttp

from .blockfactory import Block, BlockFactory
from .characterfactory import CharacterFactory
from .extractor import Extractor


class BlockExtractor(Extractor):
    __blocks: typing.List[Block]
    __block_factory: BlockFactory

    def __init__(self, character_factory: CharacterFactory):
        super().__init__()
        self.__blocks = []
        self.__block_factory = BlockFactory(character_factory)

    async def extract_to(self, target: Path) -> None:
        await self.__fetch_blocks()
        await self.__write_to_files(target)
        print("Finished Unicode")

    async def __fetch_blocks(self) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://www.unicode.org/Public/17.0.0/ucd/Blocks.txt") as response:
                lines = (await response.text()).split("\n")

                for line in lines:
                    if not line or line.startswith(("#", "@")):
                        continue
                    key, _, value = line.partition(";")
                    self.__blocks.append(self.__block_factory.build_block_from_range(value.strip(), key.strip()))

    async def __write_to_files(self, target: Path) -> None:
        for block in self.__blocks:
            if not block.characters:
                continue

            async with aiofiles.open(
                target / f"{block.name.lower().replace(' ', '_')}.csv", mode="w"
            ) as character_file:
                for character in block.characters:
                    await character_file.write(f"{character.directional_char} {character.title_case_name}\n")
