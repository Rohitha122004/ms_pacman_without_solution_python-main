#!/usr/bin/env python3
"""
Direct usage of the original Q-Learning Agent
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from Executer import Executor
from pacman.controllers.agents.q_learning_agent import QLearningAgent
from pacman.controllers.examples.starter_ghosts import StarterGhosts


def run_original_qlearning(visual=True):
    """
    Run the original QLearningAgent directly
    """
    print("=== Using Original Q-Learning Agent ===")
    print("Agent location: src/pacman/controllers/agents/q_learning_agent.py")
    print()

    # The agent automatically trains during initialization
    print("Creating QLearningAgent (this includes training)...")
    agent = QLearningAgent()

    print(f"Training completed! Q-table size: {len(agent.q_table)} states")
    print(f"Agent parameters: episodes={agent.episodes}, alpha={agent.alpha}, gamma={agent.gamma}, epsilon={agent.epsilon}")
    print()

    # Create executor and ghosts
    executor = Executor()
    ghosts = StarterGhosts()

    print("Starting game...")
    if visual:
        print("Visual mode: ON - Close window to end")
    else:
        print("Visual mode: OFF - Console only")

    # Run the game
    score = executor.run_game_timed(agent, ghosts, visual)
    print(f"\nFinal Score: {score}")
    return score


def create_custom_trained_agent(episodes=10, alpha=0.2, gamma=0.95, epsilon=0.05):
    """
    Create a QLearningAgent with custom parameters by modifying it after creation
    """
    print(f"=== Custom Q-Learning Agent (episodes={episodes}, alpha={alpha}, gamma={gamma}, epsilon={epsilon}) ===")

    # Create the agent (trains with default parameters first)
    agent = QLearningAgent()

    # Modify parameters and retrain
    agent.episodes = episodes
    agent.alpha = alpha
    agent.gamma = gamma
    agent.epsilon = epsilon

    # Clear the old Q-table and retrain
    agent.q_table.clear()
    print("Retraining with new parameters...")
    agent.train()

    print(f"Training completed! Q-table size: {len(agent.q_table)} states")
    return agent


def run_multiple_games_with_original_agent(num_games=5):
    """Test the original agent over multiple games"""
    print(f"=== Testing Original Q-Learning Agent over {num_games} games ===")

    executor = Executor()
    ghosts = StarterGhosts()
    scores = []

    for i in range(num_games):
        print(f"\n--- Game {i+1}/{num_games} ---")
        agent = QLearningAgent()  # Creates and trains a new agent each time
        score = executor.run_game_timed(agent, ghosts, False)
        scores.append(score)
        print(f"Game {i+1} Score: {score}")

    avg_score = sum(scores) / len(scores)
    print(f"\n=== Results ===")
    print(f"Average Score: {avg_score:.2f}")
    print(f"Best Score: {max(scores):.2f}")
    print(f"Worst Score: {min(scores):.2f}")


def demonstrate_agent_reuse():
    """Show that you can reuse a trained agent without retraining"""
    print("=== Agent Reuse Demonstration ===")

    # Create and train agent once
    print("Creating and training agent once...")
    agent = QLearningAgent()
    original_qtable_size = len(agent.q_table)

    print(f"Initial training completed. Q-table size: {original_qtable_size}")

    # Reuse the same agent for multiple games
    executor = Executor()
    ghosts = StarterGhosts()

    print("\nReusing the same trained agent for multiple games:")
    for i in range(3):
        score = executor.run_game_timed(agent, ghosts, False)
        print(f"Game {i+1} Score: {score} (Q-table size: {len(agent.q_table)})")

    print(f"\nAgent reused without retraining. Q-table size remained: {original_qtable_size}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Use the Original Q-Learning Agent')
    parser.add_argument('--no-visual', action='store_true', help='Run without visuals')
    parser.add_argument('--games', type=int, default=1, help='Number of games to run')
    parser.add_argument('--custom', action='store_true', help='Use custom parameters')
    parser.add_argument('--episodes', type=int, default=10, help='Custom episodes')
    parser.add_argument('--alpha', type=float, default=0.2, help='Custom learning rate')
    parser.add_argument('--gamma', type=float, default=0.95, help='Custom discount factor')
    parser.add_argument('--epsilon', type=float, default=0.05, help='Custom exploration rate')
    parser.add_argument('--test-multiple', action='store_true', help='Test over multiple games')
    parser.add_argument('--reuse-demo', action='store_true', help='Demonstrate agent reuse')

    args = parser.parse_args()

    if args.reuse_demo:
        demonstrate_agent_reuse()
    elif args.test_multiple:
        run_multiple_games_with_original_agent(args.games)
    elif args.custom:
        agent = create_custom_trained_agent(args.episodes, args.alpha, args.gamma, args.epsilon)
        executor = Executor()
        ghosts = StarterGhosts()
        score = executor.run_game_timed(agent, ghosts, not args.no_visual)
        print(f"\nCustom Agent Final Score: {score}")
    else:
        run_original_qlearning(not args.no_visual)
