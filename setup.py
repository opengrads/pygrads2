import sys, glob, os

try:
    import setuptools
except:
    pass

from distutils.core import setup
from distutils.debug import DEBUG

if os.name == 'posix':
    os_name = 'posix'
elif os.name in ['nt','dos']:
    os_name = 'windows'
else:
    print 'Unsupported operating system:',os.name
    sys.exit(1)
    
DEBUG = True

scriptfiles = filter(os.path.isfile, ['pygrads'])
if 'bdist_wininst' in sys.argv:
    if len(sys.argv) > 2 and ('sdist' in sys.argv or 'bdist_rpm' in sys.argv):
        print >> sys.stderr,"ERROR: bdist_wininst must be run alone. Exiting."
        sys.exit(1)
    scriptfiles.append('scripts/pygrads_win_post_install.py')

setup(name='pygrads',
      version='1.2.0',
      description="GrADS Client Class and IPython Environment",
      long_description = 'The module "grads" implements an interface to the Grid Analysis and Display System (GrADS) by means of bi-directional pipes. Modules "ganum" and "galab" extend the basic GrADS client class with NumPy and Pylab/Matplotlib features. The script "pygrads" is a wrapper around IPython, providing an advanced python based command line interface for GrADS. PyGrads introduces several "magic commands" (shortcuts) for easily entering GrADS and Pylab commands.',
      author = 'Arlindo da Silva',
      author_email = 'dasilva@opengrads.org',
      maintainer = 'Arlindo da Silva',
      maintainer_email = 'dasilva@opengrads.org',
      url = 'http://opengrads.org',
      download_url = "http://sourceforge.net/projects/opengrads",
      scripts = scriptfiles,
      py_modules = ['ipygrads'],
      packages = ['grads'],
      package_data = { 'grads': ["data/*.jpg"]},
      license = "GPL",
      keywords = ["python","plotting","plots","graphs","charts",
                  "atmospheric data analysis", "climate data analysis",
                  "earth sciences", "meteorology", "oceanography",
                  "weather maps"],
      classifiers = [ "Development Status :: 4 - Beta",
	     "Intended Audience :: Science/Research", 
	     "License :: OSI Approved", 
	     "Topic :: Scientific/Engineering :: Visualization",
	     "Topic :: Software Development :: Libraries :: Python Modules",
	     "Operating System :: OS Independent"]
      )

