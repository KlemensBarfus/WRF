def WRF_date_from_filename(wrf_filename):
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


