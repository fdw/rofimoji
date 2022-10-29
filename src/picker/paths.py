import os
from pathlib import Path

config_home = Path(os.environ.get("XDG_CONFIG_HOME", "~/.config")).expanduser()
config_global = [Path(dir) for dir in os.environ.get("XDG_CONFIG_DIRS", "/etc/xdg").split(":")]
data_home = Path(os.environ.get("XDG_DATA_HOME", "~/.local/share")).expanduser()
cache_home = Path(os.environ.get("XDG_CACHE_HOME", "~/.cache")).expanduser()

config_file_locations = [str(directory / "rofimoji.rc") for directory in [config_home] + config_global]
recents_file_location = data_home / "rofimoji" / "recent"
frecency_file_location = data_home / "rofimoji" / "frecency"
custom_additional_files_location = data_home / "rofimoji" / "data"

cache_file_location = cache_home / "rofimoji"
