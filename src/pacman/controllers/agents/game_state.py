from __future__ import annotations

from typing import List

from pacman.game.constants import MOVE, GHOST
from pacman.game.game import Game
from pacman.controllers.examples.null_ghosts import NullGhosts
from .transition import Transition


class GameState:
    def __init__(self, pacman_node: int, dist_to_closest_pill: int, dist_to_closest_ghost: int, ghost_is_edible: bool):
        self.pacman_node = pacman_node
        self.dist_to_closest_pill = dist_to_closest_pill // 10
        self.dist_to_closest_ghost = dist_to_closest_ghost // 10
        self.ghost_is_edible = ghost_is_edible

    @staticmethod
    def from_game(game: Game) -> 'GameState':
        pac_node = game.get_pacman_current_node_index()

        # Compute distance to closest available pill
        pill_nodes = game.get_pill_indices()
        closest_pill_dist = float('inf')
        for i, node in enumerate(pill_nodes):
            if game.is_pill_still_available(i):
                dist = game.get_shortest_path_distance(pac_node, node)
                if dist != -1 and dist < closest_pill_dist:
                    closest_pill_dist = dist
        if closest_pill_dist == float('inf'):
            closest_pill_dist = 0

        # Compute distance to closest ghost and whether that closest ghost is edible
        closest_ghost_dist = float('inf')
        edible = False
        for ghost in GHOST:
            g_node = game.get_ghost_current_node_index(ghost)
            dist = game.get_shortest_path_distance(pac_node, g_node)
            if dist != -1 and dist < closest_ghost_dist:
                closest_ghost_dist = dist
                edible = game.get_ghost_edible_time(ghost) > 0
        if closest_ghost_dist == float('inf'):
            closest_ghost_dist = 0

        return GameState(pac_node, closest_pill_dist, closest_ghost_dist, edible)

    def get_legal_moves(self) -> List[MOVE]:
        return list(MOVE)

    def get_transitions(self, game: Game, action: MOVE) -> List[Transition]:
        sim = game.copy()
        ghost_moves = NullGhosts()._get_move(sim, -1)
        sim.advance_game(action, ghost_moves)
        next_state = GameState.from_game(sim)
        reward = sim.get_score() - game.get_score()
        return [Transition(next_state, 1.0, reward)]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, GameState):
            return False
        return (
            self.pacman_node == other.pacman_node and
            self.dist_to_closest_pill == other.dist_to_closest_pill and
            self.dist_to_closest_ghost == other.dist_to_closest_ghost and
            self.ghost_is_edible == other.ghost_is_edible
        )

    def __hash__(self) -> int:
        return hash((
            self.pacman_node,
            self.dist_to_closest_pill,
            self.dist_to_closest_ghost,
            self.ghost_is_edible,
        ))
