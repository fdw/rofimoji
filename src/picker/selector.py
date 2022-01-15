from subprocess import run
from typing import List, Tuple, Dict

try:
    from picker.abstractionhelper import is_wayland, is_installed
    from picker.action import Action
except ModuleNotFoundError:
    from abstractionhelper import is_wayland, is_installed
    from action import Action


class Selector:
    @staticmethod
    def best_option(name: str = None) -> 'Selector':
        try:
            return next(selector for selector in Selector.__subclasses__() if selector.name() == name)()
        except StopIteration:
            try:
                return next(selector for selector in Selector.__subclasses__() if selector.supported())()
            except StopIteration:
                return Selector()

    @staticmethod
    def supported() -> bool:
        pass

    @staticmethod
    def name() -> str:
        pass

    def show_character_selection(
            self,
            characters: str,
            recent_characters: str,
            prompt: str,
            keybindings: Dict[Action, str],
            additional_args: List[str]
    ) -> Tuple[int, str]:
        print('Could not find a valid way to show the selection. Please check the required dependencies.')
        exit(4)

    def show_skin_tone_selection(self, skin_tones: str, prompt: str, additional_args: List[str]) -> Tuple[int, str]:
        print('Could not find a valid way to show the selection. Please check the required dependencies.')
        exit(4)


class Rofi(Selector):
    @staticmethod
    def supported() -> bool:
        return is_installed('rofi')

    @staticmethod
    def name() -> str:
        return 'rofi'

    def show_character_selection(
            self,
            characters: str,
            recent_characters: str,
            prompt: str,
            keybindings: Dict[Action, str],
            additional_args: List[str]
    ) -> Tuple[int, str]:
        parameters = [
            'rofi',
            '-dmenu',
            '-markup-rows',
            '-i',
            '-multi-select',
            '-p',
            prompt,
            '-kb-custom-11',
            keybindings[Action.COPY],
            '-kb-custom-12',
            keybindings[Action.TYPE],
            '-kb-custom-13',
            keybindings[Action.CLIPBOARD],
            '-kb-custom-14',
            keybindings[Action.UNICODE],
            '-kb-custom-15',
            keybindings[Action.COPY_UNICODE],
            *additional_args
        ]

        if recent_characters:
            parameters.extend(['-mesg', recent_characters])

        rofi = run(
            parameters,
            input=characters,
            capture_output=True,
            encoding='utf-8'
        )
        return rofi.returncode, rofi.stdout

    def show_skin_tone_selection(self, skin_tones: str, prompt: str, additional_args: List[str]) -> Tuple[int, str]:
        rofi = run(
            [
                'rofi',
                '-dmenu',
                '-i',
                '-p',
                prompt,
                *additional_args
            ],
            input=skin_tones,
            capture_output=True,
            encoding='utf-8'
        )

        return rofi.returncode, rofi.stdout


class Wofi(Selector):
    @staticmethod
    def supported() -> bool:
        return is_wayland() and is_installed('wofi')

    @staticmethod
    def name() -> str:
        return 'wofi'

    def show_character_selection(
            self,
            characters: str,
            recent_characters: str,
            prompt: str,
            keybindings: Dict[Action, str],
            additional_args: List[str]
    ) -> Tuple[int, str]:
        parameters = [
            'wofi',
            '--dmenu',
            '--allow-markup',
            '-i',
            '-p',
            prompt,
            *additional_args
        ]

        wofi = run(
            parameters,
            input=characters,
            capture_output=True,
            encoding='utf-8'
        )
        return wofi.returncode, wofi.stdout

    def show_skin_tone_selection(self, skin_tones: str, prompt: str, additional_args: List[str]) -> Tuple[int, str]:
        wofi = run(
            [
                'wofi',
                '--dmenu',
                '-i',
                '-p',
                prompt,
                *additional_args
            ],
            input=skin_tones,
            capture_output=True,
            encoding='utf-8'
        )

        return wofi.returncode, wofi.stdout
