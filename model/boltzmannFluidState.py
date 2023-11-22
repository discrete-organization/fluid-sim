import numpy as np


class BoltzmannFluidState:
    def __init__(self, shape):
        self.fluid_state: np.array = np.zeros(shape + (19,))

