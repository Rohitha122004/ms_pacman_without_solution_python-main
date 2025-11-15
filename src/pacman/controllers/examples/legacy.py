# src/pacman/controllers/examples/legacy.py

from random import Random
from typing import Dict
from pacman.controllers.controller import Controller
from pacman.game.game import Game
from pacman.game.constants import GHOST, MOVE, DM


class Legacy(Controller):
    def __init__(self):
        super().__init__()
        self.rnd = Random()
        self.my_moves: Dict[GHOST, MOVE] = {}
        self.moves = list(MOVE)

    def _get_move(self, game: Game, time_due: int) -> Dict[GHOST, MOVE]:
        self.my_moves.clear()
        target_node = game.get_pacman_current_node_index()

        if game.does_ghost_require_action(GHOST.BLINKY):
            self.my_moves[GHOST.BLINKY] = game.get_approximate_next_move_towards_target(
                game.get_ghost_current_node_index(GHOST.BLINKY),
                target_node,
                game.get_ghost_last_move_made(GHOST.BLINKY),
                DM.PATH
            )
        if game.does_ghost_require_action(GHOST.INKY):
            self.my_moves[GHOST.INKY] = game.get_approximate_next_move_towards_target(
                game.get_ghost_current_node_index(GHOST.INKY),
                target_node,
                game.get_ghost_last_move_made(GHOST.INKY),
                DM.MANHATTAN
            )
        if game.does_ghost_require_action(GHOST.PINKY):
            self.my_moves[GHOST.PINKY] = game.get_approximate_next_move_towards_target(
                game.get_ghost_current_node_index(GHOST.PINKY),
                target_node,
                game.get_ghost_last_move_made(GHOST.PINKY),
                DM.EUCLID
            )
        if game.does_ghost_require_action(GHOST.SUE):
            self.my_moves[GHOST.SUE] = self.moves[self.rnd.randint(
                0, len(self.moves) - 1)]

        return self.my_moves
