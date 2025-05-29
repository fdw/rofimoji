from subprocess import run
from typing import List

from ..abstractionhelper import is_installed, is_wayland
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

    def type_numerical(self, codepoints: List[int], active_window: str) -> None:
        codepoint_list = " ".join([f"U{codepoint:x}" for codepoint in codepoints])

        run(["wtype", "-M", "ctrl", "-M", "shift", codepoint_list, "-m", "ctrl", "-m", "shift"])
