from __future__ import annotations

from typing import Dict, List

from pacman.controllers.controller import Controller
from pacman.game.constants import MOVE
from pacman.game.game import Game

from .game_state import GameState
from .state_generator import StateGenerator
from .transition import Transition

"""
PolicyIterationAgent — template summary:
Init: enumerate states, set V(s)=0, and assign a random legal MOVE to policy(s).
Repeat until policy is stable or the iteration cap is reached:
1. Policy Evaluation: for each state, update V(s)=E[r + γ·V(s′)] using the current action and run a few sweeps.
2. Policy Improvement: for each state, set policy(s)=argmax Σ p·(r + γ·V(s′)) and mark stability only if no action changes.
Acting: convert the live game into a GameState and return the stored action (fallback MOVE.NEUTRAL when the state is unknown).
"""
class PolicyIterationAgent(Controller[MOVE]):
    def __init__(self):
        super.__init__()
        """Generate all states, initialize the policy randomly, and alternate evaluation and improvement until convergence or maxIterations."""
        self.policy: Dict[GameState, MOVE] = {}
        self.value_function: Dict[GameState, float] = {}
        self.gamma: float = 0.9
        self.max_iterations: int = 20


    def _policy_evaluation(self, states: List[GameState]) -> None:
        """Run several sweeps updating V(s) with expectations under the current policy choice."""
        pass


    def _policy_improvement(self, states: List[GameState]) -> bool:
        """For each state, pick the action that maximizes expected return and report whether any action changed."""
        return False

    def _get_move(self, game: Game, time_due: int) -> MOVE:
        """Map Game to GameState and return policy.getOrDefault(..., MOVE.NEUTRAL)."""
        return MOVE.NEUTRAL
