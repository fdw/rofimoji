rofimoji(1) "Version 6.8.0" "Rofi Third-party Add-on Documentation"

# NAME

*rofimoji* - An emoji and general character picker for rofi and rofi-likes

# SYNOPSIS

*rofimoji* [_OPTION_]...

*rofimoji* *-h* | *--help*

*rofimoji* *--version*

# DESCRIPTION

*rofimoji* is a character picker for *rofi* and other dmenu-compatible
selectors (rofi-likes). It allows the user to interactively search for
Unicode characters such as emoji by name or keyword, and then either
type the selected character into the currently focused window, copy it
to the clipboard, insert it via the clipboard, or print it to standard
output.

Characters are fuzzy-searchable by keyword. Frequently and recently
used characters are remembered and presented first, unless disabled
with *--no-frecency*.

By default the bundled emoji set is shown, but any of the distributed
character files (or user-provided files in
_${XDG_DATA_HOME}/rofimoji/data_) can be selected with *--files*.

*rofimoji* can also be run as a *rofi* mode; see *rofimoji-rofi*(7).

# OPTIONS

*--action*=_ACTION_ [_ACTION_...], *-a* _ACTION_ [_ACTION_...]
	How to insert the chosen character(s). More than one action may be
	specified, space-separated (e.g. *--action type copy*). One of:

	- _type_: type the character(s) directly via the typer
	- _copy_: copy the character(s) to the clipboard
	- _clipboard_: insert the character(s) indirectly via the clipboard
	- _type-numerical_: type the Unicode codepoints via the compose key
	- _unicode_: type the Unicode codepoints of the character(s)
	- _copy-unicode_: copy the Unicode codepoints to the clipboard
	- _print_: print the character(s) to standard output
	- _menu_: ask at selection time which action to perform

*--files*=_FILE_ [_FILE_...], *-f* _FILE_ [_FILE_...]
	Read characters from the given file(s), one entry per line.
	_FILE_ may be an absolute or relative path (globbing with asterisk
	(\*) is supported), or a bare name referring to one of the
	distributed character files or any file in
	_${XDG_DATA_HOME}/rofimoji/data_. The special value _all_ selects
	every distributed file at once.

	In a config file, multiple files are written as a list, e.g.
	_files = [emojis, math]_.

*--skin-tone*=_TONE_, *-s* _TONE_
	Skin tone to use for all supporting emoji. One of: _neutral_,
	_light_, _medium-light_, _moderate_, _dark brown_, _black_, or
	_ask_. With _ask_ (the default), the user is prompted per emoji.

*--max-recent*=_N_
	Show at most _N_ recently used characters. _N_ is capped at 10.
	Set to 0 to disable the recent-characters feature.

*--no-frecency*
	Do not sort characters by frequency-of-use. Characters appear in
	the order they appear in the source file(s).

*--only-official*
	Use only the official Unicode descriptions. Skip the additional
	descriptions shipped with *rofimoji* and any user-provided ones in
	_${XDG_DATA_HOME}/rofimoji/data_.

*--hidden-descriptions*
	List only the characters, not their descriptions. Descriptions
	remain searchable. Only meaningful for the _rofi_ selector.

*--use-icons*
	Render characters as icons in _rofi_. Not used by other selectors.

*--prompt*=_PROMPT_, *-r* _PROMPT_
	Set the prompt text shown by the selector. Default is "😀 ".

*--selector*=_SELECTOR_
	Use _SELECTOR_ as the selection dialog instead of the
	auto-detected default. One of: _rofi_, _wofi_, _fuzzel_, _bemenu_,
	_tofi_, _dmenu_, _wmenu_, _choose_, _hyprlauncher_.

*--selector-args*=_ARGS_
	A string of arguments passed through to the selector. Quoting
	matters; prefer _--selector-args="ARGS"_ or
	_--selector-args " ARGS"_ due to an argparse limitation
	(https://bugs.python.org/issue9334).

*--clipboarder*=_CLIPBOARDER_
	Use _CLIPBOARDER_ to access the clipboard. One of: _xsel_,
	_xclip_, _wl-copy_, _pbcopy_.

*--typer*=_TYPER_
	Use _TYPER_ to type characters. One of: _xdotool_, _wtype_,
	_ydotool_, _cliclick_, _wl-ime-type_.

*--keybinding-copy*=_KEY_
*--keybinding-type*=_KEY_
*--keybinding-clipboard*=_KEY_
*--keybinding-type-numerical*=_KEY_
*--keybinding-unicode*=_KEY_
*--keybinding-copy-unicode*=_KEY_
	Override the default keybinding for the copy, type, clipboard,
	type-numerical, unicode, and copy-unicode actions respectively.
	Defaults: _Alt+c_, _Alt+t_, _Alt+p_, _Alt+n_, _Alt+u_, _Alt+i_.
	Effective with the _rofi_ and _fuzzel_ selectors; see _KEYBINDINGS_.

*-h*, *--help*
	Print brief usage information and exit.

*--version*
	Print the version number and exit.

# KEYBINDINGS

Custom keybindings are supported by the _rofi_ and _fuzzel_ selectors.
All other selectors ignore the *--keybinding-\** options and only
provide the default _Enter_ confirmation.

With _rofi_ or _fuzzel_, the following keybindings are active (defaults
shown; configurable via the *--keybinding-\** options):

- _Enter_: perform the default action (see *--action*)
- _Shift+Enter_: select multiple characters
- _Alt+c_: copy the selected character(s) to the clipboard
- _Alt+t_: type the selected character(s) directly
- _Alt+p_: insert the selected character(s) via the clipboard
- _Alt+n_: type the Unicode codepoint(s) numerically
  (Ctrl+Shift+U...)
- _Alt+u_: type the Unicode codepoint(s) of the selection
- _Alt+i_: copy the Unicode codepoint(s) of the selection to
  the clipboard

Additionally, _rofi_ provides shortcuts to insert recently used
characters via _Alt+1_, _Alt+2_, etc. (inserting the Nth-most-recently
used character). These use rofi's built-in keybindings and are not
configurable through *rofimoji*. This feature is _rofi_-only; _fuzzel_
does not provide an equivalent.

# EXIT STATUS

*0*
	Success.

*1*
	A runtime error occurred (e.g. no selector found, no typer
	available, configuration error).

# ENVIRONMENT

_XDG_CONFIG_HOME_
	Base directory for the _rofimoji.rc_ config file. Defaults to
	_~/.config_.

_XDG_CONFIG_DIRS_
	Colon-separated list of system config directories searched for
	_rofimoji.rc_. Defaults to _/etc/xdg_.

_XDG_DATA_HOME_
	Base directory for user character data, the _recent_ and
	_frecency_ files. Defaults to _~/.local/share_.

_XDG_CACHE_HOME_
	Base directory for the *rofimoji* cache. Defaults to _~/.cache_.

# FILES

_~/.config/rofimoji.rc_
	Per-user configuration file. Long option names without leading
	dashes are used as keys; see _CONFIGURATION_.

_/etc/xdg/rofimoji.rc_
	System-wide configuration file. Searched via _$XDG_CONFIG_DIRS_
	(default _/etc/xdg_); each directory in that colon-separated list
	is checked.

_~/.local/share/rofimoji/recent_
	Stores the recently used characters.

_~/.local/share/rofimoji/frecency_
	Stores the frequency-of-use data used to order characters when
	*--no-frecency* is not set.

_~/.local/share/rofimoji/data/filename.additional.csv_
	Additional characters or additional descriptions for the character
	set in _filename_.

# CONFIGURATION

Options starting with _--_ can also be set in a config file. The config
file syntax allows:

- _key = value_ for options taking a value
- _flag = true_ for boolean options
- _key = [a, b, c]_ for list-valued options

For example:

```
action = copy
files = [emojis, math]
skin-tone = moderate
```

If an option is specified in more than one place, command-line values
override values from the config file. See
https://github.com/fdw/rofimoji#example-config-file for further
details.

# EXAMPLES

Run with defaults (emoji, type on selection):
	$ rofimoji
Copy instead of type, using math symbols in addition to emoji:
	$ rofimoji --action copy --files emojis,math
Use _fuzzel_ as the selector and _wl-copy_ for clipboard:
	$ rofimoji --selector fuzzel --clipboarder wl-copy
# NOTES

Report bugs and feature requests at
https://github.com/fdw/rofimoji/issues.

# AUTHORS

Fabian Winter.

# SEE ALSO

*rofimoji-rofi*(7), *rofi*(1), *wofi*(1), *fuzzel*(1), *bemenu*(1),
*tofi*(1), *dmenu*(1), *wmenu*(1), *xdotool*(1), *wtype*(1),
*ydotool*(1), *xsel*(1), *xclip*(1), *wl-copy*(1)

# COPYRIGHT

Copyright (C) 2017-2026 Fabian Winter. Released under the MIT License.
