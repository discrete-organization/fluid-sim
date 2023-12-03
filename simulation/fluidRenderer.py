import numpy as np
import pygame
from model.boltzmannFluid import BoltzmannFluid


class FluidRenderer:
    def render_fluid(self, fluid: BoltzmannFluid) -> None:
        # take velocity matrix from BoltzmanFluidState
        # matrix of velocities = [x, y, z, (v_x, v_y, v_z)]
        # change matrix to transection matrix - set constant z
        # for each cell in transection matrix
        #   calculate color based on velocity
        #   draw rectangle with color
        
        self._velocity_matrix: np.array = fluid._fluid_state.fluid_state
        helf_depth_ = self._velocity_matrix.shape[2] // 2
        self._velocity_matrix = self._velocity_matrix[:, :, helf_depth_, :]
        
        for i in range(self._velocity_matrix.shape[0]):
            for j in range(self._velocity_matrix.shape[1]):
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
        # calculate the position and size of the rectangle
        x = i * cell_size
        y = j * cell_size
        rect = pygame.Rect(x, y, cell_size, cell_size)
        # pygame.draw.rect(win, color, rect)