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

