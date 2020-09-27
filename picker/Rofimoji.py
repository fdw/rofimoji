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

from picker.Clipboarder import Clipboarder
from picker.Typer import Typer


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
                self.default_handle_recent_character(returncode - 9)
            else:
                characters = self.process_chosen_characters(
                    stdout.splitlines()
                )
                self.save_characters_to_recent_file(characters)

                if returncode == 0:
                    self.default_handle(characters)
                elif returncode == 20:
                    self.clipboarder.copy_characters_to_clipboard(characters)
                elif returncode == 21:
                    self.typer.type_characters(characters, self.active_window)
                elif returncode == 22:
                    self.clipboarder.copy_paste_characters(characters, self.active_window, self.typer)
                elif returncode == 23:
                    self.default_handle(self.get_codepoints(characters))
                elif returncode == 24:
                    self.clipboarder.copy_characters_to_clipboard(self.get_codepoints(characters))

    def parse_arguments(self) -> argparse.Namespace:
        parser = configargparse.ArgumentParser(
            description='Select, insert or copy Unicode characters using rofi.',
            default_config_files=[os.path.join(directory, 'rofimoji.rc') for directory in
                                  BaseDirectory.xdg_config_dirs]
        )
        parser.add_argument('--version', action='version', version='rofimoji 4.3.0')
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
            '--clipboarder',
            dest='clipboarder',
            action='store',
            type=str,
            default=None,
            help='Choose the application to access the clipboard with'
        )
        parser.add_argument(
            '--typer',
            dest='typer',
            action='store',
            type=str,
            default=None,
            help='Choose the application to type with'
        )

        parsed_args = parser.parse_args()
        parsed_args.rofi_args = shlex.split(parsed_args.rofi_args)

        return parsed_args

    def read_character_files(self) -> str:
        entries = ''

        file_names = self.resolve_all_files()

        for file_name in file_names:
            entries = entries + self.load_from_file(file_name)

        return entries

    def resolve_all_files(self):
        file_names = self.args.files

        if len(file_names) == 1 and file_names[0] == 'all':
            file_names = [os.path.splitext(file)[0] for file in
                          os.listdir(os.path.join(os.path.dirname(__file__), "data"))
                          if fnmatch.fnmatch(file, "*.csv")]
        return file_names

    def load_from_file(self, file_name: str) -> str:
        provided_file = os.path.join(os.path.dirname(__file__), "data", file_name + '.csv')
        if os.path.isfile(file_name):
            actual_file_name = file_name
        elif os.path.isfile(provided_file):
            actual_file_name = provided_file
        else:
            raise FileNotFoundError(f"Couldn't find file {file_name}")

        with open(actual_file_name, "r") as file:
            return file.read()

    def load_all_characters(self) -> str:
        characters = ""

        directory = os.path.join(os.path.dirname(__file__), "data")
        for filename in os.listdir(directory):
            with open(os.path.join(directory, filename), "r") as file:
                characters = characters + file.read()
        return characters

    def load_recent_characters(self, max: int) -> List[str]:
        try:
            with open(os.path.join(BaseDirectory.xdg_data_home, 'rofimoji', 'recent'), 'r') as file:
                return file.read().strip().split('\n')[:max]
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
            self,
            chosen_characters: List[str]
    ) -> str:

        result = ""
        for line in chosen_characters:
            character = line.split(" ")[0]

            characters_with_skin_tone = ''
            for element in character:
                if element in self.skin_tone_selectable_emojis:
                    characters_with_skin_tone += self.select_skin_tone(element)
                else:
                    characters_with_skin_tone += element

            result += characters_with_skin_tone

        return result

    def select_skin_tone(self, selected_emoji: chr) -> str:
        skin_tone = self.args.skin_tone

        if skin_tone == 'neutral':
            return selected_emoji
        elif skin_tone != 'ask':
            return selected_emoji + self.fitzpatrick_modifiers_reversed[skin_tone]
        else:
            modified_emojis = '\n'.join(map(
                lambda modifier: selected_emoji + modifier + " " + self.fitzpatrick_modifiers[
                    modifier],
                self.fitzpatrick_modifiers.keys()
            ))

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
        return '-'.join([str(hex(ord(c)))[2:] for c in char])

    def save_characters_to_recent_file(self, characters: str):
        max_recent_from_conf = self.args.max_recent

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

    def append_to_favorites_file(self, characters: str):
        file_name = os.path.join(BaseDirectory.xdg_data_home, 'rofimoji', 'favorites')

        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        with open(file_name, 'a+') as file:
            file.write(characters + '\n')

    def default_handle(self, characters: str):
        if self.args.copy_only:
            self.clipboarder.copy_characters_to_clipboard(characters)
        elif self.args.insert_with_clipboard:
            self.clipboarder.copy_paste_characters(characters, self.active_window, self.typer)
        else:
            self.typer.type_characters(characters, self.active_window)

    def default_handle_recent_character(self, position: int):
        recent_characters = self.load_recent_characters(position)

        self.default_handle(recent_characters[position - 1].strip())


def main():
    Rofimoji()


if __name__ == "__main__":
    main()
