from subprocess import run

from picker.Typer import Typer


class Clipboarder:
    @staticmethod
    def bestOption() -> 'Clipboarder':
        return next(clipboarder for clipboarder in [XSelClipboarder()] if clipboarder.supported())

    def supported(self) -> bool:
        pass

    def copy_characters_to_clipboard(self, characters: str) -> None:
        pass

    def copy_paste_characters(self, characters: str, active_window: str, typer: Typer) -> None:
        pass


class XSelClipboarder(Clipboarder):
    def supported(self) -> bool:
        return True

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
