import argparse
from dataclasses import dataclass


@dataclass
class SimulationArgs:
    config_path: str
    steps_per_frame: int
    output_path: str
    number_of_steps: int
    draw_on_screen: bool
    use_density: bool


class ArgsReader:
    @staticmethod
    def read_args() -> SimulationArgs:
        parser = argparse.ArgumentParser()
        parser.add_argument('--config', '-c', type=str, default='input/config.json')
        parser.add_argument('--steps-per-frame', '-s', type=int, default='10')
        parser.add_argument('--output', '-o', type=str, default='output')
        parser.add_argument('--number-of-steps', '-n', type=int, default='10000')
        parser.add_argument('--no-screen', '-ns', action='store_true')
        parser.add_argument('--use-density', '-d', action='store_true')

        args = parser.parse_args()

        return SimulationArgs(args.config, args.steps_per_frame,
                              'output/' + args.output + '.mp4',
                              args.number_of_steps, not args.no_screen,
                              args.use_density)

