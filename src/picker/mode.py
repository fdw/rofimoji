import argparse
import re
import sys
from dataclasses import dataclass
from enum import IntEnum, auto
from pickle import dump, load
from typing import Dict, List, Optional

from . import emoji_data
from .action import execute_action
from .argument_parsing import parse_arguments_flexible
from .clipboarder.clipboarder import Clipboarder
from .file_loader import read_characters_from_files
from .frecent import load_frecent_characters, save_frecent_characters
from .models import Action, CharacterEntry
from .paths import *
from .recent import load_recent_characters, save_recent_characters
from .typer.typer import Typer


class Step(IntEnum):
    SHOW_ALL = auto()
    SHORTCUTS = auto()
    SELECT_SKIN_TONE = auto()
    SELECT_ACTION = auto()
    EXECUTE = auto()
    DONE = auto()


@dataclass
class State:
    step: Step
    actions: List[Action]
    processed_characters: str
    unprocessed_characters: List[str]
    return_code: int
    __current_input: Optional[str] = None
    output: Optional[str] = None

    def save_to_cache(self) -> None:
        with cache_file_location.open("wb+") as file:
            dump(self, file)

    @staticmethod
    def load_from_cache(current_input: str, return_code: int) -> "State":
        if not cache_file_location.is_file():
            return State(
                step=Step.SHOW_ALL,
                actions=[],
                processed_characters="",
                unprocessed_characters=[],
                return_code=return_code,
                output=None,
            )

        with cache_file_location.open("rb+") as file:
            state = load(file)
            state.__current_input = current_input
            state.return_code = return_code
            state.output = None
            return state

    @staticmethod
    def remove_cache():
        try:
            cache_file_location.unlink()
        except FileNotFoundError:
            pass

    @property
    def has_input(self) -> bool:
        return self.__current_input is not None

    @property
    def current_input(self) -> str:
        temp = self.__current_input
        self.__current_input = None
        return temp

    def reset_current_input(self) -> None:
        self.__current_input = None


class ModeRofimoji:
    args: argparse.Namespace
    typer: Typer
    clipboarder: Clipboarder

    def mode(self) -> None:
        if os.environ.get("ROFI_RETV") == "0":
            State.remove_cache()

        chosen = sys.argv[-1]
        state = State.load_from_cache(chosen, int(os.environ.get("ROFI_RETV", "")))
        self.__parse_args()
        state.actions = self.args.actions

        if state.step == Step.SHOW_ALL:
            self.show_characters(state)
        if state.step == Step.SHORTCUTS:
            self.handle_shortcuts(state)
        if state.step == Step.SELECT_SKIN_TONE:
            self.select_skin_tone(state)
        if state.step == Step.SELECT_ACTION:
            self.choose_action(state)
        if state.step == Step.EXECUTE:
            self.execute_actions(state)
        if state.step == Step.DONE:
            state.remove_cache()
        else:
            state.save_to_cache()

        if state.output:
            print(state.output)

    def __parse_args(self) -> None:
        self.args = parse_arguments_flexible()
        self.typer = Typer.best_option(self.args.typer)
        self.clipboarder = Clipboarder.best_option(self.args.clipboarder)

    def show_characters(self, state: State) -> None:
        recent_characters = self.__format_recent_characters(
            load_recent_characters(self.args.max_recent, self.args.files)
        )

        state.output = "\x00markup-rows\x1ftrue\n"
        state.output += "\x00use-hot-keys\x1ftrue\n"
        if len(recent_characters) > 0:
            state.output += f"\x00message\x1f{recent_characters}"
        state.output += "\n".join(
            self.__format_characters(
                read_characters_from_files(
                    self.args.files, load_frecent_characters() if self.args.frecency else [], self.args.use_additional
                )
            )
        )
        state.output += "\n"

        state.step += 1

    def __format_recent_characters(self, recent_characters: List[str]) -> str:
        pairings = [f"\u200e{(index + 1) % 10}: {character}" for index, character in enumerate(recent_characters)]

        return " | ".join(pairings)

    def __format_characters(self, characters: List[CharacterEntry]) -> List[str]:
        if self.args.show_description:
            return [
                f"{character.character} {character.description}"
                for character in characters
                if character.description != ""
            ]
        else:
            return [
                f"{character.character}\0meta\x1f{character.description}"
                for character in characters
                if character.description != ""
            ]

    def handle_shortcuts(self, state: State) -> None:
        if 10 <= state.return_code <= 19:
            state.processed_characters = load_recent_characters(self.args.max_recent, self.args.files)[
                state.return_code - 10
            ]
            state.reset_current_input()
            state.step += 2
            return
        elif state.return_code:
            new_actions = self.__choose_action_from_return_code(state.return_code)
            if new_actions:
                state.actions = new_actions
            state.unprocessed_characters = state.current_input.splitlines()
            state.step += 1
            return
        else:
            return

    def __choose_action_from_return_code(self, return_code: int) -> List[Action]:
        if return_code == 20:
            return [Action.COPY]
        elif return_code == 21:
            return [Action.TYPE]
        elif return_code == 22:
            return [Action.CLIPBOARD]
        elif return_code == 23:
            return [Action.UNICODE]
        elif return_code == 24:
            return [Action.COPY_UNICODE]
        else:
            return []

    def __extract_char_from_input(self, line) -> str:
        return re.match(r"^(?:\u200e(?! ))?(?P<char>.[^ ]*)( .*|$)", line).group("char")

    def select_skin_tone(self, state: State) -> None:
        if state.has_input:
            state.processed_characters += self.__extract_char_from_input(state.current_input)
            state.unprocessed_characters.pop()

        for raw_character in state.unprocessed_characters:
            character = self.__extract_char_from_input(raw_character)
            save_frecent_characters(character)
            if character not in emoji_data.skin_tone_selectable_emojis:
                state.processed_characters += character
                state.unprocessed_characters = state.unprocessed_characters[1:]
            else:
                state.output = "\n".join(
                    character + modifier + " " + emoji_data.fitzpatrick_modifiers[modifier]
                    for modifier in emoji_data.fitzpatrick_modifiers
                )
                return

        state.step += 1

    def choose_action(self, state: State) -> None:
        if state.has_input:
            state.actions = [Action(state.current_input)]
            state.step += 1
            return

        if Action.MENU in state.actions:
            state.output = "\n".join([str(it) for it in Action if it != Action.MENU])
            return

        state.step += 1

    def execute_actions(self, state: State) -> Optional[str]:
        save_recent_characters(state.processed_characters, self.args.max_recent, self.args.files)
        execute_action(state.processed_characters, state.actions, "")
        state.step += 1
        return
