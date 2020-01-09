#! /usr/bin/env python
# Author: Izaak Neutelings (September 2019)
# Description: Create root files with SFs for the anti-lepton discriminators
import os
from array import array
import numpy as np
from collections import namedtuple
from ROOT import TFile, TH1F, kFullDotLarge, TGraphAsymmErrors

# SF CONTAINER
SF  = namedtuple('SF',['val','unc'])
SF0 = SF(0,0) # default
SF1 = SF(1,0) # default

def createSFTH1(histname,sflist,bins,xtitle,ytitle="SF",overflow=False):
  """Create histogram with variable bin sizes from SF list."""
  print ">>>   Creating hisogram '%s'..."%histname
  sflist = list(sflist)

  # ASSUME (nbins,xmin,xmax)
  if len(bins)==3 and isinstance(bins[0],int):
    nxbins = bins[0]
    hist   = TH1F(histname,histname,*bins)

  # VARIABLE BINS
  else:
    nxbins = len(bins)-1
    xbins  = array('d',list(bins))
    hist   = TH1F(histname,histname,nxbins,xbins)

  # APPEND LIST WITH LAST VALUE
  if overflow:
    while len(sflist)<=nxbins:
      sflist.append(sflist[-1])

  # STYLE
  hist.GetYaxis().SetTitle(ytitle)
  hist.GetXaxis().SetTitle(xtitle)
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

  # FILL
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


def createSFFile(filename,sftable,*args,**kwargs):
  """Create histogram from table."""
  print ">>> Creating '%s'..."%filename
  file = TFile(filename,'RECREATE')
  for wp in sorted(sftable,key=wporder):
    print ">>>  %s working point"%wp
    histname = wp
    sflist   = sftable[wp]
    hist     = createSFTH1(histname,sflist,*args,**kwargs)
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

def createAssymSFFile(filename, sftable, name):
  """Create histogram from table."""
  print ">>> Creating '%s'..." % filename
  file = TFile(filename, 'RECREATE')
  file.cd()
  x = [float(i) + 0.5 for i in range(len(sftable.keys()))]
  ex = [0.0] * len(sftable.keys())
  x_names = sorted(sftable.keys())
  y = [sftable[k]['val'] for k in x_names]
  eyl = [sftable[k]['down'] for k in x_names]
  eyh = [sftable[k]['up'] for k in x_names]
  g = TGraphAsymmErrors(len(x), np.array(x), np.array(y), np.array(ex), np.array(ex), np.array(eyl), np.array(eyh))

  g.GetXaxis().SetNdivisions(len(x) * 2)
  g.GetXaxis().ChangeLabel(0, -1, 0, -1, -1, -1, "")
  for i in x:
    print 1 + int(i), x_names[int(i)]
    g.GetXaxis().ChangeLabel(2 + int(i) * 2, -1, 0)
    g.GetXaxis().ChangeLabel(1 + int(i) * 2, -1, -1, -1, -1, -1, x_names[int(i)])

  g.Write(name)
  # file.ls() ; g.Draw("A*") ; raw_input()
  file.Close()
  return file

def main():

  outdir         = "../data"

  # ANTI-LEPTON SFs
  tag            = ""
  etatitle       = "#tau_{h} |#eta|"
  antiEleEtaBins = ( 0.0, 1.460, 1.558, 2.3 )
  antiMuEtaBins  = ( 0.0, 0.4, 0.8, 1.2, 1.7, 2.3 )
  antiLepSFs     = { }
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
    '2016Legacy': { # https://indico.cern.ch/event/862376/contributions/3633007/attachments/1942593/3221852/mutauFRRun2_Yiwen.pdf (slide 6)
      'Loose': ( SF(1.106,0.033), SF(1.121,0.034), SF(1.225,0.026), SF(1.115,0.198), SF(2.425,0.229), SF1 ),
      'Tight': ( SF(1.274,0.108), SF(1.144,0.231), SF(1.261,0.035), SF(1.159,0.663), SF(3.310,0.554), SF1 ),
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
      filename = "%s/TauID_SF_eta_%s_%s%s.root"%(outdir,id,year,tag)
      sftable  = antiLepSFs[id][year]
      etabins  = antiEleEtaBins if 'antiEle' in id else antiMuEtaBins
      createSFFile(filename,sftable,etabins,etatitle,overflow=True)

  # TAU ENERGY SCALES
  dmbins  = (13,0,13)
  dmtitle = "#tau_{h} decay modes"
  TESs    = { # units of percentage
    '2016Legacy': { 0: (-0.6,1.0), 1: (-0.5,0.9), 10: ( 0.0,1.1), },
    '2017ReReco': { 0: ( 0.7,0.8), 1: (-0.2,0.8), 10: ( 0.1,0.9), 11: (-0.1,1.0), },
    '2018ReReco': { 0: (-1.3,1.1), 1: (-0.5,0.9), 10: (-1.2,0.8), },
  }
  for year in TESs:
    filename = "%s/TauES_dm_%s.root"%(outdir,year)
    tesvals  = { 'tes': [ ] }
    for dm in xrange(0,dmbins[0]+1):
      tes, unc = TESs[year].get(dm,(0,0))
      tesvals['tes'].append(SF(1.+tes/100.,unc/100.))
    createSFFile(filename,tesvals,dmbins,dmtitle,overflow=False)

  # FAKE e->tau ENERGY SCALES
  FESs = {
      'DeepTau2017v2p1':
      {
          '2016Legacy':
          {
              'barrel_dm0': {"val": 1.00679, "down": 0.982 / 100, "up": 0.806 / 100},
              'barrel_dm1': {"val": 1.03389, "down": 2.475 / 100, "up":1.168 / 100},
              'endcap_dm0': {"val": 0.965, "down": 1.102 / 100, "up": 1.808 / 100},
              'endcap_dm1': {"val": 1.05, "down": 5.694 / 100, "up":6.57 / 100},
          },
          '2017ReReco':
          {
              'barrel_dm0': {"val": 1.00911, "down": 0.882 / 100, "up": 1.343 / 100},
              'barrel_dm1': {"val": 1.01154, "down": 0.973 / 100, "up": 2.162 / 100},
              'endcap_dm0': {"val": 0.97396, "down": 1.43 / 100, "up": 2.249 / 100},
              'endcap_dm1': {"val": 1.015, "down": 4.969 / 100, "up": 6.461 / 100},
          },
          '2018ReReco':
          {
              'barrel_dm0': {"val": 1.01362, "down": 0.474 / 100, "up": 0.904 / 100},
              'barrel_dm1': {"val": 1.01945, "down": 1.598 / 100, "up": 1.226 / 100},
              'endcap_dm0': {"val": 0.96903, "down": 1.25 / 100, "up": 3.404 / 100},
              'endcap_dm1': {"val": 0.985, "down": 4.309 / 100, "up": 5.499 / 100},
          },
      }
  }

  for discriminator in FESs.keys():
    for year, fesvals in FESs[discriminator].iteritems():
      filename = "%s/TauFES_eta_dm_%s_%s.root" % (outdir, discriminator, year)
      createAssymSFFile(filename, fesvals, name='fes')


if __name__ == '__main__':
  print ">>> "
  main()
  print ">>> Done"
