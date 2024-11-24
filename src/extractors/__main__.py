import asyncio
import pathlib

from .blockextractor import BlockExtractor
from .characterfactory import CharacterFactory
from .cjkextractor import CjkExtractor
from .emojiextractor import EmojiExtractor
from .extractor import Extractor
from .fileiconsextractor import FileIconsExtractor
from .fontawesome6extractor import FontAwesome6Extractor
from .gitmojiextractor import GitmojiExtractor
from .htmlcharacterextractor import HtmlCharacterExtractor
from .kaomojiextractor import KaomojiExtractor
from .mathcollectionextractor import MathExtractor
from .nerdfontextractor import NerdFontExtractor


async def extract_all():
    data_directory = pathlib.Path(__file__).parent.parent / "picker" / "data"

    character_factory = CharacterFactory()
    await character_factory.fetch_characters()

    extractors = [
        EmojiExtractor(),
        BlockExtractor(character_factory),
        CjkExtractor(),
        MathExtractor(character_factory),
        NerdFontExtractor(),
        GitmojiExtractor(),
        FontAwesome6Extractor(),
        KaomojiExtractor(),
        HtmlCharacterExtractor(),
        FileIconsExtractor(),
    ]

    for subclass in Extractor.__subclasses__():
        if not any(isinstance(extractor, subclass) for extractor in extractors):
            print(f"Did you forget to add an extractor of class {subclass.__name__}?")

    await asyncio.gather(*[extractor.extract_to(data_directory) for extractor in extractors])


if __name__ == "__main__":
    asyncio.run(extract_all())
