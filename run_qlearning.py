#!/usr/bin/env python3
"""
Simple script to run PacMan with Q-Learning Agent
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from Executer import Executor
from pacman.controllers.agents.q_learning_agent import QLearningAgent
from pacman.controllers.examples.starter_ghosts import StarterGhosts


def run_qlearning_agent(visual=True, episodes=5):
    """
    Run PacMan game with Q-Learning Agent

    Args:
        visual (bool): Whether to show visual game window
        episodes (int): Number of training episodes for Q-learning
    """
    print("=== PacMan Q-Learning Agent ===")
    print(f"Training episodes: {episodes}")
    print(f"Visual mode: {visual}")
    print()

    # Create executor and agents
    executor = Executor()
    pacman_agent = QLearningAgent()
    ghost_agent = StarterGhosts()

    print("Q-Learning Agent training completed!")
    print("Starting game...")

    if visual:
        print("Visual mode: ON - Game window will open")
        print("Close the game window to end the program")
    else:
        print("Visual mode: OFF - Running in console only")

    # Run the game
    score = executor.run_game_timed(pacman_agent, ghost_agent, visual)

    print(f"\nFinal Score: {score}")
    print("Game completed!")


def run_multiple_games(num_games=5):
    """Run multiple games and show average performance"""
    print(f"=== Running {num_games} games with Q-Learning Agent ===")

    executor = Executor()
    total_score = 0

    for i in range(num_games):
        print(f"\n--- Game {i+1}/{num_games} ---")
        pacman_agent = QLearningAgent()
        ghost_agent = StarterGhosts()
        score = executor.run_game_timed(pacman_agent, ghost_agent, False)
        total_score += score
        print(f"Game {i+1} Score: {score}")

    avg_score = total_score / num_games
    print(f"\n=== Results ===")
    print(f"Average Score over {num_games} games: {avg_score}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Run PacMan with Q-Learning Agent')
    parser.add_argument('--no-visual', action='store_true',
                       help='Run without visual window (console only)')
    parser.add_argument('--episodes', type=int, default=5,
                       help='Number of training episodes (default: 5)')
    parser.add_argument('--games', type=int, default=1,
                       help='Number of games to run (default: 1)')
    parser.add_argument('--batch', action='store_true',
                       help='Run multiple games and show average performance')

    args = parser.parse_args()

    visual = not args.no_visual

    if args.batch:
        run_multiple_games(args.games)
    else:
        run_qlearning_agent(visual, args.episodes)
