from subprocess import run

from ..abstractionhelper import is_installed, is_wayland
from .typer import Typer


class WTypeTyper(Typer):
    @staticmethod
    def supported() -> bool:
        is_here = is_wayland() and is_installed("wtype")
        # Run a sample wtype command to check if the error message is not "Compositor does not support the virtual keyboard protocol"
        is_compositor = False
        if is_here:
            is_compositor = run(["wtype", "type", "test"], capture_output=True).stderr != b"Compositor does not support the virtual keyboard protocol\n"
            print("relma2 -- is_compositor: ", is_compositor)
        return is_here and is_compositor
    
    @staticmethod
    def name() -> str:
        return "wtype"

    def get_active_window(self) -> str:
        return "not possible with wtype"

    def type_characters(self, characters: str, active_window: str) -> None:
        run(["wtype", characters])

    def insert_from_clipboard(self, active_window: str) -> None:
        run(["wtype", "-M", "shift", "-P", "Insert", "-p", "Insert", "-m", "shift"])
