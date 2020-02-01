import html
from collections import namedtuple
from typing import List, Dict

import requests

Character = namedtuple('Character', 'char name script')

supported_scripts = (
    'latin',
    'arabic',
    'egyptian',
    'hebrew',
    'greek',
    'cyrillic',
    'armenian',
    'arabic-indic',
    'samaritan',
    'bengali',
    'coptic',
    'glagolitic',
    'devanagari',
    'gurmukhi',
    'gujarati',
    'telugu',
    'kannada',
    'malayalam',
    'sinhala',
    'tibetan',
    'myanmar',
    'khmer',
    'balinese',
    'brahmi',
    'sharada',
    'grantha',
    'georgian',
    'hangul',
    'hiragana',
    'katakana',
    'bopomofo',
    'yi',
    'tangut',
    'ethiopic',
    'cherokee',
    'mongolian',
    'cypriot',
    'cuneiform',
    'braille',
    'vai',
    'bamum',
    'miao',
    'signwriting'
)


def fetch_unicode_characters() -> List[Character]:
    response = requests.get(
        'https://unicode.org/Public/UCA/latest/allkeys.txt',
        timeout=60
    )  # type: requests.Response

    lines = response.content.decode(response.encoding).split('\n')
    characters = []

    for line in lines:
        if line.startswith('#') or line.startswith('@') or len(line) == 0:
            continue
        character = extract_characters(line.split(';')[0].strip())
        description = line.split('#')[-1].strip()
        name = description.title()
        script = description.split(' ')[0].strip().lower()
        characters.append(Character(character, name, script))

    return characters


def extract_characters(string: str) -> str:
    result = []
    for character in string.split(' '):
        result.append(chr(int(character, 16)))

    return "".join(result)


def split_scripts(characters: List[Character]) -> Dict[str, List[Character]]:
    result = {}
    for character in characters:
        if character.script not in supported_scripts:
            continue
        if character.script not in result:
            result[character.script] = []
        result[character.script].append(character)

    return result


def write_symbol_files(all_characters: Dict[str, List[Character]]):
    print('Writing collected emojis to script files')
    for script in all_characters.keys():
        symbol_file = open(f"../picker/data/{script}.csv", 'w')

        for character in all_characters[script]:
            symbol_file.write(f"{character.char} {html.escape(character.name)}\n")

        symbol_file.close()


if __name__ == "__main__":
    write_symbol_files(split_scripts(fetch_unicode_characters()))
