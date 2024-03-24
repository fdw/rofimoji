from subprocess import run
from typing import Dict, List, Tuple, Union

from ..abstractionhelper import is_installed
from ..models import CANCEL, DEFAULT, Action, CharacterEntry, Shortcut
from .selector import Selector


class Tofi(Selector):
    @staticmethod
    def supported() -> bool:
        return is_installed("tofi")

    @staticmethod
    def name() -> str:
        return "tofi"

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
        parameters = [
            "tofi",
            "--require-match=true",
            "--fuzzy-match=true",
            f"--prompt-text={prompt}",
            *additional_args,
        ]

        tofi = run(
            parameters, input="\n".join(self.basic_format_characters(characters)), capture_output=True, encoding="utf-8"
        )

        return DEFAULT(), [self.extract_char_from_basic_output(line) for line in tofi.stdout.splitlines()]

    def show_skin_tone_selection(
        self, tones_emojis: List[str], prompt: str, additional_args: List[str]
    ) -> Tuple[int, str]:
        tofi = run(
            ["tofi", "--require-match=true", f"--prompt-text={prompt}", *additional_args],
            input="\n".join(tones_emojis),
            capture_output=True,
            encoding="utf-8",
        )

        return tofi.returncode, tofi.stdout

    def show_action_menu(self, additional_args: List[str]) -> List[Action]:
        tofi = run(
            [
                "tofi",
                "--require-match=true",
                "--matching-algorithm=fuzzy",
                *additional_args,
            ],
            input="\n".join([it.value for it in Action if it != Action.MENU]),
            capture_output=True,
            encoding="utf-8",
        )

        return [Action(tofi.stdout.strip())]
