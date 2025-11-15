from __future__ import annotations

import random
from typing import Dict

from pacman.controllers.controller import Controller
from pacman.game.constants import MOVE
from pacman.game.game import Game
from pacman.controllers.examples.starter_ghosts import StarterGhosts

from .game_state import GameState
from .state_action_pair import StateActionPair

"""
QLearningAgent — minimal summary:
Init: start with an empty Q-table. Use α = 0.1, γ = 0.9, ε = 0.1, and run for 5 training episodes.
Training loop per step:
1. Map the Game to your GameState and gather legal actions.
2. ε-greedy: with probability ε choose a random action, else take argmax Q(s,a).
3. Clone the game, advance one tick using the chosen MOVE against StarterGhosts.
4. Reward r = score(s′) − score(s).
5. Update Q(s,a) ← Q(s,a) + α · [r + γ · max_{a′} Q(s′,a′) − Q(s,a)].
6. Continue from the next state until the game ends.
Acting: convert the live game into a GameState and return the MOVE with the highest learned Q-value
(fallback MOVE.NEUTRAL if ties or unseen).
"""

class QLearningAgent(Controller[MOVE]):
    def __init__(self):
        """Run the template training routine immediately upon construction."""
        super().__init__()
        self.q_table: Dict[StateActionPair, float] = {}
        self.alpha: float = 0.1
        self.gamma: float = 0.9
        self.epsilon: float = 0.1
        self.episodes: int = 5
        self.train()

    def train(self) -> None:
        """Implement the episodic training loop described in the class comment."""
        return None

    def get_best_action(self, s: GameState) -> MOVE:
        """Return the action with the highest Q-value for the provided state."""
        return MOVE.NEUTRAL

    def get_max_q(self, s: GameState) -> float:
        """Helper for max_{a} Q(s,a) used inside the TD update."""
        return 0.0

    def _get_move(self, game: Game, time_due: int) -> MOVE:
        """Convert the runtime Game into a GameState and exploit the learned policy."""
        return MOVE.NEUTRAL
