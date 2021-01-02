# Rofimoji: A character picker for rofi
How often did you want to insert one of those Unicode emoji only to learn that there is no nice picker for Linux?
Fear no more, this script uses the power of [rofi](https://github.com/DaveDavenport/rofi/) (and other dmenu-derivatives like [wofi](https://hg.sr.ht/~scoopta/wofi)) to present exactly the picker you always wanted.
Insert the selected emoji directly, or copy it to the clipboard.
And you can use it to pick any weird character someone got into Unicode, too.

## How does it look?
![Screenshot of rofimoji](screenshot.png?raw=true)

## Usage
### Standalone
1. Run `rofimoji.py`
2. Search for the character you want
3. (optional) Select multiple emoji with `shift+enter`
4. Hit `enter` to insert the emoji directly \
   Hit `alt+c` to copy it to the clipboard \
   `alt+t` or `alt+p` can be used to select a specific input method \
   `alt+1` inserts the most recently used character (`alt+2` for the second most recently one etc.) \
   `alt+u` inserts the Unicode codepoint, `alt+i` copies it to the clipboard
5. Maybe select a skin color
6. 🎠

### As a rofi "mode"
1. Call rofi with `rofi -modi "emoji:<path to rofimoji.py>" -show emoji`
2. Search for the character you want
3. Hit `enter` to exexute your default action; \
   `Alt+Shift+1` for copying to the clipboard
   `Alt+Shift+3` for the "[clipboard](#insertion-method)" insertion method
   `alt+1` inserts the most recently used character (`alt+2` for the second most recently one etc.)
4. Maybe select a skin color
5. 🐉

## Insertion method
By default, `rofimoji` types the characters using either `xdotool` or `wtype` (see [Display server support](#display-server-support)). You can enforce this behavior with `--action type` (`-a type`).

For some applications (f.e. Firefox), this does not work. To work around this, `rofimoji` can copy the emojis to your clipboard and insert them from there with `shift+insert`. Afterwards, it will restore the previous contents.
Unfortunately, it depends on the receiving application whether `shift+insert` uses the clipboard or the primary selection.
Therefore, `rofimoji` uses both and also restores both.
To choose to spam your clipboards, you can either use the keybinding `alt+p` or start it as `rofimoji --action clipboard` (`-a clipboard`).
If you want to use typing, you can hit `alt+t`, even though it was started with `--action clipboard`.

Finally, with `--action copy` (or `-a copy`) you can also tell `rofimoji` to only copy the selected characters to your clipboard.

## Display server support
`rofimoji` supports both X11 and Wayland by using either `rofi`, `xsel`/`xclip` and `xdotool` on X11 or `wofi` (or some adapted `rofi`), `wl-copy` and `wtype` on Wayland. It chooses automatically the right one for the currently running session.
If you want to manually overwrite this, have a look at the `--selector`, `--clipboarder` and `--typer` options [below](#options).

Please note that `wofi` does not support custom keyboard shortcuts or recent files at the moment.

## Most recently used characters
By default, `rofimoji` will show the last ten recently used characters separately; you can insert them with `alt+1`, `alt+2` and so on. It will use the default [insertion Method](#insertion-method).
If you don't want this, you can set `--max=recent` to `0`.

The characters are saved in `$XDG_DATA_HOME/rofimoji/recent`.

## Configuration
You can configure `rofimoji` either with cli arguments or with a config file called `$XDG_CONFIG_HOME/rofimoji.rc`. For the file, use the long option names without double dashes.

### Options

| long option | short option | possible values | description |
| --- | --- | --- | --- |
| `--action` | `-a` | `type`, `copy`, `clipboard` | Chose what `rofimoji` should do with the selected characters. See [Insertion Method](#insertion-method).<br/>`type`: Directly type the characters into the last active window.<br/>`copy`: Copy them to the clipboard.<br/>`clipboard`: Insert the selected emoji through pasting from the clipboard, instead of directly typing them.  |
| `--files` | `-f` | `all`, `<yourfile>` or [any of the files in `data`](https://github.com/fdw/rofimoji/tree/master/picker/data)| Define which file(s) to load characters from. You can define your own files, or use any of the default ones.<br/>If set to `all`, all default files are used. Use with caution, that is a *lot*.<br/>If no file is set, the default emoji list is used. |
| `--skin-tone` | `-s` | `light`, `medium-light`, `moderate`, `dark brown`, `black`, as well as `neutral` and `ask` | Define the skin tone of supporting emojis. `ask` will always ask the user. |
| `--max-recent` |  | 1-10 | Show at most this many recently picked characters. The number will be capped at 10. |
| `--prompt` | `-r` | any string | Define the prompt text for `rofimoji`. |
| `--rofi-args` | | | Define arguments that `rofimoji` will pass through to `rofi`.<br/>Please note that you need to specify it as `--rofi-args="<rofi-args>"` or `--rofi-args " <rofi-args>"` because of a [bug in argparse](https://bugs.python.org/issue9334) |
| `--selector` | | `rofi`, `wofi` | Show the selection dialog with this application. |
| `--clipboarder` | | `xsel`, `xclip`, `wl-copy` | Access the clipboard with this application. |
| `--typer` | | `xdotool`, `wtype` | Type the characters using this application. |

### Example config file
`~/.config/rofimoji.rc`:
```
action = copy
files = [emojis, hebrew]
skin-tone = moderate
```

## Custom character files
You can define additional character files and load them with `-f` (see [options](#options)). In each line, one 'character' can be defined, followed by a single space character (` `). After that, you can write whatever description you want.

If you think your file is useful to others, please open a PR to include it in a future version of `rofimoji`.

## Caveats when running `rofimoji` as a rofi "mode"
Running as rofi mode has several drawbacks that cannot be changed:
- Because `rofi` is the main process, `rofimoji` cannot directly type to any window. Only copying the character works, so set the `--action` accordingly.
- You can only select one character at a time.
- The custom keyboard shortcuts are still there, but mapped to `Alt+Shift+1` (on a Qwerty keyboard) etc.

The configuration still works as described. You can have several modes in a `combi` for different character sets, for example, or set a default action and skin tone.

## Installation

### Arch
A kind soul has packaged it as [rofimoji](https://www.archlinux.org/packages/community/any/rofimoji/). To, install, use `sudo pacman -Syu rofimoji`.

### From sources
Download the wheel file from releases and install it with  `sudo pip install $filename` (or you can use `pip install --user $filename` to only install it for the local user).
Afterwards, there should be a `rofimoji` on your `$path`.
This also installs the python dependency `configargparse`.

### Dependencies
What else do you need:
- Python 3.7 or higher
- A font that can display your scripts, (for emojis, [EmojiOne](https://github.com/emojione/emojione) or [Noto Emoji](https://www.google.com/get/noto/) work)
- `rofi` or `wofi`
- A tool to programmatically type characters into applications. Either `xdotool` for X11 or `wtype` for Wayland
- A tool to copy the characters to the clipboard. `xsel` and `xclip` work on X11; `wl-copy` on Wayland

#### Examples for X11
For Ubuntu focal: `sudo aptitude install fonts-emojione python3 rofi xdotool xsel` \
For Arch: `sudo pacman -Syu emoji-font python rofi xdotool xsel`

## Updating the characters
If you really, really need to update the characters and cannot wait for the official update:

1. Install Python 3 and `pip install -r requirements.txt` in the `extractors` directory.
2. Still in the `extraactors` directory, run `python main.py`: This downloads several large lists from [unicode.org](https://unicode.org), so please don't do it too often!
3. The data files should have been updated. You probably need to install `rofimoji` again from source.
