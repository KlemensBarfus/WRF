# plot WRF met_em files
# written by K.Barfus 03.09.2019
import matplotlib as mpl
#mpl.use('Agg')
import sys
from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
from lambert import lambert_xy
from plot_data_field_on_map import plot_binary_field_on_map

filename = "/home/klemens/temp/met_em.d01.2007-06-17_01:00:00.nc" #sys.argv[1]
#if(len(sys.argv) == 3):
#  vars = [sys.argv[2]]
#else:
#  vars = ["TEST"]
vars = ["LANDMASK"]
n_vars = len(vars)
 
# get year month and day from filename
temp_str = filename.split("/")
filename_plot = filename.replace(".nc", ".png")
temp_str2 = temp_str[len(temp_str)-1]
temp_str3 = temp_str2.split(".")
domain = temp_str3[1]
date_str = temp_str3[2]
year_str = date_str[0:4]
month_str = date_str[5:7]
day_str = date_str[8:10]
hour_str = date_str[11:13]
minute_str = date_str[14:16]
second_str =  date_str[17:19]                     


f = Dataset(filename, "r", format="NetCDF4")
lat = f.variables['XLAT_C']
lat = np.squeeze(lat[0,:,:])
lon = f.variables['XLONG_C']
lon = np.squeeze(lon[0,:,:])
nxy = lat.shape
n_lon = nxy[0]
n_lat = nxy[1]
# get projection data
if(f.MAP_PROJ == 1): # Lambert
  # setup lambert conformal basemap.
  # lat_1 is first standard parallel.
  # lat_2 is second standard parallel (defaults to lat_1).
  # lon_0,lat_0 is central point.
  # rsphere=(6378137.00,6356752.3142) specifies WGS84 ellipsoid
  # area_thresh=1000 means don't plot coastline features less
  # than 1000 km^2 in area.
  r_wrf = 6370000.00
  x1, y1 = lambert_xy(lon[0,0], lat[0,0], f.CEN_LON, f.CEN_LAT, f.TRUELAT1, f.TRUELAT2, r_wrf)
  x2, y2 = lambert_xy(lon[0,n_lon-1], lat[0,n_lon-1], f.CEN_LON, f.CEN_LAT, f.TRUELAT1, f.TRUELAT2, r_wrf)
  x3, y3 = lambert_xy(lon[n_lat-1,0], lat[n_lat-1,0], f.CEN_LON, f.CEN_LAT, f.TRUELAT1, f.TRUELAT2, r_wrf)
  x4, y4 = lambert_xy(lon[n_lat-1,n_lon-1], lat[n_lat-1,n_lon-1], f.CEN_LON, f.CEN_LAT, f.TRUELAT1, f.TRUELAT2, r_wrf)
  dx1 = abs(x2-x1)
  dx2 = abs(x4-x3)
  width = max([dx1,dx2])
  dy1 = abs(y3 - y1)
  dy2 = abs(y4 - y2)
  height = max([dy1,dy2])
  print(n_vars)
  for i_var in range(0, n_vars):
    m = Basemap(width=width,height=height,
            rsphere=(r_wrf, r_wrf),\
            resolution='l',projection='lcc',\
            lat_1=f.TRUELAT1,lat_2=f.TRUELAT2,lat_0=f.CEN_LAT,lon_0=f.CEN_LON)
    m.drawcoastlines(linewidth=0.0, color="gray")
    var = f.variables[vars[i_var]]
    if(var.ndim == 3):
      var = np.squeeze(var[:,:,:])
    else:
      var = np.squeeze(var[:,:,:,:])  
    #m.drawcoastlines()
    if(vars[i_var] == "LANDMASK"):
      print("test")
      rgba_0 = (0.0,0.0,1.0,1.0)
      rgba_1 = (0.0,1.0,0.0,1.0)
      print(lon.min(), lon.max(), lat.min(), lat.max())
      plot_binary_field_on_map(var, lon, lat, m, rgba_0, rgba_1)
      #lon = f.CEN_LON
      #lat = f.CEN_LAT
      #x,y = m(lon, lat)
      #m.plot(x, y, 'o', color=rgba_0,  markersize=24)
    #m.fillcontinents(color='coral',lake_color='aqua')
    # draw parallels and meridians.
    #m.drawparallels(np.arange(-80.,81.,20.))
    #m.drawmeridians(np.arange(-180.,181.,20.))
    #m.drawmapboundary(fill_color=rgba_0)
    print("title")
    plt.title("Lambert Conformal Projection")
    print("show")
    plt.show()
    #plt.savefig(filename_plot, format='png')
    plt.close()
    #plt.show()

f.close()
