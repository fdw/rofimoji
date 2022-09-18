import os
from pathlib import Path

if "XDG_CONFIG_HOME" in os.environ:
    config_home = Path(os.environ.get("XDG_CONFIG_HOME"))
else:
    config_home = Path.home() / ".config"

if "XDG_CONFIG_DIRS" in os.environ:
    config_global = [Path(dir) for dir in os.environ.get("XDG_CONFIG_DIRS").split(":")]
else:
    config_global = [Path("/etc/xdg")]

config_file_locations = [str(directory / "rofimoji.rc") for directory in [config_home] + config_global]

if "XDG_DATA_HOME" in os.environ:
    data_home = Path(os.environ.get("XDG_DATA_HOME"))
else:
    data_home = Path.home() / ".local" / "share"

recents_file_location = data_home / "rofimoji" / "recent"
favorites_file_location = data_home / "rofimoji" / "favorites"
frecency_file_location = data_home / "rofimoji" / "frecency"
custom_additional_files_location = data_home / "rofimoji" / "data"

if "XDG_CACHE_HOME" in os.environ:
    cache_home = Path(os.environ.get("XDG_CACHE_HOME"))
else:
    cache_home = Path.home() / ".cache"

cache_file_location = cache_home / "rofimoji"
