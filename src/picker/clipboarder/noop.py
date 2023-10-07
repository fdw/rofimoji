from ..typer.typer import Typer
from .clipboarder import Clipboarder


class NoopClipboarder(Clipboarder):
    @staticmethod
    def supported() -> bool:
        return True

    @staticmethod
    def name() -> str:
        return "noop"

    def copy_characters_to_clipboard(self, characters: str) -> None:
        raise NoClipboarderFoundException()

    def copy_paste_characters(self, characters: str, active_window: str, typer: Typer) -> None:
        raise NoClipboarderFoundException()


class NoClipboarderFoundException(Exception):
    def __str__(self) -> str:
        return "Could not find a valid way to copy to clipboard. Please check the required dependencies."
