import json
import numpy as np
from typing import Generator
from utilities.DTO.D3Q19 import D3Q19ParticleFunction
from utilities.DTO.vector3 import Vector3Int, Vector3Float
from utilities.DTO.boundaryConditionDTO import (
    BoundaryConditionConstantVelocityDelta,
    BoundaryConditionInitialDelta,
    BoundaryCube,
    BoundaryConditionDelta,
    BoundaryConditionNoSlipDelta,
)
from utilities.DTO.simulationParameters import SimulationParameters


class ModelConfigReader:
    def __init__(self, file_path: str) -> None:
        try:
            with open(file_path, "r") as file:
                self._json_content = json.load(file)

        except FileNotFoundError:
            print("File not found. Please provide a valid file path.")
        except KeyError:
            print(
                "Invalid JSON format. Make sure your JSON file contains proper fields."
            )
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def boundary_conditions(self) -> Generator[BoundaryConditionDelta, None, None]:
        for boundary_condition in self._json_content["boundaries"]:
            cube_json = boundary_condition["cube"]
            data_json = boundary_condition["data"]

            cube_start_position = Vector3Int(cube_json["x"], cube_json["y"], cube_json["z"])
            cube_end_position = cube_start_position + Vector3Int(cube_json["width"], cube_json["height"], cube_json["depth"])

            boundary_cube = BoundaryCube(cube_start_position, cube_end_position)

            match boundary_condition["boundary_type"]:
                case "no-slip":
                    yield BoundaryConditionNoSlipDelta(boundary_cube)
                case "constant-velocity":
                    velocity_json = data_json["velocity"]

                    yield BoundaryConditionConstantVelocityDelta(
                        boundary_cube,
                        Vector3Float(velocity_json["x"], velocity_json["y"], velocity_json["z"]),
                    )
                case "initial":
                    yield BoundaryConditionInitialDelta(
                        boundary_cube, D3Q19ParticleFunction(data_json["boltzmann_f19"])
                    )
                case _:
                    raise ValueError("Invalid boundary condition type.")

    def lattice_dimensions(self) -> Vector3Int:
        box_config_json = self._json_content["fluid_box"]
        width = np.int32(box_config_json["width"])
        height = np.int32(box_config_json["height"])
        depth = np.int32(box_config_json["depth"])

        return Vector3Int(width, height, depth)

    def simulation_parameters(self) -> SimulationParameters:
        box_config_json = self._json_content["fluid_box"]
        viscosity = float(box_config_json["viscosity"])
        time_delta = float(box_config_json["time_delta"])
        cell_length = float(box_config_json["cell_length"])

        relaxation_time = (time_delta / cell_length ** 2 * 6 * viscosity + 1) / 2
        print(f"Relaxation time: {relaxation_time}")

        # TODO: check this calculation @Rafał
        speed_of_sound = cell_length / time_delta * 3 ** 0.5

        return SimulationParameters(viscosity, time_delta, cell_length, speed_of_sound, relaxation_time)
