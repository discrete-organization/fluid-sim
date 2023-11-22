import numpy as np
from dataclasses import dataclass


@dataclass
class Vector3Int:
    vector: np.array

    def __init__(self, x: int, y: int, z: int) -> None:
        self.vector = np.array([x, y, z])

    def __post_init__(self) -> None:
        if self.vector.shape != (3,):
            raise ValueError("vector must be a 3D vector.")
        
        if self.vector.dtype != np.int64:
            raise ValueError("vector must be of type int64.")
        
    def __add__(self, other):
        return Vector3Int(self.vector + other.vector)
    
    def __sub__(self, other):
        return Vector3Int(self.vector - other.vector)
    
    def __mul__(self, other):
        return Vector3Int(self.vector * other)
    
    def __truediv__(self, other):
        return Vector3Int(self.vector / other)
    
    def __str__(self):
        return f"Vector3({self.vector})"