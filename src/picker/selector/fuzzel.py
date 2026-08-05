from subprocess import run

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
        characters: list[CharacterEntry],
        recent_characters: list[CharacterEntry],
        prompt: str,
        show_description: bool,
        use_icons: bool,
        keybindings: dict[Action, str],
        additional_args: list[str],
    ) -> tuple[Action | DEFAULT | CANCEL, list[str] | Shortcut]:
        parameters = ["fuzzel", "--dmenu", "--fuzzy-min-length", "1", "--index", "-p", prompt, *additional_args]

        fuzzel = run(
            parameters, input="\n".join(self.basic_format_characters(characters)), capture_output=True, encoding="utf-8"
        )
        return DEFAULT(), [characters[int(fuzzel.stdout.strip())].character]

    def show_skin_tone_selection(
        self,
        selected_emoji: str,
        prompt: str,
        show_description: bool,
        use_icons: bool,
        additional_args: list[str],
    ) -> tuple[int, str]:
        fuzzel = run(
            ["fuzzel", "--dmenu", "--fuzzy-min-length", "1", "-p", prompt, *additional_args],
            input="\n".join(self._basic_format_skin_tones(selected_emoji)),
            capture_output=True,
            encoding="utf-8",
        )

        return fuzzel.returncode, self._extract_char_from_output(fuzzel.stdout)

    def show_action_menu(self, additional_args: list[str]) -> list[Action]:
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
