import os
import shutil


def is_installed(executable: str) -> bool:
    return shutil.which(executable) is not None


def is_wayland() -> bool:
    return "WAYLAND_DISPLAY" in os.environ

def get_event_code(char: str, pressrelease: bool = True) -> str:
    keypress = "KEY_" + char.upper()
    # Consult file /usr/include/linux/input-event-codes.h for the event code
    event_code = ""
    with open("/usr/include/linux/input-event-codes.h") as file:
        for line in file:
            # Line is of the form #define keypress event_code
            if keypress in line.split():
                event_code = line.split()[2]
                break
    
    # pressrelease is a bool indicating whether the event code is for a key press or release
    if pressrelease:
        return f"{event_code}:1"
    else:
        return f"{event_code}:0"