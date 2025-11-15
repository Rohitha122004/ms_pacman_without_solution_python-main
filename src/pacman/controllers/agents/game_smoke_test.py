"""
Simple smoke test: run one timed game and check it completes with a non-negative score.
Tests all three agents: ValueIteration, PolicyIteration, and QLearning.
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from Executer import Executor
from pacman.controllers.examples.starter_ghosts import StarterGhosts
from pacman.controllers.agents.value_iteration_agent import ValueIterationAgent
from pacman.controllers.agents.policy_iteration_agent import PolicyIterationAgent
from pacman.controllers.agents.q_learning_agent import QLearningAgent


def test_value_iteration_plays_one_game_and_finishes():
    """Test that ValueIterationAgent can play one game and finish with non-negative score."""
    exec = Executor()
    agent = ValueIterationAgent()
    score = exec.run_game_timed(agent, StarterGhosts(), False)
    assert score >= 0, "ValueIterationAgent score should be >= 0"
    print(f"ValueIterationAgent smoke test score: {score:.2f}")


def test_policy_iteration_plays_one_game_and_finishes():
    """Test that PolicyIterationAgent can play one game and finish with non-negative score."""
    exec = Executor()
    agent = PolicyIterationAgent()
    score = exec.run_game_timed(agent, StarterGhosts(), False)
    assert score >= 0, "PolicyIterationAgent score should be >= 0"
    print(f"PolicyIterationAgent smoke test score: {score:.2f}")


def test_q_learning_plays_one_game_and_finishes():
    """Test that QLearningAgent can play one game and finish with non-negative score."""
    exec = Executor()
    agent = QLearningAgent()
    score = exec.run_game_timed(agent, StarterGhosts(), False)
    assert score >= 0, "QLearningAgent score should be >= 0"
    print(f"QLearningAgent smoke test score: {score:.2f}")


if __name__ == "__main__":
    print("\n=== Running Smoke Tests ===\n")
    print('*'*150)
    print("Testing ValueIterationAgent...")
    test_value_iteration_plays_one_game_and_finishes()
    
    print('*'*150)
    print("\nTesting PolicyIterationAgent...")
    test_policy_iteration_plays_one_game_and_finishes()
    
    print('*'*150)
    print("\nTesting QLearningAgent...")
    test_q_learning_plays_one_game_and_finishes()
    
    print('*'*150)
    print("\n=== All Smoke Tests Passed ===")
