# src/pacman/data_recording/data_tuple.py

from enum import Enum
from typing import List
from pacman.game.constants import MOVE, GHOST, DM
from pacman.game.game import Game


class DiscreteTag(Enum):
    VERY_LOW = "VERY_LOW"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    VERY_HIGH = "VERY_HIGH"
    NONE = "NONE"

    @staticmethod
    def discretize_double(aux: float) -> 'DiscreteTag':
        if aux < 0.1:
            return DiscreteTag.VERY_LOW
        elif aux <= 0.3:
            return DiscreteTag.LOW
        elif aux <= 0.5:
            return DiscreteTag.MEDIUM
        elif aux <= 0.7:
            return DiscreteTag.HIGH
        else:
            return DiscreteTag.VERY_HIGH


class DataTuple:
    def __init__(self, game: Game = None, move: MOVE = None, data_line: str = None):
        if data_line:
            values = data_line.split(",")
            self.direction_chosen = MOVE[values[0].strip()]
            self.maze_index = int(values[1])
            self.current_level = int(values[2])
            self.pacman_position = int(values[3])
            self.pacman_lives_left = int(values[4])
            self.current_score = int(values[5])
            self.total_game_time = int(values[6])
            self.current_level_time = int(values[7])
            self.num_of_pills_left = int(values[8])
            self.num_of_power_pills_left = int(values[9])
            self.is_blinky_edible = bool(values[10])
            self.is_inky_edible = bool(values[11])
            self.is_pinky_edible = bool(values[12])
            self.is_sue_edible = bool(values[13])
            self.blinky_dist = int(values[14])
            self.inky_dist = int(values[15])
            self.pinky_dist = int(values[16])
            self.sue_dist = int(values[17])
            self.blinky_dir = MOVE[values[18].strip()]
            self.inky_dir = MOVE[values[19].strip()]
            self.pinky_dir = MOVE[values[20].strip()]
            self.sue_dir = MOVE[values[21].strip()]

            self.number_of_nodes_in_level = game.get_number_of_nodes()
            self.number_of_total_pills_in_level = len(game.get_pill_indices())
            self.number_of_total_power_pills_in_level = len(
                game.get_power_pill_indices())
        else:
            if move == MOVE.NEUTRAL:
                move = game.get_pacman_last_move_made()

            self.direction_chosen = move

            self.maze_index = game.get_maze_index()
            self.current_level = game.get_current_level()
            self.pacman_position = game.get_pacman_current_node_index()
            self.pacman_lives_left = game.get_pacman_number_of_lives_remaining()
            self.current_score = game.get_score()
            self.total_game_time = game.get_total_time()
            self.current_level_time = game.get_current_level_time()
            self.num_of_pills_left = game.get_number_of_active_pills()
            self.num_of_power_pills_left = game.get_number_of_active_power_pills()

            self.is_blinky_edible = game.is_ghost_edible(GHOST.BLINKY)
            self.is_inky_edible = game.is_ghost_edible(GHOST.INKY)
            self.is_pinky_edible = game.is_ghost_edible(GHOST.PINKY)
            self.is_sue_edible = game.is_ghost_edible(GHOST.SUE)

            self.blinky_dist = game.get_shortest_path_distance(
                self.pacman_position, game.get_ghost_current_node_index(GHOST.BLINKY))
            self.inky_dist = game.get_shortest_path_distance(
                self.pacman_position, game.get_ghost_current_node_index(GHOST.INKY))
            self.pinky_dist = game.get_shortest_path_distance(
                self.pacman_position, game.get_ghost_current_node_index(GHOST.PINKY))
            self.sue_dist = game.get_shortest_path_distance(
                self.pacman_position, game.get_ghost_current_node_index(GHOST.SUE))

            self.blinky_dir = game.get_next_move_towards_target(
                self.pacman_position, game.get_ghost_current_node_index(GHOST.BLINKY), DM.PATH)
            self.inky_dir = game.get_next_move_towards_target(
                self.pacman_position, game.get_ghost_current_node_index(GHOST.INKY), DM.PATH)
            self.pinky_dir = game.get_next_move_towards_target(
                self.pacman_position, game.get_ghost_current_node_index(GHOST.PINKY), DM.PATH)
            self.sue_dir = game.get_next_move_towards_target(
                self.pacman_position, game.get_ghost_current_node_index(GHOST.SUE), DM.PATH)

            self.number_of_nodes_in_level = game.get_number_of_nodes()
            self.number_of_total_pills_in_level = len(game.get_pill_indices())
            self.number_of_total_power_pills_in_level = len(
                game.get_power_pill_indices())

    def get_save_string(self) -> str:
        return f"{self.direction_chosen.name}, {self.maze_index}, {self.current_level}, {self.pacman_position}, {self.pacman_lives_left}, {self.current_score}, {self.total_game_time}, {self.current_level_time}, {self.num_of_pills_left}, {self.num_of_power_pills_left}, {self.is_blinky_edible}, {self.is_inky_edible}, {self.is_pinky_edible}, {self.is_sue_edible}, {self.blinky_dist}, {self.inky_dist}, {self.pinky_dist}, {self.sue_dist}, {self.blinky_dir.name}, {self.inky_dir.name}, {self.pinky_dir.name}, {self.sue_dir.name}"

    def discretize_position(self, pos: int) -> DiscreteTag:
        aux = self.normalize_position(pos)
        return DiscreteTag.discretize_double(aux)

    def normalize_position(self, pos: int) -> float:
        return (pos - 0) / (self.number_of_nodes_in_level - 0)

    def discretize_distance(self, distance: int) -> DiscreteTag:
        if distance < 0:
            return DiscreteTag.NONE
        aux = self.normalize_distance(distance)
        return DiscreteTag.discretize_double(aux)

    def normalize_distance(self, distance: int) -> float:
        if distance < 0:
            return -1
        return (distance - 0) / (150 - 0)

    def discretize_lives_left(self, lives: int) -> DiscreteTag:
        aux = self.normalize_lives_left(lives)
        return DiscreteTag.discretize_double(aux)

    def normalize_lives_left(self, lives: int) -> float:
        return (lives - 0) / (Constants.NUM_LIVES - 0)

    def discretize_number_of_pills(self, num_of_pills: int) -> DiscreteTag:
        aux = self.normalize_number_of_pills(num_of_pills)
        return DiscreteTag.discretize_double(aux)

    def normalize_number_of_pills(self, num_of_pills: int) -> float:
        return (num_of_pills - 0) / (self.number_of_total_pills_in_level - 0)

    def discretize_number_of_power_pills(self, num_of_power_pills: int) -> DiscreteTag:
        aux = self.normalize_number_of_power_pills(num_of_power_pills)
        return DiscreteTag.discretize_double(aux)

    def normalize_number_of_power_pills(self, num_of_power_pills: int) -> float:
        return (num_of_power_pills - 0) / (self.number_of_total_power_pills_in_level - 0)

    def discretize_total_game_time(self, time: int) -> DiscreteTag:
        aux = self.normalize_total_game_time(time)
        return DiscreteTag.discretize_double(aux)

    def normalize_total_game_time(self, time: int) -> float:
        return (time - 0) / (Constants.MAX_TIME - 0)

    def discretize_current_level_time(self, time: int) -> DiscreteTag:
        aux = self.normalize_current_level_time(time)
        return DiscreteTag.discretize_double(aux)

    def normalize_current_level_time(self, time: int) -> float:
        return (time - 0) / (Constants.LEVEL_LIMIT - 0)

    def discretize_current_score(self, score: int) -> DiscreteTag:
        aux = self.normalize_current_score(score)
        return DiscreteTag.discretize_double(aux)

    def normalize_current_score(self, score: int) -> float:
        return (score - 0) / (82180 - 0)
