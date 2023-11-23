import numpy as np
from utilities.DTO.boundaryConditionDTO import BoundaryConditionInitialDelta


class BoltzmannFluidState:
    def __init__(self, shape, allowed_velocities: np.ndarray[np.float64]):
        # Make sure that the allowed velocities have correct lengths (c e)
        self.fluid_state: np.array = np.zeros(shape + (19,))
        self.allowed_velocities = allowed_velocities

    def update_fluid_initial_state(self, fluid_initial_delta: BoundaryConditionInitialDelta) -> None:
        x1, y1, z1 = fluid_initial_delta.boundary_cube.start_position.to_tuple()
        x2, y2, z2 = fluid_initial_delta.boundary_cube.end_position.to_tuple()
        self.fluid_state[x1:x2, y1:y2, z1:z2] = fluid_initial_delta.boltzmann_f19.vectors


class FluidDensityState:
    def __init__(self, density_state: np.ndarray[np.float64]) -> None:
        self.density_state = density_state

    @staticmethod
    def from_boltzmann_state(boltzmann_state: BoltzmannFluidState) -> 'FluidDensityState':
        return FluidDensityState(np.sum(boltzmann_state.fluid_state, axis=-1))


class FluidVelocityState:
    def __init__(self, velocity_state: np.ndarray[np.ndarray[np.float64]]) -> None:
        self.velocity_state = velocity_state

    @staticmethod
    def from_boltzmann_state(boltzmann_state: BoltzmannFluidState, density_state: FluidDensityState)\
            -> 'FluidVelocityState':
        allowed_velocities = boltzmann_state.allowed_velocities
        fluid_state = boltzmann_state.fluid_state

        '''
            Allowed velocities are of shape (19, 3)
            Fluid state is of shape (w_x, w_y, w_z, 19)
            
            The result should be of shape (w_x, w_y, w_z, 3)
            
            We can achieve this by using np.einsum:
            Let v to be the last axis of the fluid state (it specifies the amount of fluid flowing in a direction),
            and let w to be the last axis of the allowed velocities (it specifies the direction of the fluid flow).
            
            Then, we can write the following:
            ijkv, vw -> ijkw
            
            So we for each cell (at position ijk), we multiply the amount of fluid flowing in a direction (v) with the
            direction of the fluid flow (w) in that direction.
        '''
        velocities = np.einsum("ijkv,vw->ijkw", fluid_state, allowed_velocities)
        # TODO: Verify that this is correct @Rafał

        return FluidVelocityState(velocities) / np.nan_to_num(density_state.density_state, nan=1.0)[..., np.newaxis]
