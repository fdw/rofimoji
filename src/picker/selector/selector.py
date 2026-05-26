import re
from abc import ABC, abstractmethod

from .. import emoji_data
from ..models import CANCEL, DEFAULT, Action, CharacterEntry, Shortcut


class Selector(ABC):
    @staticmethod
    def best_option(name: str | None = None) -> "Selector":
        from .bemenu import Bemenu
        from .choose import Choose
        from .dmenu import DMenu
        from .fuzzel import Fuzzel
        from .hyprlauncher import Hyprlauncher
        from .rofi import Rofi
        from .tofi import Tofi
        from .wmenu import WMenu
        from .wofi import Wofi

        available_selectors = [Rofi, Wofi, Fuzzel, Bemenu, Tofi, Hyprlauncher, DMenu, WMenu, Choose]

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
        characters: list[CharacterEntry],
        recent_characters: list[str],
        prompt: str,
        show_description: bool,
        use_icons: bool,
        keybindings: dict[Action, str],
        additional_args: list[str],
    ) -> tuple[Action | DEFAULT | CANCEL, list[str] | Shortcut]:
        pass

    @abstractmethod
    def show_skin_tone_selection(
        self,
        selected_emoji: str,
        prompt: str,
        show_description: bool,
        use_icons: bool,
        additional_args: list[str],
    ) -> tuple[int, str]:
        pass

    @abstractmethod
    def show_action_menu(self, additional_args: list[str]) -> list[Action]:
        pass

    @staticmethod
    def _basic_format_skin_tones(selected_emoji: str) -> list[str]:
        return [
            f"{selected_emoji}{modifier} {emoji_data.fitzpatrick_modifiers[modifier]}"
            for modifier in emoji_data.fitzpatrick_modifiers
        ]

    def basic_format_characters(self, characters: list[CharacterEntry], strip_tags: bool = True) -> list[str]:
        return [
            f"{entry.character} {entry.description.replace('<small>', '').replace('</small>', '') if strip_tags else entry.description}"
            for entry in characters
        ]

    def _extract_char_from_output(self, line: str) -> str:
        return re.match(r"^(?:\u200e(?! ))?(?P<char>.[^ ]*)( .*|$)", line).group("char")


class NoSelectorFoundException(Exception):
    def __str__(self) -> str:
        return "Could not find a valid way to show the selection. Please check the required dependencies."
