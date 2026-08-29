rofimoji-rofi(7) "Version 6.8.0" "Rofi Third-party Add-on Documentation"

# NAME

*rofimoji-rofi* - Running *rofimoji* as a rofi mode

# SYNOPSIS

*rofi* *-modi* _emoji:rofimoji_ *-show* _emoji_

# DESCRIPTION

*rofimoji* can be integrated into *rofi* as a mode, so that it appears
alongside rofi's other modes (applications, window list, etc.). This is
useful when *rofimoji* should behave as just another entry in a unified
launcher rather than as a standalone dialog.

Because *rofi* is the main process in this mode, *rofimoji* cannot
directly type characters into other windows. Only clipboard-based
actions are available, so *--action* should be set to _copy_,
_clipboard_, _copy-unicode_, _print_, or _menu_. The _type_,
_type-numerical_, and _unicode_ actions will not work.

Configuration options are otherwise the same as for the standalone
invocation; see *rofimoji*(1) for the full list.

# KEYBINDINGS

The same keybinding options as in standalone mode apply (see
*rofimoji*(1)), but rofi owns the keybinding table, so the shortcuts
are remapped to _Alt+Shift_ combined with the configured keys. On a
Qwerty keyboard the defaults become:

- _Enter_: perform the default action
- _Alt+Shift+c_: copy the selected character to the clipboard
- _Alt+Shift+p_: insert the selected character via the clipboard
- _Alt+Shift+i_: copy the Unicode codepoint to the clipboard
- _Alt+Shift+1_, _Alt+Shift+2_, ...: insert the Nth-most-recently-used
  character

The _Alt+Shift+t_, _Alt+Shift+n_, and _Alt+Shift+u_ keybindings (type,
type-numerical, unicode) are mapped but have no effect, since *rofimoji*
cannot type in this mode.

Unlike standalone mode, multiple-character selection via _Shift+Enter_
is not available: only a single character can be selected at a time.

# EXAMPLES

Show the emoji mode:
	$ rofi -modi emoji:rofimoji -show emoji
Combine the emoji mode with others in a _combi_:
	$ rofi -modi combi -show combi -combi-modi "window,drun,emoji:rofimoji"
# AUTHORS

Fabian Winter.

# SEE ALSO

*rofimoji*(1), *rofi*(1)

# COPYRIGHT

Copyright (C) 2017-2026 Fabian Winter. Released under the MIT License.
