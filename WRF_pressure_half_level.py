# gets the pressure on half levels for WRF [Pa]
# ouput is from bottom to top
def WRF_pressure_half_level(f_wrf, full_level_pressure=None):
  # 'f_wrf' is the file handle for the open WRF file
  from netCDF4 import Dataset
  import numpy as np
  if(full_level_pressure is None):
    pertubation_pressure = f_wrf.variables["P"][:] # P(Time, bottom_top, south_north, west_east), [Pa]
    base_state_pressure = f_wrf.variables["PB"][:] # PB(Time, bottom_top, south_north, west_east), [Pa]
    full_level_pressure = pertubation_pressure + base_state_pressure # in Pa 
  n_temp = full_level_pressure.shape
  n_time = n_temp[0]
  n_levels = n_temp[1]
  n_lat = n_temp[2]
  n_lon = n_temp[3]
  pressure_top = f_wrf.variables["P_TOP"][:]  # (Time), [Pa]
  pressure_surface = f_wrf.variables["PSFC"][:]  # (Time, south_north, west_east), [Pa]
  pressure_top = np.tile(pressure_top.reshape(len(pressure_top),1,1,1),(1,1,n_lat,n_lon)) # https://stackoverflow.com/questions/64921773/extend-1d-numpy-array-in-multiple-dimensions
  pressure_surface = pressure_surface[:,np.newaxis,:,:]
  pressure_half_levels = np.zeros((n_time,n_levels+1,n_lat,n_lon)) 
  pressure_half_levels[:,0:1,:,:] = pressure_surface
  pressure_half_levels[:,1:n_levels,:,:] = (full_level_pressure[:,0:n_levels-1,:,:] + full_level_pressure[:,1:n_levels,:,:]) / 2.0
  pressure_half_levels[:,n_levels:n_levels+1,:,:] = pressure_top
  if(full_level_pressure is None):
    return pressure_half_levels, full_level_pressure
  else:
    return pressure_half_levels

