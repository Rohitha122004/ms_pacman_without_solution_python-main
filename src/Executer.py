# src/pacman/executor.py

import random
import threading
import time
from typing import Dict, List, Optional
from pacman.game.constants import MOVE, GHOST, DELAY, INTERVAL_WAIT
from pacman.game.game import Game
from pacman.game.game_view import GameView
from pacman.controllers.controller import Controller
from pacman.controllers.human_controller import HumanController
from pacman.controllers.keyboard_input import KeyBoardInput
from pacman.controllers.examples.aggressive_ghosts import AggressiveGhosts
from pacman.controllers.examples.legacy import Legacy
from pacman.controllers.examples.legacy2_the_reckoning import Legacy2TheReckoning
from pacman.controllers.examples.nearest_pill_pacman import NearestPillPacMan
from pacman.controllers.examples.nearest_pill_pacman_vs import NearestPillPacManVS
from pacman.controllers.examples.random_ghosts import RandomGhosts
from pacman.controllers.examples.random_non_rev_pacman import RandomNonRevPacMan
from pacman.controllers.examples.random_pacman import RandomPacMan
from pacman.controllers.examples.starter_ghosts import StarterGhosts
from pacman.controllers.examples.starter_pacman import StarterPacMan
from pacman.controllers.agents.q_learning_agent import QLearningAgent
from data_recording.data_collector_controller import DataCollectorController


class Executor:
    def run_experiment(self, pacman_controller: Controller[MOVE], ghost_controller: Controller[Dict[GHOST, MOVE]], trials: int):
        # ... (This function remains the same)
        avg_score = 0
        rnd = random.Random(0)

        for i in range(trials):
            game = Game(rnd.randint(0, 2**32 - 1))
            while not game.game_over():
                game.advance_game(
                    pacman_controller.get_move(
                        game.copy(), time.time() * 1000 + DELAY),
                    ghost_controller.get_move(
                        game.copy(), time.time() * 1000 + DELAY)
                )
            avg_score += game.get_score()
            print(f"{i}\t{game.get_score()}")

        print(avg_score / trials)

    def run_game(self, pacman_controller: Controller[MOVE], ghost_controller: Controller[Dict[GHOST, MOVE]], visual: bool, delay: int):
        """
        Runs a game in synchronous mode with optional visuals and delay.
        """
        print("[DEBUG] --- Starting run_game() - visual:---", visual)
        game = Game(0)
        print("[DEBUG] Game created. Object: ", game)
        gv = None

        if visual:
            print("[DEBUG] Visual mode is ON. Creating GameView...")
            gv = GameView(game).show_game()
            print(f"[DEBUG] GameView created. Object: {gv}")
            if gv.root is None:
                print(
                    "[ERROR] gv.root is None! The window was not created correctly.")
                return  # Exit if the window object doesn't exist

            print(f"[DEBUG] Window object (gv.root): {gv.root}")

            if isinstance(pacman_controller, HumanController):
                print("[DEBUG] HumanController detected. Binding keys...")
                gv.get_frame().bind_keys(pacman_controller.get_keyboard_input())
                print("[DEBUG] Keys bound.")

            def update_game():
                # This print can be spammy, but it's useful to see if the loop runs at all
                # print("[DEBUG] update_game() tick...")
                if not game.game_over():
                    # Compute moves synchronously for this frame
                    current_time_ms = int(time.time() * 1000)
                    pac_move = pacman_controller._get_move(game.copy(), current_time_ms + DELAY)
                    # ghost_moves = ghost_controller._get_move(game.copy(), current_time_ms + DELAY)
                    # Keep controller state consistent
                    pacman_controller.last_move = pac_move
                    # ghost_controller.last_move = ghost_moves
                    game.advance_game(pac_move, ghost_controller.get_move())
                    gv.render()
                    gv.root.after(delay, update_game)
                else:
                    print("[DEBUG] Game is over. Window should close soon.")

            print("[DEBUG] Setting up the first call to update_game().")
            gv.root.after(0, update_game)

            print("[DEBUG] --- Calling mainloop() now. The window should appear. ---")
            gv.root.mainloop()
            print("[DEBUG] --- mainloop() has finished. Program is ending. ---")

        else:
            print("[DEBUG] Visual mode is OFF. Running game logic only.")
            while not game.game_over():
                pac_move = pacman_controller._get_move(game.copy(), -1)
                ghost_moves = ghost_controller._get_move(game.copy(), -1)
                pacman_controller.last_move = pac_move
                ghost_controller.last_move = ghost_moves
                game.advance_game(pac_move, ghost_moves)
                pac_move = pacman_controller._get_move(game.copy(), -1)
                ghost_moves = ghost_controller._get_move(game.copy(), -1)
                pacman_controller.last_move = pac_move
                ghost_controller.last_move = ghost_moves
                game.advance_game(pac_move, ghost_moves)
                time.sleep(delay / 1000.0)

    # --- Other methods (run_game_timed, etc.) are unchanged ---
    # ... (rest of the class methods) ...
    def run_game_timed(self, pacman_controller: Controller[MOVE], ghost_controller: Controller[Dict[GHOST, MOVE]], visual: bool) -> float:
        """
        Runs a game in asynchronous mode with a time limit.

        :param pacman_controller: The Pac-Man controller.
        :param ghost_controller: The Ghosts controller.
        :param visual: Whether to use visuals.
        :return: The final game score.
        """
        game = Game(0)
        gv = None

        if visual:
            gv = GameView(game).show_game()
            if isinstance(pacman_controller, HumanController):
                gv.get_frame().bind_keys(pacman_controller.get_keyboard_input())

            def update_game():
                if not game.game_over():
                    pacman_controller.update(
                        game.copy(), time.time() * 100 + DELAY)
                    ghost_controller.update(
                        game.copy(), time.time() * 100 + DELAY)
                    game.advance_game(
                        pacman_controller.get_move(), ghost_controller.get_move())
                    gv.render()
                    gv.root.after(DELAY, update_game)

            pacman_thread = threading.Thread(target=pacman_controller.run)
            ghost_thread = threading.Thread(target=ghost_controller.run)
            pacman_thread.start()
            ghost_thread.start()
            gv.root.after(0, update_game)
            gv.root.mainloop()
            pacman_controller.terminate()
            ghost_controller.terminate()

            return game.get_score()

        else:
            pacman_thread = threading.Thread(target=pacman_controller.run)
            ghost_thread = threading.Thread(target=ghost_controller.run)
            pacman_thread.start()
            ghost_thread.start()

            while not game.game_over():
                pacman_controller.update(
                    game.copy(), time.time() * 100 + DELAY)
                ghost_controller.update(
                    game.copy(), time.time() * 100 + DELAY)
                time.sleep(DELAY / 1000.0)
                game.advance_game(pacman_controller.get_move(),
                                  ghost_controller.get_move())

            pacman_controller.terminate()
            ghost_controller.terminate()
            return game.get_score()

    def run_game_timed_speed_optimised(self, pacman_controller: Controller[MOVE], ghost_controller: Controller[Dict[GHOST, MOVE]], fixed_time: bool, visual: bool):
        """
        Runs a game in asynchronous mode, proceeding as soon as both controllers reply, with a time limit.

        :param pacman_controller: The Pac-Man controller.
        :param ghost_controller: The Ghosts controller.
        :param fixed_time: Whether to wait for the full 40ms even if controllers responded.
        :param visual: Whether to use visuals.
        """
        game = Game(0)
        gv = None

        if visual:
            gv = GameView(game).show_game()
            if isinstance(pacman_controller, HumanController):
                gv.get_frame().bind_keys(pacman_controller.get_keyboard_input())

            def update_game():
                if not game.game_over():
                    pacman_controller.update(
                        game.copy(), time.time() * 100 + DELAY)
                    ghost_controller.update(
                        game.copy(), time.time() * 100 + DELAY)
                    waited = DELAY // INTERVAL_WAIT
                    for j in range(DELAY // INTERVAL_WAIT):
                        time.sleep(INTERVAL_WAIT / 1000.0)
                        if pacman_controller.has_computed() and ghost_controller.has_computed():
                            waited = j
                            break
                    if fixed_time:
                        time.sleep(((DELAY // INTERVAL_WAIT) - waited)
                                   * INTERVAL_WAIT / 1000.0)
                    game.advance_game(
                        pacman_controller.get_move(), ghost_controller.get_move())
                    gv.render()
                    gv.root.after(DELAY, update_game)

            pacman_thread = threading.Thread(target=pacman_controller.run)
            ghost_thread = threading.Thread(target=ghost_controller.run)
            pacman_thread.start()
            ghost_thread.start()
            gv.root.after(0, update_game)
            gv.root.mainloop()
            pacman_controller.terminate()
            ghost_controller.terminate()

        else:
            pacman_thread = threading.Thread(target=pacman_controller.run)
            ghost_thread = threading.Thread(target=ghost_controller.run)
            pacman_thread.start()
            ghost_thread.start()

            while not game.game_over():
                pacman_controller.update(
                    game.copy(), time.time() * 100 + DELAY)
                ghost_controller.update(
                    game.copy(), time.time() * 100 + DELAY)
                waited = DELAY // INTERVAL_WAIT
                for j in range(DELAY // INTERVAL_WAIT):
                    time.sleep(INTERVAL_WAIT / 1000.0)
                    if pacman_controller.has_computed() and ghost_controller.has_computed():
                        waited = j
                        break
                if fixed_time:
                    time.sleep(((DELAY // INTERVAL_WAIT) - waited)
                               * INTERVAL_WAIT / 1000.0)
                game.advance_game(pacman_controller.get_move(),
                                  ghost_controller.get_move())

            pacman_controller.terminate()
            ghost_controller.terminate()

    def run_game_timed_recorded(self, pacman_controller: Controller[MOVE], ghost_controller: Controller[Dict[GHOST, MOVE]], visual: bool, file_name: str):
        """
        Runs a game in asynchronous mode and records it to a file.

        :param pacman_controller: The Pac-Man controller.
        :param ghost_controller: The Ghosts controller.
        :param visual: Whether to use visuals.
        :param file_name: The file name to save the replay.
        """
        replay = []
        game = Game(0)
        gv = None

        if visual:
            gv = GameView(game).show_game()
            if isinstance(pacman_controller, HumanController):
                gv.get_frame().bind_keys(pacman_controller.get_keyboard_input())

            def update_game():
                if not game.game_over():
                    pacman_controller.update(
                        game.copy(), time.time() * 100 + DELAY)
                    ghost_controller.update(
                        game.copy(), time.time() * 100 + DELAY)
                    time.sleep(DELAY / 1000.0)
                    game.advance_game(
                        pacman_controller.get_move(), ghost_controller.get_move())
                    gv.render()
                    replay.append(game.get_game_state())
                    gv.root.after(DELAY, update_game)

            pacman_thread = threading.Thread(target=pacman_controller.run)
            ghost_thread = threading.Thread(target=ghost_controller.run)
            pacman_thread.start()
            ghost_thread.start()
            gv.root.after(0, update_game)
            gv.root.mainloop()
            pacman_controller.terminate()
            ghost_controller.terminate()
            self.save_to_file("\n".join(replay), file_name, False)

        else:
            pacman_thread = threading.Thread(target=pacman_controller.run)
            ghost_thread = threading.Thread(target=ghost_controller.run)
            pacman_thread.start()
            ghost_thread.start()

            while not game.game_over():
                pacman_controller.update(
                    game.copy(), time.time() * 100 + DELAY)
                ghost_controller.update(
                    game.copy(), time.time() * 100 + DELAY)
                time.sleep(DELAY / 1000.0)
                game.advance_game(pacman_controller.get_move(),
                                  ghost_controller.get_move())
                replay.append(game.get_game_state())

            pacman_controller.terminate()
            ghost_controller.terminate()
            self.save_to_file("\n".join(replay), file_name, False)

    def replay_game(self, file_name: str, visual: bool):
        """
        Replays a previously saved game.

        :param file_name: The file name of the saved game.
        :param visual: Whether to use visuals.
        """
        time_steps = self.load_replay(file_name)
        game = Game(0)
        gv = None

        if visual:
            gv = GameView(game).show_game()

            def update_game(step=0):
                if step < len(time_steps):
                    game.set_game_state(time_steps[step])
                    gv.render()
                    gv.root.after(DELAY, update_game, step + 1)

            gv.root.after(0, update_game)
            gv.root.mainloop()

        else:
            for time_step in time_steps:
                game.set_game_state(time_step)
                time.sleep(DELAY / 1000.0)

    @staticmethod
    def save_to_file(data: str, name: str, append: bool):
        """
        Saves data to a file.

        :param data: The data to save.
        :param name: The file name.
        :param append: Whether to append or overwrite the file.
        """
        try:
            with open(name, 'a' if append else 'w') as f:
                f.write(data + "\n")
        except IOError:
            print("Could not save data!")

    @staticmethod
    def load_replay(file_name: str) -> List[str]:
        """
        Loads a replay from a file.

        :param file_name: The file name of the replay.
        :return: A list of time step strings.
        """
        replay = []
        try:
            with open(file_name, 'r') as f:
                for line in f:
                    if line.strip():
                        replay.append(line.strip())
        except IOError as e:
            print(f"Error loading replay: {e}")
        return replay


def main():
    print("[DEBUG] --- Program starting, in main() ---")
    executor = Executor()
    visual = True
    delay = 40  

    ## -----------------------------------------------------------------------------------------
    ## Run multiple games in batch mode - good for testing.
    # print("[DEBUG] --- mode: experiment - batch - random ---")
    # num_trials = 10
    # executor.run_experiment(RandomPacMan(), RandomGhosts(), num_trials)

    ## -----------------------------------------------------------------------------------------
    ## Run a game in synchronous mode: game waits until controllers respond.
    # print("[DEBUG] --- mode: synchronous - random ---")
    # executor.run_game(RandomPacMan(), RandomGhosts(), visual, delay)


    ## -----------------------------------------------------------------------------------------
    ## Calling the synchronous game mode
    # print("[DEBUG] --- mode: synchronous - manual controller ---")
    # executor.run_game(HumanController(KeyBoardInput()), StarterGhosts(), visual, delay)


    ## -----------------------------------------------------------------------------------------
    ## Run the game in asynchronous mode.
    # print("[DEBUG] --- mode: asynchronous---")
    # visual = True

    # print("[DEBUG] --- mode: timed - nearest pill - aggressive ghosts ---")
    # executor.run_game_timed(NearestPillPacMan(), AggressiveGhosts(), visual)

    # print("[DEBUG] --- mode: timed - starter pac man - starter ghosts ---")
    # executor.run_game_timed(StarterPacMan(), StarterGhosts(), visual)

    # print("[DEBUG] --- mode: timed - human controller - starter ghosts ---")
    # executor.run_game_timed(HumanController(KeyBoardInput()), StarterGhosts(), visual)

    # print("[DEBUG] --- mode: timed - q learning agent - starter ghosts ---")
    visual = False
    executor.run_game_timed(QLearningAgent(), StarterGhosts(), visual)  


    ## -----------------------------------------------------------------------------------------
    ## Run the game in asynchronous mode but advance as soon as both controllers are ready.
    # visual = True
    # fixed_time = False
    # print("[DEBUG] - -- mode: timed - random pac man - random ghosts ---")
    # executor.run_game_timed_speed_optimised(RandomPacMan(), RandomGhosts(), fixed_time, visual)


    ## -----------------------------------------------------------------------------------------
    ## Run game in asynchronous mode and record it to file for replay.
    # visual = True
    # file_name = "replay.txt"
    # print("[DEBUG] --- mode: timed recorded - human controller - random ghosts ---")
    # executor.run_game_timed_recorded(HumanController(KeyBoardInput()), RandomGhosts(), visual, file_name)
    # executor.replay_game(file_name, visual)


    ## -----------------------------------------------------------------------------------------
    ## Run game for data collection
    # print("[DEBUG] --- mode: timed data collection - human controller - starter ghosts ---")
    # executor.run_game_timed(DataCollectorController(KeyBoardInput()), StarterGhosts(), visual)

    






















if __name__ == "__main__":
    main()
