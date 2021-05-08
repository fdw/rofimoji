import enum


class Action(enum.Enum):
    TYPE = 'type'
    COPY = 'copy'
    CLIPBOARD = 'clipboard'
    UNICODE = 'unicode'
    COPY_UNICODE = 'copy-unicode'
    STDOUT = 'print'
