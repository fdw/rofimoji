# Rofimoji: A character picker for rofi
How often did you want to insert one of those Unicode emoji only to learn that there is no nice picker for Linux?
Fear no more, this script uses the power of [rofi](https://github.com/DaveDavenport/rofi/) to present exactly the picker you always wanted.
Insert the selected emoji directly, or copy it to the clipboard.
And you can use it to pick any weird character someone got into Unicode, too.

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
For some applications, `xdotool` cannot type emojis (f.e. Firefox).
To work around this, `rofimoji` can copy the emojis to your clipboard and insert them from there with `shift+insert`.
Afterwards, it will restore the previous contents.
Unfortunately, it depends on the receiving application whether `shift+insert` uses the clipboard or the primary selection.
Therefore, `rofimoji` uses both and also restores both.

By default, `rofimoji` uses `xdotool type`.
To choose to spam your clipboards, you can either use the keybinding `alt+p` or start it as `rofimoji --insert-with-clipboard` (`-p`).
If you want to use typing, you can hit `alt+t`, even though it was started with `--insert-with-clipboard`.

## Configuration
You can configure `rofimoji` either with cli arguments or with a config file called `$XDG_CONFIG_HOME/rofimoji.rc`. For the file, use the long option names without double dashes.

### Options

| long option | short option | possible values | description |
| --- | --- | --- | --- |
| `--skin-tone` | `-s` | `light`, `medium-light`, `moderate`, `dark brown`, `black`, as well as `neutral` and `ask` | Define the skin tone of supporting emojis. `ask` will always ask the user. |
| `--rofi-args` | | | Define arguments that `rofimoji` will pass through to `rofi`. |
| `--files` | `-f` | `emojis`, `arabic`, `arabic-indic`, `armenian`, `balinese`, `bamum`, `bengali`, `bopomofo`, `brahmi`, `braille`, `cherokee`, `coptic`, `cuneiform`, `cypriot`, `cyrillic`, `devanagari`, `egyptian`, `ethiopic`, `georgian`, `glagolitic`, `grantha`, `greek`, `gujarati`, `gurmukhi`, `hangul`, `hebrew`, `hiragana`, `kannada`, `katakana`, `khmer`, `latin`, `malayalam`, `miao`, `mongolian`, `myanmar`, `samaritan`, `sharada`, `signwriting`, `sinhala`, `tangut`, `telugu`, `tibetan`, `vai`, `yi` or your file | Define which file(s) to load characters from. You can define your own files, or use any of the default ones.<br/>If no file is set, the default emoji list is used. |
| `--insert-with-clipboard` | `-p` | | Insert the selected emoji through pasting from the clipboard, instead of directly typing them. See [Insertion Method](#insertion-method). |
| `--copy-only` | `-c` | | Only copy the selected characters to the clipboard without typing them. |

### Example config file
`~/.config/rofimoji.rc`:
```
insert-with-clipboard = false
files = [emojis, hebrew]
skin-tone = moderate
```

## Installation

### Arch
A kind soul has packaged it as [rofimoji](https://www.archlinux.org/packages/community/any/rofimoji/). To, install, use `sudo pacman -Syu rofimoji`.

### From sources
Download/clone the repository and call `python setup.py install` (with `--user` if you want to install it only for your user).
This also installs the python dependencies `xdg` and `configargparse`.

### Dependencies
What else do you need:
- Python 3
- A font that can display your scripts, (for emojis, [EmojiOne](https://github.com/emojione/emojione) or [Noto Emoji](https://www.google.com/get/noto/) work)
- xdotool for typing the emoji
- xsel to copy the emoji to the clipboard

For Ubuntu zesty: `sudo aptitude install fonts-emojione python3 rofi xdotool xsel` \
For Arch: `sudo pacman -Syu emoji-font python rofi xdotool xsel`

## Updating the emojis
This is only needed if a new Unicode version came out and you can't wait for the official update!

1. Install Python 3 and `pip install -r requirements.txt` in the `extractors` directory.
2. Run `extract_emojis.py` - this downloads the complete list from https://unicode.org/emoji/charts-12.0/full-emoji-list.html, so don't do it too often!
3. The new `emojis.csv` should have been created. You might need to install `rofimoji` again.
