from glob import glob
from typing import Dict, List

from .models import CharacterEntry
from .paths import *


def read_characters_from_files(files: List[str], frecent: List[str], use_additional: bool) -> List[CharacterEntry]:
    all_characters: Dict[str, CharacterEntry] = {}

    for character in frecent:
        all_characters[character] = CharacterEntry(character)

    for file in __resolve_all_filenames(files, use_additional):
        characters_from_file = __load_from_file(file)
        for character_entry in characters_from_file:
            if character_entry.character in all_characters:
                all_characters[character_entry.character].merge(character_entry)
            else:
                all_characters[character_entry.character] = character_entry

    return [character for character in all_characters.values() if character.description]


def __resolve_all_filenames(file_names: List[str], use_additional: bool) -> List[Path]:
    resolved_file_names = []
    for file_name in file_names:
        resolved_file_names += __resolve_filename(file_name, use_additional)

    return resolved_file_names


def __resolve_filename(file_name: str, use_additional: bool) -> List[Path]:
    resolved_file_names = []

    for absolute_file in glob(os.path.expanduser(file_name)):
        resolved_file_names.append(Path(absolute_file))

    if resolved_file_names:
        return resolved_file_names

    for custom_files in custom_additional_files_location.glob(file_name if "*" in file_name else f"{file_name}*"):
        if not custom_files.name.endswith(".additional.csv"):
            resolved_file_names.append(custom_files)

    if resolved_file_names:
        return resolved_file_names

    for distributed_file in (Path(__file__).parent / "data").glob(file_name if "*" in file_name else f"{file_name}*"):
        resolved_file_names.append(distributed_file)
        resolved_file_names += __load_additional_files(distributed_file, use_additional)

    if resolved_file_names:
        return resolved_file_names

    if file_name == "all":
        nested_file_names = [
            __resolve_filename(file.stem, use_additional) for file in (Path(__file__).parent / "data").glob("*.csv")
        ]
        resolved_file_names += [file_name for file_names in nested_file_names for file_name in file_names]
        return resolved_file_names

    raise FileNotFoundError(f"Couldn't find file {file_name!r}")


def __load_additional_files(original_file: Path, use_additional: bool) -> List[Path]:
    additional_files = []
    custom_additional_file = custom_additional_files_location / f"{original_file.stem}.additional.csv"
    if custom_additional_file.is_file():
        additional_files.append(custom_additional_file)
    provided_additional_file = Path(__file__).parent / "data" / "additional" / f"{original_file.stem}.csv"
    if use_additional and provided_additional_file.is_file():
        additional_files.append(provided_additional_file)

    return additional_files


def __load_from_file(file: Path) -> List[CharacterEntry]:
    lines = file.read_text().strip("\n").split("\n")

    all_character_entries = []
    for line in lines:
        parsed_line = line.split(" ", 1)
        all_character_entries.append(CharacterEntry(parsed_line[0], parsed_line[1]))

    return all_character_entries
