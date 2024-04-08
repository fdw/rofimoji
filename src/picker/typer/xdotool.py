from subprocess import run

from ..abstractionhelper import is_installed, is_wayland
from .typer import Typer


class XDoToolTyper(Typer):
    @staticmethod
    def supported() -> bool:
        return not is_wayland() and is_installed("xdotool")

    @staticmethod
    def name() -> str:
        return "xdotool"

    def get_active_window(self) -> str:
        return run(args=["xdotool", "getactivewindow"], capture_output=True, encoding="utf-8").stdout[:-1]

    def type_characters(self, characters: str, active_window: str) -> None:
        # There is a timing issue for some applications that do not correctly handle inputs this fast.
        # Slowing down xdotool from 12ms per keystroke to 50ms per keystroke resolves the issue.
        run(["xdotool", "windowactivate", active_window, "type", "--delay=50ms", "--clearmodifiers", characters])

    def insert_from_clipboard(self, active_window: str) -> None:
        run(
            [
                "xdotool",
                "windowfocus",
                "--sync",
                active_window,
                "key",
                "--clearmodifiers",
                "Shift+Insert",
                "sleep",
                "0.05",
            ]
        )
