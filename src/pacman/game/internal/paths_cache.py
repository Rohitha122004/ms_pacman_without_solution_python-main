# pacman/game/internal/paths_cache.py

import os
import pickle
import gzip
import hashlib
from typing import List, Dict, Optional
from collections import defaultdict
from pacman.game.constants import MOVE
from pacman.game.internal.node import Node


class JunctionData:
    def __init__(self, node_id: int, first_move: MOVE, node_started_from: int, path: List[int], last_move: MOVE):
        self.node_id = node_id
        self.node_started_from = node_started_from
        self.first_move = first_move
        self.last_move = last_move
        self.path = path
        self.reverse_path = self._get_reverse_path(path) if path else []

    def _get_reverse_path(self, path: List[int]) -> List[int]:
        reverse_path = [0] * len(path)
        for i in range(1, len(path)):
            reverse_path[i-1] = path[len(path) - 1 - i]
        reverse_path[-1] = self.node_started_from
        return reverse_path

    def __str__(self) -> str:
        return f"{self.node_id}, {self.first_move}, {self.path}"


class DNode:
    def __init__(self, node_id: int, is_junction: bool):
        self.node_id = node_id
        self.closest_junctions: List[JunctionData] = []
        self.is_junction = is_junction
        if is_junction:
            self.closest_junctions.append(JunctionData(
                node_id, MOVE.NEUTRAL, node_id, [], MOVE.NEUTRAL))

    def get_path_to_junction(self, last_move_made: MOVE) -> List[int]:
        if self.is_junction:
            return []
        for jd in self.closest_junctions:
            if jd.first_move != last_move_made.opposite():
                return jd.path
        return None

    def get_nearest_junction(self, last_move_made: MOVE) -> Optional[JunctionData]:
        if self.is_junction:
            return self.closest_junctions[0]
        min_dist = float('inf')
        best_jd = None
        for jd in self.closest_junctions:
            if jd.first_move != last_move_made.opposite():
                new_dist = len(jd.path)
                if new_dist < min_dist:
                    min_dist = new_dist
                    best_jd = jd
        return best_jd

    def add_path(self, junction_id: int, first_move: MOVE, node_started_from: int, path: List[int], last_move: MOVE):
        self.closest_junctions.append(JunctionData(
            junction_id, first_move, node_started_from, path, last_move))

    def __str__(self) -> str:
        return f"{self.node_id}, {self.is_junction}"


class Junction:
    def __init__(self, jct_id: int, node_id: int, num_jcts: int):
        self.jct_id = jct_id
        self.node_id = node_id
        self.paths: List[Dict[MOVE, List[int]]] = [
            defaultdict(list) for _ in range(num_jcts)]

    def compute_shortest_paths(self):
        moves = list(MOVE)
        for i in range(len(self.paths)):
            if i == self.jct_id:
                self.paths[i][MOVE.NEUTRAL] = []
            else:
                distance = float('inf')
                path = None
                for move in moves:
                    if move in self.paths[i]:
                        tmp = self.paths[i][move]
                        if len(tmp) < distance:
                            distance = len(tmp)
                            path = tmp
                self.paths[i][MOVE.NEUTRAL] = path

    def add_path(self, to_junction: int, first_move_made: MOVE, path: List[int]):
        self.paths[to_junction][first_move_made] = path

    def __str__(self) -> str:
        return f"{self.jct_id}, {self.node_id}"


class PathsCache:
    # def __init__(self, maze_index: int):
    #     from ..game import Game
            
    #     self.junction_index_converter: Dict[int, int] = {}
    #     self.nodes: List[DNode] = []
    #     self.junctions: List[Junction] = []
    #     self.game = Game(0, maze_index)
    #     m = self.game.get_current_maze()
    #     jct_indices = m.junction_indices
    #     for i, idx in enumerate(jct_indices):
    #         self.junction_index_converter[idx] = i
    #     self.nodes = self._assign_junctions_to_nodes(self.game)
    #     self.junctions = self._junction_distances(self.game)
    #     for junction in self.junctions:
    #         junction.compute_shortest_paths()

    def __init__(self, game: 'Game'):
        """
        Initializes the PathsCache with a reference to the main game object.

        :param game: The active game instance.
        """
        # It's better to import at the top, but we use a forward reference 'Game'
        # to avoid circular import errors at the module level.

        # Use the provided game instance, DON'T create a new one.
        self.game = game

        # --- End of Changes ---

        self.junction_index_converter: Dict[int, int] = {}
        self.nodes: List[DNode] = []
        self.junctions: List[Junction] = []

        m = self.game.get_current_maze()
        jct_indices = m.junction_indices
        for i, idx in enumerate(jct_indices):
            self.junction_index_converter[idx] = i

        self.nodes = self._assign_junctions_to_nodes(self.game)
        self.junctions = self._junction_distances(self.game)

        for junction in self.junctions:
            junction.compute_shortest_paths()

    @classmethod
    def load_or_build(cls, game: 'Game', cache_dir: str = ".cache/paths") -> 'PathsCache':
        """
        Loads a cached PathsCache from disk if available, otherwise builds and saves it.
        
        :param game: The active game instance.
        :param cache_dir: Directory to store cache files.
        :return: A PathsCache instance.
        """
        # Create cache directory if it doesn't exist
        os.makedirs(cache_dir, exist_ok=True)
        
        # Generate a unique cache key based on maze properties
        maze = game.get_current_maze()
        cache_key = cls._generate_cache_key(maze)
        cache_file = os.path.join(cache_dir, f"v1_{cache_key}.pkl.gz")
        
        # Try to load from cache
        if os.path.exists(cache_file):
            try:
                print(f"  [DEBUG] Loading PathsCache from {cache_file}...")
                with gzip.open(cache_file, 'rb') as f:
                    cached_data = pickle.load(f)
                
                # Reconstruct PathsCache from cached data
                instance = cls.__new__(cls)
                instance.game = game
                instance.junction_index_converter = cached_data['junction_index_converter']
                instance.nodes = cached_data['nodes']
                instance.junctions = cached_data['junctions']
                
                print(f"  [DEBUG] PathsCache loaded successfully from cache.")
                return instance
            except Exception as e:
                print(f"  [WARNING] Failed to load cache: {e}. Rebuilding...")
        
        # Build new cache
        print(f"  [DEBUG] Building new PathsCache...")
        instance = cls(game)
        
        # Save to cache
        try:
            cached_data = {
                'junction_index_converter': instance.junction_index_converter,
                'nodes': instance.nodes,
                'junctions': instance.junctions
            }
            with gzip.open(cache_file, 'wb') as f:
                pickle.dump(cached_data, f, protocol=pickle.HIGHEST_PROTOCOL)
            print(f"  [DEBUG] PathsCache saved to {cache_file}")
        except Exception as e:
            print(f"  [WARNING] Failed to save cache: {e}")
        
        return instance
    
    @staticmethod
    def _generate_cache_key(maze) -> str:
        """
        Generates a unique cache key based on maze properties.
        
        :param maze: The maze object.
        :return: A hash string representing the maze configuration.
        """
        # Create a unique identifier based on maze properties
        key_data = (
            maze.name,
            len(maze.graph),
            tuple(maze.junction_indices),
            maze.initial_pacman_node_index,
            maze.initial_ghost_node_index,
            maze.lair_node_index
        )
        key_string = str(key_data)
        return hashlib.md5(key_string.encode()).hexdigest()


    def get_path_from_a2b(self, a: int, b: int) -> List[int]:
        if a == b:
            return []
        closest_from_junctions = self.nodes[a].closest_junctions
        for jd in closest_from_junctions:
            if b in jd.path:
                idx = jd.path.index(b)
                return jd.path[:idx + 1]
        closest_to_junctions = self.nodes[b].closest_junctions
        min_from = -1
        min_to = -1
        min_distance = float('inf')
        shortest_path = None
        for i, from_jd in enumerate(closest_from_junctions):
            for j, to_jd in enumerate(closest_to_junctions):
                distance = len(from_jd.path)
                tmp_path = self.junctions[self.junction_index_converter[from_jd.node_id]
                                          ].paths[self.junction_index_converter[to_jd.node_id]][MOVE.NEUTRAL]
                distance += len(tmp_path)
                distance += len(to_jd.path)
                if distance < min_distance:
                    min_distance = distance
                    min_from = i
                    min_to = j
                    shortest_path = tmp_path
        return self._concat(closest_from_junctions[min_from].path, shortest_path, closest_to_junctions[min_to].reverse_path)

    def get_path_distance_from_a2b(self, a: int, b: int, last_move_made: MOVE) -> int:
        return len(self.get_path_from_a2b(a, b, last_move_made))

    def get_path_from_a2b_ghost(self, a: int, b: int, last_move_made: MOVE) -> List[int]:
        if a == b:
            return []
        from_junction = self.nodes[a].get_nearest_junction(last_move_made)
        for i in range(len(from_junction.path)):
            if from_junction.path[i] == b:
                return from_junction.path[:i + 1]
        junction_from = from_junction.node_id
        junction_from_id = self.junction_index_converter[junction_from]
        move_entered_junction = from_junction.last_move if from_junction.last_move != MOVE.NEUTRAL else last_move_made
        junctions_to = self.nodes[b].closest_junctions
        min_dist = float('inf')
        min_jct = -1
        shortest_path = None
        for i, to_jd in enumerate(junctions_to):
            tmp_path = self.junctions[junction_from_id].paths[self.junction_index_converter[to_jd.node_id]
                                                              ][move_entered_junction]
            distance = len(tmp_path) + len(to_jd.path)
            if distance < min_dist:
                min_dist = distance
                min_jct = i
                shortest_path = tmp_path
        return self._concat(from_junction.path, shortest_path, junctions_to[min_jct].reverse_path)

    def _assign_junctions_to_nodes(self, game: 'Game') -> List[DNode]:
        from pacman.game.game import Game

        all_nodes = [DNode(i, game.is_junction(i))
                     for i in range(game.get_number_of_nodes())]
        for i in range(len(all_nodes)):
            if not all_nodes[i].is_junction:
                possible_moves = game.get_possible_moves(i)
                for j, move in enumerate(possible_moves):
                    path = []
                    current_node = game.get_neighbour(i, move)
                    last_move = move
                    path.append(current_node)
                    while not game.is_junction(current_node):
                        new_possible_moves = game.get_possible_moves(
                            current_node)
                        for q in range(len(new_possible_moves)):
                            if new_possible_moves[q].opposite() != last_move:
                                last_move = new_possible_moves[q]
                                break
                        current_node = game.get_neighbour(
                            current_node, last_move)
                        path.append(current_node)
                    all_nodes[i].add_path(
                        path[-1], possible_moves[j], i, path, last_move)
        return all_nodes

    def _junction_distances(self, game: 'Game') -> List[Junction]:
        from pacman.game.game import Game

        junctions = [Junction(i, game.get_junction_indices()[
                              i], game.get_number_of_junctions()) for i in range(game.get_number_of_junctions())]
        for i in range(len(junctions)):
            for j in range(i + 1, len(junctions)):
                path = game.get_shortest_path(game.get_junction_indices()[
                                              i], game.get_junction_indices()[j])
                first_move = game.get_move_to_make_to_reach_direct_neighbour(
                    game.get_junction_indices()[i], path[0]) if len(path) > 0 else MOVE.NEUTRAL
                junctions[i].add_path(j, first_move, path)
                reverse_path = path[::-1]
                first_move_reverse = game.get_move_to_make_to_reach_direct_neighbour(
                    game.get_junction_indices()[j], reverse_path[0]) if len(reverse_path) > 0 else MOVE.NEUTRAL
                junctions[j].add_path(i, first_move_reverse, reverse_path)
        return junctions

    def _concat(self, *arrays: List[int]) -> List[int]:
        full_array = []
        for arr in arrays:
            full_array.extend(arr)
        return full_array
