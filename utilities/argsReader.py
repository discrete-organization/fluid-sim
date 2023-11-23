import argparse
from dataclasses import dataclass


@dataclass
class SimulationArgs:
    config_path: str
    steps_per_frame: int


class ArgsReader:
    @staticmethod
    def read_args() -> SimulationArgs:
        parser = argparse.ArgumentParser()
        parser.add_argument('--config', type=str, default='input/config.json')
        parser.add_argument('--steps-per-frame', type=int, default='10')

        args = parser.parse_args()

        return SimulationArgs(args.config, args.steps_per_frame)

