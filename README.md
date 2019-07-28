# Emoji-Picker
How often did you want to insert one of those Unicode emoji only to learn that there is no nice picker for Linux?
Fear no more, this script uses the power of [rofi](https://github.com/DaveDavenport/rofi/) to present exactly the picker you always wanted.
Inserts the selected emoji directly, or copies it to the clipboard.

## Usage
1. Run `rofimoji.py`
2. Search for the emoji you want
3. (optional) Select multiple emoji with `shift+enter`
4. Hit `enter` to insert the emoji directly \
   Hit `alt+c` to copy it to the clipboard \
   `alt+t` or `alt+p` can be used to select a specific input method
5. Maybe select a skin color
6. 🎠

## How does it look?
![Screenshot of rofimoji](screenshot.png?raw=true)

## Insertion method
For some applications, `xdotool` cannot type emojis (f.e. Firefox). To work around this, `rofimoji` can copy the emojis to your clipboard and insert them from there with `shift+insert`. Afterwards, it will restore the previous contents.
Unfortunately, it depends on the receiving application whether `shift+insert` uses the clipboard or the primary selection. Therefore, `rofimoji` uses both and also restores both 😐.

By default, `rofimoji` uses `xdotool type`. To choose to spam your clipboards, you can either use the keybinding `alt+p` or start it as `rofimoji --use-clipboard` (`-c`). If you want to use typing, you can hit `alt+t`, even though it was started with `--use-clipboard`.

## Configuration
You can choose a skin tone with the `--skin-tone` (or `-s`) parameter. The available values are `light`, `medium-light`, `moderate`, `dark brown`, `black`, as well as `neutral` and `ask` to be shown the prompt (this is also the default).

If you have any arguments for rofi, you can make `rofimoji` pass them through like this: `rofimoji --rofi-args="-columns 3"`.

You can also define your own set of emojis (or whatever) and use `rofimoji` to pick them by providing the `--emoji-file` (`-f`) parameter. This could be helpful if you want them ordered in some way, only use a subset or if you want non-English descriptions.

## Installation

### Arch
A kind soul has packaged it as [rofimoji](https://www.archlinux.org/packages/community/any/rofimoji/). To, install, use `sudo pacman -Syu rofimoji`.

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
