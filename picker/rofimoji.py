#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import fnmatch
import os
import shlex
import sys
from subprocess import run
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

invisible_codepoints = {'\u200c', '\u200d', '\ufe0f'}


def main() -> None:
    args = parse_arguments()
    active_window = get_active_window()

    returncode, stdout = open_main_rofi_window(
        args.rofi_args,
        read_character_files(args.files, args.codepoints),
        args.prompt,
        args.max_recent
    )

    if returncode == 1:
        sys.exit()
    else:
        if 10 <= returncode <= 19:
            default_handle_recent_character(returncode - 9, args, active_window)
        else:
            characters = process_chosen_characters(
                stdout.splitlines(),
                args.skin_tone,
                args.rofi_args
            )
            save_characters_to_recent_file(characters, args.max_recent)

            if returncode == 0:
                default_handle(characters, args, active_window)
            elif returncode == 20:
                copy_characters_to_clipboard(characters)
            elif returncode == 21:
                type_characters(characters, active_window)
            elif returncode == 22:
                copy_paste_characters(characters, active_window)


def parse_arguments() -> argparse.Namespace:
    parser = configargparse.ArgumentParser(
        description='Select, insert or copy Unicode characters using rofi.',
        default_config_files=[os.path.join(directory, 'rofimoji.rc') for directory in
                              BaseDirectory.xdg_config_dirs]
    )
    parser.add_argument('--version', action='version', version='rofimoji 4.2.0')
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
        '--prompt',
        '-r',
        dest='prompt',
        action='store',
        default='😀 ',
        help='Set rofimoj\'s  prompt'
    )
    parser.add_argument(
        '--rofi-args',
        dest='rofi_args',
        action='store',
        default='',
        help='A string of arguments to give to rofi'
    )
    parser.add_argument(
        '--max-recent',
        dest='max_recent',
        action='store',
        type=int,
        default=10,
        help='Show at most this number of recently used characters (cannot be larger than 10)'
    )
    parser.add_argument(
        '--codepoints',
        dest='codepoints',
        action='store_true',
        help='Show character codepoints next to the character'
    )

    parsed_args = parser.parse_args()
    parsed_args.rofi_args = shlex.split(parsed_args.rofi_args)

    return parsed_args


def get_active_window() -> str:
    return run(args=['xdotool', 'getactivewindow'], capture_output=True, encoding='utf-8').stdout[:-1]


def insert_codepoint(line):
    sep = line.find(' ', 1)
    if sep < 1: print(sep)
    char = line[:sep]
    desc = line[sep+1:]
    codepoint = [str(hex(ord(c)))[2:] for c in char if c not in invisible_codepoints]
    return ' '.join((char, '<small>'+'+'.join(codepoint)+'</small>', desc))


def read_character_files(file_names: List[str], show_codepoints : bool) -> str:
    entries = ''

    file_names = resolve_all_files(file_names)

    for file_name in file_names:
        entries = entries + load_from_file(file_name)
    
    if show_codepoints:
        entries = '\n'.join(map(insert_codepoint, entries.rstrip().split('\n')))

    return entries


def resolve_all_files(file_names):
    if len(file_names) == 1 and file_names[0] == 'all':
        file_names = [os.path.splitext(file)[0] for file in
                      os.listdir(os.path.join(os.path.dirname(__file__), "data"))
                      if fnmatch.fnmatch(file, "*.csv")]
    return file_names


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


def load_recent_characters(max: int) -> List[str]:
    try:
        with open(os.path.join(BaseDirectory.xdg_data_home, 'rofimoji', 'recent'), 'r') as file:
            return file.read().strip().split('\n')[:max]
    except FileNotFoundError:
        return []


def format_recent_characters(max: int) -> str:
    pairings = [f'{(index + 1) % 10}: {character}' for index, character in
                enumerate(load_recent_characters(max))]

    return ' | '.join(pairings)


def open_main_rofi_window(rofi_args: List[str], characters: str, prompt: str, max_recent: int) -> Tuple[int, str]:
    parameters = [
        'rofi',
        '-dmenu',
        '-markup-rows',
        '-i',
        '-multi-select',
        '-p',
        prompt,
        '-kb-custom-11',
        'Alt+c',
        '-kb-custom-12',
        'Alt+t',
        '-kb-custom-13',
        'Alt+p',
        *rofi_args
    ]

    recent_characters = format_recent_characters(max_recent)
    if len(recent_characters) > 0:
        parameters.extend(['-mesg', recent_characters])

    rofi = run(
        parameters,
        input=characters,
        capture_output=True,
        encoding='utf-8'
    )
    return rofi.returncode, rofi.stdout


def process_chosen_characters(
        chosen_characters: List[str],
        skin_tone: str,
        rofi_args: List[str]
) -> str:
    result = ""
    for line in chosen_characters:
        character = line.split(" ")[0]

        characters_with_skin_tone = ''
        for element in character:
            if element in skin_tone_selectable_emojis:
                characters_with_skin_tone += select_skin_tone(element, skin_tone, rofi_args)
            else:
                characters_with_skin_tone += element

        result += characters_with_skin_tone

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

        rofi_skin = run(
            [
                'rofi',
                '-dmenu',
                '-i',
                '-p',
                selected_emoji + '   ',
                *rofi_args
            ],
            input=modified_emojis,
            capture_output=True,
            encoding='utf-8'
        )

        if rofi_skin.returncode == 1:
            return ''

        return rofi_skin.stdout.split(' ')[0]


def save_characters_to_recent_file(characters: str, max_recent_from_conf: int):
    old_file_name = os.path.join(BaseDirectory.xdg_data_home, 'rofimoji', 'recent')
    new_file_name = os.path.join(BaseDirectory.xdg_data_home, 'rofimoji', 'recent_temp')

    max_recent = min(max_recent_from_conf, 10)

    os.makedirs(os.path.dirname(new_file_name), exist_ok=True)
    with open(new_file_name, 'w+') as new_file:
        new_file.write(characters + '\n')

        try:
            with open(old_file_name, 'r') as old_file:
                index = 0
                for line in old_file:
                    if characters == line.strip():
                        continue
                    if index == max_recent - 1:
                        break
                    new_file.write(line)
                    index = index + 1

            os.remove(old_file_name)
        except FileNotFoundError:
            pass

    os.rename(new_file_name, old_file_name)


def append_to_favorites_file(characters: str):
    file_name = os.path.join(BaseDirectory.xdg_data_home, 'rofimoji', 'favorites')

    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    with open(file_name, 'a+') as file:
        file.write(characters + '\n')


def default_handle(characters: str, args: argparse.Namespace, active_window: str):
    if args.copy_only:
        copy_characters_to_clipboard(characters)
    elif args.insert_with_clipboard:
        copy_paste_characters(characters, active_window)
    else:
        type_characters(characters, active_window)


def default_handle_recent_character(position: int, args: argparse.Namespace, active_window: str):
    recent_characters = load_recent_characters(position)

    default_handle(recent_characters[position - 1].strip(), args, active_window)


def copy_paste_characters(characters: str, active_window: str) -> None:
    old_clipboard_content = run(args=['xsel', '-o', '-b'], capture_output=True).stdout
    old_primary_content = run(args=['xsel', '-o', '-p'], capture_output=True).stdout

    run(args=['xsel', '-i', '-b'], input=characters, encoding='utf-8')
    run(args=['xsel', '-i', '-p'], input=characters, encoding='utf-8')

    run([
        'xdotool',
        'windowfocus',
        '--sync',
        active_window,
        'key',
        '--clearmodifiers',
        'Shift+Insert',
        'sleep',
        '0.05',
    ])

    run(args=['xsel', '-i', '-b'], input=old_clipboard_content)
    run(args=['xsel', '-i', '-p'], input=old_primary_content)


def type_characters(characters: str, active_window: str) -> None:
    run([
        'xdotool',
        'type',
        '--window',
        active_window,
        characters
    ])


def copy_characters_to_clipboard(characters: str) -> None:
    run([
        'xsel',
        '-i',
        '-b'
    ],
        input=characters,
        encoding='utf-8'
    )


if __name__ == "__main__":
    main()
