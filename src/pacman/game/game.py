# from game.internal import , , ,
from pacman.game.internal.maze import Maze
from pacman.game.internal.ghost import Ghost
from pacman.game.internal.pacman import PacMan
from pacman.game.internal.node import Node
from pacman.game.internal.paths_cache import PathsCache
from pacman.game.internal.a_star import AStar
from pacman.game.constants import MOVE, GHOST, DM, PILL, POWER_PILL, GHOST_EAT_SCORE, EDIBLE_TIME, \
    EDIBLE_TIME_REDUCTION, LAIR_REDUCTION, LEVEL_RESET_REDUCTION, COMMON_LAIR_TIME, LEVEL_LIMIT, \
    GHOST_REVERSAL, MAX_TIME, AWARD_LIFE_LEFT, EXTRA_LIFE_SCORE, EAT_DISTANCE, NUM_GHOSTS, NUM_MAZES, MAZE_NAMES, PATH_MAZES, PATH_DISTANCES, NUM_LIVES, GHOST_SPEED_REDUCTION
import math
from random import Random
from typing import Dict, List, Optional
from enum import Enum


class Game:
    # Static mazes and caches, initialized once as they are immutable
    # mazes = [Maze(i) for i in range(NUM_MAZES)]
    # from game.internal.paths_cache import PathsCache

    # caches = [PathsCache(i) for i in range(NUM_MAZES)]
    # mazes = []
    # caches = []
    # @classmethod
    # def delayed_init(cls):
    #         from pacman.game.internal.paths_cache import PathsCache
    #         from pacman.game.internal.maze import Maze
    #         cls.mazes = [Maze(i) for i in range(NUM_MAZES)]
    #         cls.caches = [PathsCache(i) for i in range(NUM_MAZES)]

    # def __init__(self, seed: int, initial_maze: int = 0):
    #     """
    #     Initializes a new game with the given seed and optional initial maze.

    #     :param seed: The seed for the pseudo-random number generator.
    #     :param initial_maze: The maze to start the game with (default is 0).
    #     """
    #     self.delayed_init()
    #     self.seed = seed
    #     self.rnd = Random(seed)
    #     self._init(initial_maze)

    # def __init__(self, seed: int):
    #     print("  [DEBUG] --- Initializing Game() object ---")

    #     self.mazes: List[Maze] = []
    #     self.current_maze_index: int = 0
    #     self.level_time: int = 0
    #     self.total_time: int = 0
    #     self.score: int = 0
    #     self.game_over_flag: bool = False
    #     self.pacman: PacMan = PacMan(
    #         self.get_current_maze().initial_pacman_node_index, MOVE.LEFT, NUM_LIVES, False)
    #     self.ghosts: Dict[GHOST, Ghost] = {
    #         GHOST.BLINKY: Ghost(GHOST.BLINKY),
    #         GHOST.PINKY: Ghost(GHOST.PINKY),
    #         GHOST.INKY: Ghost(GHOST.INKY),
    #         GHOST.SUE: Ghost(GHOST.SUE)
    #     }
    #     self.rnd = random.Random(seed)
    #     self.path_cache = PathsCache(self)

    #     print("  [DEBUG] Basic game attributes initialized.")

    #     # Load mazes
    #     for i, maze_name in enumerate(MAZE_NAMES):
    #         print(f"  [DEBUG] Loading maze {i}: {maze_name}...")
    #         maze_file = f"{PATH_MAZES}/{maze_name}.txt"
    #         distance_file = f"{PATH_DISTANCES}/d{maze_name}"

    #         print(f"  [DEBUG]   - Maze file: {maze_file}")
    #         print(f"  [DEBUG]   - Distance file: {distance_file}")

    #         self.mazes.append(Maze(self, maze_file, distance_file))
    #         print(f"  [DEBUG] Maze {i} loaded successfully.")

    #     print("  [DEBUG] All mazes loaded.")
    #     print("  [DEBUG] --- Game() object initialization complete. ---")

    def _init(self, initial_maze: int):
        """
        Initializes game variables and sets up the initial state.

        :param initial_maze: The initial maze index.
        """
        self.maze_index = initial_maze
        self.score = 0
        self.current_level_time = 0
        self.level_count = 0
        self.total_time = 0
        self.ghost_eat_multiplier = 1
        self.game_over_flag = False
        self.time_of_last_global_reversal = -1
        self.pacman_was_eaten = False
        self.pill_was_eaten = False
        self.power_pill_was_eaten = False

        self.ghosts_eaten = {ghost: False for ghost in GHOST}
        self.current_maze = self.mazes[self.maze_index]
        self._set_pills(self.current_maze)
        self._init_ghosts()
        # self.pacman = PacMan(
            # self.current_maze.initial_pacman_node_index, MOVE.RIGHT, NUM_LIVES, False)

    # class Game:
    """
    The main game logic class, containing all game-related information.
    """

    def __init__(self, seed: int):
        print("  [DEBUG] --- Initializing Game() object ---")

        # --- 1. Load Maze Data First ---
        # The game objects depend on this data, so it must come first.
        self.mazes: List[Maze] = []
        print("  [DEBUG] Loading maze data...")
        for i in range(len(MAZE_NAMES)):
            self.mazes.append(Maze(i))

        print("  [DEBUG] All mazes loaded successfully.")

        # --- 2. Initialize Game State ---
        self.seed = seed
        self.rnd = Random(seed)
        # Path cache needs access to game mazes
        self.current_maze_index: int = 0
        print("  [DEBUG] Init current maze.")
        self.current_maze = self.mazes[self.current_maze_index]
        print("  [DEBUG] Init path finder.")
        self.path_finder = AStar()
        print("  [DEBUG] Init path cache.")
        self.path_cache = PathsCache.load_or_build(
            self, cache_dir=".cache/paths")
        # print("  [DEBUG] Init path cache.")
        self.score: int = 0
        self.level_time: int = 0
        self.total_time: int = 0
        self.game_over_flag: bool = False
        print("  [DEBUG] Game states initialized.")
        # self.game_over = False

        # --- 3. Initialize Pac-Man and Ghosts ---
        # Now that mazes are loaded, we can safely create them.
        print("  [DEBUG] Init pacMans.")
        self.pacman: PacMan = PacMan(
            current_node_index=self.get_current_maze().initial_pacman_node_index,
            last_move_made=MOVE.LEFT,
            number_of_lives_remaining=NUM_LIVES,
            has_received_extra_life=False
        )
        print("  [DEBUG] All PacMan objects initialized.")

        self.ghosts: Dict[GHOST, Ghost] = {
            ghost_type: Ghost(
                type=ghost_type,
                current_node_index=self.current_maze.lair_node_index,
                edible_time=0,
                lair_time=int(ghost_type.initial_lair_time),
                last_move_made=MOVE.NEUTRAL
            )
            for ghost_type in GHOST
        }

        print("  [DEBUG] initing game states.")
        self._init(0)
        print("  [DEBUG] All game objects initialized.")
        print("  [DEBUG] --- Game() object initialization complete. ---")

    def _new_level_reset(self):
        """
        Resets the game state for a new level, advancing to the next maze.
        """
        self.maze_index = (self.maze_index + 1) % NUM_MAZES
        self.level_count += 1
        self.current_maze = self.mazes[self.maze_index]
        self.current_level_time = 0
        self.ghost_eat_multiplier = 1
        self._set_pills(self.current_maze)
        self._level_reset()

    def _level_reset(self):
        """
        Resets the level-specific state, including ghost and Pac-Man positions.
        """
        print('level reset')
        self.ghost_eat_multiplier = 1
        self._init_ghosts()
        self.pacman.current_node_index = self.current_maze.initial_pacman_node_index
        self.pacman.last_move_made = MOVE.LEFT

    def _set_pills(self, maze: Maze):
        """
        Initializes the pill and power pill sets for the given maze.

        :param maze: The maze to initialize pills for.
        """
        self.pills = set(range(len(maze.pill_indices)))
        self.power_pills = set(range(len(maze.power_pill_indices)))

    def _init_ghosts(self):
        """
        Initializes the ghosts with their respective lair times and positions.
        """
        self.ghosts = {
            ghost_type: Ghost(
                ghost_type,
                self.current_maze.lair_node_index,
                0,
                int(ghost_type.initial_lair_time * (LAIR_REDUCTION **
                    (self.level_count % LEVEL_RESET_REDUCTION))),
                MOVE.NEUTRAL
            ) for ghost_type in GHOST
        }

    def get_game_state(self) -> str:
        """
        Returns the game state as a string for replay or communication.

        :return: A string representing the game state.
        """
        sb = []
        sb.append(f"{self.maze_index},{self.total_time},{self.score},{self.current_level_time},{self.level_count},"
                  f"{self.pacman.current_node_index},{self.pacman.last_move_made.value},"
                  f"{self.pacman.number_of_lives_remaining},{self.pacman.has_received_extra_life},")

        for ghost in self.ghosts.values():
            sb.append(
                f"{ghost.current_node_index},{ghost.edible_time},{ghost.lair_time},{ghost.last_move_made.value},")

        pill_str = "".join("1" if i in self.pills else "0" for i in range(
            len(self.current_maze.pill_indices)))
        sb.append(pill_str + ",")

        power_pill_str = "".join("1" if i in self.power_pills else "0" for i in range(
            len(self.current_maze.power_pill_indices)))
        sb.append(power_pill_str + ",")

        sb.append(f"{self.time_of_last_global_reversal},")
        sb.append(f"{self.pacman_was_eaten},")

        for ghost in GHOST:
            sb.append(f"{self.ghosts_eaten[ghost]},")

        sb.append(f"{self.pill_was_eaten},")
        sb.append(f"{self.power_pill_was_eaten}")

        return "".join(sb)

    def set_game_state(self, game_state: str):
        """
        Sets the game state from a string representation.

        :param game_state: The game state string.
        """
        values = game_state.split(",")
        index = 0

        self.maze_index = int(values[index])
        index += 1
        self.total_time = int(values[index])
        index += 1
        self.score = int(values[index])
        index += 1
        self.current_level_time = int(values[index])
        index += 1
        self.level_count = int(values[index])
        index += 1

        self.pacman = PacMan(
            int(values[index]),
            MOVE(values[index + 1]),
            int(values[index + 2]),
            values[index + 3].lower() == "true"
        )
        index += 4

        self.ghosts = {}
        for ghost_type in GHOST:
            self.ghosts[ghost_type] = Ghost(
                ghost_type,
                int(values[index]),
                int(values[index + 1]),
                int(values[index + 2]),
                MOVE(values[index + 3])
            )
            index += 4

        self.current_maze = self.mazes[self.maze_index]
        self._set_pills(self.current_maze)

        for i, char in enumerate(values[index]):
            if char == "1":
                self.pills.add(i)
            else:
                self.pills.discard(i)
        index += 1

        for i, char in enumerate(values[index]):
            if char == "1":
                self.power_pills.add(i)
            else:
                self.power_pills.discard(i)
        index += 1

        self.time_of_last_global_reversal = int(values[index])
        index += 1
        self.pacman_was_eaten = values[index].lower() == "true"
        index += 1

        self.ghosts_eaten = {}
        for ghost in GHOST:
            self.ghosts_eaten[ghost] = values[index].lower() == "true"
            index += 1

        self.pill_was_eaten = values[index].lower() == "true"
        index += 1
        self.power_pill_was_eaten = values[index].lower() == "true"

    # def copy(self) -> 'Game':
    #     """
    #     Creates a deep copy of the game state.

    #     :return: A new Game instance with copied state.
    #     """
    #     copy = Game.__new__(Game)
    #     copy.seed = self.seed
    #     copy.rnd = Random(self.seed)
    #     copy.current_maze = self.current_maze
    #     copy.pills = self.pills.copy()
    #     copy.power_pills = self.power_pills.copy()
    #     copy.maze_index = self.maze_index
    #     copy.level_count = self.level_count
    #     copy.current_level_time = self.current_level_time
    #     copy.total_time = self.total_time
    #     copy.score = self.score
    #     copy.ghost_eat_multiplier = self.ghost_eat_multiplier
    #     copy.game_over = self.game_over
    #     copy.time_of_last_global_reversal = self.time_of_last_global_reversal
    #     copy.pacman_was_eaten = self.pacman_was_eaten
    #     copy.pill_was_eaten = self.pill_was_eaten
    #     copy.power_pill_was_eaten = self.power_pill_was_eaten
    #     copy.pacman = self.pacman.copy()
    #     copy.ghosts_eaten = self.ghosts_eaten.copy()
    #     copy.ghosts = {ghost_type: ghost.copy()
    #                    for ghost_type, ghost in self.ghosts.items()}
    #     return copy


    def copy(self) -> 'Game':
        """
        Creates a deep copy of the game state.

        :return: A new Game instance with copied state.
        """
        copy = Game.__new__(Game)
        copy.seed = self.seed
        copy.rnd = Random(self.seed)

        # --- Maze state ---
        # reference to static mazes (safe, since mazes are immutable)
        copy.mazes = self.mazes
        copy.current_maze_index = self.current_maze_index
        copy.current_maze = self.current_maze

        # --- Gameplay state ---
        copy.pills = self.pills.copy()
        copy.power_pills = self.power_pills.copy()
        copy.level_count = self.level_count
        copy.current_level_time = self.current_level_time
        copy.total_time = self.total_time
        copy.score = self.score
        copy.ghost_eat_multiplier = self.ghost_eat_multiplier
        copy.game_over_flag = self.game_over_flag
        copy.time_of_last_global_reversal = self.time_of_last_global_reversal
        copy.pacman_was_eaten = self.pacman_was_eaten
        copy.pill_was_eaten = self.pill_was_eaten
        copy.power_pill_was_eaten = self.power_pill_was_eaten

        # --- Characters ---
        copy.pacman = self.pacman.copy()
        copy.ghosts_eaten = self.ghosts_eaten.copy()
        copy.ghosts = {ghost_type: ghost.copy()
                    for ghost_type, ghost in self.ghosts.items()}

        # --- Pathfinding (re-use, not deepcopy for performance) ---
        copy.path_finder = self.path_finder
        copy.path_cache = self.path_cache

        return copy

    # Game-engine methods

    def advance_game(self, pacman_move: MOVE, ghost_moves: Dict[GHOST, MOVE]):
        """
        Advances the game state using the provided moves for Pac-Man and ghosts.

        :param pacman_move: The move for Pac-Man.
        :param ghost_moves: The moves for each ghost.
        """
        self.update_pacman(pacman_move)
        self.update_ghosts(ghost_moves)
        self.update_game()

    def advance_game_without_reverse(self, pacman_move: MOVE, ghost_moves: Dict[GHOST, MOVE]):
        """
        Advances the game without allowing ghost reversals.

        :param pacman_move: The move for Pac-Man.
        :param ghost_moves: The moves for each ghost.
        """
        self.update_pacman(pacman_move)
        self.update_ghosts_without_reverse(ghost_moves)
        self.update_game()

    def advance_game_with_forced_reverse(self, pacman_move: MOVE, ghost_moves: Dict[GHOST, MOVE]):
        """
        Advances the game with forced ghost reversals.

        :param pacman_move: The move for Pac-Man.
        :param ghost_moves: The moves for each ghost.
        """
        self.update_pacman(pacman_move)
        self.update_ghosts_with_forced_reverse(ghost_moves)
        self.update_game()

    def advance_game_with_power_pill_reverse_only(self, pacman_move: MOVE, ghost_moves: Dict[GHOST, MOVE]):
        """
        Advances the game, forcing ghost reversals only if a power pill was eaten.

        :param pacman_move: The move for Pac-Man.
        :param ghost_moves: The moves for each ghost.
        """
        self.update_pacman(pacman_move)
        if self.power_pill_was_eaten:
            self.update_ghosts_with_forced_reverse(ghost_moves)
        else:
            self.update_ghosts_without_reverse(ghost_moves)
        self.update_game()

    def update_pacman(self, pacman_move: MOVE):
        """
        Updates Pac-Man's state based on the provided move.

        :param pacman_move: The move for Pac-Man.
        """
        self._update_pacman(pacman_move)
        self._eat_pill()
        self._eat_power_pill()

    def update_ghosts(self, ghost_moves: Dict[GHOST, MOVE]):
        """
        Updates ghost states with possible reversals.

        :param ghost_moves: The moves for each ghost.
        """
        ghost_moves = self._complete_ghost_moves(ghost_moves)
        if not self._reverse_ghosts(ghost_moves, False):
            self._update_ghosts(ghost_moves)

    def update_ghosts_without_reverse(self, ghost_moves: Dict[GHOST, MOVE]):
        """
        Updates ghost states without allowing reversals.

        :param ghost_moves: The moves for each ghost.
        """
        ghost_moves = self._complete_ghost_moves(ghost_moves)
        self._update_ghosts(ghost_moves)

    def update_ghosts_with_forced_reverse(self, ghost_moves: Dict[GHOST, MOVE]):
        """
        Updates ghost states with forced reversals.

        :param ghost_moves: The moves for each ghost.
        """
        ghost_moves = self._complete_ghost_moves(ghost_moves)
        self._reverse_ghosts(ghost_moves, True)

    def update_game(self, feast: bool = True, update_lair_times: bool = True, update_extra_life: bool = True,
                    update_total_time: bool = True, update_level_time: bool = True):
        """
        Updates the game state after character updates.

        :param feast: Whether to enable feasting (eating events).
        :param update_lair_times: Whether to update ghost lair times.
        :param update_extra_life: Whether to check for extra life awards.
        :param update_total_time: Whether to increment total time.
        :param update_level_time: Whether to increment level time.
        """
        if feast:
            self._feast()
        if update_lair_times:
            self._update_lair_times()
        if update_extra_life:
            self._update_pacman_extra_life()
        if update_total_time:
            self.total_time += 1
        if update_level_time:
            self.current_level_time += 1
        self._check_level_state()

    def _update_lair_times(self):
        """
        Updates the lair times for ghosts, moving them out of the lair when time reaches zero.
        """
        for ghost in self.ghosts.values():
            if ghost.lair_time > 0:
                ghost.lair_time -= 1
                if ghost.lair_time == 0:
                    ghost.current_node_index = self.current_maze.initial_ghost_node_index

    def _update_pacman_extra_life(self):
        """
        Awards an extra life to Pac-Man if the score reaches EXTRA_LIFE_SCORE.
        """
        if not self.pacman.has_received_extra_life and self.score >= EXTRA_LIFE_SCORE:
            self.pacman.has_received_extra_life = True
            self.pacman.number_of_lives_remaining += 1

    def _update_pacman(self, move: MOVE = MOVE.DOWN):
        """
        Updates Pac-Man's position based on the provided move.

        :param move: The move to apply.
        """
        self.pacman.last_move_made = self._correct_pacman_dir(move)
        if self.pacman.last_move_made != MOVE.NEUTRAL:
            # print('inside the if')
            self.pacman.current_node_index = self.current_maze.graph[
                self.pacman.current_node_index].neighbourhood[self.pacman.last_move_made]

    def _correct_pacman_dir(self, direction: MOVE) -> MOVE:
        """
        Corrects Pac-Man's move to ensure it's valid.

        :param direction: The intended move.
        :return: The corrected move.
        """
        node = self.current_maze.graph[self.pacman.current_node_index]
        if direction in node.neighbourhood:
            # print('return direction', direction)
            return direction
        if self.pacman.last_move_made in node.neighbourhood:
            # print('return last move', self.pacman.last_move_made)
            return self.pacman.last_move_made
        # print('return neutral')
        return MOVE.NEUTRAL

    def _update_ghosts(self, moves: Dict[GHOST, MOVE]):
        """
        Updates ghost positions based on provided moves.

        :param moves: The moves for each ghost.
        """
        for ghost_type, move in moves.items():
            ghost = self.ghosts[ghost_type]
            if ghost.lair_time == 0:
                if ghost.edible_time == 0 or ghost.edible_time % GHOST_SPEED_REDUCTION != 0:
                    ghost.last_move_made = self._check_ghost_dir(ghost, move)
                    moves[ghost_type] = ghost.last_move_made
                    ghost.current_node_index = self.current_maze.graph[
                        ghost.current_node_index].neighbourhood[ghost.last_move_made]

    def _complete_ghost_moves(self, moves: Optional[Dict[GHOST, MOVE]]) -> Dict[GHOST, MOVE]:
        """
        Ensures all ghosts have a move, defaulting to their last move or NEUTRAL if not provided.

        :param moves: The provided ghost moves.
        :return: A complete dictionary of ghost moves.
        """
        if moves is None:
            moves = {
                ghost_type: self.ghosts[ghost_type].last_move_made for ghost_type in GHOST}
        for ghost_type in GHOST:
            if ghost_type not in moves:
                moves[ghost_type] = MOVE.NEUTRAL
        return moves

    def _check_ghost_dir(self, ghost: Ghost, direction: MOVE) -> MOVE:
        """
        Validates a ghost's move, preventing reversals unless valid.

        :param ghost: The ghost to move.
        :param direction: The intended move.
        :return: The validated move.
        """
        node = self.current_maze.graph[ghost.current_node_index]
        if direction in node.neighbourhood and direction != ghost.last_move_made.opposite():
            return direction
        if ghost.last_move_made in node.neighbourhood:
            return ghost.last_move_made
        moves = node.all_possible_moves[ghost.last_move_made]
        return moves[self.rnd.randint(0, len(moves) - 1)]

    def _eat_pill(self):
        """
        Handles Pac-Man eating a regular pill if present at the current node.
        """
        self.pill_was_eaten = False
        pill_index = self.current_maze.graph[self.pacman.current_node_index].pill_index
        if pill_index >= 0 and pill_index in self.pills:
            self.score += PILL
            self.pills.discard(pill_index)
            self.pill_was_eaten = True

    def _eat_power_pill(self):
        """
        Handles Pac-Man eating a power pill, making ghosts edible.
        """
        self.power_pill_was_eaten = False
        power_pill_index = self.current_maze.graph[self.pacman.current_node_index].power_pill_index
        if power_pill_index >= 0 and power_pill_index in self.power_pills:
            self.score += POWER_PILL
            self.ghost_eat_multiplier = 1
            self.power_pills.discard(power_pill_index)
            new_edible_time = int(
                EDIBLE_TIME * (EDIBLE_TIME_REDUCTION ** (self.level_count % LEVEL_RESET_REDUCTION)))
            for ghost in self.ghosts.values():
                ghost.edible_time = new_edible_time if ghost.lair_time == 0 else 0
            self.power_pill_was_eaten = True

    def _reverse_ghosts(self, moves: Dict[GHOST, MOVE], force: bool) -> bool:
        """
        Reverses ghost directions if conditions are met.

        :param moves: The ghost moves.
        :param force: Whether to force reversal.
        :return: Whether any ghosts were reversed.
        """
        reversed = False
        global_reverse = self.rnd.random() < GHOST_REVERSAL
        for ghost_type, move in moves.items():
            ghost = self.ghosts[ghost_type]
            if self.current_level_time > 1 and ghost.lair_time == 0 and ghost.last_move_made != MOVE.NEUTRAL:
                if force or self.power_pill_was_eaten or global_reverse:
                    ghost.last_move_made = ghost.last_move_made.opposite()
                    ghost.current_node_index = self.current_maze.graph[
                        ghost.current_node_index].neighbourhood[ghost.last_move_made]
                    reversed = True
                    self.time_of_last_global_reversal = self.total_time
        return reversed

    def _feast(self):
        """
        Handles eating events (Pac-Man eating ghosts or ghosts eating Pac-Man).
        """
        self.pacman_was_eaten = False
        for ghost in GHOST:
            self.ghosts_eaten[ghost] = False

        for ghost in self.ghosts.values():
            distance = self.get_shortest_path_distance(
                self.pacman.current_node_index, ghost.current_node_index)
            if distance != -1 and distance <= EAT_DISTANCE:
                if ghost.edible_time > 0:  # Pac-Man eats ghost
                    self.score += GHOST_EAT_SCORE * self.ghost_eat_multiplier
                    self.ghost_eat_multiplier *= 2
                    ghost.edible_time = 0
                    ghost.lair_time = int(
                        COMMON_LAIR_TIME * (LAIR_REDUCTION ** (self.level_count % LEVEL_RESET_REDUCTION)))
                    ghost.current_node_index = self.current_maze.lair_node_index
                    ghost.last_move_made = MOVE.NEUTRAL
                    self.ghosts_eaten[ghost.type] = True
                else:  # Ghost eats Pac-Man
                    self.pacman.number_of_lives_remaining -= 1
                    self.pacman_was_eaten = True
                    if self.pacman.number_of_lives_remaining <= 0:
                        self.game_over_flag = True
                    else:
                        self._level_reset()
                    return
        for ghost in self.ghosts.values():
            if ghost.edible_time > 0:
                ghost.edible_time -= 1

    def _check_level_state(self):
        """
        Checks if the level or game is over based on time, pills, or lives.
        """
        if self.total_time + 1 > MAX_TIME:
            self.game_over_flag = True
            self.score += self.pacman.number_of_lives_remaining * AWARD_LIFE_LEFT
        elif not self.pills and not self.power_pills or self.current_level_time >= LEVEL_LIMIT:
            self._new_level_reset()

    # Query methods

    def was_pacman_eaten(self) -> bool:
        """
        :return: Whether Pac-Man was eaten in the last time step.
        """
        return self.pacman_was_eaten

    def was_ghost_eaten(self, ghost: GHOST) -> bool:
        """
        :param ghost: The ghost to check.
        :return: Whether the specified ghost was eaten.
        """
        return self.ghosts_eaten[ghost]

    def get_num_ghosts_eaten(self) -> int:
        """
        :return: The number of ghosts eaten in the last time step.
        """
        return sum(1 for ghost in GHOST if self.ghosts_eaten[ghost])

    def was_pill_eaten(self) -> bool:
        """
        :return: Whether a pill was eaten in the last time step.
        """
        return self.pill_was_eaten

    def was_power_pill_eaten(self) -> bool:
        """
        :return: Whether a power pill was eaten in the last time step.
        """
        return self.power_pill_was_eaten

    def get_time_of_last_global_reversal(self) -> int:
        """
        :return: The time of the last global reversal event.
        """
        return self.time_of_last_global_reversal

    def game_over(self) -> bool:
        """
        :return: Whether the game is over.
        """
        return self.game_over_flag

    def get_current_maze(self) -> Maze:
        """
        :return: The current maze.
        """
        # return self.current_maze
        return self.mazes[self.current_maze_index]

    def get_node_x_coord(self, node_index: int) -> int:
        """
        :param node_index: The node index.
        :return: The x-coordinate of the specified node.
        """
        return self.current_maze.graph[node_index].x

    def get_node_y_coord(self, node_index: int) -> int:
        """
        :param node_index: The node index.
        :return: The y-coordinate of the specified node.
        """
        return self.current_maze.graph[node_index].y

    def get_maze_index(self) -> int:
        """
        :return: The current maze index.
        """
        return self.maze_index

    def get_current_level(self) -> int:
        """
        :return: The current level number.
        """
        return self.level_count

    def get_number_of_nodes(self) -> int:
        """
        :return: The number of nodes in the current maze.
        """
        # return len(self.current_maze.graph)
        return len(self.get_current_maze().graph)

    def get_ghost_current_edible_score(self) -> int:
        """
        :return: The current score for eating a ghost.
        """
        return GHOST_EAT_SCORE * self.ghost_eat_multiplier

    def get_ghost_initial_node_index(self) -> int:
        """
        :return: The node index where ghosts start after leaving the lair.
        """
        return self.current_maze.initial_ghost_node_index

    def is_pill_still_available(self, pill_index: int) -> bool:
        """
        :param pill_index: The pill index.
        :return: Whether the specified pill is still available.
        """
        return pill_index in self.pills

    def is_power_pill_still_available(self, power_pill_index: int) -> bool:
        """
        :param power_pill_index: The power pill index.
        :return: Whether the specified power pill is still available.
        """
        return power_pill_index in self.power_pills

    def get_pill_index(self, node_index: int) -> int:
        """
        :param node_index: The node index.
        :return: The pill index at the specified node, or -1 if none.
        """
        return self.current_maze.graph[node_index].pill_index

    def get_power_pill_index(self, node_index: int) -> int:
        """
        :param node_index: The node index.
        :return: The power pill index at the specified node, or -1 if none.
        """
        return self.current_maze.graph[node_index].power_pill_index

    def get_junction_indices(self) -> List[int]:
        """
        :return: The indices of all junction nodes.
        """
        return self.current_maze.junction_indices

    def get_pill_indices(self) -> List[int]:
        """
        :return: The indices of all nodes with pills.
        """
        return self.current_maze.pill_indices

    def get_power_pill_indices(self) -> List[int]:
        """
        :return: The indices of all nodes with power pills.
        """
        return self.current_maze.power_pill_indices

    def get_pacman_current_node_index(self) -> int:
        """
        :return: The current node index of Pac-Man.
        """
        return self.pacman.current_node_index

    def get_pacman_last_move_made(self) -> MOVE:
        """
        :return: The last move made by Pac-Man.
        """
        return self.pacman.last_move_made

    def get_pacman_number_of_lives_remaining(self) -> int:
        """
        :return: The number of lives remaining for Pac-Man.
        """
        return self.pacman.number_of_lives_remaining

    def get_ghost_current_node_index(self, ghost_type: GHOST) -> int:
        """
        :param ghost_type: The ghost type.
        :return: The current node index of the specified ghost.
        """
        return self.ghosts[ghost_type].current_node_index

    def get_ghost_last_move_made(self, ghost_type: GHOST) -> MOVE:
        """
        :param ghost_type: The ghost type.
        :return: The last move made by the specified ghost.
        """
        return self.ghosts[ghost_type].last_move_made

    def get_ghost_edible_time(self, ghost_type: GHOST) -> int:
        """
        :param ghost_type: The ghost type.
        :return: The edible time remaining for the specified ghost.
        """
        return self.ghosts[ghost_type].edible_time

    def is_ghost_edible(self, ghost_type: GHOST) -> bool:
        """
        :param ghost_type: The ghost type.
        :return: Whether the specified ghost is edible.
        """
        return self.ghosts[ghost_type].edible_time > 0

    def get_score(self) -> int:
        """
        :return: The current score of the game.
        """
        return self.score

    def get_current_level_time(self) -> int:
        """
        :return: The time spent on the current level.
        """
        return self.current_level_time

    def get_total_time(self) -> int:
        """
        :return: The total time the game has been played.
        """
        return self.total_time

    def get_number_of_pills(self) -> int:
        """
        :return: The total number of pills in the current maze.
        """
        return len(self.current_maze.pill_indices)

    def get_number_of_power_pills(self) -> int:
        """
        :return: The total number of power pills in the current maze.
        """
        return len(self.current_maze.power_pill_indices)

    def get_number_of_active_pills(self) -> int:
        """
        :return: The number of active (uneaten) pills in the current maze.
        """
        return len(self.pills)

    def get_number_of_active_power_pills(self) -> int:
        """
        :return: The number of active (uneaten) power pills in the current maze.
        """
        return len(self.power_pills)

    def get_ghost_lair_time(self, ghost_type: GHOST) -> int:
        """
        :param ghost_type: The ghost type.
        :return: The time the specified ghost will spend in the lair.
        """
        return self.ghosts[ghost_type].lair_time

    def get_active_pills_indices(self) -> List[int]:
        """
        :return: The indices of all active pills.
        """
        return [self.current_maze.pill_indices[i] for i in self.pills]

    def get_active_power_pills_indices(self) -> List[int]:
        """
        :return: The indices of all active power pills.
        """
        return [self.current_maze.power_pill_indices[i] for i in self.power_pills]

    def does_ghost_require_action(self, ghost_type: GHOST) -> bool:
        """
        :param ghost_type: The ghost type.
        :return: Whether the ghost requires an action (at junction or just left lair).
        """
        ghost = self.ghosts[ghost_type]
        return ((self.is_junction(ghost.current_node_index) or
                 (ghost.last_move_made == MOVE.NEUTRAL and ghost.current_node_index == self.current_maze.initial_ghost_node_index)) and
                (ghost.edible_time == 0 or ghost.edible_time % GHOST_SPEED_REDUCTION != 0))

    def is_junction(self, node_index: int) -> bool:
        """
        :param node_index: The node index.
        :return: Whether the specified node is a junction.
        """
        return self.get_current_maze().graph[node_index].num_neighbouring_nodes > 2
    # return len(self.get_current_maze().graph)

    def get_possible_moves(self, node_index: int) -> List[MOVE]:
        """
        :param node_index: The node index.
        :return: The possible moves from the specified node.
        """
        return self.get_current_maze().graph[node_index].all_possible_moves[MOVE.NEUTRAL]

    def get_possible_moves_with_last_move(self, node_index: int, last_move_made: MOVE) -> List[MOVE]:
        """
        :param node_index: The node index.
        :param last_move_made: The last move made.
        :return: The possible moves excluding the reverse of the last move.
        """
        return self.current_maze.graph[node_index].all_possible_moves[last_move_made]

    def get_neighbouring_nodes(self, node_index: int) -> List[int]:
        """
        :param node_index: The node index.
        :return: The neighbouring node indices.
        """
        return self.current_maze.graph[node_index].all_neighbouring_nodes[MOVE.NEUTRAL]

    def get_neighbouring_nodes_with_last_move(self, node_index: int, last_move_made: MOVE) -> List[int]:
        """
        :param node_index: The node index.
        :param last_move_made: The last move made.
        :return: The neighbouring node indices excluding the reverse of the last move.
        """
        return self.current_maze.graph[node_index].all_neighbouring_nodes[last_move_made]

    def get_neighbour(self, node_index: int, move_to_be_made: MOVE) -> int:
        """
        :param node_index: The current node index.
        :param move_to_be_made: The move to make.
        :return: The node index reached by the move, or -1 if invalid.
        """
        neighbour = self.get_current_maze().graph[node_index].neighbourhood.get(
            move_to_be_made)
        return neighbour if neighbour is not None else -1

    def get_move_to_make_to_reach_direct_neighbour(self, current_node_index: int, neighbour_node_index: int) -> Optional[MOVE]:
        """
        :param current_node_index: The current node index.
        :param neighbour_node_index: The neighbouring node index.
        :return: The move to reach the neighbour, or None if invalid.
        """
        for move in MOVE:
            if move in self.current_maze.graph[current_node_index].neighbourhood and \
                    self.current_maze.graph[current_node_index].neighbourhood[move] == neighbour_node_index:
                return move
        return None

    # Helper methods (computational)

    def get_shortest_path_distance(self, from_node_index: int, to_node_index: int) -> int:
        """
        :param from_node_index: The starting node index.
        :param to_node_index: The target node index.
        :return: The shortest path distance between the nodes.
        """
        if from_node_index == to_node_index:
            return 0
        if from_node_index < to_node_index:
            return self.current_maze.shortest_path_distances[((to_node_index * (to_node_index + 1)) // 2) + from_node_index]
        return self.current_maze.shortest_path_distances[((from_node_index * (from_node_index + 1)) // 2) + to_node_index]

    def get_euclidean_distance(self, from_node_index: int, to_node_index: int) -> float:
        """
        :param from_node_index: The starting node index.
        :param to_node_index: The target node index.
        :return: The Euclidean distance between the nodes.
        """
        return math.sqrt((self.current_maze.graph[from_node_index].x - self.current_maze.graph[to_node_index].x) ** 2 +
                         (self.current_maze.graph[from_node_index].y - self.current_maze.graph[to_node_index].y) ** 2)

    def get_manhattan_distance(self, from_node_index: int, to_node_index: int) -> int:
        """
        :param from_node_index: The starting node index.
        :param to_node_index: The target node index.
        :return: The Manhattan distance between the nodes.
        """
        return abs(self.current_maze.graph[from_node_index].x - self.current_maze.graph[to_node_index].x) + \
            abs(self.current_maze.graph[from_node_index].y -
                self.current_maze.graph[to_node_index].y)

    def get_distance(self, from_node_index: int, to_node_index: int, distance_measure: DM) -> float:
        """
        :param from_node_index: The starting node index.
        :param to_node_index: The target node index.
        :param distance_measure: The distance measure to use.
        :return: The distance between the nodes using the specified measure.
        """
        if distance_measure == DM.PATH:
            return self.get_shortest_path_distance(from_node_index, to_node_index)
        elif distance_measure == DM.EUCLID:
            return self.get_euclidean_distance(from_node_index, to_node_index)
        elif distance_measure == DM.MANHATTAN:
            return self.get_manhattan_distance(from_node_index, to_node_index)
        return -1

    def get_distance_with_last_move(self, from_node_index: int, to_node_index: int, last_move_made: MOVE, distance_measure: DM) -> float:
        """
        :param from_node_index: The starting node index.
        :param to_node_index: The target node index.
        :param last_move_made: The last move made.
        :param distance_measure: The distance measure to use.
        :return: The distance considering the last move made.
        """
        if distance_measure == DM.PATH:
            return self.get_approximate_shortest_path_distance(from_node_index, to_node_index, last_move_made)
        elif distance_measure == DM.EUCLID:
            return self.get_euclidean_distance(from_node_index, to_node_index)
        elif distance_measure == DM.MANHATTAN:
            return self.get_manhattan_distance(from_node_index, to_node_index)
        return -1

    def get_closest_node_index_from_node_index(self, from_node_index: int, target_node_indices: List[int], distance_measure: DM) -> int:
        """
        :param from_node_index: The starting node index.
        :param target_node_indices: The list of target node indices.
        :param distance_measure: The distance measure to use.
        :return: The index of the closest target node.
        """
        min_distance = float('inf')
        target = -1
        for node_index in target_node_indices:
            distance = self.get_distance(
                node_index, from_node_index, distance_measure)
            if distance < min_distance:
                min_distance = distance
                target = node_index
        return target

    def get_farthest_node_index_from_node_index(self, from_node_index: int, target_node_indices: List[int], distance_measure: DM) -> int:
        """
        :param from_node_index: The starting node index.
        :param target_node_indices: The list of target node indices.
        :param distance_measure: The distance measure to use.
        :return: The index of the farthest target node.
        """
        max_distance = float('-inf')
        target = -1
        for node_index in target_node_indices:
            distance = self.get_distance(
                node_index, from_node_index, distance_measure)
            if distance > max_distance:
                max_distance = distance
                target = node_index
        return target

    def get_next_move_towards_target(self, from_node_index: int, to_node_index: int, distance_measure: DM) -> MOVE:
        """
        :param from_node_index: The starting node index.
        :param to_node_index: The target node index.
        :param distance_measure: The distance measure to use.
        :return: The next move to get closer to the target.
        """
        min_distance = float('inf')
        move: MOVE = MOVE.NEUTRAL
        for move_key, node in self.current_maze.graph[from_node_index].neighbourhood.items():
            distance = self.get_distance(node, to_node_index, distance_measure)
            if distance < min_distance:
                min_distance = distance
                move = move_key
        return move

    def get_next_move_away_from_target(self, from_node_index: int, to_node_index: int, distance_measure: DM) -> MOVE:
        """
        :param from_node_index: The starting node index.
        :param to_node_index: The target node index.
        :param distance_measure: The distance measure to use.
        :return: The next move to get farther from the target.
        """
        max_distance = float('-inf')
        move: MOVE = MOVE.NEUTRAL
        for move_key, node in self.current_maze.graph[from_node_index].neighbourhood.items():
            distance = self.get_distance(node, to_node_index, distance_measure)
            if distance > max_distance:
                max_distance = distance
                move = move_key
        return move

    def get_approximate_next_move_towards_target(self, from_node_index: int, to_node_index: int, last_move_made: MOVE, distance_measure: DM) -> MOVE:
        """
        :param from_node_index: The starting node index.
        :param to_node_index: The target node index.
        :param last_move_made: The last move made.
        :param distance_measure: The distance measure to use.
        :return: The approximate next move towards the target, excluding reversals.
        """
        min_distance = float('inf')
        move: MOVE = MOVE.NEUTRAL
        for move_key, node in self.current_maze.graph[from_node_index].all_neighbourhoods[last_move_made].items():
            distance = self.get_distance(node, to_node_index, distance_measure)
            if distance < min_distance:
                min_distance = distance
                move = move_key
        return move

    def get_approximate_next_move_away_from_target(self, from_node_index: int, to_node_index: int, last_move_made: MOVE, distance_measure: DM) -> MOVE:
        """
        :param from_node_index: The starting node index.
        :param to_node_index: The target node index.
        :param last_move_made: The last move made.
        :param distance_measure: The distance measure to use.
        :return: The approximate next move away from the target, excluding reversals.
        """
        max_distance = float('-inf')
        move: MOVE = MOVE.NEUTRAL
        for move_key, node in self.current_maze.graph[from_node_index].all_neighbourhoods[last_move_made].items():
            distance = self.get_distance(node, to_node_index, distance_measure)
            if distance > max_distance:
                max_distance = distance
                move = move_key
        return move

    def get_next_move_towards_target_with_reversals(self, from_node_index: int, to_node_index: int, last_move_made: MOVE, distance_measure: DM) -> MOVE:
        """
        :param from_node_index: The starting node index.
        :param to_node_index: The target node index.
        :param last_move_made: The last move made.
        :param distance_measure: The distance measure to use.
        :return: The exact next move towards the target, considering reversals.
        """
        min_distance = float('inf')
        move: MOVE = MOVE.NEUTRAL
        for move_key, node in self.current_maze.graph[from_node_index].all_neighbourhoods[last_move_made].items():
            distance = self.get_distance_with_last_move(
                node, to_node_index, last_move_made, distance_measure)
            if distance < min_distance:
                min_distance = distance
                move = move_key
        return move

    def get_next_move_away_from_target_with_reversals(self, from_node_index: int, to_node_index: int, last_move_made: MOVE, distance_measure: DM) -> MOVE:
        """
        :param from_node_index: The starting node index.
        :param to_node_index: The target node index.
        :param last_move_made: The last move made.
        :param distance_measure: The distance measure to use.
        :return: The exact next move away from the target, considering reversals.
        """
        max_distance = float('-inf')
        move: MOVE = MOVE.NEUTRAL
        for move_key, node in self.current_maze.graph[from_node_index].all_neighbourhoods[last_move_made].items():
            distance = self.get_distance_with_last_move(
                node, to_node_index, last_move_made, distance_measure)
            if distance > max_distance:
                max_distance = distance
                move = move_key
        return move

    # def get_shortest_path(self, from_node_index: int, to_node_index: int, last_move_made: Optional[MOVE] = None) -> List[int]:
    #     """
    #     :param from_node_index: The starting node index.
    #     :param to_node_index: The target node index.
    #     :param last_move_made: The last move made (optional).
    #     :return: The shortest path from start to target.
    #     """
    #     # if last_move_made is None:
    #     #     return self.caches[self.maze_index].get_path_from_a2b(from_node_index, to_node_index)
    #     # if not self.current_maze.graph[from_node_index].neighbourhood:
    #     #     return []
    #     # return self.caches[self.maze_index].get_path_from_a2b(from_node_index, to_node_index, last_move_made)
    #     if last_move_made is None:
    #         return self.path_cache.get_path_from_a2b(from_node_index, to_node_index)

    #     # If a move is specified, it's for a ghost, so use the ghost-specific pathfinder.
    #     else:
    #         return self.path_cache.get_path_from_a2b_ghost(from_node_index, to_node_index, last_move_made)

    def get_shortest_path(self, from_node_index: int, to_node_index: int, last_move_made: Optional[MOVE] = None) -> List[int]:
        # If cache isn't constructed yet (we're in __init__), use A* directly with no-heuristic
        cache_ready = hasattr(
            self, "path_cache") and self.path_cache is not None
        if not cache_ready:
            astar = AStar()
            # Adjust to your actual access to the node list:
            # e.g., self.current_maze.graph or self.graph, depending on your codebase
            astar.create_graph(self.current_maze.graph)
            move = last_move_made if last_move_made is not None else MOVE.NEUTRAL
            return astar.compute_paths_a_star(
                from_node_index, to_node_index, move, game=None  # no heuristic; safe during init
            )

        # Normal fast path via cache (your existing code)
        if last_move_made is None:
            return self.path_cache.get_path_from_a2b(from_node_index, to_node_index)
        else:
            return self.path_cache.get_path_from_a2b_ghost(from_node_index, to_node_index, last_move_made)

    def get_approximate_shortest_path_distance(self, from_node_index: int, to_node_index: int, last_move_made: MOVE) -> int:
        """
        :param from_node_index: The starting node index.
        :param to_node_index: The target node index.
        :param last_move_made: The last move made.
        :return: The approximate shortest path distance, considering the last move.
        """
        if not self.current_maze.graph[from_node_index].neighbourhood:
            return 0
        return self.caches[self.maze_index].get_path_distance_from_a2b(from_node_index, to_node_index, last_move_made)

    def get_number_of_junctions(self) -> int:
        """
        :return: The number of junctions in the current maze.
        """
        return len(self.get_junction_indices())
