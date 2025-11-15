"""
Policy quality tests for all three agents: ValueIteration, PolicyIteration, and QLearning.
Each test verifies that the trained agent outperforms a random baseline agent.
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from typing import Dict
from Executer import Executor
from pacman.controllers.controller import Controller
from pacman.controllers.examples.starter_ghosts import StarterGhosts
from pacman.controllers.examples.random_pacman import RandomPacMan
from pacman.controllers.agents.value_iteration_agent import ValueIterationAgent
from pacman.controllers.agents.policy_iteration_agent import PolicyIterationAgent
from pacman.controllers.agents.q_learning_agent import QLearningAgent
from pacman.game.constants import MOVE, GHOST


def evaluate_agent(exec: Executor, agent: Controller[MOVE], ghosts: Controller[Dict[GHOST, MOVE]], num_games: int) -> float:
    """
    Evaluates an agent over multiple games and returns the average score.
    
    :param exec: The executor instance
    :param agent: The agent to evaluate
    :param ghosts: The ghost controller
    :param num_games: Number of games to run
    :return: Average score across all games
    """
    total_score = 0
    
    for i in range(num_games):
        print(f"Game {i+1}/{num_games}")
        score = exec.run_game_timed(agent, ghosts, False)
        total_score += score
    
    return total_score / float(num_games)


def test_value_iteration_outperforms_random():
    """Test that ValueIterationAgent outperforms a random agent."""
    exec = Executor()
    agent = ValueIterationAgent()
    random_agent = RandomPacMan()
    
    print("\n=== ValueIteration Policy Quality Test ===")
    
    # Evaluate both agents
    print('test number: 1')
    trained_score = evaluate_agent(exec, agent, StarterGhosts(), 30)
    print('test number: 2')
    random_score = evaluate_agent(exec, random_agent, StarterGhosts(), 30)
    
    print(f"ValueIteration score: {trained_score:.2f}")
    print(f"Random agent score: {random_score:.2f}")
    improvement_pct = ((trained_score - random_score) / random_score * 100) if random_score > 0 else 0
    print(f"Improvement: {trained_score - random_score:.2f} ({improvement_pct:.1f}%)")
    
    assert trained_score > random_score, "ValueIterationAgent should outperform random agent"


def test_policy_iteration_outperforms_random():
    """Test that PolicyIterationAgent outperforms a random agent."""
    exec = Executor()
    agent = PolicyIterationAgent()
    random_agent = RandomPacMan()
    
    print("\n=== PolicyIteration Policy Quality Test ===")
    
    # Evaluate both agents
    print('test number: 1')
    trained_score = evaluate_agent(exec, agent, StarterGhosts(), 30)
    print('test number: 2')
    random_score = evaluate_agent(exec, random_agent, StarterGhosts(), 30)
    
    print(f"PolicyIteration score: {trained_score:.2f}")
    print(f"Random agent score: {random_score:.2f}")
    improvement_pct = ((trained_score - random_score) / random_score * 100) if random_score > 0 else 0
    print(f"Improvement: {trained_score - random_score:.2f} ({improvement_pct:.1f}%)")
    
    assert trained_score > random_score, "PolicyIterationAgent should outperform random agent"


def test_q_learning_outperforms_random():
    """Test that QLearningAgent outperforms a random agent."""
    exec = Executor()
    agent = QLearningAgent()
    random_agent = RandomPacMan()
    
    print("\n=== QLearning Policy Quality Test ===")
    
    # Evaluate both agents
    print('test number: 1')
    trained_score = evaluate_agent(exec, agent, StarterGhosts(), 30)
    print('test number: 2')
    random_score = evaluate_agent(exec, random_agent, StarterGhosts(), 30)
    
    print(f"QLearning score: {trained_score:.2f}")
    print(f"Random agent score: {random_score:.2f}")
    improvement_pct = ((trained_score - random_score) / random_score * 100) if random_score > 0 else 0
    print(f"Improvement: {trained_score - random_score:.2f} ({improvement_pct:.1f}%)")
    
    assert trained_score > random_score, "QLearningAgent should outperform random agent"


if __name__ == "__main__":
    print("\n=== Running Policy Quality Tests ===\n")
    
    print("Testing ValueIterationAgent vs Random...")
    test_value_iteration_outperforms_random()
    
    print("\nTesting PolicyIterationAgent vs Random...")
    test_policy_iteration_outperforms_random()
    
    print("\nTesting QLearningAgent vs Random...")
    test_q_learning_outperforms_random()
    
    print("\n=== All Policy Quality Tests Passed ===")
