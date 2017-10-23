"""
Geometry includes modules for generating x,y,z positions for a particle grid.
All methods will generate cubes with side length of 1, centered at 0.5
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
        for j in range(n_side+1):
            for k in range(n_side+2):
                x.append((2*i+((j+k) % 2))/float(2*n_side))
                y.append(np.sqrt(3)*(j+1./3*(k % 2))/float(2*n_side))
                z.append(2*np.sqrt(6)*k/(3*float(2*n_side)))
    arr = np.array([x,y,z]).T
    # Shift the HCP lattice to the center of the box
    arr = arr + np.stack([(1.0 - arr.max(axis=0))/2. for _ in range(arr.shape[0])])
    return arr
