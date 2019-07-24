# Tau ID scale factors

This repository contains the recommended scale factors for tau IDs. More detailed recommendations can be found on this TWiki page: https://twiki.cern.ch/twiki/bin/viewauth/CMS/TauIDRecommendation13TeV


## Installation

To install the tool for reading the tau ID scale factors, do
```
CMSSW_BASE=CMSSW_10_3_3 # or whichever one you like
cmsrel $CMSSW_BASE
cd $CMSSW_BASE/src
git clone https://github.com/cms-tau-pog/TauIDSFs TauPOG/TauIDSFs
scram b -j8
```
After compiling with this respective directory hierarchy, you can acces the tool in python as
```
from TauIDSFs.TauIDSFTool import TauIDSFTool
```
A test can be run with
```
./python/testSFs.py
```


## Application

### pT-dependent SFs

Import the `TauIDSFTool` tool as
```
from TauIDSFs.TauIDSFTool import TauIDSFTool
```
As an example, to get the scale factors for the tight working point of the `'MVAoldDM2017v2'` tau ID in 2017, initialize the tool as
```
tauSFTool = TauIDSFTool(2017,'MVAoldDM2017v2','Tight')
```
and to retrieve the scale factor for a given tau pT, do
```
SF = tauSFTool.getSFvsPT(pt)
```
The scale factor should only be applied to tau objects that match "real" taus at gen-level (`genmatch==5`). You can pass the optional `genmatch` argument and the function will return the SF if `genmatch==5`, and `1.` otherwise,
```
SF = tauSFTool.getSFvsPT(pt,genmatch)
```
The recommended uncertainties can be retrieved as
```
SF_up   = tauSFTool.getSFvsPT(pt,genmatch,unc='Up')
SF_down = tauSFTool.getSFvsPT(pt,genmatch,unc='Down')
```


### DM-dependent SFs

Analysis using tau triggers and tau pT > 40 GeV, may use DM-dependent SFs as
```
tauSFTool = TauIDSFTool(2017,'MVAoldDM2017v2','Tight',dm=True)
SF = tauSFTool.getSFvsDM(pt,dm,genmatch)
```
where `genmatch` is optional.


### Eta-dependent SFs for the anti-lepton discriminators

Coming soon.
