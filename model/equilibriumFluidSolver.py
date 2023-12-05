import numpy as np
from .boltzmannFluidUtils import (
    FluidVelocityState,
    FluidDensityState,
    BoltzmannFluidState
)
from utilities.DTO.simulationParameters import SimulationParameters


class EquilibriumWeights:
    @staticmethod
    def _get_weights() -> np.ndarray[np.float64]:
        return np.array([1 / 3] + [1 / 18] * 6 + [1 / 36] * 12)

    def __init__(self) -> None:
        self.weights = self._get_weights()


class EquilibriumFluidState:
    def __init__(self, equilibrium_state: np.ndarray[np.float64]) -> None:
        self.equilibrium_state = equilibrium_state

    @staticmethod
    def from_velocities_and_densities(density: FluidDensityState, velocity: FluidVelocityState,
                                      equilibrium_weights: EquilibriumWeights,
                                      allowed_velocities: np.ndarray[np.ndarray[np.float64]],
                                      simulation_params: SimulationParameters) -> 'EquilibriumFluidState':
        speed_of_sound = simulation_params.speed_of_sound

        speed_of_sound_squared = speed_of_sound ** 2

        # TODO: Verify that this is correct @Rafał
        u_dot_products = np.einsum("ijkv,ijkv->ijk", velocity.velocity_state, velocity.velocity_state)[:, :, :, np.newaxis]
        u_e_dot_products = np.einsum("ijkw,vw->ijkv", velocity.velocity_state, allowed_velocities)
        u_e_dot_products_squared = u_e_dot_products ** 2

        # TODO: Verify if the components of u_dot will be added correctly @Rafał

        first_element = 1
        second_element = 3 * u_e_dot_products / speed_of_sound
        third_element = 9 * u_e_dot_products_squared / (2 * speed_of_sound_squared)
        fourth_element = -3 * u_dot_products / (2 * speed_of_sound_squared)

        velocity_coefficient = first_element + second_element + third_element + fourth_element

        print(equilibrium_weights.weights)
        velocity_coefficient_weighted = np.einsum("ijkv,v->ijkv",
                                                  velocity_coefficient,
                                                  equilibrium_weights.weights)

        result_field = np.einsum("ijk,ijkv->ijkv", density.density_state, velocity_coefficient_weighted)

        return EquilibriumFluidState(result_field)


class RelaxedBoltzmannFluidState(BoltzmannFluidState):
    @staticmethod
    def _relax_fluid_state(fluid_state: np.ndarray[np.ndarray[np.ndarray[np.float32]]],
                           equilibrium_state: np.ndarray[np.ndarray[np.ndarray[np.float32]]],
                           relaxation_time: float) \
            -> np.ndarray[np.ndarray[np.ndarray[np.float32]]]:

        print("Relaxing")
        print(fluid_state.sum())
        print(equilibrium_state.sum())
        return fluid_state - (fluid_state - equilibrium_state) / relaxation_time

    def __init__(self, fluid_state: BoltzmannFluidState, equilibrium_state: EquilibriumFluidState,
                 simulation_parameters: SimulationParameters) -> None:
        self.fluid_state = self._relax_fluid_state(fluid_state.fluid_state, equilibrium_state.equilibrium_state,
                                                   simulation_parameters.relaxation_time)
        self.allowed_velocities = fluid_state.allowed_velocities

    def to_next_boltzmann_state(self) -> BoltzmannFluidState:
        new_state = np.zeros_like(self.fluid_state)

        for i, dr in enumerate(self.allowed_velocities):
            dx, dy, dz = dr.astype(np.int32) # TODO: Verify that this is correct @Rafał
            new_state[..., i] = np.roll(self.fluid_state[..., i], shift=(dx, dy, dz), axis=(0, 1, 2))

        return BoltzmannFluidState.from_fluid_state(new_state, self.allowed_velocities)
