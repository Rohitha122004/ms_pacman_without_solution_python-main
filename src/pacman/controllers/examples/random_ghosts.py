# src/pacman/controllers/examples/random_ghosts.py

from random import Random
from typing import Dict
from pacman.controllers.controller import Controller
from pacman.game.game import Game
from pacman.game.constants import GHOST, MOVE


class RandomGhosts(Controller):
    def __init__(self):
        super().__init__()
        self.moves: Dict[GHOST, MOVE] = {}
        self.all_moves = list(MOVE)
        self.rnd = Random()

    def _get_move(self, game: Game, time_due: int) -> Dict[GHOST, MOVE]:
        self.moves.clear()
        for ghost_type in GHOST:
            if game.does_ghost_require_action(ghost_type):
                self.moves[ghost_type] = self.all_moves[self.rnd.randint(
                    0, len(self.all_moves) - 1)]
        return self.moves
