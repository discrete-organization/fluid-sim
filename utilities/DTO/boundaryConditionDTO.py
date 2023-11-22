from dataclasses import dataclass
from utilities.DTO.D3Q19 import D3Q19ParticleFunction
from utilities.DTO.vector3 import Vector3Int, Vector3Float


@dataclass
class BoundaryCube:
    start_position: Vector3Int
    end_position: Vector3Int


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
