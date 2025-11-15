# src/pacman/controllers/examples/nearest_pill_pacman_vs.py

from pacman.controllers.controller import Controller
from pacman.game.game import Game
from pacman.game.game_view import GameView
from pacman.game.constants import MOVE, DM, GHOST
from tkinter import Canvas


class NearestPillPacManVS(Controller):
    def _get_move(self, game: Game, time_due: int) -> MOVE:
        current_node_index = game.get_pacman_current_node_index()
        active_pills = game.get_active_pills_indices()
        active_power_pills = game.get_active_power_pills_indices()
        target_node_indices = active_pills + active_power_pills
        nearest = game.get_closest_node_index_from_node_index(
            current_node_index, target_node_indices, DM.PATH)

        # Visuals (commented out as in original)
        # GameView.add_points(game, "green", game.get_shortest_path(game.get_pacman_current_node_index(), nearest))
        # GameView.add_points(game, "cyan", game.get_shortest_path(game.get_pacman_current_node_index(), game.get_power_pill_indices()[0]))
        # GameView.add_points(game, "cyan", game.get_a_star_path(game.get_pacman_current_node_index(), game.get_power_pill_indices()[0]))
        # GameView.add_points(game, "yellow", game.get_non_reverse_path(game.get_pacman_current_node_index(), game.get_power_pill_indices()[0], game.get_pacman_last_move_made()))
        # for i in range(len(active_power_pills)):
        #     GameView.add_lines(game, "cyan", game.get_pacman_current_node_index(), active_power_pills[i])
        # for ghost_type in GHOST:
        #     if game.get_ghost_lair_time(ghost_type) == 0:
        #         color = "green" if game.is_ghost_edible(ghost_type) else "red"
        #         GameView.add_lines(game, color, game.get_pacman_current_node_index(), game.get_ghost_current_node_index(ghost_type))
        if game.get_ghost_lair_time(GHOST.BLINKY) == 0 and len(active_power_pills) > 0:
            GameView.add_points(game, "red", game.get_a_star_path(
                game.get_ghost_current_node_index(GHOST.BLINKY), active_power_pills[0], MOVE.NEUTRAL))
            GameView.add_points(game, "yellow", game.get_a_star_path(game.get_ghost_current_node_index(
                GHOST.BLINKY), active_power_pills[0], game.get_ghost_last_move_made(GHOST.BLINKY)))
        # if game.get_ghost_lair_time(GHOST.BLINKY) == 0 and len(active_power_pills) > 0:
        #     GameView.add_points(game, "white", game.get_a_star_path(game.get_ghost_current_node_index(GHOST.BLINKY),
        #         game.get_closest_node_index_from_node_index(game.get_ghost_current_node_index(GHOST.BLINKY), active_power_pills, DM.PATH)))
        # colors = ["red", "blue", "magenta", "orange"]
        # index = 0
        # for ghost_type in GHOST:
        #     if game.get_ghost_lair_time(ghost_type) == 0:
        #         GameView.add_points(game, colors[index], game.get_a_star_path(game.get_ghost_current_node_index(ghost_type), current_node_index, game.get_ghost_last_move_made(ghost_type)))
        #         index += 1

        return game.get_next_move_towards_target(game.get_pacman_current_node_index(), nearest, DM.PATH)
