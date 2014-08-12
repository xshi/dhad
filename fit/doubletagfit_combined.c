#include <iostream>
using namespace std;
// using namespace RooFit;

// To run in batch mode:
// root -b -q 'doubletagfit_combined.c("/home/xs32/work/CLEO/analysis/DHad/dat/evt/818ipbv7/data_Double_d0_d0bar_with_mode.evt", "/home/xs32/work/CLEO/analysis/DHad/doc/dhadprd/fig/d03_test.eps", 1, 3)' >  /home/xs32/work/CLEO/analysis/DHad/doc/dhadprd/log/d03_test.log 

// root -b -q 'doubletagfit_combined.c("/home/xs32/work/CLEO/analysis/DHad/dat/evt/818ipbv7/data_Double_dp_dm_with_mode.evt", "/home/xs32/work/CLEO/analysis/DHad/doc/dhadprd/fig/dp3_test.eps", 1, 3)' >  /home/xs32/work/CLEO/analysis/DHad/doc/dhadprd/log/dp3_test.log 


void fitpars(TString mode, double& sigma, double& fa, double& fb, double& sa, double& sb){

 if (mode=="kpi"){
   sigma=0.00394;
   fa=0.195;
   fb=0.0059;
   sa=2.33;
   sb=3.43;
  } else if (mode=="kpipi0"){
    sigma=0.00671;
    fa=0.212;
    fb=0.0260;
    sa=2.53;
    sb=3.02;
  } else if (mode=="kpipipi"){
    sigma=0.00437;
    fa=0.168;
    fb=0.0115;
    sa=2.08;
    sb=3.27;
  } else if (mode=="kpipi"){
    sigma=0.00425;
    fa=0.121;
    fb=0.0060;
    sa=2.30;
    sb=4.00;
  } else if (mode=="kpipipi0"){
    sigma=0.00603;
    fa=0.277;
    fb=0.0501;
    sa=2.18;
    sb=3.32;
  } else if (mode=="kspi"){
    sigma=0.00398;
    fa=0.158;
    fb=0.0046;
    sa=2.48;
    sb=4.00;
  } else if (mode=="kspipi0"){
    sigma=0.00722;
    fa=0.169;
    fb=0.0396;
    sa=2.20;
    sb=2.17;
  } else if (mode=="kspipipi"){
    sigma=0.00439;
    fa=0.148;
    fb=0.0161;
    sa=2.52;
    sb=4.00;
  } else if (mode=="kkpi"){
    sigma=0.00468;
    fa=0.143;
    fb=0.0092;
    sa=2.05;
    sb=3.59;
  } else {
    cout << "Unknown mode1:"<<mode1<<endl;
    assert(0);
  }


}


void doubletagfit_combined(TString file, TString epsfile, int d0, int mc=0){

  gSystem->Load("/home/xs32/work/CLEO/analysis/DHad/lib/RooFitCore/libRooFitCore_3_0.so"); 
  gSystem->Load("/home/xs32/work/CLEO/analysis/DHad/lib/RooFitModels/libRooFitModels_3_0.so");

  gROOT->SetStyle("Plain"); 
  
  using namespace RooFit;
  
  RooRealVar mbc1("mbc1","M(D1)",1.83,1.89,"GeV");
  RooRealVar mbc2("mbc2","M(D2)",1.83,1.89,"GeV");
  RooRealVar Ebeam("Ebeam","Ebeam",1.885,1.89,"GeV");

  RooRealVar *r;

  r = new RooRealVar("r","r", 12.7);

  TString names[10];
 
  int nmodes;

  double mdd=1.86912;

  if (d0==1){
    nmodes=3;
    mdd=1.86415;
    names[0]="kpi";
    names[1]="kpipi0";
    names[2]="kpipipi";
  }
  else{
    nmodes=6;

    names[0]="kkpi";
    names[1]="kpipi";
    names[2]="kpipipi0";
    names[3]="kspi";
    names[4]="kspipi0";
    names[5]="kspipipi";
  }

  cout << "Here01"<<endl;

  RooCategory dmodes("dmodes","D modes");
  for (int i=0;i<nmodes;i++){
    for (int j=0;j<nmodes;j++){
      cout << "Will define mode:"<<names[i]+"_"+names[j]<<endl;
      dmodes.defineType(names[i]+"_"+names[j],i*nmodes+j+1);
    }
  }

  cout << "Here02"<<endl;

  // RooRealVar mres("mres","mres",3.77);
  RooRealVar mres("mres","mres",3.7724);

  RooRealVar res("datares","datares",mc);
  RooRealVar *gamma;
  if (mc){
    // gamma=new RooRealVar("gamma","gamma",0.0236);
    gamma=new RooRealVar("gamma","gamma",0.0252); // mc=3 data 
  }
  else{
    //gamma=new RooRealVar("gamma","gamma",0.024,0.020,0.070);
    gamma=new RooRealVar("gamma","gamma",0.0306);
  }

  RooRealVar sigmaE("sigmaE","sigmaE",0.0021);
  //RooRealVar sigmaE("sigmaE","sigmaE",0.0008,0.0005,0.004);

  //RooRealVar md("md","md",1.865,1.860,1.875);
  RooRealVar md("md","md",mdd);


  cout << "Here1"<<endl;

  RooDataSet* dataset = RooDataSet::read(file,RooArgSet(mbc1,mbc2,Ebeam,dmodes));
  
  double nevents=dataset->numEntries();

  cout << "Number of events:"<<nevents<<endl;

  dataset->Print();


  cout << "Here2"<<endl;

  RooRealVar* sigmap[10];
  RooRealVar* sigmapa[10];
  RooRealVar* sigmapb[10];
  RooRealVar* fa[10];
  RooRealVar* fb[10];

  for (int i=0;i<nmodes;i++){

    double sigma,fad,fbd,sa,sb;

    fitpars(names[i], sigma, fad, fbd, sa, sb);    

    sigmap[i]= new RooRealVar("sigmap_"+names[i],"sigmap_"+names[i],sigma);
    sigmapa[i]= new RooRealVar("sigmapa_"+names[i],"sigmapa_"+names[i],sigma*sa);
    sigmapb[i]= new RooRealVar("sigmapb_"+names[i],"sigmapb_"+names[i],sigma*sa*sb);
    fa[i]= new RooRealVar("fa_"+names[i],"fa_"+names[i],fad);
    fb[i]= new RooRealVar("fb_"+names[i],"fb_"+names[i],fbd);
  }

  RooRealVar EbeamFix("EbeamFix","EbeamFix",1.887);

  RooGaussian* Dfcn1[10];
  RooGaussian* Dfcn2[10];
  //RooDLineShape* Dfcn1[10];
  //RooDLineShape* Dfcn2[10];

  for (int i=0;i<nmodes;i++){
    //    Dfcn1[i]=new RooDLineShape("Dfcn1_"+names[i],"Dfcn1_"+names[i],1,mbc1,EbeamFix,
    //				mres,*gamma,sigmaE,
    //				*(sigmap[i]),md,res);
    //Dfcn2[i]=new RooDLineShape("Dfcn2_"+names[i],"Dfcn2_"+names[i],1,mbc2,EbeamFix,
    //			mres,*gamma,sigmaE,
    //			*(sigmap[i]),md,res);

    Dfcn1[i]=new RooGaussian("Dfcn1_"+names[i],"Dfcn1_"+names[i],mbc1,md,
			     sigmaE);

    Dfcn2[i]=new RooGaussian("Dfcn2_"+names[i],"Dfcn2_"+names[i],mbc2,md,
			       sigmaE);
  }



  RooRealVar sigmadiag("sigmadiag","sigmadiag",0.00083);
  RooRealVar alpha("alpha","alpha",36.0);

  //RooRealVar sigmadiag("sigmadiag","sigmadiag",0.0004,0.0001,0.001);
  //RooRealVar alpha("alpha","alpha",136.0,10.0,500.0);

  RooRealVar xi("xi","xi",-21.0);
  RooRealVar p("p","p",0.74);

  //RooRealVar xi("xi","xi",-45.0,-100.0,-10.0);
  //RooRealVar p("p","p",1.1,0.5,1.9);


  RooArgusBG Argus1("argus1","argus1",mbc1,EbeamFix,xi);

  RooArgusBG Argus2("argus2","argus2",mbc2,EbeamFix,xi);



  RooArgList* smear[100];
  RooDLineShape2D* fcn[100];

  RooProdPdf* Bkgd1[100];
  RooProdPdf* Bkgd2[100];

  RooProdPdf* BkgdFlat[100];
  RooDiag* Bkgd3[100];


  RooRealVar* N[100];
  RooRealVar* Nbkgd1[100];
  RooRealVar* Nbkgd2[100];
  RooRealVar* Nbkgd3[100];
  RooRealVar* NbkgdFlat[100];

  RooAddPdf* modePdf[100];

  RooSimultaneous totalPdf("totalPdf","totalPdf",dmodes);

  RooArgList bk1,bk2,bk3,bkflat,bk;

  for (int i=0;i<nmodes;i++){
    for (int j=0;j<nmodes;j++){
      smear[i*nmodes+j]=new RooArgList(*(sigmap[i]),*(sigmapa[i]),*(sigmapb[i]),
				       *(fa[i]),*(fb[i]),
				       *(sigmap[j]),*(sigmapa[j]),*(sigmapb[j]),
				       *(fa[j]),
				       "Smearing parameters for mode "+names[i]+"_"+names[j]);
      smear[i*nmodes+j]->add(*(fb[j]));

      fcn[i*nmodes+j]=new RooDLineShape2D("DLineshape_"+names[i]+"_"+names[j],
					  "DLineShape"+names[i]+"_"+names[j],
					  1,mbc1,mbc2,EbeamFix,
					  mres,*gamma, *r, 
					  sigmaE,
					  *(smear[i*nmodes+j]),
					  md,res);





      Bkgd1[i*nmodes+j]=new RooProdPdf("Bkgd1_"+names[i]+"_"+names[j],
				       "Bkgd1_"+names[i]+"_"+names[j],
				       Argus1,*(Dfcn2[j]));
      Bkgd2[i*nmodes+j]=new RooProdPdf("Bkgd2_"+names[i]+"_"+names[j],
				       "Bkgd2_"+names[i]+"_"+names[j],
				       Argus2,*(Dfcn1[i]));
      
      BkgdFlat[i*nmodes+j]=new RooProdPdf("BkgdFlat_"+names[i]+"_"+names[j],
					  "BkgdFlat_"+names[i]+"_"+names[j],
					  Argus1,Argus2);
      
      Bkgd3[i*nmodes+j]=new RooDiag("Bkgd3_"+names[i]+"_"+names[j],
				    "Bkgd3_"+names[i]+"_"+names[j],
				    mbc1,mbc2,sigmadiag,alpha,EbeamFix,xi,p);

      N[i*nmodes+j]=new RooRealVar("N_"+names[i]+"_"+names[j],
				   "N_"+names[i]+"_"+names[j],
				   nevents/(nmodes*nmodes),0.0,nevents);
      Nbkgd1[i*nmodes+j]=new RooRealVar("Nbkgd1_"+names[i]+"_"+names[j],
					"Nbkgd1_"+names[i]+"_"+names[j],
					0.0,0.0,nevents);
      Nbkgd2[i*nmodes+j]=new RooRealVar("Nbkgd2_"+names[i]+"_"+names[j],
					"Nbkgd2_"+names[i]+"_"+names[j],
					0.0,0.0,nevents);
      Nbkgd3[i*nmodes+j]=new RooRealVar("Nbkgd3_"+names[i]+"_"+names[j],
					"Nbkgd3_"+names[i]+"_"+names[j],
					0.0,0.0,nevents);
      NbkgdFlat[i*nmodes+j]=new RooRealVar("NbkgdFlat_"+names[i]+"_"+names[j],
					   "NbkgdFlat_"+names[i]+"_"+names[j],
					   0.0,0.0,nevents);

      RooArgList shapes;
      RooArgList yields;
      
      shapes.add(*(fcn[i*nmodes+j]));
      yields.add(*(N[i*nmodes+j]));

      bkflat.add(*(BkgdFlat[i*nmodes+j]));
      bk1.add(*(Bkgd1[i*nmodes+j]));
      bk2.add(*(Bkgd2[i*nmodes+j]));
      bk3.add(*(Bkgd3[i*nmodes+j]));

      bk.add(*(BkgdFlat[i*nmodes+j]));
      bk.add(*(Bkgd1[i*nmodes+j]));
      bk.add(*(Bkgd2[i*nmodes+j]));
      bk.add(*(Bkgd3[i*nmodes+j]));


      shapes.add(*(BkgdFlat[i*nmodes+j]));
      yields.add(*(NbkgdFlat[i*nmodes+j]));
      
      shapes.add(*(Bkgd1[i*nmodes+j]));
      yields.add(*(Nbkgd1[i*nmodes+j]));

      shapes.add(*(Bkgd2[i*nmodes+j]));
      yields.add(*(Nbkgd2[i*nmodes+j]));
      
      shapes.add(*(Bkgd3[i*nmodes+j]));
      yields.add(*(Nbkgd3[i*nmodes+j]));

      modePdf[i*nmodes+j]=new RooAddPdf("modePdf_"+names[i]+"_"+names[j],
					"modePdf_"+names[i]+"_"+names[j],
					shapes,
					yields);

      totalPdf.addPdf(*(modePdf[i*nmodes+j]),names[i]+"_"+names[j]);

    }
  }





  cout << "Will fit" << endl;

  totalPdf.fitTo(*dataset,"ermh");

  cout << "Done with fit" << endl;



  TCanvas *canvas=new TCanvas("canvas","Fit",400,400);


  canvas->Divide(1,1);

  canvas->cd(1);

  //gPad->SetLogy();

  RooPlot* mbcFrame=mbc1.frame(50);

  gPad->SetTopMargin(0.02);  
  gPad->SetRightMargin(0.02);  

  gPad->SetLeftMargin(0.19);  
  gPad->SetBottomMargin(0.12);  


  TString title="D0D0B";

  if (!d0) title="D+D-";

  // mbcFrame->SetMaximum(800.0);        
  // if (!d0)   mbcFrame->SetMaximum(600.0);        


  mbcFrame->SetTitle("");

  dataset->plotOn(mbcFrame);
  mbcFrame->Draw();



  totalPdf.plotOn(mbcFrame,Components(bk),ProjWData(dmodes,*dataset),LineColor(kBlue),LineStyle(kDashed));
  //totalPdf.plotOn(mbcFrame,ProjWData(Ebeam,*dataset),Components(bk),LineColor(kBlue));
  mbcFrame->Draw();


  totalPdf.plotOn(mbcFrame,ProjWData(dmodes,*dataset),LineColor(kRed));
  //totalPdf.plotOn(mbcFrame,ProjWData(Ebeam,*dataset),LineColor(kRed));
  mbcFrame->Draw();

  if (0){
  
    canvas->cd(2);

    //gPad->SetLogy();
    
    RooPlot* mbcFrame2=mbc2.frame(50);

    mbcFrame2->SetTitle("Dbar");

    dataset->plotOn(mbcFrame2);
    mbcFrame2->Draw();
    
    totalPdf.plotOn(mbcFrame2,ProjWData(dmodes,*dataset),Components(bk),LineColor(kBlue),LineStyle(kDashed));
    //totalPdf.plotOn(mbcFrame2,ProjWData(Ebeam,*dataset),Components(bk),LineColor(kBlue));
    mbcFrame2->Draw();

    totalPdf.plotOn(mbcFrame2,ProjWData(dmodes,*dataset),LineColor(kRed));
    //totalPdf.plotOn(mbcFrame2,ProjWData(Ebeam,*dataset),LineColor(kRed));
    
    mbcFrame2->Draw();

  }

  //canvas->cd(3);

  //RooPlot* aplot=new RooPlot();

  //totalPdf.paramOn(aplot,dataset,"Fit parameters",2,"NELU",0.45);
  //aplot->Draw();


  TLatex *label2 = new TLatex();
  label2->SetTextSize(0.10);
  if (d0) {
    label2->DrawLatex(1.838,10000,"D^{0}#bar D^{0}");
  }
  else {
    label2->DrawLatex(1.838,7000,"D^{+}D^{-}");
  }
  delete label2;

  TAxis *xaxis = mbcFrame->GetXaxis();
  xaxis->SetTitle("");
  xaxis->SetLabelSize(0.05);
  xaxis->SetNdivisions(305);

  TAxis *yaxis = mbcFrame->GetYaxis();
  yaxis->SetTitle("");
  yaxis->SetLabelSize(0.05);
    
  TLatex xtitle;
  TLatex ytitle;
  //latex.SetNDC();
  //latex.SetTextFont(12);
  //latex.SetTextSize(0.10);
  xtitle.SetNDC(); 
  xtitle.SetTextFont(62);
  xtitle.SetTextSize(0.06);
  //  xtitle.SetTextSize(0.050);
  xtitle.SetTextAlign(20);
  ytitle.SetNDC(); 
  ytitle.SetTextFont(62);
  ytitle.SetTextSize(0.06);
  // ytitle.SetTextSize(0.050);
  ytitle.SetTextAngle(90);
  ytitle.SetTextAlign(20);
  TGaxis::SetMaxDigits(5);

  TString mESName = "#font[32]{M}";
  Int_t mESBins = 50;   

  TString mESBinWidth = "0.0012";
  TString mESUnits = "GeV/#font[32]{c^{#font[22]{2}}}"; 

  // TString mESBinWidth = "1.2";
  // TString mESUnits = "MeV/#font[32]{c^{#font[22]{2}}}"; 

  xtitle.DrawLatex(0.55, 0.010, mESName+" ("+mESUnits+" )");
  ytitle.DrawLatex(0.05, 0.55, "Events / ("+mESBinWidth+" "+mESUnits+")");


  canvas->Print(epsfile);

}

