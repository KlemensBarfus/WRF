def WRF_deaccumulate_precipitation_data(wrf_data, ref_data=None):
  import numpy as np
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
    wrf_data_new[i,:,:] = temp * 12 # mm to mm/h
  return wrf_data_new
