# plots the WRF land use index

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import sys
from netCDF4 import Dataset
from plot_Berlin_shape import plot_Berlin_shape
import numpy as np

filename_nc = 'geo_em.d03.nc'
f = Dataset(filename_nc, "r", format="NetCDF4")
lonname = 'XLONG_M'
latname = 'XLAT_M'
lat = f.variables[latname]
if(lat.ndim == 2):
  lat = lat[:,:]
else:
  if(lat.ndim == 3):
    lat = np.squeeze(lat[0,:,:])
lon = f.variables[lonname]
if(lon.ndim == 2):
  lon = lon[:,:]
else:
  if(lon.ndim == 3):
    lon = lon[0,:,:]
LU_INDEX =  f.variables['LU_INDEX'][:]
f.close()

m = Basemap(projection='merc',
             llcrnrlon=lon.min(),
             llcrnrlat=lat.min(),
             urcrnrlon=lon.max(),
             urcrnrlat=lat.max(),
             resolution='i')

m.pcolormesh(lon, lat, np.squeeze(LU_INDEX[0,:,:]), latlon=True)

plot_Berlin_shape(m, plt, fill=False, linewidth=1.0)

filename_plot = "LU_INDEX.png"
plt.savefig(filename_plot, dpi=300, bbox_inches='tight')
plt.close()

