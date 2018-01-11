# Starbox64
## A tool for making Initial Conditions For Feedback/ISM Simulations
Starbox64 is a simple python script for generating initial conditions
for unit testing stellar feedback.  This is a simple tool for making simple ICs:
a single star (cluster) particle in the center of a uniform, periodic box of
gas.  Currently, starbox64 can generate initial conditions in gadget/AREPO HDF5
format, but tipsy support will be added any day now.

## Usage
```
./starbox64 boxSize boxN starMass -n NUM | -d RHO | -g MASS [OPTIONS]
```
Starbox will generate an HDF5 file named with the box resolution, size, and star
mass.

## Arguments/Options
By specifying one of -n, -d, or -g, the gas particle mass can be determined.

* __boxSize__: The size of the box, in parsecs
* __boxN__: The number of particles per box length
* __starMass__: The mass of the star particle in solar masses
* __-n NUM__: Set the gas density of the box to NUM, in H/cc
* __-d RHO__: Set the gas density of the box to RHO, in Msol/pc^3
* __-g MASS__: Set the gas particle mass to MASS, in Msol
* __-c__: Write out quantities with CGS units.
* __-m__: Write out quantities with Msol, pc, and km/s units.


