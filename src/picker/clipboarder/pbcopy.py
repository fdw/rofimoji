from subprocess import run

from ..abstractionhelper import is_installed
from ..typer.typer import Typer
from .clipboarder import Clipboarder


class PBCopyClipboarder(Clipboarder):
    @staticmethod
    def supported() -> bool:
        return is_installed("pbcopy")

    @staticmethod
    def name() -> str:
        return "pbcopy"

    def copy_characters_to_clipboard(self, characters: str) -> None:
        run(["pbcopy"], input=characters, encoding="utf-8")

    def copy_paste_characters(self, characters: str, active_window: str, typer: Typer) -> None:
        old_clipboard_content = run(args=["pbpaste"], capture_output=True, encoding="utf-8")

        run(args=["pbcopy"], input=characters, encoding="utf-8")

        typer.insert_from_clipboard(active_window)

        if old_clipboard_content.returncode == 0:
            run(args=["pbcopy"], input=old_clipboard_content.stdout, encoding="utf-8")
