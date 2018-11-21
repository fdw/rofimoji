import requests
from bs4 import BeautifulSoup
from collections import namedtuple
from typing import List

Emoji = namedtuple('Emoji', 'char name')


def fetch_emoji_html() -> BeautifulSoup:
    max_tries = 5
    for i in range(max_tries):
        print('Downloading emojis... try %s' % (i + 1))
        data = requests.get('https://unicode.org/emoji/charts-11.0/full-emoji-list.html', timeout=120)  # type: requests.Response
        if data:
            break

    if not data:
        print('Could not fetch emoji data. Try again later or use another URL.')
        exit(10)
    return BeautifulSoup(data.content, 'lxml')


def extract_from_html(html: BeautifulSoup) -> List[Emoji]:
    emojis = []

    for row in html.find('table').find_all('tr'):
        if row.th:
            continue
        emoji = row.find('td', {'class': 'chars'}).string
        description = row.find('td', {'class': 'name'}).string.replace('⊛ ', '')

        emojis.append(Emoji(emoji, description))

    return emojis


def write_file(emojis: List[Emoji]):
    python_file = open('emojis.py', 'w')
    python_file.write('emojis="""')

    for emoji in emojis:
        python_file.write(emoji.char + ' ' + emoji.name + '\n')

    python_file.write('"""')
    python_file.close()


write_file(extract_from_html(fetch_emoji_html()))
