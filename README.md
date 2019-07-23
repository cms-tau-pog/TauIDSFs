# Tau ID scale factors

This repository contains the recommended scale factors for tau IDs. More detailed recommendations can be found on this TWiki: https://twiki.cern.ch/twiki/bin/viewauth/CMS/TauIDRecommendation13TeV


## Installation

To install the tool for reading the tau ID scale factors, do
```
CMSSW_BASE=CMSSW_10_3_3 # or whichever one you like
cmsrel $CMSSW_BASE
cd $CMSSW_BASE/src
git clone https://github.com/cms-tau-pog/TauIDSFs TauPOG/TauIDSFs
scram b -j8
```
After compiling with this respective directory hierarchy, you can acces the tool in python as:
```
from TauIDSFs.TauIDSFTool import TauIDSFTool
```
A test can be run with
```
./python/testSFs.py
```


## Application

Import the `TauIDSFTool` tool as
```
from TauIDSFs.TauIDSFTool import TauIDSFTool
```
As an example, to get the scale factors for the tight working point of the `'MVAoldDM2017v2'` tau ID in 2017, initialize the tool as
```
tauSFTool = TauIDSFTool(2017,'MVAoldDM2017v2','Tight')
```
To retrieve the scale factor for a given tau pT, do
```
tauSFTool.getSFvsPT(pt)
```