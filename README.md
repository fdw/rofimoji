# Rofimoji: A character picker for rofi
Do you want to use one of those fancy emojis? Or one of those other interesting characters Unicode offers? But you haven't found a good picker yet?

Fear no more, `rofimoji` invokes the power of [rofi](https://github.com/DaveDavenport/rofi/) (and [other dmenu-derivatives](#supported-selectors)) to give you exactly the picker you always wanted.

## Main features
- Insert the select character directly, or copy it to the clipboard.
- Characters (and especially emojis) are fuzzy-searchable with keywords.
- [It remembers the ones you use most and presents them first.](#most-recently-used-characters)
- Emojis by default, but you can have any Unicode block you want - you can even [use your own](#custom-character-files-and-descriptions)!

## How does it look?
### Default
![Screenshot of rofimoji](screenshot.png?raw=true)

### With a [grid theme](#rofi-theming)
![Screenshot of rofimoji with a grid theme](screenshot-grid.png?raw=true)


# Usage
## Standalone
Call `rofimoji` as a standalone tool.

1. Run `rofimoji`
2. Search for the character you want
3. (optional) Select multiple emoji with `shift+enter`
4. Hit `enter` to for the default action or use one of the [shortcuts](#actions) to do something else.\
   `alt+1` directly chooses the most most recently used character (`alt+2` for the second most recently one etc.)
5. Maybe select a skin color
6. 🦾

## As a rofi mode
Integrate `rofimoji` as just another rofi mode.

1. Call rofi with `rofi -modi "emoji:rofimoji" -show emoji`
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

| long option                                                                                                             | short option | possible values                                                                                                | default value                               | description                                                                                                                                                                                                                                                                                                         |
|-------------------------------------------------------------------------------------------------------------------------|--------------|----------------------------------------------------------------------------------------------------------------|---------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `--action`                                                                                                              | `-a`         | `type`, `copy`, `clipboard`, `unicode`, `copy-unicode`, `print`, `menu`                                        | `type`                                      | Choose what `rofimoji` should do with the selected characters. See [Actions](#actions) below for details.                                                                                                                                                                                                           |
| `--files`                                                                                                               | `-f`         | `all`, `<yourfile>` or [any of the files in `data`](https://github.com/fdw/rofimoji/tree/main/src/picker/data) | `emojis`                                    | Define which file(s) to load characters from. A file name without extension (f.e. `emojis_smileys_emotion`) is enough for the distributed ones or any in `${XDG_DATA_HOME}/rofimoji/data`. Globbing with `*` is possible.<br/>`all` is a shortcut for all default files at once. Use with caution, that is a *lot*. |
| `--skin-tone`                                                                                                           | `-s`         | `light`, `medium-light`, `moderate`, `dark brown`, `black`, as well as `neutral` and `ask`                     | `ask`                                       | Define the skin tone of supporting emojis. `ask` will always ask the user.                                                                                                                                                                                                                                          |
| `--max-recent`                                                                                                          |              | 0-10                                                                                                           | 10                                          | Show at most this many recently picked characters. The number will be capped at 10. Set to `0` to disable the whole feature.                                                                                                                                                                                        |
| `--no-frecency`<br/>(`no-frecency=True` in the config file)                                                             |              | -                                                                                                              | `<false>`                                   | By default, `rofimoji` shows frequently used items first. With this option, they're shown in the order of the file.                                                                                                                                                                                                 |
| `--hidden-descriptions`<br/>(`hidden-descriptions=True` in the config file)                                             |              | -                                                                                                              | `<false>`                                   | Only list the characters, but not their description. This is useful for [grid themes](#rofi-theming) in `rofi`. Note that they're still searchable, even though the description is not shown. Not used with other selectors.                                                                                        |
| `--use-icons`                                                                                                           |              |                                                                                                                | `false`                                     | Show characters as icons in `rofi`. Not used for other selectors.                                                                                                                                                                                                                                                   |
| `--prompt`                                                                                                              | `-r`         | any string                                                                                                     | `😀 `                                       | Define the prompt text for `rofimoji`.                                                                                                                                                                                                                                                                              |
| `--selector-args`                                                                                                       |              |                                                                                                                |                                             | Define arguments that `rofimoji` will pass through to the selector.<br/>Please note that you need to specify it as `--selector-args="<selector-args>"` or `--selector-args " <selector-args>"` because of a [bug in argparse](https://bugs.python.org/issue9334)                                                    |
| `--selector`                                                                                                            |              | `rofi`, `wofi`, `fuzzel`, `dmenu`, `tofi`, `bemenu`, `wmenu`                                                   | (automatically chosen)                      | Show the selection dialog with this application.                                                                                                                                                                                                                                                                    |
| `--clipboarder`                                                                                                         |              | `xsel`, `xclip`, `wl-copy`                                                                                     | (automatically chosen)                      | Access the clipboard with this application.                                                                                                                                                                                                                                                                         |
| `--typer`                                                                                                               |              | `xdotool`, `wtype`                                                                                             | (automatically chosen)                      | Type the characters using this application.                                                                                                                                                                                                                                                                         |
| `--keybinding-copy`, `--keybinding-type`, `--keybinding-clipboard`, `--keybinding-unicode`, `--keybinding-copy-unicode` |              |                                                                                                                | `Alt+c`, `Alt+t`, `Alt+p`, `Alt+u`, `Alt+i` | Choose different keybindings than the default values.                                                                                                                                                                                                                                                               |

## Example config file
`~/.config/rofimoji.rc`:
```
action = copy
files = [emojis, math]
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

For some applications (f.e. Firefox), this does not work reliably. To work around this, `rofimoji` can copy the emojis to your clipboard and insert them from there with `shift+insert`. Afterwards, it will restore the previous contents.
Unfortunately, it depends on the receiving application whether `shift+insert` uses the clipboard or the primary selection.
Therefore, `rofimoji` uses both and also restores both.
To use this workaround, you can either use the keybinding `alt+p` or start it as `rofimoji --action clipboard` (`-a clipboard`).
If you want to have it directly typed instead, you can hit `alt+t`, even though it was started with `--action clipboard`. Note that you can [change the keybindings](#options).

Finally, with `--action copy` (or `-a copy`) you can also tell `rofimoji` to only copy the selected characters to your clipboard.

## Display server support
`rofimoji` supports both X11 and Wayland by using the correct tools for each environment (see [Supported Selectors](#supported-selectors)). It tries to automatically choose the right one for the currently running session.
If you want to manually overwrite this, have a look at the `--selector`, `--clipboarder` and `--typer` options [above](#options).

## Most recently used characters
By default, `rofimoji` will show the last ten recently used characters separately; you can insert them with `alt+1`, `alt+2` and so on. It will use the default [insertion method](#insertion-method).
If you don't want this, you can set `--max-recent` to `0`.

Additionally, `rofimoji` also remembers in general which characters are used more frequently and sorts the list accordingly. You can disable this behavior with `--no-frecency`.

## Rofi theming
By default, `rofimoji` re-uses the existing rofi configuration, but you can pass your own using `--selector-args` (for example `--selector-args="-theme ~/your-rofi-theme.rasi"`).

If you would like a more character-focused theme, you can use packaged [`grid.rasi`](https://github.com/fdw/rofimoji/blob/main/src/picker/contrib/grid.rasi) together with the `--hidden-descriptions` parameter. This theme still imports the existing `rofi` configuration but moves the entries into a grid. Of course, you can base your own theme on this. (If you have improvements, please open a PR!)
To use the arrow keys in `rofi` only for the grid and not the query, pass these `-selector-args`: `-kb-row-left Left -kb-row-right Right -kb-move-char-back Control+b -kb-move-char-forward Control+f`.

![Screenshot of rofimoji with a grid theme](screenshot-grid.png?raw=true)

# Supported characters
- [Unicode emojis](https://home.unicode.org/emoji/about-emoji/) with the official descriptions and tags. Also supports skin tones and gender variants.
- All other [Unicode](https://home.unicode.org/) characters, split into the official blocks
- CJK character sets from Unicode
- [Font Awesome 6](https://fontawesome.com/)
- [Nerd Fonts](https://www.nerdfonts.com/)
- [Gitmoji](https://gitmoji.dev/)
- Kaomoji, from [w33ble](https://github.com/w33ble/emoticon-data)

If you miss something, please open an issue!

## Custom character files and descriptions
If the predefined ones are not enough, you can define additional character files and load them with `-f` (see [options](#options)). In each line, one 'character' can be defined, followed by a single space character (` `). After that, you can write whatever description you want.

If the character is also in another selected file, all descriptions will be combined. If you give it the same name as one of those included with `rofimoji`, yours will be preferred.

For added comfort, `rofimoji` will automatically load an "additional" file for predefined ones. This file needs to called `<filename>.additional.csv` and lie in `${XDG_DATA_DIR}/rofimoji/data/`. For example, if you want to extend `emojis_smileys_emotion`, call the file `emojis_smileys_emotions.additional.csv`. This is helpful if you want additional descriptions: You can define such an additional character file, add the character and your description and your descriptions will now also be shown.

If you think your file is useful to others, please open a PR to include it in a future version of `rofimoji`.

# Installation
## From distribution repositories
[![Packaging status](https://repology.org/badge/vertical-allrepos/rofimoji.svg)](https://repology.org/project/rofimoji/versions)

## From PyPI
`rofimoji` is on [PyPI](https://pypi.org/project/rofimoji/). You can install it with `pipx install rofimoji` (or `sudo pipx install rofimoji`).

## From Github
Download the wheel file of the [latest release](https://github.com/fdw/rofimoji/releases/) and install it with  `sudo pip install $filename` (or you can use `pip install --user $filename` to only install it for the local user).
Afterwards, there should be a `rofimoji` on your `$PATH`.
This also installs the python dependency `configargparse`.

## Dependencies
What else do you need:
- Python 3.8 or higher
- A font that can display your scripts, (for emojis, [EmojiOne](https://github.com/emojione/emojione) or [Noto Emoji](https://www.google.com/get/noto/) work)
- Optionally, a tool to programmatically type characters into applications. Either `xdotool` for X11 or `wtype` for Wayland
- Optionally, a tool to copy the characters to the clipboard. `xsel` and `xclip` work on X11; `wl-copy` on Wayland

### Supported Selectors
Please note that only `rofi` (both on X and Wayland) supports custom keyboard shortcuts, recent files or a grid theme at the moment. For all others, only basic functionality works.

#### X.org
- [rofi](https://github.com/davatorium/rofi)
- [bemenu](https://github.com/Cloudef/bemenu)
- [dmenu](https://tools.suckless.org/dmenu/)

#### Wayland
- [rofi fork for Wayland](https://github.com/lbonn/rofi)
- [wofi](https://hg.sr.ht/~scoopta/wofi)
- [fuzzel](https://codeberg.org/dnkl/fuzzel)
- [tofi](https://github.com/philj56/tofi)
- [bemenu](https://github.com/Cloudef/bemenu)
- [wmenu](https://git.sr.ht/~adnano/wmenu)
