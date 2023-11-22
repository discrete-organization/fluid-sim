from typing import Tuple
from fluidDirectionProvider import FluidDirectionProvider
from boltzmannFluidState import BoltzmannFluidState
from boundaryConditions import NoSlipBoundaryConditions, ConstantVelocityBoundaryConditions
from utilities.DTO.boundaryConditionDTO import BoundaryConditionDelta,\
            BoundaryConditionNoSlip, BoundaryConditionConstantVelocity


class BoltzmannFluid:
    def __init__(self, lattice_dimensions: Tuple[int, int, int]):
        self._directions = FluidDirectionProvider.get_all_directions()
        self._normalized_directions = FluidDirectionProvider.normalize_directions(self._directions)
        self._fluid_state = BoltzmannFluidState(lattice_dimensions)
        self._no_slip_boundary_conditions = NoSlipBoundaryConditions(lattice_dimensions)
        self._constant_velocity_boundary_conditions = ConstantVelocityBoundaryConditions(lattice_dimensions)

    def update_no_slip_boundary(self, boundary_condition_delta: BoundaryConditionNoSlip):
        self._no_slip_boundary_conditions.update_boundary(boundary_condition_delta)

    def update_constant_velocity_boundary(self, boundary_condition_delta: BoundaryConditionConstantVelocity):
        self._constant_velocity_boundary_conditions.update_boundary(boundary_condition_delta)
