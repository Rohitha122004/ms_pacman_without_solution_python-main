# src/pacman/controllers/examples/aggressive_ghosts.py

from random import Random
from typing import Dict
from pacman.controllers.controller import Controller
from pacman.game.game import Game
from pacman.game.constants import GHOST, MOVE, DM


class AggressiveGhosts(Controller):
    CONSISTENCY: float = 1.0

    def __init__(self):
        super().__init__()
        self.rnd = Random()
        self.my_moves: Dict[GHOST, MOVE] = {}
        self.moves = list(MOVE)

    def _get_move(self, game: Game, time_due: int) -> Dict[GHOST, MOVE]:
        self.my_moves.clear()
        for ghost in GHOST:
            if game.does_ghost_require_action(ghost):
                if self.rnd.random() < self.CONSISTENCY:
                    self.my_moves[ghost] = game.get_approximate_next_move_towards_target(
                        game.get_ghost_current_node_index(ghost),
                        game.get_pacman_current_node_index(),
                        game.get_ghost_last_move_made(ghost),
                        DM.PATH
                    )
                else:
                    self.my_moves[ghost] = self.moves[self.rnd.randint(
                        0, len(self.moves) - 1)]
        return self.my_moves
