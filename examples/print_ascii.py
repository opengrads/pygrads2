#!/usr/bin/env python

"""Simple script to print a variables as ASCII.
   This files is here placed in the Public Domain."""


import grads

ga = grads.GaNum(Bin='gradsnc',Echo=False,Window=False)  # start grads
fh = ga.open("../data/model.nc")              # open file
ts = ga.exp('ts')                             # export a variable to python

print "   Lon     Lat      Ts"
print "-------- -------- --------"
for j in range(fh.ny):
    for i in range(fh.nx):
        print "%8.3f %8.3f %8.2f"%(ts.grid.lon[i],ts.grid.lat[j],ts[j,i])

del ga  # all done

