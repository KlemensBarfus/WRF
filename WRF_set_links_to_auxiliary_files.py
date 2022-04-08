def WRF_set_links_to_auxiliary_files(wrf_version, target_dir=""):
  # sets links to auxiliary files as they are defined in the file "WRF_list_of_links.txt" 
  # the "run" directory of WRF needs to be defined 
  # written by K.Barfus 3/2022

  # wrf version: "4.2.1" or "4.3"
  import os  

  # read links:
  filename_links = "WRF_list_of_links.txt"
  st = os.stat(filename_links)
  file_size = st.st_size
  f_in = open(filename_links, "rt")
  eof = False
  temp_str = f_in.readline() # read header line
  while eof == False:
    temp_str = f_in.readline()
    temp_str = temp_str.rstrip() # remove '\n'
    temp_str2 = temp_str.split()
    wrf_version_temp = temp_str2[0]
    if(wrf_version_temp == wrf_version or wrf_version_temp == 'all'):
      path_run = "/home/barfus/WRF"+wrf_version+"/WRF-"+wrf_version+"/run/"
      file_to_link = temp_str2[1]
      if(len(temp_str2) == 3):
        linkname = temp_str2[2]
      else:
        linkname = file_to_link
      if(len(target_dir) == 0): 
        sys_cmd = "ln -sf "+path_run+file_to_link+" "+linkname
      else:
        sys_cmd = "ln -sf "+path_run+file_to_link+" "+target_dir+linkname
    print(sys_cmd)
    os.system(sys_cmd)
    if f_in.tell() == file_size:
      eof = True
  f_in.close()

    
