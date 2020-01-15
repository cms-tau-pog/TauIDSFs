# Tau ID scale factors

This repository contains the recommended scale factors for several tau discriminators, and tools to read them.
More detailed recommendations can be found on this TWiki page: https://twiki.cern.ch/twiki/bin/viewauth/CMS/TauIDRecommendationForRun2


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
A test of the tool in python can be run with
```
./test/testTauIDSFTool.py
```


### C++

A similar C++ implementation is available in [`src/TauIDSFTool.cc`](src/TauIDSFTool.cc),
with a simple example of usage in ([`test/testTauIDSFTool.cc`](test/testTauIDSFTool.cc)).
This is also an installation test that can be compiled and run with
```
scram b runtests -j8
```


## Scale factor versions

The SFs in [`data`](data) are meant for the following campaigns:

| Year label   | MC campaign  | Data campaign |
|:------------:|:------------:| :------------:|
| `2016Legacy` | `RunIISummer16MiniAODv3` | `17Jul2018` |
| `2017ReReco` | `RunIIFall17MiniAODv2`   | `31Mar2018` |
| `2018ReReco` | `RunIIAutumn18MiniAOD`   | `17Sep2018`/`22Jan2019` |


## Usage

For more info on gen-matching of taus, please look [here](https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorking2016#MC_Matching).
Note that in nanoAOD this is available as `Tau_GenPartFlav`, but jet or no match correspond to `Tau_GenPartFlav==0` instead of `6`.

### pT-dependent SFs

As an example, to get the scale factors for the tight working point of the `'DeepTau2017v2p1VSjet'` tau ID in 2017, initialize the tool as
```
from TauPOG.TauIDSFs.TauIDSFTool import TauIDSFTool
tauSFTool = TauIDSFTool('2017ReReco','DeepTau2017v2p1VSjet','Tight')
```
and to retrieve the scale factor for a given tau pT, do
```
sf = tauSFTool.getSFvsPT(pt)
```
The scale factor should only be applied to tau objects that match "real" taus at gen-level (`genmatch==5`). You can pass the optional `genmatch` argument and the function will return the appropriate SF if `genmatch==5`, and `1.0` otherwise,
```
sf = tauSFTool.getSFvsPT(pt,genmatch)
```
The recommended uncertainties can be retrieved as
```
sf_up   = tauSFTool.getSFvsPT(pt,genmatch,unc='Up')
sf_down = tauSFTool.getSFvsPT(pt,genmatch,unc='Down')
```
or, all three in one go:
```
sf_down, sf, sf_up = tauSFTool.getSFvsPT(pt,genmatch,unc='All')
```
For the tau ID scale factor of the **embedded samples**, set the `emb` flag to `True`:
```
tauSFTool = TauIDSFTool('2017ReReco','DeepTau2017v2p1VSjet','Tight',emb=True)
```


### DM-dependent SFs

Analysis using ditau triggers and tau pT > 40 GeV, may use DM-dependent SFs as
```
from TauPOG.TauIDSFs.TauIDSFTool import TauIDSFTool
tauSFTool = TauIDSFTool('2017ReReco','MVAoldDM2017v2','Tight',dm=True)
sf        = tauSFTool.getSFvsDM(pt,dm,genmatch)
sf_up     = tauSFTool.getSFvsDM(pt,dm,genmatch,unc='Up')
sf_down   = tauSFTool.getSFvsDM(pt,dm,genmatch,unc='Down')
```
where `genmatch` is optional.


### Eta-dependent SFs for the anti-lepton discriminators

To apply SFs to electrons or muons faking taus, use the eta of the reconstructed tau and the `genmatch` code
(`1` for prompt electrons, `2` for prompt muons, `3` for electrons from tau decay and `4` for muons from tau decay):
```
python/TauIDSFTool.py
antiEleSFTool = TauIDSFTool('2017ReReco','antiEleMVA6','Loose')
antiMuSFTool  = TauIDSFTool('2017ReReco','antiMu3','Tight')
antiEleSF     = antiEleSFTool.getSFvsEta(eta,genmatch)
antiMuSF      = antiMuSFTool.getSFvsEta(eta,genmatch)
```
The uncertainty is obtained in a similar way as above.


### DM-dependent tau energy scale

The tau energy scale (TES) is provided in the files [`data/TauES_dm_*.root`](data).
Each file contains one histogram (`'tes'`) with the TES centered around `1.0`.
It should be applied to a genuine tau by multiplying the tau TLorentzVector, or equivalently, the tau energy, pT and mass as follows:
```
file = TFile("data/TauES_dm_MVAoldDM2017v2_2016Legacy.root")
hist = file.Get('tes')
tes  = hist.GetBinContent(hist.GetXaxis().FindBin(dm))

# scale the tau's TLorentzVector
tau_tlv  *= tes

# OR, scale the energy, mass and pT
tau_E  *= tes
tau_pt *= tes
tau_m  *= tes
```
A simple class, [`TauESTool`](python/TauIDSFTool.py), is provided to obtain the TES as
```
from TauPOG.TauIDSFs.TauIDSFTool import TauESTool
testool = TauESTool('2017ReReco')
tes     = testool.getTES(dm,genmatch)
tesUp   = testool.getTES(dm,genmatch,unc='Up')
tesDown = testool.getTES(dm,genmatch,unc='Down')
```


### Eta- & DM-dependent e -> tau fake energy scale

The e -> tau fake energy scale (FES) is provided in the files [`data/TauFES_eta-dm_*.root`](data).
Each file contains one graph (`'fes'`) with the FES centered around `1.0`.
It should only be applied to reconstructed taus that are faked by electrons (i.e. `genmatch==1` or `3`) and have DM 0 or 1.
The application is the similar as for the TES above.
A simple class, [`TauFESTool`](python/TauIDSFTool.py), is provided to obtain the FES as
```
from TauPOG.TauIDSFs.TauIDSFTool import TauFESTool
festool = TauESTool('2017ReReco')
fes     = festool.getFES(eta,dm,genmatch)
fesUp   = festool.getFES(eta,dm,genmatch,unc='Up')
fesDown = festool.getFES(eta,dm,genmatch,unc='Down')
```


