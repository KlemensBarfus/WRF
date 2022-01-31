# plots the WRF land use index

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import sys
from netCDF4 import Dataset
from plot_Berlin_shape import plot_Berlin_shape
import numpy as np
from WRF_get_plot_grid_for_geographical_coordinates import WRF_get_plot_grid_for_geographical_coordinates
from plot_discrete_field_on_map import plot_discrete_field_on_map

#classes_usgs = ["Urban and Built-Up Land", "Dryland Cropland and Pasture", "Irrigated Cropland and Pasture", "Mixed Dryland/Irrigated Cropland and Pasture", "Cropland/Grassland Mosaic",
#            "Cropland/Woodland Mosaic", "Grassland", "Shrubland", "Mixed Shrubland/Grassland", "Savanna", "Deciduous Broadleaf Forest", "Deciduous Needleleaf Forest", 
#            "Evergreen Broadleaf Forest", "Evergreen Needleleaf Forest", "Mixed Forest", "Water Bodies", "Herbaceous Wetland", "Wooded Wetland", "Barren or Sparsely Vegetated", 
#            "Herbaceous Tundra", "Wooded Tundra", "Mixed Tundra", "Bare Ground Tundra", "Snow or Ice"]     

classes_igbp = ['Evergreen Needleleaf Forest', 'Evergreen Broadleaf Forest', 'Deciduous Needleleaf Forest', 'Deciduous Broadleaf Forest', 'Mixed Forest', 'Closed Shrubland', 'Open Shrubland', 
                'Woody Savannas', 'Savannas', 'Grasslands', 'Permanent wetland', 'Croplands', 'Urban and Built-Up', 'Cropland/natural vegetation mosaic', 'Snow and Ice', 'Barren or Sparsely Vegetated',
                'Water', 'Wooded Tundra', 'Mixed Tundra', 'Barren Tundra', 'Lake']

rgb_igbp = [(33,137,33),(48,204,48),(152,205,48),(131,251,151),(142,187,141),(186,142,143),(254,228,178),(198,222,160),(254,214,1),(239,182,100),(70,129,177),(248,236,115),
            (255,37,0),(152,145,83),(244,244,218),(188,188,188),(0,0,255),(188,143,143),(213,121,180),(253,186,242),(0,102,204)]

n = len(rgb_igbp)
for i in range(0, n):
  temp_tuple = rgb_igbp[i]
  temp_tuple2 = tuple(ti/255 for ti in temp_tuple)
  rgb_igbp[i] = temp_tuple2

filename_nc = '/scratch/ws/0/barfus-WRF4.3/WPS-4.3/20091008/geo_em.d03_original.nc'
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
LU_INDEX =  np.squeeze(LU_INDEX[0,:,:])
f.close()

lat_plot, lon_plot = WRF_get_plot_grid_for_geographical_coordinates(lat, lon)

fig = plt.figure(figsize=(6, 6))
ax1 = fig.add_axes([0.05, 0.05, 0.75, 0.9])
cmap = mpl.cm.get_cmap('jet')
values = np.arange(21)+1
n_values = 21
#colors = []
#for i in range(0, n_values):
#  colors.append(cmap((1.0/n_values)*i))


m = Basemap(projection='merc',
             llcrnrlon=lon_plot.min(),
             llcrnrlat=lat_plot.min(),
             urcrnrlon=lon_plot.max(),
             urcrnrlat=lat_plot.max(),
             resolution='i')

m.drawcountries(zorder=10)
  
plot_discrete_field_on_map(LU_INDEX, lon_plot, lat_plot, m, values, rgb_igbp)

plot_Berlin_shape(m, plt, fill=False, linewidth=1.0, color='k')

bb = ax1.get_position() # get Bbox from ax1
values_bb = bb.get_points()
x0,y0 = m(lon_plot.min(),lat_plot.min())
x1,y1 = m(lon_plot.max(),lat_plot.max())
dx_data = abs(x1 - x0)
dy_data = abs(y1 - y0)
dy_data_dx_data = dy_data / dx_data
dx_fig = abs(values_bb[1,0]-values_bb[0,0])
dy_fig = abs(values_bb[1,1]-values_bb[0,1])
dy_fig_dx_fig = dy_fig/dx_fig
if(dy_data_dx_data < dy_fig_dx_fig):
  middle_y_fig = values_bb[0,1] + 0.5 * dy_fig
  dy_new = dy_fig * (dy_data_dx_data / dy_fig_dx_fig)
  dy_start_new = middle_y_fig - 0.5 * dy_new
  ax2 = fig.add_axes([0.83, dy_start_new+0.1, 0.05, dy_new-0.1])
else:
  ax2 = fig.add_axes([0.83, values_bb[0,1], 0.05, dy_fig])
  #ax2 = fig.add_axes([0.83, 0.1, 0.05, dy_fig-0.1])


cmap = mpl.colors.ListedColormap(rgb_igbp)
bounds = np.arange(n_values+1)+0.5
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
cb1 = mpl.colorbar.ColorbarBase(ax2, cmap=cmap, norm=norm,
                                spacing='proportional', ticks=values, boundaries=bounds, orientation='vertical')
cb1.set_ticks(values)
cb1.set_ticklabels(classes_igbp)

#for i in range(21, 26):
#  i_test = np.where(LU_INDEX == i)
#  n_test = len(i_test[0])
#  print("N_",i,": ", n_test)

#cb1 = mpl.colorbar.ColorbarBase(ax2, cmap=cmap, norm=norm,
#                                spacing='proportional', orientation='vertical')
                                
#cb1 = mpl.colorbar.ColorbarBase(ax2, cmap=cmap,
#                                norm=norm,
#                                orientation='vertical')

cb1.set_label('LU class')

  

filename_plot = "/scratch/ws/0/barfus-WRF4.3/WPS-4.3/20091008/LU_INDEX.png"
plt.savefig(filename_plot, dpi=300, bbox_inches='tight')
plt.close()

