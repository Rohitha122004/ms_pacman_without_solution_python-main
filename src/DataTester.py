from pacman.data_recording.data_saver_loader import load_pacman_data
from pacman.data_recording.data_tuple import DataTuple


def main():
    tuples = load_pacman_data()
    counter = 0
    for d in tuples:
        print(f"Normal: {d.get_save_string()}")
        print(
            f"Discrete: {d.direction_chosen}, {d.maze_index}, {d.current_level}, "
            f"{d.discretize_position(d.pacman_position)}, {d.pacman_lives_left}, "
            f"{d.discretize_current_score(d.current_score)}, {d.discretize_current_level_time(d.current_level_time)}, "
            f"{d.discretize_number_of_pills(d.num_of_pills_left)}, {d.discretize_number_of_power_pills(d.num_of_power_pills_left)}, "
            f"{d.is_blinky_edible}, {d.is_inky_edible}, {d.is_pinky_edible}, {d.is_sue_edible}, "
            f"{d.discretize_distance(d.blinky_dist)}, {d.discretize_distance(d.inky_dist)}, "
            f"{d.discretize_distance(d.pinky_dist)}, {d.discretize_distance(d.sue_dist)}, "
            f"{d.blinky_dir}, {d.inky_dir}, {d.pinky_dir}, {d.sue_dir}"
        )
        counter += 1
        if counter > 100:
            break
