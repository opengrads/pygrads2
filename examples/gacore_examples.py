#!/usr/bin/env python

"""Simple demo of the GrADS class in Python"""

#--------------------------------------------------------------------------
#
#  REVISION HISTORY:
#
#  18Mar2006  da Silva  First crack.
#
#--------------------------------------------------------------------------
#
#    Copyright (C) 2006 by Arlindo da Silva <dasilva@alum.mit.edu>
#    All Rights Reserved.
#
#    This program is free software# you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation# using version 2 of the License.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY# without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program# if not, please consult  
#              
#              http://www.gnu.org/licenses/licenses.html
#
#    or write to the Free Software Foundation, Inc., 59 Temple Place,
#    Suite 330, Boston, MA 02111-1307 USA
#
#------------------------------------------------------------------------

from grads import *
from sys   import stdout

# Start GrADS
# -----------
try:
    ga = GrADS(Verb=1, Echo=False, Port=False, Window=False,
         Opts="-c 'q config'")
    print ">>> OK <<< start GrADS"
except:
    print ">>> NOT OK <<< cannot start GrADS"

# This files does not exist
# -------------------------
try:
    fh = ga.open("wrong_file.nc")  
    print ">>> NOT OK <<< file 'wrong_file.nc' should not exist"
except GrADSError:
    print ">>> OK <<< No such file, we meant that!\n"

# Ok, this one should exist
# -------------------------
print 'Opening a CTL file:'
try:
    fh = ga.open("../data/model")
    print fh.title
    print '              File Id: ', fh.fid
    print '         Dataset type: ', fh.type
    print '    No. of Time steps: ', fh.nt
    print '    No. of Longitudes: ', fh.nx
    print '    No. of  Latitudes: ', fh.ny
    print '    No. of     Levels: ', fh.nz
    print '      Variable  names: ', fh.vars
    print '      Variable levels: ', fh.var_levs
    print '      Variable titles: ', fh.var_titles
    print ''
    print ">>> OK <<< open CTL file"
except:
    print ">>> NOT OK <<< cannot open CTL file"

# Ok, sdfopen should work as well
# -------------------------------
print 'Opening a NetCDF file:'
try:
    fh = ga.open("../data/model.nc")
    print fh.title
    print '              File Id: ', fh.fid
    print '         Dataset type: ', fh.type
    print '    No. of Time steps: ', fh.nt
    print '    No. of Longitudes: ', fh.nx
    print '    No. of  Latitudes: ', fh.ny
    print '    No. of     Levels: ', fh.nz
    print '      Variable  names: ', fh.vars
    print '      Variable levels: ', fh.var_levs
    print '      Variable titles: ', fh.var_titles
    print ''
    print ">>> OK <<< open NetCDF file"
except:
    print ">>> NOT OK <<< cannot open NetCDF file"

# Next, check the query method
# ----------------------------
try:
    qh = ga.query('dims')
    print 'Current dimensional state: '
    print '   X is '+qh.x_state+'   Lon = ',qh.lon,'  X = ',qh.x
    print '   Y is '+qh.y_state+'   Lat = ',qh.lat,'  Y = ',qh.y
    print '   Z is '+qh.z_state+'   Lev = ',qh.lev,'  Z = ',qh.z
    print '   T is '+qh.t_state+'  Time = ',qh.time,'  T = ',qh.t
    print ''
    print ">>> OK <<< query dimensions"
except:
    print ">>> NOT OK <<< cannot query dimensions"

try:
    qh = ga.query('file')
    print 'Current file state: '
    print '         Title: ', qh.title
    print '       File Id: ', qh.fid
    print '   Description: ', qh.desc
    print '        Binary: ', qh.bin
    print ''

    print '   Variable  Num levels  Description'
    for (var, nlevels, desc) in qh.var_info:
         print '   '+var.rjust(8)+'  '+str(nlevels).rjust(10)+'  '+desc

    print ''
    print ">>> OK <<< query file"
except:
    print ">>> NOT OK <<< cannot query file"

# Test output capture, 2 modes: line and words
# --------------------------------------------
try:
    ga.cmd("q config")

    print "--------------------------------------------------------------"
    print "            Captured GrADS output: Line interface"
    print "--------------------------------------------------------------"
    for i in range(1,ga.nLines):
        print ga.rline(i)
    print "                          ---------"

    print ""
    print "--------------------------------------------------------------"
    print "            Captured GrADS output: Word interface"
    print "--------------------------------------------------------------"
    for i in range(1,ga.nLines):
        for j in range(1,20):     # 20 is an over estimate, but i is OK
            stdout.write(ga.rword(i,j)+' ')
        stdout.write('\n')
    print "                          ---------"
    print ""
    print ">>> OK <<< rline()/rword() completes"
except:
    print ">>> NOT OK <<< rline()/rword() fails"

# Export/import a variable from GrADS
# -----------------------------------
print ""
print "--------------------------------------------------------------"
print "         Exporting/Importing Data (Requires GaNum)"
print "--------------------------------------------------------------"
if HAS_GANUM:
    try:
        ts = ga.exp('ts')
        print "Ts in Kelvins: ", ts.min(), ts.max()
        ts = ts - 273
        print "Ts in Celsius: ", ts.min(), ts.max()
        ga.imp('tc',ts)
        tc = ga.exp('tc')
        print "Tc in Celsius: ", tc.min(), tc.max()
        print ">>> OK <<< exp()/imp() completes"
    except:
        print ">>> NOT OK <<< exp()/imp() fails"

else:
    print ">>> OK <<< exp()/imp() not tested because NumPy is not available"

# Entering a bunch of comands at once
# -----------------------------------
print ""
print "--------------------------------------------------------------"
print "         Entering a Bunch of commands at once"   
print "--------------------------------------------------------------"
try:
    ga("""
           set lat 30 60
           set lon -80 -50
           set t 1 3
           query dims
       """)
    print ">>> OK <<< successfuly ran several commands at one"
except:
    print ">>> NOT OK <<< could not run several commands at once"

print "All done."
