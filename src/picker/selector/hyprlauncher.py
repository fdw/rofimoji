from subprocess import run

from ..abstractionhelper import is_installed, is_wayland
from ..models import CANCEL, DEFAULT, Action, CharacterEntry, Shortcut
from .selector import Selector


class Hyprlauncher(Selector):
    @staticmethod
    def supported() -> bool:
        return is_wayland() and is_installed("hyprlauncher")

    @staticmethod
    def name() -> str:
        return "hyprlauncher"

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
        parameters = ["hyprlauncher", "--dmenu", *additional_args]

        hyprlauncher = run(
            parameters, input="\n".join(self.basic_format_characters(characters)), capture_output=True, encoding="utf-8"
        )
        return DEFAULT(), [self._extract_char_from_output(line) for line in hyprlauncher.stdout.splitlines()]

    def show_skin_tone_selection(
        self,
        selected_emoji: str,
        prompt: str,
        show_description: bool,
        use_icons: bool,
        additional_args: list[str],
    ) -> tuple[int, str]:
        hyprlauncher = run(
            ["hyprlauncher", "--dmenu", *additional_args],
            input="\n".join(self._basic_format_skin_tones(selected_emoji)),
            capture_output=True,
            encoding="utf-8",
        )

        return hyprlauncher.returncode, self._extract_char_from_output(hyprlauncher.stdout)

    def show_action_menu(self, additional_args: list[str]) -> list[Action]:
        hyprlauncher = run(
            [
                "hyprlauncher",
                "--dmenu",
                *additional_args,
            ],
            input="\n".join([it.value for it in Action if it != Action.MENU]),
            capture_output=True,
            encoding="utf-8",
        )

        return [Action(hyprlauncher.stdout.strip())]
