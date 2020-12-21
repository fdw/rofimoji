#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import enum
import re
import shlex
import sys
from subprocess import run
from typing import List, Tuple

import configargparse

from picker.clipboarder import Clipboarder
from picker.typer import Typer
from picker.paths import *


class Rofimoji:
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

    class Action(enum.Enum):
        TYPE = 'type'
        COPY = 'copy'
        CLIPBOARD = 'clipboard'
        UNICODE = 'unicode'
        COPY_UNICODE = 'copy-unicode'

    fitzpatrick_modifiers_reversed = {" ".join(name.split()[:-1]): modifier for modifier, name in
                                      fitzpatrick_modifiers.items() if name != "neutral"}

    def __init__(self) -> None:
        self.args = self.parse_arguments()
        self.typer = Typer.best_option(self.args.typer)
        self.clipboarder = Clipboarder.best_option(self.args.clipboarder)
        self.active_window = self.typer.get_active_window()

        returncode, stdout = self.open_main_rofi_window()

        if returncode == 1:
            sys.exit()
        else:
            if 10 <= returncode <= 19:
                characters = self.load_recent_characters(self.args.max_recent)[returncode - 10].strip()
            else:
                self.choose_action_from_return_code(returncode)
                characters = self.process_chosen_characters(stdout.splitlines())

            self.execute_action(characters)

    def parse_arguments(self) -> argparse.Namespace:
        parser = configargparse.ArgumentParser(
            description='Select, insert or copy Unicode characters using rofi.',
            default_config_files=config_file_locations
        )
        parser.add_argument('--version', action='version', version='rofimoji 5.0.0-SNAPSHOT')
        parser.add_argument(
            '--action',
            '-a',
            dest='action',
            action='store',
            choices=[action.value for action in self.Action],
            default=self.Action.TYPE.value,
            help='How to insert the chosen characters'
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
            '--clipboarder',
            dest='clipboarder',
            action='store',
            type=str,
            choices=['xsel', 'xclip', 'wl-copy'],
            default=None,
            help='Choose the application to access the clipboard with'
        )
        parser.add_argument(
            '--typer',
            dest='typer',
            action='store',
            type=str,
            choices=['xdotool', 'wtype'],
            default=None,
            help='Choose the application to type with'
        )

        parsed_args = parser.parse_args()
        parsed_args.rofi_args = shlex.split(parsed_args.rofi_args)
        parsed_args.action = next(action for action in self.Action if action.value == parsed_args.action)

        return parsed_args

    def choose_action_from_return_code(self, return_code: int):
        if return_code == 20:
            self.args.action = self.Action.COPY
        elif return_code == 21:
            self.args.action = self.Action.TYPE
        elif return_code == 22:
            self.args.action = self.Action.CLIPBOARD
        elif return_code == 23:
            self.args.action = self.Action.UNICODE
        elif return_code == 24:
            self.args.action = self.Action.COPY_UNICODE

    def read_character_files(self) -> str:
        return ''.join(self.load_from_file(file_name) for file_name in self.resolve_all_files())

    def resolve_all_files(self) -> List[str]:
        file_names = self.args.files

        if len(file_names) == 1 and file_names[0] == 'all':
            file_names = [file.stem for file in (Path(__file__).parent / "data").glob("*.csv")]
        return file_names

    def load_from_file(self, file_name: str) -> str:
        provided_file = Path(__file__).parent / "data" / f"{file_name}.csv"
        if Path(file_name).is_file():
            actual_file_name = Path(file_name)
        elif provided_file.is_file():
            actual_file_name = provided_file
        else:
            raise FileNotFoundError(f"Couldn't find file {file_name!r}")

        return actual_file_name.read_text()

    def load_recent_characters(self, max: int) -> List[str]:
        try:
            return recents_file_location.read_text().strip().split('\n')[:max]
        except FileNotFoundError:
            return []

    def format_recent_characters(self) -> str:
        pairings = [f'{(index + 1) % 10}: {character}' for index, character in
                    enumerate(self.load_recent_characters(self.args.max_recent))]

        return ' | '.join(pairings)

    def open_main_rofi_window(self) -> Tuple[int, str]:
        rofi_args = self.args.rofi_args
        characters = self.read_character_files()
        prompt = self.args.prompt

        parameters = [
            'rofi',
            '-dmenu',
            '-markup-rows',
            '-sort',
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
            '-kb-custom-14',
            'Alt+u',
            '-kb-custom-15',
            'Alt+i',
            *rofi_args
        ]

        recent_characters = self.format_recent_characters()
        if recent_characters:
            parameters.extend(['-mesg', recent_characters])

        rofi = run(
            parameters,
            input=characters,
            capture_output=True,
            encoding='utf-8'
        )
        return rofi.returncode, rofi.stdout

    def process_chosen_characters(self, chosen_characters: List[str]) -> str:
        processed_characters = ''.join(
            self.add_skin_tone(re.match(r'^[\u200e\u200f]?(?P<char>.)\s', line).group('char'))
            for line in chosen_characters
        )
        self.save_characters_to_recent_file(processed_characters)

        return processed_characters

    def add_skin_tone(self, character: str) -> str:
        characters_with_skin_tone = []

        for element in character:
            if element in self.skin_tone_selectable_emojis:
                characters_with_skin_tone.append(self.select_skin_tone(element))
            else:
                characters_with_skin_tone.append(element)

        return ''.join(characters_with_skin_tone)

    def select_skin_tone(self, selected_emoji: chr) -> str:
        skin_tone = self.args.skin_tone

        if skin_tone == 'neutral':
            return selected_emoji
        elif skin_tone != 'ask':
            return selected_emoji + self.fitzpatrick_modifiers_reversed[skin_tone]
        else:
            modified_emojis = '\n'.join(
                selected_emoji + modifier + " " + self.fitzpatrick_modifiers[modifier]
                for modifier in self.fitzpatrick_modifiers
            )

            rofi_skin = run(
                [
                    'rofi',
                    '-dmenu',
                    '-i',
                    '-p',
                    selected_emoji + '   ',
                    *self.args.rofi_args
                ],
                input=modified_emojis,
                capture_output=True,
                encoding='utf-8'
            )

            if rofi_skin.returncode == 1:
                return ''

            return rofi_skin.stdout.split(' ')[0]

    def get_codepoints(self, char: str) -> str:
        return '-'.join(f'{ord(c):x}' for c in char)

    def save_characters_to_recent_file(self, characters: str) -> None:
        max_recent_from_conf = self.args.max_recent

        old_file_name = recents_file_location
        new_file_name = old_file_name.with_name('recent_temp')

        max_recent = min(max_recent_from_conf, 10)

        new_file_name.parent.mkdir(parents=True, exist_ok=True)
        with new_file_name.open('w+') as new_file:
            new_file.write(characters + '\n')

            try:
                with old_file_name.open('r') as old_file:
                    index = 0
                    for line in old_file:
                        if characters != line.strip():
                            if index == max_recent - 1:
                                break
                            new_file.write(line)
                            index += 1

                old_file_name.unlink()
            except FileNotFoundError:
                pass

        new_file_name.rename(old_file_name)

    def append_to_favorites_file(self, characters: str) -> None:
        favorites_file_location.parent.mkdir(parents=True, exist_ok=True)
        with favorites_file_location.open('a+') as file:
            file.write(characters + '\n')

    def execute_action(self, characters: str) -> None:
        if self.args.action == self.Action.TYPE:
            self.typer.type_characters(characters, self.active_window)
        elif self.args.action == self.Action.COPY:
            self.clipboarder.copy_characters_to_clipboard(characters)
        elif self.args.action == self.Action.CLIPBOARD:
            self.clipboarder.copy_paste_characters(characters, self.active_window, self.typer)
        elif self.args.action == self.Action.UNICODE:
            self.typer.type_characters(self.get_codepoints(characters), self.active_window)
        elif self.args.action == self.Action.COPY_UNICODE:
            self.clipboarder.copy_characters_to_clipboard(self.get_codepoints(characters))


def main():
    Rofimoji()


if __name__ == "__main__":
    main()
