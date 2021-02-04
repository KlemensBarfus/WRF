# gets the geopotential on half levels and full levels for WRF [m2 s-2]
# ouput is from bottom to top
def WRF_geopotential_half_and_full_levels(f_wrf):
  # 'f_wrf' is the file handle for the open WRF file
  from netCDF4 import Dataset
  import numpy as np
  perturbation_geopotential = f_wrf.variables["PH"][:] # PH(Time, bottom_top_stag, south_north, west_east), [m2 s-2]
  base_state_geopotential = f_wrf.variables["PHB"][:] # PHB(Time, bottom_top_stag, south_north, west_east), [m2 s-2]
  # info on variables: https://www.openwfm.org/wiki/How_to_interpret_WRF_variables
  geopotential_half_levels =  perturbation_geopotential + base_state_geopotential
  n_temp = geopotential_half_levels.shape
  nz = n_temp[1]
  geopotential_full_levels = (geopotential_half_levels[:,0:nz-1,:,:] + geopotential_half_levels[:,1:nz,:,:])*0.5
  return geopotential_half_levels, geopotential_full_levels
