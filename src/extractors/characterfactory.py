from typing import Union

import requests
from unicodedata import bidirectional


class Character(object):
    ltr_mark = '\u200e'

    def __init__(self, char: int, name: str, bidi_class: str = None):
        self.char = chr(char)
        self.name = name.strip().title()
        if not bidi_class:
            bidi_class = bidirectional(self.char)
        self.force_ltr = bidi_class in ('AL', 'AN', 'R', 'RLE', 'RLI', 'RLO')

    @property
    def directional_char(self):
        return f'{self.ltr_mark if self.force_ltr else ""}{self.char}'


class CharacterFactory(object):
    def __init__(self: 'CharacterFactory'):
        self.__characters = {}
        self.__fetch_characters()

    def __fetch_characters(self: 'CharacterFactory') -> None:
        INDEX_CODEPOINT = 0
        INDEX_NAME = 1
        INDEX_CATEGORY = 2
        INDEX_BIDI_CLASS = 4

        print('Downloading the character\'s names')

        response = requests.get(
            'https://unicode.org/Public/UNIDATA/UnicodeData.txt',
            timeout=60
        )  # type: requests.Response

        lines = response.content.decode(response.encoding).split('\n')

        for line in lines:
            fields = line.split(';')
            if len(fields) >= 2 and not fields[INDEX_CATEGORY] in ('Cc', 'Co', 'Cs') and \
                    not (fields[INDEX_NAME].startswith('<') and fields[INDEX_NAME].endswith('>')):
                character = Character(
                    int(fields[INDEX_CODEPOINT], 16),
                    fields[INDEX_NAME],
                    fields[INDEX_BIDI_CLASS]
                )
                self.__characters[character.char] = character

    def get_character(self: 'CharacterFactory', char: int) -> Union[Character, None]:
        return self.__characters.get(chr(char))
