import html
from pathlib import Path

import requests

from .characterfactory import Character


class GitmojiExtractor(object):
    def __init__(self: 'GitmojiExtractor'):
        self.icons = []

    def fetch_icons(self: 'GitmojiExtractor'):
        print("Downloading list of gitmojis")

        response = requests.get(
            "https://raw.githubusercontent.com/carloscuesta/gitmoji/master/src/data/gitmojis.json",
            timeout=60
        )
        """
        {
            'emoji': '🎨',
            'entity': '&#x1f3a8;',
            'code': ':art:',
            'description': 'Improve structure / format of the code.',
            'name': 'art',
            'semver': None
        }
        """
        for char in response.json()["gitmojis"]:
            icon = ord(char["emoji"][0])
            name = char["description"]
            self.icons.append(Character(icon, name))

    def write_to_file(self: 'GitmojiExtractor'):
        with (Path(__file__).parent.parent / 'picker' / 'data' / 'gitmoji.csv').open('w') as symbol_file:
            for icon in self.icons:
                symbol_file.write(
                    f"{icon.directional_char} {html.escape(icon.name.lower())}\n")

    def extract(self: 'GitmojiExtractor'):
        self.fetch_icons()
        self.write_to_file()


if __name__ == '__main__':
    GitmojiExtractor().extract()
