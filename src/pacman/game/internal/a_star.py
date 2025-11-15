# pacman/game/internal/a_star.py

from typing import List, Optional, TYPE_CHECKING
from queue import PriorityQueue
from pacman.game.constants import MOVE

if TYPE_CHECKING:
    from pacman.game.game import Game  # only for type hints, no runtime import


class AStarNode:
    def __init__(self, index: int):
        self.parent: Optional['AStarNode'] = None
        self.g: float = 0.0
        self.h: float = 0.0
        self.adj: List['AStarEdge'] = []
        self.index: int = index
        self.reached: Optional[MOVE] = None

    def __eq__(self, other: 'AStarNode') -> bool:
        return self.index == other.index

    def __lt__(self, other: 'AStarNode') -> bool:
        return (self.g + self.h) < (other.g + other.h)

    def __str__(self) -> str:
        return str(self.index)


class AStarEdge:
    def __init__(self, node: AStarNode, move: MOVE, cost: float):
        self.node = node
        self.move = move
        self.cost = cost


class AStar:
    def __init__(self):
        self.graph: List[AStarNode] = []

    def create_graph(self, nodes: List['Node']):
        self.graph = [AStarNode(node.node_index) for node in nodes]
        for i, node in enumerate(nodes):
            for move, neighbour in node.neighbourhood.items():
                if neighbour is not None:
                    self.graph[i].adj.append(
                        AStarEdge(self.graph[neighbour], move, 1))

    def compute_paths_a_star(
        self,
        s: int,
        t: int,
        last_move_made: MOVE,
        game: Optional['Game'] = None,  # allow None
    ) -> List[int]:
        start = self.graph[s]
        target = self.graph[t]

        open_queue = PriorityQueue()
        closed: List[AStarNode] = []

        # Heuristic function: 0 (Dijkstra) when game is None
        def h(u_idx: int, v_idx: int) -> float:
            if game is None:
                return 0.0
            # If your distance function might touch path_cache, ensure *it* also has a fallback (see step 2).
            return game.get_shortest_path_distance(u_idx, v_idx)

        start.g = 0.0
        start.h = h(start.index, target.index)
        start.reached = last_move_made
        open_queue.put(start)

        while not open_queue.empty():
            current_node = open_queue.get()
            closed.append(current_node)

            if current_node == target:
                break

            for next_edge in current_node.adj:
                # Prevent immediate reversals if last_move_made is meaningful
                if current_node.reached is not None and next_edge.move == current_node.reached.opposite():
                    continue

                cand_g = current_node.g + next_edge.cost

                if next_edge.node not in open_queue.queue and next_edge.node not in closed:
                    next_edge.node.g = cand_g
                    next_edge.node.h = h(next_edge.node.index, target.index)
                    next_edge.node.parent = current_node
                    next_edge.node.reached = next_edge.move
                    open_queue.put(next_edge.node)
                elif cand_g < next_edge.node.g:
                    next_edge.node.g = cand_g
                    next_edge.node.parent = current_node
                    next_edge.node.reached = next_edge.move

                    if next_edge.node in open_queue.queue:
                        open_queue.queue.remove(next_edge.node)
                    if next_edge.node in closed:
                        closed.remove(next_edge.node)
                    open_queue.put(next_edge.node)

        return self.extract_path(target)

    def compute_paths_a_star_neutral(self, s: int, t: int, game: Optional['Game'] = None) -> List[int]:
        return self.compute_paths_a_star(s, t, MOVE.NEUTRAL, game)

    def extract_path(self, target: AStarNode) -> List[int]:
        route = [target.index]
        current = target
        while current.parent is not None:
            route.append(current.parent.index)
            current = current.parent
        route.reverse()
        return route

    def reset_graph(self):
        for node in self.graph:
            node.g = 0.0
            node.h = 0.0
            node.parent = None
            node.reached = None
