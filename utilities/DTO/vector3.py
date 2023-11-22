import numpy as np


class Vector3Int:
    vector: np.ndarray[np.int32]

    @staticmethod
    def _check_vector(vector):
        if vector.shape != (3,):
            raise ValueError(f"vector must be a 3D vector, but is {vector.shape}")

        if vector.dtype != np.int32:
            raise ValueError(f"vector must be of type int64, but is {vector.dtype}")

    def __init__(self, x: int, y: int, z: int) -> None:
        self.vector = np.array([x, y, z])
        Vector3Int._check_vector(self.vector)

    @staticmethod
    def from_numpy(vector: np.ndarray[np.int32]):
        Vector3Int._check_vector(vector)
        x, y, z = vector

        return Vector3Int(x, y, z)
        
    def __add__(self, other):
        return Vector3Int.from_numpy(self.vector + other.vector)
    
    def __sub__(self, other):
        return Vector3Int.from_numpy(self.vector - other.vector)
    
    def __mul__(self, other):
        return Vector3Int.from_numpy(self.vector * other)
    
    def __floordiv__(self, other):
        return Vector3Int.from_numpy(self.vector // other)
    
    def __str__(self):
        return f"Vector3({self.vector})"

    def get_x(self) -> int:
        return int(self.vector[0])

    def get_y(self) -> int:
        return int(self.vector[1])

    def get_z(self) -> int:
        return int(self.vector[2])


class Vector3Float:
    vector: np.ndarray[np.float64]

    @staticmethod
    def _check_vector(vector):
        if vector.shape != (3,):
            raise ValueError(f"vector must be a 3D vector, but is {vector.shape}")

        if vector.dtype != np.float64:
            raise ValueError(f"vector must be of type int64, but is {vector.dtype}")

    def __init__(self, x: int, y: int, z: int) -> None:
        self.vector = np.array([x, y, z])
        Vector3Float._check_vector(self.vector)

    @staticmethod
    def from_numpy(vector: np.ndarray[np.float64]):
        Vector3Float._check_vector(vector)
        x, y, z = vector

        return Vector3Float(x, y, z)

    def __add__(self, other):
        return Vector3Int.from_numpy(self.vector + other.vector)

    def __sub__(self, other):
        return Vector3Int.from_numpy(self.vector - other.vector)

    def __mul__(self, other):
        return Vector3Int.from_numpy(self.vector * other)

    def __truediv__(self, other):
        return Vector3Int.from_numpy(self.vector / other)

    def __floordiv__(self, other):
        return Vector3Int.from_numpy(self.vector // other)

    def __str__(self):
        return f"Vector3({self.vector})"

    def get_x(self) -> float:
        return float(self.vector[0])

    def get_y(self) -> float:
        return float(self.vector[1])

    def get_z(self) -> float:
        return float(self.vector[2])
