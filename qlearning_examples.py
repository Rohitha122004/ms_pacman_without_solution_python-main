#!/usr/bin/env python3
"""
Simple examples showing how to use the original Q-Learning Agent
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from Executer import Executor
from pacman.controllers.agents.q_learning_agent import QLearningAgent
from pacman.controllers.examples.starter_ghosts import StarterGhosts


def example_1_basic_usage():
    """Example 1: Basic usage with visual game"""
    print("=== Example 1: Basic Visual Game ===")

    # Create agents
    pacman = QLearningAgent()  # Automatically trains during creation
    ghosts = StarterGhosts()
    executor = Executor()

    print(f"Agent trained! Q-table size: {len(pacman.q_table)}")
    print("Starting visual game... (close window to continue)")

    # Run visual game
    score = executor.run_game_timed(pacman, ghosts, visual=False)
    print(f"Final Score: {score}")
    return score


def example_2_console_mode():
    """Example 2: Console mode (faster)"""
    print("\n=== Example 2: Console Mode ===")

    pacman = QLearningAgent()
    ghosts = StarterGhosts()
    executor = Executor()

    print("Running in console mode (no visuals)...")
    score = executor.run_game_timed(pacman, ghosts, visual=False)
    print(f"Final Score: {score}")
    return score


def example_3_custom_parameters():
    """Example 3: Custom parameters"""
    print("\n=== Example 3: Custom Parameters ===")

    # Create agent with default parameters first
    agent = QLearningAgent()
    print(f"Default training completed. Q-table size: {len(agent.q_table)}")

    # Modify parameters and retrain
    print("Modifying parameters: episodes=15, alpha=0.3, epsilon=0.05")
    agent.episodes = 15
    agent.alpha = 0.3
    agent.epsilon = 0.05

    # Clear old Q-table and retrain
    agent.q_table.clear()
    agent.train()

    print(f"Custom training completed. Q-table size: {len(agent.q_table)}")

    # Test the custom agent
    executor = Executor()
    ghosts = StarterGhosts()
    score = executor.run_game_timed(agent, ghosts, visual=False)
    print(f"Custom Agent Score: {score}")
    return score


def example_4_agent_reuse():
    """Example 4: Reusing trained agent"""
    print("\n=== Example 4: Agent Reuse ===")

    # Train agent once
    print("Training agent once...")
    agent = QLearningAgent()
    original_size = len(agent.q_table)
    print(f"Initial training complete. Q-table size: {original_size}")

    # Reuse for multiple games
    executor = Executor()
    ghosts = StarterGhosts()

    print("\nReusing same agent for 3 games:")
    scores = []
    for i in range(3):
        score = executor.run_game_timed(agent, ghosts, visual=False)
        scores.append(score)
        print(f"Game {i+1}: Score {score} (Q-table still: {len(agent.q_table)})")

    print(f"\nResults: Min={min(scores)}, Max={max(scores)}, Avg={sum(scores)/len(scores):.1f}")
    print(f"Q-table size unchanged: {len(agent.q_table)} (no retraining needed)")


def example_5_batch_testing():
    """Example 5: Batch testing multiple agents"""
    print("\n=== Example 5: Batch Testing ===")

    executor = Executor()
    ghosts = StarterGhosts()
    num_tests = 5

    print(f"Testing {num_tests} different Q-learning agents:")

    scores = []
    for i in range(num_tests):
        agent = QLearningAgent()  # Each agent trains independently
        score = executor.run_game_timed(agent, ghosts, visual=False)
        scores.append(score)
        print(f"Agent {i+1}: Score {score}, Q-table size: {len(agent.q_table)}")

    print(f"\nBatch Results: Avg={sum(scores)/len(scores):.1f}, Best={max(scores)}, Worst={min(scores)}")


if __name__ == "__main__":
    print("Q-Learning Agent Usage Examples")
    print("=" * 40)

    # Run examples based on command line arguments
    if len(sys.argv) > 1:
        example_num = int(sys.argv[1])
        examples = [example_1_basic_usage, example_2_console_mode, example_3_custom_parameters,
                   example_4_agent_reuse, example_5_batch_testing]

        if 1 <= example_num <= len(examples):
            examples[example_num - 1]()
        else:
            print(f"Example {example_num} not found. Choose 1-{len(examples)}")
    else:
        # Run all examples
        example_1_basic_usage()
        example_2_console_mode()
        example_3_custom_parameters()
        example_4_agent_reuse()
        example_5_batch_testing()

        print("\n=== All Examples Complete ===")
        print("Run with 'python qlearning_examples.py <number>' to run a specific example")
