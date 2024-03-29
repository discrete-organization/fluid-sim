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
        self._simulation_args = simulation_args
        self._draw_size_resized = self._get_output_dimensions((draw_size[0], draw_size[1]))
        self._output_writer = cv2.VideoWriter(simulation_args.output_path,
                                              cv2.VideoWriter_fourcc(*'mp4v'), 24,
                                              self._draw_size_resized, True)
        self._legend_fond = pygame.font.SysFont("monospace", 15)

    def render_fluid(self, fluid: BoltzmannFluid, z: int) -> None:
        fluid_density_state: FluidDensityState = FluidDensityState.from_boltzmann_state(fluid._fluid_state)
        self._density_matrix = fluid_density_state.density_state
        fluid_velocity_state = FluidVelocityState.from_boltzmann_state(fluid._fluid_state, fluid_density_state,
                                                                       fluid._simulation_params)
        self._velocity_matrix = fluid_velocity_state.velocity_state

        self._not_no_slip_boundaries_mask = np.repeat(1 - fluid._no_slip_boundary_conditions.affected_cells, 3, axis=-1)\
            .astype(np.uint8)
        self._not_constant_velocity_boundaries_mask = np.repeat(1 - fluid._constant_velocity_boundary_conditions.affected_cells,
                                                                3, axis=-1).astype(np.uint8)
        self._density_matrix = self._density_matrix[:, :, z]
        self._velocity_matrix = self._velocity_matrix[:, :, z, :]

        if self._simulation_args.use_density:
            self._draw_density()
        else:
            self._draw_velocity()

    def _draw_density(self) -> None:
        max_density = np.max(self._density_matrix)
        min_density = np.min(self._density_matrix)
        
        mapped_density = (self._density_matrix - min_density) / (max_density - min_density) * 255 \
            if max_density != min_density else np.zeros_like(self._density_matrix)

        rgb_colors_matrix = np.repeat(mapped_density[..., np.newaxis], 3, axis=-1).astype(np.uint8)
        rgb_colors_matrix = self._apply_boundaries_masks(rgb_colors_matrix)

        self._draw_surface_from_matrix(rgb_colors_matrix)
        render_window = self._draw_density_legend(min_density, max_density)
        self._save_frame(rgb_colors_matrix, render_window)

    def _draw_velocity(self) -> None:
        speeds_matrix = np.linalg.norm(self._velocity_matrix, axis=-1)
        max_speed = np.max(speeds_matrix)
        min_speed = np.min(speeds_matrix)

        normalized_velocity_matrix = self._velocity_matrix / max_speed \
            if max_speed != 0 else np.zeros_like(self._velocity_matrix)

        hsv_colors_matrix = np.zeros(speeds_matrix.shape + (3,))

        hsv_colors_matrix[..., 0] = (np.arctan2(normalized_velocity_matrix[..., 1], normalized_velocity_matrix[..., 0])
                                     + np.pi) / (2 * np.pi)
        hsv_colors_matrix[..., 1] = np.ones_like(speeds_matrix)
        hsv_colors_matrix[..., 2] = (speeds_matrix - min_speed) / (max_speed - min_speed) \
            if max_speed != min_speed else np.zeros_like(speeds_matrix)

        rgb_colors_matrix = (colors.hsv_to_rgb(hsv_colors_matrix) * 255).astype(np.uint8)
        rgb_colors_matrix = self._apply_boundaries_masks(rgb_colors_matrix)

        self._draw_surface_from_matrix(rgb_colors_matrix)
        render_window = self._draw_velocity_legend(min_speed, max_speed)
        self._save_frame(rgb_colors_matrix, render_window)

    def _draw_density_legend(self, min_density_value: float, max_density_value: float) -> np.ndarray:
        info = pygame.display.Info()
        legend_width, legend_height = 50, 200
        legend_padding = 20
        texts_count = 10
        legend_position = (info.current_w - legend_width - legend_padding, legend_padding)

        current_x, current_y = self._window.get_size() if self._simulation_args.draw_on_screen \
            else self._draw_size_resized
        render_window = np.zeros((current_x, current_y, 3), dtype=np.uint8)

        texture_vector = np.arange(0.0, 255.0, 255.0 / legend_height)
        texture_matrix = np.repeat(texture_vector[:, np.newaxis], legend_width, axis=-1).T
        texture_matrix_rgb = np.repeat(texture_matrix[..., np.newaxis], 3, axis=-1).astype(np.uint8)

        border_color = [0, 0, 0]
        texture_matrix_rgb[0, :, :] = border_color
        texture_matrix_rgb[-1, :, :] = border_color
        texture_matrix_rgb[:, 0, :] = border_color
        texture_matrix_rgb[:, -1, :] = border_color

        texture_surface = pygame.surfarray.make_surface(texture_matrix_rgb)

        text_distance_pixels = legend_height // texts_count
        text_distance_values = (max_density_value - min_density_value) / texts_count
        text_values = np.arange(min_density_value, max_density_value + text_distance_values, text_distance_values)
        text_y_positions = np.arange(legend_padding, legend_height + legend_padding + text_distance_pixels,
                                     text_distance_pixels)

        render_window_swapped = np.swapaxes(render_window, 0, 1).copy()

        for text_value, text_y_position in zip(text_values, text_y_positions):
            text = self._legend_fond.render(f"{text_value:.2f}", True, pygame.Color("blue"))
            text_y_position_centered = text_y_position - text.get_height() // 2

            x_position = legend_position[0] - text.get_width() - legend_padding
            y_position = text_y_position_centered

            if self._simulation_args.draw_on_screen:
                self._window.blit(text, (x_position, y_position))
            render_window_swapped = cv2.putText(render_window_swapped, f"{text_value:.2f}", (x_position, text_y_position),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

        render_window = np.swapaxes(render_window_swapped, 0, 1)

        if self._simulation_args.draw_on_screen:
            self._window.blit(texture_surface, legend_position)

        start_x, start_y = legend_position[0], legend_position[1]
        end_x, end_y = legend_position[0] + legend_width, legend_position[1] + legend_height

        render_window[start_x:end_x, start_y:end_y, :] = texture_matrix_rgb

        return render_window

    def _draw_velocity_legend(self, min_speed_value: float, max_speed_value: float) -> np.ndarray:
        info = pygame.display.Info()
        legend_width, legend_height = 300, 200
        legend_padding = 20
        texts_count_val = 10
        texts_counts_direction = 7

        current_x, current_y = self._window.get_size() if self._simulation_args.draw_on_screen \
            else self._draw_size_resized
        render_window = np.zeros((current_x, current_y, 3), dtype=np.uint8)

        legend_position = (info.current_w - legend_width - legend_padding, legend_padding)

        vector_value_step = 1.0 / legend_height
        vector_direction_step = 1.0 / legend_width

        texture_vector_value = np.arange(0.0, 1.0, vector_value_step)
        texture_vector_direction = np.arange(0.0, 1.0, vector_direction_step)

        texture_matrix_value = np.repeat(texture_vector_value[:, np.newaxis], legend_width, axis=-1).T
        texture_matrix_direction = np.repeat(texture_vector_direction[:, np.newaxis], legend_height, axis=-1)

        texture_matrix_hsv = np.zeros((legend_width, legend_height, 3))
        texture_matrix_hsv[..., 0] = texture_matrix_direction
        texture_matrix_hsv[..., 1] = 1.0
        texture_matrix_hsv[..., 2] = texture_matrix_value

        texture_matrix_rgb = (colors.hsv_to_rgb(texture_matrix_hsv) * 255).astype(np.uint8)

        border_color = [0, 0, 0]
        texture_matrix_rgb[0, :, :] = border_color
        texture_matrix_rgb[-1, :, :] = border_color
        texture_matrix_rgb[:, 0, :] = border_color
        texture_matrix_rgb[:, -1, :] = border_color

        texture_surface = pygame.surfarray.make_surface(texture_matrix_rgb)

        text_distance_pixels = legend_height // texts_count_val
        text_distance_values = (max_speed_value - min_speed_value) / texts_count_val

        text_values = np.arange(min_speed_value, max_speed_value + text_distance_values, text_distance_values)
        text_values_y_positions = np.arange(legend_padding, legend_height + legend_padding + text_distance_pixels,
                                            text_distance_pixels)

        text_directions_distance_values = 2 * np.pi / texts_counts_direction
        text_directions_distance_pixels = legend_width // texts_counts_direction

        text_directions = np.arange(0.0, 2 * np.pi + text_directions_distance_values, text_directions_distance_values)
        text_directions_x_positions = np.arange(legend_position[0], legend_position[0] + legend_width +
                                                + text_directions_distance_pixels,
                                                text_directions_distance_pixels)

        render_window_swapped = np.swapaxes(render_window, 0, 1).copy()

        for text_value, text_y_position in zip(text_values, text_values_y_positions):
            text = self._legend_fond.render(f"{text_value:.2f}", True, pygame.Color("blue"))
            text_y_position_centered = text_y_position - text.get_height() // 2

            position_x = legend_position[0] - text.get_width() - legend_padding
            position_y = text_y_position_centered

            if self._simulation_args.draw_on_screen:
                self._window.blit(text, (position_x, position_y))
            render_window_swapped = cv2.putText(render_window_swapped, f"{text_value:.2f}", (position_x, text_y_position),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        for text_direction, text_x_position in zip(text_directions, text_directions_x_positions):
            text = self._legend_fond.render(f"{text_direction:.2f}", True, pygame.Color("blue"))
            text_x_position_centered = text_x_position - text.get_width() // 2

            position_x = text_x_position_centered
            position_y = legend_position[1] + legend_height + legend_padding

            if self._simulation_args.draw_on_screen:
                self._window.blit(text, (position_x, position_y))
            render_window_swapped = cv2.putText(render_window_swapped, f"{text_direction:.2f}",
                                                (text_x_position, position_y),
                                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        render_window = np.swapaxes(render_window_swapped, 0, 1)

        if self._simulation_args.draw_on_screen:
            self._window.blit(texture_surface, legend_position)

        start_x, start_y = legend_position[0], legend_position[1]
        end_x, end_y = legend_position[0] + legend_width, legend_position[1] + legend_height

        render_window[start_x:end_x, start_y:end_y, :] = texture_matrix_rgb

        return render_window

    def _apply_boundaries_masks(self, matrix: np.ndarray) -> np.ndarray:
        return matrix
        return matrix * self._not_no_slip_boundaries_mask \
            * self._not_constant_velocity_boundaries_mask

    def _draw_surface_from_matrix(self, matrix: np.ndarray[np.ndarray[np.ndarray[np.uint8]]]) -> None:
        if not self._simulation_args.draw_on_screen:
            return

        surface = pygame.surfarray.make_surface(matrix)
        self._draw_surface(surface)

    def _get_scale_quotient(self) -> float:
        current_x, current_y = self._window.get_size()
        desired_x, desired_y = self._constants.WIN_W, self._constants.WIN_H

        quotient_x, quotient_y = desired_x / current_x, desired_y / current_y
        scale_quotient = min(quotient_x, quotient_y)

        return scale_quotient

    def _draw_surface(self, surface: pygame.SurfaceType) -> None:
        current_x, current_y = self._window.get_size()
        scale_quotient = self._get_scale_quotient()

        scaled_x, scaled_y = int(current_x * scale_quotient), int(current_y * scale_quotient)
        scaled_surface = pygame.transform.scale(surface, (scaled_x, scaled_y))
        
        self._window.blit(scaled_surface, (0, 0))

    @staticmethod
    def _get_output_dimensions(previous_draw_size: tuple[int, int]) -> tuple[int, int]:
        target_min_dimension = 800

        target_shape = previous_draw_size
        min_dimension = min(target_shape)

        if min_dimension < target_min_dimension:
            scale_quotient = target_min_dimension / min_dimension
            target_shape = tuple(int(dimension * scale_quotient) for dimension in target_shape)

        return target_shape

    @staticmethod
    def _merge_frame_with_legend(frame: np.ndarray, legend_render_window: np.ndarray) -> np.ndarray:
        target_shape = FluidRenderer._get_output_dimensions((frame.shape[0], frame.shape[1]))

        frame_resized = cv2.resize(frame, target_shape[::-1], interpolation=cv2.INTER_CUBIC)
        legend_render_window_resized = cv2.resize(legend_render_window, target_shape[::-1],
                                                  interpolation=cv2.INTER_CUBIC)
        legend_mask = legend_render_window_resized > 0

        frame_resized[legend_mask] = legend_render_window_resized[legend_mask]

        return frame_resized

    def _save_frame(self, frame: np.ndarray, legend_render_window: np.ndarray) -> None:
        frame_merged = self._merge_frame_with_legend(frame, legend_render_window)

        frame_bgr = cv2.cvtColor(frame_merged, cv2.COLOR_RGB2BGR)
        frame_bgr_flipped = np.swapaxes(frame_bgr, 0, 1)
        self._output_writer.write(frame_bgr_flipped)

    def save_video(self) -> None:
        self._output_writer.release()
        print("Video saved")
