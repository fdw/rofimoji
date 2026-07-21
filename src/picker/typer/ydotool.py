from subprocess import run

from ..abstractionhelper import is_installed
from .typer import Typer

# From /usr/include/linux/input-event-codes.h
_KEYCODES = {
    "0": "11",
    "1": "2",
    "2": "3",
    "3": "4",
    "4": "5",
    "5": "6",
    "6": "7",
    "7": "8",
    "8": "9",
    "9": "10",
    "a": "30",
    "b": "48",
    "c": "46",
    "d": "32",
    "e": "18",
    "f": "33",
}

_PRESS = "1"
_RELEASE = "0"

_INSERT_KEY_CODE = "110"
_LEFT_CTRL_KEY_CODE = "29"
_LEFT_SHIFT_KEY_CODE = "42"
_SPACE_KEY_CODE = "57"
_U_KEY_CODE = "22"


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

    def type_numerical(self, codepoints: list[int], active_window: str) -> None:
        keypresses = []
        for codepoint in codepoints:
            keypresses.extend(
                [
                    f"{_LEFT_CTRL_KEY_CODE}:{_PRESS}",
                    f"{_LEFT_SHIFT_KEY_CODE}:{_PRESS}",
                    f"{_U_KEY_CODE}:{_PRESS}",
                    f"{_U_KEY_CODE}:{_RELEASE}",
                    f"{_LEFT_SHIFT_KEY_CODE}:{_RELEASE}",
                    f"{_LEFT_CTRL_KEY_CODE}:{_RELEASE}",
                ]
            )

            keypresses.extend(
                f"{_KEYCODES[digit]}:{action}" for digit in f"{codepoint:x}" for action in (_PRESS, _RELEASE)
            )

            keypresses.extend([f"{_SPACE_KEY_CODE}:{_PRESS}", f"{_SPACE_KEY_CODE}:{_RELEASE}"])

        run(["ydotool", "key", *keypresses])

    def insert_from_clipboard(self, active_window: str) -> None:
        run(
            [
                "ydotool",
                "key",
                f"{_LEFT_SHIFT_KEY_CODE}:{_PRESS}",
                f"{_INSERT_KEY_CODE}:{_PRESS}",
                f"{_INSERT_KEY_CODE}:{_RELEASE}",
                f"{_LEFT_SHIFT_KEY_CODE}:{_RELEASE}",
            ]
        )
