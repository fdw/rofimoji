from importlib import metadata
from importlib.metadata import PackageNotFoundError

try:
    __version__ = metadata.version(__package__)
except PackageNotFoundError:
    __version__ = "dirty"

del metadata
