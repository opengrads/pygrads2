#--------------------------------------------------------------------------
#
#    Copyright (C) 2007-2008 by Arlindo da Silva <dasilva@opengrads.org>
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

"""
This module defines "magic commands" for using GrADS interactively
from within iPython. This module is usually imported from the
configuration file "ipythonrc-grads". At any time, on-line help is
available with these commands:

    help(ipygrads)   This document
    qref             PyGrADS quick reference
    examples         Some PyGrADS examples

Based on command line arguments supplied by the user, the top level
script "pygrads" defines key environments variables necessary for this
module to start a GrADS connection, defining the global object "ga".
You can use "ga" to interact with GrADS directly:

    ga("q config")

However, a number of shortcuts are provided so that rarely one needs
to explicitly type "ga.cmd(...)". The following generic GrADS commands
are available:

    clear/c, define, disable, display/d, draw, enable, 
    Open/o, Print/pp, printim/pim, Set/s, query/q, reinit 

Notice that some commands (e.g., "Open") are capitalized to avoid
conflict with standard Python keywords.

In addition, any generic GrADS command can be entered by starting the
line with a period and a space ('. '), for example example

    . open model.ctl
    . display ps

The following convenience aliases are provided:

    cb         run cbarn (for color bar script)
    sh         set gxout shaded
    yat        run gxyat

These shortcuts run specific methods from module "grads" on the GrADS
object "ga":

    dd $name   runs the "imp" method, displaying a NumPy array in 
               GrADS; this is equivalent to 
                    ga.imp('<display>',$name)
    eof $name  compute EOS using Singular Value Decomposition; the
               *time* dimension contains the eofs; this equivalent to:
                $name,$name_d,$name_c = ga.eof('$name')
    ii $name   runs the "imp" method, importing a NumPy array into
               GrADS; this is equivalent to 
                     ga.imp("$name",$name)
    oo $fname  runs the "open" method,  setting "fh"
    qq $what   runs the "query" method, setting "qh"
    xx $name   runs the "exp" method, returning a NumPy array and an
               associated grid with coordinate information.
               This magic command is equivalent to 
                    $name = ga.exp("$name")
                    $lon  = $name.grid.lon
                    $lat  = $name.grid.lat
                    $lev  = $name.grid.lev
                    $time = $name.grid.time

The shortcuts "dd/ii/xx" are somewhat limited interfaces to the
"imp"/"exp" methods as they do not work on expressions; use
"ga.imp()"/"ga.exp()" directly for a more flexible alternative.

For additional information on these and other methods, consult the
documnentation for the main classes:

   help('grads')
   help('GrADS')
   help('GaNum')
   help('GaLab')
   help('gacm')

"""

__version__ = '1.0.6'

from grads import *

import os

if HAS_GALAB:
    try:
        from mpl_toolkits.basemap import cm as bacm
    except:
        try:
            from matplotlib.toolkits.basemap import cm as bacm
        except:
            print "Cannot load basemap colormaps (bacm)"

import IPython.ipapi
ip = IPython.ipapi.get()

def grads_ (self, arg=' '):
    self.api.ex("from grads import GrADS; ga=GrADS(%s)"%arg)

def gradsc (self, arg):
    self.api.ex("from grads import GrADS; ga=GrADS(Bin='gradsc',%s)"%arg)

def gradsnc (self, arg):
    self.api.ex("from grads import GrADS; ga=GrADS(Bin='gradsnc',%s)"%arg)

def gradshdf (self, arg):
    self.api.ex("from grads import GrADS; ga=GrADS(Bin='gradshdf',%s)"%arg)

def gacbarn (self,arg):
    self.api.ex("ga.cmd('run cbarn')")
 
def gaclear (self,arg):
    self.api.ex("ga.cmd('clear')")
 
def gacmd (self, arg):
    self.api.ex("ga.cmd('%s')"%arg)
 
def gadefine (self, arg):
    self.api.ex("ga.cmd('define %s')"%arg)
 
def gaenable (self, arg):
    self.api.ex("ga.cmd('enable %s')"%arg)

def gadisable (self, arg):
    self.api.ex("ga.cmd('disable %s')"%arg)

def gadisplay (self, arg):
    self.api.ex("ga.cmd('display %s')"%arg)

def gaquery (self, arg):
    self.api.ex("ga.cmd('query %s')"%arg)
 
def gapim (self, arg):
    self.api.ex("ga.cmd('printim %s')"%arg)
 
def gayat (self, arg):
    self.api.ex("ga.cmd('gxyat %s')"%arg)
 
def gapgx (self, arg=' '):
    self.api.ex("ga.cmd('print %s')"%arg)
 
def gaopen (self, arg):
    self.api.ex("ga.cmd('open %s')"%arg)
 
def gaOpen (self, arg):
    self.api.ex("fh=ga.open('%s')"%arg)
 
def gaQuery (self, arg):
    self.api.ex("qh=ga.query('%s')"%arg)
 
def gaqref (self, arg):
    text = """
Basic GrADS commands:

    clear/c, define, disable, display/d, draw, enable, 
    Open/o, Print/pp, printim/pim, Set/s, query/q, reinit 

    . $cmd     executes any GrADS command $cmd

Convenient aliases:

    cb         run cbarn (for color bar script)
    sh         set gxout shaded
    yat        run gxyat

GrADS Methods:

    dd $name   runs the "imp" method, displaying a NumPy array in 
               GrADS; this is equivalent to 
                    ga.imp('<display>',$name)
    eof $name  compute EOS using Singular Value Decomposition; the
               *time* dimension contains the eofs; this equivalent to:
                $name,$name_d,$name_c = ga.eof('$name')
    ii $name   runs the "imp" method, importing a NumPy array into
               GrADS; this is equivalent to 
                     ga.imp("$name",$name)
    oo $fname  runs the "open" method,  setting "fh"
    qq $what   runs the "query" method, setting "qh"
    xx $name   runs the "exp" method, returning a NumPy array and an
               associated grid with coordinate information.
               This magic command is equivalent to 
                    $name = ga.exp("$name")
                    $lon  = $name.grid.lon
                    $lat  = $name.grid.lat
                    $lev  = $name.grid.lev
                    $time = $name.grid.time

    """
    self.api.ex('print """%s"""'%text)

def gaexample (self, arg):
    text = """
Open a file and display a variable:

   [1] ga-> q config
   [2] ga-> o model 
   [3] ga-> d ts 
   [4] ga-> . draw title Surface Temperature (Kelvin)

Export variable "ts", change units in python, and display it in GrADS:

   [] ga-> xx ts 
   [] ga-> ts = ts - 273 
   [] ga-> c
   [] ga-> sh
   [] ga-> dd ts 
   [] ga-> cb
   [] ga-> . draw title Surface Temperature (Celsius)

Display the modified variable in Python with Matplotlib:

   [] ga-> contourf(lon,lat,ts) 
   [] ga-> title('Surface Temperature (Celsius)')
   [] ga-> figure(2) 
   [] ga-> plot(lat,ts[:,0]))
   [] ga-> title('Surface Temperature (Celsius) at lon=0')

Export an expression, change it in Python, and import it back:

   [] ga-> . set lev 300
   [] ga-> uv = ga.exp('ua*ua+va*va') 
   [] ga-> speed = sqrt(uv)
   [] ga-> ii speed
   [] ga-> d speed
   [] ga-> . draw title Wind Speed
   [] ga-> cb

If all you wanted to do was to plot the wind speed, you can do this directly,
without nthe need to explicitly importing it first:

   [] ga-> dd speed
   [] ga-> . draw title Wind Speed
   [] ga-> cb

If you have Matplotlib with the Basemap toolkit installed, you can do
most of your plotting in python. Shaded contours can be produced with
the command:

   [] ga-> ga.contourf('ts')
   [] ga-> title('Surface Temperature')

If instead you would like a continuous color scale do this

   [] ga-> clf()
   [] ga-> ga.imshow('ts')

If all you want is a plain image covering all of your graphics window
to later be exported to GoogleEarth then

   [] ga-> clf()
   [] ga-> ga.implain('ts')

A pseudo-color plot, just like one would obtain with "set gxout grfill", 
can be produced with 

   [] ga-> clf()
   [] ga-> ga.pcolor('ts')

Here is how to plot a variable on a blue marble background

   [] ga-> ga.blue_marble('on')
   [] ga-> s lon -180 180
   [] ga-> ga.imshow('ua')
   [] ga-> title('Zonal Wind')

You can also select your map projection, e.g.

   [] ga-> ga.basemap('npo')
   [] ga-> ga.contour('zg(lev=300)')
   [] ga-> title('300 hPa Heights')

If in any moment you would like to save the graphics window just type

   [] ga-> savefig('myfile.png')

For more information type:

   [] ga-> help galab
   [] ga-> help pylab

Terminating your session:

   [] quit()

Computing EOFs (experimental):

   % pygrads slp_djf.nc
   [] ga-> s t 1 41
   [] ga-> eof djfslp
   [] ga-> contourf(lon,lat,djfslp[0,:,:])
   [] ga-> s t 1
   [] ga-> sh 
   [] ga-> dd djfslp
   [] ga-> . draw title NAO Pattern

    """
    self.api.ex('print """%s"""'%text)

 
def gareinit (self,arg):
    self.api.ex("ga.cmd('reinit')")
 
def gashaded (self,arg):
    self.api.ex("ga.cmd('set gxout shaded')")
 
def gaset (self, arg):
    self.api.ex("ga.cmd('set %s')"%arg)

def gax (self, arg):
    self.api.ex("%s = ga.exp('%s');lon=%s.grid.lon; lat=%s.grid.lat;lev=%s.grid.lev;time=%s.grid.time"%(arg,arg,arg,arg,arg,arg))

def gaeof (self, arg):
    self.api.ex("%s, %s_s, %s_pc = ga.eof('%s');lon=%s.grid.lon; lat=%s.grid.lat;lev=%s.grid.lev;time=%s.grid.time"%(arg,arg,arg,arg,arg,arg,arg,arg))

def gai (self, arg):
    self.api.ex("ga.imp('%s',%s)"%(arg,arg))

def gad (self, arg):
    self.api.ex("ga.imp('<display>',%s)"%(arg))

# Expose the magic commands
ip.expose_magic('grads',   grads_)
ip.expose_magic('gradsc',  gradsc)
ip.expose_magic('gradsnc', gradsnc)
ip.expose_magic('gradshdf',gradshdf)
ip.expose_magic('cb',       gacbarn)
ip.expose_magic('c',       gaclear)
ip.expose_magic('clear',   gaclear)
ip.expose_magic('define',  gadefine)
ip.expose_magic('d',       gadisplay)
ip.expose_magic('display', gadisplay)
ip.expose_magic('enable',  gaenable)
ip.expose_magic('examples',  gaexample)
ip.expose_magic('disable', gadisable)
ip.expose_magic('.',       gacmd)
ip.expose_magic('Open',    gaopen)
ip.expose_magic('o',       gaopen)
ip.expose_magic('oo',      gaOpen)
ip.expose_magic('open',    gaopen)
ip.expose_magic('pim',     gapim)
ip.expose_magic('printim', gapim)
ip.expose_magic('Print',   gapgx)
ip.expose_magic('pp',      gapgx)
ip.expose_magic('yat',     gayat)
ip.expose_magic('s',       gaset)
ip.expose_magic('Set',     gaset)
ip.expose_magic('sh',      gashaded)
ip.expose_magic('q',       gaquery)
ip.expose_magic('query',   gaquery)
ip.expose_magic('qref',    gaqref)
ip.expose_magic('qq',      gaQuery)
ip.expose_magic('reinit',  gareinit)
ip.expose_magic('xx',      gax)
ip.expose_magic('ii',      gai)
ip.expose_magic('dd',      gad)
ip.expose_magic('eof',     gaeof)

# Retrieve GraDS options from environment (set by "pygrads" top script)
Bin   = os.getenv('GA_BIN',default='gradshdf')
Cmd   = os.getenv('GA_CMD',default='')
Opts  = os.getenv('GA_OPT',default='')
Files = os.getenv('GA_FIL')

if Cmd!='':  Opts = '-c "'+Cmd+'" '+Opts
if Opts=='': Opts=None

# Instantiate the GrADS object
# If someone has an alternative to making ga global,
# I'd like to know about it.
# --------------------------------------------------
global ga
if HAS_GALAB:
    ga = GaLab(Bin=Bin,Opts=Opts)
elif HAS_GANUM:
    ga = GaNum(Bin=Bin,Opts=Opts)
else:
    ga = GrADS(Bin=Bin,Opts=Opts)

# Change prompt to something familiar
ip.options.prompt_in1 = ' [\#] ga-> '

print """
   Welcome to PyGrADS, a GrADS-based iPython environment. 
   For more information, type 'help(ipygrads)'

?         -> Introduction and overview of IPython's features.
help      -> Python's own help system.
qref      -> PyGrADS quick reference
examples  -> Some PyGrADS examples
object?   -> Details about 'object'. ?object also works, ?? prints more.

"""

if Files!='':
    for file in split(Files,sep=' '):
        try:
            fh = ga.open(file,Quiet=True)
            print "Successfully opened <%s> as File %d"%(file,fh.fid)
        except:
            print "Failed to open GrADS file <%s>"%file


