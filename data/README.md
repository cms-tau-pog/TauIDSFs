# Tau ID scale factors

This repository contains the recommended scale factors for tau discriminators.
More detailed recommendations can be found on [this TWiki page](https://twiki.cern.ch/twiki/bin/viewauth/CMS/TauIDRecommendationForRun2)
and instructions on how to use these can be found in the [README in the parent directory](../../../#tau-id-scale-factors).


## Files

The files contain:
* `TauID_SF_dm_*_*.root`: DM-dependent SFs, with tau pT > 40 GeV.
* `TauID_SF_pt_*_*.root`: pT-dependent SFs.
* `TauID_SF_eta_*_*.root`: eta-dependent fake rate SFs for anti-lepton discriminators
* `TauES_dm_*_*.root`: Tau energy scales.
* `TauFES_eta-dm_*_*.root`: Electron to tau fake energy scales.

What they should be applied to is summarized in [README of the parent directory](../../../#summary-of-available-sfs).


## Accessing the files

More complete instructions are provided in the [README of the parent directory](../../../#tau-id-scale-factors).

A simple script is given to dump the corrections saved in histograms or functions of the files above. Use for example
```
./test/dumpTauIDSFs.py data/TauID_SF_*_DeepTau2017v2p1VSjet_*.root
```

### pT-dependent SFs
```
file = TFile("data/TauID_SF_pt_DeepTau2017v2p1VSjet_2016Legacy.root")
func = file.Get('Medium_cent')
sf   = sf.Eval(pt)
```

### DM-dependent SFs
```
file = TFile("data/TauID_SF_dm_DeepTau2017v2p1VSjet_2016Legacy.root")
hist = file.Get('Medium')
sf   = hist.GetBinContent(hist.GetXaxis().FindBin(dm))
```

### eta-dependent fake rate SFs

```
file = TFile("data/TauID_SF_eta_DeepTau2017v2p1VSmu_2016Legacy.root")
hist = file.Get('Medium')
sf   = hist.GetBinContent(hist.GetXaxis().FindBin(eta))
```

### DM-dependent energy scale

```
file = TFile("data/TauES_dm_MVAoldDM2017v2_2016Legacy.root")
hist = file.Get('tes')
tes  = hist.GetBinContent(hist.GetXaxis().FindBin(dm))
```

### DM- and eta-dependent energy scale

```
file  = TFile("data/TauFES_eta-dm_DeepTau2017v2p1VSe_2016Legacy.root")
graph = file.Get('fes')
```
