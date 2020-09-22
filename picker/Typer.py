import os
import shutil
from subprocess import run


class Typer:
    @staticmethod
    def bestOption() -> 'Typer':
        return next(typer for typer in [XDoToolTyper, WTypeTyper] if typer.supported())()

    @staticmethod
    def supported() -> bool:
        pass

    def get_active_window(self) -> str:
        pass

    def type_characters(self, characters: str, active_window: str) -> None:
        pass

    def insert_from_clipboard(self, active_window: str) -> None:
        pass


class XDoToolTyper(Typer):
    @staticmethod
    def supported() -> bool:
        return shutil.which('xdotool') is not None

    def get_active_window(self) -> str:
        return run(args=['xdotool', 'getactivewindow'], capture_output=True,
                   encoding='utf-8').stdout[:-1]

    def type_characters(self, characters: str, active_window: str) -> None:
        run([
            'xdotool',
            'type',
            '--clearmodifiers',
            '--window',
            active_window,
            characters
        ])

    def insert_from_clipboard(self, active_window: str) -> None:
        run([
            'xdotool',
            'windowfocus',
            '--sync',
            active_window,
            'key',
            '--clearmodifiers',
            'Shift+Insert',
            'sleep',
            '0.05',
        ])


class WTypeTyper:
    @staticmethod
    def supported() -> bool:
        return os.environ.get('WAYLAND_DISPLAY', False)

    def get_active_window(self) -> str:
        return "not possible with wtype"

    def type_characters(self, characters: str, active_window: str) -> None:
        run([
            'wtype',
            characters
        ])

    def insert_from_clipboard(self, active_window: str) -> None:
        run([
            'wtype',
            '-M',
            'shift',
            '-P',
            'Insert',
            '-p',
            'Insert',
            '-m',
            'shift'
        ])
