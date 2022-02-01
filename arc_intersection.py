# https://blog.mbedded.ninja/mathematics/geometry/spherical-geometry/finding-the-intersection-of-two-arcs-that-lie-on-a-sphere/                                                                             
import numpy as np
import math

def spherical_to_xyz(lat,lon,r):
  x = np.cos(lat*(math.pi/180.0))*np.cos(lon*(math.pi/180.0)) * r
  y = np.cos(lat*(math.pi/180.0))*np.sin(lon*(math.pi/180.0)) * r
  z = np.sin(lat*(math.pi/180.0)) * r
  return x, y, z
  
def cross_product(a1,a2,a3,b1,b2,b3):
  c1 = a2*b3-a3*b2
  c2 = a3*b1-a1*b3
  c3 = a1*b2-a2*b1
  return c1, c2, c3    
    
def normalize_vector(a1,a2,a3):
  b = norm_vector(a1,a2,a3)
  a1n = a1/b
  a2n = a2/b
  a3n = a3/b
  return a1n,a2n,a3n

def norm_vector(a1,a2,a3):
  b = np.sqrt(a1**2.0+a2**2.0+a3**2.0)
  return b
  
def dot_product(a1,a2,a3,b1,b2,b3):
  res = a1*b1 + a2*b2 + a3*b3
  return res  

def angle_vector(a1,a2,a3,b1,b2,b3):
  nominator = dot_product(a1,a2,a3,b1,b2,b3)
  denominator = norm_vector(a1,a2,a3) * norm_vector(b1,b2,b3)    
  theta_rad = np.arccos(nominator/denominator)
  theta = theta_rad * (180.0/math.pi)
  return theta  
    
def xyz_to_spherical(x,y,z):
  r = np.sqrt(x**2.0+y**2.0+z**2.0)
  theta = np.arctan(y/x)
  phi = np.arctan(np.sqrt(x**2.0+y**2.0)/z)
  lon = theta * (180.0/math.pi)
  phi = phi * (180.0/math.pi)
  lat = 90.0 - phi
  return r, lat, lon

def intersection_two_arcs_on_a_sphere(lat1a,lon1a,lat1b,lon1b,lat2a,lon2a,lat2b,lon2b,radius=6371.0):
  r = radius

  x1a, y1a, z1a = spherical_to_xyz(lat1a,lon1a,r)
  x1b, y1b, z1b = spherical_to_xyz(lat1b,lon1b,r)
  x2a, y2a, z2a = spherical_to_xyz(lat2a,lon2a,r)
  x2b, y2b, z2b = spherical_to_xyz(lat2b,lon2b,r)

  n1a, n1b, n1c = cross_product(x1a,y1a,z1a,x1b,y1b,z1b)
  n2a, n2b, n2c = cross_product(x2a,y2a,z2a,x2b,y2b,z2b)
  l1a, l1b, l1c = cross_product(n1a,n1b,n1c,n2a,n2b,n2c)
  i1a, i1b, i1c =normalize_vector(l1a,l1b,l1c)
  i2a = -1.0* i1a
  i2b = -1.0* i1b
  i2c = -1.0* i1c

  theta_a1_i1 = angle_vector(x1a,y1a,z1a,i1a,i1b,i1c)
  theta_a2_i1 = angle_vector(x1b,y1b,z1b,i1a,i1b,i1c)
  theta_a1_a2 = angle_vector(x1a,y1a,z1a,x1b,y1b,z1b)
  theta_b1_i1 = angle_vector(x2a,y2a,z2a,i1a,i1b,i1c)
  theta_b2_i1 = angle_vector(x2b,y2b,z2b,i1a,i1b,i1c)
  theta_b1_b2 = angle_vector(x2a,y2a,z2a,x2b,y2b,z2b)

  found = False
  test_score = abs((theta_a1_i1 + theta_a2_i1) - theta_a1_a2)
  eps = 1.0**-10
  if(test_score < eps):
    test_score = abs((theta_b1_i1 + theta_b2_i1) - theta_b1_b2)
    if(test_score < eps):
      res1 = i1a
      res2 = i1b
      res3 = i1c
      found = True
  if(found == False):
    theta_a1_i2 = angle_vector(x1a,y1a,z1a,i2a,i2b,i2c)
    theta_a2_i2 = angle_vector(x1b,y1b,z1b,i2a,i2b,i2c)
    theta_b1_i2 = angle_vector(x2a,y2a,z2a,i2a,i2b,i2c)
    theta_b2_i2 = angle_vector(x2b,y2b,z2b,i2a,i2b,i2c)
    test_score = abs((theta_a1_i2 + theta_a2_i2) - theta_a1_a2)
    if(test_score < eps):
      test_score = abs((theta_b1_i2 + theta_b2_i2) - theta_b1_b2)
      if(test_score < eps):
        res1 = i2a
        res2 = i2b
        res3 = i2c
      
  res_radius, res_lat, res_lon = xyz_to_spherical(res1,res2,res3)
  return res_lat, res_lon
