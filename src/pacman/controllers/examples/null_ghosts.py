# src/pacman/controllers/examples/null_ghosts.py

from typing import Dict
from pacman.controllers.controller import Controller
from pacman.game.game import Game
from pacman.game.constants import GHOST, MOVE


class NullGhosts(Controller):
    def _get_move(self, game: Game, time_due: int) -> Dict[GHOST, MOVE]:
        ghost_moves: Dict[GHOST, MOVE] = {}
        for ghost in GHOST:
            ghost_moves[ghost] = MOVE.NEUTRAL
        return ghost_moves
