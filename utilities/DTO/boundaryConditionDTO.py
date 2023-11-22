from dataclasses import dataclass
from utilities.DTO.D3Q19 import D3Q19ParticleFunction
from utilities.DTO.vector3 import Vector3Int, Vector3Float


@dataclass
class BoundaryCube:
    start_position: Vector3Int
    end_position: Vector3Int

    def __post_init__(self):
        if self.start_position.get_x() > self.end_position.get_x():
            raise ValueError("start_position.x must be smaller than end_position.x.")

        if self.start_position.get_y() > self.end_position.get_y():
            raise ValueError("start_position.y must be smaller than end_position.y.")

        if self.start_position.get_z() > self.end_position.get_z():
            raise ValueError("start_position.z must be smaller than end_position.z.")

    def __str__(self):
        return f"BoundaryCube({self.start_position}, {self.end_position})"

    def __contains__(self, vector: Vector3Int):
        return self.start_position.get_x() <= vector.get_x() <= self.end_position.get_x() and \
               self.start_position.get_y() <= vector.get_y() <= self.end_position.get_y() and \
               self.start_position.get_z() <= vector.get_z() <= self.end_position.get_z()


@dataclass
class BoundaryConditionDelta:
    boundary_cube: BoundaryCube


@dataclass
class BoundaryConditionNoSlip(BoundaryConditionDelta):
    pass


@dataclass
class BoundaryConditionConstantVelocity(BoundaryConditionDelta):
    velocity: Vector3Float


@dataclass
class BoundaryConditionInitial(BoundaryConditionDelta):
    boltzmann_f19: D3Q19ParticleFunction
