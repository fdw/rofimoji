from subprocess import run
from typing import Dict, List, Tuple, Union

from ..abstractionhelper import is_installed, is_macos
from ..models import CANCEL, DEFAULT, Action, CharacterEntry, Shortcut
from .selector import Selector


class Choose(Selector):
    @staticmethod
    def supported() -> bool:
        return is_macos() and is_installed("choose")

    @staticmethod
    def name() -> str:
        return "choose"

    def show_character_selection(
        self,
        characters: List[CharacterEntry],
        recent_characters: List[str],
        prompt: str,
        show_description: bool,
        use_icons: bool,
        keybindings: Dict[Action, str],
        additional_args: List[str],
    ) -> Tuple[Union[Action, DEFAULT, CANCEL], Union[List[str], Shortcut]]:
        parameters = ["choose", "-p", prompt, *additional_args]

        choose = run(
            parameters, input="\n".join(self.basic_format_characters(characters)), capture_output=True, encoding="utf-8"
        )
        return DEFAULT(), [self.extract_char_from_basic_output(line) for line in choose.stdout.splitlines()]

    def show_skin_tone_selection(
        self, tones_emojis: List[str], prompt: str, additional_args: List[str]
    ) -> Tuple[int, str]:
        choose = run(
            ["choose", "-p", prompt, *additional_args],
            input="\n".join(tones_emojis),
            capture_output=True,
            encoding="utf-8",
        )

        return choose.returncode, choose.stdout

    def show_action_menu(self, additional_args: List[str]) -> List[Action]:
        choose = run(
            [
                "choose",
                *additional_args,
            ],
            input="\n".join([it.value for it in Action if it != Action.MENU]),
            capture_output=True,
            encoding="utf-8",
        )

        return [Action(choose.stdout.strip())]
