from subprocess import run

from ..abstractionhelper import is_installed
from ..emoji_data import fitzpatrick_modifiers
from ..models import CANCEL, DEFAULT, Action, CharacterEntry, Shortcut
from .selector import Selector


class Rofi(Selector):
    @staticmethod
    def supported() -> bool:
        return is_installed("rofi")

    @staticmethod
    def name() -> str:
        return "rofi"

    def show_character_selection(
        self,
        characters: list[CharacterEntry],
        recent_characters: list[CharacterEntry],
        prompt: str,
        show_description: bool,
        use_icons: bool,
        keybindings: dict[Action, str],
        additional_args: list[str],
    ) -> tuple[Action | DEFAULT | CANCEL, list[str] | Shortcut]:
        parameters = [
            "rofi",
            "-dmenu",
            "-markup-rows",
            "-i",
            "-multi-select",
            "-no-custom",
            "-ballot-unselected-str",
            "",
            "-format",
            "i",
            "-p",
            prompt,
            "-kb-custom-11",
            keybindings[Action.COPY],
            "-kb-custom-12",
            keybindings[Action.TYPE],
            "-kb-custom-13",
            keybindings[Action.CLIPBOARD],
            "-kb-custom-14",
            keybindings[Action.TYPE_NUMERICAL],
            "-kb-custom-15",
            keybindings[Action.UNICODE],
            "-kb-custom-16",
            keybindings[Action.COPY_UNICODE],
            *additional_args,
        ]

        if recent_characters:
            parameters.extend(["-mesg", self.__format_recent_characters(recent_characters)])

        rofi = run(
            parameters,
            input="\n".join(self.__format_characters(characters, use_icons, show_description)),
            capture_output=True,
            encoding="utf-8",
        )

        if 10 <= rofi.returncode <= 19:
            return DEFAULT(), Shortcut(rofi.returncode - 10)

        action: Action | DEFAULT | CANCEL
        match rofi.returncode:
            case 1:
                action = CANCEL()
            case 20:
                action = Action.COPY
            case 21:
                action = Action.TYPE
            case 22:
                action = Action.CLIPBOARD
            case 23:
                action = Action.UNICODE
            case 24:
                action = Action.COPY_UNICODE
            case 25:
                action = Action.TYPE_NUMERICAL
            case _:
                action = DEFAULT()

        return action, [characters[int(index)].character for index in rofi.stdout.splitlines()]

    def __format_characters(
        self, characters: list[CharacterEntry], use_icons: bool, show_description: bool
    ) -> list[str]:
        if use_icons and not show_description:
            return [
                f"\0meta\x1f{entry.description_html}\x1ficon\x1f<span>{entry.character_html}</span>" for entry in characters
            ]
        elif use_icons and show_description:
            return [f"{entry.description_html}\0icon\x1f<span>{entry.character_html}</span>" for entry in characters]
        elif not use_icons and show_description:
            return [f"{entry.character_html} {entry.description_html}" for entry in characters]
        else:
            return [f"{entry.character_html}\0meta\x1f{entry.description_html}" for entry in characters]

    def __format_recent_characters(self, recent_characters: list[CharacterEntry]) -> str:
        pairings = [
            f"\u200e{(index + 1) % 10}: {character.character_html}" for index, character in enumerate(recent_characters)
        ]

        return " | ".join(pairings)

    def show_skin_tone_selection(
        self,
        selected_emoji: str,
        prompt: str,
        show_description: bool,
        use_icons: bool,
        additional_args: list[str],
    ) -> tuple[int, str]:
        formatted = self.__format_skin_tones(
            selected_emoji,
            show_description,
            use_icons,
        )
        rofi = run(
            ["rofi", "-dmenu", "-markup-rows", "-i", "-no-custom", "-format", "i", "-p", prompt, *additional_args],
            input="\n".join(formatted),
            capture_output=True,
            encoding="utf-8",
        )

        if rofi.returncode == 1:
            return rofi.returncode, ""

        return rofi.returncode, (selected_emoji + list(fitzpatrick_modifiers.keys())[int(rofi.stdout.strip())])

    def __format_skin_tones(self, selected_emoji: str, show_description: bool, use_icons: bool) -> list[str]:
        if use_icons and not show_description:
            return [
                f"\0meta\x1f{description}\x1ficon\x1f<span>{selected_emoji}{modifier}</span>"
                for (modifier, description) in fitzpatrick_modifiers.items()
            ]
        elif use_icons and show_description:
            return [
                f"{description}\0icon\x1f<span>{selected_emoji}{modifier}</span>"
                for (modifier, description) in fitzpatrick_modifiers.items()
            ]
        elif not use_icons and show_description:
            return [
                f"{selected_emoji}{modifier} {description}" for (modifier, description) in fitzpatrick_modifiers.items()
            ]
        else:
            return [
                f"{selected_emoji}{modifier}\0meta\x1f{description}"
                for (modifier, description) in fitzpatrick_modifiers.items()
            ]

    def show_action_menu(self, additional_args: list[str]) -> list[Action]:
        actions = [it for it in Action if it != Action.MENU]
        rofi = run(
            [
                "rofi",
                "-dmenu",
                "-multi-select",
                "-no-custom",
                "-ballot-unselected-str",
                "",
                "-i",
                "-format",
                "i",
                *additional_args,
            ],
            input="\n".join(str(it) for it in actions),
            capture_output=True,
            encoding="utf-8",
        )

        return [actions[int(index)] for index in rofi.stdout.splitlines()]
