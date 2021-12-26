import html
import io
import zipfile
from collections import namedtuple
from pathlib import Path
from typing import List, Dict

import requests
from bs4 import BeautifulSoup

Emoji = namedtuple('Emoji', 'char name')


class EmojiExtractor(object):

    def __init__(self):
        self.all_emojis = self.fetch_emoji_list()
        self.annotations = self.fetch_annotations()
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

    def fetch_annotations(self: 'EmojiExtractor') -> Dict[str, Dict[chr, List[str]]]:
        print('Downloading annotations')

        response = requests.get(
            'https://unicode.org/Public/cldr/39/cldr-common-39.0.zip',
            timeout=60
        )  # type: requests.Response

        characters = {}
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip:
            for path in zipfile.Path(zip, at='common/annotations/').iterdir():
                with path.open(encoding='utf-8') as file:
                    data = BeautifulSoup(file.read(), 'lxml-xml')

                    language = data.identity.language.attrs['type']

                    if language not in characters:
                        characters[language] = {}

                    if not data.annotations:
                        continue

                    for annotation in data.annotations.find_all('annotation'):
                        if 'type' in annotation.attrs and annotation.attrs['type'] == 'tts':
                            continue

                        characters[language][annotation['cp']] = [it.strip() for it in annotation.string.split('|')]

        return characters

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
            for entry in self.compile_entries():
                symbol_file.write(entry + "\n")

    def compile_entries(self: 'EmojiExtractor') -> List[str]:
        annotated_emojis = []
        for emoji in self.all_emojis:
            entry = f"{emoji.char} {html.escape(emoji.name)}"
            if emoji.char in self.annotations['en']:
                entry += f" <small>({html.escape(', '.join([annotation for annotation in self.annotations['en'][emoji.char] if annotation != emoji.name]))})</small>"
            annotated_emojis.append(entry)
        return annotated_emojis

    def write_localized_files(self: 'EmojiExtractor') -> None:
        print('Writing localized annotations files')
        for language in self.annotations.keys():
            filename = f'../picker/data/additional/emojis.{language}.csv'
            with Path(filename).open('w') as additional_file:
                for (character, annotations) in self.annotations[language].items():
                    additional_file.write(f'{character} <small>({html.escape(", ".join(annotations))})</small>\n')

    def write_metadata_file(self: 'EmojiExtractor'):
        print('Writing metadata to metadata file')
        with Path('../picker/copyme.py').open('w') as metadata_file:
            metadata_file.write('skin_tone_selectable_emojis={\'')
            metadata_file.write('\', \''.join(self.base_emojis))
            metadata_file.write('\'}\n')

    def extract(self: 'EmojiExtractor') -> None:
        self.write_symbol_file()
        self.write_localized_files()
        self.write_metadata_file()
