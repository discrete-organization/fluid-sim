import numpy as np
import pygame
from model.boltzmannFluid import BoltzmannFluid
from model.boltzmannFluidState import FluidDensityState, FluidVelocityState
from simulation import constantsDTO


class FluidRenderer:
    def __init__(self, window: pygame.Surface, constants: constantsDTO) -> None:
        self._window = window
        self._constants = constants

    def render_fluid(self, fluid: BoltzmannFluid) -> None:
        self._constants = constantsDTO()
        chosen_z = self._velocity_matrix.shape[2] // 2
        # take velocity matrix from BoltzmanFluidState
        # matrix of velocities = [x, y, z, (v_x, v_y, v_z)]
        # change matrix to transection matrix - set constant z
        # for each cell in transection matrix
        #   calculate color based on velocity
        #   draw rectangle with color
        fluid_density_state: FluidDensityState = FluidDensityState.from_boltzmann_state(fluid._fluid_state)
        self._density_matrix = fluid_density_state.density_state
        fluid_velocity_state = FluidVelocityState.from_boltzmann_state(fluid._fluid_state, fluid_density_state)
        self._velocity_matrix = fluid_velocity_state.velocity_state
        
        self._density_matrix = self._density_matrix[:, :, chosen_z]
        self._velocity_matrix = self._velocity_matrix[:, :, chosen_z, :]
        
        
        for i in range(self._density_matrix.shape[0]):
            for j in range(self._density_matrix.shape[1]):
                self._draw_cell(i, j)

    def _draw_cell(self, i: int, j: int) -> None:
        velocity_vector = self._velocity_matrix[i, j, :]
        velocity_vector = velocity_vector / np.linalg.norm(velocity_vector)
        color = self._calculate_color(velocity_vector)
        self._draw_rectangle(i, j, color)

    def _calculate_color(self, velocity_vector: np.array) -> np.array:
        return (velocity_vector + 1) * 128
    

    def _draw_rectangle(self, i, j, color):
        cell_size = 1280 // self._velocity_matrix.shape[0]
        x = i * cell_size
        y = j * cell_size
        rect = pygame.Rect(x, y, cell_size, cell_size)
        # pygame.draw.rect(win, color, rect)