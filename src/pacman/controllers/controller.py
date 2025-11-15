# src/pacman/controllers/controller.py

from abc import ABC, abstractmethod
from threading import Thread
# <-- IMPORT Generic and TypeVar
from typing import Any, Optional, TypeVar, Generic
from pacman.game.game import Game

T = TypeVar('T')  # <-- CREATE a type variable


class Controller(Generic[T], ABC, Thread):  # <-- MAKE the class generic
    """
    Abstract base class for controllers, running as a thread. Subclasses must implement get_move().
    Provides methods for the Executor to use the controller in various execution modes.
    """

    def __init__(self):
        super().__init__()
        # print('controller init')
        self.alive: bool = True
        self.was_signalled: bool = False
        self.has_computed: bool = False
        self.thread_still_running: bool = False
        self.time_due: int = 0
        self.game: Optional[Game] = None
        # Stores the last computed move (MOVE for Pac-Man, EnumMap for ghosts)
        self.last_move: Optional[T] = None  # <-- UPDATE type hint to use T

    def terminate(self) -> None:
        """
        Terminates the controller by setting alive to False and notifying the thread.
        """
        self.alive = False
        self.was_signalled = True
        # The original code's synchronization logic might need a Condition object.
        # For now, this addresses the primary error.

    def update(self, game: Game, time_due: int) -> None:
        """
        Updates the game state with a copy of the current game and the time the next move is due.

        :param game: A copy of the current game.
        :param time_due: The time the next move is due.
        """
        self.game = game
        self.time_due = time_due
        self.was_signalled = True
        self.has_computed = False

    def get_move(self) -> Optional[T]:  # <-- UPDATE type hint
        """
        Retrieves the last computed move.

        :return: The move stored in last_move.
        """
        return self.last_move

    def has_computed(self) -> bool:
        """
        Checks whether the controller computed a move since the last update.

        :return: True if a move was computed, False otherwise.
        """
        return self.has_computed

    def run(self) -> None:
        """
        Thread execution loop. Runs until terminate() is called.
        Computes moves in a separate thread when signalled.
        """
        # This loop's synchronization logic might also need review,
        # but let's solve one problem at a time.
        print('Controller: run')
        while self.alive:
            if self.was_signalled:
                if not self.thread_still_running:
                    def compute_move():
                        self.thread_still_running = True
                        if self.game is not None:
                           self.last_move = self._get_move(
                               self.game, self.time_due)
                        self.has_computed = True
                        self.thread_still_running = False

                    Thread(target=compute_move).start()
                self.was_signalled = False

    @abstractmethod
    def _get_move(self, game: Game, time_due: int) -> T:  # <-- UPDATE type hint
        """
        Abstract method to compute the next move. Must be implemented by subclasses.

        :param game: A copy of the current game.
        :param time_due: The time the next move is due.
        :return: The computed move (MOVE for Pac-Man, EnumMap for ghosts).
        """
        # return self.last_move
        raise NotImplementedError("Subclasses must implement _get_move")
        print('pass _get move')
        pass
