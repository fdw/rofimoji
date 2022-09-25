from subprocess import run
from typing import Dict, List, Tuple, Union

from .abstractionhelper import is_installed, is_wayland
from .models import CANCEL, DEFAULT, Action, Shortcut


class Selector:
    @staticmethod
    def best_option(name: str = None) -> "Selector":
        try:
            return next(selector for selector in Selector.__subclasses__() if selector.name() == name)()
        except StopIteration:
            try:
                return next(selector for selector in Selector.__subclasses__() if selector.supported())()
            except StopIteration:
                return Selector()

    @staticmethod
    def supported() -> bool:
        pass

    @staticmethod
    def name() -> str:
        pass

    def show_character_selection(
        self,
        characters: str,
        recent_characters: str,
        prompt: str,
        keybindings: Dict[Action, str],
        additional_args: List[str],
    ) -> Tuple[Union[Action, DEFAULT, CANCEL], Union[str, Shortcut]]:
        raise NoSelectorFoundException()

    def show_skin_tone_selection(self, skin_tones: str, prompt: str, additional_args: List[str]) -> Tuple[int, str]:
        raise NoSelectorFoundException

    def show_action_menu(self, additional_args: List[str]) -> List[Action]:
        raise NoSelectorFoundException


class Rofi(Selector):
    @staticmethod
    def supported() -> bool:
        return is_installed("rofi")

    @staticmethod
    def name() -> str:
        return "rofi"

    def show_character_selection(
        self,
        characters: str,
        recent_characters: str,
        prompt: str,
        keybindings: Dict[Action, str],
        additional_args: List[str],
    ) -> Tuple[Union[Action, DEFAULT, CANCEL], Union[str, Shortcut]]:
        parameters = [
            "rofi",
            "-dmenu",
            "-markup-rows",
            "-i",
            "-multi-select",
            "-ballot-unselected-str",
            "",
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
            parameters.extend(["-mesg", recent_characters])

        rofi = run(parameters, input=characters, capture_output=True, encoding="utf-8")

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
        return action, rofi.stdout

    def show_skin_tone_selection(self, skin_tones: str, prompt: str, additional_args: List[str]) -> Tuple[int, str]:
        rofi = run(
            ["rofi", "-dmenu", "-i", "-p", prompt, *additional_args],
            input=skin_tones,
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
                "-ballot-unselected-str",
                "",
                "-i",
                *additional_args,
            ],
            input="\n".join([it.value for it in Action if it != Action.MENU]),
            capture_output=True,
            encoding="utf-8",
        )

        return [Action(action) for action in rofi.stdout.strip().split("\n")]


class Wofi(Selector):
    @staticmethod
    def supported() -> bool:
        return is_wayland() and is_installed("wofi")

    @staticmethod
    def name() -> str:
        return "wofi"

    def show_character_selection(
        self,
        characters: str,
        recent_characters: str,
        prompt: str,
        keybindings: Dict[Action, str],
        additional_args: List[str],
    ) -> Tuple[Union[Action, DEFAULT, CANCEL], Union[str, Shortcut]]:
        parameters = ["wofi", "--dmenu", "--allow-markup", "-i", "-p", prompt, *additional_args]

        wofi = run(parameters, input=characters, capture_output=True, encoding="utf-8")
        return DEFAULT(), wofi.stdout

    def show_skin_tone_selection(self, skin_tones: str, prompt: str, additional_args: List[str]) -> Tuple[int, str]:
        wofi = run(
            ["wofi", "--dmenu", "-i", "-p", prompt, *additional_args],
            input=skin_tones,
            capture_output=True,
            encoding="utf-8",
        )

        return wofi.returncode, wofi.stdout

    def show_action_menu(self, additional_args: List[str]) -> List[Action]:
        wofi = run(
            [
                "wofi",
                "-dmenu",
                "-i",
                *additional_args,
            ],
            input="\n".join([it.value for it in Action if it != Action.MENU]),
            capture_output=True,
            encoding="utf-8",
        )

        return [Action(wofi.stdout.strip())]


class NoSelectorFoundException(Exception):
    def __str__(self) -> str:
        return "Could not find a valid way to show the selection. Please check the required dependencies."
