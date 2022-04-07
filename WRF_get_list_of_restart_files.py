def WRF_get_list_of_restart_files(folder, domain=0):
  # gets a list or restart files in a folder
  # list is ordered by time of writing (ascending)
  # input:
  # folder: folder to search in [string]
  # domain (optional): nesting domain to search for (default: all) [integer]
  # output:
  # list including full path
  # written by K.Barfus 2/2022   
  import glob
  import os
  import numpy as np
  if(domain == 0):
    search_string = "wrfrst_d0*"
  else:
    search_string = "wrfrst_d0"+str(domain)+"*" 
  rstfiles = glob.glob(folder+search_string)
  time_files = []
  for f in rstfiles:
    time_files.append(os.path.getmtime(f)) 
  time_files = np.asarray(time_files)
  rstfiles = np.asarray(rstfiles)
  ii = np.argsort(time_files)
  time_files = time_files[ii]
  rstfiles = rstfiles[ii]
  rstfiles = rstfiles.tolist()
  return rstfiles
