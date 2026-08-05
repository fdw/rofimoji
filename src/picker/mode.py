import argparse
import json
import os
import re
import sys
from dataclasses import asdict, dataclass
from enum import IntEnum, auto

from . import emoji_data
from .action import execute_action
from .argument_parsing import parse_arguments_flexible
from .clipboarder.clipboarder import Clipboarder
from .emoji_data import fitzpatrick_modifiers, fitzpatrick_modifiers_reversed, skin_tone_selectable_emojis
from .file_loader import read_characters_from_files
from .frecent import load_frecent_characters, save_frecent_characters
from .models import Action, CharacterEntry
from .paths import cache_file_location
from .recent import load_recent_characters, save_recent_characters
from .typer.typer import Typer


class Step(IntEnum):
    SHOW_ALL = auto()
    SHORTCUTS = auto()
    SELECT_SKIN_TONE = auto()
    SELECT_ACTION = auto()
    EXECUTE = auto()
    DONE = auto()


@dataclass(slots=True)
class State:
    step: Step
    actions: list[Action]
    processed_characters: str
    unprocessed_characters: list[str]
    return_code: int
    __current_input: str | None = None
    output: str | None = None

    def __post_init__(self):
        if isinstance(self.step, int) and not isinstance(self.step, Step):
            self.step = Step(self.step)
        if self.actions and isinstance(self.actions[0], str):
            self.actions = [Action(a) for a in self.actions]

    def save_to_cache(self) -> None:
        with cache_file_location.open("w+") as file:
            json.dump(asdict(self), file, default=str)

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

        with cache_file_location.open("r") as file:
            state = State(**json.load(file))
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

        state = State.load_from_cache(os.environ.get("ROFI_INFO", sys.argv[-1]), int(os.environ.get("ROFI_RETV", "")))
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
            state.output += f"\x00message\x1f{recent_characters}\n"
        state.output += "\n".join(
            self.__format_characters(
                read_characters_from_files(
                    self.args.files, load_frecent_characters() if self.args.frecency else [], self.args.use_additional
                )
            )
        )
        state.output += "\n"

        state.step += 1

    def __format_recent_characters(self, recent_characters: list[CharacterEntry]) -> str:
        pairings = [
            f"\u200e{(index + 1) % 10}: {character.character_html}" for index, character in enumerate(recent_characters)
        ]

        return " | ".join(pairings)

    def __format_characters(self, characters: list[CharacterEntry]) -> list[str]:
        if self.args.use_icons and not self.args.show_description:
            return [
                f" \0meta\x1f{entry.description_html}\x1ficon\x1f<span>{entry.character_html}</span>\x1finfo\x1f{entry.character}"
                for entry in characters
            ]
        elif self.args.use_icons and self.args.show_description:
            return [
                f"{entry.description_html}\0icon\x1f<span>{entry.character_html}</span>\x1finfo\x1f{entry.character}"
                for entry in characters
            ]
        elif not self.args.use_icons and self.args.show_description:
            return [f"{entry.character_html} {entry.description_html}" for entry in characters]
        else:
            return [f"{entry.character_html}\0meta\x1f{entry.description_html}" for entry in characters]

    def handle_shortcuts(self, state: State) -> None:
        if 10 <= state.return_code <= 19:
            state.processed_characters = load_recent_characters(self.args.max_recent, self.args.files)[
                state.return_code - 10
            ].character
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

    def __choose_action_from_return_code(self, return_code: int) -> list[Action]:
        match return_code:
            case 20:
                return [Action.COPY]
            case 21:
                return [Action.TYPE]
            case 22:
                return [Action.CLIPBOARD]
            case 23:
                return [Action.TYPE_NUMERICAL]
            case 24:
                return [Action.UNICODE]
            case 25:
                return [Action.COPY_UNICODE]
            case _:
                return []

    def __extract_char_from_input(self, line) -> str:
        return re.match(r"^(?:\u200e(?! ))?(?P<char>.[^ ]*)( .*|$)", line).group("char")

    def select_skin_tone(self, state: State) -> None:
        if state.has_input:
            state.processed_characters += self.__extract_char_from_input(state.current_input)
            state.unprocessed_characters.pop(0)

        while state.unprocessed_characters:
            character = self.__extract_char_from_input(state.unprocessed_characters[0])
            save_frecent_characters(character)

            if character in emoji_data.skin_tone_selectable_emojis and self.args.skin_tone == "ask":
                if self.args.use_icons and not self.args.show_description:
                    state.output = "\n".join(
                        f" \0meta\x1f{description}\x1ficon\x1f<span>{character}{modifier}</span>\x1finfo\x1f{character}{modifier}"
                        for (modifier, description) in fitzpatrick_modifiers.items()
                    )
                elif self.args.use_icons and self.args.show_description:
                    state.output = "\n".join(
                        f"{description}\0icon\x1f<span>{character}{modifier}</span>\x1finfo\x1f{character}{modifier}"
                        for (modifier, description) in fitzpatrick_modifiers.items()
                    )
                elif not self.args.use_icons and self.args.show_description:
                    state.output = "\n".join(
                        f"{character}{modifier} {description}"
                        for (modifier, description) in fitzpatrick_modifiers.items()
                    )
                else:
                    state.output = "\n".join(
                        f"{character}{modifier}\0meta\x1f{description}"
                        for (modifier, description) in fitzpatrick_modifiers.items()
                    )
                return

            if character not in skin_tone_selectable_emojis or self.args.skin_tone == "neutral":
                state.processed_characters += character
            else:
                state.processed_characters += character + fitzpatrick_modifiers_reversed[self.args.skin_tone]
            state.unprocessed_characters.pop(0)

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

    def execute_actions(self, state: State) -> str | None:
        save_recent_characters(state.processed_characters, self.args.max_recent, self.args.files)
        execute_action(state.processed_characters, state.actions, "")
        state.step += 1
        return
