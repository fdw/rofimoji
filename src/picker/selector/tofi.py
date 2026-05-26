from subprocess import run

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
        characters: list[CharacterEntry],
        recent_characters: list[str],
        prompt: str,
        show_description: bool,
        use_icons: bool,
        keybindings: dict[Action, str],
        additional_args: list[str],
    ) -> tuple[Action | DEFAULT | CANCEL, list[str] | Shortcut]:
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

        return DEFAULT(), [self._extract_char_from_output(line) for line in tofi.stdout.splitlines()]

    def show_skin_tone_selection(
        self,
        selected_emoji: str,
        prompt: str,
        show_description: bool,
        use_icons: bool,
        additional_args: list[str],
    ) -> tuple[int, str]:
        tofi = run(
            ["tofi", "--require-match=true", f"--prompt-text={prompt}", *additional_args],
            input="\n".join(self._basic_format_skin_tones(selected_emoji)),
            capture_output=True,
            encoding="utf-8",
        )

        return tofi.returncode, self._extract_char_from_output(tofi.stdout)

    def show_action_menu(self, additional_args: list[str]) -> list[Action]:
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
