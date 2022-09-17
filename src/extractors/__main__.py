import pathlib

from tqdm import tqdm

from .blockextractor import BlockExtractor
from .characterfactory import CharacterFactory
from .cjkextractor import CjkExtractor
from .emojiextractor import EmojiExtractor
from .extractor import Extractor
from .gitmojiextractor import GitmojiExtractor
from .mathcollectionextractor import MathExtractor
from .nerdfontextractor import NerdFontExtractor
from .fontawesome6extractor import FontAwesome6Extractor

if __name__ == "__main__":
    data_directory = pathlib.Path(__file__).parent.parent / "picker" / "data"

    character_factory = CharacterFactory()

    extractors = [
        EmojiExtractor(),
        BlockExtractor(character_factory),
        CjkExtractor(),
        MathExtractor(character_factory),
        NerdFontExtractor(),
        GitmojiExtractor(),
        FontAwesome6Extractor(),
    ]

    for subclass in Extractor.__subclasses__():
        if not any(isinstance(extractor, subclass) for extractor in extractors):
            print(f"Did you forget to add an extractor of class {subclass.__name__}?")

    progress = tqdm(extractors)
    for extractor in progress:
        progress.set_description(extractor.__class__.__name__)
        extractor.extract_to(data_directory)
