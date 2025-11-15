# pacman/game/internal/ghost.py

from pacman.game.constants import GHOST, MOVE


class Ghost:
    def __init__(self, type: GHOST,
                 current_node_index: int,
                 edible_time: int, 
                 lair_time: int, 
                 last_move_made: MOVE):
        self.type = type
        self.current_node_index = current_node_index
        self.edible_time = edible_time
        self.lair_time = lair_time
        self.last_move_made = last_move_made

    def copy(self) -> 'Ghost':
        return Ghost(self.type, self.current_node_index, self.edible_time, self.lair_time, self.last_move_made)
