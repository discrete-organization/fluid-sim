import unittest
import numpy as np
from model.fluidDirectionProvider import FluidDirectionProvider
from utilities.DTO.vector3 import Vector3Int



class TestFluidDirectionProvider(unittest.TestCase):
    def test_normalize_directions(self):
        directions = np.array([[0, 0], [3, 4], [5, 12]], dtype=np.int32)
        expected_result = np.array(
            [[0, 0], [0.6, 0.8], [0.381, 0.925]], dtype=np.float64
        )

        normalized_directions = FluidDirectionProvider.normalize_directions(directions)
        np.testing.assert_allclose(normalized_directions, expected_result)

    def test_get_direction(self):
        for i in range(19):
            direction = FluidDirectionProvider.get_direction(i)
            self.assertIsInstance(direction, Vector3Int)

    def test_get_all_directions(self):
        all_directions = FluidDirectionProvider.get_all_directions()
        self.assertEqual(all_directions.shape, (19, 3))
        self.assertIsInstance(all_directions, np.ndarray)

    def test_get_reverse_direction_index(self):
        for i in range(19):
            reverse_index = FluidDirectionProvider.get_reverse_direction_index(i)
            self.assertIsInstance(reverse_index, int)

    def test_get_reverse_directions_indices(self):
        reverse_indices = FluidDirectionProvider.get_reverse_directions_indices()
        self.assertEqual(reverse_indices.shape, (19,))
        self.assertIsInstance(reverse_indices, np.ndarray)


if __name__ == "__main__":
    unittest.main()
    import numpy as np
    from fluidDirectionProvider import FluidDirectionProvider