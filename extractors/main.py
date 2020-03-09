from extractors.BlockExtractor import BlockExtractor
from extractors.CharacterFactory import CharacterFactory
from extractors.EmojiExtractor import EmojiExtractor
from extractors.MathCollectionExtractor import MathExtractor

if __name__ == "__main__":
    character_factory = CharacterFactory()

    EmojiExtractor().extract()
    BlockExtractor(character_factory).extract()
    MathExtractor(character_factory).extract()
