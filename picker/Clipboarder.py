from subprocess import run

from picker.AbstractionHelper import is_wayland, is_installed
from picker.Typer import Typer


class Clipboarder:
    @staticmethod
    def best_option() -> 'Clipboarder':
        try:
            return next(clipboarder for clipboarder in [WlClipboarder, XSelClipboarder, XClipClipboarder] if clipboarder.supported())()
        except StopIteration:
            print('Could not find a valid way to copy to clipboard.')
            exit(6)

    @staticmethod
    def supported() -> bool:
        pass

    def copy_characters_to_clipboard(self, characters: str) -> None:
        pass

    def copy_paste_characters(self, characters: str, active_window: str, typer: Typer) -> None:
        pass


class XSelClipboarder(Clipboarder):
    @staticmethod
    def supported() -> bool:
        return not is_wayland() and is_installed('xsel')

    def copy_characters_to_clipboard(self, characters: str) -> None:
        run([
            'xsel',
            '-i',
            '-b'
        ],
            input=characters,
            encoding='utf-8'
        )

    def copy_paste_characters(self, characters: str, active_window: str, typer: Typer) -> None:
        old_clipboard_content = run(args=['xsel', '-o', '-b'], capture_output=True).stdout
        old_primary_content = run(args=['xsel', '-o', '-p'], capture_output=True).stdout

        run(args=['xsel', '-i', '-b'], input=characters, encoding='utf-8')
        run(args=['xsel', '-i', '-p'], input=characters, encoding='utf-8')

        typer.insert_from_clipboard(active_window)

        run(args=['xsel', '-i', '-b'], input=old_clipboard_content)
        run(args=['xsel', '-i', '-p'], input=old_primary_content)


class XClipClipboarder(Clipboarder):
    @staticmethod
    def supported() -> bool:
        return not is_wayland() and is_installed('xclip')

    def copy_characters_to_clipboard(self, characters: str) -> None:
        run([
            'xclip',
            '-i',
            '-selection',
            'clipboard'
        ],
            input=characters,
            encoding='utf-8'
        )

    def copy_paste_characters(self, characters: str, active_window: str, typer: Typer) -> None:
        old_clipboard_content = run(args=['xclip', '-o', '-selection', 'clipboard'], capture_output=True).stdout
        old_primary_content = run(args=['xclip', '-o', '-selection', 'primary'], capture_output=True).stdout

        run(args=['xclip', '-i', '-selection', 'clipboard'], input=characters, encoding='utf-8')
        run(args=['xclip', '-i', '-selection', 'primary'], input=characters, encoding='utf-8')

        typer.insert_from_clipboard(active_window)

        run(args=['xclip', '-i', '-selection', 'clipboard'], input=old_clipboard_content)
        run(args=['xclip', '-i', '-selection', 'primary'], input=old_primary_content)


class WlClipboarder(Clipboarder):
    @staticmethod
    def supported() -> bool:
        return is_wayland() and is_installed('wl-copy')

    def copy_characters_to_clipboard(self, characters: str) -> None:
        run(
            ['wl-copy'],
            input=characters,
            encoding='utf-8'
        )

    def copy_paste_characters(self, characters: str, active_window: str, typer: Typer) -> None:
        old_clipboard_content = run(args=['wl-paste'], capture_output=True).stdout
        old_primary_content = run(args=['wl-paste', '--primary'], capture_output=True).stdout

        run(args=['wl-copy'], input=characters, encoding='utf-8')
        run(args=['wl-copy', '--primary'], input=characters, encoding='utf-8')

        typer.insert_from_clipboard(active_window)

        run(args=['wl-copy'], input=old_clipboard_content)
        run(args=['wl-copy', '--primary'], input=old_primary_content)
