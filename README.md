# Emoji-Picker
How often did you want to insert one of those Unicode emoji only to learn that there is no nice picker for Linux?
Fear no more, this script uses the power of [rofi](https://github.com/DaveDavenport/rofi/) to present exactly the picker you always wanted.
Inserts the selected emoji directly, or copies it to the clipboard.

## Usage
1. Run `rofimoji.py`
2. Search for the emoji you want
3. (optional) Select multiple emoji with `shift+enter`
4. Hit `enter` to insert the emoji directly \
   Hit `alt+c` to copy it to the clipboard
5. Maybe select a skin color
6. 🎠

## How does it look?
![Screenshot of rofimoji](screenshot.png?raw=true)

## Installation

### Arch
A kind soul has packaged it as [rofimoji](https://www.archlinux.org/packages/community/any/rofimoji/). To, install, use `sudo pacman -Syu rofimoji`.

#### AUR for Manjaro and others
If `rofimoji` is not yet synced to your distro's repo, you can also install [rofimoji-git](https://aur.archlinux.org/packages/rofimoji-git/) from the AUR.

### From sources
Download `rofimoji.py` and move it somewhere on your path, for example `/usr/local/bin`.

What else do you need:
- Python 3
- A font that can display emoji, for example [EmojiOne](https://github.com/emojione/emojione) or [Noto Emoji](https://www.google.com/get/noto/)
- xdotool for typing the emoji
- xsel to copy the emoji to the clipboard

For Ubuntu zesty: `sudo aptitude install fonts-emojione python3 rofi xdotool xsel` \
For Arch: `sudo pacman -Syu emoji-font python rofi xdotool xsel`

## Updating the emojis
This is only needed if a new Unicode version came out and you can't wait for the official update!

1. Install Python 3 and `pip install -r requirements-dev.txt`
2. Run `extract_emojis.py` - this downloads the complete list from https://unicode.org/emoji/charts-12.0/full-emoji-list.html, so don't do it too often!
3. A new file `emojis.py` should have been created. Open it and copy the contents
4. Open `rofimoji.py` and replace the emoji list with the contents of `emojis.py`

## FAQ

### Why is it so pedestrian? Why not simply import from `emojis.py`?
Because now you only have to download one file, and it works 
Additionally, we need no separate I/O just to load the emojis. This is good, right?
