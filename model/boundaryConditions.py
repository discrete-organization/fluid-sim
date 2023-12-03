import numpy as np
from utilities.DTO.boundaryConditionDTO import (
    BoundaryConditionNoSlipDelta,
    BoundaryConditionConstantVelocityDelta,
    BoundaryCube
)
from .boltzmannFluidUtils import BoltzmannFluidState


class BoundaryConditions:
    def _update_affected_cells(self, boundary_cube: BoundaryCube) -> None:
        x1, y1, z1 = boundary_cube.start_position.to_tuple()
        x2, y2, z2 = boundary_cube.end_position.to_tuple()

        self.affected_cells[x1:x2, y1:y2, z1:z2] = True

    def __init__(self, shape: tuple[int, int, int], allowed_velocities: np.ndarray[np.ndarray[np.int32]]):
        self.affected_cells = np.zeros(shape, dtype=bool)
        self.allowed_velocities = allowed_velocities

    def process_fluid_state(self, _: BoltzmannFluidState) -> None:
        pass
        


class NoSlipBoundaryConditions(BoundaryConditions):
    def __init__(self, shape: tuple[int, int, int], allowed_velocities: np.ndarray[np.ndarray[np.int32]]):
        super().__init__(shape, allowed_velocities)

    def update_boundary(self, boundary_condition_delta: BoundaryConditionNoSlipDelta) -> None:
        self._update_affected_cells(boundary_condition_delta.boundary_cube)

    def process_fluid_state(self, fluid_state: BoltzmannFluidState) -> None:
        fluid_state_matrix = fluid_state.fluid_state
        affected_fluid_matrix = fluid_state_matrix[self.affected_cells, :]
        fluid_state_matrix[self.affected_cells, :] = 0

        # TODO: Verify that this is correct @Rafał
        for i, dr in enumerate(self.allowed_velocities):
            dx, dy, dz = dr
            fluid_state_matrix[self.affected_cells, :] += np.roll(affected_fluid_matrix[i], (dx, dy, dz), axis=(0, 1, 2))
            

class ConstantVelocityBoundaryConditions(BoundaryConditions):
    def _update_velocities(self, boundary_condition_delta: BoundaryConditionConstantVelocityDelta) -> None:
        x1, y1, z1 = boundary_condition_delta.boundary_cube.start_position.to_tuple()
        x2, y2, z2 = boundary_condition_delta.boundary_cube.end_position.to_tuple()
        self.velocity[x1:x2, y1:y2, z1:z2] = boundary_condition_delta.velocity.to_tuple()

    def __init__(self, shape: tuple[int, int, int], allowed_velocities: np.ndarray[np.ndarray[np.int32]]):
        super().__init__(shape, allowed_velocities)
        self.velocity = np.zeros(shape + (3,))

    def update_boundary(self, boundary_condition_delta: BoundaryConditionConstantVelocityDelta) -> None:
        self._update_affected_cells(boundary_condition_delta.boundary_cube)
        self._update_velocities(boundary_condition_delta)

    def process_fluid_state(self, fluid_state: BoltzmannFluidState) -> None:
        raise NotImplementedError()
