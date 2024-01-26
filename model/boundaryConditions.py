import numpy as np
from utilities.DTO.boundaryConditionDTO import (
    BoundaryConditionNoSlipDelta,
    BoundaryConditionConstantVelocityDelta,
    BoundaryCube
)
from .boltzmannFluidUtils import BoltzmannFluidState
from .fluidDirectionProvider import FluidDirectionProvider
from .equilibriumFluidSolver import FluidDensityState


class BoundaryConditions:
    def _update_affected_cells(self, boundary_cube: BoundaryCube) -> None:
        x1, y1, z1 = boundary_cube.start_position.to_tuple()
        x2, y2, z2 = boundary_cube.end_position.to_tuple()

        self.affected_cells[x1:x2, y1:y2, z1:z2] = True

    def __init__(self, shape: tuple[int, int, int], allowed_velocities: np.ndarray[np.ndarray[np.int32]]):
        self.affected_cells = np.zeros(shape, dtype=bool)
        self.allowed_velocities = allowed_velocities
        self.reverse_direction_indeces = FluidDirectionProvider.get_reverse_directions_indices()

    def process_fluid_state(self, _: BoltzmannFluidState) -> None:
        pass

    def remove_fluid_from_boundary(self, fluid_state: BoltzmannFluidState) -> None:
        fluid_state_matrix = fluid_state.fluid_state
        fluid_state_matrix[self.affected_cells, ...] = 0


class NoSlipBoundaryConditions(BoundaryConditions):
    def __init__(self, shape: tuple[int, int, int], allowed_velocities: np.ndarray[np.ndarray[np.int32]]):
        super().__init__(shape, allowed_velocities)

    def update_boundary(self, boundary_condition_delta: BoundaryConditionNoSlipDelta) -> None:
        self._update_affected_cells(boundary_condition_delta.boundary_cube)

    def process_fluid_state(self, fluid_state: BoltzmannFluidState) -> None:
        fluid_state_matrix = fluid_state.fluid_state
        affected_fluid_matrix = fluid_state_matrix * self.affected_cells[..., np.newaxis]
        fluid_state_matrix[self.affected_cells] = 0

        for i, dr in enumerate(self.allowed_velocities):
            dx, dy, dz = -dr.astype(np.int32)
            reverse_index = self.reverse_direction_indeces[i]
            fluid_state_matrix[..., reverse_index] += np.roll(affected_fluid_matrix[..., i],
                                                              (dx, dy, dz), axis=(0, 1, 2))


class ConstantVelocityBoundaryConditions(BoundaryConditions):
    def _update_velocities(self, boundary_condition_delta: BoundaryConditionConstantVelocityDelta) -> None:
        x1, y1, z1 = boundary_condition_delta.boundary_cube.start_position.to_tuple()
        x2, y2, z2 = boundary_condition_delta.boundary_cube.end_position.to_tuple()
        self.velocity[x1:x2, y1:y2, z1:z2] = boundary_condition_delta.velocity.to_numpy()
        self.normal_vectors[x1:x2, y1:y2, z1:z2] = boundary_condition_delta.normal.to_numpy()

    def __init__(self, shape: tuple[int, int, int], allowed_velocities: np.ndarray[np.ndarray[np.int32]]):
        super().__init__(shape, allowed_velocities)
        self.velocity = np.zeros(shape + (3,))
        self.normal_vectors = np.zeros(shape + (3,))

    def update_boundary(self, boundary_condition_delta: BoundaryConditionConstantVelocityDelta) -> None:
        self._update_affected_cells(boundary_condition_delta.boundary_cube)
        self._update_velocities(boundary_condition_delta)

    def process_fluid_state(self, fluid_state: BoltzmannFluidState) -> None:
        fluid_state_matrix = fluid_state.fluid_state
        density_state_matrix = FluidDensityState.from_boltzmann_state(fluid_state).density_state
        affected_fluid_matrix = fluid_state_matrix * self.affected_cells[..., np.newaxis]

        density_state_matrix_third = density_state_matrix / 3
        density_state_matrix_sixth = density_state_matrix / 6

        normal_vectors_dot_velocity = np.inner(self.normal_vectors, self.allowed_velocities)
        sum_partial_coefficients = 1 - np.abs(normal_vectors_dot_velocity)

        affected_fluid_mask = normal_vectors_dot_velocity < 0
        affected_fluid_matrix *= affected_fluid_mask

        fluid_state_matrix[self.affected_cells] = 0

        for i, dr in enumerate(self.allowed_velocities):
            dx, dy, dz = -dr.astype(np.int32)
            reverse_index = self.reverse_direction_indeces[i]

            tangential_vectors = dr - self.normal_vectors * np.inner(self.normal_vectors, dr)[..., np.newaxis]

            ci_dot_velocity = np.inner(self.velocity, dr)

            tangential_vectors_dot_velocity = np.sum(tangential_vectors * self.velocity, axis=-1)

            sum_tangential_coefficients = np.inner(tangential_vectors, self.allowed_velocities)

            sum_all_coefficients = sum_partial_coefficients * sum_tangential_coefficients

            all_terms_sum = affected_fluid_matrix[..., i]
            all_terms_sum += -density_state_matrix_sixth * ci_dot_velocity
            all_terms_sum += -density_state_matrix_third * tangential_vectors_dot_velocity
            all_terms_sum += 0.5 * np.sum(affected_fluid_matrix * sum_all_coefficients, axis=-1)

            fluid_state_matrix[..., reverse_index] += np.roll(all_terms_sum * affected_fluid_mask[..., i], (dx, dy, dz), axis=(0, 1, 2))
