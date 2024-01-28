# [NEXT]
## Added
- Support for [bemenu](https://github.com/Cloudef/bemenu) and [wmenu](https://git.sr.ht/~adnano/wmenu) as selectors

# [6.2.0]
## Added
- Support dmenu as selector.
- Support `rofi`'s icons.

## Changed
- Updated to Unicode (including Emojis) v15.1.
- Updates to Gitmoji, FontAwesome and NerdFonts.

# [6.1.0]
## Added
- Support [fuzzel](https://codeberg.org/dnkl/fuzzel).
- `~` is expanded for `--files`. (#136)

## Changed
- Emoji presentation is forced for emoji with default text presentation. (#142)
- Updates to Gitmoji, NerdFonts and FontAwesome.

## Fixed
- Restored compatibility with Python 3.8. (#137)
- Fixed regression that ignored `--no-frecency`. (#138)
- Fixed skin tone selection in rofi mode. (#143)
- Fix version display. (#139)

# [6.0.0]
## Added
- You can now select your desired actions through a separate menu.
- Support for grid themes using `--hidden-descriptions` and [`contrib/grid.rasi`](https://github.com/fdw/rofimoji/blob/main/src/picker/contrib/grid.rasi). (#133)

## Changed
- `rofimoji` uses [Poetry](https://python-poetry.org/) for package management. With this comes the requirement for Python 3.8.
- `--files` supports globbing, so you can ask for `--files "linear_b*"`
- The emoji file is split into several files for one category each. (#126)
- Lots of character updates:
  - Emojis are now v15
  - FontAwesome is 6.2.0
  - NerdFonts are 2.2.2
  - Gitmoji is 3.13.0

# [5.6.0]
## Changed
- Remove the unexpected and distracting empty checkboxes from rofi. (#127, #125)

# [5.5.0]
## Added
- Gitmoji and Font Awesome 6 are now also included. (#114, #121)

## Fixed
- Choosing whitespace does not break `rofimoji` anymore. (#117)

# [5.4.0]
## Added
- `rofmoji`'s predefined characters now also contain all of CJK.
- Default characters and descriptions can be extended with custom files.
- You can now specify multiple actions for the same call.

## Changed
- Updated to Unicode v14!
- Since characters are now sorted by usage frecency, they shouldn't be sorted according to the search anymore. (#110)

## Fixed
- The shortcut for `all` files can now be combined with custom files. (#101)

# [5.3.0]
## Added
- Characters are now ordered according to their usage. (#74)

## Changed
- Recently used characters are now also re-ordered on usage. (#97)

# [5.2.0]
## Added
- The keybindings for direct actions are now configurable. (#84)
- `rofimoji` is now also on [PyPI](https://pypi.org/project/rofimoji/)

## Changed
- The `--rofi-args` parameter is now deprecated in favor of a more generic `--selector-args`. It still works, but it will be removed in a later release.

## Fixed
- The recents file will not grow limitless anymore. (#86)
- The skin tone selection was calling `rofi` even if `wofi` was preferred.
- `wofi` is now called with the correct arguments to work as expected now. (#89)

# [5.1.0]
## Added
- There is a new `print` action to just print out the characters. (#75)

## Fixed
- `xclip` is called correctly. (#79)

# [5.0.0]
## Added
- `rofimoji` can now be called as a modus from rofi! (#44)
- rofimoji now also works with [wofi](https://hg.sr.ht/~scoopta/wofi/). (#53)
- `rofimoji` now has a manpage. (#57)
- There's a new file for [Nerd Font icons](https://www.nerdfonts.com/).

## Changed
- The emojis from 13.1 have been added!
- Instead of several parameters to choose the input method, they have been consolidated into `--action` (`-a`).
- The annotations on emojis don't contain their name. (#59)
- The results are now sorted by rofi, by default based on Levenshtein distance. (#59)
- All entries are now forced to be left aligned, even for right-to-left languages. (#62)
- The dependency on `pyxdg` was removed.
- Some code cleanup. (#56, #58)

# [4.3.0]
## Added
- Added support for Wayland! (#47)
- Added support for `xclip`. (#21)
- You can type and copy the unicode codepoints. (#48)

## Changed
- The order of the characters in all scripts is now the same as the official one.
- All character data has been updated.

# [4.2.0]
## Added
- The most recently characters are now shown in a separate strip and can be selected with shortcuts (`alt+1` etc). (#39)

## Fixed
- Human emojis can now have their own skin tone even if they're part of a larger sequence. (#41)

# [4.1.1]
## Fixed
- Whitespace characters can be inserted.

# [4.1.0]
## Changed
- The extractors have been rewritten: There are now many, *many* supported symbols (all that Unicode offers), but some may have been renamed.

## Added
- A new file for all kinds of maths symbols.

# [4.0.0]
## Changed
- The new emojis from v13.0 are here!
- `rofimoji` is now modular and has an actual `setup.py`, as the emojis are no longer part of the picker code.
- The arguments to insert using the clipboard have been renamed: `--insert-with-clipboard` and `-p`

## Added
- You can ask `rofimoji` to only ever copy the emojis to the clipboard with `--copy-only` (`-c`).
- There are now data files for all of Unicode's scripts.
- A configuration can also be stored in `$XDG_CONFIG_HOME/rofimoji.rc`.

# [3.0.1]
## Fixed
- A race condition with Firefox is now resolved (#23).

# [3.0.0]
## Added
- You can choose a new input method: `rofimoji` can copy your emojis, paste them into the application and restore the previous contents.
- There are now more keywords included so you can find the appropriate emoji more easily.
- You can select a skin tone by default using cli args.
- You can pass arguments to rofi using `--rofi-args`.
- And you can use alternative emoji lists when you provide the `--emoji-file` parameter.

# [2.1.0]
## Changed
- This release is based on the emoji v12, including all these: https://unicode.org/emoji/charts/emoji-versions.html#2019 .
- Renamed meta files to upper case for better visibility.
- Updated dev dependencies to new versions.

# [2.0.1]
## Fixed
- Fix bug when trying to copy multiple emojis. (#6)

# [2.0.0]
## Changed
- Download emoji list from https://unicode.org/emoji/charts-11.0/full-emoji-list.html instead of emojipedia, as that one didn't work at all anymore.
- Skin color selection is now a second step after certain ("human") emojis. Only the neutral version is included in the main list, which accordingly is a lot smaller now.

## Added
- Downloading, parsing and extracting emoji properties from https://unicode.org/Public/emoji//11.0/emoji-data.txt so that we can find "human" emojis for skin color selection.
- A changelog 😁

