from typing import List

from .game_state import GameState


class StateGenerator:
    @staticmethod
    def get_all_states() -> List[GameState]:
        states: List[GameState] = []
        for node in range(0, 100, 5):
            for pill_dist in range(10):
                for ghost_dist in range(10):
                    for edible in (True, False):
                        states.append(GameState(node, pill_dist * 10, ghost_dist * 10, edible))
        return states
