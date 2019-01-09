#!/usr/bin/env python

"""
  GaLab example collection. Notice that the classes deriving from
  the base class *Examples* do not redefine __init__(); instead,
  the derived classes define their own method startup().
"""

from matplotlib.pyplot import * 
from PIL               import Image

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
        ga.cmd("reinit")

class BlueMarbleExamples(GaLabExamples):
    """
    Examples based on the Blue Marble image.
    """

    def startup(self):
        self.file = self.DataDir + '/model.nc'

    def ex_proj_cyl(self):
        ga.basemap('cyl')
        ga.blue_marble(Show=True)
        title("Blue Marble Background (MODIS)")

    def ex_proj_geos(self):
        ga.basemap('geos',opts=-75.) # GOES East
        bm = ga.blue_marble()
        ga.map.imshow(bm,)
        title("Geostationary Projection (GOES East)")

    def ex_proj_stereo(self):

        subplot(211)
        ga.basemap('nps') 
        ga.blue_marble(Show=True)
        title("Northern Stereographic Projection")

        subplot(212)
        ga.basemap('sps') 
        ga.blue_marble(Show=True)
        title("Southern Stereographic Projection")

    def ex_proj_orthographic(self):
        ga.basemap('ortho',opts=(20.,0.)) 
        ga.blue_marble(Show=True)
        title("Orthographic Projection (Equator)")

    def ex_proj_polar_orthographic(self):

        subplot(211)
        ga.basemap('npo') 
        ga.blue_marble(Show=True)
        title("Orthographic Projection (North Pole)")

        subplot(212)
        ga.basemap('spo') 
        ga.blue_marble(Show=True)
        title("Orthographic Projection (South Pole)")

class ModelFileExamples(GaLabExamples):
    """
    A set of examples plotting data from the classic "model.nc" file.
    """

    def startup(self):
        self.file = self.DataDir + '/model.nc'

    def ex_imshow(self):
        ga.imshow('ts-273')
        title('Surface Temperature (Celsius)')

    def ex_colormaps(self):
        ga.imshow('ts-273',cmap=cm.hot,sub=211)
        title('Surface Temperature (Celsius)')
        ga.imshow('ts-273',cmap=cm.gray,sub=212)

    def ex_pcolor(self):
        ga.pcolor('ps/100')
        title('Surface Pressure (hPa)')

    def ex_implain(self):
        ga.implain('ps')

    def ex_contour(self):
        ga.cmd('set lev 300')
        ga.contourf('zg',clines=True,sub=211)
        title('300 hPa Heights')
        ga.contour('zg',N=10,sub=212)

class AeroFileExamples(GaLabExamples):
    """
    A set of examples plotting data from the "aero.nc" file.
    """

    def startup(self):
        self.file = self.DataDir + '/aero.nc'

    def ex_marble_dust(self):
        ga.blue_marble('on')    # use Blue Marble background
        ga.basemap('latlon')
        ga.imshow('duexttau',cmap=gacm.hot_l)
        title("Mineral Dust Optical Thickness") 
        ga.blue_marble('off')  

    def ex_marble_h500(self):
        ga.blue_marble('on')    # use Blue Marble background
        ga.basemap('npo')
        ga.contour('h500',N=12)
        title("500 hPa Heights") 
        ga.blue_marble('off')  

    def ex_goes_fulldisk(self):
        sat = Image.open("goes_fulldisk.jpg")
        ga.basemap('geos',opts=-75.) # GOES East
        ga.imshow('duexttau',cmap=gacm.hot_l,bgim=sat,
                   mpcol='cyan',dlon=20,dlat=15)
        title("Mineral Dust Optical Thickness") 

    def ex_goes_conus(self):
        sat = Image.open("goes_conus.jpg")
        opts=(-109.65,14.23,-44.65,62.23,-75.) # image info
        ga.basemap('geos',opts=opts,resolution='l') 
        ga.contour('h500',bgim=sat,N=12,Map=False)
        title("500 hPa Heights") 

#.........................................................................

if __name__ == "__main__":

    global ga

#   Start GrADS
#   -----------
    ga = GaLab(Bin='grads',Window=False,Echo=False)

#   Create example instances
#   ------------------------
    ex_blue = BlueMarbleExamples()
    ex_aero = AeroFileExamples()
    ex_modl = ModelFileExamples()

#   Actually run them
#   -----------------
    DryRun = False
    ex_modl('*all*',DryRun)
    ex_aero('*all*',DryRun)
    ex_blue('*all*',DryRun)

#   Summarize results
#   -----------------
    Report()
