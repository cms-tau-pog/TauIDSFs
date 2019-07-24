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

TH1* loadTH1(const TFile* file, const std::string& histname){
  TH1* hist = dynamic_cast<TH1*>((const_cast<TFile*>(file))->Get(histname.data()));
  if(!hist){
    std::cerr << std::endl << "ERROR! Failed to load histogram = '" << histname << "' from input file!" << std::endl;
    assert(0);
  }
  return hist;
}

const TF1* loadTF1(const TFile* file, const std::string& funcname){
  const TF1* function = dynamic_cast<TF1*>((const_cast<TFile*>(file))->Get(funcname.data()));
  if(!function){
    std::cerr << std::endl << "ERROR! Failed to load function = '" << funcname << "' from input file!" << std::endl;
    assert(0);
  }
  return function;
}



TauIDSFTool::TauIDSFTool(const int year, const std::string& id, const std::string& wp, const bool dm): ID(id), WP(wp){
  
  bool verbose = false;
  std::string datapath = Form("%s/src/TauPOG/TauIDSFs/data",getenv("CMSSW_BASE"));
  std::vector<std::string> antiJetIDs  = {"MVAoldDM2017v2"};
  std::vector<std::string> antiEleIDs  = {"antiEleMVAV6"};
  std::vector<std::string> antiMuonIDs = {"antiMuV3"};
  
  if(std::find(antiJetIDs.begin(),antiJetIDs.end(),ID)!=antiJetIDs.end()){
    if(dm){
      TString filename = Form("%s/TauID_SF_dm_%s_%d.root",datapath.data(),ID.data(),year);
      TFile* file = ensureTFile(filename,verbose);
      hist = loadTH1(file,WP);
      hist->SetDirectory(0);
      file->Close();
      DMs    = {0,1,10};
      isVsDM = true;
    }else{
      TString filename = Form("%s/TauID_SF_pt_%s_%d.root",datapath.data(),ID.data(),year);
      TFile* file = ensureTFile(filename,verbose);
      func[""]     = loadTF1(file,Form("%s_cent",WP.data()));
      func["Up"]   = loadTF1(file,Form("%s_up",  WP.data()));
      func["Down"] = loadTF1(file,Form("%s_down",WP.data()));
      file->Close();
      isVsPT = true;
    }
  }else if(std::find(antiEleIDs.begin(),antiEleIDs.end(),ID)!=antiEleIDs.end()){
      TString filename = Form("%s/TauID_SF_eta_%s_%d.root",datapath.data(),ID.data(),year);
      TFile* file = ensureTFile(filename,verbose);
      hist = loadTH1(file,WP);
      hist->SetDirectory(0);
      file->Close();
      genmatches = {1,3};
      isVsEta    = true;
  }else if(std::find(antiMuonIDs.begin(),antiMuonIDs.end(),ID)!=antiMuonIDs.end()){
      TString filename = Form("%s/data/TauID_SF_eta_%s_%d.root",getenv("CMSSW_BASE"),ID.data(),year);
      TFile* file = ensureTFile(filename,verbose);
      hist = loadTH1(file,WP);
      hist->SetDirectory(0);
      file->Close();
      genmatches = {2,4};
      isVsEta    = true;
  }else{
      std::cerr << "Did not recognize tau ID '" << ID << "'!" << std::endl;
      assert(0);
  }
}



float TauIDSFTool::getSFvsPT( double pt, int genmatch, const std::string& unc){
  if(!isVsPT) disabled();
  if(genmatch==5){
    float SF = func[unc]->Eval(pt);
    return SF;
  }
  return 1.0;
}

float TauIDSFTool::getSFvsPT( double pt, const std::string& unc){
  return getSFvsPT(pt,5,unc);
}



float TauIDSFTool::getSFvsDM( double pt, int dm, int genmatch, const std::string& unc) const{
  if(!isVsDM) disabled();
  if(std::find(DMs.begin(),DMs.end(),dm)!=DMs.end() or pt<=40){
    if(genmatch==5){
      Int_t bin = hist->GetXaxis()->FindBin(dm);
      float SF  = hist->GetBinContent(bin);
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

float TauIDSFTool::getSFvsDM( double pt, int dm, const std::string& unc) const{
  return getSFvsDM(pt,dm,5,unc);
}



float TauIDSFTool::getSFvsEta(double eta, int genmatch, const std::string& unc) const{
  if(!isVsEta) disabled();
  if(std::find(genmatches.begin(),genmatches.end(),genmatch)!=genmatches.end()){
    Int_t bin = hist->GetXaxis()->FindBin(eta);
    float SF  = hist->GetBinContent(bin);
    if(unc=="Up")
      SF += hist->GetBinError(bin);
    else if(unc=="Down")
      SF -= hist->GetBinError(bin);
    return SF;
  }
  return 1.0;
}
