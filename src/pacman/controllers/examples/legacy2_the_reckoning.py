# src/pacman/controllers/examples/legacy2_the_reckoning.py

from typing import Dict
from pacman.controllers.controller import Controller
from pacman.game.game import Game
from pacman.game.constants import GHOST, MOVE, DM


class Legacy2TheReckoning(Controller):
    CROWDED_DISTANCE: int = 30
    PACMAN_DISTANCE: int = 10
    PILL_PROXIMITY: int = 15

    def __init__(self):
        super().__init__()
        self.my_moves: Dict[GHOST, MOVE] = {}
        self.corner_allocation: Dict[GHOST, int] = {
            GHOST.BLINKY: 0,
            GHOST.INKY: 1,
            GHOST.PINKY: 2,
            GHOST.SUE: 3
        }

    def _get_move(self, game: Game, time_due: int) -> Dict[GHOST, MOVE]:
        pacman_index = game.get_pacman_current_node_index()
        self.my_moves.clear()

        for ghost in GHOST:
            if game.does_ghost_require_action(ghost):
                current_index = game.get_ghost_current_node_index(ghost)
                if self._is_crowded(game) and not self._close_to_ms_pacman(game, current_index):
                    self.my_moves[ghost] = self._get_retreat_actions(
                        game, ghost)
                elif game.get_ghost_edible_time(ghost) > 0 or self._close_to_power(game):
                    self.my_moves[ghost] = game.get_approximate_next_move_away_from_target(
                        current_index,
                        pacman_index,
                        game.get_ghost_last_move_made(ghost),
                        DM.PATH
                    )
                else:
                    self.my_moves[ghost] = game.get_approximate_next_move_towards_target(
                        current_index,
                        pacman_index,
                        game.get_ghost_last_move_made(ghost),
                        DM.PATH
                    )
        return self.my_moves

    def _close_to_power(self, game: Game) -> bool:
        pacman_index = game.get_pacman_current_node_index()
        power_pill_indices = game.get_active_power_pills_indices()
        for i in range(len(power_pill_indices)):
            if game.get_shortest_path_distance(power_pill_indices[i], pacman_index) < self.PILL_PROXIMITY:
                return True
        return False

    def _close_to_ms_pacman(self, game: Game, location: int) -> bool:
        return game.get_shortest_path_distance(game.get_pacman_current_node_index(), location) < self.PACMAN_DISTANCE

    def _is_crowded(self, game: Game) -> bool:
        ghosts = list(GHOST)
        distance = 0
        for i in range(len(ghosts) - 1):
            for j in range(i + 1, len(ghosts)):
                distance += game.get_shortest_path_distance(
                    game.get_ghost_current_node_index(ghosts[i]),
                    game.get_ghost_current_node_index(ghosts[j])
                )
        return (distance / 6) < self.CROWDED_DISTANCE

    def _get_retreat_actions(self, game: Game, ghost: GHOST) -> MOVE:
        current_index = game.get_ghost_current_node_index(ghost)
        pacman_index = game.get_pacman_current_node_index()
        if game.get_ghost_edible_time(ghost) == 0 and game.get_shortest_path_distance(current_index, pacman_index) < self.PACMAN_DISTANCE:
            return game.get_approximate_next_move_towards_target(
                current_index,
                pacman_index,
                game.get_ghost_last_move_made(ghost),
                DM.PATH
            )
        else:
            return game.get_approximate_next_move_towards_target(
                current_index,
                game.get_power_pill_indices()[self.corner_allocation[ghost]],
                game.get_ghost_last_move_made(ghost),
                DM.PATH
            )
