from typing import Union

import requests


class Character(object):
    def __init__(self, char: int, name: str):
        self.char = chr(char)
        self.name = name.strip().title()


class CharacterFactory(object):
    def __init__(self: 'CharacterFactory'):
        self.__fetch_characters()

    def __fetch_characters(self: 'CharacterFactory'):
        print('Downloading the character\'s names')

        self.__characters = {}

        response = requests.get(
            'https://unicode.org/Public/UNIDATA/UnicodeData.txt',
            timeout=60
        )  # type: requests.Response

        lines = response.content.decode(response.encoding).split('\n')

        for line in lines:
            if len(line) == 0:
                continue
            fields = line.split(';')
            if fields[1].startswith('<'):
                continue
            character = Character(int(fields[0], 16), fields[1])
            self.__characters[character.char] = character

    def get_character(self: 'CharacterFactory', char: int) -> Union[Character, None]:
        try:
            return self.__characters[chr(char)]
        except KeyError:
            return None
