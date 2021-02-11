module mod_thermodynamic_routines
! some thermodynamic routines

contains

real function calc_dtdp_dry(T,p)
implicit none
real, intent(in):: T ! temperature [K]
real, intent(in):: p ! pressure [hPa]
! output is:
! [K/hPa]    

real, parameter:: R0 = 287.058 ! gas constant for dry air [J * kg**-1 * K**-1]
real:: cp0, dtdp

cp0 = specific_heat_dry_air(T)  
dtdp = (T*R0)/(p*cp0)
calc_dtdp_dry = dtdp

end function
  
real function calc_dtdp_wet(T, p, rF)
implicit none 
! not applying mixed-phase model !
real, intent(in):: T  ! temperature [K]
real, intent(in):: p  ! pressure [hPa]
real, intent(in), optional:: rF ! liquid mixing ratio [kg/kg]
! rF is liquid mixing ratio <- here 0.0 because of an irreversible process
! output is:
! [K/hPa]    
real, parameter::  R0 = 287.058 ! gas constant for dry air [J * kg**-1 * K**-1]
real, parameter::  R1 = 461.5   ! gas constant for water vapour [J * kg**-1 * K**-1]
real:: pF1, p0m, rF1, lF1, LLF1
real:: cp0, cp1, cp2, Cp, v, dtdp, p0

pF1 = saturation_vapour_pressure(T) ! hPa
p0 = p - pF1                      ! hPa
rF1 = calc_rF1(pF1,p0)  ! saturation mixing ratio in g/g
lF1 = latent_heat_gas_to_liquid(T) ! J/kg
LLF1 = pF1 * lF1                   ! hPa * (J/kg)
cp0 = specific_heat_dry_air(T)     ! J/(kg*K)
cp1 = specific_heat_water_vapour(T)  ! J/(kg*K)
cp2 = specific_heat_liquid_water(T)  ! J/(kg*K)
Cp = cp0 + cp1 * rF1 + cp2 * rF      ! J/(kg*K)
v = (rF1 * lF1)/pF1 * (1.0 + (R1/R0)*rF1) * (LLF1/(R1*T**2.0))
dtdp = ((rF1*R1*T/pF1) * (1.0 + (rF1*lF1/(R0*T))))/(Cp + v)
calc_dtdp_wet = dtdp

end function


real function calc_rF1(pF1,p0)  ! Frueh and Wirth, Eq. 4
implicit none

real, intent(in):: pF1  ! saturation vapour pressure [hPa]
real, intent(in):: p0   ! partial pressure of dry air [hPa]  

real, parameter:: R0 = 287.058 ! gas constant for dry air [J * kg**-1 * K**-1]
real, parameter:: R1 = 461.5   ! gas constant for water vapour [J * kg**-1 * K**-1]

real:: res 

res = (R0 * pF1) / (R1 * p0)
calc_rF1 = res

end function  

real function saturation_vapour_pressure(T,ice_in)
implicit none
! calculates the saturation vapour pressure in hPa using the Clausius-Claperon equation
real, intent(in):: T ! temperature in [K]
logical, intent(in), optional:: ice_in
 
! keyword ice, indicates if even in case of temperatures lower than 273.15 K es is calculated with
! respect to liquid water (then ice must not been set)
! output is in hPa
! written by K.Barfus 12/2009

logical:: ice

real, parameter:: e0 = 0.611 ! [kPa]
real, parameter:: T0 = 273.15 ! [K]
real, parameter:: Rv = 461.0 ! [J K**-1 kg**-1] gas constant for water vapour
real:: L, es

if(present(ice_in))then
  ice = ice_in
 else
  ice = .false.
endif

if(ice.eqv.(.true.))then
  if(T.gt.273.15)then  ! water
    L = 2.5 * 10.0**6.0 ! J kg**-1
   else
    L = 2.83 * 10.0**6.0  ! J kg**-1
  endif
 else
  L = 2.5 * 10.0**6.0 ! J kg**-1
endif

if(T.gt.0)then 
  es = e0 * exp((L/Rv)*(1.0/T0-1.0/T))
  es = es * 10.0
 else
  es = 0.0
endif

saturation_vapour_pressure = es

end function

real function latent_heat_gas_to_liquid(T)
implicit none
! latent heat of condensation due to Rogers and Yau in J/kg
! valid for 248.15 K < T < 313.15 K
real, intent(in)::   T  ! temperature in [K]

real:: T_temp, latent_heat, res

T_temp = T - 273.15
latent_heat = 2500.8 - 2.36 * T_temp + 0.0016 * T_temp**2.0 - 0.00006 * T_temp**3.0
res = latent_heat * 1000.0
latent_heat_gas_to_liquid = res
  
! alternative approach
! calculates the latent heat of condensation (gas -> liquid) due to
! Fleagle, R.G. and J.A. Businger, (1980)
! An Introduction to Atmospheric Physics.  2d ed.  Academic Press, 432 pp.
! input
! T in K
! output in J kg^-1 K^-1
! t_temp = T - 273.15
! Lv = (25.00 - 0.02274 * t_temp) * 10.0^5.0
  
end function

real function potential_temperature(t,p)
implicit none
! calculates the potential temperature
real, intent(in):: t  ! input is temperature [K]
real, intent(in):: p  ! pressure [hPa] 

real, parameter:: p0 = 1000.0
real:: theta

theta = t * (p0/p)**(2.0/7.0)
potential_temperature = theta

end function


real function specific_heat_dry_air(T)
implicit none
! source is unknown
real, intent(in):: T  ![K]
! T should be: -40°C < T < 40^C
! output is in [J kg^-1 C^-1]

real:: t_temp, C_pd

t_temp = T - 273.15
C_pd = 1005.60 + 0.017211 * t_temp + 0.000392 * t_temp**2.0
specific_heat_dry_air = C_pd

end function

real function specific_heat_water_vapour(T)
implicit none
! Reid, R.C., J.M. Prausnitz, and B.E. Poling (1987)
! The Properties of Gases and Liquids.  4th ed.  McGraw-Hill, 741 pp.
real, intent(in):: T ! temperature [K]
! output is in J kg^-1 K^-1

real:: t_temp, c_pv

t_temp = T - 273.15
c_pv = 1858.0 + 3.820 * 10.0**(-1.0) * t_temp + 4.220 * 10.0**(-4.0) * t_temp**2.0 - &
   1.996 * 10.0**(-7.0) * T**3.0
specific_heat_water_vapour = c_pv

end function 
  
real function specific_heat_liquid_water(T)
implicit none
real, intent(in)::  T  ! temperature [K]
! output is in J kg^-1 K^-1

real:: t_temp, c_pw

t_temp = T - 273.15
c_pw =  4217.4 - 3.720283 * t_temp +0.1412855 * t_temp**2.0 - 2.654387 * 10.0**(-3.0) * t_temp**3.0 &
       + 2.093236 * 10.0**(-5.0) * t_temp**(4.0)
specific_heat_liquid_water = c_pw 

end function
  
real function spec_hum_from_dewpoint(dewpoint, pressure)
implicit none 
! calculate specific humidity from dewpoint temperature and pressure
! based on Stull: Meteorology for Scientists and Engineers.
! written by K.Barfus 2/2019
real, intent(in):: dewpoint ![K]
real, intent(in):: pressure ![hPa]
! returns specific humidity in [g/g]                                                                                                                                                                      
real:: pressure_kPa, epsilon, T0, e0, Rv_Lv, e, specific_humidity

pressure_kPa = pressure / 10.0 ! hPa -> kPa
epsilon = 0.622 ![g/g]
T0 = 273.15 ![K]
e0 = 0.6114 ![kPa]
Rv_Lv = 1.844 * 10.0**(-4) ! [K**-1]
e = exp((dewpoint/T0-1.0)/(dewpoint*Rv_Lv)+log(e0))
specific_humidity = (epsilon*e) / (pressure-e *(1.0-epsilon))
spec_hum_from_dewpoint = specific_humidity
  
end function

real function dewpoint_from_spec_hum(spec_hum,p)
implicit none
! calculates Dewpoint temperature from specific humidity and pressure
real, intent(in):: spec_hum  ! specific humidity [g/g]
real, intent(in):: p ! pressure [hPa]
! output is:
! dewpoint temperature [K] 

real, parameter:: Rd = 287.058 ! gas constant for dry air [J * kg**-1 * K**-1] 
real, parameter:: Rv = 461.5   ! gas constant for water vapour [J * kg**-1 * K**-1]

real:: p_kPa, epsilon, e, T0, RvLv, e0, Td

p_kPa = p / 10.0 ! hPa -> kPa

epsilon = Rd/Rv
e = (spec_hum * (p + epsilon)) / (epsilon + spec_hum)  ! vapor pressure in [kPa] 
T0 = 273.15 ! [K]
RvLv = 1.844*10**(-4) ! [K**-1]
e0 = 0.6113 ! [kPa]
Td = (1.0/T0 - RvLv * log(e/e0))**(-1.0)
dewpoint_from_spec_hum = Td

end function
  
real function rel_hum_from_spec_hum(q, p, t)
implicit none
! derives vapour pressure from specific humidity 
! equation derived from Stull: Meteorology for Scientists and Engineers
real, intent(in):: q ! specific humidity [g_water_vapour / g_total]
real, intent(in):: p ! pressure in hPa
real, intent(in):: t ! temperatue [K]
! output is relative humidity [%]

real, parameter:: epsilon = 0.622 ![g/g]

real:: es, qs, RH

es = saturation_vapour_pressure(t)
qs = (epsilon * es) / (p- es * (1.0-epsilon))
RH = (q / qs) * 100.0
if(RH.gt.100.0)then
  RH = 100.0
endif 

rel_hum_from_spec_hum = RH

end function

real function spec_hum_from_rel_hum(T,Pressure,RH)
implicit none
! derives the specific humidity from relative humidity
! equation derived from Stull: Meteorology for Scientists and Engineers
real, intent(in):: T ! temperature in K
real, intent(in):: Pressure ! Pressure in hPa
real, intent(in):: RH  ! relative humidity [%]

real, parameter::  eta = 0.622
  
real:: es, qs, q

es = saturation_vapour_pressure(T)
qs = (eta * es) / (Pressure - es * (1.0 - eta))
q = (RH / 100.0) * qs
  
spec_hum_from_rel_hum =  q
end function
  
real function spec_hum_from_mixing_ratio(r, p)
implicit none
! derives specific humidity from mixing ratio
! equation derived from Stull: Meteorology for Scientists and Engineers
real, intent(in):: r ! mixing ratio [g_water_vapour / g_dry]    
real, intent(in):: p ! pressure in hPa
! output is specific humidity in [g/g]

real, parameter:: epsilon = 0.622 ![g/g]
real:: e, q

e = (r*p)/(epsilon+r) 
q = (epsilon*e)/(p-e*(1.0-epsilon))
spec_hum_from_mixing_ratio = q

end function

real function mixing_ratio_from_spec_hum(q,p)
implicit none
! derives vapour pressure from specific humidity
! equation derived from Stull: Meteorology for Scientists and Engineers    
real, intent(in):: q ! specific humidity [g_water_vapour / g_total]    
real, intent(in)::  p ! pressure in hPa
! output is mixing ration in [g/g]

real:: e, epsilon, r
  
e = vap_press_from_spec_hum(q,p)
epsilon = 0.622 ! [g/g]
r = (epsilon*e)/(p-e)
mixing_ratio_from_spec_hum = r  

end function

real function vap_press_from_spec_hum(q,p)
implicit none
! derives vapour pressure from specific humidity
! equation derived from Stull: Meteorology for Scientists and Engineers  
real, intent(in):: q  ! specific humidity [g_water_vapour / g_total]    
real, intent(in):: p  ! pressure in hPa
! output is vapour pressure in [hPa]

real, parameter::  epsilon = 0.622 ![g/g]  
real:: e

e = (q*p) / (epsilon - q*(1.0 - epsilon))

vap_press_from_spec_hum = e

end function 

end module
