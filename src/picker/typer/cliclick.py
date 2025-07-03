from subprocess import run
from typing import List

from ..abstractionhelper import is_installed
from .typer import Typer


class CliclickTyper(Typer):
    @staticmethod
    def supported() -> bool:
        return is_installed("cliclick")

    @staticmethod
    def name() -> str:
        return "cliclick"

    def get_active_window(self) -> str:
        return ""

    def type_characters(self, characters: str, active_window: str) -> None:
        pass


    def insert_from_clipboard(self, active_window: str) -> None:
        run(
            [
                "cliclick",
                "-w 100",
                "kd:cmd",
                "t:v",
                "ku:cmd"
            ]
        )

    def type_numerical(self, codepoints: List[int], active_window: str) -> None:
        pass
