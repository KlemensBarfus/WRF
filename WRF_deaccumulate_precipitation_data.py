def WRF_deaccumulate_precipitation_data(wrf_data, ref_data=None, dtime=None):
  # deaccumulates WRF precipitation output and calculates mm/h
  # if ref_data (2d array) is provided, it gives the values for the accumulation start
  # otherwise the first timestep of wrf_data[ntimes,nlat,nlon] is the accumulation start.
  # if dtime (minutes) is provided, it gives the minutes between the WRF output times otherwise
  # it is set to 5 minutes
  import numpy as np
  if(dtime is None):
    dtime = 5 # minutes
  ntimesteps_per_hour = 60/dtime  
  nxy = wrf_data.shape
  wrf_data_new = np.copy(wrf_data)
  n_times = nxy[0]
  ny = nxy[1]
  nx = nxy[2]
  for i in range(0, n_times):
    if(i == 0):
      if(ref_data is not None):
        temp = wrf_data[i,:,:] - ref_data
      else:
        temp = wrf_data[i,:,:]
    else:
      temp = wrf_data[i,:,:] - wrf_data[i-1,:,:]
    wrf_data_new[i,:,:] = temp * ntimesteps_per_hour # mm to mm/h
  return wrf_data_new
