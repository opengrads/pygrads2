#!/usr/bin/env python
#
# Simple script for computing percentiles for each horizontal
# gridpoint.
#

from pylab import *
from numpy import float32
from grads import GrADS, GaField

# Start GrADS and open the data file
# ----------------------------------
ga = GrADS(Bin='gradsnc',Echo=False,Port=True)
ga.open('../data/slp_djf.nc')

# Extract a timeseries
# --------------------
ga('set t 1 41')         
x = ga.exp('djfslp/100')
g = x.grid

# Transpose spatial/temporal dimensions
# -------------------------------------
(nt,ny,nx) = x.shape;
x = transpose(x.reshape((nt,nx*ny)))

# Compute percentiles using Matlab compatible prctile function
# ------------------------------------------------------------
p = ( 0, 10, 20, 30, 40, 50, 60, 70, 80, 90 )
y = zeros((nx*ny,10),dtype=float32)
for i in range(nx*ny):
    y[i,:] = prctile(x[i,:],p)
y = transpose(y);
y = y.reshape((10,ny,nx)) # save the pecentile dimension as time

# Either do the plotting in Python ...
# ------------------------------------
ga('set t 1')
for t in range(10):
    d = y[t,:,:]
    f = GaField(d,grid=g)
    ga.imshow(f)
    title('%d Percentile'%p[t])
    savefig('py_prctiles_%d.png'%p[t])
    clf()

# ... or send results back to GrADS
# ---------------------------------
ga('set t 1 10')
g.denv.nt = 10
g.meta = g.meta[0:10,:]
slp = GaField(y,grid=g)
ga.imp('prctiles',slp)

# and plot results in GrADS
# -------------------------
ga('set gxout shaded')
ga.Echo = True
for t in range(10):
    print "- Plotting %d Percentile"%p[t]
    ga('set t %d'%(t+1))
    ga('display prctiles')
    ga('draw title %d Percentile'%p[t])
    ga('cbarn')
    ga('printim ga_prctiles_%d.png'%p[t])
    ga('clear')
        

