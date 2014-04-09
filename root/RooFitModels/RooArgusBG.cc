/*****************************************************************************
 * Project: RooFit                                                           *
 * Package: RooFitModels                                                     *
 *    File: $Id: RooArgusBG.cc,v 1.4 2007/07/03 14:55:52 xs32 Exp xs32 $
 * Authors:                                                                  *
 *   WV, Wouter Verkerke, UC Santa Barbara, verkerke@slac.stanford.edu       *
 *   DK, David Kirkby,    UC Irvine,         dkirkby@uci.edu                 *
 *                                                                           *
 * Copyright (c) 2000-2004, Regents of the University of California          *
 *                          and Stanford University. All rights reserved.    *
 *                                                                           *
 * Redistribution and use in source and binary forms,                        *
 * with or without modification, are permitted according to the terms        *
 * listed in LICENSE (http://roofit.sourceforge.net/license.txt)             *
 *****************************************************************************/

// -- CLASS DESCRIPTION [PDF] --

//#include "BaBar/BaBar.hh"
#include <iostream>
#include <math.h>

#include "RooFitModels/RooArgusBG.hh"
#include "RooFitModels/RooParmFcn.hh"
#include "RooFitCore/RooRealVar.hh"
#include "RooFitCore/RooRealConstant.hh"

ClassImp(RooArgusBG)

RooArgusBG::RooArgusBG(const char *name, const char *title,
		       RooAbsReal& _m, RooAbsReal& _m0, RooAbsReal& _c) :
  RooAbsPdf(name, title), 
  m("m","Mass",this,_m),
  m0("m0","Resonance mass",this,_m0),
  c("c","Slope parameter",this,_c),
  p("p","Power",this,(RooRealVar&)RooRealConstant::value(0.5)),
  norm(0)
{
}

RooArgusBG::RooArgusBG(const char *name, const char *title,
		       RooAbsReal& _m, RooAbsReal& _m0, RooAbsReal& _c, RooAbsReal& _p) :
  RooAbsPdf(name, title), 
  m("m","Mass",this,_m),
  m0("m0","Resonance mass",this,_m0),
  c("c","Slope parameter",this,_c),
  p("p","Power",this,_p),
  m_min(m.min()),
  m_max(m.max()),
  norm(0)
{
}

RooArgusBG::RooArgusBG(const RooArgusBG& other, const char* name) :
  RooAbsPdf(other,name), 
  m("m",this,other.m), 
  m0("m0",this,other.m0), 
  c("c",this,other.c),
  p("p",this,other.p),
  m_min(other.m_min),
  m_max(other.m_max),
  norm(0)
{
}


Double_t RooArgusBG::evaluate() const {

  assert(m0>1.88);
  assert(m0<1.895);

  if (c!=c_save||p!=p_save||norm==0){

//     std::cout << "New evaluation c="<<c<<" p="<<p<<std::endl;

    delete norm;
    c_save=c;
    p_save=p;

    int nbin=20;

    norm=new RooParmFcn("Argus normalization",nbin,1.88,1.895);

    for(int i=0;i<=nbin;i++){

      double m0=norm->getX(i);

      double integ=0.0;
      
      int ndm=640000;

      double mmax=m0;
      if (m.max()<m0) mmax=m.max();

      double dm=(mmax-m.min())/ndm;

      for (int j=0;j<ndm;j++){
	double x=m.min()+dm*(j+0.5);
	Double_t t= x/m0;
	Double_t u= 1 - t*t;
	integ+=dm*x*pow(u,p)*exp(c*u);
      }

      assert(integ==integ);
      
      norm->set(i,integ);

    }

    // cout << "Done!"<<endl;

  }


  Double_t t= m/m0;
  if(t >= 1) return 0;

  Double_t u= 1 - t*t;
  return m*pow(u,p)*exp(c*u)/norm->getVal(m0) ;
//  return m*pow(u,p)*exp(c*u);
}


Int_t RooArgusBG::getAnalyticalIntegral(RooArgSet& allVars, RooArgSet& analVars, const char* rangeName) const
{
//   return 0;
  //std::cout << "Asking to do integral in RooArgusBG"<<std::endl;

  if (m_min!=m.min()) {
    std::cout << "m.min changed to:"<<m.min()<<"  from "<<m_min<<std::endl;
    return 0;
  }
  if (m_max!=m.max()) {
    std::cout << "m.max changed to:"<<m.max()<<"  from "<<m_max<<std::endl;
    return 0;
  }

  if (matchArgs(allVars,analVars,m)) { 
     //std::cout << "Returning analytic integral!" << std::endl; 
     return 1; }
 
  return 0;

}


Double_t RooArgusBG::analyticalIntegral(Int_t code, const char* rangeName) const
{

  //std::cout << "Returning 1 in RooArgusBG"<<std::endl;

  assert(code==1);

  return 1.0;

  //if (area_save>0.0) return area_save;

  //if (c==c_save&&m0==m0_save) return area_save;

  //c_save=c;
  //m0_save=m0;

  //cout << "c,m0:"<<c<<" "<<m0<<endl;
  // Formula for integration over m when p=0.5
  //static const Double_t pi = atan2(0.0,-1.0);
  // Double_t min = (m.min() < m0) ? m.min() : m0;
  //Double_t max = (m.max() < m0) ? m.max() : m0;
  //Double_t f1 = (1.-pow(min/m0,2));
  //Double_t f2 = (1.-pow(max/m0,2));
  // Double_t aLow  = -0.5*m0*m0*(exp(c*f1)*sqrt(f1)/c + 0.5/pow(-c,1.5)*sqrt(pi)*erf(sqrt(-c*f1)));
  //Double_t aHigh = -0.5*m0*m0*(exp(c*f2)*sqrt(f2)/c + 0.5/pow(-c,1.5)*sqrt(pi)*erf(sqrt(-c*f2)));
  //Double_t area = aHigh - aLow;
  //area_save=area;
  //return area;

}


