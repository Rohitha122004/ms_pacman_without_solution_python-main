from pacman.controllers.examples.null_ghosts import NullGhosts
from pacman.controllers.examples.starter_ghosts import StarterGhosts
from pacman.controllers.agents.value_iteration_agent import ValueIterationAgent

from .game_test_utils import MAX_DURATION_SECONDS, MAX_STEPS, average_score
from .progress_tracker import TestProgressTracker

GAMES = 3


def test_02_value_iteration_stage_one():
    agent = ValueIterationAgent()
    iterations = getattr(agent, "iterations", "unknown")

    print("[ValueIteration#1] Worth 3/20 points in coursework 2.")
    print(
        f"[ValueIteration#1] Setup: ValueIterationAgent vs NullGhosts ({GAMES} games, max {MAX_STEPS} iterations, <="
        f"{MAX_DURATION_SECONDS}s)."
    )
    print("[ValueIteration#1] Pass condition: average score > 10.")
    print(f"[ValueIteration#1] Planning iterations used: {iterations}")

    average = average_score(agent, NullGhosts, GAMES, prefix="[ValueIteration#1]")
    passed = average > 10.0
    print(f"[ValueIteration#1] Result: {'PASS' if passed else 'FAIL'} (average {average:.2f})")

    TestProgressTracker.record("ValueIteration#1", passed, 3.0)
    print(TestProgressTracker.SINGLE_DIVIDER)
    assert passed, "[ValueIteration#1] Expected average score > 10 against NullGhosts."


def test_03_value_iteration_stage_two():
    agent = ValueIterationAgent()
    iterations = getattr(agent, "iterations", "unknown")

    print("[ValueIteration#2] Worth 3/20 points in coursework 2.")
    print(f"[ValueIteration#2] Training iterations: {iterations}")
    print(
        f"[ValueIteration#2] Setup: ValueIterationAgent vs NullGhosts ({GAMES} games, max {MAX_STEPS} iterations, <="
        f"{MAX_DURATION_SECONDS}s)."
    )
    print("[ValueIteration#2] Pass condition: average score >= 100.")

    average = average_score(agent, NullGhosts, GAMES, prefix="[ValueIteration#2]")
    passed = average >= 100.0
    print(f"[ValueIteration#2] Result: {'PASS' if passed else 'FAIL'} (average {average:.2f})")
    TestProgressTracker.record("ValueIteration#2", passed, 3.0)

    print(TestProgressTracker.SINGLE_DIVIDER)
    print(
        f"[ValueIteration#2] Information only: ValueIterationAgent vs StarterGhosts (3 games, max {MAX_STEPS} iterations, <="
        f"{MAX_DURATION_SECONDS}s)."
    )
    average_score(agent, StarterGhosts, 3, prefix="[ValueIteration#2][Info]")
    print(TestProgressTracker.DOUBLE_DIVIDER)

    assert passed, "[ValueIteration#2] Expected average score >= 100 against NullGhosts."
