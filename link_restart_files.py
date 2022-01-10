# links the restart files to the directory where WRF runs
# directory where restart files are stored is read from namelist.input variable
# run from the directory where WRF is started as "python3 link_restart_files.py"

import os
import glob

filename_namelist = "namelist.input"
f_in = open(filename_namelist, "rt")
found = False
while found == False:
  str1 = f_in.readline()
  if("rst_outname" in str1):
    found = True
    str1 = str1.rstrip() # remove \n from string
    i = str1.find("=")
    str2 = str1[i+1:]
    ii = [i for i, x in enumerate(str2) if (x == '"' or x == "'")]
    str3 = str2[ii[0]+1:ii[1]]
    ii = str3.rfind("/")
    path_files = str3[0:ii+1]      
f_in.close()  

# get all restart files in the directory
wrfrst_files = glob.glob(path_files+"wrfrst_d*")
for wrfrst_file in wrfrst_files:
  sys_cmd = "ln -sf "+wrfrst_file+" "+wrfrst_file[ii+1:] 
  os.system(sys_cmd)


