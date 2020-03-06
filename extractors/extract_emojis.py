import html
from collections import namedtuple
from typing import List, Dict

import requests
from bs4 import BeautifulSoup
from lxml import etree
from lxml.etree import XPath

from extractors.extractor import Extractor

Emoji = namedtuple('Emoji', 'char name')


class EmojiExtractor(Extractor):

    def __init__(self):
        super().__init__()
        self.annotations = self.fetch_annotations()

    def fetch_emoji_list(self: 'EmojiExtractor') -> List[Emoji]:
        print('Downloading list of all emojis')

        data = requests.get(
            'https://unicode.org/emoji/charts-13.0/full-emoji-list.html',
            timeout=120
        )  # type: requests.Response

        html = BeautifulSoup(data.content, 'lxml')

        emojis = []
        for row in html.find('table').find_all('tr'):
            if row.th:
                continue
            emoji = row.find('td', {'class': 'chars'}).string
            description = row.find('td', {'class': 'name'}).string.replace('⊛ ', '')

            emojis.append(Emoji(emoji, description))

        return emojis

    def fetch_human_emojis(self: 'EmojiExtractor') -> List[chr]:
        print('Downloading list of human emojis...')

        data = requests.get(
            'https://unicode.org/Public/13.0.0/ucd/emoji/emoji-data.txt',
            timeout=60
        )  # type: requests.Response

        started = False
        emojis = []
        for line in data.content.decode(data.encoding).split('\n'):
            if not started and line != '# All omitted code points have Emoji_Modifier_Base=No ':
                continue
            started = True
            if started and line == '# Total elements: 122':
                break
            if started and (line.startswith('#') or len(line) == 0):
                continue
            emojis.extend(self.resolve_character_range(line.split(';')[0].strip()))

        return emojis

    def fetch_annotations(self: 'EmojiExtractor') -> Dict[chr, List[str]]:
        print('Downloading annotations')

        data = requests.get(
            'https://raw.githubusercontent.com/unicode-org/cldr/latest/common/annotations/en.xml',
            timeout=60
        )  # type: requests.Response

        xpath = XPath('./annotations/annotation[not(@type="tts")]')
        return {element.get('cp'): element.text.split(' | ') for element in
                xpath(etree.fromstring(data.content))}

    def write_symbol_file(self: 'EmojiExtractor', all_emojis: List[Emoji]):
        print('Writing collected emojis to symbol file')
        symbol_file = open('../picker/data/emojis.csv', 'w')

        for entry in self.compile_entries(all_emojis):
            symbol_file.write(entry + "\n")

        symbol_file.close()

    def write_metadata_file(self: 'EmojiExtractor', human_emojis: List[chr]):
        print('Writing metadata to metadata file')
        metadata_file = open('../picker/copyme.py', 'w')

        metadata_file.write('skin_tone_selectable_emojis={\'')
        metadata_file.write('\', \''.join(human_emojis))
        metadata_file.write('\'}\n')
        metadata_file.close()

    def compile_entries(self: 'EmojiExtractor', emojis: List[Emoji]) -> List[str]:
        annotated_emojis = []
        for emoji in emojis:
            if emoji.char in self.annotations:
                entry = f"{emoji.char} {html.escape(emoji.name)} <small>({html.escape(', '.join(self.annotations[emoji.char]))})</small>"
            else:
                entry = f"{emoji.char} {html.escape(emoji.name)}"

            annotated_emojis.append(entry)

        return annotated_emojis

    def extract(self: 'EmojiExtractor'):
        self.write_symbol_file(self.fetch_emoji_list())
        self.write_metadata_file(self.fetch_human_emojis())
