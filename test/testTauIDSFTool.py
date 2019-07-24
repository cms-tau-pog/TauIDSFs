#! /usr/bin/env python
# Author: Izaak Neutelings (July 2019)
import time; start0 = time.time()
from TauPOG.TauIDSFs.TauIDSFTool import TauIDSFTool
start1 = time.time()



def printSFTable(year=2017,id='MVAoldDM2017v2',wp='Tight',dm=False):
  sftool = TauIDSFTool(year,id,wp,dm=dm)
  if dm:
    dmvals = [0,1,5,6,10,11]
    for pt in [25,50]:
      print ">>> "
      print ">>> SF for %s WP of %s in %s with pT = %s GeV"%(wp,id,year,pt)
      print ">>> "
      print ">>> %10s"%('var \ DM')+''.join("%10d"%dm for dm in dmvals)
      print ">>> %10s"%("central") +''.join("%10.6f"%sftool.getSFvsDM(pt,dm,5)        for dm in dmvals)
      print ">>> %10s"%("up")      +''.join("%10.6f"%sftool.getSFvsDM(pt,dm,5,'Up')   for dm in dmvals)
      print ">>> %10s"%("down")    +''.join("%10.6f"%sftool.getSFvsDM(pt,dm,5,'Down') for dm in dmvals)
      print ">>> "
      ###sftool.getSFvsPT(pt,5)     # results in an error
      ###sftool.getSFvsEta(1.5,1,5) # results in an error
  else:
      ptvals = [10,20,21,25,26,30,31,35,40,50,70,100,200,500,600,700,800,1000,1500,2000,]
      print ">>> "
      print ">>> SF for %s WP of %s in %s"%(wp,id,year)
      print ">>> "
      print ">>> %10s"%('var \ pt')+''.join("%10.1f"%pt for pt in ptvals)
      print ">>> %10s"%("central") +''.join("%10.6f"%sftool.getSFvsPT(pt,5)        for pt in ptvals)
      print ">>> %10s"%("up")      +''.join("%10.6f"%sftool.getSFvsPT(pt,5,'Up')   for pt in ptvals)
      print ">>> %10s"%("down")    +''.join("%10.6f"%sftool.getSFvsPT(pt,5,'Down') for pt in ptvals)
      print ">>> "
      ###sftool.getSFvsDM(25,1,5)   # results in an error
      ###sftool.getSFvsEta(1.5,1,5) # results in an error
  


if __name__ == "__main__":  
  print ">>> "
  print ">>> start test tau ID SF tool"
  start2 = time.time()
  for dm in [True, False]:
    for wp in ['Loose','Medium','Tight']:
      printSFTable(wp=wp,dm=dm)
  start3 = time.time()
  print ">>> "
  print ">>> done after %.1f seconds (%.1f for imports, %.1f for loops)"%(time.time()-start0,start1-start0,start3-start2)
  

