from typing import List, Optional

from .clipboarder.clipboarder import Clipboarder
from .models import Action
from .typer.typer import Typer


def execute_action(
    characters: str,
    actions: List[Action],
    active_window: str,
    typer_preference: Optional[str] = None,
    clipboarder_preference: Optional[str] = None,
) -> None:
    typer = Typer.best_option(typer_preference)
    clipboarder = Clipboarder.best_option(clipboarder_preference)

    for action in actions:
        if action == Action.TYPE:
            typer.type_characters(characters, active_window)
        elif action == Action.COPY:
            clipboarder.copy_characters_to_clipboard(characters)
        elif action == Action.CLIPBOARD:
            clipboarder.copy_paste_characters(characters, active_window, typer)
        elif action == Action.TYPE_NUMERICAL:
            typer.type_numerical(__as_codepoints(characters), active_window)
        elif action == Action.UNICODE:
            typer.type_characters(__as_codepoint_string(characters), active_window)
        elif action == Action.COPY_UNICODE:
            clipboarder.copy_characters_to_clipboard(__as_codepoint_string(characters))
        elif action == Action.STDOUT:
            print(characters)


def __as_codepoints(characters: str) -> list[int]:
    return [ord(c) for c in characters]


def __as_codepoint_string(characters: str) -> str:
    return "-".join(f"{c:x}" for c in __as_codepoints(characters))
