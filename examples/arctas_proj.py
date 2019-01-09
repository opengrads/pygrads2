#!/usr/bin/env python

"""
  GaLab example collection. Notice that the classes deriving from
  the base class *Examples* do not redefine __init__(); instead,
  the derived classes define their own method startup().
"""

from pylab import * 
from PIL   import Image

from grads    import *
from examples import *

sys.path.insert(0,'..')

class GaLabExamples(Examples):
    """
    Generic GaLabExamples.
    """
    def setup(self,name):
        if self.file != None: ga.open(self.file)
        ga.cmd('set lon -180 180')

    def teardown(self,name):
        savefig('ex_'+name+'.png')
        close(1)
        if self.file != None: ga.cmd("close 1")

class BlueMarbleExamples(GaLabExamples):
    """
    Examples based on the Blue Marble image.
    """

    def startup(self):
        self.file = self.DataDir + '/model.ctl'

    def ex_proj_stereo(self):

        ga.basemap('nps', opts=(-90.,40.)) 
        ga.blue_marble(Show=True)
        title("Northern Stereographic Projection")

    def ex_proj_polar_orthographic(self):

        ga.basemap('npo', opts=(-90.,90.)) 
        ga.blue_marble(Show=True)
        title("Orthographic Projection (North Pole)")


#.........................................................................

if __name__ == "__main__":

    global ga

#   Start GrADS
#   -----------
    ga = GaLab(Bin='gradsnc',Window=False,Echo=False)

#   Create example instances
#   ------------------------
    ex_blue = BlueMarbleExamples()

#   Actually run them
#   -----------------
    DryRun = False
    ex_blue('*all*',DryRun)
