"""
Geometry includes modules for generating x,y,z positions for a particle grid.
All methods will generate cubes with side length of 1, centered at 0.
"""
import numpy as np

def hcp(n_side):
    """
    Hexagonal close-pack.  Return x,y,z ndarrays for n_side^3 particles
    in a Hexagonal Close Pack grid.  
    """
    x = []
    y = []
    z = []
    for i in range(n_side):
        for j in range(n_side):
            for k in range(n_side):
                x.append((2*i+((j+k) % 2))/float(2*n_side))
                y.append(np.sqrt(3)*(j+1./3*(k % 2))/float(2*n_side))
                z.append(2*np.sqrt(6)*k/(3*float(2*n_side)))
                # shift to center at (0,0,0)
                x[-1] -= 0.5
                y[-1] -= 0.5
                z[-1] -= 0.5
    return np.array([x,y,z]).T
