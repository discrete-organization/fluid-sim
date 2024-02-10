import unittest
import numpy as np
from model.boltzmannFluidUtils import BoltzmannFluidState, FluidDensityState, FluidVelocityState
from utilities.DTO.boundaryConditionDTO import BoundaryConditionInitialDelta
from utilities.DTO.simulationParameters import SimulationParameters


class TestFluidVelocityState(unittest.TestCase):
    def test_from_boltzmann_state(self):
        # mock objects
        boltzmann_state = BoltzmannFluidState(...)
        density_state = FluidDensityState(...)
        simulation_config = SimulationParameters(...)

        # Call the method under test
        fluid_velocity_state = FluidVelocityState.from_boltzmann_state(
            boltzmann_state, density_state, simulation_config
        )


        self.assertIsInstance(fluid_velocity_state, FluidVelocityState)
        self.assertEqual(fluid_velocity_state.velocity_state.shape, (10, 10, 10, 3))



if __name__ == "__main__":
    unittest.main()
