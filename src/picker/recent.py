import hashlib
from typing import List

from .paths import *


def load_recent_characters(max_recent: int, files: List[str]) -> List[str]:
    try:
        return [char.strip("\n") for char in __filename_for(files).read_text().strip("\n").split("\n")][:max_recent]
    except FileNotFoundError:
        return []
    except NotADirectoryError:
        recents = [char.strip("\n") for char in recents_file_location.read_text().strip("\n").split("\n")][:max_recent]
        recents_file_location.unlink()
        save_recent_characters("".join(recents), max_recent, files)
        return recents


def save_recent_characters(new_characters: str, max_recent: int, files: List[str]) -> None:
    if max_recent == 0:
        return
    max_recent = min(max_recent, 10)

    old_file_name = __filename_for(files)
    new_file_name = old_file_name.with_suffix(".tmp")

    new_file_name.parent.mkdir(parents=True, exist_ok=True)
    with new_file_name.open("w+") as new_file:
        new_file.write(new_characters + "\n")

        try:
            with old_file_name.open("r") as old_file:
                index = 0
                for line in old_file:
                    if new_characters != line.strip("\n"):
                        if index == max_recent - 1:
                            break
                        new_file.write(line)
                        index += 1

            old_file_name.unlink()
        except FileNotFoundError:
            pass

    new_file_name.rename(old_file_name)


def __filename_for(files: List[str]) -> Path:
    return recents_file_location / hashlib.sha256(b"\0".join(f.encode() for f in sorted(files))).hexdigest()
