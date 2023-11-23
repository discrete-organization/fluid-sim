from dataclasses import dataclass


@dataclass
class SimulationParameters:
    viscosity: float
    time_delta: float
    cell_length: float
