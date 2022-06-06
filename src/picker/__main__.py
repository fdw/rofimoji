import os
import sys

from .paths import cache_file_location
from .rofimoji import Rofimoji


def main():
    return_value = os.environ.get('ROFI_RETV')

    if return_value is None:
        Rofimoji().standalone()
    elif return_value == "0":
        Rofimoji().mode_show_characters()
    elif not cache_file_location.is_file():
        chosen = sys.argv[-1]
        del sys.argv[-1]
        Rofimoji().mode_act_on_selection(chosen, int(return_value))
    else:
        chosen = sys.argv[-1]
        del sys.argv[-1]
        Rofimoji().mode_select_skin_tone(chosen)


if __name__ == "__main__":
    main()
