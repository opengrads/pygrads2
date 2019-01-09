#!/usr/bin/env python
#
# Simple script demonstrating the interp() method.
#

from pylab import *
from numpy import float32
from grads import GrADS, GaField

# Start GrADS and open the data file
# ----------------------------------
ga = GrADS(Bin='grads',Echo=False,Port=True,Window=False)
ga.open('../data/model.ctl')
ga('set t 1 5')
dh = ga.query('dims')
t1,t2 = dh.tyme
ga('set t 1')


# Create sample trajectory
# ------------------------
lats = array([ -90, -60, -45, 0,  45, 60, 90  ])
lons = array([-180, -90, -45, 0,  45, 90, 180 ])
tyme = array([  t1,  t1,  t1, t2, t2, t2, t2  ])

# Either do the plotting in Python ...
# ------------------------------------
ga('set t 1')
ts = ga.sampleXYT('ts',lons,lats,tyme)

clf()

subplot(211)
plot(lats,ts)
title("Surface Temperature")
xlabel('Latitude')

subplot(212)
plot(lons,ts)
xlabel('Longitude')
savefig('sampleXY1.png')

figure()

ga('set lev 500 200')
ua = ga.sampleXY('ua',lons,lats)
ta = ga.sampleXY('ta',lons,lats)
zg = ga.sampleXY('zg',lons,lats)

for i in range(len(lats)):
    subplot(121)
    plot(ta[i],zg[i]/1000); ylabel('Z'); xlabel('T')
    subplot(122)
    plot(ua[i],zg[i]/1000); ylabel('Z'); xlabel('U')

savefig('sampleXY2.png')
figure()
imshow(ua)
savefig('sampleXY3.png')







    

