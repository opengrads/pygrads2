import sys, os

class Examples:
    """
    A base class for building examples.
    """

    PASS = 0
    FAIL = 0

    def __init__ (self, DataDir=None ):
        self.examples = [ x[3:] for x in self.__class__.__dict__.keys() \
                                if x.startswith("ex_") ]
        if DataDir is None:
            sample = 'model.grb'
            for dir in ( '.', 'data', '../data', '../../../data'):
                if os.path.exists(dir+'/'+sample):
                    DataDir = dir 
                    break
        self.DataDir = DataDir
        self.startup()

    def __call__ (self, name, DryRun=False):
        "Runs a particular example, opening a given data file"
        self.DryRun = DryRun
        if name=="*all*":  names = self.examples
        else:                names = [ name ]
        for name_ in names:
            sys.stdout.write("- Running example %s ... "%name_)
            if self.DryRun:
                sys.stdout.write("OK\n")
            else:
                try:
                    self.setup(name_)
                    getattr(self,'ex_'+name_)()
                    self.teardown(name_)
                    Examples.PASS += 1
                    sys.stdout.write("OK\n")
                except:
                    Examples.FAIL += 1
                    sys.stdout.write("FAILED\n")

    def startup(self):
        pass

    def setup(self,name):
        pass

    def teardown(self,name):
        pass

def Report():
    np = Examples.PASS
    nf = Examples.FAIL
    nt = np + nf
    if nt==0:
        print "Nothing to report: no examples have been run."
    elif nf==0:
        print "All %d examples completed sucessfully - check the plots."%nt
    elif np==0:
        print "All %d examples FAILED to complete."%nt
    else:
        pf = 100.*nf/float(nt)
        print "%d out of %d examples (%2.1f%%) FAILED to complete."%(nf,nt,pf)




