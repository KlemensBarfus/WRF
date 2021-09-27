def get_WRF_files_in_folder_by_date(path, start_date, stop_date, domain):
  # gets all wrf files (into a list) for a certain domain from a folder defined by
  # path: path where the files are
  # start_date: start date as datetime object
  # stop_date: stop_date as datetime object
  # strucure of the filename is "wrf_d04_2013-09-07_22:00:00"
  import datetime
  import glob
  import numpy as np
  import os
  import sys
  # check if path exists
  if(os.path.exists(path) == False):
    sys.exit("ERROR: get_WRF_files_in_folder_by_date: path does not exist")
  else:  
    domain_str = str(domain).zfill(2)
    all_wrf_files = glob.glob(path+"wrf_d"+domain_str+"_*")
    valid_files = []
    valid_files_date = []
    for files in all_wrf_files:
      temp_str =  files.split("/")
      filename_temp = temp_str[len(temp_str)-1]
      temp_str2 = filename_temp.split("_")
      temp_str3 = temp_str2[2]
      temp_str4 = temp_str3.split("-")
      year_temp = int(temp_str4[0]) 
      month_temp = int(temp_str4[1])
      day_temp = int(temp_str4[2])
      temp_str3 = temp_str2[3]
      temp_str4 = temp_str3.split(":")
      hour_temp = int(temp_str4[0])
      minute_temp = int(temp_str4[1])
      second_temp = int(temp_str4[2])
      date_temp = datetime.datetime(year_temp,month_temp,day_temp,hour_temp,minute_temp,second_temp)
      if(date_temp >= start_date and date_temp <= stop_date):
        valid_files.append(files)
        valid_files_date.append(date_temp)
    if(len(valid_files) == 0):
      sys.exit("ERROR: get_WRF_files_in_folder_by_date: no files found")
    else:  
      valid_files_date = np.asarray(valid_files_date)
      valid_files = np.asarray(valid_files)
      index_sorted = np.argsort(valid_files_date)
      valid_files = valid_files[index_sorted]
      valid_files = valid_files.tolist()
      return valid_files
