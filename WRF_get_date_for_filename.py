def WRF_get_date_for_filename(date):
  import datetime
  # returns the date as used for WRF filename                                                                                                                                                               
  # input is a datetime object                                                                                                                                                                              
  wrf_filename_date = str(date.year)+"-"+str(date.month).zfill(2)+"-"+str(date.day).zfill(2)+"_"+ \
                      str(date.hour).zfill(2)+":"+str(date.minute).zfill(2)+":"+str(date.second).zfill(2)
  return wrf_filename_date
