from __future__ import annotations

import contextlib
import io
import sys
from typing import Callable, Union

from pacman.controllers.controller import Controller
from pacman.game.game import Game

MAX_STEPS = 2000
MAX_DURATION_SECONDS = 10

ControllerFactory = Union[Controller, Callable[[], Controller]]


def _instantiate(controller: ControllerFactory) -> Controller:
    return controller() if callable(controller) else controller


@contextlib.contextmanager
def _suppress_output():
    buffer = io.StringIO()
    original_stdout = sys.stdout
    try:
        sys.stdout = buffer
        yield
    finally:
        sys.stdout = original_stdout


def suppress_game_output():
    return _suppress_output()


def play_timed_game(
    pacman_controller: Controller,
    ghost_controller: Controller,
    *,
    max_steps: int = MAX_STEPS,
    seed: int = 0,
) -> float:
    with _suppress_output():
        game = Game(seed)
    steps = 0
    while not game.game_over() and steps < max_steps:
        with _suppress_output():
            pac_move = pacman_controller._get_move(game.copy(), -1)
            ghost_moves = ghost_controller._get_move(game.copy(), -1)
            game.advance_game(pac_move, ghost_moves)
        steps += 1
    return float(game.get_score())


def average_score(
    pacman_controller: ControllerFactory,
    ghost_controller: ControllerFactory,
    games: int,
    *,
    prefix: str = "",
    seed_offset: int = 0,
) -> float:
    total = 0.0
    for index in range(games):
        pacman = _instantiate(pacman_controller)
        ghosts = _instantiate(ghost_controller)
        score = play_timed_game(pacman, ghosts, seed=seed_offset + index)
        print(
            f"{prefix}  - Game {index + 1}/{games} "
            f"(max {MAX_STEPS} iterations, <={MAX_DURATION_SECONDS}s): {score:.2f}"
        )
        total += score
    average = total / games
    print(f"{prefix}  > Average over {games} game(s): {average:.2f}")
    return average
