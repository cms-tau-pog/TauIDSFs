# Tau ID scale factors

This repository contains the recommended scale factors (SFs) for several tau discriminators, and tools to read them.
More detailed recommendations can be found on this TWiki page: https://twiki.cern.ch/twiki/bin/viewauth/CMS/TauIDRecommendationForRun2


## Installation of the tool

To install the tool for reading the tau ID SFs, do
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

After compiling with this respective directory hierarchy, you can acces the tool
([`python/TauIDSFTool.py`](python/TauIDSFTool.py)) in python as
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


### Python without CMSSW

Alternatively, if you want to use the python tool standalone without CMSSW,
clone the repository and assure that your `PYTHONPATH` points to the `TauIDSFTool` module.
```
export PYTHONPATH=<path to python directory>:$PYTHONPATH
```
Afterwards, you should be able to do:
```
from TauIDSFTool import TauIDSFTool
```


## Summary of available SFs

This is a rough summary of the available SFs for `DeepTau2017v2p1` in [`data/`](data):

| Tau component  | `genmatch`  | `DeepTau2017v2p1` `VSjet`  | `DeepTau2017v2p1` `VSe`  | `DeepTau2017v2p1` `VSmu`  | energy scale   |
|:--------------:|:-----------:|:--------------------------:|:------------------------:|:-------------------------:|:--------------:|
| real tau       | `5`         | vs. pT, or vs. DM          | – (*)                    | – (*)                     | vs. DM         |
| e -> tau fake  | `1`, `3`    | –                          | vs. eta                  | –                         | vs. DM and eta |
| mu -> tau fake | `2`, `4`    | –                          | –                        | vs. eta                   | – (±1% unc.)   |

(*) An extra uncertainty is recommended if you use a different working point (WP) combination than was used to measure the SFs,
see the [TWiki](https://twiki.cern.ch/twiki/bin/viewauth/CMS/TauIDRecommendationForRun2).
The tool should take this automatically into account with the `otherVSlepWP` flag.

The gen-matching is defined as:
* `1` for prompt electrons
* `2` for prompt muons
* `3` for electrons from tau decay
* `4` for muons from tau decay
* `5` for real taus
* `6` for no match, or jets faking taus.
For more info on gen-matching of taus, please see [here](https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorking2016#MC_Matching).
Note that in nanoAOD this is available as `Tau_GenPartFlav`, but jet or no match correspond to `Tau_GenPartFlav==0` instead of `6`.

The SFs are meant for the following campaigns:

| Year label   | MC campaign              | Data campaign           |
|:------------:|:------------------------:| :----------------------:|
| `2016Legacy` | `RunIISummer16MiniAODv3` | `17Jul2018`             |
| `2017ReReco` | `RunIIFall17MiniAODv2`   | `31Mar2018`             |
| `2018ReReco` | `RunIIAutumn18MiniAOD`   | `17Sep2018`/`22Jan2019` |



## Usage

A simple script is given to dump the corrections saved in histograms or functions of the files in [`data/`](data). Use for example
```
./test/dumpTauIDSFs.py data/TauID_SF_*_DeepTau2017v2p1VSjet_*.root
```

### pT-dependent SFs

The pT-dependent SFs are provided as `TF1` functions. For example, to obtain those for the medium WP of the `'DeepTau2017v2p1VSjet'` discriminator for 2016, use
```
file = TFile("data/TauID_SF_pt_DeepTau2017v2p1VSjet_2016Legacy.root")
func = file.Get('Medium_cent')
sf   = sf.Eval(pt)
```
The tool can be used as
```
from TauPOG.TauIDSFs.TauIDSFTool import TauIDSFTool
tauSFTool = TauIDSFTool('2016Legacy','DeepTau2017v2p1VSjet','Medium')
```
and to retrieve the SF for a given tau pT, do
```
sf = tauSFTool.getSFvsPT(pt)
```
The SF should only be applied to tau objects that match "real" taus at gen-level (`genmatch==5`).
You can pass the optional `genmatch` argument and the function will return the appropriate SF if `genmatch==5`, and `1.0` otherwise,
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
For the tau ID SF of the **embedded samples**, set the `emb` flag to `True`:
```
tauSFTool = TauIDSFTool('2017ReReco','DeepTau2017v2p1VSjet','Medium',emb=True)
```
If your analysis uses a DeepTauVSe WP looser than VLoose and/or DeepTauVSmu looser than medium discriminators,
should add additional uncertainty using the `otherVSlepWP` flag:
```
tauSFTool = TauIDSFTool('2017ReReco','DeepTau2017v2p1VSjet','Medium',otherVSlepWP=True)
```


### DM-dependent SFs

Analyses using ditau triggers and tau pT > 40 GeV, may use DM-dependent SFs.
They are provided as `TH1` histograms. For example, to obtain those for the medium WP of the `'DeepTau2017v2p1VSjet'` discriminator for 2016, use
```
file = TFile("data/TauID_SF_dm_DeepTau2017v2p1VSjet_2016Legacy.root")
hist = file.Get('Medium')
sf   = hist.GetBinContent(hist.GetXaxis().FindBin(dm))
```
or with the tool,
```
from TauPOG.TauIDSFs.TauIDSFTool import TauIDSFTool
tauSFTool = TauIDSFTool('2017ReReco','MVAoldDM2017v2','Tight',dm=True)
sf        = tauSFTool.getSFvsDM(pt,dm,genmatch)
sf_up     = tauSFTool.getSFvsDM(pt,dm,genmatch,unc='Up')
sf_down   = tauSFTool.getSFvsDM(pt,dm,genmatch,unc='Down')
```
where `genmatch` is optional.


### Eta-dependent fake rate SFs for the anti-lepton discriminators

To apply SFs to electrons or muons faking taus, use the eta of the reconstructed tau and the `genmatch` code.
They are provided as `TH1` histograms:
```
file = TFile("data/TauID_SF_eta_DeepTau2017v2p1VSmu_2016Legacy.root")
hist = file.Get('Medium')
sf   = hist.GetBinContent(hist.GetXaxis().FindBin(eta))
```
or with the tool,
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
It should be applied to a genuine tau by multiplying the tau `TLorentzVector`, or equivalently, the tau energy, pT and mass as follows:
```
file = TFile("data/TauES_dm_MVAoldDM2017v2_2016Legacy.root")
hist = file.Get('tes')
tes  = hist.GetBinContent(hist.GetXaxis().FindBin(dm))

# scale the tau's TLorentzVector
tau_tlv *= tes

# OR, scale the energy, mass and pT
tau_E  *= tes
tau_pt *= tes
tau_m  *= tes
```
A simple class, [`TauESTool`](python/TauIDSFTool.py), is provided to obtain the TES as
```
from TauPOG.TauIDSFs.TauIDSFTool import TauESTool
testool = TauESTool('2017ReReco','DeepTau2017v2p1VSjet')
tes     = testool.getTES(pt,dm,genmatch)
tesUp   = testool.getTES(pt,dm,genmatch,unc='Up')
tesDown = testool.getTES(pt,dm,genmatch,unc='Down')
```
This method computes the right uncertainty at intermediate (34 GeV < pT < 170 GeV) and higher pT values (pT > 170 GeV).
Analyses that only want to use the TES at high pT, can use the following instead:
```
tes     = testool.getTES_highpt(dm,genmatch)
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

