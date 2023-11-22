import numpy as np
from dataclasses import dataclass

@dataclass
class D3Q19ParticleFunction:
    vectors: np.array

    def __init__(self, vectors: list[float]) -> None:
        self.vectors = np.array(vectors)

    def __post_init__(self):
        self.vectors = np.array(self.vectors)

        if self.vectors.shape != (19, 3):
            raise ValueError("vectors must be a 19x3 matrix.")
        
        if self.vectors.dtype != np.int64:
            raise ValueError("vectors must be of type int64.")
        
    def __len__(self):
        return self.vectors.__len__()
    
    def __str__(self):
        return f"D3Q19({self.vectors})"
    
    def __getitem__(self, key):
        return self.vectors[key]
    
    def __setitem__(self, key, value):
        self.vectors[key] = value

    def __iter__(self):
        return self.vectors.__iter__()
    
    def __next__(self):
        return self.vectors.__next__()
    
    
