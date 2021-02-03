def WRF_destagger_var(var, dim):
  import numpy as np  
  # destaggers 4d variable with dimensions [time, z, y, x]
  # staggered dimension is given by dim [0-3]
  nxyz = var.shape
  if(dim == 0):
    n_staggered_dim = nxyz[0]
    var_res = (var[0:n_staggered_dim-1,:,:,:] + var[1:n_staggered_dim,:,:,:])/2.0
  if(dim == 1):
    n_staggered_dim = nxyz[1]
    var_res = (var[:,0:n_staggered_dim-1,:,:] + var[:,1:n_staggered_dim,:,:])/2.0
  if(dim == 2):
    n_staggered_dim = nxyz[2]
    var_res = (var[:,:,0:n_staggered_dim-1,:] + var[:,:,1:n_staggered_dim,:])/2.0
  if(dim == 3):
    n_staggered_dim = nxyz[3]
    var_res = (var[:,:,:,0:n_staggered_dim-1] + var[:,:,:,1:n_staggered_dim])/2.0
  return var_res
