from abc import ABC
from dataclasses import dataclass
import numpy as np
from utilities.DTO.D3Q19 import D3Q19ParticleFunction
from utilities.DTO.vector3 import Vector3Int


@dataclass
class BoundaryCube:
    start_position: Vector3Int
    end_position: Vector3Int


@dataclass
class BoundaryConditionDelta(ABC):
    boundary_cube: BoundaryCube

    def __new__(cls, *args, **kwargs) -> None: 
        if cls == BoundaryConditionDelta or cls.__bases__[0] == BoundaryConditionDelta: 
            raise TypeError("Cannot instantiate abstract class.") 


@dataclass
class BoundaryConditionNoSlip(BoundaryConditionDelta):
    pass

@dataclass
class BoundaryConditionConstantVelocity(BoundaryConditionDelta):
    velocity: Vector3Int

@dataclass
class BoundaryConditionInitial(BoundaryConditionDelta):
    function: D3Q19ParticleFunction