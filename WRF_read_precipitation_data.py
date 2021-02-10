def WRF_read_precipitation_data(file_wrf):
  # reads WRF precipitation data
  # no deaccumulation
  # file_wrf is either a file handle or a filename
  from netCDF4 import Dataset
  import numpy as np
  import datetime
  if(type(file_wrf) is str):
    f_wrf = Dataset(file_wrf, "r", format="NetCDF4")
  else:
    f_wrf = file_wrf
  # get time and lat/lon
  lat = np.squeeze(f_wrf.variables["XLAT"][:])
  lon = np.squeeze(f_wrf.variables["XLONG"][:])
  times_temp = f_wrf.variables["Times"][:]
  times = []
  for t in times_temp:
    t2 = t.tostring().decode()
    year_temp = int(t2[0:4])
    month_temp = int(t2[5:7])
    day_temp = int(t2[8:10])
    hour_temp = int(t2[11:13])
    minute_temp = int(t2[14:16])
    second_temp = int(t2[17:19])
    date_temp = datetime.datetime(year_temp,month_temp,day_temp,hour_temp,minute_temp,second_temp)
    times.append(date_temp)
  times = np.asarray(times) 
  rainc = f_wrf.variables["RAINC"][:]
  rainnc = f_wrf.variables["RAINNC"][:]
  rain = np.add(rainc,rainnc)
  if(type(file_wrf) is str):
    f_wrf.close()
  return rain, times, lat, lon
