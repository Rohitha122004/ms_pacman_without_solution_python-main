from pacman.controllers.examples.null_ghosts import NullGhosts
from pacman.controllers.examples.random_pacman import RandomPacMan
from pacman.controllers.examples.starter_ghosts import StarterGhosts

from .game_test_utils import play_timed_game
from .progress_tracker import TestProgressTracker


def test_01_game_smoke():
    print("[SMOKE] Ms Pac-Man framework readiness check (no marks associated to this test).")
    print("[SMOKE] Pass condition: RandomPacMan score must be >= 0 within 2000 iterations (<=10s).")

    play_timed_game(RandomPacMan(), NullGhosts())
    starter_score = play_timed_game(RandomPacMan(), StarterGhosts())
    passed = starter_score >= 0.0
    print(f"[SMOKE] build {'success' if passed else 'failure'}")

    print(TestProgressTracker.DOUBLE_DIVIDER)
    print(
        "The following results worth 17/20 points. Submit your reports to canvas to gain the rest 3/20 points of"
        " coursework 2."
    )

    assert passed, "[SMOKE] Game loop should finish without a negative score"
