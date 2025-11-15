from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .game_state import GameState


@dataclass(frozen=True)
class Transition:
    next_state: 'GameState'
    probability: float
    reward: float
