#!/usr/bin/env python

"""
  GaNum example collection. Notice that the classes deriving from
  the base class *Examples* do not redefine __init__(); instead,
  the derived classes define their own method startup().
"""

from grads    import *
from examples import *

sys.path.insert(0,'..')

class GaNumExamples(Examples):
    """
    Generic NumExamples.
    """
    def setup(self,name):
        ga.open(self.file)
        ga('set gxout shaded')

    def teardown(self,name):
        ga.cmd("reinit")

class ModelFileExamples(GaNumExamples):
    """
    A set of examples using the classic "model.nc" file.
    """

    def startup(self):
        self.file = self.DataDir + '/model.nc'

    def ex_export(self):

        ga('set t 1')
        ga('set z 1')
        ts = ga.exp('ts')

        ga('set t 1 5')
        ts = ga.exp('ts')

        ga('set z 1 7')
        ua = ga.exp('ua')

    def ex_import(self):

        ga('set t 1')
        ga('set z 1')
        ts = ga.exp('ts') - 273.0
        ga.imp('ts1',ts)

        ga('set t 1 5')
        ts = ga.exp('ts')  - 273.0
        ga.imp('ts2',ts)

        ga('set z 1 7')
        ua = ga.exp('ua') 
        ga.imp('ts3',ua)

        ga('set t 3')
        ga('set z 4')
        ga.imp('ts3',ua)

    def ex_display_ts(self):
        ga('set t 1')
        ga('set z 1')
        ts = ga.exp('ts') - 273.0
        ga.imp('<display>',ts)
        ga('draw title Surface Temperature at t=1')
        ga('printim ex_display_ts.png')

    def ex_display_ps(self):
        ga('set t 1 5')
        ps = ga.exp('ps') 
        ga('set t 5')
        ga.imp('<display>',ps)
        ga('draw title Surface Pressure at t=5')
        ga('printim ex_display_ps.png')

    def ex_display_ua(self):
        ga('set t 1 5')
        ga('set z 1 7')
        ua = ga.exp('ua')
        ga('set t 3')
        ga('set z 7')
        ga.imp('<display>',ua)
        ga('draw title Zonal Wind at t=3, z=4')
        ga('printim ex_display_ua.png')

    def ex_diff_ua(self):
        ga('set t 1 5')
        ga('set z 1 7')
        ua = ga.exp('ua')
        ga.imp('uadef',ua)
        ga('set t 3')
        ga('set z 7')
        ga('display ua - uadef')
        ga('draw title Zonal Wind: Imported minus Original')
        ga('printim ex_diff_ua.png')

    def ex_lsq(self):
        y_expr = '0.25*ua + 0.75*va + zg/1000'
        x_exprs = ('ua','va','zg')

        ga('set z 7')
        
        c, info = ga.lsq(y_expr, x_exprs)
        y_lsq = '%f * ua + %f * va + %f * zg'%(c[0],c[1],c[2])

        ga('define y1 = %s'%y_expr)
        ga('define y2 = %s'%y_lsq)
        ga('set gxout contour')
        ga('display y1')
        ga('display y2')
        ga('draw title In: %s \ Lsq: %s'%(y_expr,y_lsq))
        ga('printim ex_lsq.png')

class SlpFileExamples(GaNumExamples):
    """
    A set of examples using the "slp_djf.nc" file.
    """

    def startup(self):
        self.file = self.DataDir + '/slp_djf.nc'

    def ex_eof(self):
        ga('set t 1 41')
        v, d, c = ga.eof('djfslp')
        ga('set t 1')
        ga.imp('<display>',v)
        ga('draw title NAO Pattern')
        ga('printim ex_eof.png')

#.........................................................................

if __name__ == "__main__":

    global ga

#   Start GrADS
#   -----------
    ga = GaNum(Bin='grads',Window=False,Echo=False)

#   Create example instances
#   ------------------------
    ex_modl = ModelFileExamples()
    ex_eofs = SlpFileExamples()

#   Actually run them
#   -----------------
    DryRun = False
    ex_eofs('*all*',DryRun)
    ex_modl('*all*',DryRun)

#   Summarize results
#   -----------------
    Report()
