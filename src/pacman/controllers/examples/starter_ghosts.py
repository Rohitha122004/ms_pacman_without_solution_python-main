# src/pacman/controllers/examples/starter_ghosts.py

from random import Random
from typing import Dict
from pacman.controllers.controller import Controller
from pacman.game.game import Game
from pacman.game.constants import GHOST, MOVE, DM


class StarterGhosts(Controller):
    CONSISTENCY: float = 0.9
    PILL_PROXIMITY: int = 15

    def __init__(self):
        super().__init__()
        self.rnd = Random()
        self.my_moves: Dict[GHOST, MOVE] = {}

    def _get_move(self, game: Game, time_due: int) -> Dict[GHOST, MOVE]:
        for ghost in GHOST:
            if game.does_ghost_require_action(ghost):
                if game.get_ghost_edible_time(ghost) > 0 or self._close_to_power(game):
                    self.my_moves[ghost] = game.get_approximate_next_move_away_from_target(
                        game.get_ghost_current_node_index(ghost),
                        game.get_pacman_current_node_index(),
                        game.get_ghost_last_move_made(ghost),
                        DM.PATH
                    )
                else:
                    if self.rnd.random() < self.CONSISTENCY:
                        self.my_moves[ghost] = game.get_approximate_next_move_towards_target(
                            game.get_ghost_current_node_index(ghost),
                            game.get_pacman_current_node_index(),
                            game.get_ghost_last_move_made(ghost),
                            DM.PATH
                        )
                    else:
                        possible_moves = game.get_possible_moves_with_last_move(
                            game.get_ghost_current_node_index(ghost),
                            game.get_ghost_last_move_made(ghost)
                        )
                        self.my_moves[ghost] = possible_moves[self.rnd.randint(
                            0, len(possible_moves) - 1)]
        return self.my_moves

    def _close_to_power(self, game: Game) -> bool:
        power_pills = game.get_power_pill_indices()
        for i in range(len(power_pills)):
            if game.is_power_pill_still_available(i) and game.get_shortest_path_distance(power_pills[i], game.get_pacman_current_node_index()) < self.PILL_PROXIMITY:
                return True
        return False
