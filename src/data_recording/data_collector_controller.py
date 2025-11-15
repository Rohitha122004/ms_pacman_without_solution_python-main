# src/pacman/data_recording/data_collector_controller.py

from pacman.controllers.human_controller import HumanController
from pacman.game.game import Game
from pacman.game.constants import MOVE
from .data_tuple import DataTuple
from .data_saver_loader import DataSaverLoader
from pacman.controllers.keyboard_input import KeyBoardInput


class DataCollectorController(HumanController):
    def __init__(self, input: KeyBoardInput):
        super().__init__(input)

    def _get_move(self, game: Game, due_time: int) -> MOVE:
        move = super()._get_move(game, due_time)
        data = DataTuple(game, move)
        DataSaverLoader.save_pacman_data(data)
        return move
