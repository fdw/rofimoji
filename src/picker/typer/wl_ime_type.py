from subprocess import run
from typing import List

from ..abstractionhelper import is_installed, is_wayland
from .typer import Typer


class WlImeTypeTyper(Typer):
    @staticmethod
    def supported() -> bool:
        return is_wayland() and is_installed("wl-ime-type")

    @staticmethod
    def name() -> str:
        return "wl-ime-type"

    def get_active_window(self) -> str:
        return "not possible with wl-ime-type"

    def type_characters(self, characters: str, active_window: str) -> None:
        run(["wl-ime-type", characters])

    def insert_from_clipboard(self, active_window: str) -> None:
        return "not possible with wl-ime-type"

    def type_numerical(self, codepoints: List[int], active_window: str) -> None:
        return "not possible with wl-ime-type"
