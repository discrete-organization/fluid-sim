import numpy as np
from utilities.DTO.boundaryConditionDTO import (
    BoundaryConditionNoSlipDelta,
    BoundaryConditionConstantVelocityDelta,
    BoundaryConditionInitialDelta,
    BoundaryCube
)


class BoundaryConditions:
    def _update_affected_cells(self, boundary_cube: BoundaryCube) -> None:
        x1, y1, z1 = boundary_cube.start_position.to_tuple()
        x2, y2, z2 = boundary_cube.end_position.to_tuple()

        self.affected_cells[x1:x2, y1:y2, z1:z2] = True

    def __init__(self, shape):
        self.affected_cells = np.zeros(shape, dtype=bool)


class NoSlipBoundaryConditions(BoundaryConditions):
    def __init__(self, shape):
        super().__init__(shape)

    def update_boundary(self, boundary_condition_delta: BoundaryConditionNoSlipDelta) -> None:
        self._update_affected_cells(boundary_condition_delta.boundary_cube)


class ConstantVelocityBoundaryConditions(BoundaryConditions):
    def _update_velocities(self, boundary_condition_delta: BoundaryConditionConstantVelocityDelta) -> None:
        x1, y1, z1 = boundary_condition_delta.boundary_cube.start_position.to_tuple()
        x2, y2, z2 = boundary_condition_delta.boundary_cube.end_position.to_tuple()
        self.velocity[x1:x2, y1:y2, z1:z2] = boundary_condition_delta.velocity.to_tuple()

    def __init__(self, shape):
        super().__init__(shape)
        self.velocity = np.zeros(shape + (3,))

    def update_boundary(self, boundary_condition_delta: BoundaryConditionConstantVelocityDelta) -> None:
        self._update_affected_cells(boundary_condition_delta.boundary_cube)
        self._update_velocities(boundary_condition_delta)

