/*****************************************************************************
 * Project: RooFit                                                           *
 * Package: RooFitModels                                                     *
 *    File: $Id:$
 * Authors:                                                                  *
 *   Anders Ryd, Cornell U.                                                  *
 *                                                                           *
 * Copyright (c) 2004 Cornell U.                                             *
 *                                                                           *
 * Redistribution and use in source and binary forms,                        *
 * with or without modification, are permitted according to the terms        *
 * listed in LICENSE (http://roofit.sourceforge.net/license.txt)             *
 *****************************************************************************/

// -- CLASS DESCRIPTION [PDF] --

//#include "BaBar/BaBar.hh"
#include <iostream>
#include <math.h>

#include "RooFitModels/RooDiag.hh"
#include "RooFitCore/RooRealVar.hh"
#include "RooFitCore/RooRealConstant.hh"

ClassImp(RooDiag)

RooDiag::RooDiag(const char *name, const char *title,
		 RooAbsReal& _m1, RooAbsReal& _m2,
		 RooAbsReal& _s, RooAbsReal& _alpha, 
		 RooAbsReal& _m0, RooAbsReal& _c, RooAbsReal& _p) :
  RooAbsPdf(name, title), 
  m1("m1","Mass1",this,_m1),
  m2("m2","Mass2",this,_m2),
  s("s","sigma",this,_s),
  alpha("alpha","alpha",this,_alpha),
  m0("m0","Resonance mass",this,_m0),
  c("c","Slope parameter",this,_c),
  p("p","power parameter",this,_p),
  m0_save(0.0),
  s_save(0.0),
  alpha_save(0.0),
  c_save(0.0),
  p_save(0.0),
  integ(0.0),
  integ1d(0.0)
{
}

RooDiag::RooDiag(const RooDiag& other, const char* name) :
  RooAbsPdf(other,name), 
  m1("m1",this,other.m1), 
  m2("m2",this,other.m2), 
  s("s",this,other.s), 
  alpha("alpha",this,other.alpha), 
  m0("m0",this,other.m0), 
  c("c",this,other.c),
  p("p",this,other.p),
  m0_save(other.m0_save),
  s_save(other.s_save),
  alpha_save(other.alpha_save),
  c_save(other.c_save),
  p_save(other.p_save),
  integ(other.integ),
  integ1d(other.integ1d)
{
}


Double_t RooDiag::evaluate() const {

  if (m1>m0) return 0.0;
  if (m2>m0) return 0.0;

  Double_t ms=0.5*(m1+m2);
  Double_t mdiff=0.5*(m2-m1);

  Double_t t= ms/m0;
  assert(t <= 1);

  Double_t u= 1 - t*t;

  static double invsqrt2pi=1.0/sqrt(2*atan2(0.0,-1.0));

  double sigma=s*(1+alpha*(1-t));

  return (invsqrt2pi/sigma)*exp(-0.5*mdiff*mdiff/(sigma*sigma))*ms*pow(u,p)*exp(c*u);
}


Int_t RooDiag::getAnalyticalIntegral(RooArgSet& allVars, RooArgSet& analVars, const char* rangeName) const
{

  if (matchArgs(allVars,analVars,m1,m2)) return 1;

  if (matchArgs(allVars,analVars,m1)) return 2;

  if (matchArgs(allVars,analVars,m2)) return 3;


  if (matchArgs(allVars,analVars,m2,m0)) std::cout << "Want integral 1....";
  if (matchArgs(allVars,analVars,m1,m0)) std::cout << "Want integral 2....";
  if (matchArgs(allVars,analVars,m0)) std::cout << "Want integral 3....";
  if (matchArgs(allVars,analVars,m2,m1,m0)) std::cout << "Want integral 4....";

  std::cout << "Can not do integral"<<std::endl;
  

  return 0;

}


Double_t RooDiag::analyticalIntegral(Int_t code, const char* rangeName) const
{


  if (code==2) {

    if (m2>m0) return 0.0;

    int nbins=1000;

    double intsum=0.0;
    
    double ddm1=(m1.max()-m1.min())/nbins;

    for (int i1=0;i1<nbins;i1++){
      double mm1=m1.min()+(i1+0.5)*ddm1;
      if (mm1>m0) continue;
    
      Double_t ms=0.5*(mm1+m2);
      Double_t mdiff=0.5*(m2-mm1);
    
      Double_t t= ms/m0;
      assert (t <= 1);
      
      Double_t u= 1-t*t;
      
      static double invsqrt2pi=1.0/sqrt(2*atan2(0.0,-1.0));

      double sigma=s*(1+alpha*(1-t));
  
      intsum+=ddm1*(invsqrt2pi/sigma)*exp(-0.5*mdiff*mdiff/(sigma*sigma))*ms*pow(u,p)*exp(c*u);
      
    }

    return intsum;
  }
  if (code==3) {

    if (m1>m0) return 0.0;

    int nbins=1000;

    double intsum=0.0;
    
    double ddm2=(m2.max()-m2.min())/nbins;

    for (int i2=0;i2<nbins;i2++){
      double mm2=m2.min()+(i2+0.5)*ddm2;
      if (mm2>m0) continue;
    
      Double_t ms=0.5*(mm2+m1);
      Double_t mdiff=0.5*(mm2-m1);
    
      Double_t t= ms/m0;
      assert (t <= 1);
      
      Double_t u= 1-t*t;
      
      static double invsqrt2pi=1.0/sqrt(2*atan2(0.0,-1.0));

      double sigma=s*(1+alpha*(1-t));
  
      intsum+=ddm2*(invsqrt2pi/sigma)*exp(-0.5*mdiff*mdiff/(sigma*sigma))*ms*pow(u,p)*exp(c*u);
      
    }

    return intsum;


  }

  assert(code==1);

  //for the ploting...
  //if (m0_save==m0&&s_save==s&&c_save==c){
  if (s_save==s&&c_save==c&&alpha_save==alpha&&p_save==p){
    return integ;
  }


  ///////
  
  //int nbins=10000;

  // double intsum=0.0;

  //double ddm1=(m1.max()-m1.min())/nbins;
  //double ddm2=(m2.max()-m2.min())/nbins;

  //for (int i1=0;i1<nbins;i1++){
  //  double mm1=m1.min()+(i1+0.5)*ddm1;
  //  if (mm1>m0) continue;
  //  for (int i2=0;i2<nbins;i2++){
  //    double mm2=m2.min()+(i2+0.5)*ddm2;
  //    if (mm2>m0) continue;
  //    Double_t ms=0.5*(mm1+mm2);
  //    Double_t mdiff=0.5*(mm2-mm1);
      
  //    Double_t t= ms/m0;
  //    assert (t <= 1);
      
  //    Double_t u= 1-t*t;
      
  //    static double invsqrt2pi=1.0/sqrt(2*atan2(0.0,-1.0));

  //    double sigma=s*(1+alpha*(1-t));
  
  //    intsum+=ddm1*ddm2* (invsqrt2pi/sigma)*exp(-0.5*mdiff*mdiff/(sigma*sigma))*ms*pow(u,p)*exp(c*u);      
  //  }
  //}
  
  ////
    
  alpha_save=alpha;
  m0_save=m0;
  s_save=s;
  c_save=c;
  p_save=p;

  //std::cout << "RooDiag doing integral" << std::endl;

  // Formula for integration over m when p=0.5
  //static const Double_t pi = atan2(0.0,-1.0);
  //cout << "pi:"<<pi<<endl;
  Double_t min1 = (m1.min() < m0) ? m1.min() : m0;
  Double_t max1 = (m1.max() < m0) ? m1.max() : m0;

  Double_t min2 = (m2.min() < m0) ? m2.min() : m0;
  Double_t max2 = (m2.max() < m0) ? m2.max() : m0;

  //cout << "min1 min2:"<<min1<<" "<<min2<<endl;
  //cout << "max1 max2:"<<max1<<" "<<max2<<endl;

  //assert(fabs(min1-min2)<0.0001);
  //assert(fabs(max1-max2)<0.0001);

  Double_t avgmax=0.5*(max1+max2);
  Double_t avgmin=0.5*(min1+min2);

  int nstep=10000;

  Double_t dms=(avgmax-avgmin)/nstep;

  int i=0;

  Double_t integral=0;

  for(i=0;i<nstep;i++){
    Double_t ms=avgmin+(i+0.5)*dms;
    
    Double_t t= ms/m0;
    if(t >= 1) {
      assert(0);
      return 0;
    }
    
    Double_t u= 1 - t*t;
    
    Double_t Argus=ms*pow(u,p)*exp(c*u);


    Double_t deltambcmax1=max2-ms;
    Double_t deltambcmax2=ms-min1;

    Double_t deltambcmax=deltambcmax1<deltambcmax2?deltambcmax1:deltambcmax2;

    Double_t deltambcmin1=min2-ms;
    Double_t deltambcmin2=ms-max1;

    Double_t deltambcmin=deltambcmin1>deltambcmin2?deltambcmin1:deltambcmin2;

    assert(deltambcmin<deltambcmax);

    double sigma=s*(1+alpha*(1-t));

    static double invsqrttwo=1.0/sqrt(2.0);

    //Double_t GausInt=0.5*(erf(invsqrttwo*deltambcmax/sigma)-erf(invsqrttwo*deltambcmin/sigma));
    Double_t GausInt=erf(invsqrttwo*deltambcmax/sigma);

    //cout << "ms,GausInt:"<<ms<<" "<<GausInt<<endl;

    integral+=dms*GausInt*Argus;

  }

  integral=2*integral;

  //cout << "intsum, integral:"<<intsum<<" "<<integral<<endl;

  integ=integral;

  return integral;

}


