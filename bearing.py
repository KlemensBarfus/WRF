# calculates the initial bearing due to the formula given in
# http://www.movable-type.co.uk/scripts/latlong.html
# written by K.Barfus 4/2016
# θ = atan2( sin Δλ ⋅ cos φ2 , cos φ1 ⋅ sin φ2 − sin φ1 ⋅ cos φ2 ⋅ cos Δλ )

import math

def bearing(lon1, lat1, lon2, lat2):
  radius = 6371.0 # [km] radius of the eerth in km
  rad = math.pi/180.0
  deg = 180.0/math.pi
  lon1_rad = lon1 * rad
  lat1_rad = lat1 * rad
  lon2_rad = lon2 * rad
  lat2_rad = lat2 * rad
  delta_lon = lon2 - lon1
  delta_lon_rad = delta_lon * rad

  bearing_rad = math.atan2(math.sin(delta_lon_rad) * math.cos(lat2_rad), math.cos(lat1_rad) * math.sin(lat2_rad) - math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(delta_lon_rad))
  bearing_deg = bearing_rad * deg

  return bearing_deg
