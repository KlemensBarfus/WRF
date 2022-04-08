def WRF_get_time_from_filename(wrf_filename):
  # purpose returns the time from the typical wrf filename like 
  # "wrfrst_d03_2007-06-16_14:00:00" as datetime object
  # filename can include the path
  # input:
  # filename [string]
  # output:
  # simulation time [datetime object]
  # written by K.Barfus 2/2022    
  import datetime
  ii = wrf_filename.rfind("wrf")
  temp_str = wrf_filename[ii:]
  #wrfrst_d03_2007-06-16_14:00:00
  temp_str2 = temp_str.split("_")
  date_str = temp_str2[2]
  year = int(date_str[0:4])
  month = int(date_str[5:7])
  day = int(date_str[8:10])
  time_str = temp_str2[3]
  hour = int(time_str[0:2])
  minute = int(time_str[3:5])
  second = int(time_str[6:8])
  date = datetime.datetime(year,month,day,hour,minute,second)
  return date