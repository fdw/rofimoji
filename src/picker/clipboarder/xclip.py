import subprocess
from subprocess import run

from ..abstractionhelper import is_installed, is_wayland
from ..typer.typer import Typer
from .clipboarder import Clipboarder


class XClipClipboarder(Clipboarder):
    @staticmethod
    def supported() -> bool:
        return not is_wayland() and is_installed("xclip")

    @staticmethod
    def name() -> str:
        return "xclip"

    def copy_characters_to_clipboard(self, characters: str) -> None:
        run(
            ["xclip", "-i", "-selection", "clipboard"],
            input=characters,
            encoding="utf-8",
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
        )

    def copy_paste_characters(self, characters: str, active_window: str, typer: Typer) -> None:
        old_clipboard_content = run(
            args=["xclip", "-out", "-selection", "clipboard", "-target", "text/plain;charset=utf-8"],
            capture_output=True,
            encoding="utf-8",
        )
        old_primary_content = run(
            args=["xclip", "-out", "-selection", "primary", "-target", "text/plain;charset=utf-8"],
            capture_output=True,
            encoding="utf-8",
        )

        run(
            args=["xclip", "-i", "-selection", "clipboard"],
            input=characters,
            encoding="utf-8",
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
        )
        run(
            args=["xclip", "-i", "-selection", "primary"],
            input=characters,
            encoding="utf-8",
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
        )

        typer.insert_from_clipboard(active_window)

        if old_clipboard_content.returncode == 0:
            run(
                args=["xclip", "-i", "-selection", "clipboard"],
                input=old_clipboard_content.stdout,
                stderr=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                encoding="utf-8",
            )
        if old_primary_content.returncode == 0:
            run(
                args=["xclip", "-i", "-selection", "primary"],
                input=old_primary_content.stdout,
                stderr=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                encoding="utf-8",
            )
