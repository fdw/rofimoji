#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse
import os
import sys
from subprocess import Popen, PIPE
from typing import List, Tuple, Union

import configargparse
import xdg
from xdg import BaseDirectory

skin_tone_selectable_emojis = {'☝', '⛹', '✊', '✋', '✌', '✍', '🎅', '🏂', '🏃', '🏄', '🏇', '🏊',
                               '🏋', '🏌', '👂', '👃', '👆', '👇', '👈', '👉', '👊', '👋', '👌',
                               '👍', '👎', '👏', '👐', '👦', '👧', '👨', '👩', '👪', '👫', '👬',
                               '👭', '👮', '👯', '👰', '👱', '👲', '👳', '👴', '👵', '👶', '👷',
                               '👸', '👼', '💁', '💂', '💃', '💅', '💆', '💇', '💏', '💑', '💪',
                               '🕴', '🕵', '🕺', '🖐', '🖕', '🖖', '🙅', '🙆', '🙇', '🙋', '🙌',
                               '🙍', '🙎', '🙏', '🚣', '🚴', '🚵', '🚶', '🛀', '🛌', '🤏', '🤘',
                               '🤙', '🤚', '🤛', '🤜', '🤝', '🤞', '🤟', '🤦', '🤰', '🤱', '🤲',
                               '🤳', '🤴', '🤵', '🤶', '🤷', '🤸', '🤹', '🤼', '🤽', '🤾', '🦵',
                               '🦶', '🦸', '🦹', '🦻', '🧍', '🧎', '🧏', '🧑', '🧒', '🧓', '🧔',
                               '🧕', '🧖', '🧗', '🧘', '🧙', '🧚', '🧛', '🧜', '🧝'}

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

    returncode, stdout = open_main_rofi_window(args.rofi_args, load_emojis(args.file))

    if returncode == 1:
        sys.exit()
    else:
        emojis = compile_chosen_emojis(stdout.splitlines(), args.skin_tone, args.rofi_args)

        if returncode == 0:
            if args.copy_only:
                copy_emojis_to_clipboard(emojis)
            else:
                insert_emojis(emojis, active_window, args.insert_with_clipboard)
        elif returncode == 10:
            copy_emojis_to_clipboard(emojis)
        elif returncode == 11:
            type_emojis(emojis, active_window)
        elif returncode == 12:
            copy_paste_emojis(emojis, active_window)


def parse_arguments() -> argparse.Namespace:
    parser = configargparse.ArgumentParser(
        description='Select, insert or copy Unicode emojis using rofi',
        default_config_files=[os.path.join(directory, 'rofimoji.rc') for directory in xdg.BaseDirectory.xdg_config_dirs]
    )
    parser.add_argument('--version', action='version', version='rofimoji 4.0.0-SNAPSHOT')
    parser.add_argument(
        '--insert-with-clipboard',
        '-p',
        dest='insert_with_clipboard',
        action='store_true',
        help='Do not type the emoji directly, but copy it to the clipboard, insert it from there '
             'and then restore the clipboard\'s original value '
    )
    parser.add_argument(
        '--copy-only',
        '-c',
        dest='copy_only',
        action='store_true',
        help='Only copy the emoji to the clipboard but do not insert it'
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
        '--emoji-file',
        '-f',
        dest='file',
        action='store',
        default=None,
        help='Read emojis from this file instead, one entry per line'
    )
    parser.add_argument(
        '--rofi-args',
        dest='rofi_args',
        action='store',
        default='',
        help='A string of arguments to give to rofi'
    )
    parsed_args = parser.parse_args()
    parsed_args.rofi_args = parsed_args.rofi_args.split()

    return parsed_args


def get_active_window() -> str:
    xdotool = Popen(args=['xdotool', 'getactivewindow'], stdout=PIPE)
    return xdotool.communicate()[0].decode("utf-8")[:-1]


def load_emojis(file_name: Union[str, None]) -> str:
    if file_name is not None:
        try:
            with open(file_name, "r") as file:
                return file.read()
        except IOError:
            return load_all_emojis()
    else:
        return load_all_emojis()


def load_all_emojis() -> str:
    characters = ""

    directory = os.path.join(os.path.dirname(__file__), "data")
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), "r") as file:
            characters = characters + file.read()
    return characters


def open_main_rofi_window(args: List[str], emojis: str) -> Tuple[int, bytes]:
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
    (stdout, _) = rofi.communicate(input=emojis.encode('UTF-8'))
    return rofi.returncode, stdout


def compile_chosen_emojis(chosen_emojis: List[bytes], skin_tone: str, rofi_args: List[str]) -> str:
    emojis = ""
    for line in chosen_emojis:
        emoji = line.decode('utf-8').split()[0]

        if emoji in skin_tone_selectable_emojis:
            emoji = select_skin_tone(emoji, skin_tone, rofi_args)

        emojis += emoji

    return emojis


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


def insert_emojis(emojis: str, active_window: str, insert_with_clipboard: bool = False) -> None:
    if insert_with_clipboard:
        copy_paste_emojis(emojis, active_window)
    else:
        type_emojis(emojis, active_window)


def copy_paste_emojis(emojis: str, active_window: str) -> None:
    old_clipboard_content = Popen(args=['xsel', '-o', '-b'], stdout=PIPE) \
        .communicate()[0]
    old_primary_content = Popen(args=['xsel', '-o', '-p'], stdout=PIPE) \
        .communicate()[0]

    Popen(args=['xsel', '-i', '-b'], stdin=PIPE) \
        .communicate(input=emojis.encode('utf-8'))
    Popen(args=['xsel', '-i', '-p'], stdin=PIPE) \
        .communicate(input=emojis.encode('utf-8'))

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


def type_emojis(emojis: str, active_window: str) -> None:
    Popen([
        'xdotool',
        'type',
        '--clearmodifiers',
        '--window',
        active_window,
        emojis
    ])


def copy_emojis_to_clipboard(emojis: str) -> None:
    xsel = Popen(
        [
            'xsel',
            '-i',
            '-b'
        ],
        stdin=PIPE
    )
    xsel.communicate(input=emojis.encode('utf-8'))


if __name__ == "__main__":
    main()
