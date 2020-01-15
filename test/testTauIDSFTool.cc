/*
 * @executable testTauIDSFTool
 * @brief Train MVA for identifying hadronic tau decays
 * @instructions Compile and run with "scram b runtests"
 * @author Izaak Neutelings
 * @date July 2019
 *
 */

#include "TauPOG/TauIDSFs/interface/TauIDSFTool.h"
//#include <TBenchmark.h> // for timer
#include <iostream>
#include <iomanip> // std::setw
#include <string>
#include <vector>
#include <chrono>


void printSFTable(std::string year, std::string id, std::string wp, std::string vs, const bool emb=false){
  bool dm = (vs=="dm");
  TauIDSFTool* sftool = new TauIDSFTool(year,id,wp,dm,emb);
  std::cout << std::fixed;
  std::cout.precision(5);
  if(vs=="pt"){
      std::vector<int> ptvals = {10,20,21,25,26,30,31,35,40,50,70,100,200,500,600,700,800,1000,1500,2000,};
      std::cout << ">>>  " << std::endl;
      std::cout << ">>> SF for "<<wp<<" WP of "<<id<<" in "<<year;
      if (emb){
          std::cout << " for the embedded samples. " << std::endl;
      }
      else {
          std::cout << std::endl;
      }
      std::cout << ">>>  " << std::endl;
      std::cout << ">>>  " << std::setw(9) << "var \\ pt";
      for(auto const& pt: ptvals)
        std::cout << std::setw(9) << pt
        ;
      std::cout << std::endl;
      std::cout << ">>>  " << std::setw(9) << "central";
      for(auto const& pt: ptvals)
        std::cout << std::setw(9) << sftool->getSFvsPT(pt,5);
      std::cout << std::endl;
      std::cout << ">>>  " << std::setw(9) << "up";
      for(auto const& pt: ptvals)
        std::cout << std::setw(9) << sftool->getSFvsPT(pt,5,"Up");
      std::cout << std::endl;
      std::cout << ">>>  " << std::setw(9) << "down";
      for(auto const& pt: ptvals)
        std::cout << std::setw(9) << sftool->getSFvsPT(pt,5,"Down");
      std::cout << std::endl;
      std::cout << ">>>  " << std::endl;
      //sftool->getSFvsDM(25,1,5);   // results in an error
      //sftool->getSFvsEta(1.5,1,5); // results in an error
  }else if(vs=="dm"){
    std::vector<int> DMs    = {0,1,5,6,10,11};
    std::vector<int> ptvals = {25,50};
    for(auto const& pt: ptvals){
      std::cout << ">>>  " << std::endl;
      std::cout << ">>> SF for "<<wp<<" WP of "<<id<<" in "<<year<<" with pT = "<<pt<<" GeV";
      if (emb) {
          std::cout << " for the embedded samples." << std::endl;
      }
      else {
          std::cout << std::endl;
      }
      std::cout << ">>>  " << std::endl;
      std::cout << ">>>  " << std::setw(9) << "var \\ DM";
      for(auto const& dm_: DMs)
        std::cout << std::setw(9) << dm_;
      std::cout << std::endl;
      std::cout << ">>>  " << std::setw(9) << "central";
      for(auto const& dm_: DMs)
        std::cout << std::setw(9) << sftool->getSFvsDM(pt,dm_,5);
      std::cout << std::endl;
      std::cout << ">>>  " << std::setw(9) << "up";
      for(auto const& dm_: DMs)
        std::cout << std::setw(9) << sftool->getSFvsDM(pt,dm_,5,"Up");
      std::cout << std::endl;
      std::cout << ">>>  " << std::setw(9) << "down";
      for(auto const& dm_: DMs)
        std::cout << std::setw(9) << sftool->getSFvsDM(pt,dm_,5,"Down");
      std::cout << std::endl;
      std::cout << ">>>  " << std::endl;
      //sftool->getSFvsPT(pt,5);    // results in an error
      //sftool->getSFvsEta(1.5,1,5); // results in an error
    }
  }else if(vs=="eta"){
    std::vector<float> etavals = {0,0.2,0.5,1.0,1.5,2.0,2.2,2.3,2.4};
    std::vector<int> genmatches = {1,2};
    for(auto const& genmatch: genmatches){
      std::cout << ">>> " << std::endl;
      std::cout << ">>> SF for "<<wp<<" WP of "<<id<<" in "<<year<<" with genmatch "<<genmatch << std::endl;
      std::cout << ">>> " << std::endl;
      std::cout << ">>>  " << std::setw(9) << "var \\ eta";
      for(auto const& eta: etavals)
        std::cout << std::setw(9) << eta;
      std::cout << std::endl;
      std::cout << ">>>  " << std::setw(9) << "central";
      for(auto const& eta: etavals)
        std::cout << std::setw(9) << sftool->getSFvsEta(eta,genmatch);
      std::cout << std::endl;
      std::cout << ">>>  " << std::setw(9) << "up";
      for(auto const& eta: etavals)
        std::cout << std::setw(9) << sftool->getSFvsEta(eta,genmatch,"Up");
      std::cout << std::endl;
      std::cout << ">>>  " << std::setw(9) << "down";
      for(auto const& eta: etavals)
        std::cout << std::setw(9) << sftool->getSFvsEta(eta,genmatch,"Down");
      std::cout << std::endl;
      std::cout << ">>>  " << std::endl;
      //sftool->getSFvsPT(pt,5);    // results in an error
      //sftool->getSFvsDM(1.5,1,5); // results in an error
    }
  }
}



int main(int argc, char* argv[]){
  std::cout << ">>> " << std::endl;
  std::cout << ">>> testTauIDSFTool" << std::endl;
  auto start = std::chrono::system_clock::now();
  
  std::vector<std::string> years = {
    //"2016Legacy",
    "2017ReReco",
    //"2018ReReco"
  };
  std::vector<std::string> WPs   = {"Loose","Medium","Tight"};
  std::vector<std::string> IDs   = {
    "MVAoldDM2017v2",
    "DeepTau2017v2p1VSjet",
    "antiEleMVA6",
    "antiMu3",
    "DeepTau2017v2p1VSe",
    "DeepTau2017v2p1VSmu",
  };
  
  for(auto const& id: IDs){
    for(auto const& year: years){
      std::vector<std::string> vslist;
      if(id.find("anti")!=std::string::npos or id.find("VSe")!=std::string::npos or id.find("VSmu")!=std::string::npos)
        vslist = {"eta"};
      else
        vslist = {"pt","dm"};
      for(auto const& vs: vslist){
        for(auto const& wp: WPs){
          if(id=="antiMu3" and wp=="Medium") continue;
          printSFTable(year,id,wp,vs);
          if(id=="DeepTau2017v2p1VSjet")
            printSFTable(year,id,wp,vs,true);
        }
      }
    }
  }
  
  auto end = std::chrono::system_clock::now();
  std::chrono::duration<double> seconds = end-start;
  
  std::cout << ">>> " << std::endl;
  std::cout << ">>> done after " << seconds.count() << " seconds" << std::endl;
  
  return 0;
}
