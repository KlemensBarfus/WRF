def WRF_check_if_output_file_exists(folder,date,domain):
  # input: 
  # folder: the folder where to look for the file [string]
  # date: date as datetime object
  # domain: number of the domain [integer]
  # output:
  # logical with True when file exists [True or False]
  # requires:
  # WRF_get_date_for_filename
  # written by K. Barfus, 2/2022    
  import datetime
  import os
  temp_date_str = WRF_get_date_for_filename(date)
  test_filename = folder+"wrf_d0"+str(domain)+"_"+temp_date_str
  flag = os.path.exists(test_filename)
  return flag 

