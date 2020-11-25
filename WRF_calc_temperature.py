def WRF_calc_temperature(theta,P):
 # calculates temperature in [K]
 # input is in destaggered arrays [n_times, nz, ny, nx] 
 # theta: potential temperature [K] (WRF variable "T"+300.0)
 # P Pressure in [Pa] (WRF variable "P"? + PHB")

 Rd_Cp   = 0.28571 #(dimensionless)
 T =  theta*((P/100000. )**(Rd_Cp)) 
 return T



