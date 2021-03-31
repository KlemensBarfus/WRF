# calculates the midpoint between two geographical points
# due to http://www.movable-type.co.uk/scripts/latlong.html
# written by K. Barfus 3/2015

import math

def half_way_point_great_circle(lon1, lat1, lon2, lat2):
  radius = 6371.0 # [km] radius of the eerth in km
  rad = math.pi/180.0
  deg = 180.0/math.pi
  lon1_rad = lon1 * rad
  lat1_rad = lat1 * rad
  lon2_rad = lon2 * rad
  lat2_rad = lat2 * rad
  Bx = math.cos(lat2_rad) * math.cos(lon2_rad - lon1_rad)
  By = math.cos(lat2_rad) * math.sin(lon2_rad - lon1_rad) 
  lat_m_rad = math.atan2(math.sin(lat1_rad) + math.sin(lat2_rad), math.sqrt(math.cos(lat1_rad) + Bx)**2.0 + By**2.0)
  lon_m_rad = lon1_rad + math.atan2(By, math.cos(lat1_rad)+Bx)
  lat_m_deg = lat_m_rad * deg
  lon_m_deg = lon_m_rad * deg
  res = {'lon': lon_m_deg, 'lat': lat_m_deg}
  return res

