from typing import List, Dict

from .paths import *


def load_recent_characters(max_recent: int, character_set_hash: str) -> List[str]:
    recents_files_directory.mkdir(parents=True, exist_ok=True)
    recents_file_location = recents_files_directory / character_set_hash
    try:
        return [char.strip("\n") for char in recents_file_location.read_text().strip("\n").split("\n")][:max_recent]
    except FileNotFoundError:
        return []


def save_recent_characters(new_characters: str, character_set_hash: str) -> None:
    max_recent = 10

    recents_files_directory.mkdir(parents=True, exist_ok=True)
    old_file_name = recents_files_directory / character_set_hash
    new_file_name = old_file_name.with_name("recent.tmp")

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
