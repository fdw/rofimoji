import os

from .mode import ModeRofimoji
from .standalone import StandaloneRofimoji


def main():
    if "ROFI_RETV" not in os.environ:
        StandaloneRofimoji().standalone()
    else:
        ModeRofimoji().mode()


if __name__ == "__main__":
    main()
