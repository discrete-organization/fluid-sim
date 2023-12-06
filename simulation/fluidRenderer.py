import numpy as np
import pygame
import cv2
from typing import Tuple
from matplotlib import colors
from model.boltzmannFluidUtils import FluidDensityState, FluidVelocityState
from model.boltzmannFluid import BoltzmannFluid
from .windowDTO import WindowProperties
from utilities.argsReader import SimulationArgs


class FluidRenderer:
    def __init__(self, window: pygame.Surface, constants: WindowProperties,
                 simulation_args: SimulationArgs, draw_size: Tuple[int, int, int]) -> None:
        self._window = window
        self._constants = constants
        self._draw_size = draw_size
        self._simulation_args = simulation_args
        self._output_writer = cv2.VideoWriter(simulation_args.output_path,
                                              cv2.VideoWriter_fourcc(*'mp4v'), 24,
                                              draw_size[:2], True)

    def render_fluid(self, fluid: BoltzmannFluid) -> None:
        fluid_density_state: FluidDensityState = FluidDensityState.from_boltzmann_state(fluid._fluid_state)
        self._density_matrix = fluid_density_state.density_state
        fluid_velocity_state = FluidVelocityState.from_boltzmann_state(fluid._fluid_state, fluid_density_state,
                                                                       fluid._simulation_params)
        self._velocity_matrix = fluid_velocity_state.velocity_state
        
        # TODO Create adjustable transection, modifiable with slider
        chosen_z = self._velocity_matrix.shape[2] // 2
        self._density_matrix = self._density_matrix[:, :, chosen_z]
        self._velocity_matrix = self._velocity_matrix[:, :, chosen_z, :]

        if self._simulation_args.use_density:
            self._draw_density()
        else:
            self._draw_velocity()

    def _draw_density(self):
        max_density = np.max(self._density_matrix)
        min_density = np.min(self._density_matrix)
        
        mapped_density = (self._density_matrix - min_density) / (max_density - min_density) * 255 \
            if max_density != min_density else np.zeros_like(self._density_matrix)

        rgb_colors_matrix = np.repeat(mapped_density[..., np.newaxis], 3, axis=-1).astype(np.uint8)

        self._draw_surface_from_matrix(rgb_colors_matrix)
        self._save_frame(rgb_colors_matrix)

    def _draw_velocity(self):
        speeds_matrix = np.linalg.norm(self._velocity_matrix, axis=-1)
        max_speed = np.max(speeds_matrix)
        min_speed = np.min(speeds_matrix)

        normalized_velocity_matrix = self._velocity_matrix / max_speed \
            if max_speed != 0 else np.zeros_like(self._velocity_matrix)

        hsv_colors_matrix = np.zeros(speeds_matrix.shape + (3,))

        hsv_colors_matrix[..., 0] = (np.arctan2(normalized_velocity_matrix[..., 1], normalized_velocity_matrix[..., 0]) + np.pi) \
            / (2 * np.pi)
        hsv_colors_matrix[..., 1] = np.ones_like(speeds_matrix)
        hsv_colors_matrix[..., 2] = (speeds_matrix - min_speed) / (max_speed - min_speed) \
            if max_speed != min_speed else np.zeros_like(speeds_matrix)

        rgb_colors_matrix = (colors.hsv_to_rgb(hsv_colors_matrix) * 255).astype(np.uint8)

        self._draw_surface_from_matrix(rgb_colors_matrix)
        self._save_frame(rgb_colors_matrix)

    def _draw_surface_from_matrix(self, matrix: np.ndarray[np.ndarray[np.ndarray[np.uint8]]]) -> None:
        if not self._simulation_args.draw_on_screen:
            return

        surface = pygame.surfarray.make_surface(matrix)
        self._draw_surface(surface)
    
    def _draw_surface(self, surface: pygame.SurfaceType) -> None:
        current_x, current_y = self._window.get_size()
        desired_x, desired_y = self._constants.WIN_W, self._constants.WIN_H

        quotient_x, quotient_y = desired_x / current_x, desired_y / current_y
        scale_quotient = min(quotient_x, quotient_y)

        scaled_x, scaled_y = int(current_x * scale_quotient), int(current_y * scale_quotient)
        scaled_surface = pygame.transform.scale(surface, (scaled_x, scaled_y))

        self._window.blit(scaled_surface, (0, 0))

    def _save_frame(self, frame: np.ndarray) -> None:
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frame_bgr_flipped = np.swapaxes(frame_bgr, 0, 1)
        self._output_writer.write(frame_bgr_flipped)

    def save_video(self):
        self._output_writer.release()
        print("Video saved")
