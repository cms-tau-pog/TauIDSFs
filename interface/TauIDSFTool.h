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
#include <string>    // std::string
#include <vector>    // std::vector
#include <map>       // std::map
#include <stdlib.h>  // getenv
#include <functional>

class TauIDSFTool {
    
  protected:
    
    std::map<const std::string,const TF1*> func;
    TH1* hist;
    void disabled() const{
      std::cerr << std::endl << "ERROR! Method has been disabled! isVsPT = "<<isVsPT<<", isVsDM = "<<isVsDM<<", isVsEta = "<<isVsEta<< std::endl;
      assert(0);
    }
    
  public:
    
    //std::string year;
    std::string ID;
    std::string WP;
    //std::string filename;
    std::vector<int> DMs;
    std::vector<int> genmatches;
    bool isVsPT  = false;
    bool isVsDM  = false;
    bool isVsEta = false;
    
    TauIDSFTool(const int year, const std::string& id="MVAoldDM2017v2", const std::string& wp="Tight", const bool dm=false);
    ~TauIDSFTool() { }
    
    float getSFvsPT( double pt,          int genmatch, const std::string& unc="");
    float getSFvsPT( double pt,                        const std::string& unc="");
    float getSFvsDM( double pt,  int dm, int genmatch, const std::string& unc="") const;
    float getSFvsDM( double pt,  int dm,               const std::string& unc="") const;
    float getSFvsEta(double eta,         int genmatch, const std::string& unc="") const;
  
};

#endif // TauIDSFTool_h