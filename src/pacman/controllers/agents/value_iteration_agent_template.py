from __future__ import annotations

from typing import Dict, List

from pacman.controllers.controller import Controller
from pacman.game.constants import MOVE
from pacman.game.game import Game

from .game_state import GameState
from .state_generator import StateGenerator
from .transition import Transition


class ValueIterationAgent(Controller[MOVE]):
    """
    ValueIterationAgent — template summary:
    Initialize: generate your abstract state space, set V(s)=0, and set policy(s)=MOVE.NEUTRAL.
    Repeat for a fixed number of sweeps:
    1. For each state, enumerate legal actions.
    2. For each action, evaluate the expectation of r + γ·V(s′) over all transitions returned by the model.
    3. Store the best value and action into fresh maps and replace the old ones at the end of the sweep.
    Acting: map the live game to a GameState and return policy(state), falling back to MOVE.NEUTRAL when the state was never seen.
    """

    def __init__(self) -> None:
        super.__init__()
        """Use StateGenerator.getAllStates() to build the abstract state list, then initialize V(s) and run the iterative backups described above."""
        self.value_function: Dict[GameState, float] = {}
        self.policy: Dict[GameState, MOVE] = {}
        self.gamma: float = 0.9
        self.iterations: int = 20
        self.states: List[GameState] = []

    def _get_move(self, game: Game, time_due: int) -> MOVE:
        """Map the current Game into a GameState and read the action from the policy map."""
        return MOVE.NEUTRAL
