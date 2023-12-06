from utilities.DTO.vector3 import Vector3Int
import numpy as np


class FluidDirectionProvider:
    @staticmethod
    def __get_direction_for_0(_: int) -> Vector3Int:
        return Vector3Int(0, 0, 0)

    @staticmethod
    def __get_direction_for_1_to_6(n: int) -> Vector3Int:
        k = n - 1

        one_position = k // 2
        value = -1 if k % 2 == 1 else 1

        result = np.zeros(3).astype(np.int32)

        result[one_position] = value

        return Vector3Int.from_numpy(result)

    @staticmethod
    def __get_direction_for_7_18(n: int) -> Vector3Int:
        k = n - 7

        zero_position = 2 - k // 4
        ones_state = k % 4

        first_one = (ones_state % 2) * 2 - 1
        second_one = (ones_state // 2) * 2 - 1

        if zero_position == 0:
            return Vector3Int(0, first_one, second_one)
        if zero_position == 1:
            return Vector3Int(first_one, 0, second_one)
        return Vector3Int(first_one, second_one, 0)

    @staticmethod
    def get_direction(n: int) -> Vector3Int:
        if n < 0 or n > 18:
            raise ValueError(f"n must be between 0 and 18, but is {n}")

        if n == 0:
            return FluidDirectionProvider.__get_direction_for_0(n)
        if n <= 6:
            return FluidDirectionProvider.__get_direction_for_1_to_6(n)
        return FluidDirectionProvider.__get_direction_for_7_18(n)

    @staticmethod
    def get_all_directions() -> np.ndarray[np.ndarray[np.int32]]:
        result = np.zeros((19, 3))

        for i in range(19):
            result[i] = FluidDirectionProvider.get_direction(i).to_numpy()

        return result

    @staticmethod
    def normalize_directions(directions: np.ndarray[np.ndarray[np.int32]]) -> np.ndarray[np.ndarray[np.float64]]:
        lengths = np.sqrt(np.sum(np.square(directions), -1))

        normalized_directions = np.zeros_like(directions, dtype=np.float64)
        normalized_directions[1:] = directions[1:] / lengths[1:, None]

        return normalized_directions
    
    @staticmethod
    def get_reverse_direction_index(direction_index: int) -> int:
        if direction_index == 0:
            return 0
        if direction_index <= 6:
            return direction_index - 1 if direction_index % 2 == 0 else direction_index + 1
        index_from_7 = direction_index - 7
        part = index_from_7 // 4
        index_in_part = index_from_7 % 4

        return 7 + part * 4 + 3 - index_in_part

    @staticmethod
    def get_reverse_directions_indices() -> np.ndarray[np.int32]:
        return np.array([FluidDirectionProvider.get_reverse_direction_index(i) for i in range(19)])
