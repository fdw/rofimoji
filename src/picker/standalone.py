import sys
from typing import List, Tuple, Union

from . import emoji_data
from .action import execute_action
from .argument_parsing import parse_arguments_strict
from .clipboarder.clipboarder import Clipboarder
from .file_loader import read_characters_from_files
from .frecent import load_frecent_characters, save_frecent_characters
from .models import CANCEL, DEFAULT, Action, Shortcut
from .recent import load_recent_characters, save_recent_characters
from .selector.selector import Selector
from .typer.typer import Typer


class StandaloneRofimoji:
    def __init__(self) -> None:
        self.args = parse_arguments_strict()
        self.selector = Selector.best_option(self.args.selector)
        self.typer = Typer.best_option(self.args.typer)
        self.clipboarder = Clipboarder.best_option(self.args.clipboarder)
        self.active_window = self.typer.get_active_window()

    def standalone(self) -> None:
        action, value = self.__open_main_selector_window()

        if action == CANCEL():
            sys.exit()
        elif action != DEFAULT():
            self.args.actions = [action]

        if isinstance(value, Shortcut):
            characters = load_recent_characters(self.args.max_recent, self.args.files)[value.index]
        else:
            characters = self.__process_chosen_characters(value)

        if Action.MENU in self.args.actions:
            self.args.actions = self.selector.show_action_menu(self.args.selector_args)

        save_recent_characters(characters, self.args.max_recent, self.args.files)
        execute_action(characters, self.args.actions, self.active_window, self.args.typer, self.args.clipboarder)

    def __open_main_selector_window(self) -> Tuple[Union[Action, DEFAULT, CANCEL], Union[List[str], Shortcut]]:
        return self.selector.show_character_selection(
            read_characters_from_files(
                self.args.files, load_frecent_characters() if self.args.frecency else [], self.args.use_additional
            ),
            load_recent_characters(self.args.max_recent, self.args.files),
            self.args.prompt,
            self.args.show_description,
            self.args.use_icons,
            self.args.keybindings,
            self.args.selector_args,
        )

    def __process_chosen_characters(self, characters: List[str]) -> str:
        characters_with_skin_tones = []
        for character in characters:
            save_frecent_characters(character)
            characters_with_skin_tones.append(self.__add_skin_tone_to_character(character))

        return "".join(characters_with_skin_tones)

    def __add_skin_tone_to_character(self, character: str) -> str:
        characters_with_skin_tone = []

        for element in character:
            if element in emoji_data.skin_tone_selectable_emojis:
                characters_with_skin_tone.append(self.__select_skin_tone(element))
            else:
                characters_with_skin_tone.append(element)

        return "".join(characters_with_skin_tone)

    def __select_skin_tone(self, selected_emoji: str) -> str:
        skin_tone = self.args.skin_tone

        if skin_tone == "neutral":
            return selected_emoji
        elif skin_tone != "ask":
            return selected_emoji + emoji_data.fitzpatrick_modifiers_reversed[skin_tone]
        else:
            modified_emojis = [
                selected_emoji + modifier + " " + emoji_data.fitzpatrick_modifiers[modifier]
                for modifier in emoji_data.fitzpatrick_modifiers
            ]

            return_code, skin_tone = self.selector.show_skin_tone_selection(
                modified_emojis, selected_emoji + "   ", self.args.selector_args
            )

            if return_code == 1:
                return ""

            return skin_tone.split(" ")[0]
