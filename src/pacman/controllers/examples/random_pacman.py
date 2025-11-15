# src/pacman/controllers/examples/random_pacman.py

from random import Random
from pacman.controllers.controller import Controller
from pacman.game.game import Game
from pacman.game.constants import MOVE


class RandomPacMan(Controller):
    def __init__(self):
        super().__init__()
        self.rnd = Random()
        self.all_moves = list(MOVE)

    def _get_move(self, game: Game, time_due: int) -> MOVE:
        return self.all_moves[self.rnd.randint(0, len(self.all_moves) - 1)]
