import os
import shutil


def is_installed(executable: str) -> bool:
    return shutil.which(executable) is not None


def is_wayland() -> bool:
    return "WAYLAND_DISPLAY" in os.environ
