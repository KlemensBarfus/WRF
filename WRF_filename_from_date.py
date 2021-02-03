def WRF_filename_from_date(date, n_domain, suffix=""):
  # results in e.g. "wrf_d04_2071-07-16_17:30:00"
  import datetime
  year = str(date.year).zfill(4)
  month = str(date.month).zfill(2)
  day = str(date.day).zfill(2)
  hour = str(date.hour).zfill(2)
  minute = str(date.minute).zfill(2)
  second = str(date.second).zfill(2)
  str1 = "wrf_d"+str(n_domain).zfill(2)+"_"
  str2 = year+"-"+month+"-"+day+"_"
  str3 = hour+":"+minute+":"+second
  res_filename = str1+str2+str3+suffix
  return res_filename


