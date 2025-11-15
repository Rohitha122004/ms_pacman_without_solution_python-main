"""
Convergence tests for all three agents: ValueIteration, PolicyIteration, and QLearning.

For ValueIteration and PolicyIteration: These agents converge during construction,
so we verify that their policy remains stable across multiple evaluations.

For QLearning: We verify that additional training improves or maintains performance.
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from typing import Dict
from Executer import Executor
from pacman.controllers.controller import Controller
from pacman.controllers.examples.starter_ghosts import StarterGhosts
from pacman.controllers.agents.value_iteration_agent import ValueIterationAgent
from pacman.controllers.agents.policy_iteration_agent import PolicyIterationAgent
from pacman.controllers.agents.q_learning_agent import QLearningAgent
from pacman.game.constants import MOVE


def evaluate_mean_score(agent: Controller[MOVE], games: int) -> float:
    """
    Evaluates an agent over multiple games and returns the average score.
    
    :param agent: The agent to evaluate
    :param games: Number of games to run
    :return: Average score across all games
    """
    exec = Executor()
    ghosts = StarterGhosts()
    total = 0
    for i in range(games):
        print(f"Game {i+1}/{games}")
        total += exec.run_game_timed(agent, ghosts, False)
    return total / float(games)


def test_value_iteration_converges():
    """
    ValueIteration converges during construction. We verify that the agent's
    performance is stable across multiple game evaluations.
    """
    agent = ValueIterationAgent()
    
    # Evaluate the agent multiple times to verify stability
    print("ValueIteration stability test...")
    print('test number: 1')
    score1 = evaluate_mean_score(agent, 5)
    print('test number: 2')
    score2 = evaluate_mean_score(agent, 5)
    print('test number: 3')
    score3 = evaluate_mean_score(agent, 5)
    
    print(f"ValueIteration stability test - Scores: {score1:.1f}, {score2:.1f}, {score3:.1f}")
    
    # Since the agent is deterministic after training, scores should be very similar
    # Allow small variance due to ghost randomness
    max_diff = max(abs(score2 - score1), abs(score3 - score2))
    avg_score = (score1 + score2 + score3) / 3.0
    
    print(f"Average score: {avg_score:.1f}, Max difference: {max_diff:.2f}")
    
    # Verify that the policy is stable (variance should be reasonable)
    assert max_diff < avg_score * 0.3, "ValueIteration should produce stable results"  # Allow 30% variance due to stochastic ghosts


def test_policy_iteration_converges():
    """
    PolicyIteration converges during construction. We verify that the agent's
    performance is stable across multiple game evaluations.
    """
    agent = PolicyIterationAgent()
    
    # Evaluate the agent multiple times to verify stability
    print("PolicyIteration stability test...")
    print('test number: 1')
    score1 = evaluate_mean_score(agent, 5)
    print('test number: 2')
    score2 = evaluate_mean_score(agent, 5)
    print('test number: 3')
    score3 = evaluate_mean_score(agent, 5)
    
    print(f"PolicyIteration stability test - Scores: {score1:.1f}, {score2:.1f}, {score3:.1f}")
    
    # Since the agent is deterministic after training, scores should be very similar
    # Allow small variance due to ghost randomness
    max_diff = max(abs(score2 - score1), abs(score3 - score2))
    avg_score = (score1 + score2 + score3) / 3.0
    
    print(f"Average score: {avg_score:.1f}, Max difference: {max_diff:.2f}")
    
    # Verify that the policy is stable (variance should be reasonable)
    assert max_diff < avg_score * 0.3, "PolicyIteration should produce stable results"  # Allow 30% variance due to stochastic ghosts


def test_q_learning_improves_or_is_non_decreasing():
    """
    QLearning agent should improve or maintain performance with additional training.
    """
    agent = QLearningAgent()
    
    # Evaluate baseline performance after initial training
    print("QLearning stability test...")
    print('test number: 1')
    score1 = evaluate_mean_score(agent, 5)
    print(f"QLearning initial score: {score1:.1f}")
    
    # Additional training
    agent.train()
    
    # Evaluate after additional training
    print('test number: 2')
    score2 = evaluate_mean_score(agent, 5)
    print(f"QLearning score after additional training: {score2:.1f}")
    
    # Allow small tolerance for noise
    assert score2 + 10 >= score1, "QLearning score should not decrease significantly after additional training"
    
    print(f"Score change: {score2 - score1:.1f}")


if __name__ == "__main__":
    print("\n=== Running Convergence Tests ===\n")
    
    print("Testing ValueIteration convergence...")
    test_value_iteration_converges()
    
    print("\nTesting PolicyIteration convergence...")
    test_policy_iteration_converges()
    
    print("\nTesting QLearning improvement...")
    test_q_learning_improves_or_is_non_decreasing()
    
    print("\n=== All Convergence Tests Passed ===")
