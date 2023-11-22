from typing import Tuple
import numpy as np


class BoltzmannFluid:
    fluid_lattice: np.ndarray

    def __init__(self, lattice_dimensions: Tuple[int, int, int]):
        self.fluid_lattice = np.zeros(lattice_dimensions)
