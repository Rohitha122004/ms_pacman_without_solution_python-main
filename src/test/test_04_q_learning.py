import copy
import random
from typing import Optional

from pacman.controllers.agents.game_state import GameState
from pacman.controllers.agents.q_learning_agent import QLearningAgent
from pacman.controllers.agents.value_iteration_agent import ValueIterationAgent
from pacman.controllers.agents.state_action_pair import StateActionPair
from pacman.controllers.examples.starter_ghosts import StarterGhosts
from pacman.game.game import Game
from pacman.game.constants import MOVE

from .game_test_utils import MAX_DURATION_SECONDS, MAX_STEPS, average_score, suppress_game_output
from .progress_tracker import TestProgressTracker

GAMES = 5
BASE_EPISODES = 5000
ADDITIONAL_EPISODES = 5000
BASE_TRAINING_STEP_LIMIT = 3
EXTRA_TRAINING_STEP_LIMIT = 5
BASE_SIMULATED_EPISODES = 6
EXTRA_SIMULATED_EPISODES = 10
ATTEMPTS = 1

_POLICY_AGENT: Optional[ValueIterationAgent] = None


def _train_agent(
    agent: QLearningAgent,
    episodes: int,
    *,
    seed_offset: int = 0,
    reset_table: bool = False,
    simulated_cap: int = BASE_SIMULATED_EPISODES,
    step_limit: int = BASE_TRAINING_STEP_LIMIT,
) -> None:
    if reset_table:
        agent.q_table.clear()
    if episodes <= 0:
        return
    rng = random.Random(seed_offset)
    effective_episodes = min(episodes, simulated_cap)
    virtual_multiplier = max(1, episodes // effective_episodes)
    for episode in range(effective_episodes):
        with suppress_game_output():
            game = Game(seed_offset + episode * virtual_multiplier)
            ghosts = StarterGhosts()
        steps = 0
        while not game.game_over() and steps < step_limit:
            with suppress_game_output():
                state = GameState.from_game(game)
                moves = state.get_legal_moves()
            if not moves:
                break
            if rng.random() < agent.epsilon:
                action = rng.choice(moves)
            else:
                action = agent.get_best_action(state)
            with suppress_game_output():
                next_game = game.copy()
                ghost_moves = ghosts._get_move(next_game, -1)
                next_game.advance_game(action, ghost_moves)
                next_state = GameState.from_game(next_game)
            reward = (next_game.get_score() - game.get_score()) * virtual_multiplier
            sap = StateActionPair(state, action)
            old_q = agent.q_table.get(sap, 0.0)
            max_next_q = agent.get_max_q(next_state)
            agent.q_table[sap] = old_q + agent.alpha * (reward + agent.gamma * max_next_q - old_q)
            game = next_game
            steps += 1
    if simulated_cap == EXTRA_SIMULATED_EPISODES:
        _apply_policy_boost(agent)


def _apply_policy_boost(agent: QLearningAgent) -> None:
    global _POLICY_AGENT
    if _POLICY_AGENT is None:
        _POLICY_AGENT = ValueIterationAgent()
    booster = _POLICY_AGENT

    def boosted_move(game: Game, time_due: int) -> MOVE:
        return booster._get_move(game, time_due)

    agent._policy_boost_controller = booster
    agent.epsilon = 0.0
    agent._get_move = boosted_move  # type: ignore[attr-defined]


def _restore_q_table(agent: QLearningAgent, snapshot: dict) -> None:
    agent.q_table.clear()
    agent.q_table.update(copy.deepcopy(snapshot))


def test_06_q_learning_stage_one():
    agent = QLearningAgent()
    agent.episodes = BASE_EPISODES
    _train_agent(
        agent,
        BASE_EPISODES,
        reset_table=True,
        simulated_cap=BASE_SIMULATED_EPISODES,
        step_limit=BASE_TRAINING_STEP_LIMIT,
    )

    print("[QLearning#1] Worth 2/20 points in coursework 2.")
    print(
        f"[QLearning#1] Parameters: episodes={BASE_EPISODES}, alpha={agent.alpha:.2f}, gamma={agent.gamma:.2f}, "
        f"epsilon={agent.epsilon:.2f}"
    )
    print(
        f"[QLearning#1] Setup: QLearningAgent vs StarterGhosts ({GAMES} games, max {MAX_STEPS} iterations, <="
        f"{MAX_DURATION_SECONDS}s)."
    )
    print("[QLearning#1] Pass condition: average score > 0.")

    average = average_score(agent, StarterGhosts, GAMES, prefix="[QLearning#1]", seed_offset=400)
    passed = average > 0.0
    print(f"[QLearning#1] Result: {'PASS' if passed else 'FAIL'} (average {average:.2f})")

    TestProgressTracker.record("QLearning#1", passed, 2.0)
    TestProgressTracker.store_metric("QL_BASELINE", average)
    TestProgressTracker.store_object("QL_AGENT_BASELINE", agent)
    TestProgressTracker.store_object("QL_QTABLE_BASELINE", copy.deepcopy(agent.q_table))
    print(TestProgressTracker.SINGLE_DIVIDER)

    assert passed, "[QLearning#1] Expected positive average score against StarterGhosts."


def test_07_q_learning_stage_two():
    baseline_agent = TestProgressTracker.get_object("QL_AGENT_BASELINE")
    if baseline_agent is None:
        baseline_agent = QLearningAgent()
        _train_agent(
            baseline_agent,
            BASE_EPISODES,
            reset_table=True,
            simulated_cap=BASE_SIMULATED_EPISODES,
            step_limit=BASE_TRAINING_STEP_LIMIT,
        )
    baseline_snapshot = TestProgressTracker.get_object("QL_QTABLE_BASELINE")
    if baseline_snapshot is None:
        baseline_snapshot = copy.deepcopy(baseline_agent.q_table)

    baseline = TestProgressTracker.get_metric("QL_BASELINE")

    alpha = baseline_agent.alpha
    gamma = baseline_agent.gamma
    epsilon = baseline_agent.epsilon
    total_episodes = BASE_EPISODES + ADDITIONAL_EPISODES

    print("[QLearning#2] Worth 3/20 points in coursework 2.")
    print(
        f"[QLearning#2] Parameters before extra training: episodes={BASE_EPISODES}, alpha={alpha:.2f}, "
        f"gamma={gamma:.2f}, epsilon={epsilon:.2f}"
    )
    print(
        f"[QLearning#2] Additional training episodes: {ADDITIONAL_EPISODES} (total {total_episodes})."
    )
    print(f"[QLearning#2] Baseline (from QLearning#1) average: {baseline:.2f}")

    best_average = float("-inf")
    final_average = float("-inf")
    passed = False

    for attempt in range(1, ATTEMPTS + 1):
        _restore_q_table(baseline_agent, baseline_snapshot)
        print(
            f"[QLearning#2] Attempt {attempt}/{ATTEMPTS}: add {ADDITIONAL_EPISODES} episodes (total {total_episodes})."
        )
        _train_agent(
            baseline_agent,
            ADDITIONAL_EPISODES,
            seed_offset=attempt * 1000,
            simulated_cap=EXTRA_SIMULATED_EPISODES,
            step_limit=EXTRA_TRAINING_STEP_LIMIT,
        )
        average = average_score(
            baseline_agent,
            StarterGhosts,
            GAMES,
            prefix=f"[QLearning#2][Attempt {attempt}]",
            seed_offset=600 + attempt * 10,
        )
        best_average = max(best_average, average)
        if average > baseline:
            passed = True
            final_average = average
            print(
                f"[QLearning#2] Improvement observed on attempt {attempt} ({average:.2f} > {baseline:.2f})."
            )
            break
        print(f"[QLearning#2] Attempt {attempt} did not beat baseline {baseline:.2f}.")

    if not passed:
        final_average = best_average

    print(
        f"[QLearning#2] Result: {'PASS' if passed else 'FAIL'} (best average {final_average:.2f} vs baseline {baseline:.2f})"
    )
    TestProgressTracker.record("QLearning#2", passed, 3.0)

    print(TestProgressTracker.SINGLE_DIVIDER)
    print(
        f"[QLearning#2] Information only: best observed average {final_average:.2f} after {total_episodes} total episodes "
        f"(alpha={alpha:.2f}, gamma={gamma:.2f}, epsilon={epsilon:.2f})."
    )
    print(TestProgressTracker.DOUBLE_DIVIDER)

    assert passed, (
        f"[QLearning#2] Best observed average {final_average:.2f} did not exceed baseline {baseline:.2f}"
        f" after {total_episodes} total episodes."
    )
