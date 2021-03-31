#       calculates the distance of two points defined by latitude and longitude applying the so-called Haversine formula
#       described in R. W. Sinnott, "Virtues of the Haversine," Sky and Telescope, vol. 68, no. 2, 1984, p. 159
#       assumes a sphere and so does not take into the oblatness of the earth
#       radius of the earth is assumed as 6371 km

import math

def distance_between_two_points(lon1, lat1, lon2, lat2):
  R = 6371.0 # radius of the earth in km
  dLat = lat2-lat1
  dLat_rad = dLat * math.pi / 180.0
  dLon = lon2-lon1
  dLon_rad = dLon * math.pi / 180.0
  lat1_rad = lat1 * math.pi / 180.0
  lat2_rad = lat2 * math.pi / 180.0

  a = math.sin(dLat_rad/2.0) * math.sin(dLat_rad/2.0) + math.sin(dLon_rad/2.0) * math.sin(dLon_rad/2.0) * math.cos(lat1_rad) * math.cos(lat2_rad)
  c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0-a))
  d = R * c

  return d
