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
   `alt+t` or `alt+p` can be used to select a specific input method \
   `alt+1` inserts the most recently used character (`alt+2` for the second most recently one etc.) \
   `alt+u` inserts the Unicode codepoint, `alt+i` copies it to the clipboard
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

## Most recently used characters
By default, `rofimoji` will show the last ten recently used characters separately; you can insert them with `alt+1`, `alt+2` and so on. It will use the default [insertion Method](#insertion-method).
If you don't want this, you can set `--max=recent` to `0`.

The characters are saved in `$XDG_DATA_HOME/rofimoji/recent`.

## Display Server Support
`rofimoji` supports both X11 and Wayland by using either `xsel`/`xclip` and `xdotool` on X11 or `wl-copy` and `wtype` on Wayland. It chooses automatically the right one for the currently running session.
If you want to manually overwrite this, have a look at the `--clipboarder` and `--typer` options [below](#options).

## Configuration
You can configure `rofimoji` either with cli arguments or with a config file called `$XDG_CONFIG_HOME/rofimoji.rc`. For the file, use the long option names without double dashes.

### Options

| long option | short option | possible values | description |
| --- | --- | --- | --- |
| `--skin-tone` | `-s` | `light`, `medium-light`, `moderate`, `dark brown`, `black`, as well as `neutral` and `ask` | Define the skin tone of supporting emojis. `ask` will always ask the user. |
| `--prompt` | `-r` | any string | Define the prompt text for `rofimoji`. |
| `--rofi-args` | | | Define arguments that `rofimoji` will pass through to `rofi`.<br/>Please note that you need to specify it as `--rofi-args="<rofi-args>"` or `--rofi-args " <rofi-args>"` because of a [bug in argparse](https://bugs.python.org/issue9334) |
| `--files` | `-f` | `all`, `<yourfile>` or [any of the files in `data`](https://github.com/fdw/rofimoji/tree/master/picker/data)| Define which file(s) to load characters from. You can define your own files, or use any of the default ones.<br/>If set to `all`, all default files are used. Use with caution, that is a *lot*.<br/>If no file is set, the default emoji list is used. |
| `--insert-with-clipboard` | `-p` | | Insert the selected emoji through pasting from the clipboard, instead of directly typing them. See [Insertion Method](#insertion-method). |
| `--copy-only` | `-c` | | Only copy the selected characters to the clipboard without typing them. |
| `--max-recent` |  | 1-10 | Show at most this many recently picked characters. The number will be capped at 10. |
| `--clipboarder` | | `xsel`, `xclip`, `wl-copy` | Access the clipboard with this application. |
| `--typer` | | `xdotool`, `wtype` | Type the characters using this application. |

### Example config file
`~/.config/rofimoji.rc`:
```
insert-with-clipboard = false
files = [emojis, hebrew]
skin-tone = moderate
```

## Custom character files
You can define additional character files and load them with `-f` (see [options](#options)). In each line, one 'character' can be defined, followed by a single space character (` `). After that, you can write whatever description you want.

If you think your file is useful to others, you can open a PR to include it in future versions of `rofimoji`.

## Installation

### Arch
A kind soul has packaged it as [rofimoji](https://www.archlinux.org/packages/community/any/rofimoji/). To, install, use `sudo pacman -Syu rofimoji`.

### From sources
Download the wheel file from releases and install it with  `sudo pip install $filename` (or you can use `pip install --user $filename` to only install it for the local user).
Afterwards, there should be a `rofimoji` on your `$path`.
This also installs the python dependencies `xdg` and `configargparse`.

### Dependencies
What else do you need:
- Python 3.7 or higher
- A font that can display your scripts, (for emojis, [EmojiOne](https://github.com/emojione/emojione) or [Noto Emoji](https://www.google.com/get/noto/) work)
- A tool to programmatically type characters into applications. Either `xdotool` for X11 or `wtype` for Wayland
- A tool to copy the characters to the clipboard. `xsel` and `xclip` work on X11; `wl-copy` on Wayland

#### Examples for X11
For Ubuntu focal: `sudo aptitude install fonts-emojione python3 rofi xdotool xsel` \
For Arch: `sudo pacman -Syu emoji-font python rofi xdotool xsel`

## Updating the emojis
If you really, really need to update the characters and cannot wait for the official update:

1. Install Python 3 and `pip install -r requirements.txt` in the `extractors` directory.
2. Still in the `extraactors` directory, run `python main.py`: This downloads several large lists from [unicode.org](https://unicode.org), so please don't do it too often!
3. The data files should have been updated. You probably need to install `rofimoji` again from source.
