# reads dataset from a WRF intermediate file
# into a list
# written by K.Barfus 31.07.2015
import struct
import numpy as np
import array
import os

class dataset:
  ifv = 0.0
  hdate = ''
  xfcst = 0.0
  map_source = ''
  field = ''
  units_string = ''
  desc = ''
  xlvl = 0.0
  nx = 0
  ny = 0
  iproj = 0
  startloc = ''
  startlat = 0.0
  startlon = 0.0
  deltalat = 0.0
  deltalon = 0.0
  earth_radius = 0.0
  dx = 0.0
  dy = 0.0
  truelat1 = 0.0
  truelat2 = 0.0
  xlonc = 0.0
  nlats = 0.0
  is_wind_earth_rel = None
  slab = None
  
def print_dataset(res):
  print('ifv: ', res.ifv)
  print('hdate: ', res.hdate)
  print('xfcst: ', res.xfcst)
  print('map_source: ', res.map_source)
  print('field: ', res.field)
  print(' units_string: ', res.units_string)
  print(' desc: ', res.desc)
  print(' xlvl: ', res.xlvl)
  print(' nx: ', res.nx)
  print(' ny: ', res.ny)
  print(' iproj: ', res.iproj)
  print(' startloc: ', res.startloc)
  print(' startlat: ', res.startlat)
  print(' startlon: ', res.startlon)
  print(' deltalat: ', res.deltalat)
  print(' deltalon: ', res.deltalon)
  print(' earth_radius: ', res.earth_radius)
  print(' dx: ', res.dx)
  print(' dy: ', res.dy)
  print(' truelat1: ', res.truelat1)
  print(' truelat2: ', res.truelat2)
  print(' xlonc: ', res.xlonc)
  print(' nlats: ', res.nlats)
  print(' is_wind_earth_rel: ', res.is_wind_earth_rel)
  print(' slab: ', res.slab)


def read_dataset(f):
  d = dataset()
  recl=struct.unpack('>i',f.read(4))[0]
  d.ifv = struct.unpack('>i',f.read(recl))[0]
  recl_close=struct.unpack('>i',f.read(4))[0] # record closing bytes
  recl=struct.unpack('>i',f.read(4))[0]
  record2= struct.unpack(str(recl)+'s',f.read(recl))[0]
  d.hdate = record2[0:24].decode('UTF8')
  d.xfcst = struct.unpack('>f', record2[24:28])[0]
  d.map_source = record2[28:60].decode('UTF8')
  d.field = record2[60:69].decode('UTF8')
  d.units_string = record2[69:94].decode('UTF8')
  d.desc = record2[94:140].decode('UTF8')
  d.xlvl = struct.unpack('>f', record2[140:144])[0]
  d.nx = struct.unpack('>i', record2[144:148])[0]
  d.ny = struct.unpack('>i', record2[148:152])[0]
  d.iproj = struct.unpack('>i', record2[152:156])[0]
  recl_close=struct.unpack('>i',f.read(4))[0] # record closing bytes
  recl=struct.unpack('>i',f.read(4))[0]
  record3= struct.unpack(str(recl)+'s',f.read(recl))[0]
  d.startloc = record3[0:8].decode('UTF8')
  if(d.iproj == 0): # Cylindrical equidistant projection
    d.startlat = struct.unpack('>f', record3[8:12])[0]
    d.startlon = struct.unpack('>f', record3[12:16])[0]
    d.deltalat = struct.unpack('>f', record3[16:20])[0]
    d.deltalon = struct.unpack('>f', record3[20:24])[0]
    d.earth_radius = struct.unpack('>f', record3[24:28])[0]
  if(d.iproj == 1): # Mercator projection
    d.startlat = struct.unpack('>f', record3[8:12])[0]
    d.startlon = struct.unpack('>f', record3[12:16])[0]
    d.dx = struct.unpack('>f', record3[16:20])[0]
    d.dy = struct.unpack('>f', record3[20:24])[0]
    d.truelat1 = struct.unpack('>f', record3[24:28])[0]
    d.earth_radius = struct.unpack('>f', record3[28:32])[0]
  if(d.iproj == 3): # Lambert conformal projection
    d.startlat = struct.unpack('>f', record3[8:12])[0]
    d.startlon = struct.unpack('>f', record3[12:16])[0]
    d.dx = struct.unpack('>f', record3[16:20])[0]
    d.dy = struct.unpack('>f', record3[20:24])[0]
    d.xlonc = struct.unpack('>f', record3[24:28])[0]
    d.truelat1 = struct.unpack('>f', record3[28:32])[0]
    d.truelat2 = struct.unpack('>f', record3[32:36])[0]
    d.earth_radius = struct.unpack('>f', record3[36:40])[0]
  if(d.iproj == 4): # Gaussian projection
    d.startlat = struct.unpack('>f', record3[8:12])[0]
    d.startlon = struct.unpack('>f', record3[12:16])[0]
    d.nlats = struct.unpack('>f', record3[16:20])[0]
    d.deltalon = struct.unpack('>f', record3[20:24])[0]
    d.earth_radius = struct.unpack('>f', record3[24:28])[0]
  if(d.iproj == 5): # Polar-stereographic projection
    d.startlat = struct.unpack('>f', record3[8:12])[0]
    d.startlon = struct.unpack('>f', record3[12:16])[0]
    d.dx = struct.unpack('>f', record3[16:20])[0]
    d.dy = struct.unpack('>f', record3[20:24])[0]
    d.xlonc = struct.unpack('>f', record3[24:28])[0]
    d.truelat1 = struct.unpack('>f', record3[28:32])[0]
    d.earth_radius = struct.unpack('>f', record3[32:36])[0]
  recl_close=struct.unpack('>i',f.read(4))[0] # record closing bytes
  recl=struct.unpack('>i',f.read(4))[0]
  record4= struct.unpack(str(recl)+'s',f.read(recl))[0]
  d.is_wind_earth_rel = struct.unpack('>i', record4[0:4])[0]
  recl_close=struct.unpack('>l',f.read(4))[0] # record closing bytes
  # record 5
  recl=struct.unpack('>i',f.read(4))[0]
  record5 = struct.unpack(str(recl)+'s', f.read(recl))[0]
  slab = np.frombuffer(record5, dtype='>f')
  d.slab = slab.reshape(d.nx,d.ny)
  recl=struct.unpack('>i',f.read(4))[0]
  return d


def write_dataset(g, d):
  # record1
  g.write(struct.pack('>i', 4)) # record opening bytes
  g.write(struct.pack('>i', d.ifv))
  g.write(struct.pack('>i', 4)) # record closing bytes
  # record2
  g.write(struct.pack('>i', 156)) # record opening bytes
  g.write(struct.pack('24s', bytes(d.hdate, 'utf-8')))
  g.write(struct.pack('>f', d.xfcst))
  g.write(struct.pack('32s', bytes(d.map_source, 'utf-8')))
  g.write(struct.pack('9s', bytes(d.field, 'utf-8')))
  g.write(struct.pack('25s', bytes(d.units_string, 'utf-8')))
  g.write(struct.pack('46s', bytes(d.desc, 'utf-8')))
  g.write(struct.pack('>f', d.xlvl))
  g.write(struct.pack('>i', d.nx))
  g.write(struct.pack('>i', d.ny))
  g.write(struct.pack('>i', d.iproj))
  g.write(struct.pack('>i', 156)) # record closing bytes
  # record3
  if(d.iproj == 0): # Cylindrical equidistant projection
    g.write(struct.pack('>i', 28)) # record opening bytes
    g.write(struct.pack('8s', bytes(d.startloc, 'utf-8')))
    g.write(struct.pack('>f', d.startlat))
    g.write(struct.pack('>f', d.startlon))
    g.write(struct.pack('>f', d.deltalat))
    g.write(struct.pack('>f', d.deltalon))
    g.write(struct.pack('>f', d.earth_radius))
    g.write(struct.pack('>i', 28)) # record closing bytes
  if(d.iproj == 1): # Mercator projection
    g.write(struct.pack('>i', 32)) # record opening bytes
    g.write(struct.pack('8s', bytes(d.startloc, 'utf-8')))
    g.write(struct.pack('>f', d.startlat))
    g.write(struct.pack('>f', d.startlon))
    g.write(struct.pack('>f', d.dx))
    g.write(struct.pack('>f', d.dy))
    g.write(struct.pack('>f', d.truelat1))
    g.write(struct.pack('>f', d.earth_radius))
    g.write(struct.pack('>i', 32)) # record closing bytes
  if(d.iproj == 3): # Lambert conformal projection
    g.write(struct.pack('>i', 40)) # record opening bytes
    g.write(struct.pack('8s', bytes(d.startloc, 'utf-8')))
    print("output_test")
    print(d.startloc) 
    g.write(struct.pack('>f', d.startlat))
    print(d.startlat)
    g.write(struct.pack('>f', d.startlon))
    print(d.startlon)
    g.write(struct.pack('>f', d.dx))
    print(d.dx)
    g.write(struct.pack('>f', d.dy))
    print(d.dy)
    g.write(struct.pack('>f', d.xlonc))
    g.write(struct.pack('>f', d.truelat1))
    print(d.truelat1)
    g.write(struct.pack('>f', d.truelat2))
    print(d.truelat2)
    g.write(struct.pack('>f', d.earth_radius))
    print(d.earth_radius)
    g.write(struct.pack('>i', 40)) # record closing bytes
  if(d.iproj == 4): # Gaussian projection
    g.write(struct.pack('>i', 28)) # record opening bytes
    g.write(struct.pack('8s', bytes(d.startloc, 'utf-8')))
    g.write(struct.pack('>f', d.startlat))
    g.write(struct.pack('>f', d.startlon))
    g.write(struct.pack('>f', d.nlats))
    g.write(struct.pack('>f', d.deltalon))
    g.write(struct.pack('>f', d.earth_radius))
    g.write(struct.pack('>i', 28)) # record closing bytes
  if(d.iproj == 5): # Polar-stereographic projection
    g.write(struct.pack('>i', 36)) # record opening bytes
    g.write(struct.pack('8s', bytes(d.startloc, 'utf-8')))
    g.write(struct.pack('>f', d.startlat))
    g.write(struct.pack('>f', d.startlon))
    g.write(struct.pack('>f', d.dx))
    g.write(struct.pack('>f', d.dy))
    g.write(struct.pack('>f', d.xlonc))
    g.write(struct.pack('>f', d.truelat1))
    g.write(struct.pack('>f', d.earth_radius))
    g.write(struct.pack('>i', 36)) # record closing bytes
  # record4
  g.write(struct.pack('>i', 4)) # record opening bytes
  g.write(struct.pack('>i', d.is_wind_earth_rel))
  g.write(struct.pack('>i', 4)) # record closing bytes
  # record 5
  recl = d.nx*d.ny*4
  g.write(struct.pack('>i', recl)) # record opening bytes
  slab_temp = d.slab.astype('>f')
  g.write(slab_temp.tobytes(order='F'))
  g.write(struct.pack('>i', recl)) # record closing bytes


