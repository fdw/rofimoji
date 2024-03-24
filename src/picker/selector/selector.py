import re
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple, Union

from ..models import CANCEL, DEFAULT, Action, CharacterEntry, Shortcut


class Selector(ABC):
    @staticmethod
    def best_option(name: Optional[str] = None) -> "Selector":
        from .bemenu import Bemenu
        from .dmenu import DMenu
        from .fuzzel import Fuzzel
        from .rofi import Rofi
        from .tofi import Tofi
        from .wmenu import WMenu
        from .wofi import Wofi

        available_selectors = [Rofi, Wofi, Fuzzel, Bemenu, Tofi, DMenu, WMenu]

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
        characters: List[CharacterEntry],
        recent_characters: List[str],
        prompt: str,
        show_description: bool,
        use_icons: bool,
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

    def basic_format_characters(self, characters: List[CharacterEntry]) -> List[str]:
        return [f"{entry.character} {entry.description}" for entry in characters]

    def extract_char_from_basic_output(self, line: str) -> str:
        return re.match(r"^(?:\u200e(?! ))?(?P<char>.[^ ]*)( .*|$)", line).group("char")

    def extract_char_from_input(self, character_definition: str) -> str:
        return re.match(r"^(?:\u200e(?! ))?(?P<char>.[^ ]*)", character_definition).group("char")


class NoSelectorFoundException(Exception):
    def __str__(self) -> str:
        return "Could not find a valid way to show the selection. Please check the required dependencies."
