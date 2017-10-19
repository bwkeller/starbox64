#!/usr/bin/env python3
import argparse
import numpy as np
import iowriter
import geometry

# Units in CGS
PC_IN_CGS = 3.086e18
MSOL_IN_CGS = 1.988e33
MP_IN_CGS = 1.674e-24
MYR_IN_CGS = 3.154e13

# Physical Constants
K_B = 1.381e-16
ZSOL = 0.013

def calc_mass(args):
    if args.number_density:
        mass = MP_IN_CGS * args.number_density * np.power(PC_IN_CGS *
                args.boxSize, 3) / args.boxN 
    elif args.mass_density:
        mass = MSOL_IN_CGS * args.mass_density * (np.power(args.boxSize, 3) /
                args.boxN)
    elif args.gas_mass:
        mass = MSOL_IN_CGS * args.gas_mass 
    else:
        raise RuntimeError("Cannot calculate density!")
    return mass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("boxSize", help="The size of the box, in parsecs", type=float)
    parser.add_argument("boxN", help="The number of particles per box length", type=int)
    parser.add_argument("starMass", 
            help="The mass of the star particle(s) in solar masses", type=float)
    parser.add_argument("-z", "--zmetal", 
            help="""The metallicity of the gas, either as a fraction 
            or a multiple of solar (eg, 0.013 or 1S)""", 
            type=str)
    parser.add_argument("-f", "--format", help="""The output format for the initial conditions.
            Currently supported formats are ArepoHDF.""", type=str)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-n", "--number_density", help="The density of the gas, in H/cc",
            type=float)
    group.add_argument("-d", "--mass_density", help="The density of the gas, in Msol/pc^3",
            type=float)
    group.add_argument("-g", "--gas_mass", help="The gas particle mass, in solar masses",
            type=float)
    args = parser.parse_args()
    
    fname = "box_%d_%3.2e_pc_%3.2e_star.hdf5" % (args.boxN, args.boxSize, args.starMass)
    fname = "test.hdf5"
    iowriter.write_arepo_HDF(fname, np.power(args.boxN, 3), args.boxSize*PC_IN_CGS, calc_mass(args),
            geometry.hcp(args.boxN), args.starMass*MSOL_IN_CGS)
