import html
from collections import namedtuple
from pathlib import Path
from typing import List

import requests
from bs4 import BeautifulSoup

Emoji = namedtuple('Emoji', 'char name')


class EmojiExtractor(object):

    def __init__(self):
        self.all_emojis = self.fetch_emoji_list()
        self.base_emojis = self.fetch_base_emojis()

    def fetch_emoji_list(self: 'EmojiExtractor') -> List[Emoji]:
        print('Downloading list of all emojis')

        data = requests.get(
            'https://unicode.org/emoji/charts-14.0/full-emoji-list.html',
            timeout=120
        )  # type: requests.Response

        html = BeautifulSoup(data.text, 'lxml')

        emojis = []
        for row in html.find('table').find_all('tr'):
            if not row.th:
                emoji = row.find('td', {'class': 'chars'}).string
                description = row.find('td', {'class': 'name'}).string.replace('⊛ ', '')
                emojis.append(Emoji(emoji, description))

        return emojis

    def fetch_base_emojis(self: 'EmojiExtractor') -> List[chr]:
        print('Downloading list of human emojis...')

        data = requests.get(
            'https://unicode.org/Public/14.0.0/ucd/emoji/emoji-data.txt',
            timeout=60
        )  # type: requests.Response

        started = False
        emojis = []
        for line in data.text.split('\n'):
            if not started and line != '# All omitted code points have Emoji_Modifier_Base=No ':
                continue
            started = True
            if line == '# Total elements: 132':
                break
            if line and not line.startswith('#'):
                emojis.extend(self.resolve_character_range(line.split(';')[0].strip()))

        return emojis

    def resolve_character_range(self, line: str) -> List[str]:
        try:
            (start, end) = line.split('..')
            return [chr(char) for char in range(int(start, 16), int(end, 16) + 1)]
        except ValueError:
            return [self.resolve_character(line)]

    def resolve_character(self, string: str) -> str:
        return "".join(chr(int(character, 16)) for character in string.split(' '))

    def write_symbol_file(self: 'EmojiExtractor'):
        print('Writing collected emojis to symbol file')
        with Path('../picker/data/emojis.csv').open('w') as symbol_file:
            for emoji in self.all_emojis:
                symbol_file.write(f"{emoji.char} {html.escape(emoji.name)}" + "\n")

    def write_metadata_file(self: 'EmojiExtractor'):
        print('Writing metadata to metadata file')
        with Path('../picker/copyme.py').open('w') as metadata_file:
            metadata_file.write('skin_tone_selectable_emojis={\'')
            metadata_file.write('\', \''.join(self.base_emojis))
            metadata_file.write('\'}\n')

    def extract(self: 'EmojiExtractor') -> None:
        self.write_symbol_file()
        self.write_metadata_file()
