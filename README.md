# Chaotic Divergence in the Three-Body Problem

## Overview
Because no general analytical solution exists for a system of three or more celestial bodies, predicting their orbits requires numerical integration. This repository explores the chaotic nature of the Three-Body Problem by simulating and visualizing Sensitive Dependence on Initial Conditions (The Butterfly Effect).

## Computational Methods
This script simulates two parallel multi-star systems using a 4th-order Runge-Kutta algorithm. The second system's initial conditions are perturbed by a microscopic fraction ($10^{-5}$ Astronomical Units). By tracking the physical distance between the two systems over time on a logarithmic scale, the script visually proves the exponential growth of error in chaotic systems (Lyapunov divergence).

**Skills Demonstrated:**
* Chaos Theory & Orbital Mechanics
* High-Precision Numerical Integration (`scipy.integrate`)
* Logarithmic Data Plotting & Analysis

## Usage
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the simulation: `python butterfly_effect.py`

The output generates two plots: one detailing the orbital tracks, and a logarithmic plot demonstrating the exponential divergence of the two universes over time.
