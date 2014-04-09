/*****************************************************************************
 * Project: RooFit                                                           *
 * Package: RooFitModels                                                     *
 *    File: $$
 * Authors:                                                                  *
 *   WV, Wouter Verkerke, UC Santa Barbara, verkerke@slac.stanford.edu       *
 *   DK, David Kirkby,    UC Irvine,         dkirkby@uci.edu                 *
 *   AR, Anders Ryd,      Cornell U.,        ryd@lepp.cornell.edu            *
 *                                                                           *
 * Copyright (c) 2000-2004, Regents of the University of California          *
 *                          and Stanford University. All rights reserved.    *
 * copyright (c) 2004       Cornell University
 *                                                                           *
 * Redistribution and use in source and binary forms,                        *
 * with or without modification, are permitted according to the terms        *
 * listed in LICENSE (http://roofit.sourceforge.net/license.txt)             *
 *****************************************************************************/

// -- CLASS DESCRIPTION [PDF] --

#include <iostream>
#include <math.h>
#include <vector>
#include <string>


#include "RooFitModels/RooDLineShape2D.hh"
#include "RooFitModels/RooDLineShapeImp2D.hh"
#include "RooFitCore/RooAbsReal.hh"
#include "RooFitCore/RooRealVar.hh"
#include "RooFitCore/RooArgSet.hh"
#include "RooFitCore/RooArgList.hh"


RooDLineShape2D::RooDLineShape2D(const char *name, const char *title, 
 				 int npointEbeam, 
				 RooAbsReal& _mbc1,
				 RooAbsReal& _mbc2,
				 RooAbsReal& _Ebeam,
				 RooAbsReal& _mres,
				 RooAbsReal& _gamma, 
				 RooAbsReal& _r, 
				 RooAbsReal& _sigmaE,
				 RooArgList& _smearpar,
				 RooAbsReal& _md, 
				 RooAbsReal& _nonres
) :
  RooAbsPdf(name, title),
  mbc1("mbc1", "Dependent", this, _mbc1),
  mbc2("mbc2", "Dependent", this, _mbc2),
  mres("mres", "mres", this, _mres),
  Ebeam("Ebeam", "Ebeam", this, _Ebeam),
  gamma("gamma", "gamma", this, _gamma),
  r("r", "r", this, _r),
  sigmaE("sigmaE", "sigmaE", this, _sigmaE),
  sigmap1("sigmap1", "sigmap1", this, (RooAbsReal&)_smearpar[0]),
  sigmap1a("sigmap1a", "sigmap1a", this, (RooAbsReal&)_smearpar[1]),
  sigmap1b("sigmap1b", "sigmap1b", this, (RooAbsReal&)_smearpar[2]),
  f1a("f1a", "f1a", this, (RooAbsReal&)_smearpar[3]),
  f1b("f1b", "f1b", this, (RooAbsReal&)_smearpar[4]),
  sigmap2("sigmap2", "sigmap2", this, (RooAbsReal&)_smearpar[5]),
  sigmap2a("sigmap2a", "sigmap2a", this, (RooAbsReal&)_smearpar[6]),
  sigmap2b("sigmap2b", "sigmap2b", this, (RooAbsReal&)_smearpar[7]),
  f2a("f2a", "f2a", this, (RooAbsReal&)_smearpar[8]),
  f2b("f2b", "f2b", this, (RooAbsReal&)_smearpar[9]),
  md("md", "md", this, _md),
  nonres("nonres", "nonres", this, _nonres),
  m_npointEbeam(npointEbeam)
{
}

RooDLineShape2D::RooDLineShape2D(const RooDLineShape2D& other, 
				 const char* name) :
  RooAbsPdf(other, name), 
  mbc1("mbc1", this, other.mbc1), 
  mbc2("mbc2", this, other.mbc2), 
  mres("mres", this, other.mres),
  Ebeam("Ebeam", this, other.Ebeam),
  gamma("gamma", this, other.gamma),
  r("r", this, other.r),
  sigmaE("sigmaE", this, other.sigmaE), 
  sigmap1("sigmap1", this, other.sigmap1),
  sigmap1a("sigmap1a", this, other.sigmap1a),
  sigmap1b("sigmap1b", this, other.sigmap1b),
  f1a("f1a", this, other.f1a),
  f1b("f1b", this, other.f1b),
  sigmap2("sigmap2", this, other.sigmap2),
  sigmap2a("sigmap2a", this, other.sigmap2a),
  sigmap2b("sigmap2b", this, other.sigmap2b),
  f2a("f2a", this, other.f2a),
  f2b("f2b", this, other.f2b),
  md("md", this, other.md),
  nonres("nonres", this, other.nonres),
  m_npointEbeam(other.m_npointEbeam)
{
}

Double_t RooDLineShape2D::evaluate() const {

  int newval=(mres_save!=mres)|| 
    (gamma_save!=gamma)||
    (r_save!=r)||
    (sigmaE_save!=sigmaE)||
    (sigmap1_save!=sigmap1)||
    (sigmap1a_save!=sigmap1a)||
    (sigmap1b_save!=sigmap1b)||
    (f1a_save!=f1a)||
    (f1b_save!=f1b)||
    (sigmap2_save!=sigmap2)||
    (sigmap2a_save!=sigmap2a)||
    (sigmap2b_save!=sigmap2b)||
    (f2a_save!=f2a)||
    (f2b_save!=f2b)||
    (md_save!=md);

  static unsigned int i_cache=0;

  static std::vector<Double_t> val_cache;
  static std::vector<Double_t> mbc1_cache;
  static std::vector<Double_t> mbc2_cache;
  static std::vector<Double_t> ebeam_cache;
  

  static int count2=0;

  if (count2<100){
    count2++;

    //std::cout << mbc1 << " "<< mbc2 << " "<< Ebeam << std::endl;

  }

 
  if (shapes.size()==0||newval){

    count2=0;

    i_cache=0;
  
    val_cache.clear();
    mbc1_cache.clear();
    mbc2_cache.clear();
    ebeam_cache.clear();

   
    for (unsigned int i=0;i<shapes.size();i++){
      delete shapes[i];
    }
    
    shapes.clear();

    //std::cout <<"New evaluation md:"<<std::endl;
    //std::cout <<"  sigmap1:"<<sigmap1<<std::endl;
    //std::cout <<"  sigmap1a:"<<sigmap1a<<std::endl;
    //std::cout <<"  sigmap1b:"<<sigmap1b<<std::endl;
    //std::cout <<"  f1a:"<<f1a<<std::endl;
    //std::cout <<"  f1b:"<<f1b<<std::endl;
    //std::cout <<"  sigmap2:"<<sigmap2<<std::endl;
    //std::cout <<"  sigmap2a:"<<sigmap2a<<std::endl;
    //std::cout <<"  sigmap2b:"<<sigmap2b<<std::endl;
    //std::cout <<"  f2a:"<<f2a<<std::endl;
    //std::cout <<"  f2b:"<<f2b<<std::endl;

    mres_save=mres; 
    gamma_save=gamma;
    r_save=r;
    sigmaE_save=sigmaE;
    sigmap1_save=sigmap1;
    sigmap1a_save=sigmap1a;
    sigmap1b_save=sigmap1b;
    f1a_save=f1a;
    f1b_save=f1b;
    sigmap2_save=sigmap2;
    sigmap2a_save=sigmap2a;
    sigmap2b_save=sigmap2b;
    f2a_save=f2a;
    f2b_save=f2b;
    md_save=md;

    assert(m_npointEbeam>0);

    for(int i=0;i<m_npointEbeam;i++){

      double ebeam;

      if (m_npointEbeam==1) {
	if (Ebeam.max()>1e10) {
	  ebeam=Ebeam;
	}
	else{
	  ebeam=0.5*(Ebeam.min()+Ebeam.max());
	}
      }
      else{
	ebeam=Ebeam.min()+i*(Ebeam.max()-Ebeam.min())/(m_npointEbeam-1.0);
      }
     
      
      shapes.push_back(new RooDLineShapeImp2D(mres,
					      gamma,
					      r,
					      sigmaE,
					      sigmap1,
					      sigmap1a,
					      sigmap1b,
					      f1a,
					      f1b,
					      sigmap2,
					      sigmap2a,
					      sigmap2b,
					      f2a,
					      f2b,
					      md,
					      ebeam,nonres)); 

    }

    //std::cout << "Done with new evaluation"<<std::endl;
 
  }


  if (i_cache>=mbc1_cache.size()) i_cache=0;

  if (i_cache<mbc1_cache.size()&&
      mbc1_cache[i_cache]==mbc1&&
      mbc2_cache[i_cache]==mbc2&&
      ebeam_cache[i_cache]==Ebeam){
    //std::cout << "Found a match:"<<i_cache<<" "<<mbc1_cache.size()<<std::endl;
    i_cache++;
    assert(val_cache[i_cache-1]>=0.0);
    return val_cache[i_cache-1];
  }



  static int count=0;

  count++;

  if (count%1000==0){
    //std::cout << "Evaluation number:"<<count<<std::endl;
  }


  if (mbc1>Ebeam.max()) return 1e-20;
  if (mbc2>Ebeam.max()) return 1e-20;

  double ret_val=0.0;

  if (m_npointEbeam==1){

    double ebeam=0.0;

    if (Ebeam.max()>1e10){
      ebeam=Ebeam;
    }
    else{
      ebeam=0.5*(Ebeam.min()+Ebeam.max());
    }

    if (mbc1>ebeam) {
      //std::cout << "mbc, ebeam:"<<mbc<<" "<<ebeam<<std::endl;
      ret_val=1e-20;
    }

    if (mbc2>ebeam) {
      //std::cout << "mbc, ebeam:"<<mbc<<" "<<ebeam<<std::endl;
      ret_val=1e-20;
    }

    if (ret_val==0.0){
      ret_val=shapes[0]->evaluate(mbc1,mbc2); 
    }

    assert(ret_val>=0.0);

  } else {
    
    double DeltaEbeam=(Ebeam.max()-Ebeam.min())/(m_npointEbeam-1.0);
    
    unsigned int i1=(int)((Ebeam-Ebeam.min())/DeltaEbeam);
    unsigned int i2=i1+1;
    
    //std::cout << "Ebeam, Ebeam.min(), mbc, i1:"<<Ebeam<<" "<<Ebeam.min()<<" "<<
    //  mbc<<" "<<i1<<std::endl;
    
    //due to rounding...
    assert(i2<1+shapes.size());
    if (i2==shapes.size()) i2=shapes.size()-1;

    double Ebeam1=Ebeam.min()+i1*DeltaEbeam;
    double Ebeam2=Ebeam.min()+i2*DeltaEbeam;

    //std::cout << "Ebeam1, Ebeam2, DeltaEbeam:"<<Ebeam1<<" "<<Ebeam2<<" "<<DeltaEbeam<<endl;

    assert(Ebeam1<=Ebeam); 
    assert(Ebeam2>=Ebeam); 

    //if (mbc>Ebeam2) return shapes[i2]->evaluate(mbc); 

    double w=(Ebeam2-Ebeam)/DeltaEbeam;
  
    //return shapes[2]->evaluate1(mbc);
    ret_val=shapes[i1]->evaluate(mbc1,mbc2)*w+shapes[i2]->evaluate(mbc1,mbc2)*(1.0-w);
    
    if (ret_val<0.0) {
      if (ret_val<-1e-10){
      std::cout << "Negative:"<<shapes[i1]->evaluate(mbc1,mbc2)<<" "
		<<shapes[i2]->evaluate(mbc1,mbc2)<<" "<<w<<std::endl;
      }
      ret_val=0.0;
    }
    
  }

  assert(ret_val>=0.0);

  val_cache.push_back(ret_val);
  mbc1_cache.push_back(mbc1);
  mbc2_cache.push_back(mbc2);
  ebeam_cache.push_back(Ebeam);
  
 
  return ret_val;

}


Int_t RooDLineShape2D::getAnalyticalIntegral(RooArgSet& allVars, RooArgSet& analVars, const char* rangeName) const
{

  //std::cout << "Asking for RooDLineShape2D integral"<< std::cout;

  if (matchArgs(allVars,analVars,mbc1,mbc2)) return 1 ;

  if (matchArgs(allVars,analVars,mbc1)) return 2 ;

  if (matchArgs(allVars,analVars,mbc2)) return 3 ;

  std::cout << "Integral not matching!"<<std::endl;

  return 0 ;
}


Double_t RooDLineShape2D::analyticalIntegral(Int_t code, const char* rangeName) const
{


  //std::cout << "Calculating RooDLineShape2D integral"<< std::cout;

  if (code==1)   {

    return 1.0;

    int nbin=1000;

    double dm1=(mbc1.max()-mbc1.min())/nbin;
    double dm2=(mbc2.max()-mbc2.min())/nbin;

    double sum=0.0;
    
    for (int i1=0;i1<nbin;i1++){
      std::cout << "Doing integral:"<<i1<<std::endl;
      double m1=mbc1.min()+(i1+0.5)*dm1;
      for (int i2=0;i2<nbin;i2++){
	double m2=mbc2.min()+(i2+0.5)*dm2;
	sum+=dm1*dm2*shapes[0]->evaluate(m1,m2);
      }
    }

    std::cout << "RooDLineShape2D sum:"<<sum<<std::endl;

    return 1.0;
  }

  if (code==2) return shapes[0]->evalInt1(mbc2);
  
  if (code==3) return shapes[0]->evalInt2(mbc1);

  std::cout << "code="<<code<<" mbc1:"<<mbc1<<" mbc2:"<<mbc2<<std::endl;

  assert(0);

}
