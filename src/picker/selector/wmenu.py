from subprocess import run
from typing import Dict, List, Tuple, Union

from ..abstractionhelper import is_installed
from ..models import CANCEL, DEFAULT, Action, Shortcut
from .selector import Selector


class WMenu(Selector):
    @staticmethod
    def supported() -> bool:
        return is_installed("wmenu")

    @staticmethod
    def name() -> str:
        return "wmenu"

    def show_character_selection(
        self,
        characters: Dict[str, str],
        recent_characters: List[str],
        prompt: str,
        show_description: bool,
        use_icons: bool,
        keybindings: Dict[Action, str],
        additional_args: List[str],
    ) -> Tuple[Union[Action, DEFAULT, CANCEL], Union[List[str], Shortcut]]:
        parameters = ["wmenu", "-i", "-p", prompt, *additional_args]

        wmenu = run(
            parameters, input="\n".join(self.basic_format_characters(characters)), capture_output=True, encoding="utf-8"
        )
        return DEFAULT(), [self.extract_char_from_basic_output(line) for line in wmenu.stdout.splitlines()]

    def show_skin_tone_selection(
        self, tones_emojis: List[str], prompt: str, additional_args: List[str]
    ) -> Tuple[int, str]:
        wmenu = run(
            ["wmenu", "-p", prompt, *additional_args],
            input="\n".join(tones_emojis),
            capture_output=True,
            encoding="utf-8",
        )

        return wmenu.returncode, wmenu.stdout

    def show_action_menu(self, additional_args: List[str]) -> List[Action]:
        wmenu = run(
            [
                "wmenu",
                *additional_args,
            ],
            input="\n".join([it.value for it in Action if it != Action.MENU]),
            capture_output=True,
            encoding="utf-8",
        )

        return [Action(wmenu.stdout.strip())]
