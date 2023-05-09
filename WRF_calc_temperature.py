def WRF_calc_temperature(theta,P):
  # calculates temperature in [K]
  # input is in destaggered arrays [n_times, nz, ny, nx] 
  # theta: potential temperature [K] (WRF variable "T"+300.0)
  # P Pressure in [Pa] (WRF variable "P"? + PHB")

  theta = np.asarray(theta)
  P = np.asarray(P)
  scalarinput = False
  if theta.ndim == 0:
    theta = theta[None]  # Makes x 1D
    P = P[None]
    scalarinput = True

    Rd_Cp   = 0.28571 #(dimensionless)
    T =  theta*((P/100000. )**(Rd_Cp))

    if scalar_input:
      return np.squeeze(T)
    return T




