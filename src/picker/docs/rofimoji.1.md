% ROFIMOJI(1) Version 6.3.2 | Rofi Third-party Add-on Documentation
% Fabian Winter
% June 11, 2024

# NAME


**rofimoji** \- An emoji and general character picker for rofi and rofi-likes

# SYNOPSIS

| **rofimoji** \[**-h**] \[**\--version**] \[**\--action** {*type*,*copy*,*clipboard*,*unicode*,*copy-unicode*,*print*,*menu*}]
         \[**\--skin-tone** {*neutral*,*light*,*medium-light*,*moderate*,*dark brown*,*black*,*ask*}]
         \[**\--files** {*all*,*FILE* \[*FILE* ...]]} \[**\--prompt** *PROMPT*]
         \[**\--selector-args** *SELECTOR_ARGS*] \[**\--max-recent** *MAX_RECENT*] \[**\--no-frecency**] \[**\--hidden-descriptions**]
         \[**\--clipboarder** *CLIPBOARDER*] \[**\--typer** *TYPER*] \[**\--selector** *SELECTOR*]

# DESCRIPTION

Select, insert, or copy Unicode characters like emoji using rofi.

# OPTIONS

-h, \--help

:   Prints brief usage information.

\--version

:   show program's version number and exit

\--action, -a

: Possible values: type, copy, clipboard, unicode, copy-unicode, print, menu

      Choose what to do with the selected characters: Directly type them with the "Typer", copy them to the clipboard using the "Clipboarder", or insert them indirectly using the clipboard. "unicode" will type the unicode codepoints of the chosen characters, "copy-unicode" will copy it. "print" just outputs them on stdout.
      If you want to decide on the fly, use "menu".

\--files _FILE_ [_FILE_ ...], -f _FILE_ [_FILE_ ...]

:  Read characters from this file (or these files), one entry per line. Absolute and relative paths are supported, as is globbing (`--files /home/you/characters.csv ../other*.csv`).
:  A filename without extension is enough (`--files musical_symbols supplemental_arrows`) for included character files and all in `${XDG_DATA_HOME}/rofimoji/data`. Here, too, globbing is supported and done by default.
:  In the config file, several files need to be listed as `files=[_FILE_, _FILE_]`.

\--skin-tone=_skin-tone_, -s _skin-tone_

: Possible values: neutral, light, medium-light, moderate, dark brown, black, ask

      Decide on a skin-tone for all supported emojis. If not
      set (or set to "ask"), you will be asked for each one

\--max-recent _MAX-RECENT_

: Show at most this number of recently used characters
   (cannot be larger than 10)

\--no-frecency

: Don't show frequently used characters at the start.

\--hidden-descriptions

: Only list the characters, but not their description. Note that you can still search through the descriptions. Only used for `rofi`.

\--use-icons

: Show characters as icons on `rofi`. Not used with other selectors.

\--prompt _PROMPT_, -r _PROMPT_

: Set rofimoji's prompt

\--selector-args _SELECTOR-ARGS_

: A string of arguments to give to the selector.

\--selector _SELECTOR_

: Possible values: rofi, wofi, fuzzel, dmenu, tofi, bemenu, wmenu

      Choose the selector application manually. Usually `rofi`, but you may want something else.

\--clipboarder _CLIPBOARDER_

: Possible values: xsel, xclip, wl-copy

      Choose the application to access the clipboard with manually.

\--typer _TYPER_

: Possible values: xdotool, wtype

      Choose the application to type with manually.

\--keybinding-copy, \--keybinding-type, \--keybinding-clipboard, \--keybinding-unicode, \--keybinding-copy-unicode

: Define different keybindings for these actions.


# KEYBINDINGS

(optional) Select multiple emoji with shift+enter

*enter* to insert the emoji directly

*alt+c* to copy it to the clipboard

*alt+t* to type it directly

*alt+p* to insert using the clipboard

*alt+1*, *alt+2* to insert the most recently used character (alt+2 for the second most recently one etc.)

*alt+u* to insert the Unicode codepoint

*alt+i* to copy the Unicode codepoint to the clipboard

Please note that wofi does not support keybindings other than *enter*.

# FILES

*~/.config/rofimoji.rc*

:   Per-user configuration file.

*/etc/xdg/xdg-i3/rofimoji.rc*

:   Global configuration file.

*~/.local/share/rofimoji/recent*

:   Stores the recently used characters

*~/.local/share/rofimoji/data/**filename**.additional.csv*

:   Contains additional characters or additional descriptions for the character set in **filename**

# CONFIGURATION

Args that start with "\--" (eg. \--version) can also be set in a config file.

Config file syntax allows: key=value, flag=true, stuff=[a,b,c] (for details, see syntax at https://github.com/fdw/rofimoji#example-config-file). If an arg is
specified in more than one place, then commandline values override values from the config file.

# WEBSITE

https://github.com/fdw/rofimoji
