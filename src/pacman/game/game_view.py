import tkinter as tk
from PIL import Image, ImageTk
import os
from typing import Dict, List, Tuple
from pacman.game.constants import MOVE, GHOST, MAG, GV_WIDTH, GV_HEIGHT, PATH_IMAGES, MAZE_NAMES, EDIBLE_ALERT, MAZE_NAMES, PATH_IMAGES
from pacman.game.game import Game


class DebugPointer:
    def __init__(self, x: int, y: int, color: str):
        self.x = x
        self.y = y
        self.color = color


class DebugLine:
    def __init__(self, x1: int, y1: int, x2: int, y2: int, color: str):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color


class GameView:
    debug_pointers: List[DebugPointer] = []
    debug_lines: List[DebugLine] = []
    is_visible = True
    save_image = False
    image_file_name = ""

    def __init__(self, game: Game):
        """
        Initializes the game view.

        :param game: The game instance to visualize.
        """
        self.game = game
        # self.images = Images()
        self.images = None
        self.last_pacman_move = game.get_pacman_last_move_made()
        self.time = game.get_total_time()
        self.root = None  # This will now be correctly assigned
        self.canvas = None
        self.frame = None
        self.offscreen = None
        self.photo = None

    # Visual aids for debugging

    @staticmethod
    def add_points(game: Game, color: str, *node_indices: int):
        """
        Adds nodes to be highlighted with the specified color.

        :param game: The game instance.
        :param color: The color to use (e.g., 'red', '#FF0000').
        :param node_indices: The node indices to highlight.
        """
        if GameView.is_visible:
            for index in node_indices:
                GameView.debug_pointers.append(DebugPointer(
                    game.get_node_x_coord(index),
                    game.get_node_y_coord(index),
                    color
                ))

    @staticmethod
    def add_lines(game: Game, color: str, from_node_indices: List[int], to_node_indices: List[int]):
        """
        Adds lines between nodes with the specified color.

        :param game: The game instance.
        :param color: The color to use.
        :param from_node_indices: The starting node indices.
        :param to_node_indices: The ending node indices.
        """
        if GameView.is_visible:
            for from_idx, to_idx in zip(from_node_indices, to_node_indices):
                GameView.debug_lines.append(DebugLine(
                    game.get_node_x_coord(from_idx),
                    game.get_node_y_coord(from_idx),
                    game.get_node_x_coord(to_idx),
                    game.get_node_y_coord(to_idx),
                    color
                ))

    @staticmethod
    def add_line(game: Game, color: str, from_node_index: int, to_node_index: int):
        """
        Adds a single line between two nodes with the specified color.

        :param game: The game instance.
        :param color: The color to use.
        :param from_node_index: The starting node index.
        :param to_node_index: The ending node index.
        """
        if GameView.is_visible:
            GameView.debug_lines.append(DebugLine(
                game.get_node_x_coord(from_node_index),
                game.get_node_y_coord(from_node_index),
                game.get_node_x_coord(to_node_index),
                game.get_node_y_coord(to_node_index),
                color
            ))

    def draw_debug_info(self):
        """
        Draws debug information (points and lines) on the canvas and clears them.
        """
        for dp in GameView.debug_pointers:
            self.canvas.create_rectangle(
                dp.x * MAG + 1, dp.y * MAG + 5,
                dp.x * MAG + 11, dp.y * MAG + 15,
                fill=dp.color, outline=dp.color
            )

        for dl in GameView.debug_lines:
            self.canvas.create_line(
                dl.x1 * MAG + 5, dl.y1 * MAG + 10,
                dl.x2 * MAG + 5, dl.y2 * MAG + 10,
                fill=dl.color
            )

        GameView.debug_pointers.clear()
        GameView.debug_lines.clear()

    @staticmethod
    def save_image(file_name: str):
        """
        Requests to save the current game state as an image.

        :param file_name: The name of the image file.
        """
        GameView.save_image = True
        GameView.image_file_name = file_name

    # def _save_image(self):
    #     """
    #     Saves the current canvas as a PNG image.
    #     """
    #     try:
    #         os.makedirs("myData", exist_ok=True)
    #         self.canvas.postscript(file="temp.ps")
    #         img = Image.open("temp.ps")
    #         img.save(f"myData/{self.image_file_name}.png", "png")
    #         os.remove("temp.ps")
    #     except Exception as e:
    #         print(f"Error saving image: {e}")
    #     GameView.save_image = False
    def _save_image(self):
        """
        Saves the current canvas as a PNG image without requiring Ghostscript.
        Captures the canvas area directly from the screen.
        """
        try:
            # Ensure target folder exists
            os.makedirs("myData", exist_ok=True)

            # Make sure geometry is up to date
            self.canvas.update_idletasks()

            # Compute absolute screen bbox of the canvas
            x = self.canvas.winfo_rootx()
            y = self.canvas.winfo_rooty()
            w = x + self.canvas.winfo_width()
            h = y + self.canvas.winfo_height()

            # Grab pixels and save
            from PIL import ImageGrab
            img = ImageGrab.grab(bbox=(x, y, w, h))
            img.save(f"myData/{self.image_file_name}.png", "PNG")
        except Exception as e:
            print(f"Error saving image: {e}")
        finally:
            GameView.save_image = False

    # Rendering methods

    def render(self):
        """
        Renders the game state on the canvas.
        """
        if self.canvas is None:
            return

        self.time = self.game.get_total_time()
        self.canvas.delete("all")  # Clear the canvas

        self.draw_maze()
        self.draw_debug_info()
        self.draw_pills()
        self.draw_power_pills()
        self.draw_pacman()
        self.draw_ghosts()
        self.draw_lives()
        self.draw_game_info()

        if self.game.game_over():
            self.draw_game_over()

        if GameView.save_image:
            self._save_image()

    def draw_maze(self):
        """
        Draws the current maze.
        """
        self.canvas.create_rectangle(
            0, 0, GV_WIDTH * MAG, GV_HEIGHT * MAG + 20, fill="black")
        maze_image = self.images.get_maze(self.game.get_maze_index())
        self.canvas.create_image(2, 6, anchor="nw", image=maze_image)

    def draw_pills(self):
        """
        Draws the remaining pills.
        """
        pill_nodes = self.game.get_pill_indices()  # list of NODE indices
        # Availability checks use the pill LIST index (0..len-1)
        for pill_idx, node_idx in enumerate(pill_nodes):
            if self.game.is_pill_still_available(pill_idx):
                self.canvas.create_oval(
                    self.game.get_node_x_coord(node_idx) * MAG + 4,
                    self.game.get_node_y_coord(node_idx) * MAG + 8,
                    self.game.get_node_x_coord(node_idx) * MAG + 7,
                    self.game.get_node_y_coord(node_idx) * MAG + 11,
                    fill="white", outline="white"
                )

    def draw_power_pills(self):
        """
        Draws the remaining power pills.
        """
        power_nodes = self.game.get_power_pill_indices()  # list of NODE indices
        # Availability checks use the power pill LIST index (0..len-1)
        for pp_idx, node_idx in enumerate(power_nodes):
            if self.game.is_power_pill_still_available(pp_idx):
                self.canvas.create_oval(
                    self.game.get_node_x_coord(node_idx) * MAG + 1,
                    self.game.get_node_y_coord(node_idx) * MAG + 5,
                    self.game.get_node_x_coord(node_idx) * MAG + 9,
                    self.game.get_node_y_coord(node_idx) * MAG + 13,
                    fill="white", outline="white"
                )

    def draw_pacman(self):
        """
        Draws Pac-Man at its current position.
        """
        pac_loc = self.game.get_pacman_current_node_index()
        tmp_last_pacman_move = self.game.get_pacman_last_move_made()
        if tmp_last_pacman_move != MOVE.NEUTRAL:
            self.last_pacman_move = tmp_last_pacman_move
        pac_image = self.images.get_pacman(self.last_pacman_move, self.time)
        self.canvas.create_image(
            self.game.get_node_x_coord(pac_loc) * MAG - 1,
            self.game.get_node_y_coord(pac_loc) * MAG + 3,
            anchor="nw", image=pac_image
        )

    def draw_ghosts(self):
        """
        Draws the ghosts at their current positions.
        """
        for ghost_type in GHOST:
            current_node_index = self.game.get_ghost_current_node_index(
                ghost_type)
            node_x_coord = self.game.get_node_x_coord(current_node_index)
            node_y_coord = self.game.get_node_y_coord(current_node_index)
            if self.game.get_ghost_edible_time(ghost_type) > 0:
                blinking = self.game.get_ghost_edible_time(
                    ghost_type) < EDIBLE_ALERT and ((self.time % 6) // 3) == 0
                ghost_image = self.images.get_edible_ghost(blinking, self.time)
                self.canvas.create_image(
                    node_x_coord * MAG - 1,
                    node_y_coord * MAG + 3,
                    anchor="nw", image=ghost_image
                )
            else:
                index = ghost_type.value  # Using enum value as index
                ghost_image = self.images.get_ghost(
                    ghost_type, self.game.get_ghost_last_move_made(ghost_type), self.time)
                x_offset = (
                    index * 5) if self.game.get_ghost_lair_time(ghost_type) > 0 else 0
                self.canvas.create_image(
                    node_x_coord * MAG - 1 + x_offset,
                    node_y_coord * MAG + 3,
                    anchor="nw", image=ghost_image
                )

    def draw_lives(self):
        """
        Draws the remaining lives for Pac-Man.
        """
        for i in range(self.game.get_pacman_number_of_lives_remaining() - 1):  # -1 as current life is included
            lives_image = self.images.get_pacman_for_extra_lives()
            self.canvas.create_image(
                210 - (30 * i) // 2,
                260,
                anchor="nw", image=lives_image
            )

    def draw_game_info(self):
        """
        Draws the game information (score, level, time).
        """
        self.canvas.create_text(4, 271, text="S: ", fill="white", anchor="nw")
        self.canvas.create_text(16, 271, text=str(
            self.game.get_score()), fill="white", anchor="nw")
        self.canvas.create_text(78, 271, text="L: ", fill="white", anchor="nw")
        self.canvas.create_text(90, 271, text=str(
            self.game.get_current_level() + 1), fill="white", anchor="nw")
        self.canvas.create_text(116, 271, text="T: ",
                                fill="white", anchor="nw")
        self.canvas.create_text(129, 271, text=str(
            self.game.get_current_level_time()), fill="white", anchor="nw")

    def draw_game_over(self):
        """
        Draws the 'Game Over' message.
        """
        self.canvas.create_text(80, 150, text="Game Over",
                                fill="white", anchor="nw")

    def get_preferred_size(self) -> Tuple[int, int]:
        """
        :return: The preferred size of the game view (width, height).
        """
        return GV_WIDTH * MAG, GV_HEIGHT * MAG + 20

    def show_game(self) -> 'GameView':
        """
        Displays the game window.

        :return: The GameView instance.
        """
        # self.frame = GameFrame(self)
        # self.root.after(2000, self.render)  # Delay rendering by 2 seconds
        # Create the window and assign it to self.root
        self.frame = GameFrame(self)

        # REMOVE the incorrect .after() call. The Executor handles the game loop.
        # self.root.after(2000, self.render)
        return self

    def get_frame(self) -> 'GameFrame':
        """
        :return: The game frame.
        """
        return self.frame


class GameFrame(tk.Tk):
    def __init__(self, game_view: GameView):
        """
        Initializes the game window.

        :param game_view: The GameView instance to display.
        """
        super().__init__()
        self.game_view = game_view
        self.game_view.root = self 
        self.title("Ms. Pac-Man")
        self.canvas = tk.Canvas(
            self,
            width=GV_WIDTH * MAG,
            height=GV_HEIGHT * MAG + 20,
            bg="black"
        )
        self.game_view.images = Images(master=self)
        self.canvas.pack()

        self.canvas.focus_set()
        self.focus_force()

        self.game_view.canvas = self.canvas
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(
            f"+{int(screen_width * 3 / 8)}+{int(screen_height * 3 / 8)}")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.update()
        
    # ADD THIS NEW METHOD
    def bind_keys(self, keyboard_input):
        """Binds keyboard events to the game."""
        # self.bind("<KeyPress-Up>", lambda e: keyboard_input.key_pressed(e))
        # self.bind("<KeyPress-Down>", lambda e: keyboard_input.key_pressed(e))
        # self.bind("<KeyPress-Left>", lambda e: keyboard_input.key_pressed(e))
        # self.bind("<KeyPress-Right>", lambda e: keyboard_input.key_pressed(e))
        # self.bind("<KeyPress>", lambda e: keyboard_input.key_pressed(e))

        self.bind("<KeyPress>", keyboard_input.key_pressed)
        print("[DEBUG] Keyboard input has been bound to the game window.")


class Images:
    def __init__(self, master=None):
        """
        Initializes the image resources for the game.
        """
        self.master = master
        self.pacman: Dict[MOVE, List[ImageTk.PhotoImage]] = {}
        self.ghosts: Dict[GHOST, Dict[MOVE, List[ImageTk.PhotoImage]]] = {}
        self.edible_ghosts: List[ImageTk.PhotoImage] = []
        self.edible_blinking_ghosts: List[ImageTk.PhotoImage] = []
        self.mazes: List[ImageTk.PhotoImage] = []

        # Load Pac-Man images
        self.pacman[MOVE.UP] = [
            self._load_image("mspacman-up-normal.png"),
            self._load_image("mspacman-up-open.png"),
            self._load_image("mspacman-up-closed.png")
        ]
        self.pacman[MOVE.RIGHT] = [
            self._load_image("mspacman-right-normal.png"),
            self._load_image("mspacman-right-open.png"),
            self._load_image("mspacman-right-closed.png")
        ]
        self.pacman[MOVE.DOWN] = [
            self._load_image("mspacman-down-normal.png"),
            self._load_image("mspacman-down-open.png"),
            self._load_image("mspacman-down-closed.png")
        ]
        self.pacman[MOVE.LEFT] = [
            self._load_image("mspacman-left-normal.png"),
            self._load_image("mspacman-left-open.png"),
            self._load_image("mspacman-left-closed.png")
        ]

        # Load ghost images
        self.ghosts[GHOST.BLINKY] = {
            MOVE.UP: [self._load_image("blinky-up-1.png"), self._load_image("blinky-up-2.png")],
            MOVE.RIGHT: [self._load_image("blinky-right-1.png"), self._load_image("blinky-right-2.png")],
            MOVE.DOWN: [self._load_image("blinky-down-1.png"), self._load_image("blinky-down-2.png")],
            MOVE.LEFT: [self._load_image(
                "blinky-left-1.png"), self._load_image("blinky-left-2.png")]
        }
        self.ghosts[GHOST.PINKY] = {
            MOVE.UP: [self._load_image("pinky-up-1.png"), self._load_image("pinky-up-2.png")],
            MOVE.RIGHT: [self._load_image("pinky-right-1.png"), self._load_image("pinky-right-2.png")],
            MOVE.DOWN: [self._load_image("pinky-down-1.png"), self._load_image("pinky-down-2.png")],
            MOVE.LEFT: [self._load_image(
                "pinky-left-1.png"), self._load_image("pinky-left-2.png")]
        }
        self.ghosts[GHOST.INKY] = {
            MOVE.UP: [self._load_image("inky-up-1.png"), self._load_image("inky-up-2.png")],
            MOVE.RIGHT: [self._load_image("inky-right-1.png"), self._load_image("inky-right-2.png")],
            MOVE.DOWN: [self._load_image("inky-down-1.png"), self._load_image("inky-down-2.png")],
            MOVE.LEFT: [self._load_image(
                "inky-left-1.png"), self._load_image("inky-left-2.png")]
        }
        self.ghosts[GHOST.SUE] = {
            MOVE.UP: [self._load_image("sue-up-1.png"), self._load_image("sue-up-2.png")],
            MOVE.RIGHT: [self._load_image("sue-right-1.png"), self._load_image("sue-right-2.png")],
            MOVE.DOWN: [self._load_image("sue-down-1.png"), self._load_image("sue-down-2.png")],
            MOVE.LEFT: [self._load_image(
                "sue-left-1.png"), self._load_image("sue-left-2.png")]
        }

        # Load edible ghost images
        self.edible_ghosts = [
            self._load_image("edible-ghost-1.png"),
            self._load_image("edible-ghost-2.png")
        ]
        self.edible_blinking_ghosts = [
            self._load_image("edible-ghost-blink-1.png"),
            self._load_image("edible-ghost-blink-2.png")
        ]

        # Load maze images
        self.mazes = [self._load_image(maze_name) for maze_name in MAZE_NAMES]

    def get_pacman(self, move: MOVE, time: int) -> ImageTk.PhotoImage:
        """
        :param move: The move direction for Pac-Man.
        :param time: The current game time for animation.
        :return: The Pac-Man image for the given move and time.
        """
        return self.pacman[move][(time % 6) // 2]

    def get_pacman_for_extra_lives(self) -> ImageTk.PhotoImage:
        """
        :return: The Pac-Man image used for extra lives display.
        """
        return self.pacman[MOVE.RIGHT][0]

    def get_ghost(self, ghost: GHOST, move: MOVE, time: int) -> ImageTk.PhotoImage:
        """
        :param ghost: The ghost type.
        :param move: The move direction for the ghost.
        :param time: The current game time for animation.
        :return: The ghost image for the given type, move, and time.
        """
        if move == MOVE.NEUTRAL:
            return self.ghosts[ghost][MOVE.UP][(time % 6) // 3]
        return self.ghosts[ghost][move][(time % 6) // 3]

    def get_edible_ghost(self, blinking: bool, time: int) -> ImageTk.PhotoImage:
        """
        :param blinking: Whether the edible ghost is blinking.
        :param time: The current game time for animation.
        :return: The edible ghost image.
        """
        if not blinking:
            return self.edible_ghosts[(time % 6) // 3]
        return self.edible_blinking_ghosts[(time % 6) // 3]

    def get_maze(self, maze_index: int) -> ImageTk.PhotoImage:
        """
        :param maze_index: The index of the maze.
        :return: The maze image.
        """
        return self.mazes[maze_index]

    def _load_image(self, file_name: str) -> ImageTk.PhotoImage:
        """
        Loads an image from the specified file.

        :param file_name: The name of the image file.
        :return: The loaded image as a PhotoImage.
        """
        try:
            path = os.path.join(PATH_IMAGES, file_name)
            print(path)
            image = Image.open(path)
            return ImageTk.PhotoImage(image, master=self.master)
        except Exception as e:
            print(f"Error loading image {file_name}: {e}")
            return None
