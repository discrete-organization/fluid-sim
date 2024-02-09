# Lattice Boltzmann Fluid Simulation

## About
This repo features a simple fluid simulation using the Lattice Boltzmann Method. The Lattice Boltzmann Method (LBM) is a numerical method based on a probabilistic description of the particles' movements, specifically designed for simulating fluid flows. In LBM, the fluid is represented as a collection of fictitious populations that move and collide on a lattice. Each population carries information about the fluid properties, such as density and velocity, and follows simplified collision and streaming rules.    
In our model we used D3Q19, a 3D lattice with 19 velocities. Choosing such a lattice gave us results accurate enough, that after averaging the state function values, the fluid exhibited consistency with Navier-Stokes equations.

## Installation
In order to run the program, you will need to install Python3.11 and pip. Then install the required dependencies by typing:
```bash
pip install -r requirements.txt
```

## Usage
Begin with creating `config.json` file. Example configuration file can be found in `/input` folder.
Then run the program by typing:
```bash
python main.py
```
Use following flags to change the default behaviour:
- z, --zaxis: select render depth
- c, --config: path to the configuration file
- s, --steps-per-frame: number of steps between each frame
- o, --output: path to the output folder
- n, --number-of-steps: number of steps to simulate
- ns, --no-screen: do not display the simulation on the screen
- d, --use-density: use density instead of velocity to calculate the state function

## Results
### Example 1
[Config file](input/config.json)

Density:
![density1](https://github.com/discrete-organization/fluid-sim/assets/93160829/b7585e5a-34b9-4e1e-a42d-445121b7a8f9)

Velocity:
![velocity1](https://github.com/discrete-organization/fluid-sim/assets/93160829/f6ff659a-1d4d-4b57-b877-6b6a1584b09a)

### Example 2
[Config file](input/config1.json)

Density:
![density2](https://github.com/discrete-organization/fluid-sim/assets/93160829/c0c23332-a822-4ab4-9e34-f3b90769966b)

Velocity:
![velocity2](https://github.com/discrete-organization/fluid-sim/assets/93160829/fe0f924f-82c6-4498-8023-d47376c2a63f)
