#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import fnmatch
import os
import shlex
import sys
from subprocess import Popen, PIPE
from typing import List, Tuple

import configargparse
from xdg import BaseDirectory

skin_tone_selectable_emojis = {'☝', '⛹', '✊', '✋', '✌', '✍', '🎅', '🏂', '🏃', '🏄', '🏇', '🏊',
                               '🏋', '🏌', '👂', '👃', '👆', '👇', '👈', '👉', '👊', '👋', '👌',
                               '👍', '👎', '👏', '👐', '👦', '👧', '👨', '👩', '👪', '👫', '👬',
                               '👭', '👮', '👯', '👰', '👱', '👲', '👳', '👴', '👵', '👶', '👷',
                               '👸', '👼', '💁', '💂', '💃', '💅', '💆', '💇', '💏', '💑', '💪',
                               '🕴', '🕵', '🕺', '🖐', '🖕', '🖖', '🙅', '🙆', '🙇', '🙋', '🙌',
                               '🙍', '🙎', '🙏', '🚣', '🚴', '🚵', '🚶', '🛀', '🛌', '🤌', '🤏',
                               '🤘', '🤙', '🤚', '🤛', '🤜', '🤝', '🤞', '🤟', '🤦', '🤰', '🤱',
                               '🤲', '🤳', '🤴', '🤵', '🤶', '🤷', '🤸', '🤹', '🤼', '🤽', '🤾',
                               '🥷', '🦵', '🦶', '🦸', '🦹', '🦻', '🧍', '🧎', '🧏', '🧑', '🧒',
                               '🧓', '🧔', '🧕', '🧖', '🧗', '🧘', '🧙', '🧚', '🧛', '🧜', '🧝'}

fitzpatrick_modifiers = {
    '': 'neutral',
    '🏻': 'light skin',
    '🏼': 'medium-light skin',
    '🏽': 'moderate skin',
    '🏾': 'dark brown skin',
    '🏿': 'black skin'
}

fitzpatrick_modifiers_reversed = {" ".join(name.split()[:-1]): modifier for modifier, name in
                                  fitzpatrick_modifiers.items() if name != "neutral"}


def main() -> None:
    args = parse_arguments()
    active_window = get_active_window()

    returncode, stdout = open_main_rofi_window(args.rofi_args, read_character_files(args.files))

    if returncode == 1:
        sys.exit()
    else:
        characters = process_chosen_characters(stdout.splitlines(), args.skin_tone, args.rofi_args)

        if returncode == 0:
            if args.copy_only:
                copy_characters_to_clipboard(characters)
            else:
                insert_characters(characters, active_window, args.insert_with_clipboard)
        elif returncode == 10:
            copy_characters_to_clipboard(characters)
        elif returncode == 11:
            type_characters(characters, active_window)
        elif returncode == 12:
            copy_paste_characters(characters, active_window)


def parse_arguments() -> argparse.Namespace:
    parser = configargparse.ArgumentParser(
        description='Select, insert or copy Unicode characters using rofi',
        default_config_files=[os.path.join(directory, 'rofimoji.rc') for directory in
                              BaseDirectory.xdg_config_dirs]
    )
    parser.add_argument('--version', action='version', version='rofimoji 4.0.0-SNAPSHOT')
    parser.add_argument(
        '--insert-with-clipboard',
        '-p',
        dest='insert_with_clipboard',
        action='store_true',
        help='Do not type the character directly, but copy it to the clipboard, insert it from '
             'there and then restore the clipboard\'s original value '
    )
    parser.add_argument(
        '--copy-only',
        '-c',
        dest='copy_only',
        action='store_true',
        help='Only copy the character to the clipboard but do not insert it'
    )
    parser.add_argument(
        '--skin-tone',
        '-s',
        dest='skin_tone',
        action='store',
        choices=['neutral', 'light', 'medium-light', 'moderate', 'dark brown', 'black', 'ask'],
        default='ask',
        help='Decide on a skin-tone for all supported emojis. If not set (or set to "ask"), '
             'you will be asked for each one '
    )
    parser.add_argument(
        '--files',
        '-f',
        dest='files',
        action='store',
        default=['emojis'],
        nargs='+',
        metavar='FILE',
        help='Read characters from this file instead, one entry per line'
    )
    parser.add_argument(
        '--rofi-args',
        dest='rofi_args',
        action='store',
        default='',
        help='A string of arguments to give to rofi'
    )

    parsed_args = parser.parse_args()
    parsed_args.rofi_args = shlex.split(parsed_args.rofi_args)

    return parsed_args


def get_active_window() -> str:
    xdotool = Popen(args=['xdotool', 'getactivewindow'], stdout=PIPE)
    return xdotool.communicate()[0].decode("utf-8")[:-1]


def read_character_files(file_names: List[str]) -> str:
    entries = ''

    if len(file_names) == 1 and file_names[0] == 'all':
        file_names = [os.path.splitext(file)[0] for file in
                      os.listdir(os.path.join(os.path.dirname(__file__), "data"))
                      if fnmatch.fnmatch(file, "*.csv")]

    for file_name in file_names:
        entries = entries + load_from_file(file_name)

    return entries


def load_from_file(file_name: str) -> str:
    provided_file = os.path.join(os.path.dirname(__file__), "data", file_name + '.csv')
    if os.path.isfile(file_name):
        actual_file_name = file_name
    elif os.path.isfile(provided_file):
        actual_file_name = provided_file
    else:
        raise FileNotFoundError(f"Couldn't find file {file_name}")

    with open(actual_file_name, "r") as file:
        return file.read()


def load_all_characters() -> str:
    characters = ""

    directory = os.path.join(os.path.dirname(__file__), "data")
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), "r") as file:
            characters = characters + file.read()
    return characters


def open_main_rofi_window(args: List[str], characters: str) -> Tuple[int, bytes]:
    rofi = Popen(
        [
            'rofi',
            '-dmenu',
            '-markup-rows',
            '-i',
            '-multi-select',
            '-p',
            ' 😀   ',
            '-kb-custom-1',
            'Alt+c',
            '-kb-custom-2',
            'Alt+t',
            '-kb-custom-3',
            'Alt+p',
            *args
        ],
        stdin=PIPE,
        stdout=PIPE
    )
    (stdout, _) = rofi.communicate(input=characters.encode('UTF-8'))
    return rofi.returncode, stdout


def process_chosen_characters(
        chosen_characters: List[bytes],
        skin_tone: str,
        rofi_args: List[str]
) -> str:
    result = ""
    for line in chosen_characters:
        character = line.decode('utf-8').split()[0]

        if character in skin_tone_selectable_emojis:
            character = select_skin_tone(character, skin_tone, rofi_args)

        result += character

    return result


def select_skin_tone(selected_emoji: chr, skin_tone: str, rofi_args: List[str]) -> str:
    if skin_tone == 'neutral':
        return selected_emoji
    elif skin_tone != 'ask':
        return selected_emoji + fitzpatrick_modifiers_reversed[skin_tone]
    else:
        modified_emojis = '\n'.join(map(
            lambda modifier: selected_emoji + modifier + " " + fitzpatrick_modifiers[modifier],
            fitzpatrick_modifiers.keys()
        ))

        rofi_skin = Popen(
            [
                'rofi',
                '-dmenu',
                '-i',
                '-p',
                selected_emoji + '   ',
                *rofi_args
            ],
            stdin=PIPE,
            stdout=PIPE
        )

        (stdout_skin, _) = rofi_skin.communicate(input=modified_emojis.encode('utf-8'))

        if rofi_skin.returncode == 1:
            return ''

        return stdout_skin.split()[0].decode('utf-8')


def insert_characters(
        characters: str,
        active_window: str,
        insert_with_clipboard: bool = False
) -> None:
    if insert_with_clipboard:
        copy_paste_characters(characters, active_window)
    else:
        type_characters(characters, active_window)


def copy_paste_characters(characters: str, active_window: str) -> None:
    old_clipboard_content = Popen(args=['xsel', '-o', '-b'], stdout=PIPE) \
        .communicate()[0]
    old_primary_content = Popen(args=['xsel', '-o', '-p'], stdout=PIPE) \
        .communicate()[0]

    Popen(args=['xsel', '-i', '-b'], stdin=PIPE) \
        .communicate(input=characters.encode('utf-8'))
    Popen(args=['xsel', '-i', '-p'], stdin=PIPE) \
        .communicate(input=characters.encode('utf-8'))

    Popen([
        'xdotool',
        'windowfocus',
        '--sync',
        active_window,
        'key',
        '--clearmodifiers',
        'Shift+Insert',
        'sleep',
        '0.05',
    ]).wait()

    Popen(args=['xsel', '-i', '-b'], stdin=PIPE) \
        .communicate(input=old_clipboard_content)
    Popen(args=['xsel', '-i', '-p'], stdin=PIPE) \
        .communicate(input=old_primary_content)


def type_characters(characters: str, active_window: str) -> None:
    Popen([
        'xdotool',
        'type',
        '--clearmodifiers',
        '--window',
        active_window,
        characters
    ])


def copy_characters_to_clipboard(characters: str) -> None:
    xsel = Popen(
        [
            'xsel',
            '-i',
            '-b'
        ],
        stdin=PIPE
    )
    xsel.communicate(input=characters.encode('utf-8'))


if __name__ == "__main__":
    main()
