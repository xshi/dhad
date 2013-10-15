//------------------------------------------------------------------
//
// Fitting the crossfeeds for the backgrouds non-diagonal
// 
// Adapted from Peter's PyROOT script
//
// Author:      Xin Shi
// Created:     Wed Apr 14 EST 2010
// $Id$
// 
//------------------------------------------------------------------

#include <iostream> // For ROOT4.03

using namespace RooFit ;


void crossfeeds_nondiag(TString title, 
			TString bkgfile,
			TString epsfile,
			TString txtfile,
			Double_t alpha_,
			Double_t mass_,
			Double_t n_,
			Double_t sigma_
			)
{

  RooRealVar mbc("mbc", "m_{BC}", 1.83, 1.89, "GeV");
  RooRealVar ebeam("ebeam", "Ebeam", 0., 100., "GeV");
  RooRealVar chg("chg", "Charge", -2, 2);
  RooCategory passed("passed", "Event should be used for plot");

  passed.defineType("yes", 1);
  passed.defineType("no", 0);

  RooRealVar arg_cutoff ("arg_cutoff", "Argus cutoff", 1.8865, 1.885, 1.8875,"GeV"); 
  RooRealVar arg_slope ("arg_slope", "Argus slope", -13, -100, 40);

  RooRealVar mbc_float ("mbc_float", "Floating D mass", mass_, "GeV"); 
  RooRealVar sigma ("sigma", "CB width", sigma_, "GeV"); 
  RooRealVar alpha("alpha", "CB shape cutoff", alpha_);
  RooRealVar n("n", "CB tail parameter", n_);

  RooCBShape cb_float ("cb_float", "Floating Crystal Barrel", mbc, mbc_float, sigma, alpha, n); 
  RooArgusBG argus("argus", "Argus BG", mbc, arg_cutoff, arg_slope);

  RooRealVar yld("yield", "D yield", 0, -30, 100000); 
  RooRealVar bkg("bkg", "Background", 20, 0, 40000);

  // Build pdf
  RooAddPdf sumpdf_float("sumpdf_float", "Generic D sum pdf", RooArgList(cb_float, argus),
			   RooArgList(yld, bkg));
  
  RooDataSet* dset = RooDataSet::read(bkgfile, RooArgList(mbc, ebeam, passed), "", "");

  RooPlot* xframe  = mbc.frame();

  RooDataSet* dset2 = dset->reduce("passed==1");

  dset2->plotOn(xframe);
  
  // RooFitResult* rv = sumpdf_float.fitTo(*dset2, Extended(kTRUE), Save(kTRUE),
  // 					Hesse(kTRUE), Verbose(kTRUE));
  RooFitResult* rv = sumpdf_float.fitTo(*dset2, "ermh");

  sumpdf_float.paramOn(xframe, dset2);

  if ((yld.getVal() < 0) && (-yld.getVal()/bkg.getVal() > 0.5)){
    yld.setVal(0);
    bkg.setVal(1);
  }
  
  sumpdf_float.plotOn(xframe);
  sumpdf_float.plotOn(xframe, Components(RooArgSet(argus)),
                      LineColor(kRed), LineStyle(kDashed));

  TCanvas* c1 = new TCanvas("c1","Canvas", 2);
  
  xframe->SetTitleOffset(2.2, "Y");
  xframe->SetTitleOffset(1.1, "X");
  xframe->SetTitle(title);

  c1->SetLeftMargin(0.17);
  xframe->Draw();
  
  if ( rv && rv->covQual() != 3){
    // fit has failed
    TText *txt = new TText();
    txt->SetTextSize(.08);
    txt->SetTextAlign(22);
    txt->SetTextAngle(30);
    txt->DrawTextNDC(0.5, 0.5, "FAILED");
  }
  

  c1->Update();
  c1->Print(epsfile);
  c1->Clear();

  FILE* table = fopen(txtfile.Data(), "w+");
  fprintf(table, "Name\t|| Value\t|| Error\n");
  //  fprintf(table, "yldsigma\t| %.10f\t| \n", yld.getVal()/yld.getError());
  fprintf(table, "entries\t| %.10f\t| \n", dset->numEntries());
  fprintf(table, "yld\t| %.10f\t| %.10f\n",  yld.getVal(), yld.getError());
  //  fprintf(table, "ratio\t| %.10f\t| \n",  yld.getVal()/dset->numEntries());
  //  fprintf(table, "ratioerr\t| %.10f\t| \n",  yld.getError()/dset->numEntries());
  fclose(table);

  cout << "Saved output as: " << txtfile << endl;

  rv->Delete();
}
