import re
from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Union

from ..models import CANCEL, DEFAULT, Action, Shortcut


class Selector(ABC):
    @staticmethod
    def best_option(name: str = None) -> "Selector":
        from .dmenu import DMenu
        from .fuzzel import Fuzzel
        from .rofi import Rofi
        from .tofi import Tofi
        from .wofi import Wofi

        available_selectors = [Rofi, Wofi, Fuzzel, Tofi, DMenu]

        if name is not None:
            try:
                return next(selector for selector in available_selectors if selector.name() == name)()
            except StopIteration:
                raise NoSelectorFoundException()
        else:
            try:
                return next(selector for selector in available_selectors if selector.supported())()
            except StopIteration:
                raise NoSelectorFoundException()

    @staticmethod
    @abstractmethod
    def supported() -> bool:
        pass

    @staticmethod
    @abstractmethod
    def name() -> str:
        pass

    @abstractmethod
    def show_character_selection(
        self,
        characters: List[str],
        recent_characters: List[str],
        prompt: str,
        keybindings: Dict[Action, str],
        additional_args: List[str],
    ) -> Tuple[Union[Action, DEFAULT, CANCEL], Union[List[str], Shortcut]]:
        pass

    @abstractmethod
    def show_skin_tone_selection(
        self, tones_emojis: List[str], prompt: str, additional_args: List[str]
    ) -> Tuple[int, str]:
        pass

    @abstractmethod
    def show_action_menu(self, additional_args: List[str]) -> List[Action]:
        pass

    def extract_char_from_input(self, line) -> str:
        return re.match(r"^(?:\u200e(?! ))?(?P<char>.[^ ]*)( .*|$)", line).group("char")


class NoSelectorFoundException(Exception):
    def __str__(self) -> str:
        return "Could not find a valid way to show the selection. Please check the required dependencies."
