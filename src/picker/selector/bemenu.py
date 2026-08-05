from subprocess import run

from ..abstractionhelper import is_installed
from ..models import CANCEL, DEFAULT, Action, CharacterEntry, Shortcut
from .selector import Selector


class Bemenu(Selector):
    @staticmethod
    def supported() -> bool:
        return is_installed("bemenu")

    @staticmethod
    def name() -> str:
        return "bemenu"

    def show_character_selection(
        self,
        characters: list[CharacterEntry],
        recent_characters: list[CharacterEntry],
        prompt: str,
        show_description: bool,
        use_icons: bool,
        keybindings: dict[Action, str],
        additional_args: list[str],
    ) -> tuple[Action | DEFAULT | CANCEL, list[str] | Shortcut]:
        parameters = ["bemenu", "--ignorecase", "-p", prompt, *additional_args]

        bemenu = run(
            parameters, input="\n".join(self.basic_format_characters(characters)), capture_output=True, encoding="utf-8"
        )
        return DEFAULT(), [self._extract_char_from_output(line) for line in bemenu.stdout.splitlines()]

    def show_skin_tone_selection(
        self,
        selected_emoji: str,
        prompt: str,
        show_description: bool,
        use_icons: bool,
        additional_args: list[str],
    ) -> tuple[int, str]:
        bemenu = run(
            ["bemenu", "-p", prompt, *additional_args],
            input="\n".join(self._basic_format_skin_tones(selected_emoji)),
            capture_output=True,
            encoding="utf-8",
        )

        return bemenu.returncode, self._extract_char_from_output(bemenu.stdout)

    def show_action_menu(self, additional_args: list[str]) -> list[Action]:
        bemenu = run(
            [
                "bemenu",
                *additional_args,
            ],
            input="\n".join([it.value for it in Action if it != Action.MENU]),
            capture_output=True,
            encoding="utf-8",
        )

        return [Action(bemenu.stdout.strip())]
