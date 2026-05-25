from abc import ABC, abstractmethod


class Typer(ABC):
    @staticmethod
    def best_option(name: str | None = None) -> "Typer":
        from .cliclick import CliclickTyper
        from .noop import NoopTyper
        from .wl_ime_type import WlImeTypeTyper
        from .wtype import WTypeTyper
        from .xdotool import XDoToolTyper
        from .ydotool import YdotoolTyper as YDoToolTyper

        available_typers = [XDoToolTyper, WTypeTyper, YDoToolTyper, CliclickTyper, WlImeTypeTyper, NoopTyper]

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
    def type_numerical(self, codepoints: list[int], active_window: str) -> None:
        pass
