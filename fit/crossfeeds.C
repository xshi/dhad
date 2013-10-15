//------------------------------------------------------------------
//
// Fitting the crossfeeds for the backgrouds
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

void crossfeeds(TString title, 
		TString bkgfile,
		TString epsfile,
		TString txtfile
		)
{

  RooRealVar mbc("mbc", "m_{BC}", 1.83, 1.89, "GeV");
  RooRealVar ebeam("ebeam", "Ebeam", 0., 100., "GeV");
  RooRealVar chg("chg", "Charge", -2, 2);
  RooCategory passed("passed", "Event should be used for plot");

  passed.defineType("yes", 1);
  passed.defineType("no", 0);

  RooRealVar arg_cutoff ("arg_cutoff", "Argus cutoff", 1.8869, 1.885, 1.8875,"GeV"); 
  RooRealVar arg_slope ("arg_slope", "Argus slope", -13, -100, 40);
  RooRealVar mbc_float ("mbc_float", "Floating D mass", 1.869, 1.855, 1.875,"GeV"); 
  RooRealVar sigma ("sigma", "CB width", 0.00145, 0.0001, 0.005,"GeV"); 
  RooRealVar alpha("alpha", "CB shape cutoff", -1.515, -2., 2);
  RooRealVar n("n", "CB tail parameter", 6, 0, 20);
  RooCBShape cb_float ("cb_float", "Floating Crystal Barrel", mbc, mbc_float, sigma, alpha, n); 
  RooArgusBG argus("argus", "Argus BG", mbc, arg_cutoff, arg_slope);

    
  RooRealVar yld("yield", "D yield", 25700, -30, 100000); 
  RooRealVar bkg("bkg", "Background", 1300, 0, 40000);

  // Build pdf
  RooAddPdf sumpdf_float("sumpdf_float", "Generic D sum pdf", RooArgList(cb_float, argus),
			   RooArgList(yld, bkg));
  
  RooDataSet* dset = RooDataSet::read(bkgfile, RooArgList(mbc, ebeam, passed), "", "");

  RooPlot* xframe  = mbc.frame();

  RooDataSet* dset2 = dset->reduce("passed==1");

  dset2->plotOn(xframe);

  arg_cutoff.setVal(1.8865); 
  arg_cutoff.setConstant(1);
  RooFitResult* rv = sumpdf_float.fitTo(*dset2, "ermq");
  // RooFitResult* rv = sumpdf_float.fitTo(*dset2, Extended(kTRUE), Save(kTRUE),
  // 					Hesse(kFALSE), Verbose(kFALSE)); 
  rv->Print();
 
  sumpdf_float.plotOn(xframe);
  sumpdf_float.plotOn(xframe, Components(RooArgSet(argus)),
                      LineColor(kRed), LineStyle(kDashed));
  sumpdf_float.paramOn(xframe, dset2);

  TCanvas* c1 = new TCanvas("c1","Canvas", 2);
  
  xframe->SetTitleOffset(2.2, "Y");
  xframe->SetTitleOffset(1.1, "X");
  xframe->SetTitle(title);

  c1->SetLeftMargin(0.17);
  xframe->Draw();
  if (rv->covQual() != 3){
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
  fprintf(table, "mass\t| %.10f\t| %.10f\n", mbc_float.getVal(), mbc_float.getError());
  fprintf(table, "sigma\t| %.10f\t| %.10f\n", sigma.getVal(), sigma.getError());
  fprintf(table, "n\t| %.10f\t| %.10f\n", n.getVal(), n.getError());
  fprintf(table, "alpha\t| %.10f\t| %.10f\n", alpha.getVal(), alpha.getError());
  fprintf(table, "entries\t| %.10f\t| \n", dset->numEntries());
  fprintf(table, "yield\t| %.10f\t| \n", yld.getVal());
  fprintf(table, "ratio\t| %.10f\t| \n", yld.getVal()/dset->numEntries());
  fclose(table);
  
  cout << "Saved output as: " << txtfile << endl;

  rv->Delete();

}
