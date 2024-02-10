import unittest
import numpy as np
from model.equilibriumFluidSolver import EquilibriumFluidState
from model.equilibriumFluidSolver import EquilibriumWeights
from model.boltzmannFluidUtils import (
    FluidVelocityState,
    FluidDensityState,
    BoltzmannFluidState
)
from utilities.DTO.simulationParameters import SimulationParameters

class TestEquilibriumFluidState(unittest.TestCase):
    def test_from_velocities_and_densities(self):
        # dummy input data
        density = FluidDensityState(np.array([1, 2, 3]))
        velocity = FluidVelocityState(
            np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]], [[9, 10], [11, 12]]])
        )
        equilibrium_weights = EquilibriumWeights(np.array([0.1, 0.2, 0.3]))
        allowed_velocities = np.array(
            [
                [[0.1, 0.2], [0.3, 0.4]],
                [[0.5, 0.6], [0.7, 0.8]],
                [[0.9, 1.0], [1.1, 1.2]],
            ]
        )
        simulation_params = SimulationParameters(speed_of_sound=2.0)

        # expected result
        speed_of_sound_squared = simulation_params.speed_of_sound**2
        u_dot_products = np.einsum(
            "ijkv,ijkv->ijk", velocity.velocity_state, velocity.velocity_state
        )[:, :, :, np.newaxis]
        u_e_dot_products = np.einsum(
            "ijkw,vw->ijkv", velocity.velocity_state, allowed_velocities
        )
        u_e_dot_products_squared = u_e_dot_products**2
        velocity_coefficient = (
            1
            + 3 * u_e_dot_products / simulation_params.speed_of_sound
            + 9 * u_e_dot_products_squared / (2 * speed_of_sound_squared)
            - 3 * u_dot_products / (2 * speed_of_sound_squared)
        )
        velocity_coefficient_weighted = np.einsum(
            "ijkv,v->ijkv", velocity_coefficient, equilibrium_weights.weights
        )
        result_field = np.einsum(
            "ijk,ijkv->ijkv", density.density_state, velocity_coefficient_weighted
        )

        # Call the method
        result = EquilibriumFluidState.from_velocities_and_densities(
            density,
            velocity,
            equilibrium_weights,
            allowed_velocities,
            simulation_params,
        )

        np.testing.assert_allclose(result.equilibrium_state, result_field)


if __name__ == "__main__":
    unittest.main()
