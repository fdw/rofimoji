from subprocess import run

from ..abstractionhelper import is_installed
from ..action import __get_codepoints as get_codepoints, __get_event_code as get_event_code
from .typer import Typer

class YdotoolTyper(Typer):
    @staticmethod
    def name():
        return "ydotool"
    
    @staticmethod
    def supported():
        return is_installed("ydotool")
    
    def get_active_window(self):
        return "not possible with ydotool"
    
    def type_characters(self, characters: str, active_window: str) -> None:
        # characters is assumed to be a string of emojis; for each emoji,
        # get the unicode code point, then for each char in the unicode code point,
        # get the event code for the char, then send the event code to ydotool
        for character in characters:
            # Get the unicode code point for the emoji
            unicode_code_point = get_codepoints(character)

            # Get keypresses for Ctrl, Shift, U, and the unicode code point
            Ctrl = get_event_code("LeftCtrl") + ":1"
            Shift = get_event_code("LeftShift") + ":1"
            U_press = get_event_code("U") + ":1"
            Ctrl_release = get_event_code("LeftCtrl") + ":0"
            Shift_release = get_event_code("LeftShift") + ":0"
            U_release = get_event_code("U") + ":0"
            points = []
            
            for point in unicode_code_point:
                points.append(get_event_code(point) + ":1")
                points.append(get_event_code(point) + ":0")

            # Send the event codes to ydotool
            run(["ydotool", "key", Ctrl, Shift, U_press, U_release] + points + [Shift_release, Ctrl_release])

    def insert_from_clipboard(self, active_window: str) -> None:
        Shift = get_event_code("LeftShift") + ":1"
        Shift_release = get_event_code("LeftShift") + ":0"
        Insert = get_event_code("Insert") + ":1"
        Insert_release = get_event_code("Insert") + ":0"
        
        run(["ydotool", "key", Shift, Insert, Insert_release, Shift_release]) 
