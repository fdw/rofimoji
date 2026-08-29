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
        parameters = [
            "fuzzel",
            "--dmenu",
            "--fuzzy-min-length",
            "1",
            "--index",
            "-p",
            prompt,
            *self.__build_parameters_for_keybindings(keybindings),
            *additional_args,
        ]

        fuzzel = run(
            parameters, input="\n".join(self.basic_format_characters(characters)), capture_output=True, encoding="utf-8"
        )

        if fuzzel.returncode == 1:
            return CANCEL(), []
        elif fuzzel.returncode >= 10:
            action = list(keybindings.keys())[fuzzel.returncode - 10]
        else:
            action = DEFAULT()

        return action, [characters[int(fuzzel.stdout.strip())].character]

    def __build_parameters_for_keybindings(self, keybindings: dict[Action, str]) -> list[str]:
        params = []
        for index, shortcut in enumerate(keybindings.values()):
            params.append(f"--override=key-bindings.custom-{1 + index}={self.__translate_shortcut(shortcut)}")
        return params

    def __translate_shortcut(self, shortcut: str) -> str:
        return "+".join("Mod1" if token == "Alt" else token for token in shortcut.split("+"))

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
