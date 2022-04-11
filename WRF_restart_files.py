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

def WRF_unlink_restart_files(folder):
  # unlinks all restart files in "folder"
  import glob
  import os
  restart_links = glob.glob(folder+"wrfrst_d0*")
  for restart_link in restart_links:                                                                                                                                                                      
    sys_cmd = "unlink "+restart_link                                                                                                                                                                      
    os.system(sys_cmd)

def WRF_link_restart_files(path_rstfiles, target_dir="./"):
  # links all restart files from "folder"
  import os 
  rstfiles = get_list_of_restart_files(path_rstfiles)
  for rstfile in rstfiles:                                                                                                                                                                                
    temp_str = rstfile.split("/")                                                                                                                                                                         
    linkname = home_folder+temp_str[len(temp_str)-1]                                                                                                                                                      
    sys_cmd = "ln -sf "+rstfile+" "+target_dir+linkname
    os.system(sys_cmd)

def WRF_remove_rstfiles_in_dir(path="", rst_files=[], domain=None):
  # removes WRF restart files in directory
  # several options exist:
  # 1.) "path" defined and nothing else: all restart files in path are deleted
  # 2.) "path" and "domain" are defined and rst_files not: all restart files of defined domain are deleted in "path"
  # 3.) "path" and "rst_files" are defined, "domain" not: "path" and each entry of rst_files are combined and deleted
  # 4.) "path", "rst_files" and "domain" are defined: "path" and each entry of rst_files are combined and if belong to the domain deleted
  # 5.) "path", "rst_files" are defined and "domain" not: "path" and each entry of rst_files are combined and deleted
  # 6.) "path" not defined, "rst_files" defined and "domain" not defined: all entries in rst_files are deleted
  # 7.) "path" not defined, "rst_files" and "domain" defined: all entries in rst_files of domain are deleted
  # input:
  # path (optional): path to directory [string]
  # rst_files (optional): restart files to remove [list]
  # domain (optional): domain number(s) [list]
  # output:
  # no output
  # written by K.Barfus 3/2022     
  import os
  import glob
  if(len(path) > 0): # path defined
    if(len(rst_files) > 0):
      if(domain is None):
        for entry in rst_files:
          sys_cmd = "rm "+path+entry
          os.system(sys_cmd)
      else: # domain not none
        for entry in rst_files:
          if("d0"+str(domain) in entry):
            sys_cmd = "rm "+path+entry
            os.system(sys_cmd)
    else: # rst_files not defined
      if(domain is none): 
        search_string = path+"wrfrst_d0?_????-??-??_??:??:??"
      else:
        search_string = path+"wrfrst_d0"+str(domain)+"_????-??-??_??:??:??"
      res = glob.glob(search_string)
      for r in res:
        sys_cmd = "rm "+r
        os.system(sys_cmd) 
  else:  # path not defined so rst_files is defined
    if(domain is None): # all rst_files are removed
      for entry in rst_files:
        sys_cmd = "rm "+entry
        os.system(sys_cmd)
    else:  # domain defined
      for entry in rst_files:
        if("d0"+str(domain) in entry):
          sys_cmd = "rm "+entry
          os.system(sys_cmd) 

 
  






