import argparse
from dataclasses import dataclass


@dataclass
class SimulationArgs:
    config_path: str
    steps_per_frame: int
    output_path: str


class ArgsReader:
    @staticmethod
    def read_args() -> SimulationArgs:
        parser = argparse.ArgumentParser()
        parser.add_argument('--config', type=str, default='input/config.json')
        parser.add_argument('--steps-per-frame', type=int, default='10')
        parser.add_argument('--output', '-o', type=str, default='output.mp4')

        args = parser.parse_args()

        return SimulationArgs(args.config, args.steps_per_frame, args.output)

