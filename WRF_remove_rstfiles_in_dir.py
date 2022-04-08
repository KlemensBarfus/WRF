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

 
  






