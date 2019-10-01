# Author: Izaak Neutelings (September 2019)
# Description: Create root files with SFs for the anti-lepton discriminators
import os
from array import array
from collections import namedtuple
from ROOT import TFile, TH1F, kFullDotLarge

SF  = namedtuple('SF',['val','unc'])
SF1 = SF(1,0) # default


def createSFTH1(histname,sflist,etabins):
  """Create histogram from SF list."""
  print ">>>   Creating hisogram '%s'..."%histname
  nxbins = len(etabins)-1
  xbins  = array('d',list(etabins))
  hist   = TH1F(histname,histname,nxbins,xbins)
  hist.GetYaxis().SetTitle("SF")
  hist.GetXaxis().SetTitle("#tau_{h} |#eta|")
  hist.GetXaxis().SetLabelSize(0.04)
  hist.GetYaxis().SetLabelSize(0.04)
  hist.GetXaxis().SetTitleSize(0.05)
  hist.GetYaxis().SetTitleSize(0.05)
  hist.GetXaxis().SetTitleOffset(0.90)
  hist.SetMinimum(0)
  hist.SetLineWidth(2)
  hist.SetMarkerStyle(kFullDotLarge)
  hist.SetMarkerSize(0.8)
  hist.SetOption('PEHIST')
  sflist = list(sflist)
  while len(sflist)<len(etabins):
    sflist.append(sflist[-1])
  for i, sf in enumerate(sflist,1):
    if i>nxbins:
      binstr = "[%4.2f, inf]"%(hist.GetXaxis().GetBinLowEdge(i))
      ofstr  = "(overflow)"
    else:
     binstr = "[%4.2f,%4.2f]"%(hist.GetXaxis().GetBinLowEdge(i),hist.GetXaxis().GetBinUpEdge(i))
     ofstr  = ""
    print ">>>     Bin %s, %s:  SF = %6.3f +- %.3f %s"%(i,binstr,sf.val,sf.unc,ofstr)
    hist.SetBinContent(i,sf.val)
    hist.SetBinError(i,sf.unc)
  return hist
  

def createSFFile(filename,sftable,etabins):
  """Create histogram from table."""
  print ">>> Creating '%s'..."%filename
  file = TFile(filename,'RECREATE')
  for wp in sorted(sftable,key=wporder):
    print ">>>  %s working point"%wp
    histname = wp
    sflist   = sftable[wp]
    hist     = createSFTH1(histname,sflist,etabins)
    hist.Write(histname,TH1F.kOverwrite)
  file.Close()
  return file
  

def wporder(key):
  """Custom ordering of WPs."""
  key   = key.lower()
  order = ['loose','medium','tight']
  if key.replace('v','') in order:
    index = order.index(key.replace('v','')) - key.count('v')*('loose' in key) + key.count('v')*('tight' in key)
  else:
    index = 100
  return index
  

def main():
  
  outdir = "../data"
  antiEleEtaBins = ( 0.0, 1.460, 1.558, 2.3 )
  antiMuEtaBins = ( 0.0, 0.4, 0.8, 1.2, 1.7, 2.3 )
  antiLepSFs = { }
  antiLepSFs['antiEleMVA6'] = {
    '2016Legacy': { # https://indico.cern.ch/event/828205/contributions/3468902/attachments/1863558/3063927/EtoTauFRLegacy16.pdf
      'VLoose': ( SF(1.175,0.003), SF1, SF(1.288,0.006), SF1 ), # LEGACY
      'Loose':  ( SF(1.38, 0.011), SF1, SF(1.24, 0.05 ), SF1 ),
      'Medium': ( SF(1.88, 0.04 ), SF1, SF(1.11, 0.10 ), SF1 ),
      'Tight':  ( SF(2.16, 0.10 ), SF1, SF(0.91, 0.20 ), SF1 ),
      'VTight': ( SF(2.04, 0.16 ), SF1, SF(0.78, 0.31 ), SF1 ),
    },
    '2017ReReco': { # https://twiki.cern.ch/twiki/bin/viewauth/CMS/TauIDRecommendation13TeV#Electron_to_tau_fake_rate
      'VLoose': ( SF(1.09,0.01), SF1, SF(1.19,0.01), SF1 ),
      'Loose':  ( SF(1.17,0.04), SF1, SF(1.25,0.06), SF1 ),
      'Medium': ( SF(1.40,0.12), SF1, SF(1.21,0.26), SF1 ),
      'Tight':  ( SF(1.80,0.20), SF1, SF(1.53,0.60), SF1 ),
      'VTight': ( SF(1.96,0.27), SF1, SF(1.66,0.80), SF1 ),
    },
    '2018ReReco': { # https://indico.cern.ch/event/831606/contributions/3483937/attachments/1871414/3079821/EtoTauFR2018-updated.pdf
      'VLoose': ( SF(1.130,0.005), SF1, SF(1.003,0.005), SF1 ), # PRELIMINARY
      'Loose':  ( SF(1.229,0.018), SF1, SF(0.926,0.015), SF1 ),
      'Medium': ( SF(1.36, 0.004), SF1, SF(0.91, 0.05 ), SF1 ),
      'Tight':  ( SF(1.46, 0.008), SF1, SF(1.02, 0.14 ), SF1 ),
      'VTight': ( SF(1.56, 0.16 ), SF1, SF(1.03, 0.24 ), SF1 ),
    },
  }
  antiLepSFs['antiMu3'] = {
    '2016Legacy': { # https://twiki.cern.ch/twiki/bin/viewauth/CMS/TauIDRecommendation13TeV#Muon_to_tau_fake_rate
      'Loose': ( SF(1.146,0.50), SF(1.084,0.50), SF(1.218,0.50), SF(1.490,0.50), SF(2.008,0.50), SF1 ), # WRONG; TO BE UPDATED
      'Tight': ( SF(1.470,0.50), SF(1.367,0.50), SF(1.251,0.50), SF(1.770,0.50), SF(1.713,0.50), SF1 ),
    },
    '2017ReReco': { # https://twiki.cern.ch/twiki/bin/viewauth/CMS/TauIDRecommendation13TeV#Muon_to_tau_fake_rate
      'Loose': ( SF(1.06,0.05), SF(1.02,0.04), SF(1.10,0.04), SF(1.03,0.18), SF(1.94,0.35), SF1 ),
      'Tight': ( SF(1.17,0.12), SF(1.29,0.30), SF(1.14,0.05), SF(0.93,0.60), SF(1.61,0.60), SF1 ),
    },
    '2018ReReco': { # https://indico.cern.ch/event/814232/contributions/3397978/attachments/1831354/2999219/mu-tau_FR_2018.pdf
      'Loose': ( SF(1.05,0.05), SF(0.96,0.04), SF(1.06,0.05), SF(1.45,0.08), SF(1.75,0.16), SF1 ),
      'Tight': ( SF(1.23,0.05), SF(1.37,0.18), SF(1.12,0.04), SF(1.84,0.32), SF(2.01,0.43), SF1 ),
    },
  }
  
  for id in antiLepSFs:
    for year in antiLepSFs[id]:
      filename = "%s/TauID_SF_eta_%s_%s.root"%(outdir,id,year)
      sftable  = antiLepSFs[id][year]
      etabins  = antiEleEtaBins if 'antiEle' in id else antiMuEtaBins
      createSFFile(filename,sftable,etabins)
  

if __name__ == '__main__':
  print ">>> "
  main()
  print ">>> Done"
  
