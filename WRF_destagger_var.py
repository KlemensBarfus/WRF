def WRF_destagger_var(v, dim):
  # destaggers n-dimensional variable with dimensions (e.g. [time, z, y, x])
  # staggered dimension is given by dim
  import numpy as np
  nd = v.shape
  nd = np.asarray(nd)
  q0 = np.arange(0,nd[dim]-1)
  q1 = np.arange(1,nd[dim])
  v0 = np.take(v, q0, axis=dim)
  v1 = np.take(v, q1, axis=dim)
  res = np.add(v0,v1) / 2.0
  return res

