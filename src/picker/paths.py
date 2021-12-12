from pathlib import Path
import os

if os.environ.get('XDG_CONFIG_HOME'):
    config_home = Path(os.environ.get('XDG_CONFIG_HOME'))
else:
    config_home = Path.home() / '.config'

if os.environ.get('XDG_CONFIG_DIRS'):
    config_global = [Path(dir) for dir in os.environ.get('XDG_CONFIG_DIRS').split(':')]
else:
    config_global = [Path('/etc/xdg')]

config_file_locations = [str(directory / 'rofimoji.rc') for directory in [config_home] + config_global]

if os.environ.get('XDG_DATA_HOME'):
    data_home = Path(os.environ.get('XDG_DATA_HOME'))
else:
    data_home = Path.home() / '.local' / 'share'

recents_file_location = data_home / 'rofimoji' / 'recent'
favorites_file_location = data_home / 'rofimoji' / 'favorites'
frecency_file_location = data_home / 'rofimoji' / 'frecency'
custom_additional_files_location = data_home / 'rofimoji' / 'data'

if os.environ.get('XDG_CACHE_HOME'):
    cache_home = Path(os.environ.get('XDG_CACHE_HOME'))
else:
    cache_home = Path.home() / '.cache'

cache_file_location = cache_home / 'rofimoji'
