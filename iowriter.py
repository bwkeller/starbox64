import h5py
import numpy as np

def write_arepo_HDF(fname, N, gas_mass, gas_pos, part_type=6):
    f = h5py.File(fname, 'w')
    config = f.create_group('Config')
    header = f.create_group('Header')
    params = f.create_group('Parameters')
    gas = f.create_group('PartType0')
    stars = f.create_group('PartType1')

    zeropart = np.zeros(part_type)
    numpart = np.zeros(part_type)
    numpart[0] = N

    header.attrs['NumPart_ThisFile'] = numpart
    header.attrs['NumPart_Total'] = numpart
    header.attrs['NumPart_Total_HighWord'] = zeropart

    header.attrs['MassTable'] = zeropart
    header.attrs['Time'] = 0
    header.attrs['Redshift'] = 0
    header.attrs['BoxSize'] = 1
    header.attrs['NumFilesPerSnapshot'] = 0

    # Cosmology is not important here, we aren't using comoving coordinates
    header.attrs['Omega0'] = 0
    header.attrs['OmegaLambda'] = 0
    header.attrs['OmegaBaryon'] = 0
    header.attrs['HubbleParam'] = 0

    header.attrs['Flag_Sfr'] = 0
    header.attrs['Flag_Cooling'] = 0
    header.attrs['Flag_StellarAge'] = 0
    header.attrs['Flag_Metals'] = 0
    header.attrs['Flag_Feedback'] = 0
    header.attrs['Flag_DoublePrecision'] = 1
    gas['Masses'] = gas_mass
    gas['Velocities'] = np.zeros((N, 3))
    gas['Coordinates'] = gas_pos
    gas['ParticleIDs'] = np.arange(N)+1
    f.close()
