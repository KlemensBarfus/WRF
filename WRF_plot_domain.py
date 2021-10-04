def WRF_plot_domain(filename,m, rgb, latname='XLAT_M', lonname='XLONG_M'):
  from netCDF4 import Dataset
  from matplotlib.patches import Polygon
  import numpy as np
  import matplotlib.pyplot as plt
  # plots the WRF_domain boundaries on a given map defined by m
  # written by K. Barfus 20/09/2017

  f = Dataset(filename, "r", format="NetCDF4")
  lat = f.variables[latname]
  if(lat.ndim == 2):
    lat = lat[:,:]
  else:
    if(lat.ndim == 3):  
      lat = lat[0,:,:]
  lon = f.variables[lonname]
  if(lon.ndim == 2):
    lon = lon[:,:]
  else:
    if(lon.ndim == 3):  
      lon = lon[0,:,:]
  f.close()  
  nxy = lat.shape
  nx = nxy[1]
  ny = nxy[0]
  n_all = 2 * nx + 2 * (ny - 2)
  jj = 0
  xy_all = np.zeros((n_all,2))
  #for ii in range(0, len(m.Berlin_WGS84_l[0])):
  #  xy_all[ii,0] = m.Berlin_WGS84_l[0][ii][0] 
  #  xy_all[ii,1] =  m.Berlin_WGS84_l[0][ii][1]
  #  jj = jj + 1  
   # first line ("lower")
  for ix in range(0, nx):
    if(ix == 0):
      lon_temp = lon[0,ix] - 0.5 * (lon[0,ix+1] - lon[0,ix])
    else:
      if(ix == nx-1):
        lon_temp = lon[0,ix] + 0.5 * (lon[0,ix] - lon[0,ix-1])
      else:
        lon_temp = lon[0,ix]
    lat_temp = lat[0,ix] - 0.5 * (lat[1,ix] - lat[0,ix])
    xy_all[jj,:] = m(lon_temp, lat_temp)
    jj = jj + 1 
  # second line ("right")
  for iy in range(1, ny-1):
    lon_temp = lon[iy,nx-1] + 0.5 * (lon[iy,nx-1] - lon[iy,nx-2])   
    lat_temp = lat[iy,nx-1]
    xy_all[jj,:] = m(lon_temp, lat_temp)
    jj = jj + 1
  # third line ("upper")
  for ix in range(nx-1, -1, -1):
    if(ix == nx-1):
      lon_temp = lon[ny-1,ix] + 0.5 * (lon[ny-1,ix] - lon[ny-1,ix-1])  
    else:
      if(ix == 0):
        lon_temp = lon[ny-1,ix] - 0.5 * (lon[ny-1,ix+1] - lon[ny-1,ix])
      else:
        lon_temp = lon[ny-1,ix]
    lat_temp = lat[ny-1,ix] + 0.5 * (lat[ny-1,ix] - lat[ny-2,ix])  
    xy_all[jj,:] = m(lon_temp, lat_temp)
    jj = jj + 1
  # fourth line ("left")
  for iy in range(ny-2, 0, -1):
    lon_temp = lon[iy,0] - 0.5 * (lon[iy,1] - lon[iy,0])   
    lat_temp = lat[iy,0]  
    xy_all[jj,:] = m(lon_temp, lat_temp)
    jj = jj + 1
  poly = Polygon(xy_all, color=rgb, edgecolor=rgb, fill=False, linewidth=2, zorder=10) #, transform=IdentityTransform())
  plt.gca().add_patch(poly)
  
