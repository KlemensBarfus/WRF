# This algorithm returns a point that is a specified distance and bearing from the input point. 
# Inputs are 2 coordinates x1,y1, bearing (an angle) and distance (units match EARTH_RADIUS). 
# It returns coordinates x2, y2. This algorithm returns a point that is a specified distance and bearing from the input point.
#  Inputs are 2 coordinates x1,y1, 
# bearing (an angle) and distance (units match EARTH_RADIUS). It returns coordinates x2, y2. 
# http://trac.osgeo.org/openlayers/wiki/GreatCircleAlgorithms

import math

def great_circle_waypoint(lon1, lat1, bear_angle, distance):

  earth_radius = 6371.0 # [km] radius of the earth in km
  rad = math.pi/180.0
  deg = 180.0/math.pi
  lon1_rad = lon1 * rad
  lat1_rad = lat1 * rad
  bearing_rad = bear_angle * rad

  # Convert arc distance to radians
  c = distance / earth_radius

  # print('lat1_rad: ',lat1_rad,' c: ',c,' bearing_rad: ',bearing_rad,' deg: ',deg)
  lat2_deg = math.asin(math.sin(lat1_rad) * math.cos(c) + math.cos(lat1_rad) * math.sin(c) * math.cos(bearing_rad)) * deg

  a = math.sin(c) * math.sin(bearing_rad)
  b = math.cos(lat1_rad) * math.cos(c) - math.sin(lat1_rad) * math.sin(c) * math.cos(bearing_rad)

  if(b == 0.0):
    lon2_deg = lon1_deg
  else:
    lon2_deg = lon1 + math.atan(a/b) * deg

  res =  {'lon': lon2_deg, 'lat': lat2_deg}
  return res
