
def date_from_WRF_filename(wrf_filename):
  # e.g. "wrf_d04_2071-07-16_17:30:00"                                                                                                                                                                      
  import datetime
  temp_str = wrf_filename.split("_")
  temp_date_str = temp_str[2]
  temp_time_str = temp_str[3]
  temp_date_str2 = temp_date_str.split("-")
  year = int(temp_date_str2[0])
  month = int(temp_date_str2[1])
  day = int(temp_date_str2[2])
  temp_time_str2 = temp_time_str.split(":")
  hour = int(temp_time_str2[0])
  minute = int(temp_time_str2[1])
  second = int(temp_time_str2[2])
  rec_date = datetime.datetime(year,month,day,hour,minute,second)
  return rec_date

def WRF_filename_from_date(date, n_domain):
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
  res_filename = str1+str2+str3
  return res_filename
