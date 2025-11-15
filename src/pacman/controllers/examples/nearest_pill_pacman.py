# src/pacman/controllers/examples/nearest_pill_pacman.py

from pacman.controllers.controller import Controller
from pacman.game.game import Game
from pacman.game.constants import MOVE, DM


class NearestPillPacMan(Controller):
    def _get_move(self, game: Game, time_due: int) -> MOVE:
        current_node_index = game.get_pacman_current_node_index()
        active_pills = game.get_active_pills_indices()
        active_power_pills = game.get_active_power_pills_indices()
        target_node_indices = active_pills + active_power_pills
        return game.get_next_move_towards_target(
            game.get_pacman_current_node_index(),
            game.get_closest_node_index_from_node_index(
                current_node_index, target_node_indices, DM.PATH),
            DM.PATH
        )
