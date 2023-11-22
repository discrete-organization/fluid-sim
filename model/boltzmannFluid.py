from typing import Tuple
from fluidDirectionProvider import FluidDirectionProvider
from boltzmannFluidState import BoltzmannFluidState


class BoltzmannFluid:
    def __init__(self, lattice_dimensions: Tuple[int, int, int]):
        self._directions = FluidDirectionProvider.get_all_directions()
        self._normalized_directions = FluidDirectionProvider.normalize_directions(self._directions)
        self._fluid_state = BoltzmannFluidState(lattice_dimensions)
