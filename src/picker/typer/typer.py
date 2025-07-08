from abc import ABC, abstractmethod
from typing import List, Optional


class Typer(ABC):
    @staticmethod
    def best_option(name: Optional[str] = None) -> "Typer":
        from .cliclick import CliclickTyper
        from .noop import NoopTyper
        from .wtype import WTypeTyper
        from .xdotool import XDoToolTyper
        from .ydotool import YdotoolTyper as YDoToolTyper

        available_typers = [XDoToolTyper, WTypeTyper, YDoToolTyper, CliclickTyper, NoopTyper]

        if name is not None:
            return next(typer for typer in available_typers if typer.name() == name)()
        else:
            return next(typer for typer in available_typers if typer.supported())()

    @staticmethod
    @abstractmethod
    def supported() -> bool:
        pass

    @staticmethod
    @abstractmethod
    def name() -> str:
        pass

    @abstractmethod
    def get_active_window(self) -> str:
        pass

    @abstractmethod
    def type_characters(self, characters: str, active_window: str) -> None:
        pass

    @abstractmethod
    def insert_from_clipboard(self, active_window: str) -> None:
        pass

    @abstractmethod
    def type_numerical(self, codepoints: List[int], active_window: str) -> None:
        pass
