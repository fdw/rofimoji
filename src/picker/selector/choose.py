from subprocess import run

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
        characters: list[CharacterEntry],
        recent_characters: list[str],
        prompt: str,
        show_description: bool,
        use_icons: bool,
        keybindings: dict[Action, str],
        additional_args: list[str],
    ) -> tuple[Action | DEFAULT | CANCEL, list[str] | Shortcut]:
        parameters = ["choose", "-p", prompt, *additional_args]

        choose = run(
            parameters, input="\n".join(self.basic_format_characters(characters)), capture_output=True, encoding="utf-8"
        )
        return DEFAULT(), [self.extract_char_from_basic_output(line) for line in choose.stdout.splitlines()]

    def show_skin_tone_selection(
        self, tones_emojis: list[str], prompt: str, additional_args: list[str]
    ) -> tuple[int, str]:
        choose = run(
            ["choose", "-p", prompt, *additional_args],
            input="\n".join(tones_emojis),
            capture_output=True,
            encoding="utf-8",
        )

        return choose.returncode, choose.stdout

    def show_action_menu(self, additional_args: list[str]) -> list[Action]:
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
