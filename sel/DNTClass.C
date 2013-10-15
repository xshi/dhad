#define DNTClass_cxx
#include "DNTClass.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <cstring>

void DNTClass::Loop()
{
//   In a ROOT session, you can do:
//      Root > .L DNTClass.C
//      Root > DNTClass t
//      Root > t.GetEntry(12); // Fill t data members with entry number 12
//      Root > t.Show();       // Show values of entry 12
//      Root > t.Show(16);     // Read and show values of entry 16
//      Root > t.Loop();       // Loop on all entries
//

//     This is the loop skeleton where:
//    jentry is the global entry number in the chain
//    ientry is the entry number in the current Tree
//  Note that the argument to GetEntry must be:
//    jentry for TChain::GetEntry
//    ientry for TTree::GetEntry and TBranch::GetEntry
//
//       To read only selected branches, Insert statements like:
// METHOD1:
//    fChain->SetBranchStatus("*",0);  // disable all branches
//    fChain->SetBranchStatus("branchname",1);  // activate branchname
// METHOD2: replace line
//    fChain->GetEntry(jentry);       //read all branches
//by  b_branchname->GetEntry(ientry); //read only this branch



   if (fChain == 0) return;

   Long64_t nentries = fChain->GetEntriesFast();

   Int_t nbytes = 0, nb = 0;
   for (Long64_t jentry=0; jentry<10;jentry++) {
      Long64_t ientry = LoadTree(jentry);
      if (ientry < 0) break;
      nb = fChain->GetEntry(jentry);   nbytes += nb;
      // if (Cut(ientry) < 0) continue;

      // cout << "nbytes = " << nbytes
      // 	   << " run = " << run 
      // 	   << " event = " << event << endl;

      ts_->Fill();
      //if (jentry > 10) break;

      //ts_->Fill();
   }

   outputFile_->Write();
}

void DNTClass::Skim(TString skimfile)
{
  cout << "Skim file: " << skimfile << endl;
  
  if (fChain == 0) return;

  Long64_t nentries = fChain->GetEntriesFast();

  Int_t nbytes = 0, nb = 0;
  //for (Long64_t jentry=0; jentry<10;jentry++) {
  for (Long64_t jentry=0; jentry<nentries;jentry++) {

    Long64_t ientry = LoadTree(jentry);
    if (ientry < 0) break;
    nb = fChain->GetEntry(jentry);   nbytes += nb;
    // if (Cut(ientry) < 0) continue;
    if (FoundEvent(skimfile, run, event))
      ts_->Fill();
  }
  
  outputFile_->Write();
}


Bool_t DNTClass::FoundEvent(TString skimfile, Int_t run_, Int_t event_)
{
  string line;
  ifstream infile;
  vector<string> lines;

  infile.open(skimfile);
  while (getline(infile, line))
    lines.push_back(line);
  infile.close();
  
  for (int i = 0; i < lines.size(); i++)
    {
      line = lines[i];
      char* str = line.c_str();
      char* tok = strtok (str, " ");
      vector<string> parts;
      while (tok != NULL){
	parts.push_back(tok);
	tok = strtok (NULL, " ");
      }
      run = atoi(parts[0].c_str());
      event = atoi(parts[1].c_str());
      
      if (run == run_ && event == event_) 
	{
	  cout << "Found run: " << run << " event: " << event << endl;	  
	  return kTRUE;
	}
    }
  return kFALSE;
}


