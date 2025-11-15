# src/pacman/controllers/key_board_input.py

from tkinter import Tk, Canvas
from typing import Optional
from pacman.game.constants import MOVE

class KeyBoardInput:
    """
    A simple key handler for capturing keyboard input.
    """

    def __init__(self):
        # self.key: Optional[str] = None
        self.key: MOVE = MOVE.NEUTRAL
        self.last_key: MOVE = MOVE.NEUTRAL
        # No internal Tkinter window. Key binding should be done on the main game window/canvas.

    # def get_key(self) -> Optional[str]:
    def get_key(self) -> MOVE:
        """
        Gets the last key pressed.

        :return: The key code of the last key pressed, or None if no key was pressed.
        """
        print('get_key keyboardinput', self.key)
        return self.key

    # def key_pressed(self, event) -> None:
    #     """
    #     Handles key press events.

    #     :param event: The key event.
    #     """
    #     # self.key = event.keysym_num
    #     self.key = getattr(event, "keysym_num", None) or getattr(
    #         event, "keycode", None)

    def key_pressed(self, event):
        """
        Updates the last key pressed based on the event.

        :param event: The key press event.
        """
        key = event.keysym
        # print('key pressed: ', key)
        self.key = key  # Add this to update self.key with the string key like 'Up'

        # --- ADD THIS LINE ---
        print(f"[DEBUG] Key press detected: '{key}'")

        if key == 'Up':
            self.last_key = MOVE.UP
        elif key == 'Down':
            self.last_key = MOVE.DOWN
        elif key == 'Left':
            self.last_key = MOVE.LEFT
        elif key == 'Right':
            self.last_key = MOVE.RIGHT
            
        
