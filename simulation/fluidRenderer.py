import numpy as np
import pygame
from model.boltzmannFluidUtils import FluidDensityState, FluidVelocityState
from model.boltzmannFluid import BoltzmannFluid
from .windowDTO import WindowProperties


class FluidRenderer:
    def __init__(self, window: pygame.Surface, constants: WindowProperties) -> None:
        self._window = window
        self._constants = constants

    def render_fluid(self, fluid: BoltzmannFluid) -> None:
        self._constants = WindowProperties()
  
        fluid_density_state: FluidDensityState = FluidDensityState.from_boltzmann_state(fluid._fluid_state)
        self._density_matrix = fluid_density_state.density_state
        fluid_velocity_state = FluidVelocityState.from_boltzmann_state(fluid._fluid_state, fluid_density_state)
        self._velocity_matrix = fluid_velocity_state.velocity_state
        
        # TODO Create adjustable transection, modifiable with slider
        chosen_z = self._velocity_matrix.shape[2] // 2
        self._density_matrix = self._density_matrix[:, :, chosen_z]
        self._velocity_matrix = self._velocity_matrix[:, :, chosen_z, :]
        
        for i in range(self._density_matrix.shape[0]):
            for j in range(self._density_matrix.shape[1]):
                self._draw_cell(i, j)

    def _draw_cell(self, i: int, j: int) -> None:
        velocity_vector = self._velocity_matrix[i, j, :]
        velocity_vector = velocity_vector / np.linalg.norm(velocity_vector)
        self._draw_rectangle(i, j, self._calculate_color(velocity_vector))

    def _calculate_color(self, velocity_vector: np.array) -> np.array:
        return (velocity_vector + 1) * 128

    def _draw_rectangle(self, i: int, j: int, color) -> None:
        cell_size = self._constants.WIN_W // self._velocity_matrix.shape[0]
        x = i * cell_size
        y = j * cell_size
        rect = pygame.Rect(x, y, cell_size, cell_size)
        pygame.draw.rect(self._window, color, rect)