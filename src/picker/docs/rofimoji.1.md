% ROFIMOJI(1) Version 5.5.0 | Rofi Third-party Add-on Documentation
% Fabian Winter
% July 17, 2022

# NAME


**rofimoji** \- A character (emoji) picker for rofi

# SYNOPSIS

| **rofimoji** \[**-h**] \[**\--version**] \[**\--action** {*type*,*copy*,*clipboard*,*unicode*,*copy-unicode*,*print*}]
         \[**\--skin-tone** {*neutral*,*light*,*medium-light*,*moderate*,*dark brown*,*black*,*ask*}]
         \[**\--files** {*all*,*FILE* \[*FILE* ...]]} \[**\--prompt** *PROMPT*]
         \[**\--selector-args** *SELECTOR_ARGS*] \[**\--max-recent** *MAX_RECENT*] \[**\--no-frecency**]
         \[**\--clipboarder** *CLIPBOARDER*] \[**\--typer** *TYPER*] \[**\--selector** *SELECTOR*]

# DESCRIPTION

Select, insert, or copy Unicode characters like emoji using rofi.

# OPTIONS

-h, \--help

:   Prints brief usage information.

\--version

:   show program's version number and exit

\--action, -a

: Possible values: type, copy, clipboard, unicode, copy-unicode, print

      Choose what to do with the selected characters: Directly type them with the "Typer", copy them to the clipboard using the "Clipboarder", or insert them indirectly using the clipboard. "unicode" will type the unicode codepoints of the chosen characters, "copy-unicode" will copy it. "print" just outputs them on stdout.

\--skin-tone=_skin-tone_, -s _skin-tone_

: Possible values: neutral, light, medium-light, moderate, dark brown, black, ask

      Decide on a skin-tone for all supported emojis. If not
      set (or set to "ask"), you will be asked for each one

\--files=_FILE_ [_FILE_ ...], -f _FILE_ [_FILE_ ...]

:  Read characters from this file instead, one entry per line
:  In the config file, several files need to be listed as `files=[_FILE_, _FILE_ ]`.

\--prompt _PROMPT_, -r _PROMPT_

:  Set rofimoji's prompt

\--selector-args _SELECTOR-ARGS_

:  A string of arguments to give to the selector.

\--max-recent _MAX-RECENT_

:  Show at most this number of recently used characters
   (cannot be larger than 10)

\--no-frecency

:  Don't show frequently used characters at the start.

\--clipboarder _CLIPBOARDER_

: Possible values: xsel, xclip, wl-copy

      Choose the application to access the clipboard with manually.

\--typer _TYPER_

: Possible values: xdotool, wtype

      Choose the application to type with manually.

\--selector _SELECTOR_

: Possible values: rofi, wofi

      Choose the selector application manually. Usually `rofi`, but for Wayland, you may want `wofi`.
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
