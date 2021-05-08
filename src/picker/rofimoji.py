#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import re
import shlex
import sys
from typing import List, Tuple

import configargparse

try:
    from picker.action import Action
    from picker.clipboarder import Clipboarder
    from picker.typer import Typer
    from picker.selector import Selector
    from picker.paths import *
except ModuleNotFoundError:
    from action import Action
    from clipboarder import Clipboarder
    from typer import Typer
    from selector import Selector
    from paths import *

__version__ = '5.2.0'


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
        self.selector = Selector.best_option(self.args.selector)
        self.typer = Typer.best_option(self.args.typer)
        self.clipboarder = Clipboarder.best_option(self.args.clipboarder)
        self.active_window = self.typer.get_active_window()

    def parse_arguments(self) -> argparse.Namespace:
        parser = configargparse.ArgumentParser(
            description='Select, insert or copy Unicode characters using rofi.',
            default_config_files=config_file_locations
        )
        parser.add_argument('--version', action='version', version='rofimoji ' + __version__)
        parser.add_argument(
            '--action',
            '-a',
            dest='action',
            action='store',
            choices=[action.value for action in Action],
            default=Action.TYPE.value,
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
            '--selector',
            dest='selector',
            action='store',
            type=str,
            choices=['rofi', 'wofi'],
            default=None,
            help='Choose the application to select the characters with'
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
        parser.add_argument(
            '--keybinding-copy',
            dest='keybinding_copy',
            action='store',
            type=str,
            default='Alt+c',
            help='Choose the keyboard shortcut to copy the character to the clipboard'
        )
        parser.add_argument(
            '--keybinding-type',
            dest='keybinding_type',
            action='store',
            type=str,
            default='Alt+t',
            help='Choose the keyboard shortcut to directly type the character'
        )
        parser.add_argument(
            '--keybinding-clipboard',
            dest='keybinding_clipboard',
            action='store',
            type=str,
            default='Alt+p',
            help='Choose the keyboard shortcut to insert the character via the clipboard'
        )
        parser.add_argument(
            '--keybinding-unicode',
            dest='keybinding_unicode',
            action='store',
            type=str,
            default='Alt+u',
            help='Choose the keyboard shortcut to directly type the character\'s unicode codepoint'
        )
        parser.add_argument(
            '--keybinding-copy-unicode',
            dest='keybinding_copy_unicode',
            action='store',
            type=str,
            default='Alt+i',
            help='Choose the keyboard shortcut to copy the character\'s unicode codepoint to the clipboard'
        )

        parsed_args = parser.parse_args()
        parsed_args.rofi_args = shlex.split(parsed_args.rofi_args)
        parsed_args.action = next(action for action in Action if action.value == parsed_args.action)
        parsed_args.keybindings = {
            Action.TYPE: parsed_args.keybinding_type,
            Action.COPY: parsed_args.keybinding_copy,
            Action.CLIPBOARD: parsed_args.keybinding_clipboard,
            Action.UNICODE: parsed_args.keybinding_unicode,
            Action.COPY_UNICODE: parsed_args.keybinding_copy_unicode,
        }

        return parsed_args

    def standalone(self) -> None:
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

    def mode_show_characters(self) -> None:
        recent_characters = self.format_recent_characters()

        print("\x00markup-rows\x1ftrue\n")
        if len(recent_characters) > 0:
            print(f"\x00message\x1f{recent_characters}")
        print(self.read_character_files())

    def mode_act_on_selection(self, chosen_character: str, returncode: int) -> None:
        if 10 <= returncode <= 19:
            characters = self.load_recent_characters(self.args.max_recent)[returncode - 10].strip()
            self.execute_action(characters)
        else:
            self.choose_action_from_return_code(returncode)
            self.save_selection_to_cache(re.match(r'^(?:\u200e(?! ))?(?P<char>.[^ ]*) .*', chosen_character).group('char'), '')
            self.mode_select_skin_tone('')

    def mode_select_skin_tone(self, processed_character: str) -> None:
        (characters, processed_characters) = self.load_selection_from_cache()
        processed_characters += processed_character.split(' ')[0]

        for character in characters:
            if character not in self.skin_tone_selectable_emojis:
                processed_characters += character
                characters = characters[1:]
            else:
                self.save_selection_to_cache(characters[1:], processed_characters)
                print('\n'.join(
                    character + modifier + " " + self.fitzpatrick_modifiers[modifier]
                    for modifier in self.fitzpatrick_modifiers
                ))
                return

        cache_file_location.unlink()
        self.save_characters_to_recent_file(processed_characters)
        self.execute_action(processed_characters)

    def choose_action_from_return_code(self, return_code: int):
        if return_code == 20:
            self.args.action = Action.COPY
        elif return_code == 21:
            self.args.action = Action.TYPE
        elif return_code == 22:
            self.args.action = Action.CLIPBOARD
        elif return_code == 23:
            self.args.action = Action.UNICODE
        elif return_code == 24:
            self.args.action = Action.COPY_UNICODE

    def read_character_files(self) -> str:
        return ''.join(self.load_from_file(file_name) for file_name in self.resolve_all_files())

    def resolve_all_files(self) -> List[str]:
        file_names = self.args.files

        if len(file_names) == 1 and file_names[0] == 'all':
            file_names = [file.stem for file in (Path(__file__).parent / "data").glob("*.csv")]
        return file_names

    def load_from_file(self, file_name: str) -> str:
        provided_file = Path(__file__).parent / "data" / f"{file_name}.csv"
        if Path(file_name).expanduser().is_file():
            actual_file_name = Path(file_name).expanduser()
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
        pairings = [f'\u200e{(index + 1) % 10}: {character}' for index, character in
                    enumerate(self.load_recent_characters(self.args.max_recent))]

        return ' | '.join(pairings)

    def open_main_rofi_window(self) -> Tuple[int, str]:
        return self.selector.show_character_selection(
            self.read_character_files(),
            self.format_recent_characters(),
            self.args.prompt,
            self.args.keybindings,
            self.args.rofi_args
        )

    def process_chosen_characters(self, chosen_characters: List[str]) -> str:
        processed_characters = ''.join(
            self.add_skin_tone(re.match(r'^(?:\u200e(?! ))?(?P<char>.[^ ]*) .*', character).group('char'))
            for character in chosen_characters
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

            returncode, skin_tone = self.selector.show_skin_tone_selection(
                modified_emojis,
                selected_emoji + '   ',
                self.args.rofi_args
            )

            if returncode == 1:
                return ''

            return skin_tone.split(' ')[0]

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
        if self.args.action == Action.TYPE:
            self.typer.type_characters(characters, self.active_window)
        elif self.args.action == Action.COPY:
            self.clipboarder.copy_characters_to_clipboard(characters)
        elif self.args.action == Action.CLIPBOARD:
            self.clipboarder.copy_paste_characters(characters, self.active_window, self.typer)
        elif self.args.action == Action.UNICODE:
            self.typer.type_characters(self.get_codepoints(characters), self.active_window)
        elif self.args.action == Action.COPY_UNICODE:
            self.clipboarder.copy_characters_to_clipboard(self.get_codepoints(characters))
        elif self.args.action == Action.STDOUT:
            print(characters)

    def save_selection_to_cache(self, characters: str, processed_characters: str) -> None:
        with cache_file_location.open('w+') as file:
            file.write(f'{self.args.action.value}\n{characters}\n{processed_characters}')

    def load_selection_from_cache(self) -> Tuple[str, str]:
        cache = cache_file_location.read_text().split('\n')
        self.args.action = next(action for action in Action if action.value == cache[0].strip())
        return cache[1], cache[2]


def main():
    return_value = os.environ.get('ROFI_RETV')

    if return_value is None:
        Rofimoji().standalone()
    elif return_value == "0":
        Rofimoji().mode_show_characters()
    elif not cache_file_location.is_file():
        chosen = sys.argv[-1]
        del sys.argv[-1]
        Rofimoji().mode_act_on_selection(chosen, int(return_value))
    else:
        chosen = sys.argv[-1]
        del sys.argv[-1]
        Rofimoji().mode_select_skin_tone(chosen)


if __name__ == "__main__":
    main()
