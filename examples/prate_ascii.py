#!/usr/bin/env python

"""Simple script to print a variables as ASCII.
   This file is in the Public Domain."""

import grads

year = 2007

ga = grads.GaNum(Bin='gradsnc',Echo=False,Window=False)  # start grads
fh = ga.open("prate.sfc.gauss.%d.nc"%year)               # open file

for t in range(fh.nt):                                   # loop over time
    ga('set t %d'%(t+1))                                   # set the time
    (yyyy,mm,dd,hh) = ga.rword(1,4).split(':' )
    date = yyyy + '%02d%02d'%(int(mm),int(dd))
    print "- Writing data on " + date
    f = open('prate_ascii_%s_%d.csv'%(yyyy,t+1),"w")     # open output file
    f.write("yyyymmdd,latval,lonval,prate\n")            # write header
    prate = ga.exp('prate')                              # get prate array
    for j in range(fh.ny):                               # loop over lat
        for i in range(fh.nx):                           # loop over lon
            f.write("%s, %6.3f, %6.3f,%16.13f\n"% \
                  (date,prate.grid.lat[j],prate.grid.lon[i],prate[j,i]))
    f.close()                                            # close the file
            
del ga                                                   # all done

