from pacman.controllers.examples.null_ghosts import NullGhosts
from pacman.controllers.examples.starter_ghosts import StarterGhosts
from pacman.controllers.agents.policy_iteration_agent import PolicyIterationAgent

from .game_test_utils import MAX_DURATION_SECONDS, MAX_STEPS, average_score
from .progress_tracker import TestProgressTracker

GAMES = 3


def test_04_policy_iteration_stage_one():
    agent = PolicyIterationAgent()

    print("[PolicyIteration#1] Worth 3/20 points in coursework 2.")
    print(
        f"[PolicyIteration#1] Setup: PolicyIterationAgent vs NullGhosts ({GAMES} games, max {MAX_STEPS} iterations, <="
        f"{MAX_DURATION_SECONDS}s)."
    )
    print("[PolicyIteration#1] Pass condition: average score > 10.")

    average = average_score(agent, NullGhosts, GAMES, prefix="[PolicyIteration#1]")
    passed = average > 10.0
    print(f"[PolicyIteration#1] Result: {'PASS' if passed else 'FAIL'} (average {average:.2f})")

    TestProgressTracker.record("PolicyIteration#1", passed, 3.0)
    print(TestProgressTracker.SINGLE_DIVIDER)
    assert passed, "[PolicyIteration#1] Expected average score > 10 against NullGhosts."


def test_05_policy_iteration_stage_two():
    agent = PolicyIterationAgent()
    max_iterations = getattr(agent, "max_iterations", "unknown")

    print("[PolicyIteration#2] Worth 3/20 points in coursework 2.")
    print(f"[PolicyIteration#2] Max improvement iterations: {max_iterations}")
    print(
        f"[PolicyIteration#2] Setup: PolicyIterationAgent vs NullGhosts ({GAMES} games, max {MAX_STEPS} iterations, <="
        f"{MAX_DURATION_SECONDS}s)."
    )
    print("[PolicyIteration#2] Pass condition: average score >= 100.")

    average = average_score(agent, NullGhosts, GAMES, prefix="[PolicyIteration#2]")
    passed = average >= 100.0
    print(f"[PolicyIteration#2] Result: {'PASS' if passed else 'FAIL'} (average {average:.2f})")
    TestProgressTracker.record("PolicyIteration#2", passed, 3.0)

    print(TestProgressTracker.SINGLE_DIVIDER)
    print(
        f"[PolicyIteration#2] Information only: PolicyIterationAgent vs StarterGhosts (3 games, max {MAX_STEPS} iterations, <="
        f"{MAX_DURATION_SECONDS}s)."
    )
    average_score(agent, StarterGhosts, 3, prefix="[PolicyIteration#2][Info]")
    print(TestProgressTracker.DOUBLE_DIVIDER)

    assert passed, "[PolicyIteration#2] Expected average score >= 100 against NullGhosts."
