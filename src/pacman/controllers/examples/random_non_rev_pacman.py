
# src/pacman/controllers/examples/random_non_rev_pacman.py

from random import Random
from pacman.controllers.controller import Controller
from pacman.game.game import Game
from pacman.game.constants import MOVE


class RandomNonRevPacMan(Controller):
    def __init__(self):
        super().__init__()
        self.rnd = Random()

    def _get_move(self, game: Game, time_due: int) -> MOVE:
        possible_moves = game.get_possible_moves(
            game.get_pacman_current_node_index(), game.get_pacman_last_move_made())
        return possible_moves[self.rnd.randint(0, len(possible_moves) - 1)]
