#! /usr/bin/env python
# Author: Izaak Neutelings (September 2019)
# Description: Create root files with SFs for the anti-lepton discriminators
import os
from math import sqrt
from array import array
import numpy as np
#from collections import namedtuple
from ROOT import TFile, TH1F, kFullDotLarge, TGraphAsymmErrors


# SF CONTAINER
###SF  = namedtuple('SF',['val','unc'])
class SF:
  """Simple container class, that allows for multiplication."""
  def __init__(self,val,*args):
    self.val     = val
    self.unc     = args[0]
    self.uncUp   = args[0]
    self.uncDown = args[1] if len(args)>=2 else args[0]
  def __mul__(self,osf):
    if isinstance(osf,SF):
      val = self.val*osf.val
      unc = val*sqrt((self.unc/float(self.val))**2 + (osf.unc/float(osf.val))**2)
      return SF(val,unc)
    return SF(osf*val,osf*unc)
SF0 = SF(0,0) # default 0
SF1 = SF(1,0) # default 1


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
      binstr = "[%5.2f, inf ]"%(hist.GetXaxis().GetBinLowEdge(i))
      ofstr  = "(overflow)"
    else:
     binstr = "[%5.2f,%5.2f]"%(hist.GetXaxis().GetBinLowEdge(i),hist.GetXaxis().GetBinUpEdge(i))
     ofstr  = ""
    print ">>>     Bin %2s, %s:  SF = %6.3f +- %.3f %s"%(i,binstr,sf.val,sf.unc,ofstr)
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
  
  outdir         = "data" #"../data"
  
  doVSLep        = True and False
  doTES          = True #and False
  doTES_highpt   = True #and False
  doFES          = True and False
  
  # ANTI-LEPTON SFs
  if doVSLep:
    tag            = ""
    etatitle       = "#tau_{h} |#eta|"
    antiEleEtaBins = ( 0.0, 1.460, 1.558, 2.3 )
    antiMuEtaBins  = ( 0.0, 0.4, 0.8, 1.2, 1.7, 2.3 )
    antiLepSFs     = { }
    #antiLepSFs['antiEleMVA6'] = {
    #  '2016Legacy': { # https://indico.cern.ch/event/828205/contributions/3468902/attachments/1863558/3063927/EtoTauFRLegacy16.pdf
    #    'VLoose': ( SF(1.175,0.003), SF1, SF(1.288,0.006), SF1 ), # LEGACY
    #    'Loose':  ( SF(1.38, 0.011), SF1, SF(1.24, 0.05 ), SF1 ),
    #    'Medium': ( SF(1.88, 0.04 ), SF1, SF(1.11, 0.10 ), SF1 ),
    #    'Tight':  ( SF(2.16, 0.10 ), SF1, SF(0.91, 0.20 ), SF1 ),
    #    'VTight': ( SF(2.04, 0.16 ), SF1, SF(0.78, 0.31 ), SF1 ),
    #  },
    #  '2017ReReco': { # https://twiki.cern.ch/twiki/bin/viewauth/CMS/TauIDRecommendation13TeV#Electron_to_tau_fake_rate
    #    'VLoose': ( SF(1.09,0.01), SF1, SF(1.19,0.01), SF1 ),
    #    'Loose':  ( SF(1.17,0.04), SF1, SF(1.25,0.06), SF1 ),
    #    'Medium': ( SF(1.40,0.12), SF1, SF(1.21,0.26), SF1 ),
    #    'Tight':  ( SF(1.80,0.20), SF1, SF(1.53,0.60), SF1 ),
    #    'VTight': ( SF(1.96,0.27), SF1, SF(1.66,0.80), SF1 ),
    #  },
    #  '2018ReReco': { # https://indico.cern.ch/event/831606/contributions/3483937/attachments/1871414/3079821/EtoTauFR2018-updated.pdf
    #    'VLoose': ( SF(1.130,0.005), SF1, SF(1.003,0.005), SF1 ), # PRELIMINARY
    #    'Loose':  ( SF(1.229,0.018), SF1, SF(0.926,0.015), SF1 ),
    #    'Medium': ( SF(1.36, 0.004), SF1, SF(0.91, 0.05 ), SF1 ),
    #    'Tight':  ( SF(1.46, 0.008), SF1, SF(1.02, 0.14 ), SF1 ),
    #    'VTight': ( SF(1.56, 0.16 ), SF1, SF(1.03, 0.24 ), SF1 ),
    #  },
    #}
    #antiLepSFs['antiMu3'] = {
    #  '2016Legacy': { # https://indico.cern.ch/event/862376/contributions/3633007/attachments/1942593/3221852/mutauFRRun2_Yiwen.pdf (slide 6)
    #    'Loose': ( SF(1.106,0.033), SF(1.121,0.034), SF(1.225,0.026), SF(1.115,0.198), SF(2.425,0.229), SF1 ),
    #    'Tight': ( SF(1.274,0.108), SF(1.144,0.231), SF(1.261,0.035), SF(1.159,0.663), SF(3.310,0.554), SF1 ),
    #  },
    #  '2017ReReco': { # https://twiki.cern.ch/twiki/bin/viewauth/CMS/TauIDRecommendation13TeV#Muon_to_tau_fake_rate
    #    'Loose': ( SF(1.06,0.05), SF(1.02,0.04), SF(1.10,0.04), SF(1.03,0.18), SF(1.94,0.35), SF1 ),
    #    'Tight': ( SF(1.17,0.12), SF(1.29,0.30), SF(1.14,0.05), SF(0.93,0.60), SF(1.61,0.60), SF1 ),
    #  },
    #  '2018ReReco': { # https://indico.cern.ch/event/814232/contributions/3397978/attachments/1831354/2999219/mu-tau_FR_2018.pdf
    #    'Loose': ( SF(1.05,0.05), SF(0.96,0.04), SF(1.06,0.05), SF(1.45,0.08), SF(1.75,0.16), SF1 ),
    #    'Tight': ( SF(1.23,0.05), SF(1.37,0.18), SF(1.12,0.04), SF(1.84,0.32), SF(2.01,0.43), SF1 ),
    #  },
    #}
    antiLepSFs['DeepTau2017v2p1VSe'] = {
      # https://indico.cern.ch/event/865792/contributions/3659828/attachments/1954858/3246751/ETauFR-update2Dec.pdf (slides 15, 26, 37)
      '2016Legacy': {
        'VVLoose': ( SF(1.38,0.08), SF1, SF(1.29,0.08), SF1 ),
        'VLoose':  ( SF(1.22,0.08), SF1, SF(1.13,0.09), SF1 ),
        'Loose':   ( SF(1.28,0.10), SF1, SF(0.99,0.16), SF1 ),
        'Medium':  ( SF(1.44,0.13), SF1, SF(1.08,0.21), SF1 ),
        'Tight':   ( SF(1.22,0.38), SF1, SF(1.47,0.32), SF1 ),
        'VTight':  ( SF(1.52,0.36), SF1, SF(1.59,0.60), SF1 ),
        'VVTight': ( SF(2.42,0.43), SF1, SF(2.40,1.04), SF1 ),
      },
      '2017ReReco': {
        'VVLoose': ( SF(1.11,0.09), SF1, SF(1.03,0.09), SF1 ),
        'VLoose':  ( SF(0.93,0.08), SF1, SF(1.00,0.12), SF1 ),
        'Loose':   ( SF(0.96,0.11), SF1, SF(0.91,0.20), SF1 ),
        'Medium':  ( SF(1.18,0.20), SF1, SF(0.86,0.21), SF1 ),
        'Tight':   ( SF(1.22,0.32), SF1, SF(0.93,0.38), SF1 ),
        'VTight':  ( SF(1.18,0.47), SF1, SF(0.95,0.78), SF1 ),
        'VVTight': ( SF(0.85,2.39), SF1, SF(1.07,1.41), SF1 ),
      },
      '2018ReReco': {
        'VVLoose': ( SF(0.91,0.06), SF1, SF(0.91,0.07), SF1 ),
        'VLoose':  ( SF(0.95,0.07), SF1, SF(0.86,0.10), SF1 ),
        'Loose':   ( SF(1.06,0.09), SF1, SF(0.78,0.12), SF1 ),
        'Medium':  ( SF(1.25,0.14), SF1, SF(0.65,0.15), SF1 ),
        'Tight':   ( SF(1.47,0.27), SF1, SF(0.66,0.20), SF1 ),
        'VTight':  ( SF(1.79,0.42), SF1, SF(0.91,0.50), SF1 ),
        'VVTight': ( SF(2.46,0.90), SF1, SF(0.46,1.00), SF1 ),
      },
    }
    antiLepSFs['DeepTau2017v2p1VSmu'] = {
      # https://indico.cern.ch/event/866243/contributions/3650016/attachments/1950974/3238736/mutauFRRun2_Yiwen_20191121.pdf (slides 8-10)
      '2016Legacy': {
        'VLoose': ( SF(0.978,0.029)*SF(1.311,0.057), SF(1.003,0.037)*SF(0.995,0.116), SF(0.992,0.052)*SF(1.275,0.081), SF(1.003,0.037)*SF(0.892,0.156), SF(0.966,0.040)*SF(5.111,0.282), SF1 ),
        'Loose':  ( SF(0.978,0.029)*SF(1.411,0.084), SF(1.003,0.037)*SF(0.952,0.210), SF(0.992,0.052)*SF(1.337,0.145), SF(1.003,0.037)*SF(1.037,0.329), SF(0.966,0.040)*SF(6.191,0.386), SF1 ),
        'Medium': ( SF(0.978,0.029)*SF(1.442,0.097), SF(1.003,0.037)*SF(0.941,0.272), SF(0.992,0.052)*SF(1.288,0.204), SF(1.003,0.037)*SF(1.054,0.469), SF(0.966,0.040)*SF(5.341,0.616), SF1 ),
        'Tight':  ( SF(0.978,0.029)*SF(1.463,0.097), SF(1.003,0.037)*SF(0.722,0.289), SF(0.992,0.052)*SF(1.337,0.239), SF(1.003,0.037)*SF(0.966,0.650), SF(0.966,0.040)*SF(5.451,0.846), SF1 ),
      },
      '2017ReReco': {
        'VLoose': ( SF(0.979,0.033)*SF(1.117,0.067), SF(0.953,0.034)*SF(0.952,0.070), SF(0.983,0.037)*SF(0.952,0.070), SF(0.988,0.038)*SF(0.744,0.126), SF(1.004,0.052)*SF(4.592,0.247), SF1 ),
        'Loose':  ( SF(0.979,0.033)*SF(1.076,0.112), SF(0.953,0.034)*SF(0.940,0.140), SF(0.983,0.037)*SF(0.940,0.140), SF(0.988,0.038)*SF(0.916,0.272), SF(1.004,0.052)*SF(5.596,0.422), SF1 ),
        'Medium': ( SF(0.979,0.033)*SF(1.062,0.149), SF(0.953,0.034)*SF(0.819,0.206), SF(0.983,0.037)*SF(0.819,0.206), SF(0.988,0.038)*SF(1.021,0.375), SF(1.004,0.052)*SF(4.235,0.617), SF1 ),
        'Tight':  ( SF(0.979,0.033)*SF(0.991,0.152), SF(0.953,0.034)*SF(0.675,0.259), SF(0.983,0.037)*SF(0.675,0.259), SF(0.988,0.038)*SF(1.098,0.457), SF(1.004,0.052)*SF(4.175,0.779), SF1 ),
      },
      '2018ReReco': {
        'VLoose': ( SF(0.936,0.040)*SF(1.019,0.060), SF(0.874,0.028)*SF(1.154,0.106), SF(0.912,0.030)*SF(1.128,0.073), SF(0.953,0.040)*SF(0.974,0.147), SF(0.936,0.038)*SF(5.342,0.339), SF1 ),
        'Loose':  ( SF(0.936,0.040)*SF(0.993,0.097), SF(0.874,0.028)*SF(1.371,0.202), SF(0.912,0.030)*SF(1.165,0.135), SF(0.953,0.040)*SF(0.860,0.265), SF(0.936,0.038)*SF(6.631,0.473), SF1 ),
        'Medium': ( SF(0.936,0.040)*SF(0.940,0.120), SF(0.874,0.028)*SF(1.519,0.269), SF(0.912,0.030)*SF(1.032,0.193), SF(0.953,0.040)*SF(0.817,0.392), SF(0.936,0.038)*SF(5.597,0.691), SF1 ),
        'Tight':  ( SF(0.936,0.040)*SF(0.820,0.130), SF(0.874,0.028)*SF(1.436,0.292), SF(0.912,0.030)*SF(0.989,0.220), SF(0.953,0.040)*SF(0.875,0.434), SF(0.936,0.038)*SF(4.739,0.848), SF1 ),
      },
    }
    for id in antiLepSFs:
      for year in antiLepSFs[id]:
        filename = "%s/TauID_SF_eta_%s_%s%s.root"%(outdir,id,year,tag)
        sftable  = antiLepSFs[id][year]
        etabins  = antiEleEtaBins if any(s in id for s in ['antiEle','VSe']) else antiMuEtaBins
        createSFFile(filename,sftable,etabins,etatitle,overflow=True)

  # TAU ENERGY SCALES low pT (Z -> tautau)
  if doTES:
    dmbins  = (13,0,13)
    dmtitle = "#tau_{h} decay modes"
    TESs    = { # units of percentage
      'MVAoldDM2017v2': {
        '2016Legacy': { 0: (-0.6,1.0), 1: (-0.5,0.9), 10: ( 0.0,1.1), 11: ( 0.0,1.1), },
        '2017ReReco': { 0: ( 0.7,0.8), 1: (-0.2,0.8), 10: ( 0.1,0.9), 11: (-0.1,1.0), },
        '2018ReReco': { 0: (-1.3,1.1), 1: (-0.5,0.9), 10: (-1.2,0.8), 11: (-1.2,0.8), },
      },
      # https://indico.cern.ch/event/887196/contributions/3743090/attachments/1984772/3306737/TauPOG_TES_20200210.pdf
      'DeepTau2017v2p1VSjet': {
        '2016Legacy': { 0: (-0.9,0.8), 1: (-0.1,0.6), 10: ( 0.3,0.8), 11: (-0.2,1.1), },
        '2017ReReco': { 0: ( 0.4,1.0), 1: ( 0.2,0.6), 10: ( 0.1,0.7), 11: (-1.3,1.4), },
        '2018ReReco': { 0: (-1.6,0.9), 1: (-0.4,0.6), 10: (-1.2,0.7), 11: (-0.4,1.2), },
      },
    }
    
    for id in TESs:
      for year in TESs[id]:
        filename = "%s/TauES_dm_%s_%s.root"%(outdir,id,year)
        tesvals  = { 'tes': [ ] }
        for dm in xrange(0,dmbins[0]+1):
          tes, unc = TESs[id][year].get(dm,(0,0)) # default
          tesvals['tes'].append(SF(1.+tes/100.,unc/100.))
        createSFFile(filename,tesvals,dmbins,dmtitle,overflow=False)
  
  # TAU ENERGY SCALES at high pT (W* + jets)
  if doTES_highpt:
    dmbins  = (13,0,13)
    dmtitle = "#tau_{h} decay modes"
    TESs    = { # units of percentage
      'MVAoldDM2017v2': { # central values from Z -> tautau measurement
        '2016Legacy': { 0: (0.991,0.030), 1: (0.995,0.030), 10: (1.000,0.030), },
        '2017ReReco': { 0: (1.004,0.030), 1: (0.998,0.030), 10: (1.001,0.030), },
        '2018ReReco': { 0: (0.984,0.030), 1: (0.995,0.030), 10: (0.988,0.030), },
      },
      # https://indico.cern.ch/event/871696/contributions/3687829/attachments/1968053/3276394/TauES_WStar_Run2.pdf
      'DeepTau2017v2p1VSjet': {
        '2016Legacy': { 0: (0.991,0.030), 1: (1.042,0.020), 10: (1.004,0.012), 11: (0.970,0.027), },
        '2017ReReco': { 0: (1.004,0.030), 1: (1.014,0.027), 10: (0.978,0.017), 11: (0.944,0.040), },
        '2018ReReco': { 0: (0.984,0.030), 1: (1.004,0.020), 10: (1.006,0.011), 11: (0.955,0.039), },
      },
    }
    for id in TESs:
      for year in TESs[id]:
        filename = "%s/TauES_dm_%s_%s_ptgt100.root"%(outdir,id,year)
        tesvals  = { 'tes': [ ] }
        for dm in xrange(0,dmbins[0]+1):
          tes, unc = TESs[id][year].get(dm,(0,0)) # default
          tesvals['tes'].append(SF(tes,unc))
        createSFFile(filename,tesvals,dmbins,dmtitle,overflow=False)
  
  # FAKE e->tau ENERGY SCALES
  if doFES:
    FESs = {
      'DeepTau2017v2p1VSe': {
        '2016Legacy': {
          'barrel_dm0': {"val": 1.00679, "down": 0.982 / 100, "up": 0.806 / 100},
          'barrel_dm1': {"val": 1.03389, "down": 2.475 / 100, "up":1.168 / 100},
          'endcap_dm0': {"val": 0.965, "down": 1.102 / 100, "up": 1.808 / 100},
          'endcap_dm1': {"val": 1.05, "down": 5.694 / 100, "up":6.57 / 100},
        },
        '2017ReReco': {
          'barrel_dm0': {"val": 1.00911, "down": 0.882 / 100, "up": 1.343 / 100},
          'barrel_dm1': {"val": 1.01154, "down": 0.973 / 100, "up": 2.162 / 100},
          'endcap_dm0': {"val": 0.97396, "down": 1.43 / 100, "up": 2.249 / 100},
          'endcap_dm1': {"val": 1.015, "down": 4.969 / 100, "up": 6.461 / 100},
        },
        '2018ReReco': {
          'barrel_dm0': {"val": 1.01362, "down": 0.474 / 100, "up": 0.904 / 100},
          'barrel_dm1': {"val": 1.01945, "down": 1.598 / 100, "up": 1.226 / 100},
          'endcap_dm0': {"val": 0.96903, "down": 1.25 / 100, "up": 3.404 / 100},
          'endcap_dm1': {"val": 0.985, "down": 4.309 / 100, "up": 5.499 / 100},
        },
      }
    }
    for discriminator in FESs.keys():
      for year, fesvals in FESs[discriminator].iteritems():
        filename = "%s/TauFES_eta-dm_%s_%s.root" % (outdir, discriminator, year)
        createAssymSFFile(filename, fesvals, name='fes')


if __name__ == '__main__':
  print ">>> "
  main()
  print ">>> Done"
