#!/usr/bin/env python
#
# Simple script testing the ext()/expr() methods
#

from pylab import *
from grads import GrADS

# Start GrADS and open the data file
# ----------------------------------
ga = GrADS(Bin='grads',Echo=False,Port=True,Window=False)
ga.open('../data/model.ctl')

# XY slices
# ---------
ts1 = ga.exp('ts')
ts2 = ga.expr('ts')
print "XY Skin temperature: "
print ts1.data-ts2.data

# XYT slices
# ----------
ga('set t 2 3')
ts1 = ga.exp('ts')
ts2 = ga.expr('ts')
print "XYT Skin temperature: "
print ts1.data-ts2.data

# XYZ slices
# ----------
ga('set t 3')
ga('set z 5 6')
xx1 = ga.exp('ua')
xx2 = ga.expr('ua')
print "XYZ Zonal Wind"
print xx1.data-xx2.data

# XZT slices
# ----------
ga('set t 2 4')
ga('set z 1 5')
ga('set y 20')
xx2 = ga.expr('ua')
print "XZT Zonal Wind"
print xx2


    

