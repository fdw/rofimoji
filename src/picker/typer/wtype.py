from subprocess import run

from ..abstractionhelper import is_installed, is_wayland
from ..action import __get_codepoints as get_codepoints
from .typer import Typer


class WTypeTyper(Typer):
    @staticmethod
    def supported() -> bool:
        return is_wayland() and is_installed("wtype")

    @staticmethod
    def name() -> str:
        return "wtype"

    def get_active_window(self) -> str:
        return "not possible with wtype"

    def type_characters(self, characters: str, active_window: str) -> None:
        run(["wtype", characters])

    def insert_from_clipboard(self, active_window: str) -> None:
        run(["wtype", "-M", "shift", "-P", "Insert", "-p", "Insert", "-m", "shift"])

    def type_numerical(self, characters: str, active_window: str) -> None:
        unicode_codepoints = get_codepoints(characters)
        codepoint_list = unicode_codepoints.split("-")
        codepoint_list = ["U" + codepoint for codepoint in codepoint_list]
        codepoint_list = " ".join(codepoint_list)

        run(["wtype", "-M", "ctrl", "-M", "shift", codepoint_list, "-m", "ctrl", "-m", "shift"])
        
        # Type Space then Backspace to "confirm" the character
        run(["wtype", "-k", "Space"])
        run(["wtype", "-k", "BackSpace"])