# Emoji-Picker

How often did you want to insert one of those Unicode emoji only to learn that there is no nice picker for Linux?
Fear no more, this script uses the power of [rofi](https://github.com/DaveDavenport/rofi/) to present exactly the picker you always wanted.
Inserts the selected emoji directly, or copies it to the clipboard.

## Usage

1. Run `rofimoji.py`
2. Search for the emoji you want
3. - Hit enter to insert the emoji directly
   - Hit `Alt+c` to copy it to the clipboard
4. 🎠

## Installation

Download `rofimoji.py` and move it somewhere on your path, for example `/usr/local/bin`.
Make sure you have Python 3 and a font that can display emoji (like [EmojiOne](https://github.com/emojione/emojione) or [Noto Emoji](https://www.google.com/get/noto/))

Additional dependencies:
- xdotool (X11 command-line automation tool)

## Updating the emojis

This is only needed if a new Unicode version came out and you can't wait for the official update!

1. Install Python 3 and `pip install -r requirements-dev.txt`
2. Run `extract_emojis.py` - this downloads the complete list from https://emojipedia.org/emoji/, so don't do it too often!
3. A new file `emojis.py` should have been created. Open it and copy the contents
4. Open `rofimoji.py` and replace the emoji list with the contents of `emojis.py`

## FAQ

### Why is it so pedestrian? Why not simple import from `emojis.py`?
Because now you only have to download one file, and it works 
Additionally, we need no separate I/O just to load the emojis. This is good, right?
