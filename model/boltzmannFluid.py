from typing import Tuple
from .fluidDirectionProvider import FluidDirectionProvider
from .boltzmannFluidUtils import (
    BoltzmannFluidState,
    FluidDensityState,
    FluidVelocityState
)
from .boundaryConditions import NoSlipBoundaryConditions, ConstantVelocityBoundaryConditions
from .equilibriumFluidSolver import EquilibriumFluidState, EquilibriumWeights, RelaxedBoltzmannFluidState
from utilities.DTO.boundaryConditionDTO import (
    BoundaryConditionNoSlipDelta,
    BoundaryConditionConstantVelocityDelta,
    BoundaryConditionInitialDelta
)
from utilities.DTO.simulationParameters import SimulationParameters


class BoltzmannFluid:
    '''
    One BoltzmannFluid object represents one frame in the fluid simulation.
    '''
    def __init__(self, lattice_dimensions: Tuple[int, int, int], simulation_params: SimulationParameters):
        self._directions = FluidDirectionProvider.get_all_directions()
        self._normalized_directions = FluidDirectionProvider.normalize_directions(self._directions)
        self._fluid_state = BoltzmannFluidState(lattice_dimensions, self._directions) # Verify this is correct @Rafał
        self._no_slip_boundary_conditions = NoSlipBoundaryConditions(lattice_dimensions, self._directions)
        self._constant_velocity_boundary_conditions = ConstantVelocityBoundaryConditions(lattice_dimensions,
                                                                                         self._directions)
        self._equilibrium_weights = EquilibriumWeights()
        self._simulation_params = simulation_params

    def update_no_slip_boundary(self, boundary_condition_delta: BoundaryConditionNoSlipDelta):
        self._no_slip_boundary_conditions.update_boundary(boundary_condition_delta)

    def update_constant_velocity_boundary(self, boundary_condition_delta: BoundaryConditionConstantVelocityDelta):
        self._constant_velocity_boundary_conditions.update_boundary(boundary_condition_delta)

    def update_initial_boundary(self, boundary_condition_delta: BoundaryConditionInitialDelta):
        self._fluid_state.update_fluid_initial_state(boundary_condition_delta)

    def prepare_boundary_conditions(self):
        self._no_slip_boundary_conditions.remove_fluid_from_boundary(self._fluid_state)
        self._constant_velocity_boundary_conditions.remove_fluid_from_boundary(self._fluid_state)

    def simulation_step(self):
        density_state = FluidDensityState.from_boltzmann_state(self._fluid_state)
        velocity_state = FluidVelocityState.from_boltzmann_state(self._fluid_state, density_state,
                                                                 self._simulation_params)
        equilibrium_state = EquilibriumFluidState.from_velocities_and_densities(density_state, velocity_state,
                                                                                self._equilibrium_weights,
                                                                                self._directions,
                                                                                self._simulation_params)
        relaxed_state = RelaxedBoltzmannFluidState(self._fluid_state, equilibrium_state, self._simulation_params)
        self._fluid_state = relaxed_state.to_next_boltzmann_state()

        print("Koniec", self._fluid_state.fluid_state.sum())

        self._no_slip_boundary_conditions.process_fluid_state(self._fluid_state)
        # self._constant_velocity_boundary_conditions.process_fluid_state(self._fluid_state)
