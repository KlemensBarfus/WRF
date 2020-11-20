def WRF_read_precipitation_data(file_wrf):
  # reads WRF precipitation data
  # file_wrf is either a file handle or a filename
  from netCDF4 import Dataset
  if(type(file_wrf) is str):
    f_wrf = Dataset(file_wrf, "r", format="NetCDF4")
  else:
    f_wrf = file_wrf
  rainc = f_wrf.variables["RAINC"][:]
  rainnc = f_wrf.variables["RAINNC"][:]
  rain = np.add(rainc,rainnc)
  if(type(file_wrf) is str):
    f_wrf.close()
  return rain
