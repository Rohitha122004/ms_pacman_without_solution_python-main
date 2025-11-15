
# src/pacman/controllers/examples/starter_pacman.py

from typing import List
from pacman.controllers.controller import Controller
from pacman.game.game import Game
from pacman.game.constants import MOVE, GHOST, DM


class StarterPacMan(Controller):
    MIN_DISTANCE: int = 20

    def _get_move(self, game: Game, time_due: int) -> MOVE:
        current = game.get_pacman_current_node_index()

        # Strategy 1: if any non-edible ghost is too close, run away
        for ghost in GHOST:
            if game.get_ghost_edible_time(ghost) == 0 and game.get_ghost_lair_time(ghost) == 0:
                if game.get_shortest_path_distance(current, game.get_ghost_current_node_index(ghost)) < self.MIN_DISTANCE:
                    return game.get_next_move_away_from_target(
                        game.get_pacman_current_node_index(),
                        game.get_ghost_current_node_index(ghost),
                        DM.PATH
                    )

        # Strategy 2: find the nearest edible ghost and go after them
        min_distance = float('inf')
        min_ghost = None

        for ghost in GHOST:
            if game.get_ghost_edible_time(ghost) > 0:
                distance = game.get_shortest_path_distance(
                    current, game.get_ghost_current_node_index(ghost))
                if distance < min_distance:
                    min_distance = distance
                    min_ghost = ghost

        if min_ghost is not None:
            return game.get_next_move_towards_target(
                game.get_pacman_current_node_index(),
                game.get_ghost_current_node_index(min_ghost),
                DM.PATH
            )

        # Strategy 3: go after the pills and power pills
        pills = game.get_pill_indices()
        power_pills = game.get_power_pill_indices()
        targets: List[int] = []

        for i in range(len(pills)):
            if game.is_pill_still_available(i):
                targets.append(pills[i])

        for i in range(len(power_pills)):
            if game.is_power_pill_still_available(i):
                targets.append(power_pills[i])

        return game.get_next_move_towards_target(
            current,
            game.get_closest_node_index_from_node_index(
                current, targets, DM.PATH),
            DM.PATH
        )
