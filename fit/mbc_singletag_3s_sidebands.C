#include <iostream>

using namespace RooFit;

void mbc_singletag_3s_sidebands(TString title1, TString title2,
				TString file, TString epsfile, TString txtfile, 
				//		      TString sbfile,
				int mc, int num_fcn,
				double sp1, double sp2, double sp3,
				double sf2, double sf3, int d, TString opts){
  
  // sp1 = sigma of signal
  // sp2 = ratio of sigmas betwwen sigma2 sigma 1
  // sp3 = ratio of sigmas betwwen sigma3 sigma 2
  // sf2, sf3, - fractions
  // xi_side - slope of argus
  // p_side - power of argus
  // data mc = 0  
  // mc   mc = 1  

  RooRealVar mbc("mbc","mbc",1.83,1.89,"GeV");
  RooRealVar Ebeam("Ebeam","Ebeam",1.8815,1.892,"GeV");

  RooRealVar flavor("flavor","flavor",-2.0,2.0,"Type");

  RooCategory dflav("dflav","D0 flavor");
  dflav.defineType("dflav",1);
  dflav.defineType("dbarflav",-1);
  // data res = 0
  // mc   res = 1  

  RooRealVar res("datares","datares",mc);

  RooRealVar mres("mres","mres",3.77);
  RooRealVar *gamma=0;
  if (mc) {
    gamma=new RooRealVar("gamma","gamma",0.0236);
  }
  else {
    //gamma=new RooRealVar("gamma","gamma",0.030,0.001,0.060);
    gamma=new RooRealVar("gamma","gamma",0.0306);
  }

  RooRealVar *r=0;

  r=new RooRealVar("r","r",15.0);

  RooRealVar sigmaE("sigmaE","sigmaE",0.0021);

  RooDataSet* dataset = RooDataSet::read(file,RooArgSet(mbc,Ebeam,dflav));

  //mbc.setFitRange(1.83,1.89);
  //mbc.setFitBins(60);
  //Ebeam.setFitRange(1.8815,1.892);
  //Ebeam.setFitBins(10);
  RooDataSet* bdataset = RooDataSet::read(sbfile, RooArgSet(mbc,Ebeam,dflav));
  RooDataHist* bdatahist1 = bdataset->binnedClone()->reduce(RooArgSet(mbc), "dflav==dflav::dflav");
  bdatahist1->Print("v");
  RooHistPdf bhistpdf1("bhistpdf1", "bhistpdf1",
		      RooArgSet(mbc), *bdatahist1);
  RooDataHist* bdatahist2 = bdataset->binnedClone()->reduce(RooArgSet(mbc), "dflav==dflav::dbarflav");
  RooHistPdf bhistpdf2("bhistpdf2", "bhistpdf2",
		      RooArgSet(mbc), *bdatahist2);


  RooRealVar sigmap("sigmap","sigmap",0.0055,0.004,0.011); 

  RooRealVar* sigmap1;
  if (opts.Contains("w")) {
    sigmap1 = new RooRealVar("sigmap1","sigmap1",sp1);
  } else {
    sigmap1 = new RooRealVar("sigmap1","sigmap1",0.0045,0.002,0.040); 
  }

  RooRealVar scalep2("scalep2","scalep2",2.00,1.00,4.00);
  //RooRealVar scalep2("scalep2","scalep2",sp2);
  RooRealVar scalep3("scalep3","scalep3",2.00,1.00,4.00);
  //RooRealVar scalep3("scalep3","scalep3",sp3);
  if (! opts.Contains("g")) {
    scalep2.setVal(sp2); scalep2.setConstant(1);
    scalep3.setVal(sp2); scalep3.setConstant(1);
  }    
 
  RooFormulaVar sigmap2("sigmap2","sigma2","sigmap1*scalep2",
                       RooArgSet(*sigmap1,scalep2));

  RooFormulaVar sigmap3("sigmap3","sigma3","sigmap1*scalep2*scalep3",
                        RooArgSet(*sigmap1,scalep2,scalep3));
  

  RooRealVar* md;
  //RooRealVar md("md","md",1.865,1.860,1.875);
  if (opts.Contains("f")) {
    md = new RooRealVar("md","md",1.869035);
  } else {
    md = new RooRealVar("md","md",1.869,1.863,1.875);
  }
  if (opts.Contains("m")) {
    delete md;
    md = new RooRealVar("md", "md", 1.865368);
  }


  RooDLineShape fcn1("DLineshape1","DLineShape1",4,mbc,Ebeam,
		    mres,*gamma,*r,sigmaE,sigmap,*md,res);

  RooDLineShape fcn1_1("DLineshape1_1","DLineShape1_1",4,mbc,Ebeam,
		    mres,*gamma,*r,sigmaE,*sigmap1,*md,res);
  RooDLineShape fcn1_2("DLineshape1_2","DLineShape1_2",4,mbc,Ebeam,
		    mres,*gamma,*r,sigmaE,sigmap2,*md,res);
  RooDLineShape fcn1_3("DLineshape1_3","DLineShape1_3",4,mbc,Ebeam,
		    mres,*gamma,*r,sigmaE,sigmap3,*md,res);
  
  RooDLineShape fcn2("DLineshape2","DLineShape2",4,mbc,Ebeam,
		    mres,*gamma,*r,sigmaE,sigmap,*md,res);

  RooDLineShape fcn2_1("DLineshape2_1","DLineShape2_1",4,mbc,Ebeam,
		    mres,*gamma,*r,sigmaE,*sigmap1,*md,res);
  RooDLineShape fcn2_2("DLineshape2_2","DLineShape2_2",4,mbc,Ebeam,
		    mres,*gamma,*r,sigmaE,sigmap2,*md,res);
  RooDLineShape fcn2_3("DLineshape2_3","DLineShape2_3",4,mbc,Ebeam,
		    mres,*gamma,*r,sigmaE,sigmap3,*md,res);

  //RooRealVar xi("xi","xi",-30.814);
  RooRealVar xi1("xi1","xi1",-20.0,-100.0,-1.0);
  RooRealVar xi2("xi2","xi2",-20.0,-100.0,-1.0);
 
  RooRealVar Eb("Eb","Eb",1.887);

/*   RooRealVar *p=0; */
/*   if (p_side != 0.0) { */
/*     p = new RooRealVar("p","p",p_side);  */
/*     //p = new RooRealVar("p","p",0.5); */
/*   } */
/*   else { */
/*     if (opts.Contains("f")) { */
/*       p = new RooRealVar("p","p",0.5); */
/*     } else { */
/*       p = new RooRealVar("p","p",0.5,0.1,1.5); */
/*     } */
/*   } */

/*   RooRealVar *xi=0; */
/*   if (xi_side != 0.0) { */
/*     xi = new RooRealVar("xi","xi",xi_side); */
/*   } */
/*   else { */
/*     xi= new RooRealVar("xi","xi",-20.0,-100.0,-1.0); */
/*     //xi= new RooRealVar("xi","xi",-9.05); */
/*   } */


/*   RooArgusBG Bkgd1("argus1","argus1",mbc,Ebeam,*xi,*p); */
/*   RooArgusBG Bkgd2("argus2","argus2",mbc,Ebeam,*xi,*p); */

  dataset->Print();

  RooRealVar N1("N1","N1",80000.0,0.0,2000000.0);
  RooRealVar N2("N2","N2",80000.0,0.0,2000000.0);


  RooRealVar Nbkgd1("Nbkgd1","Nbkgd1",4000.0,0.0,2000000.0);
  RooRealVar Nbkgd2("Nbkgd2","Nbkgd2",4000.0,0.0,2000000.0);
 

  RooRealVar f2("f2","f2",sf2);
  RooRealVar f3("f3","f3",sf3);
  RooFormulaVar f1("f1","f1","1.0-f2-f3",RooArgSet(f2,f3));

  RooAddPdf signal1_2("signal1_2","signal1_2",
		      RooArgList(fcn1_1,fcn1_2),f1);
  RooAddPdf signal2_2("signal2_2","signal2_2",
		      RooArgList(fcn2_1,fcn2_2),f1);

  RooAddPdf signal1_3("signal1_3","signal1_3",
                      RooArgList(fcn1_1,fcn1_2,fcn1_3),RooArgList(f1,f2));
  RooAddPdf signal2_3("signal2_3","signal2_3",
                      RooArgList(fcn2_1,fcn2_2,fcn2_3),RooArgList(f1,f2));

  RooArgList shapes1;
  RooArgList yields1;
 
  RooArgList shapes2;
  RooArgList yields2;
  if (num_fcn != 0)
    {
      if (num_fcn == 1)
	{
	  shapes1.add(fcn1);
	  yields1.add(N1);
	  shapes2.add(fcn2);
	  yields2.add(N2);
	}

      if ( num_fcn == 2 )
	{
	  shapes1.add(signal1_2);
	  yields1.add(N1);
	  shapes2.add(signal2_2);
	  yields2.add(N2);
	}

      if ( num_fcn == 3 )
	{
	  shapes1.add(signal1_3);
	  yields1.add(N1);
	  shapes2.add(signal2_3);
	  yields2.add(N2);
	}
    }

  shapes1.add(bhistpdf1);
  yields1.add(Nbkgd1);

  shapes2.add(bhistpdf2);
  yields2.add(Nbkgd2);

  RooAddPdf totalPdf1("totalPdf1","totalPdf1",
		     shapes1,yields1);
  RooAddPdf totalPdf2("totalPdf2","totalPdf2",
		     shapes2,yields2);
 
  RooSimultaneous totalPdf("totalPdf","totalPdf",dflav);

  totalPdf.addPdf(totalPdf1,"dflav");
  totalPdf.addPdf(totalPdf2,"dbarflav");
  totalPdf.fitTo(*dataset,"ermh4");

  if (opts.Contains("p")) {
    TCanvas *canvas= new TCanvas("canvas","mbc",900,300);

    canvas->Divide(3,1);
    canvas_1->SetLogy();
    canvas_2->SetLogy();

    //totalPdf.fitTo(*dataset,"ermh");
    //totalPdf.fitTo(bdataset,"ermh");

    Ebeam.setBins(900);
    
    RooDataHist ebeamdata("ebeamdata", "ebeamdata", 
			  RooArgSet(Ebeam,dflav), *dataset);

    canvas->cd(1);
    RooPlot* mbcFrame=mbc.frame();
    RooPlot* mbcFrame=mbc.frame(60);
    mbcFrame->Draw();
    
    dataset->plotOn(mbcFrame,Cut("dflav==dflav::dflav"));
    mbcFrame->getAttMarker()->SetMarkerSize(0.6);
    mbcFrame->Draw();
    //    canvas->Update();

    //RooPlot* paramWin1 = totalPdf1.paramOn(mbcFrame,dataset,
    //                                    "Fit parameters",2,"NELU",0.65);
    //paramWin1->getAttText()->SetTextSize(0.03);
    //mbcFrame->Draw();
    
    dflav="dflav";
    if (num_fcn != 0) {
      if (!opts.Contains("d")) {
	totalPdf.plotOn(mbcFrame,LineColor(kRed),LineWidth(0.6),
			Slice(dflav),ProjWData(RooArgSet(Ebeam,dflav),ebeamdata));
      } else {
	totalPdf.plotOn(mbcFrame,LineColor(kRed),LineWidth(0.6),
			Slice(dflav),ProjWData(*dataset));
      }
      mbcFrame->Draw();
  
 
      if (num_fcn == 2) {
	if (!opts.Contains("d")) {
	  totalPdf.plotOn(mbcFrame,Components(RooArgSet(bhistpdf1,fcn1_2)),
			  Slice(dflav),LineColor(kGreen),LineWidth(0.6),
			  ProjWData(RooArgSet(Ebeam,dflav),ebeamdata));
	} else {
	  totalPdf.plotOn(mbcFrame,Components(RooArgSet(bhistpdf1,fcn1_2)),
			  Slice(dflav),LineColor(kGreen),LineWidth(0.6),
			  ProjWData(*dataset));
	}
	
	mbcFrame->Draw();
      }

      if (num_fcn == 3) {
	if (!opts.Contains("d")) {
	  totalPdf.plotOn(mbcFrame,Components(RooArgSet(bhistpdf1,fcn1_3,fcn1_2)),
			  Slice(dflav),LineColor(kGreen),LineWidth(0.6),
			  ProjWData(RooArgSet(Ebeam,dflav),ebeamdata));
	  totalPdf.plotOn(mbcFrame,Components(RooArgSet(bhistpdf1,fcn1_3)),
			  Slice(dflav),LineColor(kMagenta),LineWidth(0.6),
			  ProjWData(RooArgSet(Ebeam,dflav),ebeamdata));
	} else {
	  totalPdf.plotOn(mbcFrame,Components(RooArgSet(bhistpdf1,fcn1_3,fcn1_2)),
			  Slice(dflav),LineColor(kGreen),LineWidth(0.6),
			  ProjWData(*dataset));
	  totalPdf.plotOn(mbcFrame,Components(RooArgSet(bhistpdf1,fcn1_3)),
			  Slice(dflav),LineColor(kMagenta),LineWidth(0.6),
			  ProjWData(*dataset));
	}

	mbcFrame->Draw();
      }
   
    } 
    //    canvas->Update();
    if (!opts.Contains("d")) {
      totalPdf.plotOn(mbcFrame,Components(RooArgSet(bhistpdf1)),
		      Slice(dflav),LineColor(kBlue),LineWidth(0.6),
		      ProjWData(RooArgSet(Ebeam,dflav),ebeamdata));
    } else {
      totalPdf.plotOn(mbcFrame,Components(RooArgSet(bhistpdf1)),
		      Slice(dflav),LineColor(kBlue),LineWidth(0.6),
		      ProjWData(*dataset));
    }
    
    mbcFrame->Draw();
    
    mbcFrame->SetTitle(title1);
    mbcFrame->Draw();
    
    canvas->cd(2);
    RooPlot* mbcFrame=mbc.frame();
    RooPlot* mbcFrame=mbc.frame(60);
    mbcFrame->Draw();
    
    dataset->plotOn(mbcFrame,Cut("dflav==dflav::dbarflav"));
    mbcFrame->getAttMarker()->SetMarkerSize(0.6);
    mbcFrame->Draw();
    
    //RooPlot* paramWin2 = totalPdf2.paramOn(mbcFrame,dataset,
    //				  "Fit parameters",2,"NELU",0.65);
    //paramWin2->getAttText()->SetTextSize(0.03);
    //mbcFrame->Draw();
    
    dflav="dbarflav";
    if (num_fcn != 0) {
      if (!opts.Contains("d")) {
	totalPdf.plotOn(mbcFrame,LineColor(kRed),LineWidth(0.6),
			Slice(dflav),ProjWData(RooArgSet(Ebeam,dflav),ebeamdata));
      } else {
	totalPdf.plotOn(mbcFrame,LineColor(kRed),LineWidth(0.6),
			Slice(dflav),ProjWData(*dataset));
      }
      mbcFrame->Draw();
      
      if (num_fcn == 2) {
	if (!opts.Contains("d")) {
	  totalPdf.plotOn(mbcFrame,Components(RooArgSet(bhistpdf2,fcn2_2)),
			  Slice(dflav),LineColor(kGreen),LineWidth(0.6),
			  ProjWData(RooArgSet(Ebeam,dflav),ebeamdata));
	} else {
	  totalPdf.plotOn(mbcFrame,Components(RooArgSet(bhistpdf2,fcn2_2)),
			  Slice(dflav),LineColor(kGreen),LineWidth(0.6),
			  ProjWData(*dataset));
	}
	
	mbcFrame->Draw();
      }

      if (num_fcn == 3) {
	if (!opts.Contains("d")) {
	  totalPdf.plotOn(mbcFrame,Components(RooArgSet(bhistpdf2,fcn2_3,fcn2_2)),
			  Slice(dflav),LineColor(kGreen),LineWidth(0.6),
			  ProjWData(RooArgSet(Ebeam,dflav),ebeamdata));
	  
	  totalPdf.plotOn(mbcFrame,Components(RooArgSet(bhistpdf2,fcn2_3)),
			  Slice(dflav),LineColor(kMagenta),LineWidth(0.6),
			  ProjWData(RooArgSet(Ebeam,dflav),ebeamdata));
	} else {
	  totalPdf.plotOn(mbcFrame,Components(RooArgSet(bhistpdf2,fcn2_3,fcn2_2)),
			  Slice(dflav),LineColor(kGreen),LineWidth(0.6),
			  ProjWData(*dataset));
	  
	  totalPdf.plotOn(mbcFrame,Components(RooArgSet(bhistpdf2,fcn2_3)),
			  Slice(dflav),LineColor(kMagenta),LineWidth(0.6),
			  ProjWData(*dataset));
	}
	
	mbcFrame->Draw();
      }
      
    }
    
    if (!opts.Contains("d")) {
      totalPdf.plotOn(mbcFrame,Components(RooArgSet(bhistpdf2)),
		      Slice(dflav),LineColor(kBlue),LineWidth(0.6),
		      ProjWData(RooArgSet(Ebeam,dflav),ebeamdata));
    } else {
      totalPdf.plotOn(mbcFrame,Components(RooArgSet(bhistpdf2)),
		      Slice(dflav),LineColor(kBlue),LineWidth(0.6),
		      ProjWData(*dataset));
    }
    mbcFrame->Draw();
    
    mbcFrame->SetTitle(title2);
    mbcFrame->Draw();
    
    
    if (d > 0) {
      canvas->cd(3);
      RooPlot* mbcFrame=mbc.frame();
      
      //dataset->plotOn(mbcFrame,Cut("dflav==dflav::dflav"));
      //mbcFrame->getAttMarker()->SetMarkerSize(0.6);
      //mbcFrame->Draw();
      
      RooPlot* paramWin1 = totalPdf.paramOn(mbcFrame,dataset,
					    "Fit parameters",2,"NELU",0.65);
      paramWin1->getAttText()->SetTextSize(0.03);
      mbcFrame->Draw();
      dflav="dflav";
      
      /* 
	 if (num_fcn != 0)
	 {
	 if (opts.Contains("f")) {
	 totalPdf.plotOn(mbcFrame,LineColor(kRed),LineWidth(0.6),
	 Slice(dflav),ProjWData(RooArgSet(dflav),ebeamdata));
	 } else {
	 totalPdf.plotOn(mbcFrame,LineColor(kRed),LineWidth(0.6),
	 Slice(dflav),ProjWData(RooArgSet(Ebeam,dflav),ebeamdata));
	 }
	 mbcFrame->Draw();
	 
	 if (num_fcn == 2)
	 {
	 if (opts.Contains("f")) {
	 totalPdf.plotOn(mbcFrame,Components(RooArgSet(Bkgd1,fcn1_2)),
	 Slice(dflav),LineColor(kGreen),LineWidth(0.6),
	 ProjWData(RooArgSet(dflav),ebeamdata));
	 } else {
	 totalPdf.plotOn(mbcFrame,Components(RooArgSet(Bkgd1,fcn1_2)),
	 Slice(dflav),LineColor(kGreen),LineWidth(0.6),
	 ProjWData(RooArgSet(Ebeam,dflav),ebeamdata));
	 }
	 
	 mbcFrame->Draw();
	 }
	 
	 if (num_fcn == 3)
	 {
	 if (opts.Contains("f")) {
	 totalPdf.plotOn(mbcFrame,Components(RooArgSet(Bkgd1,fcn1_3,fcn1_2)),
	 Slice(dflav),LineColor(kGreen),LineWidth(0.6),
	 ProjWData(RooArgSet(dflav),ebeamdata));
	 totalPdf.plotOn(mbcFrame,Components(RooArgSet(Bkgd1,fcn1_3)),
	 Slice(dflav),LineColor(kMagenta),LineWidth(0.6),
	 ProjWData(RooArgSet(dflav),ebeamdata));
	 } else {
	 totalPdf.plotOn(mbcFrame,Components(RooArgSet(Bkgd1,fcn1_3,fcn1_2)),
	 Slice(dflav),LineColor(kGreen),LineWidth(0.6),
	 ProjWData(RooArgSet(Ebeam,dflav),ebeamdata));
	 totalPdf.plotOn(mbcFrame,Components(RooArgSet(Bkgd1,fcn1_3)),
	 Slice(dflav),LineColor(kMagenta),LineWidth(0.6),
	 ProjWData(RooArgSet(Ebeam,dflav),ebeamdata));
	 }
	 
	 mbcFrame->Draw();
	 }
	 
	 }
	 
	 
	 //totalPdf.plotOn(mbcFrame,Components(RooArgSet(Bkgd1)),
	 //              Slice(dflav),LineColor(kBlue),LineWidth(0.6),
	 //            ProjWData(RooArgSet(Ebeam,dflav),ebeamdata));
	 if (opts.Contains("f")) {
	 totalPdf.plotOn(mbcFrame,Components(RooArgSet(Bkgd1)),
	 Slice(dflav),LineColor(kBlue),LineWidth(0.6),
	 ProjWData(RooArgSet(dflav),ebeamdata));
	 } else {
	 totalPdf.plotOn(mbcFrame,Components(RooArgSet(Bkgd1)),
	 Slice(dflav),LineColor(kBlue),LineWidth(0.6),
	 ProjWData(RooArgSet(dflav),ebeamdata));
	 }
	 
	 mbcFrame->Draw();
      */
      mbcFrame->SetTitle(title1);
      mbcFrame->Draw();
      
    }
  
    if ( d < 0 ) {
      canvas->cd(3);
      RooPlot* mbcFrame=mbc.frame();
      
      dataset->plotOn(mbcFrame,Cut("dflav==dflav::dbarflav"));
      mbcFrame->getAttMarker()->SetMarkerSize(0.6);
      mbcFrame->Draw();
      
      RooPlot* paramWin2 = totalPdf2.paramOn(mbcFrame,dataset,
					     "Fit parameters",2,"NELU",0.65);
      paramWin2->getAttText()->SetTextSize(0.03);
      mbcFrame->Draw();
      
      dflav="dbarflav";
      /* 
	 if (num_fcn != 0)
	 {
	 if (opt.Contains("f")) {
	 totalPdf.plotOn(mbcFrame,LineColor(kRed),LineWidth(0.6),
	 Slice(dflav),ProjWData(RooArgSet(dflav),ebeamdata));
	 } else {
	 totalPdf.plotOn(mbcFrame,LineColor(kRed),LineWidth(0.6),
	 Slice(dflav),ProjWData(RooArgSet(Ebeam,dflav),ebeamdata));
	 }
	 mbcFrame->Draw();
	 
	 if (num_fcn == 2)
	 {
	 if (opt.Contains("f")) {
	 totalPdf.plotOn(mbcFrame,Components(RooArgSet(Bkgd2,fcn2_2)),
	 Slice(dflav),LineColor(kGreen),LineWidth(0.6),
	 ProjWData(RooArgSet(dflav),ebeamdata));
	 } else {
	 totalPdf.plotOn(mbcFrame,Components(RooArgSet(Bkgd2,fcn2_2)),
	 Slice(dflav),LineColor(kGreen),LineWidth(0.6),
	 ProjWData(RooArgSet(Ebeam,dflav),ebeamdata));
	 }
	 mbcFrame->Draw();
	 }
	 if (num_fcn == 3)
	 {
	 if (opt.Contains("f")) {
	 totalPdf.plotOn(mbcFrame,Components(RooArgSet(Bkgd2,fcn2_3,fcn2_2)),
	 Slice(dflav),LineColor(kGreen),LineWidth(0.6),
	 ProjWData(RooArgSet(dflav),ebeamdata));
	 
	 totalPdf.plotOn(mbcFrame,Components(RooArgSet(Bkgd2,fcn2_3)),
	 Slice(dflav),LineColor(kMagenta),LineWidth(0.6),
	 ProjWData(RooArgSet(dflav),ebeamdata));
	 } else {
	 totalPdf.plotOn(mbcFrame,Components(RooArgSet(Bkgd2,fcn2_3,fcn2_2)),
	 Slice(dflav),LineColor(kGreen),LineWidth(0.6),
	 ProjWData(RooArgSet(Ebeam,dflav),ebeamdata));
	 
	 totalPdf.plotOn(mbcFrame,Components(RooArgSet(Bkgd2,fcn2_3)),
	 Slice(dflav),LineColor(kMagenta),LineWidth(0.6),
	 ProjWData(RooArgSet(Ebeam,dflav),ebeamdata));
	 }
	 
	 mbcFrame->Draw();
	 }
	 
	 }
	 
	 //totalPdf.plotOn(mbcFrame,Components(RooArgSet(Bkgd2)),
	 //              Slice(dflav),LineColor(kBlue),LineWidth(0.6),
	 //            ProjWData(RooArgSet(Ebeam,dflav),ebeamdata));
	 
	 //totalPdf.plotOn(mbcFrame,Components(RooArgSet(Bkgd2)),
	 //              Slice(dflav),LineColor(kBlue),LineWidth(0.6),
	 //            ProjWData(RooArgSet(dflav),ebeamdata));
	 
	 mbcFrame->Draw();
      */
      mbcFrame->SetTitle(title2);
      mbcFrame->Draw();
    }

    canvas->Print(epsfile);
  }
 

  // Print out
  
  Double_t yield1 = N1.getVal();
  Double_t yield1_err = N1.getError();

  Double_t back1 = Nbkgd1.getVal();
  Double_t back1_err = Nbkgd1.getError();
  
  Double_t yield2 = N2.getVal();
  Double_t yield2_err = N2.getError();

  Double_t back2 = Nbkgd2.getVal();
  Double_t back2_err = Nbkgd2.getError();


  Double_t Gamma = gamma->getVal()*1000;
  Double_t Gamma_err = gamma->getError()*1000;
  
  ofstream table(txtfile);
 
  table <<"Decay"<<" | "<< "yield for signal"<<
    " | "<< "yield for back"<< endl;
  
  table << title1<<" | "<< yield1<<"+/-"<<yield1_err <<
    " | "<< back1<<"+/-"<< back1_err <<endl;

  table << title2<<" | "<< yield2<<"+/-"<<yield2_err <<
                   " | "<< back2<<"+/-"<< back2_err <<endl;

  cout << "all done" << endl;

}



