# pacman/game/internal/node.py

from typing import Dict
from pacman.game.constants import MOVE


class Node:
    def __init__(self, node_index: int, x: int, y: int, pill_index: int, power_pill_index: int, neighbours: list[int]):
        self.node_index = node_index
        self.x = x
        self.y = y
        self.pill_index = pill_index
        self.power_pill_index = power_pill_index
        self.neighbourhood: Dict[MOVE, int] = {}
        self.all_possible_moves: Dict[MOVE, List[MOVE]] = {}
        self.all_neighbouring_nodes: Dict[MOVE, List[int]] = {}
        self.all_neighbourhoods: Dict[MOVE, Dict[MOVE, int]] = {}

        moves = list(MOVE)
        for i, neigh in enumerate(neighbours):
            if neigh != -1:
                self.neighbourhood[moves[i]] = neigh

        self.num_neighbouring_nodes = len(self.neighbourhood)

        for move in moves:
            if move in self.neighbourhood:
                tmp = self.neighbourhood.copy()
                tmp.pop(move)
                self.all_neighbourhoods[move.opposite()] = tmp

        self.all_neighbourhoods[MOVE.NEUTRAL] = self.neighbourhood

        neighbouring_nodes = [0] * self.num_neighbouring_nodes
        possible_moves = [None] * self.num_neighbouring_nodes
        index = 0

        for move in moves:
            if move in self.neighbourhood:
                neighbouring_nodes[index] = self.neighbourhood[move]
                possible_moves[index] = move
                index += 1

        for move in moves:
            if move.opposite() in self.neighbourhood:
                tmp_neighbouring_nodes = [0] * \
                    (self.num_neighbouring_nodes - 1)
                tmp_possible_moves = [None] * (self.num_neighbouring_nodes - 1)
                index = 0

                for m in moves:
                    if m != move.opposite() and m in self.neighbourhood:
                        tmp_neighbouring_nodes[index] = self.neighbourhood[m]
                        tmp_possible_moves[index] = m
                        index += 1

                self.all_neighbouring_nodes[move] = tmp_neighbouring_nodes
                self.all_possible_moves[move] = tmp_possible_moves

        self.all_neighbouring_nodes[MOVE.NEUTRAL] = neighbouring_nodes
        self.all_possible_moves[MOVE.NEUTRAL] = possible_moves
