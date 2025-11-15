import os
from typing import List
from ..constants import PATH_MAZES, PATH_DISTANCES, NODE_NAMES, DIST_NAMES
from .node import Node
from .a_star import AStarNode, AStar


class Maze:
    def __init__(self, index: int):
        """
        Initializes a maze with the specified index, loading nodes and distances.

        :param index: The index of the maze (used to select node and distance files).
        """
        self.astar = AStar()
        # Pre-computed shortest path distances
        self.shortest_path_distances: List[int] = []
        self.pill_indices: List[int] = []  # Indices of nodes with pills
        # Indices of nodes with power pills
        self.power_pill_indices: List[int] = []
        self.junction_indices: List[int] = []  # Indices of junction nodes
        self.initial_pacman_node_index: int = 0  # Starting node for Pac-Man
        self.lair_node_index: int = 0  # Ghost lair node
        self.initial_ghost_node_index: int = 0  # Starting node for ghosts
        self.graph: List[Node] = []  # The maze graph as a list of nodes
        self.name: str = ""  # Name of the maze

        self.load_nodes(NODE_NAMES[index])
        self.load_distances(DIST_NAMES[index])
        self.astar.create_graph(self.graph)

    def load_nodes(self, file_name: str):
        """
        Loads maze nodes from a file and initializes maze-specific information.

        :param file_name: The name of the maze file (without path).
        """
        try:
            with open(os.path.join(PATH_MAZES, f"{file_name}.txt"), 'r') as br:
                # Read preamble
                pr = br.readline().strip().split("\t")
                self.name = pr[0]
                self.initial_pacman_node_index = int(pr[1])
                self.lair_node_index = int(pr[2])
                self.initial_ghost_node_index = int(pr[3])
                graph_size = int(pr[4])
                pill_count = int(pr[5])
                power_pill_count = int(pr[6])
                junction_count = int(pr[7])

                self.graph = [None] * graph_size
                self.pill_indices = [0] * pill_count
                self.power_pill_indices = [0] * power_pill_count
                self.junction_indices = [0] * junction_count

                node_index = 0
                pill_index = 0
                power_pill_index = 0
                junction_index = 0

                # Read node data
                for line in br:
                    nd = line.strip().split("\t")
                    node = Node(
                        node_index=int(nd[0]),
                        x=int(nd[1]),
                        y=int(nd[2]),
                        pill_index=int(nd[7]),
                        power_pill_index=int(nd[8]),
                        neighbours=[int(nd[3]), int(nd[4]),
                                    int(nd[5]), int(nd[6])]
                    )
                    self.graph[node_index] = node
                    node_index += 1

                    if node.pill_index >= 0:
                        self.pill_indices[pill_index] = node.node_index
                        pill_index += 1
                    elif node.power_pill_index >= 0:
                        self.power_pill_indices[power_pill_index] = node.node_index
                        power_pill_index += 1

                    if node.num_neighbouring_nodes > 2:
                        self.junction_indices[junction_index] = node.node_index
                        junction_index += 1

        except IOError as e:
            print(f"Error loading nodes from {file_name}: {e}")

    def load_distances(self, file_name: str):
        """
        Loads pre-computed shortest path distances from a file.

        :param file_name: The name of the distance file (without path).
        """
        graph_size = len(self.graph)
        self.shortest_path_distances = [
            0] * ((graph_size * (graph_size - 1)) // 2 + graph_size)

        try:
            with open(os.path.join(PATH_DISTANCES, file_name), 'r') as br:
                index = 0
                for line in br:
                    self.shortest_path_distances[index] = int(line.strip())
                    index += 1
        except IOError as e:
            print(f"Error loading distances from {file_name}: {e}")
