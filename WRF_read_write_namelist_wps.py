# routines to read, write and modify namelist.wps files for WRF
# written by K. Barfus, 3/2022

def get_val_in_proper_type(string, german=False):
  # checks if a string is a number
  # if "german" is True "," is also accepted instead of "."
  flag_number = True
  i = 0
  number_digits = 0
  number_points_comma = 0
  while(i < len(string) and flag_number == True):
    if(string[i].isdigit()):
      number_digits = number_digits + 1
    else:
      if(string[i] in [",","."]):
        if(string[i] == ","):
          if(german == True): 
            number_points_comma = number_points_comma + 1
            if(number_points_comma > 1):
              flag_number = False
          else:
            flag_number = False
        if(string[i] == "."):
          if(german == False):
            number_points_comma = number_points_comma + 1
            if(number_points_comma > 1):
              flag_number = False
          else:
            flag_number = False
      else:
        flag_number = False
    i = i + 1    
  if(number_points_comma == 0):
    if(number_digits == len(string)):
      flag_number = True
      val = int(string)
  if(number_points_comma == 1):
    if(len(string) > 1):
      if(number_digits == len(string)-1):
        if("," in string):
          string = string.replace(",",".")
        flag_number = True
        val = float(string)
    else:
      flag_number = False
      val = string.strip("\'\"")
  else:
    if (flag_number == False):
      val = string.strip("\'\"")
  return flag_number, val
    

def read_namelist_wps(filename):
  import os
  r = {'share': dict(), 'geogrid': dict(), 'ungrib': dict(), 'metgrid': dict()}
  st = os.stat(filename)
  file_size = st.st_size
  f_in = open(filename, 'rt')
  eof = False
  while eof == False:
    line = f_in.readline()
    line = line.rstrip()
    print(line)
    # check for sections
    flag_section = False
    if("&share" in line):
      section = "share"
      flag_section = True
    if("&geogrid" in line):
      section = "geogrid"
      flag_section = True
    if("&ungrib" in line):
      section = "ungrib"
      flag_section = True
    if("&metgrid" in line):
      section = "metgrid"
      flag_section = True
    # check for stop sign of section "/" or empty line
    if(flag_section == False):
      flag_stop_section = False
      if(line.strip() == "/" or line.strip() ==""):
        flag_stop_section = True
      else:
        line_split = line.split("=")
        name = line_split[0].strip() # remove any blanks
        line_split[1] = line_split[1].rstrip(",") # remove last comma  
        var_temp = line_split[1].strip()
        var_temp2 = var_temp.split(",")
        i = 0
        while(i < len(var_temp2)):
          if(len(var_temp2[i].rstrip()) == 0):
            del(var_temp2[i])
          else:
            var_temp2[i] = var_temp2[i].strip()
            flag_temp, var_temp3 = get_val_in_proper_type(var_temp2[i])
            var_temp2[i] = var_temp3
            i = i + 1
        #print(name, ":", var_temp2)
        r[section][name] = var_temp2
    if f_in.tell() == file_size:
      eof = True
  f_in.close()
  print(r)
  return r

def namelist_formatting(key):
  # used to generate a nice fornmatting of several keys defined in "t"
  # result is padded by blanks up to the length of the longest key in each 
  # inner list
  # written by K.Barfus 4/2022    
  t = [
   ["parent_id", "parent_grid_ratio", "i_parent_start", "j_parent_start",
    "e_we", "e_sn", "geog_data_res"],
   ["ref_lat", "ref_lon", "truelat1", "truelat2", "stand_lon"]
  ]
  i = 0
  found = False
  res_string = key
  while(found == False and i < len(t)):
    if(key in t[i]):
      found = True
      max_length = 0
      for tt in t[i]:
        if(len(tt) > max_length):
          max_length = len(tt)
      res_string = key.ljust(max_length)
    else:
      i = i + 1
  return res_string     
  
    

def write_namelist_wps(filename,r):
  f_out = open(filename, 'wt')
  sections = ['share', 'geogrid', 'ungrib', 'metgrid']
  for section in sections:  
    # write section
    f_out.write("&"+section+"\n")
    keys = list(r[section].keys())
    for key in keys:
      name_temp = namelist_formatting(key)
      value_temp = r[section][key]
      if(isinstance(value_temp[0], str) == False):
        value_temp = [str(v) for v in value_temp]
      else:
        value_temp = ["'"+ v + "'" for v in value_temp]  
      value = ", ".join(value_temp)
      string = " "+ name_temp + " = " + value + ",\n"
      f_out.write(string)
    f_out.write("/\n") # closing "/"
    f_out.write("\n") # empty line  
  f_out.close()


filename_wps = "namelist.wps"
r = read_namelist_wps(filename_wps)
filename_out = "namelist2.wps"
write_namelist_wps(filename_out, r)


