#! /usr/bin/env python
# Author: Izaak Neutelings (July 2019)
import time; start0 = time.time()
from TauPOG.TauIDSFs.TauIDSFTool import TauIDSFTool



def tauIDSFs(year=2017,id='MVAoldDM2017v2',wp='Tight'):
  sftool = TauIDSFTool(year,id,wp,dm=False)
  ptvals = [ 10, 15, 20, 21, 25, 26, 30, 31, 35, 40, 50, 70, 100, 200, 500, 1000, 1500, 2000, ]
  print ">>> SF for %s WP of %s in %s"%(wp,id,year)
  print ">>> "
  print ">>> %10s"%('var \ pt')+' '.join("%10.1f"%p for p in ptvals)
  print ">>> %10s"%("central") +' '.join("%10.5f"%sftool.getSFvsPT(p,5)        for p in ptvals)
  print ">>> %10s"%("up")      +' '.join("%10.5f"%sftool.getSFvsPT(p,5,'Up')   for p in ptvals)
  print ">>> %10s"%("down")    +' '.join("%10.5f"%sftool.getSFvsPT(p,5,'Down') for p in ptvals)
  print ">>> "
  


if __name__ == "__main__":
  for wp in ['Loose','Medium','Tight']:
    tauIDSFs(wp=wp)
  print ">>> done after %.1f seconds"%(time.time()-start0)
