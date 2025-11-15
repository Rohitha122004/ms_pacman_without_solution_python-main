# src/pacman/controllers/human_controller.py

from pacman.game.constants import MOVE
from pacman.game.game import Game
from .controller import Controller
from .keyboard_input import KeyBoardInput

class HumanController(Controller):
    """
    A controller that allows a human player to control Pac-Man using arrow keys.
    """
    def __init__(self, input: KeyBoardInput):
        """
        Initializes the controller with a keyboard input handler.

        :param input: The KeyBoardInput instance for capturing key presses.
        """
        super().__init__()
        self.input = input

    def get_keyboard_input(self) -> KeyBoardInput:
        """
        Gets the keyboard input handler.

        :return: The KeyBoardInput instance.
        """
        return self.input

    def _get_move(self, game: Game, time_due: int) -> MOVE:
        """
        Computes the next move based on the last key pressed.

        :param game: A copy of the current game.
        :param time_due: The time the next move is due.
        :return: The computed move (MOVE enum).
        """
        # Prefer the MOVE cached by KeyBoardInput (set in key_pressed)
        move = getattr(self.input, "last_key", MOVE.NEUTRAL)
        if move in {MOVE.UP, MOVE.DOWN, MOVE.LEFT, MOVE.RIGHT}:
            self.last_move = move
            return self.last_move

        # Fall back to the raw keysym from get_key() (e.g., 'Up', 'Down') or a MOVE
        key = self.input.get_key()
        mapping = {
            "Up": MOVE.UP,
            "Right": MOVE.RIGHT,
            "Down": MOVE.DOWN,
            "Left": MOVE.LEFT,
            MOVE.UP: MOVE.UP,
            MOVE.RIGHT: MOVE.RIGHT,
            MOVE.DOWN: MOVE.DOWN,
            MOVE.LEFT: MOVE.LEFT,
        }
        # If mapping is unknown, keep previous direction (sticky) or NEUTRAL
        self.last_move = mapping.get(key, self.last_move or MOVE.NEUTRAL)
        return self.last_move
