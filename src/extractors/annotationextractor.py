import io
import zipfile
from typing import List, Dict
import html
from pathlib import Path


import requests
from bs4 import BeautifulSoup


class AnnotationExtractor(object):
    def __init__(self):
        self.annotations = self.fetch_annotations()

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

    def write_annotation_files(self: 'EmojiExtractor') -> None:
        print('Writing localized annotations files')
        for language in self.annotations.keys():
            filename = f'../picker/data/annotations/{language}.csv'
            with Path(filename).open('w') as additional_file:
                for (character, annotations) in self.annotations[language].items():
                    additional_file.write(f'{character} {html.escape(", ".join(annotations))}\n')

    def extract(self: 'EmojiExtractor') -> None:
        self.write_annotation_files()
