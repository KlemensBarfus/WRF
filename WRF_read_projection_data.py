def WRF_read_projection_data(filename):
  import numpy as np  
  from netCDF4 import Dataset
  f = Dataset(filename, "r", format="NetCDF4")
  center_latitude = f.getncattr('CEN_LAT')
  center_longitude = f.getncattr('CEN_LON')
  truelat1 = f.getncattr('TRUELAT1')
  truelat2 = f.getncattr('TRUELAT2')attribute_names = []
  standard_longitude = f.getncattr('STAND_LON')
  for name in f.ncattrs():
    attribute_names.append(name)
  if('MAP_PROJ_CHAR' in attribute_names):
    map_projection = f.getncattr('MAP_PROJ_CHAR')
  else:
    map_projection_nr = f.getncattr('MAP_PROJ')
    if(map_projection_nr == 1):
      map_projection = 'Lambert Conformal'
  f.close()
  proj = {'center_latitude': center_latitude, 'center_longitude': center_longitude, 'truelat1': truelat1, 'truelat2': truelat2, \
          'standard_longitude': standard_longitude, 'map_projection': map_projection}
  return proj
  
