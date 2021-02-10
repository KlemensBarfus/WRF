# gets the wind from a WRF file at x hPa
def WRF_get_wind_at_x_hPa(file_wrf, pressure_level_hPa):
  from netCDF4 import Dataset
  import numpy as np
  from mod_vintp2p_afterburner import mod_vintp2p_afterburner
  from WRF_pressure_half_level import WRF_pressure_half_level
  from WRF_geopotential_half_and_full_levels import WRF_geopotential_half_and_full_levels
  from WRF_destagger_var import WRF_destagger_var
  from WRF_calc_temperature import WRF_calc_temperature
  # f_wrf is a file handle for the WRF file or a filename
  # pressure_level_hPa is the desired level in [hPa]

  plevo = [pressure_level_hPa * 100.0]
  plevo = np.asarray(plevo)

  if(type(file_wrf) is str):
    f_wrf = Dataset(file_wrf, "r", format="NetCDF4")
  else:
    f_wrf = file_wrf

  U_staggered = f_wrf.variables["U"][:] # (Time, bottom_top, south_north, west_east_stag)
  V_staggered = f_wrf.variables["V"][:] # (Time, bottom_top, south_north_stag, west_east)
  T = f_wrf.variables["T"][:]
  press_half_level, press = WRF_pressure_half_level(f_wrf)
  geopot_half_level, geopot = WRF_geopotential_half_and_full_levels(f_wrf)
  if(type(file_wrf) is str):
    f_wrf.close()
  
  theta = T + 300.0
  temperature = WRF_calc_temperature(theta, press)

  # destagger U and V
  uwind = WRF_destagger_var(U_staggered, 3)
  vwind = WRF_destagger_var(V_staggered, 2)

  # turn around variables (bottom_top -> top_bottom) for interpolation routine
  uwind = uwind[:,::-1,:,:]
  vwind = vwind[:,::-1,:,:]
  press_half_level = press_half_level[:,::-1,:,:]
  press = press[:,::-1,:,:]
  geopot_half_level = geopot_half_level[:,::-1,:,:]
  geopot = geopot[:,::-1,:,:]
  temperature = temperature[:,::-1,:,:]

  var = 'W'
  u_wind_x_hPa = mod_vintp2p_afterburner.vintp2p_afterburner(var,np.copy(uwind,order='F'), np.copy(plevo,order='F'), np.copy(press_half_level,order='F'), \
                              np.copy(press,order='F'), np.copy(geopot_half_level, order='F'), np.copy(geopot,order='F'), np.copy(temperature,order='F'))
  v_wind_x_hPa = mod_vintp2p_afterburner.vintp2p_afterburner(var,np.copy(vwind,order='F'), np.copy(plevo,order='F'), np.copy(press_half_level,order='F'), \
                              np.copy(press,order='F'), np.copy(geopot_half_level, order='F'), np.copy(geopot,order='F'), np.copy(temperature,order='F'))

  u_wind_x_hPa = np.squeeze(u_wind_x_hPa)
  v_wind_x_hPa = np.squeeze(v_wind_x_hPa)
  return u_wind_x_hPa, v_wind_x_hPa
