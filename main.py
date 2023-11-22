from simulation.simulator import Simulator
from utilities.boundaryConditionsReader import BoundaryConditionsReader


if __name__ == "__main__":
    simulator = Simulator()
    simulator.run()

    br = BoundaryConditionsReader("input/BoundaryConditions.json")

    for x in br.boundary_conditions():
        print(x)
