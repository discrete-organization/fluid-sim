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
- c, --config: path to the configuration file
- s, --steps-per-frame: number of steps between each frame
- o, --output: path to the output folder
- n, --number-of-steps: number of steps to simulate
- ns, --no-screen: do not display the simulation on the screen
- d, --use-density: use density instead of velocity to calculate the state function
