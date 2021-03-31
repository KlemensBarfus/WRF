# gets the coordinates for plotting longitude and latitude from an arbitrary grid of latitudes and longitudes
# like it is provides by WRF (rotated etc.)
# assumes extrapolation at the boundaries
# assumes [n_lon,n_lat] ordering of the grids but not an increases of lon / lat in predefined direction
# written by K. Barfus 29.4.2015

import numpy as np
from half_way_point_great_circle import half_way_point_great_circle
from distance_between_two_points import distance_between_two_points
from bearing import bearing
from great_circle_waypoint import great_circle_waypoint

def WRF_get_plot_grid_for_geographical_coordinates(lat, lon):
  n_temp = lon.shape
  n_lon = n_temp[1]
  n_lat = n_temp[0]
  lon_plot = np.zeros((n_lat,n_lon,4))
  lat_plot = np.zeros((n_lat,n_lon,4))

  fac = 0.2

  bear_angle = np.zeros((n_lat,n_lon,4))
  distance = np.zeros((n_lat,n_lon,4))
   
  for i_lon in range(0, n_lon):
    for i_lat in range(0, n_lat):
      # lower left point
      if((i_lon > 0) and (i_lon <= n_lon-1)):
        if((i_lat > 0) and (i_lat <= n_lat-1)):
          res = half_way_point_great_circle(lon[i_lat-1,i_lon-1], lat[i_lat-1,i_lon-1], lon[i_lat,i_lon], lat[i_lat,i_lon])
          distance[i_lat,i_lon,0] = distance_between_two_points(lon[i_lat,i_lon], lat[i_lat,i_lon],res['lon'], res['lat'])
          bear_angle[i_lat,i_lon,0] = bearing(lon[i_lat,i_lon], lat[i_lat,i_lon], res['lon'], res['lat'])
          res = great_circle_waypoint(lon[i_lat,i_lon], lat[i_lat,i_lon], bear_angle[i_lat,i_lon,0], (1.0+fac)*distance[i_lat,i_lon,0])
          lon_plot[i_lat,i_lon,0] = res['lon']
          lat_plot[i_lat,i_lon,0] = res['lat']
      if(i_lon == 0): 
        if(i_lat < n_lat-1):
          res = half_way_point_great_circle(lon[i_lat,i_lon], lat[i_lat,i_lon], lon[i_lat+1,i_lon+1], lat[i_lat+1,i_lon+1])
          distance[i_lat,i_lon,0] = distance_between_two_points(lon[i_lat,i_lon], lat[i_lat,i_lon],res['lon'], res['lat'])
          bear_angle[i_lat,i_lon,0] = bearing(res['lon'], res['lat'], lon[i_lat,i_lon], lat[i_lat,i_lon])
          res = great_circle_waypoint(lon[i_lat,i_lon], lat[i_lat,i_lon], bear_angle[i_lat,i_lon,0], (1.0+fac)*distance[i_lat,i_lon,0])
          lon_plot[i_lat,i_lon,0] = res['lon']
          lat_plot[i_lat,i_lon,0] = res['lat']
      if(i_lat == 0):
        if((i_lon >= 1) and (i_lon < n_lon-1)):
          res = half_way_point_great_circle(lon[i_lat,i_lon], lat[i_lat,i_lon], lon[i_lat+1,i_lon+1], lat[i_lat+1,i_lon+1])
          distance[i_lat,i_lon,0] = distance_between_two_points(lon[i_lat,i_lon], lat[i_lat,i_lon],res['lon'], res['lat'])
          bear_angle[i_lat,i_lon,0] = bearing(res['lon'], res['lat'], lon[i_lat,i_lon], lat[i_lat,i_lon])
          res = great_circle_waypoint(lon[i_lat,i_lon], lat[i_lat,i_lon], bear_angle[i_lat,i_lon,0], (1.0+fac)*distance[i_lat,i_lon,0])
          lon_plot[i_lat,i_lon,0] = res['lon']
          lat_plot[i_lat,i_lon,0] = res['lat']
      # lower right point
      if((i_lon >= 0) and (i_lon < n_lon-1)):
        if((i_lat > 0) and (i_lat <= n_lat-1)):
          res = half_way_point_great_circle(lon[i_lat,i_lon], lat[i_lat,i_lon], lon[i_lat-1,i_lon+1], lat[i_lat-1,i_lon+1])
          distance[i_lat,i_lon,1] = distance_between_two_points(lon[i_lat,i_lon], lat[i_lat,i_lon],res['lon'], res['lat'])
          bear_angle[i_lat,i_lon,1] = bearing(lon[i_lat,i_lon], lat[i_lat,i_lon], res['lon'], res['lat'])
          res = great_circle_waypoint(lon[i_lat,i_lon], lat[i_lat,i_lon], bear_angle[i_lat,i_lon,1], (1.0+fac)*distance[i_lat,i_lon,1])
          lon_plot[i_lat,i_lon,1] = res['lon']
          lat_plot[i_lat,i_lon,1] = res['lat']
      if(i_lat == 0):
        if(i_lon > 0):
          res = half_way_point_great_circle(lon[i_lat,i_lon], lat[i_lat,i_lon], lon[i_lat+1,i_lon-1], lat[i_lat+1,i_lon-1])
          distance[i_lat,i_lon,1] = distance_between_two_points(lon[i_lat,i_lon], lat[i_lat,i_lon],res['lon'], res['lat'])
          bear_angle[i_lat,i_lon,1] = bearing(res['lon'], res['lat'], lon[i_lat,i_lon], lat[i_lat,i_lon])
          res = great_circle_waypoint(lon[i_lat,i_lon], lat[i_lat,i_lon], bear_angle[i_lat,i_lon,1], (1.0+fac)*distance[i_lat,i_lon,1])
          lon_plot[i_lat,i_lon,1] = res['lon']
          lat_plot[i_lat,i_lon,1] = res['lat']
      if(i_lon == n_lon-1):
        if((i_lat >= 1) and (i_lat < n_lat-1)):
          res = half_way_point_great_circle(lon[i_lat,i_lon], lat[i_lat,i_lon], lon[i_lat+1,i_lon-1], lat[i_lat+1,i_lon-1])
          distance[i_lat,i_lon,1] = distance_between_two_points(lon[i_lat,i_lon], lat[i_lat,i_lon],res['lon'], res['lat'])
          bear_angle[i_lat,i_lon,1] = bearing(res['lon'], res['lat'], lon[i_lat,i_lon], lat[i_lat,i_lon])
          res = great_circle_waypoint(lon[i_lat,i_lon], lat[i_lat,i_lon], bear_angle[i_lat,i_lon,1], (1.0+fac)*distance[i_lat,i_lon,1])
          lon_plot[i_lat,i_lon,1] = res['lon']
          lat_plot[i_lat,i_lon,1] = res['lat']
      # upper right
      if((i_lon >= 0) and (i_lon < n_lon-1)):
        if((i_lat >= 0) and (i_lat < n_lat-1)):
          res = half_way_point_great_circle(lon[i_lat,i_lon], lat[i_lat,i_lon], lon[i_lat+1,i_lon+1], lat[i_lat+1,i_lon+1])
          distance[i_lat,i_lon,2] = distance_between_two_points(lon[i_lat,i_lon], lat[i_lat,i_lon],res['lon'], res['lat'])
          bear_angle[i_lat,i_lon,2] = bearing(lon[i_lat,i_lon], lat[i_lat,i_lon], res['lon'], res['lat'])
          res = great_circle_waypoint(lon[i_lat,i_lon], lat[i_lat,i_lon], bear_angle[i_lat,i_lon,2], (1.0+fac)*distance[i_lat,i_lon,2])
          lon_plot[i_lat,i_lon,2] = res['lon']
          lat_plot[i_lat,i_lon,2] = res['lat']
      if(i_lat == n_lat-1):
        if(i_lon > 0):
          res = half_way_point_great_circle(lon[i_lat,i_lon], lat[i_lat,i_lon], lon[i_lat-1,i_lon-1], lat[i_lat-1,i_lon-1])
          distance[i_lat,i_lon,2] = distance_between_two_points(lon[i_lat,i_lon], lat[i_lat,i_lon],res['lon'], res['lat'])
          bear_angle[i_lat,i_lon,2] = bearing(res['lon'], res['lat'], lon[i_lat,i_lon], lat[i_lat,i_lon])
          res = great_circle_waypoint(lon[i_lat,i_lon], lat[i_lat,i_lon], bear_angle[i_lat,i_lon,2], (1.0+fac)*distance[i_lat,i_lon,2])
          lon_plot[i_lat,i_lon,2] = res['lon']
          lat_plot[i_lat,i_lon,2] = res['lat']
      if(i_lon == n_lon-1):
        if((i_lat >= 1) and (i_lat <= n_lat-1)):
          res = half_way_point_great_circle(lon[i_lat,i_lon], lat[i_lat,i_lon], lon[i_lat-1,i_lon-1], lat[i_lat-1,i_lon-1])
          distance[i_lat,i_lon,2] = distance_between_two_points(lon[i_lat,i_lon], lat[i_lat,i_lon],res['lon'], res['lat'])
          bear_angle[i_lat,i_lon,2] = bearing(res['lon'], res['lat'], lon[i_lat,i_lon], lat[i_lat,i_lon])
          res = great_circle_waypoint(lon[i_lat,i_lon], lat[i_lat,i_lon], bear_angle[i_lat,i_lon,2], (1.0+fac)*distance[i_lat,i_lon,2])
          lon_plot[i_lat,i_lon,2] = res['lon']
          lat_plot[i_lat,i_lon,2] = res['lat']
      # upper left
      if((i_lon >= 1) and (i_lon <= n_lon-1)):
        if((i_lat >= 0) and (i_lat < n_lat-1)):
          res = half_way_point_great_circle(lon[i_lat,i_lon], lat[i_lat,i_lon], lon[i_lat+1,i_lon-1], lat[i_lat+1,i_lon-1])
          distance[i_lat,i_lon,3] = distance_between_two_points(lon[i_lat,i_lon], lat[i_lat,i_lon],res['lon'], res['lat'])
          bear_angle[i_lat,i_lon,3] = bearing(lon[i_lat,i_lon], lat[i_lat,i_lon], res['lon'], res['lat'])
          res = great_circle_waypoint(lon[i_lat,i_lon], lat[i_lat,i_lon], bear_angle[i_lat,i_lon,3], (1.0+fac)*distance[i_lat,i_lon,3])
          lon_plot[i_lat,i_lon,3] = res['lon']
          lat_plot[i_lat,i_lon,3] = res['lat']
      if(i_lon == 0):
        if(i_lat > 0):
          res = half_way_point_great_circle(lon[i_lat,i_lon], lat[i_lat,i_lon], lon[i_lat-1,i_lon+1], lat[i_lat-1,i_lon+1])
          distance[i_lat,i_lon,3] = distance_between_two_points(lon[i_lat,i_lon], lat[i_lat,i_lon],res['lon'], res['lat'])
          bear_angle[i_lat,i_lon,3] = bearing(res['lon'], res['lat'], lon[i_lat,i_lon], lat[i_lat,i_lon])
          res = great_circle_waypoint(lon[i_lat,i_lon], lat[i_lat,i_lon], bear_angle[i_lat,i_lon,3], (1.0+fac)*distance[i_lat,i_lon,3])
          lon_plot[i_lat,i_lon,3] = res['lon']
          lat_plot[i_lat,i_lon,3] = res['lat']
      if(i_lat == n_lat-1):
        if((i_lon >= 1) and (i_lon < n_lon-1)):
          res = half_way_point_great_circle(lon[i_lat,i_lon], lat[i_lat,i_lon], lon[i_lat-1,i_lon+1], lat[i_lat-1,i_lon+1])
          distance[i_lat,i_lon,3] = distance_between_two_points(lon[i_lat,i_lon], lat[i_lat,i_lon],res['lon'], res['lat'])
          bear_angle[i_lat,i_lon,3] = bearing(res['lon'], res['lat'], lon[i_lat,i_lon], lat[i_lat,i_lon])
          res = great_circle_waypoint(lon[i_lat,i_lon], lat[i_lat,i_lon], bear_angle[i_lat,i_lon,3], (1.0+fac)*distance[i_lat,i_lon,3])
          lon_plot[i_lat,i_lon,3] = res['lon']
          lat_plot[i_lat,i_lon,3] = res['lat']



  # get lon/lat_plot[0,0]
  z = np.polyfit(lon[0,1:n_lon-1], distance[0,1:n_lon-1,1], 2)
  f = np.poly1d(z)
  distance[0,0,1] = f(lon[0,0])
  z = np.polyfit(lon[0,1:n_lon-1], bear_angle[0,1:n_lon-1,1], 2)
  f = np.poly1d(z)
  bear_angle[0,0,1] = f(lon[0,0])
  res = great_circle_waypoint(lon[0,0], lat[0,0], bear_angle[0,0,1], (1.0+fac)*distance[0,0,1])
  lon_plot[0,0,1] = res['lon']
  lat_plot[0,0,1] = res['lat']
  z = np.polyfit(lon[0,1:n_lon-1], distance[0,1:n_lon-1,3], 2)
  f = np.poly1d(z)
  distance[0,0,3] = f(lon[0,0])
  z = np.polyfit(lon[0,1:n_lon-1], bear_angle[0,1:n_lon-1,3], 2)
  f = np.poly1d(z)
  bear_angle[0,0,3] = f(lon[0,0])
  res = great_circle_waypoint(lon[0,0], lat[0,0], bear_angle[0,0,3], (1.0+fac)*distance[0,0,3])
  lon_plot[0,0,3] = res['lon']
  lat_plot[0,0,3] = res['lat']

  # get lon/lat_plot[n_lon-1,0]
  z = np.polyfit(lon[0,0:n_lon-2], distance[0,0:n_lon-2,0], 2)
  f = np.poly1d(z)
  distance[0,n_lon-1,0] = f(lon[0,n_lon-1])
  z = np.polyfit(lon[0,0:n_lon-2], bear_angle[0,0:n_lon-2,0], 2)
  f = np.poly1d(z)
  bear_angle[0,n_lon-1,0] = f(lon[0,n_lon-1])
  res = great_circle_waypoint(lon[0,n_lon-1], lat[0,n_lon-1], bear_angle[0,n_lon-1,0], (1.0+fac)*distance[0,n_lon-1,0])
  lon_plot[0,n_lon-1,0] = res['lon']
  lat_plot[0,n_lon-1,0] = res['lat']
  z = np.polyfit(lon[0,0:n_lon-2], distance[0,0:n_lon-2,2], 2)
  f = np.poly1d(z)
  distance[0,n_lon-1,2] = f(lon[0,n_lon-1])
  z = np.polyfit(lon[0,0:n_lon-2], bear_angle[0,0:n_lon-2,2], 2)
  f = np.poly1d(z)
  bear_angle[0,n_lon-1,2] = f(lon[0,n_lon-1])
  res = great_circle_waypoint(lon[0,n_lon-1], lat[0,n_lon-1], bear_angle[0,n_lon-1,2], (1.0+fac)*distance[0,n_lon-1,2])
  lon_plot[0,n_lon-1,2] = res['lon']
  lat_plot[0,n_lon-1,2] = res['lat']

  # get lon/lat_plot[n_lon-1,n_lat-1]
  z = np.polyfit(lon[n_lat-1,0:n_lon-2], distance[n_lat-1,0:n_lon-2,1], 2)
  f = np.poly1d(z)
  distance[n_lat-1,n_lon-1,1] = f(lon[n_lat-1,n_lon-1])
  z = np.polyfit(lon[n_lat-1,0:n_lon-2], bear_angle[n_lat-1,0:n_lon-2,1], 2)
  f = np.poly1d(z)
  bear_angle[n_lat-1,n_lon-1,1] = f(lon[n_lat-1,n_lon-1])
  res = great_circle_waypoint(lon[n_lat-1,n_lon-1], lat[n_lat-1,n_lon-1], bear_angle[n_lat-1,n_lon-1,1], (1.0+fac)*distance[n_lat-1,n_lon-1,1])
  lon_plot[n_lat-1,n_lon-1,1] = res['lon']
  lat_plot[n_lat-1,n_lon-1,1] = res['lat']
  z = np.polyfit(lon[n_lat-1,0:n_lon-2], distance[n_lat-1,0:n_lon-2,3], 2)
  f = np.poly1d(z)
  distance[n_lat-1,n_lon-1,3] = f(lon[n_lat-1,n_lon-1])
  z = np.polyfit(lon[n_lat-1,0:n_lon-2], bear_angle[n_lat-1,0:n_lon-2,3], 2)
  f = np.poly1d(z)
  bear_angle[n_lat-1,n_lon-1,3] = f(lon[n_lat-1,n_lon-1])
  res = great_circle_waypoint(lon[n_lat-1,n_lon-1], lat[n_lat-1,n_lon-1], bear_angle[n_lat-1,n_lon-1,3], (1.0+fac)*distance[n_lat-1,n_lon-1,3])
  lon_plot[n_lat-1,n_lon-1,3] = res['lon']
  lat_plot[n_lat-1,n_lon-1,3] = res['lat']


  # get lon/lat_plot[0,0]
  z = np.polyfit(lon[n_lat-1,1:n_lon-1], distance[n_lat-1,1:n_lon-1,0], 2)
  f = np.poly1d(z)
  distance[n_lat-1,0,0] = f(lon[n_lat-1,0])
  z = np.polyfit(lon[n_lat-1,1:n_lon-1], bear_angle[n_lat-1,1:n_lon-1,0], 2)
  f = np.poly1d(z)
  bear_angle[n_lat-1,0,0] = f(lon[n_lat-1,0])
  res = great_circle_waypoint(lon[n_lat-1,0], lat[n_lat-1,0], bear_angle[n_lat-1,0,0], (1.0+fac)*distance[n_lat-1,0,0])
  lon_plot[n_lat-1,0,0] = res['lon']
  lat_plot[n_lat-1,0,0] = res['lat']
  z = np.polyfit(lon[n_lat-1,1:n_lon-1], distance[n_lat-1,1:n_lon-1,2], 2)
  f = np.poly1d(z)
  distance[n_lat-1,0,2] = f(lon[n_lat-1,0])
  z = np.polyfit(lon[n_lat-1,1:n_lon-1], bear_angle[n_lat-1,1:n_lon-1,2], 2)
  f = np.poly1d(z)
  bear_angle[n_lat-1,0,2] = f(lon[n_lat-1,0])
  res = great_circle_waypoint(lon[n_lat-1,0], lat[n_lat-1,0], bear_angle[n_lat-1,0,2], (1.0+fac)*distance[n_lat-1,0,2])
  lon_plot[n_lat-1,0,2] = res['lon']
  lat_plot[n_lat-1,0,2] = res['lat']

  return lat_plot, lon_plot          
 

