from typing import Dict, List

from .paths import *


def read_characters_from_files(files: List[str], frecent: List[str], use_additional: bool) -> List[str]:
    all_characters: Dict[str, List[str]] = {}

    if frecent:
        for character in frecent:
            all_characters[character] = []

    for file in __resolve_all_files(files, use_additional):
        characters_from_file = __load_from_file(file)
        for line in characters_from_file:
            parsed_line = line.split(" ", 1)
            all_characters.setdefault(parsed_line[0], []).append(parsed_line[1]) if 1 < len(parsed_line) else ""

    collected_characters: Dict[str, str] = {
        character: ", ".join(descriptions) for character, descriptions in all_characters.items()
    }

    return [f"{key} {value}" for key, value in collected_characters.items() if value != ""]


def __resolve_all_files(files: List[str], use_additional: bool) -> List[Path]:
    resolved_file_names = []
    for file_name in files:
        resolved_file_names += __resolve_file(file_name, use_additional)

    return resolved_file_names


def __resolve_file(file_name: str, use_additional: bool) -> List[Path]:
    resolved_file_names = []

    provided_file = Path(__file__).parent / "data" / f"{file_name}.csv"

    if Path(file_name).expanduser().is_file():
        resolved_file_names.append(Path(file_name).expanduser())
    elif provided_file.is_file():
        resolved_file_names.append(provided_file)
        custom_additional_file = custom_additional_files_location / f"{file_name}.additional.csv"
        if custom_additional_file.is_file():
            resolved_file_names.append(custom_additional_file)
        provided_additional_file = Path(__file__).parent / "data" / "additional" / f"{file_name}.csv"
        if use_additional and provided_additional_file.is_file():
            resolved_file_names.append(provided_additional_file)
    elif file_name == "all":
        nested_file_names = [__resolve_file(file.stem) for file in (Path(__file__).parent / "data").glob("*.csv")]
        resolved_file_names += [file_name for file_names in nested_file_names for file_name in file_names]
    else:
        raise FileNotFoundError(f"Couldn't find file {file_name!r}")

    return resolved_file_names


def __load_from_file(file: Path) -> List[str]:
    return file.read_text().strip("\n").split("\n")
