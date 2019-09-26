#! /usr/bin/env python
# Author: Izaak Neutelings (July 2019)
import time; start0 = time.time()
from TauPOG.TauIDSFs.TauIDSFTool import TauIDSFTool
start1 = time.time()



def printSFTable(year,id,wp,vs='pt'):
  assert vs in ['pt','dm','eta'], "'vs' argument should be pt', 'dm' or 'eta'!"
  dm = (vs=='dm')
  sftool = TauIDSFTool(year,id,wp,dm=dm)
  if vs=='pt':
      ptvals = [10,20,21,25,26,30,31,35,40,50,70,100,200,500,600,700,800,1000,1500,2000,]
      print ">>> "
      print ">>> SF for %s WP of %s in %s"%(wp,id,year)
      print ">>> "
      print ">>> %10s"%('var \ pt')+''.join("%9.1f"%pt for pt in ptvals)
      print ">>> %10s"%("central") +''.join("%9.5f"%sftool.getSFvsPT(pt,5)        for pt in ptvals)
      print ">>> %10s"%("up")      +''.join("%9.5f"%sftool.getSFvsPT(pt,5,'Up')   for pt in ptvals)
      print ">>> %10s"%("down")    +''.join("%9.5f"%sftool.getSFvsPT(pt,5,'Down') for pt in ptvals)
      print ">>> "
      ###sftool.getSFvsDM(25,1,5)   # results in an error
      ###sftool.getSFvsEta(1.5,1,5) # results in an error
  elif vs=='dm':
    dmvals = [0,1,5,6,10,11]
    for pt in [25,50]:
      print ">>> "
      print ">>> SF for %s WP of %s in %s with pT = %s GeV"%(wp,id,year,pt)
      print ">>> "
      print ">>> %10s"%('var \ DM')+''.join("%9d"%dm for dm in dmvals)
      print ">>> %10s"%("central") +''.join("%9.5f"%sftool.getSFvsDM(pt,dm,5)        for dm in dmvals)
      print ">>> %10s"%("up")      +''.join("%9.5f"%sftool.getSFvsDM(pt,dm,5,'Up')   for dm in dmvals)
      print ">>> %10s"%("down")    +''.join("%9.5f"%sftool.getSFvsDM(pt,dm,5,'Down') for dm in dmvals)
      print ">>> "
      ###sftool.getSFvsPT(pt,5)     # results in an error
      ###sftool.getSFvsEta(1.5,1,5) # results in an error
  elif vs=='eta':
    etavals = [0,0.2,0.5,1.0,1.5,2.0,2.2,2.3,2.4]
    for genmatch in [1,2]:
      print ">>> "
      print ">>> SF for %s WP of %s in %s with genmatch %d"%(wp,id,year,genmatch)
      print ">>> "
      print ">>> %10s"%('var \ eta')+''.join("%9.3f"%eta for eta in etavals)
      print ">>> %10s"%("central")  +''.join("%9.5f"%sftool.getSFvsEta(eta,genmatch)        for eta in etavals)
      print ">>> %10s"%("up")       +''.join("%9.5f"%sftool.getSFvsEta(eta,genmatch,'Up')   for eta in etavals)
      print ">>> %10s"%("down")     +''.join("%9.5f"%sftool.getSFvsEta(eta,genmatch,'Down') for eta in etavals)
      print ">>> "
      ###sftool.getSFvsPT(pt,5)     # results in an error
      ###sftool.getSFvsEta(1.5,1,5) # results in an error
  


if __name__ == "__main__":  
  print ">>> "
  print ">>> start test tau ID SF tool"
  start2 = time.time()
  years  = [2017] # [2016,2017,2018]
  ids    = ['MVAoldDM2017v2','DeepTau2017v2p1','antiEleMVA6','antiMu3']
  for year in years:
    for id in ids:
      vslist = ['eta'] if 'anti' in id else [ 'pt', 'dm' ]
      for vs in vslist:
        for wp in ['Loose','Medium','Tight']:
          if 'antiMu' in id and wp=='Medium': continue
          printSFTable(year,id,wp,vs)
  start3 = time.time()
  print ">>> "
  print ">>> done after %.1f seconds (%.1f for imports, %.1f for loops)"%(time.time()-start0,start1-start0,start3-start2)
  

