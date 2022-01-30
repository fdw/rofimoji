# Rofimoji: A character picker for rofi
Do you want to use one of those fancy emojis? Or one of those other interesting characters Unicode offers? But you haven't found a good picker yet?

Fear no more, `rofimoji` invokes the power of [rofi](https://github.com/DaveDavenport/rofi/) (and other dmenu-derivatives like [wofi](https://hg.sr.ht/~scoopta/wofi)) to give you exactly the picker you always wanted.

## Main features
- Insert the select character directly, or copy it to the clipboard.
- Characters (and especially emojis) are fuzzy-searchable with keywords.
- [It remembers the ones you use most and presents them first.](#most-recently-used-characters)
- Emojis by default, but you can have any Unicode block you want - you can even [use your own](#custom-character-files-and-descriptions)!

## How does it look?
![Screenshot of rofimoji](screenshot.png?raw=true)

# Usage
## Standalone
Call `rofimoji` as a standalone tool.

1. Run `rofimoji.py`
2. Search for the character you want
3. (optional) Select multiple emoji with `shift+enter`
4. Hit `enter` to for the default action or use one of the [shortcuts](#actions) to do something else.\
   `alt+1` directly chooses the most most recently used character (`alt+2` for the second most recently one etc.)
5. Maybe select a skin color
6. 🎠

## As a rofi mode
Integrate `rofimoji` as just another rofi mode.

1. Call rofi with `rofi -modi "emoji:<path to rofimoji.py>" -show emoji`
2. Search for the character you want
3. Hit `enter` to execute your default action; \
   `Alt+Shift+1` for copying to the clipboard \
   `Alt+Shift+3` for the "[clipboard](#insertion-method)" insertion method \
   `alt+1` inserts the most recently used character (`alt+2` for the second most recently one etc.)
4. Maybe select a skin color
5. 🐉

### Caveats when running `rofimoji` as a rofi mode
There are some limitations to this approach, though:
Running as rofi mode has several drawbacks that cannot be changed:
- Because `rofi` is the main process, `rofimoji` cannot directly type to any window. Only copying the character works, so set the `--action` accordingly.
- You can only select one character at a time.
- The custom keyboard shortcuts are still there, but mapped to `Alt+Shift+1` (on a Qwerty keyboard) etc.

The configuration still works as described. You can have several modes in a `combi` for different character sets, for example, or set a default action and skin tone.

# Configuration
You can configure `rofimoji` either with cli arguments or with a config file called `$XDG_CONFIG_HOME/rofimoji.rc`. For the file, use the long option names without double dashes.

## Options

| long option                                                                                                             | short option | possible values                                                                                                | default value                               | description                                                                                                                                                                                                                                                                         |
|-------------------------------------------------------------------------------------------------------------------------|--------------|----------------------------------------------------------------------------------------------------------------|---------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `--action`                                                                                                              | `-a`         | `type`, `copy`, `clipboard`, `unicode`, `copy-unicode`, `print`                                                | `type`                                      | Choose what `rofimoji` should do with the selected characters. See [Actions](#actions) below for details.                                                                                                                                                                           |
| `--files`                                                                                                               | `-f`         | `all`, `<yourfile>` or [any of the files in `data`](https://github.com/fdw/rofimoji/tree/main/src/picker/data) | `emojis`                                    | Define which file(s) to load characters from. You can define your own files, or use any of the default ones.<br/>`all` is a shortcut for all default files at once. Use with caution, that is a *lot*.                                                                              |
| `--skin-tone`                                                                                                           | `-s`         | `light`, `medium-light`, `moderate`, `dark brown`, `black`, as well as `neutral` and `ask`                     | `ask`                                       | Define the skin tone of supporting emojis. `ask` will always ask the user.                                                                                                                                                                                                          |
| `--max-recent`                                                                                                          |              | 1-10                                                                                                           | 10                                          | Show at most this many recently picked characters. The number will be capped at 10.                                                                                                                                                                                                 |
| `--no-frecency`<br/>(`no-frecency=True` in the config file)                                                             |              | -                                                                                                              | `<false>`                                   | By default, `rofimoji` shows frequently used items first. With this option, they're shown in the order of the file.                                                                                                                                                                 |
| `--prompt`                                                                                                              | `-r`         | any string                                                                                                     | `😀 `                                       | Define the prompt text for `rofimoji`.                                                                                                                                                                                                                                              |
| `--selector-args`                                                                                                       |              |                                                                                                                |                                             | Define arguments that `rofimoji` will pass through to the selector (`rofi` or `wofi`).<br/>Please note that you need to specify it as `--selector-args="<selector-args>"` or `--selector-args " <selector-args>"` because of a [bug in argparse](https://bugs.python.org/issue9334) |
| `--selector`                                                                                                            |              | `rofi`, `wofi`                                                                                                 | (automatically chosen)                      | Show the selection dialog with this application.                                                                                                                                                                                                                                    |
| `--clipboarder`                                                                                                         |              | `xsel`, `xclip`, `wl-copy`                                                                                     | (automatically chosen)                      | Access the clipboard with this application.                                                                                                                                                                                                                                         |
| `--typer`                                                                                                               |              | `xdotool`, `wtype`                                                                                             | (automatically chosen)                      | Type the characters using this application.                                                                                                                                                                                                                                         |
| `--keybinding-copy`, `--keybinding-type`, `--keybinding-clipboard`, `--keybinding-unicode`, `--keybinding-copy-unicode` |              |                                                                                                                | `Alt+c`, `Alt+t`, `Alt+p`, `Alt+u`, `Alt+i` | Choose different keybindings than the default values.                                                                                                                                                                                                                               |

## Example config file
`~/.config/rofimoji.rc`:
```
action = copy
files = [emojis, hebrew]
skin-tone = moderate
```

## Actions

The `--action` (`-a`) option defines what action will be taken when a character is selected. Multiple actions can be specified with a space character in between (for example: `-a type copy`).
The options are:

| name           | shortcut | description                                                                                                                                    |
|----------------|----------|------------------------------------------------------------------------------------------------------------------------------------------------|
| `type`         | `alt+t`  | Directly type the characters into the last active window. This is the *default*                                                                |
| `copy`         | `alt+c`  | Copy them to the clipboard.                                                                                                                    |
| `clipboard`    | `alt+p`  | Insert the selected characters through pasting from the clipboard, instead of directly typing them. See [Insertion Method](#insertion-method). |
| `unicode`      | `alt+u`  | Type the unicode codepoints of the selected characters.                                                                                        |
| `copy-unicode` | `alt+i`  | Copy the codepoints to clipboard.                                                                                                              |
| `print`        |          | Print the chosen characters to `stdout`.                                                                                                       |

## Insertion method
By default, `rofimoji` types the characters using either `xdotool` or `wtype` (see [display server support](#display-server-support)). You can enforce this behavior with `--action type` (`-a type`).

For some applications (f.e. Firefox), this does not work. To work around this, `rofimoji` can copy the emojis to your clipboard and insert them from there with `shift+insert`. Afterwards, it will restore the previous contents.
Unfortunately, it depends on the receiving application whether `shift+insert` uses the clipboard or the primary selection.
Therefore, `rofimoji` uses both and also restores both.
To choose to spam your clipboards, you can either use the keybinding `alt+p` or start it as `rofimoji --action clipboard` (`-a clipboard`).
If you want to use typing, you can hit `alt+t`, even though it was started with `--action clipboard`. Note that you can [change the keybindings](#options).

Finally, with `--action copy` (or `-a copy`) you can also tell `rofimoji` to only copy the selected characters to your clipboard.

## Display server support
`rofimoji` supports both X11 and Wayland by using either `rofi`, `xsel`/`xclip` and `xdotool` on X11 or `wofi` (or some adapted `rofi`), `wl-copy` and `wtype` on Wayland. It chooses automatically the right one for the currently running session.
If you want to manually overwrite this, have a look at the `--selector`, `--clipboarder` and `--typer` options [above](#options).

Please note that `wofi` does not support custom keyboard shortcuts or recent files at the moment.

## Most recently used characters
By default, `rofimoji` will show the last ten recently used characters separately; you can insert them with `alt+1`, `alt+2` and so on. It will use the default [insertion method](#insertion-method).
If you don't want this, you can set `--max=recent` to `0`.

Additionally, `rofimoji` also remembers in general which characters are used more frequently and sorts the list accordingly. You can disable this behavior with `--no-frecency`.

## Supported characters
Obviously, `rofimoji` is mostly used for emojis. However, it also supports all (yes, all) other Unicode blocks, for example [mathematical symbols](https://github.com/fdw/rofimoji/blob/main/src/picker/data/math.csv), [Greek and Coptic](https://github.com/fdw/rofimoji/blob/main/src/picker/data/greek_and_coptic.csv) or [Linear B (Ideograms)](https://github.com/fdw/rofimoji/blob/main/src/picker/data/linear_b_ideograms.csv). Simply load them with `-f` (see [options](#options)).
If you miss something that should be there, please open an issue.

## Custom character files and descriptions
If the predefined ones are not enough, you can define additional character files and load them with `-f` (see [options](#options)). In each line, one 'character' can be defined, followed by a single space character (` `). After that, you can write whatever description you want.

If the character already exists, the new description will be appended. In other words, if you're not happy with the official descriptions, you can define a custom character file, add the character and your description, and this descriptions will now also be shown.

For added comfort, `rofimoji` will automatically load an "additional" file for predefined ones. This file needs to called `<filename>.additional.csv` and lie in `${XDG_DATA_DIR}/rofimoji/data/`. For example, if you want to extend `emojis`, call the file `emojis.additional.csv`.

If you think your file is useful to others, please open a PR to include it in a future version of `rofimoji`.

# Installation
## From distribution repositories
[![Packaging status](https://repology.org/badge/vertical-allrepos/rofimoji.svg)](https://repology.org/project/rofimoji/versions)

## From PyPI
`rofimoji` is on [PyPI](https://pypi.org/project/rofimoji/). You can install it with `pip install --user rofimoji` (or `sudo pip install rofimoji`).

## From Github
Download the wheel file of the [latest release](https://github.com/fdw/rofimoji/releases/) and install it with  `sudo pip install $filename` (or you can use `pip install --user $filename` to only install it for the local user).
Afterwards, there should be a `rofimoji` on your `$PATH`.
This also installs the python dependency `configargparse`.

## Dependencies
What else do you need:
- Python 3.7 or higher
- A font that can display your scripts, (for emojis, [EmojiOne](https://github.com/emojione/emojione) or [Noto Emoji](https://www.google.com/get/noto/) work)
- `rofi` (in version 1.6.0 or higher if you want to use the mode) or `wofi`
- A tool to programmatically type characters into applications. Either `xdotool` for X11 or `wtype` for Wayland
- A tool to copy the characters to the clipboard. `xsel` and `xclip` work on X11; `wl-copy` on Wayland

# Feedback
This project is driven by feedback from you! So, if you have an idea, a feature request or just want to say "thanks", open an issue, a discussion or give a star. Thank you so much 🙏
