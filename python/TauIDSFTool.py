# Author: Izaak Neutelings (July 2019)
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/TauIDRecommendation13TeV
import os
from TauPOG.TauIDSFs import modulepath, ensureTFile
datapath = modulepath+"/../data"

class TauIDSFTool:
    
    def __init__(self, year, id='MVAoldDM2017v2', wp='Tight', dm=False):
        """Choose the IDs and WPs for SFs. For available tau IDs and WPs, check
        https://cms-nanoaod-integration.web.cern.ch/integration/master-102X/mc102X_doc.html#Tau"""
        
        assert year in [2016,2017,2018], "You must choose a year from 2016, 2017, or 2018."
        
        self.func_sf = { }
        self.hist_sf = { }
        if id in ['MVAoldDM2017v2']:
          if dm:
            file = ensureTFile("%s/TauIDSF_dm_%s_%d.root"%(datapath,id,year))
            self.hist_sf[None]   = file.Get("%s_cent"%(wp))
            self.hist_sf['Up']   = file.Get("%s_up"%(wp))
            self.hist_sf['Down'] = file.Get("%s_down"%(wp))
            self.hist_sf[None].SetDirectory(0)
            self.hist_sf['Up'].SetDirectory(0)
            self.hist_sf['Down'].SetDirectory(0)
            file.Close()
          else:
            file = ensureTFile("%s/TauIDSF_pt_%s_%d.root"%(datapath,id,year))
            self.func_sf[None]   = file.Get("%s_cent"%(wp))
            self.func_sf['Up']   = file.Get("%s_up"%(wp))
            self.func_sf['Down'] = file.Get("%s_down"%(wp))
            file.Close()
        else:
          raise IOError("Could not recognize tau ID '%s'!"%id)
        
    def getSFvsPT(self, pt, genmatch=5, unc=None):
        """Get tau ID SF vs. tau pT."""
        if genmatch==5:
          return self.func_sf[unc].Eval(pt)
        else:
          return 1.
        
    def getSFvsDM(self, pt, dm, genmatch=5, unc=None):
        """Get tau ID SF vs. tau pT."""
        if genmatch==5 and pt>40:
          bin = self.hist_sf[unc].GetXaxis().FindBin(dm)
          return self.hist_sf[unc].GetBinContent(bin)
        if pt<40:
          return 0.0
        