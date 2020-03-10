#include "TauPOG/TauIDSFs/interface/TauIDSFTool.h"
#include <iostream> // std::cerr, std::endl
#include <iomanip>
#include <assert.h> // assert



TFile* ensureTFile(const TString filename, bool verbose=false){
  if(verbose)
    std::cout << "Opening " << filename << std::endl;
  TFile* file = new TFile(filename);
  if(!file or file->IsZombie()) {
    std::cerr << std::endl << "ERROR! Failed to open input file = '" << filename << "'!" << std::endl;
    assert(0);
  }
  return file;
}

TH1* extractTH1(const TFile* file, const std::string& histname){
  TH1* hist = dynamic_cast<TH1*>((const_cast<TFile*>(file))->Get(histname.data()));
  if(!hist){
    std::cerr << std::endl << "ERROR! Failed to load histogram = '" << histname << "' from input file!" << std::endl;
    assert(0);
  }
  return hist;
}

const TF1* extractTF1(const TFile* file, const std::string& funcname){
  const TF1* function = dynamic_cast<TF1*>((const_cast<TFile*>(file))->Get(funcname.data()));
  if(!function){
    std::cerr << std::endl << "ERROR! Failed to load function = '" << funcname << "' from input file!" << std::endl;
    assert(0);
  }
  return function;
}



void TauIDSFTool::disabled() const {
  std::cerr << std::endl << "ERROR! Method has been disabled! isVsPT = "<<isVsPT<<", isVsDM = "
            << isVsDM<<", isVsEta = "<<isVsEta<< std::endl;
  assert(0);
}


TauIDSFTool::TauIDSFTool(const std::string& year, const std::string& id, const std::string& wp, const bool dm, const bool embedding): ID(id), WP(wp){

  bool verbose = false;
  std::string datapath                = Form("%s/src/TauPOG/TauIDSFs/data",getenv("CMSSW_BASE"));
  std::vector<std::string> years      = {"2016Legacy","2017ReReco","2018ReReco"};
  std::vector<std::string> antiJetIDs = {"MVAoldDM2017v2","DeepTau2017v2p1VSjet"};
  std::vector<std::string> antiEleIDs = {"antiEleMVA6",   "DeepTau2017v2p1VSe"};
  std::vector<std::string> antiMuIDs  = {"antiMu3",       "DeepTau2017v2p1VSmu"};

  if(std::find(years.begin(),years.end(),year)==years.end()){
    std::cerr << std::endl << "ERROR! '"<<year<<"' is not a valid year! Please choose from ";
     std::vector<std::string>::iterator it = years.begin();
    for(it=years.begin(); it!=years.end(); it++){
      if(it!=years.begin()) std::cerr << ", ";
      std::cerr << *it;
    }
    std::cerr << std::endl;
    assert(0);
  }

  if(std::find(antiJetIDs.begin(),antiJetIDs.end(),ID)!=antiJetIDs.end()){
    if(dm){
      TString filename;
      if (embedding) {
          if (ID.find("oldDM") != std::string::npos)
          {
             std::cerr << "Scale factors for embedded samples are not provided for the MVA IDs." << std::endl;
             assert(0);
          }
          filename = Form("%s/TauID_SF_dm_%s_%s_EMB.root",datapath.data(),ID.data(),year.data());
      }
      else {
          filename = Form("%s/TauID_SF_dm_%s_%s.root",datapath.data(),ID.data(),year.data());
      }
      TFile* file = ensureTFile(filename,verbose);
      hist = extractTH1(file,WP);
      hist->SetDirectory(nullptr);
      file->Close();
      delete file;
      DMs    = {0,1,10};
      if (ID.find("oldDM") == std::string::npos)
      {
          DMs.push_back(11);
      }
      isVsDM = true;
    }else{
      TString filename;
      if (embedding) {
          if (ID.find("oldDM") != std::string::npos)
          {
             std::cerr << "Scale factors for embedded samples are not provided for the MVA IDs." << std::endl;
             assert(0);
          }
          filename = Form("%s/TauID_SF_pt_%s_%s_EMB.root",datapath.data(),ID.data(),year.data());
      }
      else {
          filename = Form("%s/TauID_SF_pt_%s_%s.root",datapath.data(),ID.data(),year.data());
      }
      TFile* file = ensureTFile(filename,verbose);
      func[""]     = extractTF1(file,Form("%s_cent",WP.data()));
      func["Up"]   = extractTF1(file,Form("%s_up",  WP.data()));
      func["Down"] = extractTF1(file,Form("%s_down",WP.data()));
      file->Close();
      delete file;
      isVsPT = true;
    }
  }else if(std::find(antiEleIDs.begin(),antiEleIDs.end(),ID)!=antiEleIDs.end()){
      if (embedding){
          std::cerr << "SF for ID " << ID << " not available for the embedded samples!" << std::endl;
          assert(0);
      }
      TString filename = Form("%s/TauID_SF_eta_%s_%s.root",datapath.data(),ID.data(),year.data());
      TFile* file = ensureTFile(filename,verbose);
      hist = extractTH1(file,WP);
      hist->SetDirectory(nullptr);
      file->Close();
      delete file;
      genmatches = {1,3};
      isVsEta    = true;
  }else if(std::find(antiMuIDs.begin(),antiMuIDs.end(),ID)!=antiMuIDs.end()){
      if (embedding){
          std::cerr << "SF for ID " << ID << " not available for the embedded samples!" << std::endl;
          assert(0);
      }
      TString filename = Form("%s/TauID_SF_eta_%s_%s.root",datapath.data(),ID.data(),year.data());
      TFile* file = ensureTFile(filename,verbose);
      hist = extractTH1(file,WP);
      hist->SetDirectory(nullptr);
      file->Close();
      delete file;
      genmatches = {2,4};
      isVsEta    = true;
  }else{
      std::cerr << "Did not recognize tau ID '" << ID << "'!" << std::endl;
      assert(0);
  }
}



float TauIDSFTool::getSFvsPT(double pt, int genmatch, const std::string& unc){
  if(!isVsPT) disabled();
  if(genmatch==5){
    float SF = static_cast<float>(func[unc]->Eval(pt));
    return SF;
  }
  return 1.0;
}

float TauIDSFTool::getSFvsPT(double pt, const std::string& unc){
  return getSFvsPT(pt,5,unc);
}



float TauIDSFTool::getSFvsDM(double pt, int dm, int genmatch, const std::string& unc) const{
  if(!isVsDM) disabled();
  if(std::find(DMs.begin(),DMs.end(),dm)!=DMs.end() or pt<=40){
    if(genmatch==5){
      Int_t bin = hist->GetXaxis()->FindBin(dm);
      float SF  = static_cast<float>(hist->GetBinContent(bin));
      if(unc=="Up")
        SF += hist->GetBinError(bin);
      else if(unc=="Down")
        SF -= hist->GetBinError(bin);
      return SF;
    }
    return 1.0;
  }
  return 0.0;
}

float TauIDSFTool::getSFvsDM(double pt, int dm, const std::string& unc) const{
  return getSFvsDM(pt,dm,5,unc);
}



float TauIDSFTool::getSFvsEta(double eta, int genmatch, const std::string& unc) const{
  if(!isVsEta) disabled();
  if(std::find(genmatches.begin(),genmatches.end(),genmatch)!=genmatches.end()){
    Int_t bin = hist->GetXaxis()->FindBin(eta);
    float SF  = static_cast<float>(hist->GetBinContent(bin));
    if(unc=="Up")
      SF += hist->GetBinError(bin);
    else if(unc=="Down")
      SF -= hist->GetBinError(bin);
    return SF;
  }
  return 1.0;
}
