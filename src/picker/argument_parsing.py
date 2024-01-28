import argparse
import shlex

import configargparse

from . import __version__
from .models import Action
from .paths import *


def parse_arguments_strict() -> argparse.Namespace:
    return __parse_arguments(only_known=True)


def parse_arguments_flexible() -> argparse.Namespace:
    return __parse_arguments(only_known=False)


def __parse_arguments(only_known: bool) -> argparse.Namespace:
    parser = configargparse.ArgumentParser(
        description="Select, insert or copy Unicode characters using rofi.",
        default_config_files=config_file_locations,
    )
    parser.add_argument("--version", action="version", version="rofimoji " + __version__)
    parser.add_argument(
        "--action",
        "-a",
        dest="actions",
        action="store",
        type=Action,
        choices=list(Action),
        default=[Action.TYPE],
        nargs="*",
        metavar="ACTION",
        help="How to insert the chosen characters. More than one action may be specified in "
        "a space separated list (for example: `--action type copy`). Options: "
        + ", ".join(f'"{a.value}"' for a in Action),
    )
    parser.add_argument(
        "--skin-tone",
        "-s",
        dest="skin_tone",
        action="store",
        choices=["neutral", "light", "medium-light", "moderate", "dark brown", "black", "ask"],
        default="ask",
        help='Decide on a skin-tone for all supported emojis. If not set (or set to "ask"), '
        "you will be asked for each one ",
    )
    parser.add_argument(
        "--files",
        "-f",
        dest="files",
        action="store",
        default=["emojis*"],
        nargs="+",
        metavar="FILE",
        help="Read characters from this file instead, one entry per line",
    )
    parser.add_argument("--prompt", "-r", dest="prompt", action="store", default="😀 ", help="Set rofimoj's  prompt")
    parser.add_argument(
        "--selector-args",
        dest="selector_args",
        action="store",
        default=False,
        help="A string of arguments to give to the selector",
    )
    parser.add_argument(
        "--max-recent",
        dest="max_recent",
        action="store",
        type=int,
        default=10,
        help="Show at most this number of recently used characters (cannot be larger than 10)",
    )
    parser.add_argument(
        "--no-frecency", dest="frecency", action="store_false", help="Don't show frequently used characters first"
    )
    parser.set_defaults(frecency=True)
    parser.add_argument(
        "--only-official",
        dest="use_additional",
        action="store_false",
        help="Use only the official Unicode descriptions",
    )
    parser.set_defaults(use_additional=True)
    parser.add_argument(
        "--hidden-descriptions",
        dest="show_description",
        action="store_false",
        help="Show only the character without its description",
    )
    parser.set_defaults(show_description=True)
    parser.add_argument(
        "--use-icons",
        dest="use_icons",
        action="store_true",
        help="Use rofi's icon to show the character",
    )
    parser.set_defaults(use_icons=False)
    parser.add_argument(
        "--selector",
        dest="selector",
        action="store",
        type=str,
        choices=["rofi", "wofi", "fuzzel", "dmenu", "tofi", "bemenu", "wmenu"],
        default=None,
        help="Choose the application to select the characters with",
    )
    parser.add_argument(
        "--clipboarder",
        dest="clipboarder",
        action="store",
        type=str,
        choices=["xsel", "xclip", "wl-copy"],
        default=None,
        help="Choose the application to access the clipboard with",
    )
    parser.add_argument(
        "--typer",
        dest="typer",
        action="store",
        type=str,
        choices=["xdotool", "wtype"],
        default=None,
        help="Choose the application to type with",
    )
    parser.add_argument(
        "--keybinding-copy",
        dest="keybinding_copy",
        action="store",
        type=str,
        default="Alt+c",
        help="Choose the keyboard shortcut to copy the character to the clipboard",
    )
    parser.add_argument(
        "--keybinding-type",
        dest="keybinding_type",
        action="store",
        type=str,
        default="Alt+t",
        help="Choose the keyboard shortcut to directly type the character",
    )
    parser.add_argument(
        "--keybinding-clipboard",
        dest="keybinding_clipboard",
        action="store",
        type=str,
        default="Alt+p",
        help="Choose the keyboard shortcut to insert the character via the clipboard",
    )
    parser.add_argument(
        "--keybinding-unicode",
        dest="keybinding_unicode",
        action="store",
        type=str,
        default="Alt+u",
        help="Choose the keyboard shortcut to directly type the character's unicode codepoint",
    )
    parser.add_argument(
        "--keybinding-copy-unicode",
        dest="keybinding_copy_unicode",
        action="store",
        type=str,
        default="Alt+i",
        help="Choose the keyboard shortcut to copy the character's unicode codepoint to the clipboard",
    )

    if only_known:
        parsed_args = parser.parse_args()
    else:
        parsed_args, _ = parser.parse_known_args()

    if parsed_args.selector_args:
        parsed_args.selector_args = shlex.split(parsed_args.selector_args)
    else:
        parsed_args.selector_args = []

    parsed_args.keybindings = {
        Action.TYPE: parsed_args.keybinding_type,
        Action.COPY: parsed_args.keybinding_copy,
        Action.CLIPBOARD: parsed_args.keybinding_clipboard,
        Action.UNICODE: parsed_args.keybinding_unicode,
        Action.COPY_UNICODE: parsed_args.keybinding_copy_unicode,
    }

    return parsed_args
