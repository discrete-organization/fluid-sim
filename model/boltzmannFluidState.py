import numpy as np
from utilities.DTO.boundaryConditionDTO import BoundaryConditionInitial


class BoltzmannFluidState:
    def __init__(self, shape):
        self.fluid_state: np.array = np.zeros(shape + (19,))

    def update_fluid_initial_state(self, fluid_initial_delta: BoundaryConditionInitial):
        pass
