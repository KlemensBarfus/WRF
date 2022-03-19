def get_WRF_plot_coordinates(filename_wrf):
  # gets the wrf coordinates (plot coordinates, so nx/ny+1) for the national product
  import math
  import numpy as np
  from WRF_get_plot_grid_for_geographical_coordinates import WRF_get_plot_grid_for_geographical_coordinates
  import netCDF4
    
  nc_file = netCDF4.Dataset(filename_wrf)
  if('XLONG' in nc_file.variables):
    lon = nc_file.variables['XLONG'][:,:,:] # XLAT(Time, south_north, west_east)
    lat = nc_file.variables['XLAT'][:,:,:]
  else:
    if('XLONG_M' in nc_file.variables):
      lon = nc_file.variables['XLONG_M'][:,:,:] # XLAT(Time, south_north, west_east)
      lat = nc_file.variables['XLAT_M'][:,:,:]
  nc_file.close()
  lon = np.squeeze(lon[0,:,:])
  lat =	np.squeeze(lat[0,:,:])
  lat_plot, lon_plot = WRF_get_plot_grid_for_geographical_coordinates(lat, lon)
  return lat_plot, lon_plot

def get_WRF_coordinates(filename_wrf):
  import math
  import numpy as np
  import netCDF4

  nc_file = netCDF4.Dataset(filename_wrf)
  if('XLONG' in nc_file.variables):
    lon = nc_file.variables['XLONG'][:,:,:] # XLAT(Time, south_north, west_east)
    lat = nc_file.variables['XLAT'][:,:,:]
  else:
    if('XLONG_M' in nc_file.variables):
      lon = nc_file.variables['XLONG_M'][:,:,:] # XLAT(Time, south_north, west_east)
      lat = nc_file.variables['XLAT_M'][:,:,:]
  nc_file.close()
  lon = np.squeeze(lon[0,:,:])
  lat = np.squeeze(lat[0,:,:])
  return lat, lon

  

def save_WRF_coordinates(filename_wrf):
  import numpy as np
  from netCDF4 import Dataset
  #get domain
  ii = filename_wrf.find("d0")
  domain_str = filename_wrf[ii:ii+3] 
  lat_temp, lon_temp = get_WRF_coordinates(filename_wrf)
  lat_plot_temp, lon_plot_temp = get_WRF_plot_coordinates(filename_wrf)
  n_temp = lat_temp.shape
  n_lat = n_temp[0]
  n_lon = n_temp[1]
  temp_str = filename_wrf.split("/")
  if(len(temp_str) > 1): # path exists
    path = "/".join(temp_str[0:len(temp_str)-1])+"/"
  else:
    path = ""                    
  filename_out = path+"WRF_coordinates_"+domain_str+".nc"
  f = Dataset(filename_out,'w', format='NETCDF4') #'w' stands for write
  f.createDimension('lon', n_lon)
  f.createDimension('lat', n_lat)
  f.createDimension('corners', 4)
  lon = f.createVariable('lon', 'f4', ('lat','lon'))
  lat = f.createVariable('lat', 'f4', ('lat','lon'))
  lon_plot = f.createVariable('lon_plot', 'f4', ('lat','lon','corners'))
  lat_plot = f.createVariable('lat_plot', 'f4', ('lat','lon','corners'))
  corners = f.createVariable('corners', 'S4', ('corners'))
  lon[:] = lon_temp
  lat[:] = lat_temp
  lon_plot[:] = lon_plot_temp
  lat_plot[:] = lat_plot_temp
  corners[:] = np.asarray(['lower left', 'lower right', 'upper right', 'upper left'])
  f.close()

def read_WRF_coordinates(filename):
  import numpy as np
  from netCDF4 import Dataset
  f = Dataset(filename,'r', format='NETCDF4')
  lon = f.variables['lon'][:]
  lat =	f.variables['lat'][:]
  f.close()
  return lat, lon

def read_WRF_plot_coordinates(filename):
  import numpy as np
  from netCDF4 import Dataset
  f = Dataset(filename,'r', format='NETCDF4')
  lon_plot = f.variables['lon_plot'][:]
  lat_plot = f.variables['lat_plot'][:]
  f.close()
  return lat_plot, lon_plot
  
#filename = '/home/klemens/Python_routines/wrf_d04_1979-06-21_22:30:00'
#save_WRF_coordinates(filename)
#filename = '/home/klemens/Python_routines/WRF_coordinates_d04.nc'
#lat, lon = read_WRF_coordinates(filename)
#lat_plot, lon_plot = read_WRF_plot_coordinates(filename)
