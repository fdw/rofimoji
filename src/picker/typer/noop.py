from .typer import Typer


class NoopTyper(Typer):
    @staticmethod
    def supported() -> bool:
        return True

    @staticmethod
    def name() -> str:
        return "noop"

    def get_active_window(self) -> str:
        return ""

    def type_characters(self, characters: str, active_window: str) -> None:
        raise NoTyperFoundException()

    def insert_from_clipboard(self, active_window: str) -> None:
        raise NoTyperFoundException()


class NoTyperFoundException(Exception):
    def __str__(self) -> str:
        return "Could not find a valid way to type characters. Please check the required dependencies."
