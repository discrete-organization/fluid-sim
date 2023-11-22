import json
from typing import Generator
from utilities.DTO.D3Q19 import D3Q19ParticleFunction
from utilities.DTO.vector3 import Vector3Int, Vector3Float
from utilities.DTO.boundaryConditionDTO import (
    BoundaryConditionConstantVelocity,
    BoundaryConditionInitial,
    BoundaryCube,
    BoundaryConditionDelta,
    BoundaryConditionNoSlip,
)


class BoundaryConditionsReader:
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

            cube_start_position = Vector3Int(
                cube_json["x"], cube_json["y"], cube_json["z"]
            )
            cube_end_position = cube_start_position + Vector3Int(
                cube_json["width"], cube_json["height"], cube_json["depth"]
            )

            boundary_cube = BoundaryCube(cube_start_position, cube_end_position)

            match boundary_condition["boundary_type"]:
                case "no-slip":
                    yield BoundaryConditionNoSlip(boundary_cube)
                case "constant-velocity":
                    velocity_json = data_json["velocity"]

                    yield BoundaryConditionConstantVelocity(
                        boundary_cube,
                        Vector3Float(velocity_json["x"], velocity_json["y"], velocity_json["z"]),
                    )
                case "initial":
                    yield BoundaryConditionInitial(
                        boundary_cube, D3Q19ParticleFunction(data_json["boltzmann_f19"])
                    )
                case _:
                    raise ValueError("Invalid boundary condition type.")
