#!/usr/bin/env python
import numpy as np
import argparse

# Units in CGS
PC_IN_CGS = 3.086e18
MSOL_IN_CGS = 1.988e33
MP_IN_CGS = 1.674e-24
MYR_IN_CGS = 3.154e13

# Physical Constants
K_B = 1.381e-16
ZSOL = 0.013

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("boxSize", help="The size of the box, in parsecs", type=float)
    parser.add_argument("boxN", help="The number of particles per box length", type=int)
    parser.add_argument("starMass", 
            help="The mass of the star particle(s) in solar masses", type=float)
    parser.add_argument("-z", "--zmetal", 
            help="The metallicity of the gas, either as a fraction or a multiple of solar (eg, 0.013 or 1S)", 
            type=str)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-n", "--number_density", help="The density of the gas, in H/cc",
            type=float)
    group.add_argument("-d", "--mass_density", help="The density of the gas, in Msol/pc^3",
            type=float)
    group.add_argument("-g", "--gas_mass", help="The gas particle mass, in solar masses",
            type=float)
    args = parser.parse_args()
