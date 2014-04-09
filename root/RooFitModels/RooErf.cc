/*****************************************************************************
 * Project: RooFit                                                           *
 * Package: RooFitModels                                                     *
 *    File: $Id: RooErf.cc,v 1.2 2007/07/09 13:08:07 xs32 Exp xs32 $
 * Authors:                                                                  *
 *   WV, Wouter Verkerke, UC Santa Barbara, verkerke@slac.stanford.edu       *
 *   DK, David Kirkby,    UC Irvine,         dkirkby@uci.edu                 *
 *                                                                           *
 * Copyright (c) 2000-2002, Regents of the University of California          *
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

#include "RooFitModels/RooErf.hh"
#include "RooFitCore/RooRealVar.hh"

ClassImp(RooErf)

RooErf::RooErf(const char *name, const char *title,
			       RooAbsReal& _x, RooAbsReal& _m, RooAbsReal& _s) :
  RooAbsPdf(name, title), 
  x("x","Dependent",this,_x),
  m("m","Exponent",this,_m),
  s("s","Exponent",this,_s)
{
}

RooErf::RooErf(const RooErf& other, const char* name) :
  RooAbsPdf(other, name), x("x",this,other.x), m("m",this,other.m), s("s",this,other.s)
{
}

Double_t RooErf::evaluate() const{
  return 1.0+TMath::Erf((x-m)/s);
}

Int_t RooErf::getAnalyticalIntegral(RooArgSet& allVars, RooArgSet& analVars, const char*) const 
{
  return 0 ;
  if (matchArgs(allVars,analVars,x)) return 1 ;
}

Double_t RooErf::analyticalIntegral(Int_t code, const char*) const 
{
  switch(code) {
  case 1: 
    {
      static double invsqrtpi=1.0/sqrt(4*atan(1.0));
      return (x.max()-x.min())+s*((x.max()-m)*TMath::Erf((x.max()-m)/s)+
		invsqrtpi*exp(-((x.max()-m)*(x.max()-m)/(2.0*s*s)))
		-(x.min()-m)*TMath::Erf((x.min()-m)/s)-
		invsqrtpi*exp(-((x.min()-m)*(x.min()-m)/(2.0*s*s))));
    }
  }
  
  assert(0) ;
  return 0 ;
}

