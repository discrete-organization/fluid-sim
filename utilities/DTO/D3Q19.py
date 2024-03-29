import numpy as np
from dataclasses import dataclass


@dataclass
class D3Q19ParticleFunction:
    vectors: np.array

    def __init__(self, vectors: list[float]) -> None:
        self.vectors = np.array(vectors)

    def __post_init__(self):
        self.vectors = np.array(self.vectors)

        if self.vectors.shape != (19,):
            raise ValueError("vectors must be a 19 sized matrix.")
        
        if self.vectors.dtype != np.float64:
            raise ValueError("vectors must be of type float64.")
        
    def __str__(self):
        return f"D3Q19({self.vectors})"
    
    def __getitem__(self, key):
        return self.vectors[key]

    def __iter__(self):
        return self.vectors.__iter__()
