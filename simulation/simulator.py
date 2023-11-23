import pygame
from simulation.fluidRenderer import FluidRenderer
from utilities.argsReader import ArgsReader
from utilities.modelConfigReader import ModelConfigReader
from model.boltzmannFluid import BoltzmannFluid
from utilities.DTO.boundaryConditionDTO import (
    BoundaryConditionNoSlipDelta,
    BoundaryConditionConstantVelocityDelta
)


class Simulator:   
    def _init_fluid(self) -> None:
        lattice_shape = self._model_config_reader.lattice_dimensions()
        self._fluid = BoltzmannFluid(lattice_shape.to_tuple())
        for boundary_condition_delta in self._model_config_reader.boundary_conditions():
            match boundary_condition_delta:
                case BoundaryConditionNoSlipDelta() as no_slip_boundary_condition_delta:
                    self._fluid.update_no_slip_boundary(no_slip_boundary_condition_delta)
                case BoundaryConditionConstantVelocityDelta() as constant_velocity_boundary_condition_delta:
                    self._fluid.update_constant_velocity_boundary(constant_velocity_boundary_condition_delta)
                case _:
                    raise ValueError("Invalid boundary condition type.")

    def _pygame_init(self) -> None:
        pygame.init()
        self._screen = pygame.display.set_mode((1280, 720))
        self._clock = pygame.time.Clock()
        self._running = True
        self._simulation_steps_count = 0
        self._fluid_renderer = FluidRenderer()

    def _process_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False

    def _simulation_step(self) -> None:
        # TODO: simulation step
        self._simulation_steps_count += 1

    def _pygame_render(self) -> None:
        self._screen.fill((0, 0, 0))
        self._fluid_renderer.render_fluid(self._fluid)

    def _pygame_loop(self) -> None:
        while self._running:
            self._process_events()
            for _ in range(self._simulation_args.steps_per_frame):
                self._simulation_step()
            self._pygame_render()
            pygame.display.flip()
            self._clock.tick(60)

    def _pygame_quit(self) -> None:
        self._running = False
        pygame.quit()

    def __init__(self):
        self._simulation_steps_count = 0
        self._simulation_args = ArgsReader.read_args()
        self._model_config_reader = ModelConfigReader(self._simulation_args.config_path)

    def run(self) -> None:
        self._pygame_init()
        self._pygame_loop()
        self._pygame_quit()
