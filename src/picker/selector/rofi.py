from subprocess import run
from typing import Dict, List, Tuple, Union

from .selector import Selector
from ..abstractionhelper import is_installed
from ..models import CANCEL, DEFAULT, Action, Shortcut


class Rofi(Selector):
    @staticmethod
    def supported() -> bool:
        return is_installed("rofi")

    @staticmethod
    def name() -> str:
        return "rofi"

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
        parameters = [
            "rofi",
            "-dmenu",
            "-markup-rows",
            "-i",
            "-multi-select",
            "-no-custom",
            "-ballot-unselected-str",
            "",
            "-format",
            "i",
            "-p",
            prompt,
            "-kb-custom-11",
            keybindings[Action.COPY],
            "-kb-custom-12",
            keybindings[Action.TYPE],
            "-kb-custom-13",
            keybindings[Action.CLIPBOARD],
            "-kb-custom-14",
            keybindings[Action.UNICODE],
            "-kb-custom-15",
            keybindings[Action.COPY_UNICODE],
            *additional_args,
        ]

        if recent_characters:
            parameters.extend(["-mesg", self.__format_recent_characters(recent_characters)])

        rofi = run(
            parameters,
            input="\n".join(self.__format_characters(characters, use_icons, show_description)),
            capture_output=True,
            encoding="utf-8",
        )

        if 10 <= rofi.returncode <= 19:
            return DEFAULT(), Shortcut(rofi.returncode - 10)

        action: Union[Action, DEFAULT, CANCEL]
        if rofi.returncode == 1:
            action = CANCEL()
        elif rofi.returncode == 20:
            action = Action.COPY
        elif rofi.returncode == 21:
            action = Action.TYPE
        elif rofi.returncode == 22:
            action = Action.CLIPBOARD
        elif rofi.returncode == 23:
            action = Action.UNICODE
        elif rofi.returncode == 24:
            action = Action.COPY_UNICODE
        else:
            action = DEFAULT()
        return action, [
            self.extract_char_from_input(list(characters)[int(index)]) for index in rofi.stdout.splitlines()
        ]

    def __format_characters(self, characters: Dict[str, str], use_icons: bool, show_description: bool) -> List[str]:
        if use_icons and not show_description:
            return [f"\0meta\x1f{value}\x1ficon\x1f<span>{key}</span>" for key, value in characters.items()]
        elif use_icons and show_description:
            return [f"{value}\0icon\x1f{key}" for key, value in characters.items()]
        elif not use_icons and show_description:
            return self.basic_format_characters(characters)
        else:
            return [f"{key}\0meta\x1f{value}" for key, value in characters.items()]

    def __format_recent_characters(self, recent_characters: List[str]) -> str:
        pairings = [f"\u200e{(index + 1) % 10}: {character}" for index, character in enumerate(recent_characters)]

        return " | ".join(pairings)

    def show_skin_tone_selection(
        self, tones_emojis: List[str], prompt: str, additional_args: List[str]
    ) -> Tuple[int, str]:
        rofi = run(
            ["rofi", "-dmenu", "-i", "-no-custom", "-p", prompt, *additional_args],
            input="\n".join(tones_emojis),
            capture_output=True,
            encoding="utf-8",
        )

        return rofi.returncode, rofi.stdout

    def show_action_menu(self, additional_args: List[str]) -> List[Action]:
        rofi = run(
            [
                "rofi",
                "-dmenu",
                "-multi-select",
                "-no-custom",
                "-ballot-unselected-str",
                "",
                "-i",
                *additional_args,
            ],
            input="\n".join([str(it) for it in Action if it != Action.MENU]),
            capture_output=True,
            encoding="utf-8",
        )

        return [Action(action) for action in rofi.stdout.strip().split("\n")]
