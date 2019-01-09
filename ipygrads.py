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
This module defines "magic commands" for using GrADS interactively from within
iPython. At any time, on-line help is available with these commands:

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
line with a period and a space ('. '), for example:

    . open model.ctl
    . display ps

If instead you type a lonely "." you will enter the "classic GrADS" mode.
Your prompt will change to:

    ga->

and until you enter another lonely "." you be interacting directly with GrADS,
with no python whatsover involved.

The following convenience aliases are provided:

    cb         run cbarn (for color bar script)
    sh         set gxout shaded
    yat        run gxyat

These shortcuts run specific methods from module "grads" on the GrADS
object "ga":

    dm $name   displays $name in GrADS showing the resulting image in your
               Matplotlib window. This is equivalent to
                    ga.cmd('display $name')
                    ga.imexp()
    dd $name   runs the "imp" method, displaying a NumPy array in 
               GrADS; this is equivalent to 
                    ga.imp('<display>',$name)
    eof $name  compute EOF using Singular Value Decomposition; the
               *time* dimension contains the eofs; this equivalent to:
                $name,$name_d,$name_c = ga.eof('$name')
    ii $name   runs the "imp" method, importing a NumPy array into
               GrADS; this is equivalent to 
                     ga.imp("$name",$name0
    im         shows content of your GrADS graphics buffer in your
               Matplotlib canvas; same as
                     ga.imexp()
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

__version__ = '1.0.8'

from grads import *

import os
from tempfile import mktemp

if HAS_GAYA:
    from mayavi import mlab

if HAS_GALAB:
    from matplotlib.image  import imread
    from matplotlib.pyplot import imshow, axes, axis
    try:
        from mpl_toolkits.basemap import cm as bacm
    except:
        try:
            from matplotlib.toolkits.basemap import cm as bacm
        except:
            print "Cannot load basemap colormaps (bacm)"

# Coping with the IPython API change from v0.10 to v0.11
try:
    import IPython.ipapi                  # IPython 0.10 and earlier
    ip = IPython.ipapi.get()
    def_Magic = ip.expose_magic
    IPY_LEGACY = True
except:
    from IPython import InteractiveShell  # IPython 0.11 and later
    ip = InteractiveShell.instance()
    def_Magic = ip.define_magic
    IPY_LEGACY = False

def ip_Exec(self,cmd):
    if IPY_LEGACY:
        self.api.ex(cmd)
    else:
        ip.ex(cmd)

def grads_ (self, arg=' '):
    ip_Exec(self,"from grads import GrADS; ga=GrADS(%s)"%arg)

def gradsc (self, arg):
    ip_Exec(self,"from grads import GrADS; ga=GrADS(Bin='gradsc',%s)"%arg)

def gradsnc (self, arg):
    ip_Exec(self,"from grads import GrADS; ga=GrADS(Bin='gradsnc',%s)"%arg)

def gradshdf (self, arg):
    ip_Exec(self,"from grads import GrADS; ga=GrADS(Bin='gradshdf',%s)"%arg)

def gacbarn (self,arg):
    ip_Exec(self,"ga.cmd('run cbarn')")
 
def gaclear (self,arg):
    ip_Exec(self,"ga.cmd('clear')")
 
def gacmd (self, arg):
    if arg == "":
        print 'Entering classic mode; type "." to return to pygrads'
        cmd = raw_input("ga-> ")
        while cmd != ".":
            try:
                ip_Exec(self,"ga.cmd('%s')"%cmd)
            except:
                pass
            cmd = raw_input("ga-> ")
        print 'Returning to pygrads...'
    else:
       ip_Exec(self,"ga.cmd('%s')"%arg)
 
def gadefine (self, arg):
    ip_Exec(self,"ga.cmd('define %s')"%arg)
 
def gaenable (self, arg):
    ip_Exec(self,"ga.cmd('enable %s')"%arg)

def gadisable (self, arg):
    ip_Exec(self,"ga.cmd('disable %s')"%arg)

def gadisplay (self, arg):
    ip_Exec(self,"ga.cmd('display %s')"%arg)

def gaimexp (self, arg):
    ip_Exec(self,"ga.imexp()")

def gadisplaym (self, arg):
    ip_Exec(self,"ga.cmd('display %s')"%arg)
    ip_Exec(self,"ga.imexp()")
    
def gaquery (self, arg):
    ip_Exec(self,"ga.cmd('query %s')"%arg)
 
def gapim (self, arg):
    ip_Exec(self,"ga.cmd('printim %s')"%arg)
 
def gayat (self, arg):
    ip_Exec(self,"ga.cmd('gxyat %s')"%arg)
 
def gapgx (self, arg=' '):
    ip_Exec(self,"ga.cmd('print %s')"%arg)
 
def gaopen (self, arg):
    ip_Exec(self,"ga.cmd('open %s')"%arg)
 
def gaOpen (self, arg):
    ip_Exec(self,"fh=ga.open('%s')"%arg)
 
def gaQuery (self, arg):
    ip_Exec(self,"qh=ga.query('%s')"%arg)
 
def gaprt (self, arg):
    ip_Exec(self,"print %s"%arg)

def gaqref (self, arg):
    text = """
Basic GrADS commands:

    clear/c, define, disable, display/d, draw, enable, 
    Open/o, Print/pp, printim/pim, Set/s, query/q, reinit 

    . $cmd     executes any GrADS command $cmd

    .          lonely "." enters "classic GrADS" mode

Convenient aliases:

    cb         run cbarn (for color bar script)
    sh         set gxout shaded
    yat        run gxyat

GrADS Methods:

    dm $name   displays $name in GrADS showing the resulting image in your
               Matplotlib window. This is equivalent to
                    ga.cmd('display $name')
                    ga.imexp()
    dd $name   runs the "imp" method, displaying a NumPy array in 
               GrADS; this is equivalent to 
                    ga.imp('<display>',$name)
    eof $name  compute EOF using Singular Value Decomposition; the
               *time* dimension contains the eofs; this equivalent to:
                $name,$name_d,$name_c = ga.eof('$name')
    ii $name   runs the "imp" method, importing a NumPy array into
               GrADS; this is equivalent to 
                     ga.imp("$name",$name)
    im         shows content of your GrADS graphics buffer in your
               Matplotlib canvas; same as
                     ga.imexp()
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
    ip_Exec(self,'print """%s"""'%text)

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

Now, if you would like to have your GrADS produced plot to appear on your
Matplotlib window enter:

   [] ga-> dm ts

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
    ip_Exec(self,'print """%s"""'%text)

 
def gareinit (self,arg):
    ip_Exec(self,"ga.cmd('reinit')")
 
def gashaded (self,arg):
    ip_Exec(self,"ga.cmd('set gxout shaded')")
 
def gaset (self, arg):
    ip_Exec(self,"ga.cmd('set %s')"%arg)

def gax (self, arg):
    ip_Exec(self,"%s = ga.exp('%s');lon=%s.grid.lon; lat=%s.grid.lat;lev=%s.grid.lev;time=%s.grid.time"%(arg,arg,arg,arg,arg,arg))

def gaeof (self, arg):
    ip_Exec(self,"%s, %s_s, %s_pc = ga.eof('%s');lon=%s.grid.lon; lat=%s.grid.lat;lev=%s.grid.lev;time=%s.grid.time"%(arg,arg,arg,arg,arg,arg,arg,arg))

def gai (self, arg):
    ip_Exec(self,"ga.imp('%s',%s)"%(arg,arg))

def gad (self, arg):
    ip_Exec(self,"ga.imp('<display>',%s)"%(arg))

# Expose the magic commands
def_Magic('grads',   grads_)
def_Magic('gradsc',  gradsc)
def_Magic('gradsnc', gradsnc)
def_Magic('gradshdf',gradshdf)
def_Magic('cb',       gacbarn)
def_Magic('c',       gaclear)
def_Magic('clear',   gaclear)
def_Magic('define',  gadefine)
def_Magic('d',       gadisplay)
def_Magic('dm',      gadisplaym)
def_Magic('im',      gaimexp)
def_Magic('imexp',   gaimexp)
def_Magic('display', gadisplay)
def_Magic('enable',  gaenable)
def_Magic('examples',  gaexample)
def_Magic('disable', gadisable)
def_Magic('.',       gacmd)
def_Magic('Open',    gaopen)
def_Magic('o',       gaopen)
def_Magic('oo',      gaOpen)
def_Magic('open',    gaopen)
def_Magic('pim',     gapim)
def_Magic('printim', gapim)
def_Magic('Print',   gapgx)
def_Magic('p',       gaprt)
def_Magic('pp',      gapgx)
def_Magic('yat',     gayat)
def_Magic('s',       gaset)
def_Magic('Set',     gaset)
def_Magic('sh',      gashaded)
def_Magic('q',       gaquery)
def_Magic('query',   gaquery)
def_Magic('qref',    gaqref)
def_Magic('qq',      gaQuery)
def_Magic('reinit',  gareinit)
def_Magic('xx',      gax)
def_Magic('ii',      gai)
def_Magic('dd',      gad)
def_Magic('eof',     gaeof)

# Retrieve GraDS options from environment (set by "pygrads" top script)
Bin   = os.getenv('GA_BIN',default='grads')
Cmd   = os.getenv('GA_CMD',default='')
Opts  = os.getenv('GA_OPT',default='')
Files = os.getenv('GA_FIL')

if Cmd!='':  Opts = '-c "'+Cmd+'" '+Opts
# if Opts=='': Opts=None

# Instantiate the GrADS object
# If someone has an alternative to making ga global,
# I'd like to know about it.
# --------------------------------------------------
global ga
if HAS_GAYA:
    ga = GaYa(Bin=Bin,Opts=Opts)
elif HAS_GALAB:
    ga = GaLab(Bin=Bin,Opts=Opts)
elif HAS_GANUM:
    ga = GaNum(Bin=Bin,Opts=Opts)
else:
    ga = GrADS(Bin=Bin,Opts=Opts)

# if you set up a Profile, then this should replace the banner, rather than being
# a print statement:
print """
   Welcome to PyGrADS, a GrADS-based iPython environment. 
   For more information, type 'help(ipygrads)'

?         -> Introduction and overview of IPython's features.
help      -> Python's own help system.
qref      -> PyGrADS quick reference
examples  -> Some PyGrADS examples
object?   -> Details about 'object'. ?object also works, ?? prints more.

"""

if Files:
    for file in Files.split(' '):
        try:
            fh = ga.open(file,Quiet=True)
            print "Successfully opened <%s> as File %d"%(file,fh.fid)
        except:
            print "Failed to open GrADS file <%s>"%file


