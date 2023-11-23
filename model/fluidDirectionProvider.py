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
            raise Exception("Invalid direction index.")

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
    def normalize_directions(directions: np.ndarray[np.ndarray[np.int32]]) -> np.ndarray[np.ndarray[np.int32]]:
        lengths = np.sqrt(np.sum(np.square(directions), -1))

        normalized_directions = np.zeros_like(directions)
        normalized_directions[1:] = directions[1:] / lengths[1:, None]

        return normalized_directions
