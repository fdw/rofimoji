import html
from pathlib import Path
from collections import namedtuple

import requests
from bs4 import BeautifulSoup

Icon = namedtuple('Icon', 'icon name')

class NerdExtractor(object):
    def __init__(self: 'NerdExtractor'):
        self.icons = []

    def fetch_icons(self: 'NerdExtractor'):
        print('Downloading list of Nerd Font icons')

        response = requests.get(
            'https://www.nerdfonts.com/cheat-sheet',
            timeout=60
        )

        characters = BeautifulSoup(response.content.decode(response.encoding), 'html.parser').find(id='glyphCheatSheet').find_all(class_='column')
        for c in characters:
            icon = chr(int(c.find(class_='codepoint').string, 16))
            name = c.find(class_='class-name').string
            self.icons.append(Icon(icon, name))


    def write_to_file(self: 'NerdExtractor'):
        if len(self.icons) == 0:
            return

        with Path("../picker/data/nerd_font.csv").open('w') as symbol_file:
            for icon in self.icons:
                symbol_file.write(f'{icon.icon} {html.escape(icon.name.lower())}\n')

        symbol_file.close()

    def extract(self: 'NerdExtractor'):
        self.fetch_icons()
        self.write_to_file()


if __name__ == '__main__':
    NerdExtractor().extract()
