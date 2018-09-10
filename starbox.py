#!/usr/bin/env python3
import argparse
from scipy import optimize
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

def calc_mass(args, N):
    if args.number_density:
        print("Using Number Density: %g H/cc" % args.number_density)
        mass = MP_IN_CGS * args.number_density * np.power(PC_IN_CGS *
                args.boxSize, 3) / N
    elif args.mass_density:
        print("Using Mass Density: %g Msol/pc^3" % args.mass_density)
        mass = MSOL_IN_CGS * args.mass_density * np.power(args.boxSize, 3) / N
    elif args.gas_mass:
        print("Using Gas Particle Mass: %g Msol" % args.gas_mass)
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
    parser.add_argument("-o", "--overdensity", help="""Add a spherical overdensity of radius r 
            and mass m in the format -o/--overdensity r,m.""", type=str)
    units = parser.add_mutually_exclusive_group()
    units.add_argument("-c", "--cgs", help="Code units will be written out in CGS",
            action='store_true', default=False)
    units.add_argument("-m", "--msol", help="Code units will be written out MSol, pc, km/s",
            action='store_true', default=True)
    mass_den = parser.add_mutually_exclusive_group(required=True)
    mass_den.add_argument("-n", "--number_density", help="The density of the gas, in H/cc",
            type=float)
    mass_den.add_argument("-d", "--mass_density", help="The density of the gas, in Msol/pc^3",
            type=float)
    mass_den.add_argument("-g", "--gas_mass", help="The gas particle mass, in solar masses",
            type=float)
    args = parser.parse_args()
    
    fname = "box_%d_%3.2e_pc_%3.2e_star.hdf5" % (args.boxN, args.boxSize, args.starMass)
    pos = geometry.hcp(args.boxN)
    gas_mass = calc_mass(args, pos.shape[0])
    if(args.overdensity):
        ball_r = float(args.overdensity.split(',')[0])
        ball_m = MSOL_IN_CGS*float(args.overdensity.split(',')[1])
        null,hole = geometry.slice_ball(pos, ball_r/args.boxSize)
        N_box = int(np.power(6*ball_m/(np.pi*gas_mass), 1./3))
        ball_pos = geometry.hcp(2*N_box)
        cntr=np.random.rand(1,3)/(1e5*N_box)+np.array((0.5,0.5,0.5))
        def iterate_ball(r):
            ball,null = geometry.slice_ball(ball_pos, r, center=cntr)
            return ball_m/gas_mass-ball.shape[0]
        r = optimize.bisect(iterate_ball, 0.25, 0.5)
        ball,null = geometry.slice_ball(ball_pos, r, center=cntr)
        ball -= 0.5
        ball *= ball_r/(args.boxSize*np.linalg.norm(ball).max())
        ball += 0.5
        pos = np.concatenate((ball,hole))
    print("Stellar Mass: %g Msol" % args.starMass)
    print ("Generating Box with %d particles" % pos.shape[0])
    print("Particle Mass: %e Msol" % (gas_mass/MSOL_IN_CGS))
    if(args.cgs):
        iowriter.write_arepo_HDF(fname, args.boxSize*PC_IN_CGS, gas_mass,
                pos, args.starMass*MSOL_IN_CGS, 1, 1, 1)
    if(args.msol):
        iowriter.write_arepo_HDF(fname, args.boxSize, gas_mass/MSOL_IN_CGS,
                pos, args.starMass, PC_IN_CGS, MSOL_IN_CGS, 1e5)
