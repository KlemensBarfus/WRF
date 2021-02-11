module mod_vintp2p_afterburner
use mod_thermodynamic_routines

contains
real function extra_P(surface_geopotential, pressure_half_level, pressure_full_level, temperature)
implicit none

real, intent(in):: surface_geopotential
real, intent(in):: pressure_half_level 
real, intent(in):: pressure_full_level
real, intent(in):: temperature

real:: zlapse, PlanetGrav, PlanetRD, zrg
real:: alpha, tstar, tmsl, zprt, zprtal, slp 

zlapse = 0.0065
PlanetGrav = 9.80665
PlanetRD = 287.058
zrg = 1.0 / PlanetGrav

if((surface_geopotential.lt.0.0001).and.(surface_geopotential.gt.(-0.0001)))then
  extra_P = pressure_half_level
 else
  alpha = PlanetRD * zlapse * zrg
  tstar = (1.0 + alpha * (pressure_half_level/pressure_full_level - 1.0)) * temperature
  if(tstar.lt.255.0)then
    tstar = 0.5 * (255.0 + tstar)
  endif
  tmsl = tstar + zlapse * zrg * surface_geopotential
  if((tmsl.gt.290.5).and.(tstar.gt.290.5))then
    tstar = 0.5 * (290.5 + tstar)
    tmsl  = tstar
  endif
  if((tmsl-tstar.lt.0.000001).and.(tstar-tmsl.lt.0.000001))then
    alpha = 0.0
   else
    if((surface_geopotential.gt.0.0001).or.(surface_geopotential.lt.(-0.0001)))then
      alpha = PlanetRD * (tmsl-tstar) / surface_geopotential
    endif
  endif
  zprt   = surface_geopotential / (PlanetRD * tstar)
  zprtal = zprt * alpha
  extra_P = pressure_half_level * exp(zprt*(1.0-zprtal*(0.5-zprtal/3.0)))
endif

end function

real function extra_T(pres, halfp, fullp, geop, temp)
implicit none

real, intent(in):: pres
real, intent(in):: halfp
real, intent(in):: fullp
real, intent(in):: geop
real, intent(in):: temp

real:: PlanetGrav, PlanetRD, zlapse
real:: zrg, tstar, ztsz, z1, ztmsl, zalph, zhts, zalp 


PlanetGrav = 9.80665
PlanetRD = 287.058
zlapse = 0.0065

zrg   = 1.0 / PlanetGrav
tstar = (1.0 + zlapse * PlanetRD * zrg * (halfp/fullp - 1.0)) * temp
ztsz  = tstar
z1    = tstar + zlapse * zrg * geop
if(tstar.lt.255.0)then
  tstar = 0.5 * (255.0 + tstar)
endif
ztmsl = tstar + zlapse * zrg * geop
if((ztmsl.gt.290.5).and.(tstar.gt.290.5))then
  tstar = 0.5 * (290.5 + tstar)
  ztmsl = tstar
endif
if((ztmsl.gt.290.5).and.(tstar.le.290.5))then
  ztmsl=290.5
endif
zalph = PlanetRD*zlapse*zrg
if((ztmsl-tstar.lt.0.000001).and.(tstar-ztmsl.lt.0.000001))then
  zalph=0.0
endif
if(((ztmsl-tstar.gt.0.000001).or.(tstar-ztmsl.gt.0.000001)).and.((geop.gt.0.0001).or.(geop.lt.(-0.0001))))then
  zalph = PlanetRD*(ztmsl-tstar)/geop
endif
if(pres.le.halfp)then
  extra_T = ((halfp-pres)*temp+ (pres-fullp)*tstar)/ (halfp-fullp)
 else
  ztmsl = z1
  tstar = ztsz
  zhts  = geop * zrg
  if((zhts.gt.2000.).and.(z1.gt.298.))then
    ztmsl = 298.
    if(zhts.lt.2500.)then
      ztmsl = 0.002*((2500.-zhts)*z1+(zhts-2000.)*ztmsl)
    endif
  endif
  if((ztmsl-tstar).lt.0.000001)then
    zalph = 0.
   else
    if((geop.gt.0.0001).or.(geop.lt.(-0.0001)))then
      zalph = PlanetRD*(ztmsl-tstar)/geop
     else
      zalph = PlanetRD*zlapse*zrg
    endif
  endif
  zalp  = zalph*log(pres/halfp)
  extra_T = tstar*(1.0+zalp*(1.0+zalp*(0.5+0.16666666667*zalp)))
endif

end function

real function extra_Z(pres, halfp, fullp, geop, temp)
implicit none

real, intent(in):: pres
real, intent(in):: halfp
real, intent(in):: fullp
real, intent(in):: geop
real, intent(in):: temp

real:: PlanetGrav, PlanetRD, zlapse, ztlim
real:: zrg, alpha, tstar, tmsl, zalp, zalpal 

PlanetGrav = 9.80665
PlanetRD = 287.058
zlapse = 0.0065
ztlim = 290.5

zrg   = 1.0 / PlanetGrav
alpha = PlanetRD * zlapse * zrg
tstar = (1.0 + alpha * (halfp/fullp - 1.0)) * temp
if(tstar.lt.255.0)then
  tstar = 0.5 * (255.0 + tstar)
endif
tmsl = tstar + zlapse * zrg * geop
if((tmsl.gt.ztlim).and.(tstar.gt.ztlim))then
  tstar = 0.5 * (ztlim + tstar)
  tmsl  = tstar
endif
if((tmsl.gt.ztlim).and.(tstar.le.ztlim))then
  tmsl = ztlim
endif
if((tmsl-tstar.lt.0.000001).and.(tstar-tmsl.lt.0.000001))then
  alpha = 0.0
 else
  if((geop.gt.0.0001).or.(geop.lt.(-0.0001)))then
    alpha = PlanetRD * (tmsl-tstar) / geop
  endif
endif
zalp   = log(pres/halfp);
zalpal = zalp * alpha
!extra_Z = ((geop - PlanetRD*tstar*zalp*(1.0 + zalpal*(0.5 + zalpal/6.0)))*zrg)
! <- original afterburner equation calculating geometrical height
extra_Z = geop - PlanetRD*tstar*zalp*(1.0 + zalpal*(0.5 + zalpal/6.0))

end function

real function lin_int_p(pres, pressure1, pressure2, var1, var2)
implicit none

real, intent(in):: pres
real, intent(in):: pressure1
real, intent(in):: pressure2
real, intent(in):: var1
real, intent(in):: var2


real:: d_press, d_var, grad_var_press

d_press = pressure1 - pressure2
d_var = var1 - var2
grad_var_press = d_var / d_press
lin_int_p = var1 + (pres - pressure1) * grad_var_press

end function

real function lin_int_log_p(pres, pressure1, pressure2, var1, var2)
implicit none

real, intent(in):: pres
real, intent(in):: pressure1
real, intent(in):: pressure2
real, intent(in):: var1
real, intent(in):: var2


real:: d_press, d_var, grad_var_press  

d_press = log(pressure1) - log(pressure2)
d_var = var1 - var2
grad_var_press = d_var / d_press
lin_int_log_p = var1 + (log(pres) - log(pressure1)) * grad_var_press

end function


subroutine vintp2p_afterburner(varname, ntime, nlevel, nlat, nlon, var, npres, pres, pressure_half_level, pressure_full_level, geopotential_half_level, geopotential_full_level, temperature, resvar)
implicit none


character(1), intent(in):: varname
integer, intent(in):: ntime
integer, intent(in):: nlevel
integer, intent(in):: nlat
integer, intent(in):: nlon
real, dimension(1:ntime,1:nlevel,1:nlat,1:nlon), intent(in):: var
integer, intent(in):: npres
real, dimension(1:npres), intent(in):: pres
real, dimension(1:ntime,1:nlevel+1,1:nlat,1:nlon), intent(in):: pressure_half_level
real, dimension(1:ntime,1:nlevel,1:nlat,1:nlon), intent(in):: pressure_full_level
real, dimension(1:ntime,1:nlevel+1,1:nlat,1:nlon), intent(in):: geopotential_half_level
real, dimension(1:ntime,1:nlevel,1:nlat,1:nlon), intent(in):: geopotential_full_level
real, dimension(1:ntime,1:nlevel,1:nlat,1:nlon), intent(in):: temperature
real, dimension(1:ntime,1:npres,1:nlat,1:nlon), intent(out):: resvar

!integer:: ntime
!integer:: nlevel
!integer:: nlat
!integer:: nlon
!real, dimension(10,10,10,10):: var
!integer:: npres
!real, dimension(10):: pres
!real, dimension(10,10,10,10):: pressure_half_level
!real, dimension(10,10,10,10):: pressure_full_level
!real, dimension(10,10,10,10):: geopotential_half_level
!real, dimension(10,10,10,10):: geopotential_full_level
!real, dimension(10,10,10,10):: temperature
!real, dimension(10,10,10,10):: resvar

integer:: itime, ilat, ilon, ipres, itemp
logical:: found 
real:: temp_T, temp_SH1, temp_SH2, temp_SH, temp_RH, d_press, d_var, grad_var_press, resvar_temp, resvar_temperature

do itime = 1, ntime
  do ilat = 1, nlat
    do ilon = 1, nlon
      do ipres = 1, npres
        itemp = 1
        found = .false.
        do 
          if(found.eqv.(.true.))exit
          ! above uppest level
          if(found.eqv.(.false.))then 
            if((trim(adjustl(varname)).eq.'T').or.(trim(adjustl(varname)).eq.'R').or.(trim(adjustl(varname)).eq.'W').or.(trim(adjustl(varname)).eq.'S'))then
              if(pres(ipres).lt.pressure_full_level(itime,1,ilat,ilon))then
                found = .true.
                resvar(itime,ipres,ilat,ilon) = -99999999.99
              endif
            endif
            if(trim(adjustl(varname)).eq.'G')then
              if(pres(ipres).lt.pressure_half_level(itime,1,ilat,ilon))then
                found = .true.
                resvar(itime,ipres,ilat,ilon) = -99999999.99
              endif
            endif
          endif
          ! interpolation
          if(found.eqv.(.false.))then
            if(trim(adjustl(varname)).eq.'G')then
              if((pres(ipres).ge.pressure_half_level(itime,itemp,ilat,ilon).and.(pres(ipres).le.pressure_half_level(itime,itemp+1,ilat,ilon))))then
                found = .true.
                resvar(itime,ipres,ilat,ilon) = lin_int_p(pres(ipres), pressure_half_level(itime,itemp,ilat,ilon), pressure_half_level(itime,itemp+1,ilat,ilon), &
                                                                        geopotential_half_level(itime,itemp,ilat,ilon), geopotential_half_level(itime,itemp+1,ilat,ilon))
              endif
            endif
            if(trim(adjustl(varname)).ne.'G')then
              if((pres(ipres).ge.pressure_full_level(itime,itemp,ilat,ilon)).and.(pres(ipres).le.pressure_full_level(itime,itemp+1,ilat,ilon)))then
                found = .true.
                if(trim(adjustl(varname)).eq.'T')then !linear interpolation
                  resvar(itime,ipres,ilat,ilon) = lin_int_p(pres(ipres), pressure_full_level(itime,itemp,ilat,ilon), pressure_full_level(itime,itemp+1,ilat,ilon), &
                                                                          temperature(itime,itemp,ilat,ilon), temperature(itime,itemp+1,ilat,ilon))
                endif
                if(trim(adjustl(varname)).eq.'R')then
                  temp_T = lin_int_p(pres(ipres), pressure_full_level(itime,itemp,ilat,ilon), pressure_full_level(itime,itemp+1,ilat,ilon), &
                                                         temperature(itime,itemp,ilat,ilon), temperature(itime,itemp+1,ilat,ilon))
                  temp_SH1 = spec_hum_from_rel_hum(temperature(itime,itemp,ilat,ilon),pressure_full_level(itime,itemp,ilat,ilon)/100.0,var(itime,itemp,ilat,ilon))
                  temp_SH2 = spec_hum_from_rel_hum(temperature(itime,itemp+1,ilat,ilon),pressure_full_level(itime,itemp+1,ilat,ilon)/100.0,var(itime,itemp+1,ilat,ilon))
                  temp_SH = lin_int_log_p(pres(ipres), pressure_full_level(itime,itemp,ilat,ilon), pressure_full_level(itime,itemp+1,ilat,ilon), temp_SH1, temp_SH2)
                  temp_RH = rel_hum_from_spec_hum(temp_SH, pres(ipres)/100.0, temp_T)
                  resvar(itime,ipres,ilat,ilon) = temp_RH
                endif
                if((trim(adjustl(varname)).ne.'T').and.(trim(adjustl(varname)).ne.'R'))then ! linear interpolation in log pressure space
                  resvar(itime,ipres,ilat,ilon) = lin_int_log_p(pres(ipres), pressure_full_level(itime,itemp,ilat,ilon), pressure_full_level(itime,itemp+1,ilat,ilon), &
                       var(itime,itemp,ilat,ilon), var(itime,itemp+1,ilat,ilon))
                endif
              endif
            endif
          endif
          !# extrapolation below the ground   
          if(found.eqv.(.false.))then
            if(trim(adjustl(varname)).eq.'T')then
              if(pres(ipres).gt.pressure_full_level(itime,nlevel,ilat,ilon))then
                found = .true.
                resvar_temp = extra_T(pres(ipres), pressure_half_level(itime,nlevel+1,ilat,ilon), pressure_full_level(itime,nlevel,ilat,ilon), geopotential_half_level(itime,nlevel+1,ilat,ilon), &
                                    temperature(itime,nlevel,ilat,ilon))  
                resvar(itime,ipres,ilat,ilon) = resvar_temp
              endif
            endif
            if(trim(adjustl(varname)).eq.'G')then
              if(pres(ipres).gt.pressure_half_level(itime,nlevel+1,ilat,ilon))then        
                found = .true.
                resvar_temp = extra_Z(pres(ipres), pressure_half_level(itime,nlevel+1,ilat,ilon), pressure_full_level(itime,nlevel,ilat,ilon), geopotential_half_level(itime,nlevel+1,ilat,ilon), &
                                    temperature(itime,nlevel,ilat,ilon))
                resvar(itime,ipres,ilat,ilon) = resvar_temp
              endif
            endif
            if(trim(adjustl(varname)).eq.'S')then
              if(pres(ipres).gt.pressure_full_level(itime,nlevel,ilat,ilon))then
                found = .true.   
                resvar_temperature = extra_T(pres(ipres), pressure_half_level(itime,nlevel+1,ilat,ilon), pressure_full_level(itime,nlevel,ilat,ilon), &
                                         geopotential_half_level(itime,nlevel+1,ilat,ilon), temperature(itime,nlevel,ilat,ilon))
                temp_RH = rel_hum_from_spec_hum(var(itime,nlevel,ilat,ilon), pressure_full_level(itime,nlevel,ilat,ilon)/100.0, temperature(itime,nlevel,ilat,ilon))
                resvar_temp = spec_hum_from_rel_hum(resvar_temperature,pres(ipres)/100.0,temp_RH)
                resvar(itime,ipres,ilat,ilon) = resvar_temp
              endif  
            endif
            if((trim(adjustl(varname)).eq.'W').or.(trim(adjustl(varname)).eq.'R'))then
              if(pres(ipres).gt.pressure_full_level(itime,nlevel,ilat,ilon))then
                found = .true.  
                resvar(itime,ipres,ilat,ilon) = var(itime,nlevel,ilat,ilon)
              endif   
            endif
          endif 
          if(found.eqv.(.false.))then
            itemp = itemp + 1
            if(itemp > nlevel)then
              itemp = 1
            endif
          endif 
        enddo
      enddo
    enddo
  enddo
enddo

end subroutine

end module mod_vintp2p_afterburner
