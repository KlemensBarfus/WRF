# routines to read, write and modify either namelist.wps or namelist.input files for WRF
# written by K. Barfus, 3/2022

def get_val_in_proper_type(string, german=False):
  # checks if a string is a number
  # if "german" is True "," is also accepted instead of "."
  flag_number = True
  # check for logical
  if(".true." in string or ".false." in string):
    if(string == ".true."):
      val = True
    if(string == ".false."):
      val = False
  else:  
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
    if(flag_number == True):  
      if(number_points_comma == 0):
        if(number_digits == len(string)):
          val = int(string)
      else:    
        if(number_points_comma == 1):
          if(len(string) > 1):
            if(number_digits == len(string)-1):
              if("," in string):
                string = string.replace(",",".")
              val = float(string)
        else:
          flag_number = False
          val = string.strip("\'\"")
    else:
      val = string.strip("\'\"")
  return flag_number, val
    

def WRF_read_namelist(filename):
  import os
  # check if namelist.wps or namelist.input
  if(".wps" in filename):
    r = {'share': dict(), 'geogrid': dict(), 'ungrib': dict(), 'metgrid': dict()}
  else:
    r = {'time_control': dict(), 'domains': dict(), 'physics': dict(), 'fdda': dict(), 'dynamics': dict(), 'bdy_control': dict(), \
       'grib2': dict(), 'namelist_quilt': dict()}
  st = os.stat(filename)
  file_size = st.st_size
  f_in = open(filename, 'rt')
  eof = False
  while eof == False:
    line = f_in.readline()
    line = line.rstrip()
    # check for sections
    flag_section = False
    for key in r.keys():
      if("&"+key in line):
        section = key
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
  return r

def namelist_input_formatting(key):
  # used to generate a nice fornmatting of several keys defined in "t"
  # result is padded by blanks up to the length of the longest key in each 
  # inner list
  # written by K.Barfus 4/2022    
  t = [
    ["run_days", "run_hours", "run_minutes", "run_seconds", "aaaaaaaaaaaaaaaaaaaaaaa"],
    ["interval_seconds", "input_from_file", "history_interval", "history_outname", "frames_per_outfile", "restart", 
     "restart_interval", "rst_outname", "io_form_history", "io_form_restart", "io_form_input", "io_form_boundary", "debug_level", "write_hist_at_0h_rst", "aaaaaaaaaaaaaaaaaaaaaaa"], 
    ["time_step", "time_step_fract_num", "time_step_fract_den", "max_dom", "e_we", "e_sn", "e_vert", "p_top_requested", "num_metgrid_levels", "num_metgrid_soil_levels", 
     "dx", "dy", "grid_id", "parent_id", "i_parent_start", "j_parent_start", "parent_grid_ratio", "parent_time_step_ratio", "feedback", "smooth_option", "aaaaaaaaaaaaaaaaaaaaaaa"],
    ["mp_physics", "ra_lw_physics", "ra_sw_physics", "radt", "sf_sfclay_physics", "sf_surface_physics", "bl_pbl_physics", "bldt", "cu_physics", "cudt", "isfflx", "ifsnow", "icloud", 
     "surface_input_source", "num_soil_layers", "sf_urban_physics", "aaaaaaaaaaaaaaaaaaaaaaa"],
    ["w_damping", "diff_opt", "km_opt", "diff_6th_opt", "diff_6th_factor", "base_temp", "damp_opt", "zdamp", "dampcoef", "khdif", "kvdif", "non_hydrostatic", "moist_adv_opt",
     "scalar_adv_opt", "aaaaaaaaaaaaaaaaaaaaaaa"],
    ["spec_bdy_width", "spec_zone", "relax_zone", "specified", "nested", "aaaaaaaaaaaaaaaaaaaaaaa"],    
    ["nio_tasks_per_group", "nio_groups", "aaaaaaaaaaaaaaaaaaaaaaa"]
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

def namelist_wps_formatting(key):
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

    

def WRF_write_namelist(filename,r):
  f_out = open(filename, 'wt')
  wps_flag = False
  input_flag = False
  if("share" in r.keys()):
    sections = ['share', 'geogrid', 'ungrib', 'metgrid']
    wps_flag = True
  else:  
    sections = ['time_control', 'domains', 'physics', 'fdda', 'dynamics', 'bdy_control', 'grib2', 'namelist_quilt']
    input_flag = True
  for section in sections:  
    # write section
    f_out.write("&"+section+"\n")
    keys = list(r[section].keys())
    for key in keys:
      if(wps_flag == True):
        name_temp = namelist_wps_formatting(key)
      if(input_flag == True):
        name_temp = namelist_input_formatting(key)
      value_temp = r[section][key]
      if(type(value_temp[0]) is bool):
        for i in range(0, len(value_temp)):
          if(value_temp[i] == True):
            value_temp[i] = ".true."
          else:
            value_temp[i] = ".false."
      else:
        if(isinstance(value_temp[0], str) == False):
          value_temp = [str(v) for v in value_temp]
        else:
          value_temp = ["'"+ str(v) + "'" for v in value_temp]  
      value = ", ".join(value_temp)
      if(wps_flag == True):
        string = " "+name_temp + " = " + value + ",\n"
      else:  
        string = name_temp + " = " + value + ",\n"
      f_out.write(string)
    f_out.write("/\n") # closing "/"
    f_out.write("\n") # empty line  
  f_out.close()

def datetime_to_namelist_wps_date(d):
  import datetime
  # converts a datetime object to namelist_wps time string (2009_05_20_12:00:00)
  res1 = d.year+"_"+d.month.zfill(2)+"_"+d.day.zfill(2)
  res2 = d.hour.zfill(2)+":"+d.minute.zfill(2)+":"+d.second.zfill(2)
  res = res1 + "_" + res2
  return res

def namelist_wps_date_to_datetime(string):
  import datetime
  # converts a namelist_wps time string (2009_05_20_12:00:00) to a datetime object  
  rec_year = int(string[0:4])
  rec_month = int(string[5:7])
  rec_day = int(string[8:10])
  rec_hour = int(string[11:13])
  rec_minute = int(string[14:16])
  rec_second = int(string[17:19])
  res = datetime.datetime(rec_year,rec_month,rec_day,rec_hour,rec_minute,rec_second)
  return res
  

#filename_input = "namelist.wps"
#r = read_namelist(filename_input)
#filename_out = "namelist2.wps"
#write_namelist(filename_out, r)


