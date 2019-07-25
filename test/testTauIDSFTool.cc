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


void printSFTable(int year=2017,std::string id="MVAoldDM2017v2",std::string wp="Tight",bool dm=false){
  TauIDSFTool* sftool = new TauIDSFTool(year,id,wp,dm);
  std::cout << std::fixed;
  std::cout.precision(5);
  if(dm){
    std::vector<int> DMs    = {0,1,5,6,10,11};
    std::vector<int> ptvals = {25,50};
    for(auto const& pt: ptvals){
      std::cout << ">>> " << std::endl;
      std::cout << ">>> SF for "<<wp<<" WP of "<<id<<" in "<<year<<" with pT = "<<pt<<" GeV" << std::endl;
      std::cout << ">>> " << std::endl;
      std::cout << ">>> " << std::setw(9) << "var \\ DM";
      for(auto const& dm_: DMs)
        std::cout << std::setw(9) << dm_;
      std::cout << std::endl;
      std::cout << ">>> " << std::setw(9) << "central";
      for(auto const& dm_: DMs)
        std::cout << std::setw(9) << sftool->getSFvsDM(pt,dm_,5);
      std::cout << std::endl;
      std::cout << ">>> " << std::setw(9) << "up";
      for(auto const& dm_: DMs)
        std::cout << std::setw(9) << sftool->getSFvsDM(pt,dm_,5,"Up");
      std::cout << std::endl;
      std::cout << ">>> " << std::setw(9) << "down";
      for(auto const& dm_: DMs)
        std::cout << std::setw(9) << sftool->getSFvsDM(pt,dm_,5,"Down");
      std::cout << std::endl;
      std::cout << ">>> " << std::endl;
      //sftool->getSFvsPT(pt,5);    // results in an error
      //sftool->getSFvsEta(1.5,1,5); // results in an error
    }
  }else{
      std::vector<int> ptvals = {10,20,21,25,26,30,31,35,40,50,70,100,200,500,600,700,800,1000,1500,2000,};
      std::cout << ">>> " << std::endl;
      std::cout << ">>> SF for "<<wp<<" WP of "<<id<<" in "<<year<< std::endl;
      std::cout << ">>> " << std::endl;
      std::cout << ">>> " << std::setw(9) << "var \\ pt";
      for(auto const& pt: ptvals)
        std::cout << std::setw(9) << pt
        ;
      std::cout << std::endl;
      std::cout << ">>> " << std::setw(9) << "central";
      for(auto const& pt: ptvals)
        std::cout << std::setw(9) << sftool->getSFvsPT(pt,5);
      std::cout << std::endl;
      std::cout << ">>> " << std::setw(9) << "up";
      for(auto const& pt: ptvals)
        std::cout << std::setw(9) << sftool->getSFvsPT(pt,5,"Up");
      std::cout << std::endl;
      std::cout << ">>> " << std::setw(9) << "down";
      for(auto const& pt: ptvals)
        std::cout << std::setw(9) << sftool->getSFvsPT(pt,5,"Down");
      std::cout << std::endl;
      std::cout << ">>> " << std::endl;
      //sftool->getSFvsDM(25,1,5);   // results in an error
      //sftool->getSFvsEta(1.5,1,5); // results in an error
  }
}



int main(int argc, char* argv[]){
  std::cout << ">>> " << std::endl;
  std::cout << ">>> testTauIDSFTool" << std::endl;
  
  time_t time0, time1;
  time(&time0);
  
  std::vector<bool> DMs        = {true,false};
  std::vector<std::string> WPs = {"Loose","Medium","Tight"};
  std::string id = "MVAoldDM2017v2";
  
  for(auto const& dm: DMs){
    for(auto const& wp: WPs){
      printSFTable(2017,id,wp,dm);
    }
  }
  
  time(&time1);
  float seconds = time1 - time0;
  
  std::cout << ">>> " << std::endl;
  std::cout << ">>> done after " << seconds << " seconds" << std::endl;
  
  return 0;
}
