from abc import ABC, abstractmethod
from typing import Optional

from ..typer.typer import Typer


class Clipboarder(ABC):
    @staticmethod
    def best_option(name: Optional[str] = None) -> "Clipboarder":
        from .noop import NoopClipboarder
        from .wl import WlClipboarder
        from .xclip import XClipClipboarder
        from .xsel import XSelClipboarder

        available_clipboarders = [XSelClipboarder, XClipClipboarder, WlClipboarder, NoopClipboarder]

        if name is not None:
            return next(clipboarder for clipboarder in available_clipboarders if clipboarder.name() == name)()
        else:
            return next(clipboarder for clipboarder in available_clipboarders if clipboarder.supported())()

    @staticmethod
    @abstractmethod
    def supported() -> bool:
        pass

    @staticmethod
    @abstractmethod
    def name() -> str:
        pass

    @abstractmethod
    def copy_characters_to_clipboard(self, characters: str) -> None:
        pass

    @abstractmethod
    def copy_paste_characters(self, characters: str, active_window: str, typer: Typer) -> None:
        pass
