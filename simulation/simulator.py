import pygame
import os

from simulation.windowDTO import WindowProperties
from .fluidRenderer import FluidRenderer
from utilities.argsReader import ArgsReader
from utilities.modelConfigReader import ModelConfigReader
from model.boltzmannFluid import BoltzmannFluid
from utilities.DTO.boundaryConditionDTO import (
    BoundaryConditionNoSlipDelta,
    BoundaryConditionConstantVelocityDelta,
    BoundaryConditionInitialDelta
)


class Simulator:   
    def __init__(self):
        self._simulation_steps_count = 0
        self._simulation_args = ArgsReader.read_args()
        self._model_config_reader = ModelConfigReader(self._simulation_args.config_path)
        print(self._simulation_args)

    def run(self) -> None:
        self._init_fluid()
        self._pygame_init()
        self._pygame_loop()
        self._pygame_quit()

    def _init_fluid(self) -> None:
        lattice_shape = self._model_config_reader.lattice_dimensions()
        simulation_parameters = self._model_config_reader.simulation_parameters()
        self._fluid = BoltzmannFluid(lattice_shape.to_tuple(), simulation_parameters)
        for boundary_condition_delta in self._model_config_reader.boundary_conditions():
            match boundary_condition_delta:
                case BoundaryConditionNoSlipDelta() as no_slip_boundary_condition_delta:
                    self._fluid.update_no_slip_boundary(no_slip_boundary_condition_delta)
                case BoundaryConditionConstantVelocityDelta() as constant_velocity_boundary_condition_delta:
                    self._fluid.update_constant_velocity_boundary(constant_velocity_boundary_condition_delta)
                case BoundaryConditionInitialDelta() as initial_boundary_condition_delta:
                    self._fluid.update_initial_boundary(initial_boundary_condition_delta)
                case _:
                    raise ValueError(f"Invalid boundary condition type: {type(boundary_condition_delta)}")
        self._fluid.prepare_boundary_conditions()

        if not 0 <= self._simulation_args.z < lattice_shape.get_z():
            raise ValueError(f"Invalid z coordinate: {self._simulation_args.z}. Change value to one within the boundaries ({lattice_shape.get_z()}).")

    def _pygame_init(self) -> None:
        pygame.init()
        pygame.display.set_caption("Fluid simulation")
        info = pygame.display.Info()
        self.constants = WindowProperties(info.current_w, info.current_h)
        self.window = pygame.display.set_mode((self.constants.WIN_W, self.constants.WIN_H)) \
            if self._simulation_args.draw_on_screen else None
        self._clock = pygame.time.Clock()
        self._running = True
        self._simulation_steps_count = 0
        self._fluid_renderer = FluidRenderer(self.window, self.constants, self._simulation_args,
                                             self._model_config_reader.lattice_dimensions().to_tuple())

    def _prepare_output_directory(self) -> None:
        if not os.path.exists(self._simulation_args.output_path):
            os.makedirs(self._simulation_args.output_path)

    def _process_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False

    def _simulation_step(self) -> None:
        self._fluid.simulation_step()
        self._simulation_steps_count += 1
        print(f"Simulation step: {self._simulation_steps_count}/{self._simulation_args.number_of_steps}")

    def _pygame_render(self) -> None:
        if self._simulation_args.draw_on_screen:
            self.window.fill(self.constants.BLACK)

        self._fluid_renderer.render_fluid(self._fluid, self._simulation_args.z)

        if not self._simulation_args.draw_on_screen:
            return
        pygame.display.flip()
        self._clock.tick(60)

    def _pygame_loop(self) -> None:
        self._pygame_render()

        while self._simulation_steps_count < self._simulation_args.number_of_steps and self._running:
            self._process_events()

            number_of_steps = min(self._simulation_args.steps_per_frame,
                                  self._simulation_args.number_of_steps - self._simulation_steps_count)
            for _ in range(number_of_steps):
                self._simulation_step()
            self._pygame_render()

        self._fluid_renderer.save_video()

    def _pygame_quit(self) -> None:
        self._running = False
        pygame.quit()

