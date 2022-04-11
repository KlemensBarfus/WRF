# gets datestring for filename and datetime object from filename

def WRF_get_date_for_filename(date):
  import datetime
  # returns the date as used for WRF filename                                                                                                                                                               
  # input is a datetime object                                                                                                                                                                              
  wrf_filename_date = str(date.year)+"-"+str(date.month).zfill(2)+"-"+str(date.day).zfill(2)+"_"+ \
                      str(date.hour).zfill(2)+":"+str(date.minute).zfill(2)+":"+str(date.second).zfill(2)
  return wrf_filename_date

def WRF_get_date_from_filename(filename):
  # input:
  # filename: filename, that may include the path [string]
  # output:
  # datetime object
  # written by K. Barfus 3/2022
  import datetime
  i = filename.rfind("wrf")
  temp_str = filename[i:]
  temp_str2 = temp_str.split("_")
  date_str = temp_str2[2]
  time_str = temp_str2[3]
  year = int(date_str[0:4])
  month = int(date_str[5:7])
  day = int(date_str[8:10])
  hour = int(time_str[0:2])
  minute = int(time_str[3:5])
  second = int(time_str[6:8])
  date_res = datetime.datetime(year,month,day,hour,minute,second)
  return date_res
