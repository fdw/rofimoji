from subprocess import run
from typing import List

from ..abstractionhelper import is_installed
from .typer import Typer


class YdotoolTyper(Typer):
    @staticmethod
    def name():
        return "ydotool"

    @staticmethod
    def supported():
        return is_installed("ydotool")

    def get_active_window(self):
        return "not possible with ydotool"

    def type_characters(self, characters: str, active_window: str) -> None:
        pass

    def type_numerical(self, codepoints: List[int], active_window: str) -> None:
        keypresses = []
        for codepoint in codepoints:
            keypresses.append = [
                (self.__get_event_code("LeftCtrl") + ":1"),
                (self.__get_event_code("LeftShift") + ":1"),
                (self.__get_event_code("U") + ":1"),
                (self.__get_event_code("U") + ":0"),
                (self.__get_event_code("LeftShift") + ":0"),
                (self.__get_event_code("LeftCtrl") + ":0"),
                (self.__get_event_code(f"{codepoint:x}") + ":1"),
                (self.__get_event_code(f"{codepoint:x}") + ":0"),
            ]

        run(["ydotool", "key", *keypresses])

    def insert_from_clipboard(self, active_window: str) -> None:
        run(
            [
                "ydotool",
                "key",
                (self.__get_event_code("LeftShift") + ":1"),
                (self.__get_event_code("Insert") + ":1"),
                (self.__get_event_code("Insert") + ":0"),
                (self.__get_event_code("LeftShift") + ":0"),
            ]
        )

    def __get_event_code(self, char: str) -> str:
        return str(self._keycodes[char])

    # From /usr/include/linux/input-event-codes.h
    _keycodes = {
        "0": 11,
        "1": 2,
        "2": 3,
        "3": 4,
        "4": 5,
        "5": 6,
        "6": 7,
        "7": 8,
        "8": 9,
        "9": 10,
        "a": 30,
        "b": 48,
        "c": 46,
        "d": 32,
        "e": 18,
        "f": 33,
        "u": 22,
        "Enter": 28,
        "LeftCtrl": 29,
        "LeftShift": 42,
        "BackSpace": 14,
        "Tab": 15,
    }
