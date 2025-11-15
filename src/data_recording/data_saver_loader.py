# src/pacman/data_recording/data_saver_loader.py

from typing import List
from .data_tuple import DataTuple


class DataSaverLoader:
    FILE_NAME: str = "trainingData.txt"

    @staticmethod
    def save_pacman_data(data: DataTuple) -> None:
        with open(DataSaverLoader.FILE_NAME, "a") as file:
            file.write(data.get_save_string() + "\n")

    @staticmethod
    def load_pacman_data() -> List[DataTuple]:
        with open(DataSaverLoader.FILE_NAME, "r") as file:
            data = file.read()
        data_lines = data.split("\n")
        data_tuples = []
        for line in data_lines:
            if line.strip():
                data_tuples.append(DataTuple(line))
        return data_tuples
