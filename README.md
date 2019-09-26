# Tau ID scale factors

This repository contains the recommended scale factors for tau IDs. More detailed recommendations can be found on this TWiki page: https://twiki.cern.ch/twiki/bin/viewauth/CMS/TauIDRecommendation13TeV


## Installation

To install the tool for reading the tau ID scale factors, do
```
export SCRAM_ARCH=slc6_amd64_gcc700 # for CMSSW_10_3_3, check "scram list"
CMSSW_BASE=CMSSW_10_3_3             # or whichever release you desire
cmsrel $CMSSW_BASE
cd $CMSSW_BASE/src
git clone https://github.com/cms-tau-pog/TauIDSFs TauPOG/TauIDSFs
cmsenv
scram b -j8
```

### Python

After compiling with this respective directory hierarchy, you can acces the tool ([`python/TauIDSFTool.py`](python/TauIDSFTool.py)) in python as
```
from TauPOG.TauIDSFs.TauIDSFTool import TauIDSFTool
```
A test of the tool can be run with
```
./test/testTauIDSFTool.py
```

### C++

A similar C++ implementation is available ([`src/TauIDSFTool.cc`](src/TauIDSFTool.cc)). A test in C++ ([`test/testTauIDSFTool.cc`](test/testTauIDSFTool.cc)) can be compiled and run with
```
scram b runtests -j8
```


## Usage

### pT-dependent SFs

As an example, to get the scale factors for the tight working point of the `'MVAoldDM2017v2'` tau ID in 2017, initialize the tool as
```
from TauPOG.TauIDSFs.TauIDSFTool import TauIDSFTool
tauSFTool = TauIDSFTool(2017,'MVAoldDM2017v2','Tight')
```
and to retrieve the scale factor for a given tau pT, do
```
SF = tauSFTool.getSFvsPT(pt)
```
The scale factor should only be applied to tau objects that match "real" taus at gen-level (`genmatch==5`). You can pass the optional `genmatch` argument and the function will return the appropriate SF if `genmatch==5`, and `1.0` otherwise,
```
SF = tauSFTool.getSFvsPT(pt,genmatch)
```
The recommended uncertainties can be retrieved as
```
SF_up   = tauSFTool.getSFvsPT(pt,genmatch,unc='Up')
SF_down = tauSFTool.getSFvsPT(pt,genmatch,unc='Down')
```
Currently, the SFs are meant for 2016 Legacy (`RunIISummer16MiniAODv3` MC with `17Jul2018` data), 2017 ReReco (`RunIIFall17MiniAODv2` MC with `31Mar2018`), and 2018 ReReco (`RunIIAutumn18MiniAOD` MC with `17Sep2018`/`22Jan2019` data).


### DM-dependent SFs

Analysis using tau triggers and tau pT > 40 GeV, may use DM-dependent SFs as
```
from TauPOG.TauIDSFs.TauIDSFTool import TauIDSFTool
tauSFTool = TauIDSFTool(2017,'MVAoldDM2017v2','Tight',dm=True)
SF        = tauSFTool.getSFvsDM(pt,dm,genmatch)
SF_up     = tauSFTool.getSFvsDM(pt,dm,genmatch,unc='Up')
SF_down   = tauSFTool.getSFvsDM(pt,dm,genmatch,unc='Down')
```
where `genmatch` is optional.


### Eta-dependent SFs for the anti-lepton discriminators

To apply SFs to electrons or muons faking taus, use the eta of the reconstructed tau and the genmatch code (1 for prompt electrons, 2 for prompt muons, 3 for electrons from tau decay and 4 for muons from tau decay):
```
from TauPOG.TauIDSFs.TauIDSFTool import TauIDSFTool
antiEleSFTool = TauIDSFTool(2017,'antiEleMVA6','Loose')
antiMuSFTool  = TauIDSFTool(2017,'antiMu3','Tight')
antiEleSF     = antiEleSFTool.getSFvsEta(eta,genmatch)
antiMuSF      = antiMuSFTool.getSFvsEta(eta,genmatch)
```
For the uncertainty, please seek the recommendations by the TauPOG. Note: The SFs for `againstMu3` in 2016 Legacy ([`data/TauID_SF_eta_antiMu3_2016.root`](data/TauID_SF_eta_antiMu3_2016.root)) are must placeholders.
