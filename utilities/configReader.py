import json
from typing import Generator
from utilities.DTO.vector3 import Vector3Int
from utilities.DTO.boundaryConditionDTO import BoundaryConditionConstantVelocity, BoundaryConditionInitial, BoundaryCube, BoundaryConditionDelta


class BoundaryConditionsReader:
    def __init__(self, file_path: str) -> None:
        try:
            with open(file_path, "r") as file:
                self.json_content = json.load(file)

        except FileNotFoundError:
            print("File not found. Please provide a valid file path.")
        except KeyError:
            print("Invalid JSON format. Make sure your JSON file contains proper fields.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")


    def boundaryConditions(self) -> Generator[BoundaryConditionDelta, None, None]:
        for boundary_condition in self.json_content["boundaries"]:
            match boundary_condition["boundary_type"]:
                case "no-slip":
                    yield BoundaryConditionDelta(
                        boundary_cube=BoundaryCube(
                            start_position=Vector3Int(boundary_condition["start_position"]),
                            end_position=Vector3Int(boundary_condition["end_position"])
                        )
                    )
                case "constant-velocity":
                    yield BoundaryConditionConstantVelocity(
                        boundary_cube=BoundaryCube(
                            start_position=Vector3Int(boundary_condition["start_position"]),
                            end_position=Vector3Int(boundary_condition["end_position"])
                        ),
                        velocity=Vector3Int(boundary_condition["velocity"])
                    )
                case "initial":
                    yield BoundaryConditionInitial(
                        boundary_cube=BoundaryCube(
                            start_position=Vector3Int(boundary_condition["start_position"]),
                            end_position=Vector3Int(boundary_condition["end_position"])
                        ),
                        function=boundary_condition["function"]
                    )
                case _:
                    raise ValueError("Invalid boundary condition type.")
            
        
