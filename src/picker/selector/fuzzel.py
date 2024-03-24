from subprocess import run
from typing import Dict, List, Tuple, Union

from ..abstractionhelper import is_installed, is_wayland
from ..models import CANCEL, DEFAULT, Action, CharacterEntry, Shortcut
from .selector import Selector


class Fuzzel(Selector):
    @staticmethod
    def supported() -> bool:
        return is_wayland() and is_installed("fuzzel")

    @staticmethod
    def name() -> str:
        return "fuzzel"

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
        parameters = ["fuzzel", "--dmenu", "--fuzzy-min-length", "1", "--index", "-p", prompt, *additional_args]

        fuzzel = run(
            parameters, input="\n".join(self.basic_format_characters(characters)), capture_output=True, encoding="utf-8"
        )
        return DEFAULT(), [characters[int(fuzzel.stdout.strip())].character]

    def show_skin_tone_selection(
        self, tones_emojis: List[str], prompt: str, additional_args: List[str]
    ) -> Tuple[int, str]:
        fuzzel = run(
            ["fuzzel", "--dmenu", "--fuzzy-min-length", "1", "-p", prompt, *additional_args],
            input="\n".join(tones_emojis),
            capture_output=True,
            encoding="utf-8",
        )

        return fuzzel.returncode, fuzzel.stdout

    def show_action_menu(self, additional_args: List[str]) -> List[Action]:
        fuzzel = run(
            [
                "fuzzel",
                "--dmenu",
                *additional_args,
            ],
            input="\n".join([it.value for it in Action if it != Action.MENU]),
            capture_output=True,
            encoding="utf-8",
        )

        return [Action(fuzzel.stdout.strip())]
