# pacman/game/internal/pac_man.py

from pacman.game.constants import MOVE


class PacMan:
    def __init__(self, current_node_index: int, last_move_made: MOVE, number_of_lives_remaining: int, has_received_extra_life: bool):
        self.current_node_index = current_node_index
        self.last_move_made = last_move_made
        self.number_of_lives_remaining = number_of_lives_remaining
        self.has_received_extra_life = has_received_extra_life

    def copy(self) -> 'PacMan':
        return PacMan(self.current_node_index, self.last_move_made, self.number_of_lives_remaining, self.has_received_extra_life)
