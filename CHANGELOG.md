# [4.3.0]
## Added
- Added support for Wayland! (#47)
- Added support for `xclip` (#21)
- You can type and copy the unicode codepoints (#48)

# [4.2.0]
## Added
- The most recently characters are now shown in a separate strip and can be selected with shortcuts (`alt+1` etc). (#39)

## Fixed
- Human emojis can now have their own skin tone even if they're part of a larger sequence (#41)

# [4.1.1]
## Fixed
- Whitespace characters can be inserted

# [4.1.0]
## Changed
- The extractors have been rewritten: There are now many, *many* supported symbols (all that Unicode offers), but some may have been renamed.

## Added
- A new file for all kinds of maths symbols

# [4.0.0]
## Changed
- `rofimoji` is now modular and has an actual `setup.py`, as the emojis are no longer part of the picker code.
- The arguments to insert using the clipboard have been renamed: `--insert-with-clipboard` and `-p`

## Added
- You can ask `rofimoji` to only ever copy the emojis to the clipboard with `--copy-only` (`-c`)
- There are now data files for all of Unicode's scripts.
- A configuration can also be stored in `$XDG_CONFIG_HOME/rofimoji.rc`.

# [3.0.1]
## Fixed
- @chmduquesne fixed a race condition with Firefox (#23)

# [3.0.0]
## Added
- You can choose a new input method: `rofimoji` can copy your emojis, paste them into the application and restore the previous contents
- There are now more keywords included so you can find the appropriate emoji more easily
- You can select a skin tone by default using cli args
- You can pass arguments to rofi using `--rofi-args`
- And you can use alternative emoji lists when you provide the `--emoji-file` parameter

# [2.1.0]
## Changed
- This release is based on the emoji v12, including all these: https://unicode.org/emoji/charts/emoji-versions.html#2019
- Renamed meta files to upper case for better visibility
- Updated dev dependencies to new versions

# [2.0.1]
## Fixed
- Fix bug when trying to copy multiple emojis. (#6)

# [2.0.0]
## Changed
- Download emoji list from https://unicode.org/emoji/charts-11.0/full-emoji-list.html instead of emojipedia, as that one didn't work at all anymore
- Skin color selection is now a second step after certain ("human") emojis. Only the neutral version is included in the main list, which accordingly is a lot smaller now.

## Added
- Downloading, parsing and extracting emoji properties from https://unicode.org/Public/emoji//11.0/emoji-data.txt so that we can find "human" emojis for skin color selection
- A changelog 😁

