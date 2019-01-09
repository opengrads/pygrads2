#!python
"""Windows-specific part of the installation. Adapted from IPython's
   post-install script. """

import os, sys, shutil

try:
    import IPython
    has_ipython = True
except ImportError:
    has_ipython = False

def mkshortcut(target,description,link_file,*args,**kw):
    """make a shortcut if it doesn't exist, and register its creation"""
    
    create_shortcut(target, description, link_file,*args,**kw)
    file_created(link_file)

def install_19():
    """Routine to be run by the win32 installer with the -install switch."""

    # Get some system constants
    prefix = sys.prefix
    python = prefix + r'\python.exe'

    # Lookup path to common startmenu ...
    ip_dir = get_special_folder_path('CSIDL_COMMON_PROGRAMS') + r'\PyGrADS for GrADS 1.9'

    ix11_dir = ip_dir + r'\IPython (Graphics)'
    ibat_dir = ip_dir + r'\IPython (Batch)'
    
    px11_dir = ip_dir + r'\Python (Graphics)'
    pbat_dir = ip_dir + r'\Python (Batch)'
    
    # Some usability warnings at installation time.  I don't want them at the
    # top-level, so they don't appear if the user is uninstalling.

    if has_ipython is False:
        print ('To take full advantage of PyGrADS, you need IPython from:\n'
               'http://ipython.scipy.org/')

    try:
        import ctypes
    except ImportError:
        print ('To take full advantage of PyGrADS, you need ctypes from:\n'
               'http://sourceforge.net/projects/ctypes')

    try:
        import win32con
    except ImportError:
        print ('To take full advantage of PyGrADS, you need pywin32 from:\n'
               'http://starship.python.net/crew/mhammond/win32/Downloads.html')

    try:
        import readline
    except ImportError:
        print ('To take full advantage of PyGrADS, you need readline from:\n'
               'http://sourceforge.net/projects/uncpythontools')

    # Create PyGrADS entry directories ...
    for dir in [ ip_dir, ix11_dir, ibat_dir, px11_dir, pbat_dir ]:
        if not os.path.isdir(dir):
            os.mkdir(dir)
            directory_created(dir)

    # Create program shortcuts: IPyGrADS ...

    f = ip_dir + r'\PyGrADS.lnk'
    a = prefix + r'\scripts\pygrads -d'
    mkshortcut(python,'Python Interface to GrADS 1.9',f,a)

    f = ix11_dir + r'\HDF (Landscape).lnk'
    a = prefix + r'\scripts\pygrads -H'
    mkshortcut(python,'Python Interface to GrADS 1.9',f,a)

    f = ix11_dir + r'\NetCDF OPeNDAP (Landscape).lnk'
    a = prefix + r'\scripts\pygrads -d'
    mkshortcut(python,'Python Interface to GrADS 1.9',f,a)
    mkshortcut(python,'Python Interface to GrADS 1.9',f,a)

    f = ix11_dir + r'\HDF (Portrait).lnk'
    a = prefix + r'\scripts\pygrads -Hp'
    mkshortcut(python,'Python Interface to GrADS 1.9',f,a)

    f = ix11_dir + r'\NetCDF OPeNDAP (Portrait).lnk'
    a = prefix + r'\scripts\pygrads -dp'
    mkshortcut(python,'Python Interface to GrADS 1.9',f,a)

    f = ibat_dir + r'\HDF (Landscape).lnk'
    a = prefix + r'\scripts\pygrads -Hb'
    mkshortcut(python,'Python Interface to GrADS 1.9',f,a)
    f = ibat_dir + r'\NetCDF OPeNDAP (Landscape).lnk'
    a = prefix + r'\scripts\pygrads -db'
    mkshortcut(python,'Python Interface to GrADS 1.9',f,a)

    f = ibat_dir + r'\HDF (Portrait).lnk'
    a = prefix + r'\scripts\pygrads -Hbp'
    mkshortcut(python,'Python Interface to GrADS 1.9',f,a)
    f = ibat_dir + r'\NetCDF OPeNDAP (Portrait).lnk'
    a = prefix + r'\scripts\pygrads -dbp'
    mkshortcut(python,'Python Interface to GrADS 1.9',f,a)

    # Create program shortcuts: Classic Python...

    f = px11_dir + r'\HDF (Landscape).lnk'
    a = '-i -c"import sys;from grads import *; ga = GrADS(Bin=\'gradshdf\',Window=True,Port=False); sys.ps1=\'ga->>> \'; print \'Running GrADS under the classic Python shell; ga object is callable.\'; print \'Example: ga(%s)\'; print "'%r"\'q config\'"
    mkshortcut(python,'PyGrADS: Classic Python Shell',f,a)
    
    f = px11_dir + r'\NetCDF OPeNDAP (Landscape).lnk'
    a = '-i -c"import sys;from grads import *; ga = GrADS(Bin=\'gradsdods\',Window=True,Port=False); sys.ps1=\'ga->>> \'; print \'Running GrADS under the classic Python shell; ga object is callable.\'; print \'Example: ga(%s)\'; print "'%r"\'q config\'"
    mkshortcut(python,'PyGrADS: Classic Python Shell',f,a)

    f = px11_dir + r'\HDF (Portrait).lnk'
    a = '-i -c"import sys;from grads import *; ga = GrADS(Bin=\'gradshdf\',Window=True,Port=True); sys.ps1=\'ga->>> \'; print \'Running GrADS under the classic Python shell; ga object is callable.\'; print \'Example: ga(%s)\'; print "'%r"\'q config\'"
    mkshortcut(python,'PyGrADS: Classic Python Shell',f,a)
    f = px11_dir + r'\NetCDF OPeNDAP (Portrait).lnk'
    a = '-i -c"import sys;from grads import *; ga = GrADS(Bin=\'gradsdods\',Window=True,Port=True); sys.ps1=\'ga->>> \'; print \'Running GrADS under the classic Python shell; ga object is callable.\'; print \'Example: ga(%s)\'; print "'%r"\'q config\'"
    mkshortcut(python,'PyGrADS: Classic Python Shell',f,a)

    f = pbat_dir + r'\HDF (Landscape).lnk'
    a = '-i -c"import sys;from grads import *; ga = GrADS(Bin=\'gradshdf\',Window=False,Port=False); sys.ps1=\'ga->>> \'; print \'Running GrADS under the classic Python shell; ga object is callable.\'; print \'Example: ga(%s)\'; print "'%r"\'q config\'"
    mkshortcut(python,'PyGrADS: Classic Python Shell',f,a)
    f = pbat_dir + r'\NetCDF OPeNDAP (Landscape).lnk'
    a = '-i -c"import sys;from grads import *; ga = GrADS(Bin=\'gradsdods\',Window=False,Port=False); sys.ps1=\'ga->>> \'; print \'Running GrADS under the classic Python shell; ga object is callable.\'; print \'Example: ga(%s)\'; print "'%r"\'q config\'"
    mkshortcut(python,'PyGrADS: Classic Python Shell',f,a)

    f = pbat_dir + r'\HDF (Portrait).lnk'
    a = '-i -c"import sys;from grads import *; ga = GrADS(Bin=\'gradshdf\',Window=False,Port=True); sys.ps1=\'ga->>> \'; print \'Running GrADS under the classic Python shell; ga object is callable.\'; print \'Example: ga(%s)\'; print "'%r"\'q config\'"
    mkshortcut(python,'PyGrADS: Classic Python Shell',f,a)
    f = pbat_dir + r'\NetCDF OPeNDAP (Portrait).lnk'
    a = '-i -c"import sys;from grads import *; ga = GrADS(Bin=\'gradsdods\',Window=False,Port=True); sys.ps1=\'ga->>> \'; print \'Running GrADS under the classic Python shell; ga object is callable.\'; print \'Example: ga(%s)\'; print "'%r"\'q config\'"
    mkshortcut(python,'PyGrADS: Classic Python Shell',f,a)

    # TO DO: Create documentation shortcuts ...    

    # make pygrads.py
    shutil.copy(prefix + r'\scripts\pygrads', prefix + r'\scripts\pygrads.py')

    print 'PyGrADS for GrADS 1.9 sucessfully installed.'    

#.....................................................................................................

def install_20():
    """Routine to be run by the win32 installer with the -install switch."""

    # Get some system constants
    prefix = sys.prefix
    python = prefix + r'\python.exe'

    # Lookup path to common startmenu ...
    ip_dir = get_special_folder_path('CSIDL_COMMON_PROGRAMS') + r'\PyGrADS for GrADS 2.0'

    ix11_dir = ip_dir + r'\IPython (Graphics)'
    ibat_dir = ip_dir + r'\IPython (Batch)'
    
    px11_dir = ip_dir + r'\Python (Graphics)'
    pbat_dir = ip_dir + r'\Python (Batch)'
    
    # Some usability warnings at installation time.  I don't want them at the
    # top-level, so they don't appear if the user is uninstalling.

    if has_ipython is False:
        print ('To take full advantage of PyGrADS, you need IPython from:\n'
               'http://ipython.scipy.org/')

    try:
        import ctypes
    except ImportError:
        print ('To take full advantage of PyGrADS, you need ctypes from:\n'
               'http://sourceforge.net/projects/ctypes')

    try:
        import win32con
    except ImportError:
        print ('To take full advantage of PyGrADS, you need pywin32 from:\n'
               'http://starship.python.net/crew/mhammond/win32/Downloads.html')

    try:
        import readline
    except ImportError:
        print ('To take full advantage of PyGrADS, you need readline from:\n'
               'http://sourceforge.net/projects/uncpythontools')

    # Create PyGrADS entry directories ...
    for dir in [ ip_dir, ix11_dir, ibat_dir, px11_dir, pbat_dir ]:
        if not os.path.isdir(dir):
            os.mkdir(dir)
            directory_created(dir)

    # Create program shortcuts: IPyGrADS ...

    f = ip_dir + r'\PyGrADS.lnk'
    a = prefix + r'\scripts\pygrads -D'
    mkshortcut(python,'Python Interface to GrADS 2.0',f,a)

    f = ix11_dir + r'\Landscape.lnk'
    a = prefix + r'\scripts\pygrads -D'
    mkshortcut(python,'Python Interface to GrADS 2.0',f,a)

    f = ix11_dir + r'\Portrait.lnk'
    a = prefix + r'\scripts\pygrads -Dp'
    mkshortcut(python,'Python Interface to GrADS 2.0',f,a)

    f = ibat_dir + r'\Landscape.lnk'
    a = prefix + r'\scripts\pygrads -Db'
    mkshortcut(python,'Python Interface to GrADS 2.0',f,a)

    f = ibat_dir + r'\Portrait.lnk'
    a = prefix + r'\scripts\pygrads -Dbp'
    mkshortcut(python,'Python Interface to GrADS 2.0',f,a)

    # Create program shortcuts: Classic Python...

    f = px11_dir + r'\Landscape.lnk'
    a = '-i -c"import sys;from grads import *; ga = GrADS(Bin=\'gradsdap\',Window=True,Port=False); sys.ps1=\'ga->>> \'; print \'Running GrADS under the classic Python shell; ga object is callable.\'; print \'Example: ga(%s)\'; print "'%r"\'q config\'"
    mkshortcut(python,'PyGrADS: Classic Python Shell',f,a)

    f = px11_dir + r'\Portrait.lnk'
    a = '-i -c"import sys;from grads import *; ga = GrADS(Bin=\'gradsdap\',Window=True,Port=True); sys.ps1=\'ga->>> \'; print \'Running GrADS under the classic Python shell; ga object is callable.\'; print \'Example: ga(%s)\'; print "'%r"\'q config\'"
    mkshortcut(python,'PyGrADS: Classic Python Shell',f,a)

    f = pbat_dir + r'\Landscape.lnk'
    a = '-i -c"import sys;from grads import *; ga = GrADS(Bin=\'gradsdap\',Window=False,Port=False); sys.ps1=\'ga->>> \'; print \'Running GrADS under the classic Python shell; ga object is callable.\'; print \'Example: ga(%s)\'; print "'%r"\'q config\'"
    mkshortcut(python,'PyGrADS: Classic Python Shell',f,a)

    f = pbat_dir + r'\Portrait.lnk'
    a = '-i -c"import sys;from grads import *; ga = GrADS(Bin=\'gradsdap\',Window=False,Port=True); sys.ps1=\'ga->>> \'; print \'Running GrADS under the classic Python shell; ga object is callable.\'; print \'Example: ga(%s)\'; print "'%r"\'q config\'"
    mkshortcut(python,'PyGrADS: Classic Python Shell',f,a)

    # TO DO: Create documentation shortcuts ...    

    # make pygrads.py
    shutil.copy(prefix + r'\scripts\pygrads', prefix + r'\scripts\pygrads.py')

    print 'PyGrADS for GrADS 2.0 sucessfully installed.'    

#.....................................................................................................

def remove():
    """Routine to be run by the win32 installer with the -remove switch."""
    pass

# main()

if len(sys.argv) > 1:
    if sys.argv[1] == '-install':
        install_19()
        install_20()
    elif sys.argv[1] == '-remove':
        remove()
    else:
        print "Script was called with option %s" % sys.argv[1]
