#ifndef TauIDSFTool_h
#define TauIDSFTool_h

/*
 * @class TauIDSFTool
 *
 * Class to retrieve tau ID SFs.
 *  - pT-dependent SFs for MVAoldDM2017v2
 *  - DM-dependent SFs for MVAoldDM2017v2
 *  - eta-dependent SFs for anti-lepton discriminators
 * Source: https://twiki.cern.ch/twiki/bin/viewauth/CMS/TauIDRecommendation13TeV
 * Inspiration from TauTriggerSFs/src/TauTriggerSFs2017.cc
 *
 * @author Izaak Neutelings
 * @date July 2019
 *
 */

#include <TFile.h>   // TFile
#include <TH1.h>     // TH1
#include <TF1.h>     // TF1
#include <TString.h> // Form
#include <TGraph.h>     // TGraph
#include <string>    // std::string
#include <vector>    // std::vector
#include <map>       // std::map
#include <stdlib.h>  // getenv
#include <functional>

class TauIDSFTool {

  protected:

    std::map<const std::string,const TF1*> func;
    std::map<const std::string,const TGraph*> graph;
    TH1* hist;
    std::map<std::string, const TF1*> funcs_dm0;
    std::map<std::string, const TF1*> funcs_dm1;
    std::map<std::string, const TF1*> funcs_dm10;
    std::map<std::string, const TF1*> funcs_dm11;
    [[noreturn]] void disabled() const;

  public:

    std::string ID;
    std::string WP;
    std::string WP_VSELE;
    std::vector<int> DMs;
    std::vector<int> genmatches;
    bool isVsPT  = false;
    bool isHighPTVsPT  = false;
    bool isVsDM  = false;
    bool isVsEta = false;
    bool isVsDMandPT  = false;

    TauIDSFTool(const std::string& year, const std::string& id="DeepTau2017v2p1VSjet", const std::string& wp="Medium", const std::string& wp_vsele="VVLoose",
                const bool dm=false, const bool ptdm=true, const bool embedding=false, const bool highpT=false);
    ~TauIDSFTool() { }

    float getSFvsPT( double pt,          int genmatch, const std::string& unc="");
    float getSFvsPT( double pt,                        const std::string& unc="");
    float getHighPTSFvsPT( double pt,          int genmatch, const std::string& unc="");
    float getHighPTSFvsPT( double pt,          const std::string& unc="");
    float getSFvsDM( double pt,  int dm, int genmatch, const std::string& unc="") const;
    float getSFvsDM( double pt,  int dm,               const std::string& unc="") const;
    float getSFvsEta(double eta,         int genmatch, const std::string& unc="") const;
    float getSFvsDMandPT( double pt,  int dm, int genmatch, const std::string& unc="") const;
    float getSFvsDMandPT( double pt,  int dm,               const std::string& unc="") const;

};

#endif // TauIDSFTool_h
