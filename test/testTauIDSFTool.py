#! /usr/bin/env python
# Author: Izaak Neutelings (July 2019)
import time; start0 = time.time()
from TauPOG.TauIDSFs.TauIDSFTool import TauIDSFTool, TauESTool, TauFESTool
start1 = time.time()

def green(string,**kwargs): return "\x1b[0;32;40m%s\033[0m"%string

def printSFTable(year,id,wp,vs='pt',emb=False,otherVSlepWP=False):
  assert vs in ['pt','dm','eta'], "'vs' argument should be pt', 'dm' or 'eta'!"
  dm = (vs=='dm')
  if emb and 'VSjet' not in id:
      print "SFs for ID '%s' not available for embedded samples. Skipping..."%id
      return
  sftool = TauIDSFTool(year,id,wp,dm=dm,emb=emb,otherVSlepWP=otherVSlepWP)
  if vs=='pt':
      ptvals = [10,20,21,25,26,30,31,35,40,50,70,100,200,500,600,700,800,1000,1500,2000,]
      print ">>> "
      print ">>> SF for %s WP of %s in %s"%(wp,green(id),year)
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
      print ">>> SF for %s WP of %s in %s with pT = %s GeV"%(wp,green(id),year,pt)
      print ">>> "
      print ">>> %10s"%('var \ DM')+''.join("%9d"%dm for dm in dmvals)
      print ">>> %10s"%("central") +''.join("%9.5f"%sftool.getSFvsDM(pt,dm,5)        for dm in dmvals)
      print ">>> %10s"%("up")      +''.join("%9.5f"%sftool.getSFvsDM(pt,dm,5,'Up')   for dm in dmvals)
      print ">>> %10s"%("down")    +''.join("%9.5f"%sftool.getSFvsDM(pt,dm,5,'Down') for dm in dmvals)
      print ">>> "
      ###sftool.getSFvsPT(pt,5)     # results in an error
      ###sftool.getSFvsEta(1.5,1,5) # results in an error
  elif vs=='eta':
    if emb:
      print "vsEta binned SFs not available for embedded samples. Skipping..."
      return
    etavals = [0,0.2,0.5,1.0,1.5,2.0,2.2,2.3,2.4]
    for genmatch in [1,2]:
      print ">>> "
      print ">>> SF for %s WP of %s in %s with genmatch %d"%(wp,green(id),year,genmatch)
      print ">>> "
      print ">>> %10s"%('var \ eta')+''.join("%9.3f"%eta for eta in etavals)
      print ">>> %10s"%("central")  +''.join("%9.5f"%sftool.getSFvsEta(eta,genmatch)        for eta in etavals)
      print ">>> %10s"%("up")       +''.join("%9.5f"%sftool.getSFvsEta(eta,genmatch,'Up')   for eta in etavals)
      print ">>> %10s"%("down")     +''.join("%9.5f"%sftool.getSFvsEta(eta,genmatch,'Down') for eta in etavals)
      print ">>> "
      ###sftool.getSFvsPT(pt,5)     # results in an error
      ###sftool.getSFvsEta(1.5,1,5) # results in an error
  

def printTESTable(year,id):
  testool = TauESTool(year,id)
  ptvals  = [25,102,175] #[25,30,102,170,175]
  dmvals  = [0,1,5,10,11]
  for pt in ptvals:
    print ">>> "
    print ">>> TES for '%s' ('%s') and pT = %s GeV"%(green(id),year,pt)
    print ">>> "
    print ">>> %10s"%('var \ DM')+''.join("%9d"%dm for dm in dmvals)
    print ">>> %10s"%("central") +''.join("%9.5f"%testool.getTES(pt,dm,5)        for dm in dmvals)
    print ">>> %10s"%("up")      +''.join("%9.5f"%testool.getTES(pt,dm,5,'Up')   for dm in dmvals)
    print ">>> %10s"%("down")    +''.join("%9.5f"%testool.getTES(pt,dm,5,'Down') for dm in dmvals)
    print ">>> "
  

def printFESTable(year):
  testool = TauFESTool(year)
  etas    = [0.5,2.0]
  dmvals  = [0,1,10]
  for eta in etas:
    print ">>> "
    print ">>> TES for eta = %.1f in '%s'"%(eta,year)
    print ">>> "
    print ">>> %10s"%('var \ DM')+''.join("%9d"%dm for dm in dmvals)
    print ">>> %10s"%("central") +''.join("%9.5f"%testool.getFES(eta,dm,1)        for dm in dmvals)
    print ">>> %10s"%("up")      +''.join("%9.5f"%testool.getFES(eta,dm,1,'Up')   for dm in dmvals)
    print ">>> %10s"%("down")    +''.join("%9.5f"%testool.getFES(eta,dm,1,'Down') for dm in dmvals)
    print ">>> "
  

if __name__ == "__main__":  
  print ">>> "
  print ">>> start test tau ID SF tool"
  
  testIDTool   = True #and False
  testTESTool  = True #and False
  testFESTool  = True #and False
  emb          = True and False
  otherVSlepWP = True and False
  
  start2       = time.time()
  years        = [
    '2016Legacy',
    '2017ReReco',
    '2018ReReco',
  ]
  tauIDs      = [
    #'MVAoldDM2017v2',
    'DeepTau2017v2p1VSjet',
    #'antiEleMVA6',
    #'antiMu3',
    'DeepTau2017v2p1VSmu',
    'DeepTau2017v2p1VSe'
  ]
  WPs         = [
    #'Loose',
    'Medium',
    #'Tight'
  ]
  for year in years:
    for id in tauIDs:
      vslist = ['eta'] if any(s in id for s in ['anti','VSe','VSmu']) else ['pt','dm']
      for vs in vslist:
        for wp in WPs:
          if 'antiMu' in id and wp=='Medium': continue
          if testIDTool:
            printSFTable(year,id,wp,vs,emb,otherVSlepWP)
    if testTESTool:
      for id in ['MVAoldDM2017v2','DeepTau2017v2p1VSjet']:
        printTESTable(year,id)
    if testFESTool:
      printFESTable(year)
  
  start3 = time.time()
  print ">>> "
  print ">>> done after %.1f seconds (%.1f for imports, %.1f for loops)"%(time.time()-start0,start1-start0,start3-start2)
  
