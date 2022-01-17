import enum


class Action(enum.Enum):
    TYPE = 'type'
    COPY = 'copy'
    CLIPBOARD = 'clipboard'
    UNICODE = 'unicode'
    COPY_UNICODE = 'copy-unicode'
    STDOUT = 'print'
    
    def __str__(self):
        return self.value
