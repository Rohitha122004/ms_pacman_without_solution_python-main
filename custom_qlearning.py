#!/usr/bin/env python3
"""
Customizable Q-Learning Agent for PacMan
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from pacman.controllers.agents.q_learning_agent import QLearningAgent


class CustomQLearningAgent(QLearningAgent):
    """Customizable Q-Learning Agent with adjustable parameters"""

    def __init__(self, episodes=5, alpha=0.1, gamma=0.9, epsilon=0.1):
        """
        Initialize Custom Q-Learning Agent

        Args:
            episodes (int): Number of training episodes
            alpha (float): Learning rate (0 < alpha <= 1)
            gamma (float): Discount factor (0 <= gamma <= 1)
            epsilon (float): Exploration rate (0 <= epsilon <= 1)
        """
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.episodes = episodes

        # Initialize parent class without training
        super(QLearningAgent, self).__init__()

        # Override parameters and retrain
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.episodes = episodes
        self.train()

    def __str__(self):
        return (f"CustomQLearningAgent(episodes={self.episodes}, "
                f"alpha={self.alpha}, gamma={self.gamma}, epsilon={self.epsilon})")


def demonstrate_parameter_effects():
    """Show how different parameters affect performance"""
    print("=== Q-Learning Parameter Effects ===")
    print("This demonstrates how different parameter settings affect the agent:")
    print()

    from Executer import Executor
    from pacman.controllers.examples.starter_ghosts import StarterGhosts

    executor = Executor()
    ghosts = StarterGhosts()

    # Test different parameter combinations
    parameter_sets = [
        {"episodes": 1, "alpha": 0.1, "gamma": 0.9, "epsilon": 0.1, "name": "Quick Learning"},
        {"episodes": 10, "alpha": 0.1, "gamma": 0.9, "epsilon": 0.1, "name": "More Training"},
        {"episodes": 5, "alpha": 0.5, "gamma": 0.9, "epsilon": 0.1, "name": "High Learning Rate"},
        {"episodes": 5, "alpha": 0.1, "gamma": 0.5, "epsilon": 0.1, "name": "Low Discount"},
        {"episodes": 5, "alpha": 0.1, "gamma": 0.9, "epsilon": 0.3, "name": "High Exploration"},
    ]

    for params in parameter_sets:
        print(f"\n--- Testing: {params['name']} ---")
        agent = CustomQLearningAgent(**params)
        score = executor.run_game_timed(agent, ghosts, False)
        print(f"Average Score: {score".2f"}")
        print(f"Q-table size: {len(agent.q_table)} states")


if __name__ == "__main__":
    # Example usage
    print("Custom Q-Learning Agent Examples")
    print("=" * 40)

    # Create a custom agent with different parameters
    custom_agent = CustomQLearningAgent(
        episodes=10,    # More training
        alpha=0.2,      # Higher learning rate
        gamma=0.95,     # Higher discount factor
        epsilon=0.05    # Lower exploration (more greedy)
    )

    print(f"Created: {custom_agent}")
    print("This agent will train for 10 episodes with higher learning rate and lower exploration.")

    print("\nTo run parameter comparison:")
    print("python custom_qlearning.py --compare")

    import sys
    if "--compare" in sys.argv:
        demonstrate_parameter_effects()
