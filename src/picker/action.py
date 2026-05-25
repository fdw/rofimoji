from .clipboarder.clipboarder import Clipboarder
from .models import Action
from .typer.typer import Typer


def execute_action(
    characters: str,
    actions: list[Action],
    active_window: str,
    typer_preference: str | None = None,
    clipboarder_preference: str | None = None,
) -> None:
    typer = Typer.best_option(typer_preference)
    clipboarder = Clipboarder.best_option(clipboarder_preference)

    for action in actions:
        match action:
            case Action.TYPE:
                typer.type_characters(characters, active_window)
            case Action.COPY:
                clipboarder.copy_characters_to_clipboard(characters)
            case Action.CLIPBOARD:
                clipboarder.copy_paste_characters(characters, active_window, typer)
            case Action.TYPE_NUMERICAL:
                typer.type_numerical(__as_codepoints(characters), active_window)
            case Action.UNICODE:
                typer.type_characters(__as_codepoint_string(characters), active_window)
            case Action.COPY_UNICODE:
                clipboarder.copy_characters_to_clipboard(__as_codepoint_string(characters))
            case Action.STDOUT:
                print(characters)


def __as_codepoints(characters: str) -> list[int]:
    return [ord(c) for c in characters]


def __as_codepoint_string(characters: str) -> str:
    return "-".join(f"{c:x}" for c in __as_codepoints(characters))
