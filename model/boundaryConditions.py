import numpy as np
from utilities.DTO.boundaryConditionDTO import BoundaryConditionNoSlip, BoundaryConditionConstantVelocity


class BoundaryConditions:
    def __init__(self, shape):
        self.affected_cells = np.zeros(shape, dtype=bool)


class NoSlipBoundaryConditions(BoundaryConditions):
    def __init__(self, shape):
        super().__init__(shape)

    def update_boundary(self, boundary_condition_delta: BoundaryConditionNoSlip):
        pass


class ConstantVelocityBoundaryConditions(BoundaryConditions):
    def __init__(self, shape):
        super().__init__(shape)
        self.velocity = np.zeros(shape + (3,))

    def update_boundary(self, boundary_condition_delta: BoundaryConditionConstantVelocity):
        pass
