import numpy as np
from utilities.DTO.boundaryConditionDTO import BoundaryConditionInitialDelta


class BoltzmannFluidState:
    def __init__(self, shape):
        self.fluid_state: np.array = np.zeros(shape + (19,))

    def update_fluid_initial_state(self, fluid_initial_delta: BoundaryConditionInitialDelta):
        x1, y1, z1 = fluid_initial_delta.boundary_cube.start_position.to_tuple()
        x2, y2, z2 = fluid_initial_delta.boundary_cube.end_position.to_tuple()
        self.fluid_state[x1:x2, y1:y2, z1:z2] = fluid_initial_delta.boltzmann_f19.vectors
