import html
import math

from .models import CharacterEntry
from .paths import frecency_file_location


def load_frecent_characters() -> list[CharacterEntry]:
    return [CharacterEntry(character) for character in __load_frecent_characters().keys()]


def __load_frecent_characters() -> dict[str, float]:
    frecencies = {}
    try:
        with frecency_file_location.open("r") as file:
            for line in file:
                (frecency, character) = line.strip("\n").split(" ")
                frecencies[character] = float(frecency)
    except FileNotFoundError:
        pass

    return frecencies


def save_frecent_characters(chosen_character: str) -> None:
    new_file_name = frecency_file_location.with_name("frecency.tmp")

    new_file_name.parent.mkdir(parents=True, exist_ok=True)

    chosen_character = html.escape(chosen_character)
    frecencies = __load_frecent_characters()

    frecencies[chosen_character] = frecencies.get(chosen_character, 0) + 1.1

    with new_file_name.open("w+") as new_file:
        for character, frecency in sorted(frecencies.items(), key=lambda item: item[1], reverse=True):
            new_file.write(f"{math.floor(frecency)} {character}\n")

    new_file_name.rename(frecency_file_location)
