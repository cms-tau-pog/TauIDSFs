# Tau ID scale factors

This repository contains the recommended scale factors (SFs) for several tau discriminators, and tools to read them.
More detailed recommendations can be found on this TWiki page: https://twiki.cern.ch/twiki/bin/viewauth/CMS/TauIDRecommendationForRun2

> :warning: Please note that in the near future the SFs in the format of ROOT files will be phased out,
and in the long term superseded by the [`correctionlib` tool](https://github.com/cms-nanoAOD/correctionlib)
and [JSON files](https://gitlab.cern.ch/cms-nanoAOD/jsonpog-integration/) provided centrally by the XPOG.
More detailed instructions for tau corrections are
[here](https://gitlab.cern.ch/cms-tau-pog/jsonpog-integration/-/tree/master/POG/TAU#taupog-recommonded-tau-corrections).


## Table of Contents  
* [Installation of the tool](#installation-of-the-tool)<br>
  * [Python](#python)<br>
  * [C++](#c)<br>
  * [Python without CMSSW](#python-without-cmssw)<br>
* [Summary of available SFs](#summary-of-available-sfs)<br>
* [Usage](#usage)<br>
  * [pT-dependent SFs](#pt-dependent-sfs)<br>
  * [DM-dependent SFs](#dm-dependent-sfs)<br>
  * [Eta-dependent fake rate SFs for the anti-lepton discriminators](#eta-dependent-fake-rate-sfs-for-the-anti-lepton-discriminators)<br>
  * [DM-dependent tau energy scale](#dm-dependent-tau-energy-scale)<br>
  * [Eta- & DM-dependent e -> tau fake energy scale](#eta---dm-dependent-e---tau-fake-energy-scale)<br>


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

| Tau component  | `genmatch`  | `DeepTau2017v2p1` `VSjet`  | `DeepTau2017v2p1` `VSe`  | `DeepTau2017v2p1` `VSmu`  | `DeepTau2018v2p5` `VSjet`  | energy scale   |
|:--------------:|:-----------:|:--------------------------:|:------------------------:|:-------------------------:|:--------------:|
| real tau       | `5`         | vs pT and DM (for MC) or vs. pT, or vs. DM (for Embed.)          | – (*)                    | – (*)                     | vs pT and DM (for MC), no Embed. corrections derived yet | vs. DM         |
| e -> tau fake  | `1`, `3`    | –                          | vs. eta                  | –                         |    | vs. DM and eta |
| mu -> tau fake | `2`, `4`    | –                          | –                        | vs. eta                   |    | – (±1% unc.)   |

(*) The scale factors are provided only for a sub-set of the working points. For the VSele discriminator, they are measured for the VVLoose and Tight WPs - users are strongly encoraged to use one of these two working points and should report to the TauPOG for approval if another working point is used. For the VSmu, they are measured for the Tight WP but we don't expect a large dependence on the chosen VSmu WP in this case so you are free to use any available WP you like for the muon rejection. 

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

| Year label       | MC campaign              | Data campaign             |
|:----------------:|:------------------------:| :------------------------:|
| `2016Legacy` (*)    | `RunIISummer16MiniAODv3` | `17Jul2018`               |
| `2017ReReco` (*)    | `RunIIFall17MiniAODv2`   | `31Mar2018`               |
| `2018ReReco` (*)    | `RunIIAutumn18MiniAOD`   | `17Sep2018`/`22Jan2019`   |
| `UL2016_preVFP`  | `RunIISummer20UL16*APV`  | `(HIPM_)UL2016_MiniAODv*` |
| `UL2016_postVFP` | `RunIISummer20UL16`      | `UL2016_MiniAODv*`        |
| `UL2017`         | `RunIISummer20UL17`      | `UL2017_MiniAODv*`        |
| `UL2018`         | `RunIISummer20UL18`      | `UL2018_MiniAODv*`        |

(*) The SFs provided for pre-UL samples follow the old conventions for the binning by either pT or DM, and follow the old uncertainty scheme where only total uncertainties are reported



## Usage

A simple script is given to dump the corrections saved in histograms or functions of the files in [`data/`](data). Use for example
```
./test/dumpTauIDSFs.py data/TauID_SF_*_DeepTau2017v2p1VSjet_*.root
```

### DM and pT-dependent SFs
The DM and pT dependent SFs are provided as TF1 functions in the "TauID_SF_dm_DeepTau2017v2p1VSjet_VSjetX_VSeleY_Mar07.root" ROOT files for DeepTau2017v2p1 and "TauID_SF_dm_DeepTau2018v2p5VSjet_VSjetX_VSeleY_Jul18.root" for DeepTau2018v2p5, where X corresponds to the VSjet WP and Y corresponds to the VSele WP. 

The ROOT files contain several functions. The central values are obtained from the functions named like "DM$DM_$ERA_fit" where $DM is the decay mode = 0, 1, 10, or 11, and $ERA = 2016_preVFP, 2016_postVFP, 2017, or 2018.

For example to obtain the central value of the SFs for the Medium VSjet and VVLoose VSele WPs of the `'DeepTau2017v2p1VSjet'` discriminator for DM=1 in 2018, use
```
file = TFile("data/TauID_SF_dm_DeepTau2017v2p1VSjet_VSjetMedium_VSeleVVLoose_Mar07.root")
func = file.Get('DM1_2018_fit')
sf   = func.Eval(pt)
```

There are also  that correspond to systematic variations that can be accessed in the same way. 
The table below gives a summary of the function names and what uncertainties they correspond to for DeepTau2017v2p1:

| Uncertainty      | Function name in ROOT files | String to pass to the tool | Notes                            | Correlated by era | Correlated by DM |
|:----------------:|:---------------------------:| :-------------------------:| :-------------------------------:| :----------------:| :----------------:|
| `Statistical uncertainty 1` | `DM$DM_$ERA_fit_uncert0_{up,down}` | `uncert0_{up,down}` | `Statistical uncertainty on linear fit parameters from eigendecomposition of covariance matrix.` | &cross; | &cross; |
| `Statistical uncertainty 2` | `DM$DM_$ERA_fit_uncert1_{up,down}` | `uncert1_{up,down}` | `Statistical uncertainty on linear fit parameters from eigendecomposition of covariance matrix.` | &cross; | &cross; |
| `Systematic alleras`        | `DM$DM_$ERA_syst_alleras_{up,down}_fit` | `syst_alleras_{up,down}` | `The component of the systematic uncertainty that is correlated across DMs and eras` | &check; | &check; |
| `Systematic by-era`         | `DM$DM_$ERA_syst_$ERA_{up,down}_fit`    | `syst_$ERA_{up,down}` | `The component of the systematic uncertainty that is correlated across DMs but uncorrelated by eras` | &cross; | &check; |
| `Systematic by-era and by-DM` | `DM$DM_$ERA_syst_dm$DM_$ERA_{up,down}_fit` | `syst_dm$DM_$ERA_{up,down}` | `The component of the systematic uncertainty that is uncorrelated across DMs and eras` | &cross; | &cross; |

The table below gives a summary of the function names and what uncertainties they correspond to for DeepTau2018v2p5:

| Uncertainty      | Function name in ROOT files | String to pass to the tool | Notes                            | Correlated by era | Correlated by DM |
|:----------------:|:---------------------------:| :-------------------------:| :-------------------------------:| :----------------:| :----------------:|
| `Statistical uncertainty 1` | `DM$DM_$ERA_fit_uncert0_{up,down}` | `uncert0_{up,down}` | `Statistical uncertainty on linear fit parameters from eigendecomposition of covariance matrix for the low pT (20-50 GeV) regime.` | &cross; | &cross; |
| `Statistical uncertainty 2` | `DM$DM_$ERA_fit_uncert1_{up,down}` | `uncert1_{up,down}` | `Statistical uncertainty on linear fit parameters from eigendecomposition of covariance matrix for the medium pT (50-140 GeV) regime.` | &cross; | &cross; |
| `Statistical uncertainty 3` | `DM$DM_$ERA_fit_uncert0_{up,down}` | `uncert2_{up,down}` | `Statistical uncertainty on linear fit parameters from eigendecomposition of covariance matrix for the low pT (20-50 GeV) regime.` | &cross; | &cross; |
| `Statistical uncertainty 4` | `DM$DM_$ERA_fit_uncert1_{up,down}` | `uncert3_{up,down}` | `Statistical uncertainty on linear fit parameters from eigendecomposition of covariance matrix for the medium pT (50-140 GeV) regime.` | &cross; | &cross; |
| `Systematic alleras`        | `DM$DM_$ERA_syst_alleras_{up,down}_fit` | `syst_alleras_{up,down}` | `The component of the systematic uncertainty that is correlated across DMs and eras` | &check; | &check; |
| `Systematic by-era`         | `DM$DM_$ERA_syst_$ERA_{up,down}_fit`    | `syst_$ERA_{up,down}` | `The component of the systematic uncertainty that is correlated across DMs but uncorrelated by eras` | &cross; | &check; |
| `Systematic by-era and by-DM` | `DM$DM_$ERA_syst_dm$DM_$ERA_{up,down}_fit` | `syst_dm$DM_$ERA_{up,down}` | `The component of the systematic uncertainty that is uncorrelated across DMs and eras` | &cross; | &cross; |

The SFs can also be accessed using the tool:

```
from TauPOG.TauIDSFs.TauIDSFTool import TauIDSFTool
tauSFTool = TauIDSFTool(year='UL2018',id='DeepTau2017v2p1VSjet',wp='Medium',wp_vsele='VVLoose',ptdm=True)
sf        = tauSFTool.getSFvsDMandPT(pt,dm,genmatch)
```

And uncertainty variations can be accessed using:

```
sf        = tauSFTool.getSFvsDMandPT(pt,dm,genmatch,unc)
```

where the `unc` string is used to identify the systematic variation as given in the third column in the above table 

### High-pT pT-dependent SFs

Analyses that are sensitive to taus with pT>140 GeV should switch to the dedicated high pT SFs measured in bins of pT above 140 GeV

The SFs are provided as TGraphAsymmErrors objects in the "TauID_SF_Highpt_DeepTau2017v2p1VSjet_VSjetX_VSeleY_Mar07.root" ROOT files, where X corresponds to the VSjet WP and Y corresponds to the VSele WP. 

The ROOT files contain several graphs. The central values are obtained from the graphs named like "DMinclusive_$ERA" where $ERA = 2016_preVFP, 2016_postVFP, 2017, or 2018. These graphs contain 2 pT bins with pT 100-200, and pT>200 GeV. You should only use these as binned values. For taus between 140-200 GeV use the first bin, and for taus with pT>200 GeV use the second bin. 

The SFs can also be accessed using the tool:

```
from TauPOG.TauIDSFs.TauIDSFTool import TauIDSFTool
tauSFTool = TauIDSFTool(year='UL2018',id='DeepTau2017v2p1VSjet',wp='Medium',wp_vsele='VVLoose',highpT=True)
sf        = tauSFTool.getHighPTSFvsPT(pt,genmatch)
```

And uncertainty variations can be accessed using:

```
sf        = tauSFTool.getHighPTSFvsPT(pt,genmatch,unc)
```

where "unc" dependends on the uncertainty source. The table below describes the uncertainty sources and the string you need to pass to the tool to retrieve them:

| Uncertainty      | String to pass to the tool | Notes                            | Correlated by era | Correlated by pT |
|:----------------:|:--------------------------:| :-------------------------------:| :----------------:| :---------------:|
| `Statistical uncertainty 1` | `stat_bin1_{up,down}` | `Statistical uncertainty on the pT 140-200 GeV bin. Note this also includes systematic uncertainties that are decorrelated by pT bin and era (since they also behave like statistical uncertainties)` | &cross; | &cross; | 
| `Statistical uncertainty 2` | `stat_bin2_{up,down}` | `Statistical uncertainty on the pT >200 GeV bin. Note this also includes systematic uncertainties that are decorrelated by pT bin and era (since they also behave like statistical uncertainties)` | &cross; | &cross; |
| `Systematic` | `syst_{up,down}` | `The systematic uncertainty that is correlated across pT regions and eras` | &check; | &check; |
| `Extrapolation Systematic` | `extrap_{up,down}` | `The systematics uncertainty due to the extrapolation of the SF to higher pT regions` | &check; | &check; | 

### pT-dependent SFs

***Deprecated for UL MC - use DM and pT-dependent SFs instead!***

***The embedded scale factors still follow the old prescriptions for pT or DM binned SFs so these instructions still apply in this case***

The pT-dependent SFs are provided as `TF1` functions. For example, to obtain those for the medium WP of the `'DeepTau2017v2p1VSjet'` discriminator for 2016, use
```
file = TFile("data/TauID_SF_pt_DeepTau2017v2p1VSjet_2016Legacy.root")
func = file.Get('Medium_cent')
sf   = func.Eval(pt)
```
The tool can be used as
```
from TauPOG.TauIDSFs.TauIDSFTool import TauIDSFTool
tauSFTool = TauIDSFTool('2016Legacy','DeepTau2017v2p1VSjet','Medium',ptdm=False)
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

***Deprecated for UL MC - use DM and pT-dependent SFs instead!***

***The embedded scale factors still follow the old prescriptions for pT or DM binned SFs so these instructions still apply in this case***

Analyses using ditau triggers and tau pT > 40 GeV, may use DM-dependent SFs.
Please note that no SFs are available for decay modes 5 and 6, and the tool will return 1 by default, please read this
[TWiki section](https://twiki.cern.ch/twiki/bin/view/CMS/TauIDRecommendationForRun2#Decay_Mode_Reconstruction).
They are provided as `TH1` histograms. For example, to obtain those for the medium WP of the `'DeepTau2017v2p1VSjet'` discriminator for 2016, use
```
file = TFile("data/TauID_SF_dm_DeepTau2017v2p1VSjet_2016Legacy.root")
hist = file.Get('Medium')
sf   = hist.GetBinContent(hist.GetXaxis().FindBin(dm))
```
or with the tool,
```
from TauPOG.TauIDSFs.TauIDSFTool import TauIDSFTool
tauSFTool = TauIDSFTool('2017ReReco','MVAoldDM2017v2','Tight',dm=True,ptdm=False)
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

<p align="center">
  <img src="docs/TESunc.png" alt="Tau energy scale uncertainty treatment" width="390"/>
</p>

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

