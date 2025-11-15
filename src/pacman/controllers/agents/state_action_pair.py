from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING
from pacman.game.constants import MOVE

if TYPE_CHECKING:
    from .game_state import GameState


@dataclass(frozen=True)
class StateActionPair:
    state: 'GameState'
    action: MOVE
