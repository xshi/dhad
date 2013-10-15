#include <iostream>
#include <stdio.h>
using namespace RooFit;


void lineshapefit2d(TString mode1,
		    double dsigma1,
		    double df1a,
		    double df1b,
		    double ds1a,
		    double ds1b,
		    TString mode2, 
		    double dsigma2,
		    double df2a,
		    double df2b,
		    double ds2a,
		    double ds2b,
		    TString file, 
		    TString epsfile,
		    TString txtfile,
		    int mc = 0,
		    TString opt="",
		    TString title1='',
		    TString title2='',
		    double gammad=0.0275,
		    double setMres = 3.774,
		    double setR=15.0,
		    double setN      = 4000.0,
		    double setNbkgd1 = 1.0,
		    double setNbkgd2 = 1.0,
		    double setNbkgd3 = 1.0,
		    double setNbkgdFlat = 1.0
		    ){


  // opt meanings:
  // a means that sigma on diag is const

  // f means to fit for the lineshape parameters, sigma, fa fb, sa, sb
   //f1 means Use the s1b and f1b only for modes with pi0
   
  // g means to float 3770 widht
  // h means gamma=35.0MeV

  // l means gamma=23.6MeV
  // m means float d mass

  // p means p=0.5

  // s means float sigmaE

  TString  rootfile ;
  rootfile = epsfile ;
  rootfile.Replace(epsfile.Sizeof()-4, 3, "root");

  TCanvas *canvas=new TCanvas("c","DLineShape",900,300);

  RooRealVar mbc1("mbc1","mbc1",1.83,1.89,"GeV");
  RooRealVar mbc2("mbc2","mbc2",1.83,1.89,"GeV");
//  RooRealVar Ebeam("Ebeam","Ebeam",1.8815,1.892,"GeV");
  RooRealVar Ebeam("Ebeam","Ebeam",1.8854,1.8911,"GeV");

  RooRealVar EbeamFix("EbeamFix","EbeamFix",1.887);

//   double dsigma1,df1a,df1b,ds1a,ds1b;
//   double dsigma2,df2a,df2b,ds2a,ds2b;
//   fitpars(mode1,dsigma1,df1a,df1b,ds1a,ds1b);
//   fitpars(mode2,dsigma2,df2a,df2b,ds2a,ds2b);

  RooRealVar res("datares","datares",mc);

  RooRealVar mres("mres","mres",setMres);
  RooRealVar *gamma;
  // mc = 0  BW shape  
  // mc = -1 "Broken" MC
  // mc = 1  MARK III (data)
  // mc = 3  BES 2007 paper (BES2006 lineshape hepex/0612056) 
  //         RooFitModels/RooDEnergyImp.cc

  if (mc == -1){
    gamma=new RooRealVar("gamma","gamma",0.0236);
  }
  else{
    if (opt.Contains("l")) gammad=0.0236;
    if (opt.Contains("h")) gammad=0.035;
    if (opt.Contains("g")){
      gamma=new RooRealVar("gamma","gamma",0.024,0.002,0.050);
    }
    else{
      gamma=new RooRealVar("gamma","gamma",gammad);
    }
  }
  RooRealVar* sigmaE;
  if (opt.Contains('s')) {
    sigmaE = new RooRealVar("sigmaE","sigmaE",0.0021,0.0015,0.0025);
  } else {
    sigmaE = new RooRealVar("sigmaE","sigmaE",0.0021);
  }

  double mdd=1.86912;

  if (mode1=="kpi"||mode1=="kpipi0"||mode1=="kpipipi") mdd=1.86415;

  RooRealVar* md;
  if (opt.Contains('m')) {
    md = new RooRealVar("md","md",mdd,1.863,1.873);
  } else {
    md = new RooRealVar("md","md",mdd);
  }


  RooDataSet* dataset = RooDataSet::read(file,RooArgSet(mbc1,mbc2,Ebeam));
  //RooDataSet* dataset = RooDataSet::read(file,RooArgSet(mbc1,mbc2));

  RooRealVar *s1a;
  RooRealVar *s1b;
  RooRealVar *sigmacommon1;
  RooRealVar *f1a;
  RooRealVar *f1b;


  RooAbsReal *s2a;
  RooAbsReal *s2b;
  RooAbsReal *sigmacommon2;
  RooAbsReal *f2a;
  RooAbsReal *f2b;


  if (opt.Contains("f")){
    s1a=new RooRealVar("s1a","s1a",ds1a,1.5,4.0);

    sigmacommon1=new RooRealVar("sigmacommon1","sigmacommon1",dsigma1,0.003,0.008);
    f1a=new RooRealVar("f1a","f1a",df1a,0.0,0.5);

    if (opt.Contains("f1")){
//   Use the s1b and f1b only for modes with pi0
       if (mode1=="kpipi0"||mode1=="kpipipi0"||mode1=="kspipi0"){
	  s1b=new RooRealVar("s1b","s1b",2.0,1.5,4.0);
	  f1b=new RooRealVar("f1b","f1b",0.05,0.0,0.4);
       }
       else {
	  s1b=new RooRealVar("s1b","s1b",1.0);
	  f1b=new RooRealVar("f1b","f1b",0.0);
       }
    }
    else {
       s1b=new RooRealVar("s1b","s1b",ds1b,1.5,4.0);
       f1b=new RooRealVar("f1b","f1b",df1b,0.0,0.4);
    }

    if (mode1==mode2){
      s2a=new RooFormulaVar("s2a","s1a",RooArgList(*s1a));
      s2b=new RooFormulaVar("s2b","s1b",RooArgList(*s1b));
      sigmacommon2=new RooFormulaVar("sigmacommon2","sigmacommon1",RooArgList(*sigmacommon1));
      f2a=new RooFormulaVar("f2a","f1a",RooArgList(*f1a));
      f2b=new RooFormulaVar("f2b","f1b",RooArgList(*f1b));
    }
    else{
      s2a=new RooRealVar("s2a","s2a",2.0,1.5,4.0);
      s2b=new RooRealVar("s2b","s2b",2.0,1.5,4.0);
      sigmacommon2=new RooRealVar("sigmacommon2","sigmacommon2",0.005,0.003,0.008);
      f2a=new RooRealVar("f2a","f2a",0.05,0.0,0.4);
      f2b=new RooRealVar("f2b","f2b",0.05,0.0,0.4);
	}
  }
  else {
    s1a=new RooRealVar("s1a","s1a",ds1a);
    s1b=new RooRealVar("s1b","s1b",ds1b);
    sigmacommon1=new RooRealVar("sigmacommon1","sigmacommon1",dsigma1);
    f1a=new RooRealVar("f1a","f1a",df1a);
    f1b=new RooRealVar("f1b","f1b",df1b);


    s2a=new RooRealVar("s2a","s2a",ds2a);
    s2b=new RooRealVar("s2b","s2b",ds2b);
    sigmacommon2=new RooRealVar("sigmacommon2","sigmacommon2",dsigma2);
    f2a=new RooRealVar("f2a","f2a",df2a);
    f2b=new RooRealVar("f2b","f2b",df2b);


  }

  RooRealVar *r;

  r=new RooRealVar("r","r", setR);
  //r=new RooRealVar("r","r",15.0);

  RooFormulaVar sigma1a("sigma1a","sigmacommon1*s1a",
			     RooArgList(*s1a,*sigmacommon1));
  RooFormulaVar sigma1b("sigma1b","sigmacommon1*s1a*s1b",
			  RooArgList(*s1a,*s1b,*sigmacommon1));













  RooFormulaVar sigma2a("sigma2a","sigmacommon2*s2a",
			     RooArgList(*s2a,*sigmacommon2));
  RooFormulaVar sigma2b("sigma2b","sigmacommon2*s2a*s2b",
			  RooArgList(*s2a,*s2b,*sigmacommon2));











  RooArgList smear(*sigmacommon1,sigma1a,sigma1b,*f1a,*f1b,
  		   *sigmacommon2,sigma2a,sigma2b,*f2a,"Smearing parameters");


  smear.add(*f2b);

  RooDLineShape2D fcn("DLineshape","DLineShape",1,mbc1,mbc2,EbeamFix,
		      mres,*gamma,*r,
		      *sigmaE,
		      smear,
		      *md,res);



  //RooRealVar xi("xi","xi",-20.0,-100.0,-1.0);
  RooRealVar xi("xi","xi",-21.0);
  //RooRealVar c("c","c",0.49);


  RooArgusBG Argus1("argus1","argus1",mbc1,EbeamFix,xi);

  RooArgusBG Argus2("argus2","argus2",mbc2,EbeamFix,xi);


  std::cout << "Will construct first lineshape"<<std::endl;

  RooDLineShape Dfcn1("Dfcn1","Dfcn1",1,mbc1,EbeamFix,mres,*gamma,*r,*sigmaE,
                      *sigmacommon1,*md,res);

  std::cout << "Will construct second lineshape"<<std::endl;

  RooDLineShape Dfcn2("Dfcn2","Dfcn2",1,mbc2,EbeamFix,mres,*gamma,*r,*sigmaE,
                      *sigmacommon2,*md,res);

  std::cout << "Done with lineshape"<<std::endl;

  RooProdPdf Bkgd1("Bkgd1","Bkgd1",Argus1,Dfcn2);
  RooProdPdf Bkgd2("Bkgd2","Bkgd2",Argus2,Dfcn1);

  RooProdPdf BkgdFlat("BkgdFlat","BkgdFlat",Argus1,Argus2);

  
  //RooRealVar pdiag("pdiag","pdiag",0.5,0.5,2.0);

  double pdiagd=0.74;
  if (opt.Contains("p")) pdiagd=0.5;

  RooRealVar pdiag("pdiag","pdiag",pdiagd);



  //RooRealVar xidiag("xidiag","xidiag",-10.0,-100.0,0.0);


  double xidiagd=-21.0;
  if (opt.Contains("p")) xidiagd=-15.0;

  RooRealVar xidiag("xidiag","xidiag",xidiagd);


  //RooRealVar sigmadiag("sigmadiag","sigmadiag",0.002,0.0001,0.01);
  RooRealVar sigmadiag("sigmadiag","sigmadiag",0.00083);
  //RooRealVar sigmadiag("sigmadiag","sigmadiag",0.0005);
  //RooRealVar alphadiag("alphadiag","alphadiag",0.0,-1.0,10000.0);

  double alphadiagd=36.0;

  if (opt.Contains("a")) alphadiagd=0.0;

  RooRealVar alphadiag("alphadiag","alphadiag",alphadiagd);
  

  

  RooDiag Bkgd3("Bkgd3","Bkgd3",mbc1,mbc2,sigmadiag,alphadiag,
		Ebeam,xidiag,pdiag);



  dataset->Print();

  RooRealVar N("N","N", setN, 0.0,2000000.0);

  if (setNbkgd1 == 0) {
    RooRealVar Nbkgd1("Nbkgd1","Nbkgd1",0.0);
  }
  else{ 
    RooRealVar Nbkgd1("Nbkgd1","Nbkgd1",1.0,0.0,2000000.0);
  }

  if (setNbkgd2 == 0) {
    RooRealVar Nbkgd2("Nbkgd2","Nbkgd2",0.0);
  }
  else{ 
    RooRealVar Nbkgd2("Nbkgd2","Nbkgd2",1.0,0.0,2000000.0);
  }

  if (setNbkgd3 == 0) {
    RooRealVar Nbkgd3("Nbkgd3","Nbkgd3",0.0);
  }
  else{ 
    RooRealVar Nbkgd3("Nbkgd3","Nbkgd3",1.0,0.0,2000000.0);
  }

  if (setNbkgdFlat == 0) {
    RooRealVar NbkgdFlat("NbkgdFlat","NbkgdFlat",0.0);
  }
  else{ 
    RooRealVar NbkgdFlat("NbkgdFlat","NbkgdFlat",1.0,0.0,2000000.0);
  }


  RooArgList shapes;
  RooArgList yields;

  shapes.add(fcn);
  yields.add(N);

  shapes.add(BkgdFlat);
  yields.add(NbkgdFlat);

  shapes.add(Bkgd1);
  yields.add(Nbkgd1);

  shapes.add(Bkgd2);
  yields.add(Nbkgd2);

  shapes.add(Bkgd3);
  yields.add(Nbkgd3);

  RooAddPdf totalPdf("totalPdf","totalPdf",
		     shapes,yields);

  cout << "Will fit" << endl;


  totalPdf.fitTo(*dataset,"ermh");

  cout << "Done with fit" << endl;

  cout << "Signal Yield "<<N.getVal()<<" +- "<<N.getError()<<endl;

  if (txtfile != ''){
  

  FILE* table = fopen(txtfile.Data(), "w+");

  fprintf(table, "Name\t|| Value\t|| Error\n");
  fprintf(table, "N\t| %.10f\t| %.10f\n", N.getVal(), N.getError());
  fprintf(table, "Nbkgd1\t| %.10f\t| %.10f\n", Nbkgd1.getVal(), Nbkgd1.getError());
  fprintf(table, "Nbkgd2\t| %.10f\t| %.10f\n", Nbkgd2.getVal(), Nbkgd2.getError());
  fprintf(table, "Nbkgd3\t| %.10f\t| %.10f\n", Nbkgd3.getVal(), Nbkgd3.getError());
  fprintf(table, "NbkgdFlat\t| %.10f\t| %.10f\n", NbkgdFlat.getVal(), NbkgdFlat.getError());
  if (opt.Contains("f")){
  fprintf(table, "f1a\t| %.10f\t| %.10f\n", f1a.getVal(), f1a.getError());
  fprintf(table, "f1b\t| %.10f\t| %.10f\n", f1b.getVal(), f1b.getError());
  fprintf(table, "s1a\t| %.10f\t| %.10f\n", s1a.getVal(), s1a.getError());
  fprintf(table, "s1b\t| %.10f\t| %.10f\n", s1b.getVal(), s1b.getError());
  fprintf(table, "sigmacommon1\t| %.10f\t| %.10f\n", sigmacommon1.getVal(), sigmacommon1.getError());
  }
  if (opt.Contains('m')) {
  fprintf(table, "md\t| %.10f\t| %.10f\n", md.getVal(), md.getError());
  }
  if (opt.Contains('s')) {
  fprintf(table, "sigmaE\t| %.10f\t| %.10f\n", sigmaE.getVal(), sigmaE.getError());
  }
  fclose(table);





/*  ofstream table(txtfile);
  table.precision(10);

  table << "Name"     <<"\t|| "<< "Value"  << "\t|| "   << " Error"   << endl;
  table << "N"        <<"\t|  "<< N.getVal() << "\t|  " << N.getError()<< endl;
  table << "Nbkgd1"   <<"\t|  "<< Nbkgd1.getVal()<< "\t|  " << Nbkgd1.getError()<< endl;
  table << "Nbkgd2"   <<"\t|  "<< Nbkgd2.getVal()<< "\t|  " << Nbkgd2.getError()<< endl;
  table << "Nbkgd3"   <<"\t|  "<< Nbkgd3.getVal()<< "\t|  " << Nbkgd3.getError()<< endl;
  table << "NbkgdFlat"<<"\t|  "<< NbkgdFlat.getVal()<< "\t|  " << NbkgdFlat.getError()<< endl;
  
  table.close();
*/

  cout << "Fit done." << endl;
  }
 

  //canvas_1->SetLogy();
  //canvas_2->SetLogy();


  canvas->Divide(3,1);

  canvas->cd(1);

  //gPad->SetLogy();

  RooPlot* mbcFrame=mbc1.frame(60);

  mbcFrame->SetTitle(title1);

  dataset->plotOn(mbcFrame);
  mbcFrame->Draw();

  //totalPdf.paramOn(mbcFrame,dataset,"Fit parameters",2,"NELU",0.45);
  //mbcFrame->Draw();

  dataset->plotOn(mbcFrame);
  mbcFrame->Draw();


  //totalPdf.plotOn(mbcFrame,ProjWData(Ebeam,*dataset),Components(RooArgSet(BkgdFlat,Bkgd1,Bkgd2,Bkgd3)),LineColor(kBlue));
  totalPdf.plotOn(mbcFrame,Components(RooArgSet(BkgdFlat,Bkgd1,Bkgd2,Bkgd3)),LineColor(kBlue));
  mbcFrame->Draw();



  //totalPdf.plotOn(mbcFrame,ProjWData(Ebeam,*dataset),LineColor(kRed));
  totalPdf.plotOn(mbcFrame,LineColor(kRed));
  
  mbcFrame->SetMinimum(0.5);
  gPad->SetLogy();
  
  mbcFrame->Draw();


  canvas->cd(2);

  //gPad->SetLogy();

  RooPlot* mbcFrame2=mbc2.frame(60);

  mbcFrame2->SetTitle(title2);

  dataset->plotOn(mbcFrame2);
  mbcFrame2->Draw();


  dataset->plotOn(mbcFrame2);
  mbcFrame2->Draw();


  //totalPdf.plotOn(mbcFrame2,ProjWData(Ebeam,*dataset),Components(RooArgSet(BkgdFlat,Bkgd1,Bkgd2,Bkgd3)),LineColor(kBlue));
  totalPdf.plotOn(mbcFrame2,Components(RooArgSet(BkgdFlat,Bkgd1,Bkgd2,Bkgd3)),LineColor(kBlue));
  mbcFrame2->Draw();


  //totalPdf.plotOn(mbcFrame2,ProjWData(Ebeam,*dataset),LineColor(kRed));
  totalPdf.plotOn(mbcFrame2,LineColor(kRed));

  mbcFrame2->SetMinimum(0.5);
  gPad->SetLogy();

  mbcFrame2->Draw();

  canvas->cd(3);


  RooPlot* aplot=new RooPlot();

  totalPdf.paramOn(aplot,dataset," ",2,"NELU",0.1,0.9,0.9);
  
  aplot->SetTitle("Fit Parameters");


  aplot->GetXaxis()->SetLabelSize(0);
  aplot->GetXaxis()->SetTickLength(0);
  aplot->GetXaxis()->SetTitle("");
  aplot->GetXaxis()->CenterTitle();
  //aplot->GetYaxis()->SetAxisColor(0);
  aplot->GetYaxis()->SetLimits(0, 10);
  aplot->GetYaxis()->SetLabelSize(0);
  aplot->GetYaxis()->SetTitleSize(0.03);
  aplot->GetYaxis()->SetTickLength(0);
  //

  aplot->getAttText()->SetTextSize(0.06);




  aplot->Draw();

  canvas->Print(epsfile);
    
  TString  cxxfile ;
  cxxfile = epsfile ;
  cxxfile.Replace(epsfile.Sizeof()-4, 3, "C");
  canvas->SaveAs(cxxfile);

  TString  rootfile ;
  rootfile = epsfile ;
  rootfile.Replace(epsfile.Sizeof()-4, 3, "root");
  canvas->SaveAs(rootfile);

}
