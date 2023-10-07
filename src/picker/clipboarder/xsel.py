from subprocess import run

from ..abstractionhelper import is_installed, is_wayland
from ..typer.typer import Typer
from .clipboarder import Clipboarder


class XSelClipboarder(Clipboarder):
    @staticmethod
    def supported() -> bool:
        return not is_wayland() and is_installed("xsel")

    @staticmethod
    def name() -> str:
        return "xsel"

    def copy_characters_to_clipboard(self, characters: str) -> None:
        run(["xsel", "-i", "-b"], input=characters, encoding="utf-8")

    def copy_paste_characters(self, characters: str, active_window: str, typer: Typer) -> None:
        old_clipboard_content = run(args=["xsel", "-o", "-b"], capture_output=True).stdout
        old_primary_content = run(args=["xsel", "-o", "-p"], capture_output=True).stdout

        run(args=["xsel", "-i", "-b"], input=characters, encoding="utf-8")
        run(args=["xsel", "-i", "-p"], input=characters, encoding="utf-8")

        typer.insert_from_clipboard(active_window)

        run(args=["xsel", "-i", "-b"], input=old_clipboard_content)
        run(args=["xsel", "-i", "-p"], input=old_primary_content)
