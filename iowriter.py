import h5py
import numpy as np

def write_arepo_HDF(fname, box_size, gas_mass, gas_pos, star_mass, part_type=6):
    f = h5py.File(fname, 'w')
    config = f.create_group('Config')
    header = f.create_group('Header')
    params = f.create_group('Parameters')
    gas = f.create_group('PartType0')
    stars = f.create_group('PartType4')

    zeropart = np.zeros(part_type)
    numpart = np.zeros(part_type)
    numpart[0] = gas_pos.shape[0]
    numpart[4] = 1
    masspart = np.zeros(part_type, dtype='<f8')
    masspart[0] = gas_mass
    masspart[4] = star_mass

    header.attrs['NumPart_ThisFile'] = numpart
    header.attrs['NumPart_Total'] = numpart
    header.attrs['NumPart_Total_HighWord'] = zeropart

    # MassTable isn't used for gas particles, since they can advect mass!
    header.attrs['MassTable'] = masspart
    header.attrs['Time'] = 0
    header.attrs['Redshift'] = 0
    header.attrs['BoxSize'] = box_size
    header.attrs['NumFilesPerSnapshot'] = 1

    header.attrs['UnitLength_in_cm'] = 1
    header.attrs['UnitMass_in_g'] = 1
    header.attrs['UnitVelocity_cm_per_s'] = 1

    # Cosmology is not important here, we aren't using comoving coordinates
    header.attrs['Omega0'] = 0
    header.attrs['OmegaLambda'] = 0
    header.attrs['OmegaBaryon'] = 0
    header.attrs['HubbleParam'] = 0

    header.attrs['Flag_Sfr'] = 0
    header.attrs['Flag_Cooling'] = 0
    header.attrs['Flag_StellarAge'] = 0
    header.attrs['Flag_Metals'] = 1
    header.attrs['Flag_Feedback'] = 1
    header.attrs['Flag_DoublePrecision'] = 1
    gas['Velocities'] = np.zeros(gas_pos.shape)
    gas['Masses'] = gas_mass*np.ones(gas_pos.shape[0])
    gas['InternalEnergy'] = np.zeros(gas_pos.shape[0])
    gas['Coordinates'] = gas_pos*box_size
    gas['ParticleIDs'] = np.arange(gas_pos.shape[0])+1
    gas['AllowRefinement'] = np.ones(gas_pos.shape[0])
    stars['Velocities'] = np.zeros((1,3))
    stars['Coordinates'] = np.ones((1,3))*box_size/2.
    stars['StellarAge'] = [0]
    stars['ParticleIDs'] = [0]
    f.close()
