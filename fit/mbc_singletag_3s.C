#include <iostream>
#include <stdio.h>

using namespace RooFit;

void mbc_singletag_3s(TString title1, 
		      TString title2,
		      TString file, 
		      TString epsfile,
		      TString txtfile,  
		      int mc, 
		      int num_fcn,
		      double xi_side,
		      double p_side,
		      double sp1, 
		      double sp2, 
		      double sp3,
		      double sfa, 
		      double sf3, 
		      int d,
		      TString opts,
		      double setGamma=0.0275, 
		      int floatwidth=0, 
		      double setR=15.0,
		      double setMres = 3.774,
		      double setN1   = 800000.0,
		      double setN2   = 800000.0,
		      double setNbkgd1  = 4000.0,
		      double setNbkgd2  = 4000.0,
		      double setmd   = 1.869,
		      double setp    = 0.5, 
		      double setsigmap1 = 0.0045,
		      double setxi   = -20.0, 
		      double min = 0.5,
		      TString options = "", 
		      TString MINUIT = "ermh4"){


  // sp1 = sigma of signal
  // sp2 = ratio of sigmas betwwen sigma2 sigma 1
  // sp3 = ratio of sigmas betwwen sigma3 sigma 2
  // sfa, sf3, - fractions
  // xi_side - slope of argus
  // p_side - power of argus

  // opts meanings:

  // d - RooArgSet(Ebeam,dflav),ebeamdata
  // f - md fix 1.869035, also fix p = 0.5
  // !g -       scalep2.setVal(sp2); scalep2.setConstant(1);
  //            scalep3.setVal(sp2); scalep3.setConstant(1);
  // m - md fix 1.865368
  // p - plot 
  // w - sigmap1 float
  // Fa  - float fa (sfa)


   char tempString[500];
   Double_t  chisq1;
   Double_t  chisq2;

   RooRealVar mbc("mbc","mbc",1.83,1.89,"GeV");
   RooRealVar Ebeam("Ebeam","Ebeam",1.8815,1.892,"GeV");

   RooRealVar flavor("flavor","flavor",-2.0,2.0,"Type");

   RooCategory dflav("dflav","D0 flavor");
   dflav.defineType("dflav",1);
   dflav.defineType("dbarflav",-1);
   // data res = 0
   // mc   res = 1  
   
   RooRealVar res("datares","datares",mc);
   RooRealVar mres("mres","mres",setMres);
   RooRealVar *gamma=0;
   
   // mc = -1 "Broken" MC
   // mc = 0  BW shape  
   // mc = 1  MARK III (data)
  
   // mc = 3  BES 2007 paper (BES2006 lineshape hepex/0612056) 
   //         RooFitModels/RooDEnergyImp.cc

   if (mc != -1) {
      if (floatwidth == 0){
	 gamma=new RooRealVar("gamma","gamma",setGamma);
      }
      else{
	 gamma=new RooRealVar("gamma","gamma", setGamma,0.001,0.060);
      }
   }
   else {
      gamma=new RooRealVar("gamma","gamma",0.0236);
   }
   
   RooRealVar *r=0;
   
   r=new RooRealVar("r","r", setR);
   
   RooRealVar sigmaE("sigmaE","sigmaE",0.0021);
   
   RooDataSet* dataset = RooDataSet::read(file,RooArgSet(mbc,Ebeam,dflav));
   
   RooRealVar sigmap("sigmap","sigmap", 0.0055, 0.004,0.011); 
   
   RooRealVar* sigmap1;
   

//    if (opts.Contains("w")) {
//       sigmap1 = new RooRealVar("sigmap1","sigmap1",sp1);
//    } else {
//       if (opts.Contains("f")) {
//       sigmap1 = new RooRealVar("sigmap1","sigmap1",0.0045); 
//       }
//       else{
//       sigmap1 = new RooRealVar("sigmap1","sigmap1", setsigmap1,0.002,0.040); 
//       }
//    }

   if (options.Contains("fix_sigmap1")) {
      sigmap1 = new RooRealVar("sigmap1","sigmap1", setsigmap1);
   } else {
     sigmap1 = new RooRealVar("sigmap1","sigmap1", setsigmap1,0.002,0.040); 
   }

   RooRealVar scalep2("scalep2","scalep2",2.00,1.500,5.500);
   RooRealVar scalep3("scalep3","scalep3",5.00,3.00,10.000);
   if (! opts.Contains("g")) {
      scalep2.setVal(sp2); scalep2.setConstant(1);
      scalep3.setVal(sp3); scalep3.setConstant(1);
   }    
   
   RooFormulaVar sigmap2("sigmap2","sigma2","sigmap1*scalep2",
			 RooArgSet(*sigmap1,scalep2));
   
   RooFormulaVar sigmap3("sigmap3","sigma3","sigmap1*scalep2*scalep3",
			 RooArgSet(*sigmap1,scalep2,scalep3));
   
   
   RooRealVar* md;
//    if (opts.Contains("f")) {
//       md = new RooRealVar("md","md",setmd);
//    } else {
//       md = new RooRealVar("md","md", setmd,1.863,1.875);
//    }
//    if (opts.Contains("m")) {
//       delete md;
//       md = new RooRealVar("md", "md", setmd);
//    }


   if (options.Contains("fix_md")) {
      md = new RooRealVar("md","md", setmd);
   } else {
      md = new RooRealVar("md","md", setmd,1.863,1.875);
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
   
   RooRealVar Eb("Eb","Eb",1.887);
   
   RooRealVar *p=0;
//    if (p_side != 0.0) {
//       p = new RooRealVar("p","p",p_side); 
//    }
//    else {
//       if (opts.Contains("f")) {
// 	 p = new RooRealVar("p","p",0.5);
//       } else {
// 	 p = new RooRealVar("p","p", setp,0.1,1.5);
//       }
//    }

   if (p_side != 0.0) {
      p = new RooRealVar("p","p",p_side); 
   }
   else {
     if (options.Contains("fix_p")) {
       p = new RooRealVar("p","p",setp);
      } 
     else {
       p = new RooRealVar("p","p", setp, 0.1, 1.5);
     }
   }
   
   RooRealVar *xi=0;
//    if (xi_side != 0.0) {
//       xi = new RooRealVar("xi","xi",xi_side);
//    }
//    else {
//       if (opts.Contains("f")) {
// 	xi= new RooRealVar("xi","xi",-20.0);
//       }
//       else{
// 	xi= new RooRealVar("xi","xi",setxi,-100.0,-0.1);
//       }
//    }
   if (xi_side != 0.0) {
     xi = new RooRealVar("xi","xi",xi_side);
   }
   else {
     if (options.Contains("fix_xi")) {
       xi= new RooRealVar("xi","xi", setxi);
     }
     else{
       xi= new RooRealVar("xi","xi",setxi,-100.0,-0.1);
     }
   }
   
   
   RooArgusBG Bkgd1("argus1","argus1",mbc,Ebeam,*xi,*p);
   RooArgusBG Bkgd2("argus2","argus2",mbc,Ebeam,*xi,*p);
   
   dataset->Print();

   if (options.Contains("fix_n1n2")) {
     RooRealVar N1("N1","N1",setN1);
     RooRealVar N2("N2","N2",setN2);
   }
   else{
     RooRealVar N1("N1","N1",setN1,0.0,200000000.0);
     RooRealVar N2("N2","N2",setN2,0.0,200000000.0);
   }

   if (opts.Contains("f")) {
     RooRealVar Nbkgd1("Nbkgd1","Nbkgd1",4000.0);
     RooRealVar Nbkgd2("Nbkgd2","Nbkgd2",4000.0);
   }
   else{
     RooRealVar Nbkgd1("Nbkgd1","Nbkgd1",setNbkgd1, 0.0, 200000000.0);
     RooRealVar Nbkgd2("Nbkgd2","Nbkgd2",setNbkgd2, 0.0, 200000000.0);
   } 

   if (options.Contains("fa_float")) {
     RooRealVar fa("fa","fa", 0.2, 0.0, 0.5);
   }
   else{
    RooRealVar fa("fa","fa",sfa);
   }




   RooRealVar f3("f3","f3",sf3);
   RooFormulaVar f1("f1","f1","1.0-fa-f3",RooArgSet(fa,f3));

   RooAddPdf signal1_2("signal1_2","signal1_2",
		       RooArgList(fcn1_1,fcn1_2),f1);
   RooAddPdf signal2_2("signal2_2","signal2_2",
		       RooArgList(fcn2_1,fcn2_2),f1);

   RooAddPdf signal1_3("signal1_3","signal1_3",
		       RooArgList(fcn1_1,fcn1_2,fcn1_3),RooArgList(f1,fa));
   RooAddPdf signal2_3("signal2_3","signal2_3",
		       RooArgList(fcn2_1,fcn2_2,fcn2_3),RooArgList(f1,fa));

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

   shapes1.add(Bkgd1);
   yields1.add(Nbkgd1);

   shapes2.add(Bkgd2);
   yields2.add(Nbkgd2);

   RooAddPdf totalPdf1("totalPdf1","totalPdf1", shapes1,yields1);
   RooAddPdf totalPdf2("totalPdf2","totalPdf2", shapes2,yields2);
 
   RooSimultaneous totalPdf("totalPdf","totalPdf",dflav);

   totalPdf.addPdf(totalPdf1,"dflav");
   totalPdf.addPdf(totalPdf2,"dbarflav");
   if (!options.Contains("test")) {
     RooFitResult* fitres = totalPdf.fitTo(*dataset,MINUIT);
     // RooFitResult* fitres = totalPdf.fitTo(*dataset, Extended(kTRUE), Save(kTRUE),
     // Minos(kFALSE), Hesse(kTRUE)); 
   }
   
   if (opts.Contains("Fa")) {
     TString  txtfile1 ;
     txtfile1 = txtfile;
     txtfile1.Replace(txtfile.Sizeof()-5, 0, "_nll");

     FILE* ttt = fopen(txtfile1.Data(), "w+");
     fprintf(ttt, "fa\t| -log(L)\n");

     double famin  = 0;
     double Nllmin = 0;
     
     double myx[10];
     double myy[10];

     char tmp005[100];

     if (options.Contains("mode0")) {
       fa.setConstant(kTRUE);
       if (!options.Contains("test")) {
	 famin = fa.getVal();
	 Nllmin = fitres->minNll();
	 RooFitResult* fitres = totalPdf.fitTo(*dataset,MINUIT);
	 Nllmin = fitres->minNll();}
       else{ famin = 0.1919770406; Nllmin = -981717.5732458038; }
       
       sprintf(tmp005, "fa = %f, -log(L)=%f ", famin, Nllmin);

       fprintf(ttt, "%.10f\t| %.10f\t\n",  famin, Nllmin);
       
       famin = 0.182; 
       fa.setVal(famin);
       fa.setConstant(kTRUE);
       if (!options.Contains("test")) {
	 RooFitResult* fitres = totalPdf.fitTo(*dataset,MINUIT);
	 Nllmin = fitres->minNll();}
       fprintf(ttt, "%.10f\t| %.10f\t\n",  famin, Nllmin);
       
       if (!options.Contains("test")) {
       for (int ii=0; ii<10;ii++){
	 cout << fa.getVal() << endl;
	 famin = 0.125 + ii*0.03;
	 fa.setVal(famin);
	 fa.setConstant(kTRUE);
	 RooFitResult* fitres = totalPdf.fitTo(*dataset,MINUIT);
	 Nllmin = fitres->minNll();
	 myx[ii] = famin;
	 myy[ii] = Nllmin;
	 fprintf(ttt, "%.10f\t| %.10f\t\n",  famin, Nllmin);}}
       else{
	 myx[0] = 0.1250000000 ; myy[0] = -981716.7702510187 ;
	 myx[1] = 0.1550000000 ; myy[1] = -981717.4157330478 ;
	 myx[2] = 0.1850000000 ; myy[2] = -981717.5704506522 ;
	 myx[3] = 0.2150000000 ; myy[3] = -981717.5482880061 ;
	 myx[4] = 0.2450000000 ; myy[4] = -981717.4919983140 ;
	 myx[5] = 0.2750000000 ; myy[5] = -981717.4445960498 ;
	 myx[6] = 0.3050000000 ; myy[6] = -981717.3982418077 ;
	 myx[7] = 0.3350000000 ; myy[7] = -981717.3284391155 ;
	 myx[8] = 0.3650000000 ; myy[8] = -981717.2010539190 ;
	 myx[9] = 0.3950000000 ; myy[9] = -981716.9871923171 ;
       }
     }
     
     if (options.Contains("mode1")) {
       fa.setConstant(kTRUE);
       if (!options.Contains("test")) {
	 famin = fa.getVal();
	 Nllmin = fitres->minNll();
	 RooFitResult* fitres = totalPdf.fitTo(*dataset,MINUIT);
	 Nllmin = fitres->minNll();}
       else{ famin = 0.2135003847; Nllmin = -2680417.5070470721; }
       
       sprintf(tmp005, "fa = %f, -log(L)=%f ", famin, Nllmin);

       fprintf(ttt, "%.10f\t| %.10f\t\n",  famin, Nllmin);
       
       famin = 0.196; 
       fa.setVal(famin);
       fa.setConstant(kTRUE);
       if (!options.Contains("test")) {
	 RooFitResult* fitres = totalPdf.fitTo(*dataset,MINUIT);
	 Nllmin = fitres->minNll();}
       fprintf(ttt, "%.10f\t| %.10f\t\n",  famin, Nllmin);
       
       if (!options.Contains("test")) {
       for (int ii=0; ii<10;ii++){
	 cout << fa.getVal() << endl;
	 famin = 0.18 + ii*0.008;
	 fa.setVal(famin);
	 fa.setConstant(kTRUE);
	 RooFitResult* fitres = totalPdf.fitTo(*dataset,MINUIT);
	 Nllmin = fitres->minNll();
	 myx[ii] = famin;
	 myy[ii] = Nllmin;
	 fprintf(ttt, "%.10f\t| %.10f\t\n",  famin, Nllmin);}}
       else{
	 myx[0] = 0.1000000000  ; myy[0] = -2680381.6718755504;
	 myx[1] = 0.1150000000  ; myy[1] = -2680392.0573015986;
	 myx[2] = 0.1300000000  ; myy[2] = -2680400.3369507231;
	 myx[3] = 0.1450000000  ; myy[3] = -2680406.7099096673;
	 myx[4] = 0.1600000000  ; myy[4] = -2680411.3870465225;
	 myx[5] = 0.1750000000  ; myy[5] = -2680414.5827377541;
	 myx[6] = 0.1900000000  ; myy[6] = -2680416.5144029548;
	 myx[7] = 0.2050000000  ; myy[7] = -2680417.3950802600;
	 myx[8] = 0.2200000000  ; myy[8] = -2680417.4314163541;
	 myx[9] = 0.2350000000  ; myy[9] = -2680416.8167262720;
       }
     }
       
     fclose(ttt);
     TCanvas *  MyCa = new TCanvas("MyCa","My Plot",20,50,1050,600);
     TGraph  *  MyGr = new TGraph(10,myx,myy);
     MyGr->SetTitle("fa vs -log(L)");
     MyGr->GetXaxis()->SetTitle("fa");
     MyGr->GetYaxis()->SetTitle("-log(L)");
     MyGr->Draw("ACP");

     TPaveText *pt = new TPaveText(0.11,0.77,0.4,0.74,"BRNDC");
     pt->SetBorderSize(0);
     pt->SetTextAlign(12);
     TText *text = pt->AddText(tmp005);
     pt->Draw();

     TString  epsfile1 ;
     epsfile1 = epsfile;
     epsfile1.Replace(epsfile.Sizeof()-5, 0, "_nll");
     
     MyCa->Print(epsfile1);
   }
   
   if (opts.Contains("p")) {
     TCanvas *canvas= new TCanvas("canvas","mbc",900,300);

      canvas->Divide(3,1);
      canvas_1->SetLogy();
      canvas_2->SetLogy();

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
    
      dflav="dflav";
      if (num_fcn != 0) {
	 if (!opts.Contains("d")) {
	    totalPdf.plotOn(mbcFrame,LineColor(kRed),LineWidth(0.6),
			    Slice(dflav),ProjWData(RooArgSet(Ebeam,dflav),ebeamdata));
	 } else {
	    totalPdf.plotOn(mbcFrame,LineColor(kRed),LineWidth(0.6),
			    Slice(dflav),ProjWData(*dataset));
	 }
	 
	 chisq1 = mbcFrame->chiSquare()*mbcFrame->GetNbinsX();
	 mbcFrame->Draw();
  
 
	 if (num_fcn == 2) {
	    if (!opts.Contains("d")) {
	       totalPdf.plotOn(mbcFrame,Components(RooArgSet(Bkgd1,fcn1_2)),
			       Slice(dflav),LineColor(kGreen),LineWidth(0.6),
			       ProjWData(RooArgSet(Ebeam,dflav),ebeamdata));
	    } else {
	       totalPdf.plotOn(mbcFrame,Components(RooArgSet(Bkgd1,fcn1_2)),
			       Slice(dflav),LineColor(kGreen),LineWidth(0.6),
			       ProjWData(*dataset));
	    }
	
	    mbcFrame->Draw();
	 }

	 if (num_fcn == 3) {
	    if (!opts.Contains("d")) {
	       totalPdf.plotOn(mbcFrame,Components(RooArgSet(Bkgd1,fcn1_3,fcn1_2)),
			       Slice(dflav),LineColor(kGreen),LineWidth(0.6),
			       ProjWData(RooArgSet(Ebeam,dflav),ebeamdata));
	       totalPdf.plotOn(mbcFrame,Components(RooArgSet(Bkgd1,fcn1_3)),
			       Slice(dflav),LineColor(kMagenta),LineWidth(0.6),
			       ProjWData(RooArgSet(Ebeam,dflav),ebeamdata));
	    } else {
	       totalPdf.plotOn(mbcFrame,Components(RooArgSet(Bkgd1,fcn1_3,fcn1_2)),
			       Slice(dflav),LineColor(kGreen),LineWidth(0.6),
			       ProjWData(*dataset));
	       totalPdf.plotOn(mbcFrame,Components(RooArgSet(Bkgd1,fcn1_3)),
			       Slice(dflav),LineColor(kMagenta),LineWidth(0.6),
			       ProjWData(*dataset));
	    }

	    mbcFrame->Draw();
	 }
   
      } 

      if (!opts.Contains("d")) {
	 totalPdf.plotOn(mbcFrame,Components(RooArgSet(Bkgd1)),
			 Slice(dflav),LineColor(kBlue),LineWidth(0.6),
			 ProjWData(RooArgSet(Ebeam,dflav),ebeamdata));
      } else {
	 totalPdf.plotOn(mbcFrame,Components(RooArgSet(Bkgd1)),
			 Slice(dflav),LineColor(kBlue),LineWidth(0.6),
			 ProjWData(*dataset));
      }
    
      mbcFrame->SetTitle(title1);
      mbcFrame->SetMinimum(min);

      mbcFrame->Draw();
    
      canvas->cd(2);
      RooPlot* mbcFrame=mbc.frame();
      RooPlot* mbcFrame=mbc.frame(60);
      mbcFrame->Draw();
    
      dataset->plotOn(mbcFrame,Cut("dflav==dflav::dbarflav"));
      mbcFrame->getAttMarker()->SetMarkerSize(0.6);
      mbcFrame->Draw();
    
      dflav="dbarflav";
      if (num_fcn != 0) {
	 if (!opts.Contains("d")) {
	    totalPdf.plotOn(mbcFrame,LineColor(kRed),LineWidth(0.6),
			    Slice(dflav),ProjWData(RooArgSet(Ebeam,dflav),ebeamdata));
	 } else {
	    totalPdf.plotOn(mbcFrame,LineColor(kRed),LineWidth(0.6),
			    Slice(dflav),ProjWData(*dataset));
	 }
	 chisq2 = mbcFrame->chiSquare()*mbcFrame->GetNbinsX();
	 mbcFrame->Draw();
      
	 if (num_fcn == 2) {
	    if (!opts.Contains("d")) {
	       totalPdf.plotOn(mbcFrame,Components(RooArgSet(Bkgd2,fcn2_2)),
			       Slice(dflav),LineColor(kGreen),LineWidth(0.6),
			       ProjWData(RooArgSet(Ebeam,dflav),ebeamdata));
	    } else {
	       totalPdf.plotOn(mbcFrame,Components(RooArgSet(Bkgd2,fcn2_2)),
			       Slice(dflav),LineColor(kGreen),LineWidth(0.6),
			       ProjWData(*dataset));
	    }
	
	    mbcFrame->Draw();
	 }

	 if (num_fcn == 3) {
	    if (!opts.Contains("d")) {
	       totalPdf.plotOn(mbcFrame,Components(RooArgSet(Bkgd2,fcn2_3,fcn2_2)),
			       Slice(dflav),LineColor(kGreen),LineWidth(0.6),
			       ProjWData(RooArgSet(Ebeam,dflav),ebeamdata));
	  
	       totalPdf.plotOn(mbcFrame,Components(RooArgSet(Bkgd2,fcn2_3)),
			       Slice(dflav),LineColor(kMagenta),LineWidth(0.6),
			       ProjWData(RooArgSet(Ebeam,dflav),ebeamdata));
	    } else {
	       totalPdf.plotOn(mbcFrame,Components(RooArgSet(Bkgd2,fcn2_3,fcn2_2)),
			       Slice(dflav),LineColor(kGreen),LineWidth(0.6),
			       ProjWData(*dataset));
	  
	       totalPdf.plotOn(mbcFrame,Components(RooArgSet(Bkgd2,fcn2_3)),
			       Slice(dflav),LineColor(kMagenta),LineWidth(0.6),
			       ProjWData(*dataset));
	    }
	
	    mbcFrame->Draw();
	 }
      
      }
    
      if (!opts.Contains("d")) {
	 totalPdf.plotOn(mbcFrame,Components(RooArgSet(Bkgd2)),
			 Slice(dflav),LineColor(kBlue),LineWidth(0.6),
			 ProjWData(RooArgSet(Ebeam,dflav),ebeamdata));
      } else {
	 totalPdf.plotOn(mbcFrame,Components(RooArgSet(Bkgd2)),
			 Slice(dflav),LineColor(kBlue),LineWidth(0.6),
			 ProjWData(*dataset));
      }
      mbcFrame->SetTitle(title2);
      mbcFrame->SetMinimum(min);

      mbcFrame->Draw();

      if (d > 0) {
	 canvas->cd(3);
	 RooPlot* mbcFrame=mbc.frame();
      
	 RooPlot* paramWin1 = totalPdf.paramOn(mbcFrame,dataset,
					       "",2,"NELU",0.1,0.9,0.9);

	 mbcFrame->GetXaxis()->SetLabelSize(0);
	 mbcFrame->GetXaxis()->SetTickLength(0);
	 mbcFrame->GetXaxis()->SetLabelSize(0);
	 mbcFrame->GetXaxis()->SetTitle("");
	 mbcFrame->GetXaxis()->CenterTitle();

	 mbcFrame->GetYaxis()->SetLabelSize(0);
	 mbcFrame->GetYaxis()->SetTitleSize(0.03);
	 mbcFrame->GetYaxis()->SetTickLength(0);


	 paramWin1->getAttText()->SetTextSize(0.06);

	 mbcFrame->Draw();
	 dflav="dflav";
      
	 mbcFrame->SetTitle("Fit Parameters");

	 TPaveText * ATextBox;
	 ATextBox = new TPaveText(.1, .1, .8, .2,"BRNDC");

	 sprintf(tempString, "#chi^{2}_{1} = %.1f, #chi^{2}_{2} = %.1f",chisq1,chisq2); 
	 ATextBox->AddText(tempString);

	 mbcFrame->addObject(ATextBox);

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
	 RooPlot* paramWin2 = totalPdf.paramOn(mbcFrame,  Format("NELU", AutoPrecision(6)), Layout(0.1, 0.8, 0.9) );
      
	 mbcFrame->Draw();
      
	 dflav="dbarflav";
	 mbcFrame->SetTitle(title2);
	 mbcFrame->Draw();
      }

      canvas->Print(epsfile);

      // **********************************************
      // Dump (sum) RooPlot in a file for later viewing
      // **********************************************
      
      TCanvas *canvastmp= new TCanvas("canvastmp","mbc",400,400);
      
      RooPlot* mbcFrame=mbc.frame(60);
      
      dataset->plotOn(mbcFrame);
      mbcFrame->getAttMarker()->SetMarkerSize(0.6);
      
      if (num_fcn != 0) {
	if (!opts.Contains("d")) {
	  totalPdf.plotOn(mbcFrame,LineColor(kRed),LineWidth(2),
			  ProjWData(RooArgSet(Ebeam),ebeamdata));
	} else {
	  totalPdf.plotOn(mbcFrame,LineColor(kRed),LineWidth(2),
			  ProjWData(*dataset));
	}
      }
      //    canvas->Update();
      if (!opts.Contains("d")) {
	totalPdf.plotOn(mbcFrame,Components(RooArgSet(Bkgd1,Bkgd2)),
			LineColor(kBlue),LineWidth(2),
			ProjWData(RooArgSet(Ebeam),ebeamdata));
      } else {
	totalPdf.plotOn(mbcFrame,Components(RooArgSet(Bkgd1,Bkgd2)),
			LineColor(kBlue),LineWidth(2),
			ProjWData(*dataset));
      }
      
      dataset->plotOn(mbcFrame);
      mbcFrame->getAttMarker()->SetMarkerSize(0.6);
      
      mbcFrame->SetTitle(title1);
      TFile* loc_out=TFile::Open(epsfile.ReplaceAll(".eps", 4, ".root",
						    5), "RECREATE");
      mbcFrame->Write("frame");

      // **********************************************

      TString  rootfile ;
      canvas->Write("canvas");
      loc_out->Write(); loc_out->Close();
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
  
   Double_t Xi = xi->getVal();
   Double_t Xi_err = xi->getError();

   Double_t P = p->getVal();
   Double_t P_err = p->getError();  

   Double_t Dmass = md->getVal();
   Double_t Dmass_err =md->getError();

   Double_t Sigmap_1 = sigmap1->getVal();
   Double_t Sigmap_1_err =sigmap1->getError();

   Double_t Fa = fa.getVal();
   Double_t Fa_err = fa.getError();

   if (!options.Contains("test")) {
   Double_t minNll  = fitres->minNll();
   }
   else{
   Double_t minNll  = 0;
   }


// --------------------------------------------------------------------------
   FILE* table = fopen(txtfile.Data(), "w+");

   fprintf(table, "Name\t|| Value\t|| Error\n");
   if (num_fcn != 0){
      fprintf(table, "N1\t| %.10f\t| %.10f\n", yield1, yield1_err);
      fprintf(table, "N2\t| %.10f\t| %.10f\n", yield2, yield2_err);
   }
   fprintf(table, "Nbkgd1\t| %.10f\t| %.10f\n", back1, back1_err);
   fprintf(table, "Nbkgd2\t| %.10f\t| %.10f\n", back2, back2_err);
   if (options.Contains("fa_float")) {
      fprintf(table, "fa\t| %.10f\t| %.10f\n", Fa, Fa_err);
   }
   if (floatwidth != 0){
      fprintf(table, "Gamma\t| %.10f\t| %.10f\n", Gamma, Gamma_err);
   }
   if (num_fcn != 0){
      fprintf(table, "md\t| %.10f\t| %.10f\n", Dmass, Dmass_err);
   }  
   fprintf(table, "p\t| %.10f\t| %.10f\n", P, P_err);
   if (num_fcn != 0){
      fprintf(table, "sigmap1\t| %.10f\t| %.10f\n", Sigmap_1, Sigmap_1_err);
   }  
   fprintf(table, "xi\t| %.10f\t| %.10f\n", Xi, Xi_err);
   fprintf(table, "chisq1\t| %.10f\t| %.10f\n", chisq1, 0);
   fprintf(table, "chisq2\t| %.10f\t| %.10f\n", chisq2, 0);
   if (options.Contains("getNll")) {
      fprintf(table, "Nll\t| %.10f\t| %.10f\n", minNll, 0);
   }

   fclose(table);

   cout << "Fit done." << endl;

}



