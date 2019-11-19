# Tau ID scale factors

This repository contains the recommended scale factors for tau discriminators.
More detailed recommendations can be found on [this TWiki page](https://twiki.cern.ch/twiki/bin/viewauth/CMS/TauIDRecommendationForRun2)
and instructions on how to use these can be found in the [README in the parent directory](https://github.com/cms-tau-pog/TauIDSFs#tau-id-scale-factors).


## Files

The files contain:
* `TauID_SF_dm_*_*.root`: DM-dependent SFs, with tau pT > 40 GeV.
* `TauID_SF_pt_*_*.root`: pT-dependent SFs.
* `TauID_SF_eta_*_*.root`: eta-dependent SFs for anti-lepton discriminators
* `TauES_dm_*.root`: Tau energy scales.


## Scale factor versions

The SFs in [`data`](data) are meant for the following campaigns:

| Year label   | MC campaign  | Data campaign |
|:------------:|:------------:| :------------:|
| `2016Legacy` | `RunIISummer16MiniAODv3` | `17Jul2018` |
| `2017ReReco` | `RunIIFall17MiniAODv2`   | `31Mar2018` |
| `2018ReReco` | `RunIIAutumn18MiniAOD`   | `17Sep2018`/`22Jan2019` |
