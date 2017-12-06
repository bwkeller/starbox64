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
    idx = np.concatenate(np.meshgrid(range(n_side), range(n_side), range(n_side),
        indexing='ij')).reshape(3, n_side*(n_side)*(n_side))
    i = idx[0]
    j = idx[1]
    k = idx[2]
    x = (2*i+((j+k) % 2))/float(2*n_side)
    y = np.sqrt(3)*(j+1./3*(k % 2))/float(2*n_side)
    z = 2*np.sqrt(6)*k/(3*float(2*n_side))
    arr = np.array([x,y,z]).T
    # Shift the HCP lattice to the center of the box
    edge = arr.max(axis=0)+np.sqrt(6)/(6.*n_side)
    arr = arr / np.stack([edge for _ in range(arr.shape[0])])
    return arr
