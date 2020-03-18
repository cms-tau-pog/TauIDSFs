#! /usr/bin/env python
# Author: Izaak Neutelings (March 2020)
# Usage:
#   ./test/dumpTauIDSFs.py data/TauID_*_DeepTau2017v2p1VSjet_*.root
#   ./test/dumpTauIDSFs.py data/TauES_*_DeepTau2017v2p1VSjet_*.root
import os, re
import ROOT; ROOT.PyConfig.IgnoreCommandLineOptions = True
from ROOT import gROOT
from TauPOG.TauIDSFs.helpers import ensureTFile, extractTH1
from argparse import ArgumentParser
epilog ="""example: ./test/dumpTauIDSFs.py data/TauID_*_DeepTau2017v2p1VSjet_*.root"""
parser = ArgumentParser(epilog=epilog) #usage=usage)
parser.add_argument('filenames', nargs='+', default=False,
                                 help="TauPOG root file with histogram (TH1) or function (TF1)" )
args = parser.parse_args()

def green(string,**kwargs): return "\x1b[0;32;40m%s\033[0m"%string

def dumpContents(filename):
  file  = ensureTFile(filename)
  hists = getObjects(file,type='TH1')
  funcs = getObjects(file,type='TF1')
  for hist in hists:
    print ">>>"
    print '>>>   Histogram "%s"'%(green(hist.GetName()))
    printTH1(hist)
  for func in funcs:
    print ">>>"
    print '>>>   Function "%s"'%(green(func.GetName()))
    printTF1(func)
  file.Close()
  
def printTH1(hist):
  nbins = hist.GetXaxis().GetNbins()
  print ">>> %6s %7s - %6s %9s +- %7s"%("bin","xmin","xmax","content","error")
  for bin in xrange(0,nbins+2):
    xmin = "%.2f"%hist.GetXaxis().GetBinLowEdge(bin) if bin>0 else '-Inf'
    xmax = "%.2f"%hist.GetXaxis().GetBinUpEdge(bin) if bin<nbins+1 else '+Inf'
    print ">>> %6s %7s - %6s %9.3f +- %7.3f"%(
      bin,xmin,xmax,hist.GetBinContent(bin),hist.GetBinError(bin))
  
def printTF1(func):
  formula  = str(func.GetExpFormula()).replace(' ','')
  sfexps   = formula.split('+(')
  xminrexp = re.compile(r'x>=?(\d+\.?\d*)')
  xmaxrexp = re.compile(r'x<=?(\d+\.?\d*)')
  sfrexp   = re.compile(r'\*(\d+\.?\d*)')
  formrexp = re.compile(r'\((\d+\.\d+)[+-](\d+\.\d+)\*\(x/(\d+\.?\d*)\)\)') # linear interpolation formula
  lastrexp = re.compile(r'\((\d+\.\d+)([+-]\d+\.\d+)\)') # last bin
  print ">>>    '%s'"%formula
  print ">>> %6s %7s - %6s   %-20s  %-15s"%("bin","xmin","xmax","sf","expr.")
  for i, sfexp in enumerate(sfexps):
    if i!=0: sfexp = '('+sfexp
    xmins   = xminrexp.findall(sfexp)
    xmaxs   = xmaxrexp.findall(sfexp)
    sfs     = sfrexp.findall(sfexp)
    formsfs = formrexp.findall(sfexp)
    lastsfs = lastrexp.findall(sfexp)
    xmin    = float(xmins[0]) if xmins else '-Inf'
    xmax    = float(xmaxs[0]) if xmaxs else '+Inf'
    if sfs:
      sf    = "%.3f"%float(sfs[0])
    elif formsfs:
      sf    = "%.3f%+.3f*x/%.1f"%(float(formsfs[0][0]),float(formsfs[0][1]),float(formsfs[0][2]))
    elif lastsfs:
      sf    = "%.3f"%(float(lastsfs[0][0])+float(lastsfs[0][1]))
    else:
      sf    = '?'
    print ">>> %6s %7s - %6s   %-20s  %-15s"%(i,xmin,xmax,sf,sfexp)
  
def getObjects(dir,type='TH1'):
  objs = [ ]
  for key in dir.GetListOfKeys():
    if gROOT.GetClass(key.GetClassName()).InheritsFrom(type):
      objname = key.GetName()
      obj = dir.Get(objname)
      obj.SetName(objname) # if key name != obj name
      objs.append(obj)
  return objs
  
if __name__ == "__main__":
  filenames = args.filenames
  for filename in filenames:
    print ">>> "
    print '>>> File "%s"'%(green(filename))
    dumpContents(filename)
  print ">>> "
  print ">>> Done"
  