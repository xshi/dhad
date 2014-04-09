/*****************************************************************************
 * Project: RooFit                                                           *
 * Package: RooFitModels                                                     *
 *    File: $Id: RooGaussian.cc,v 1.23 2005/02/25 14:25:06 wverkerke Exp $
 * Authors:                                                                  *
 *   WV, Wouter Verkerke, UC Santa Barbara, verkerke@slac.stanford.edu       *
 *   DK, David Kirkby,    UC Irvine,         dkirkby@uci.edu                 *
 *                                                                           *
 * Copyright (c) 2000-2005, Regents of the University of California          *
 *                          and Stanford University. All rights reserved.    *
 *                                                                           *
 * Redistribution and use in source and binary forms,                        *
 * with or without modification, are permitted according to the terms        *
 * listed in LICENSE (http://roofit.sourceforge.net/license.txt)             *
 *****************************************************************************/

// -- CLASS DESCRIPTION [PDF] --
// Gaussian PDF...

#include <iostream>
#include <math.h>
using std::cout ;
using std::endl ;

#include "RooFitModels/RooGaussian.hh"
#include "RooFitCore/RooAbsReal.hh"
#include "RooFitCore/RooRealVar.hh"
#include "RooFitCore/RooRandom.hh"

ClassImp(RooGaussian)

RooGaussian::RooGaussian(const char *name, const char *title,
			 RooAbsReal& _x, RooAbsReal& _mean,
			 RooAbsReal& _sigma) :
  RooAbsPdf(name,title),
  x("x","Dependent",this,_x),
  mean("mean","Mean",this,_mean),
  sigma("sigma","Width",this,_sigma)
{
}


RooGaussian::RooGaussian(const RooGaussian& other, const char* name) : 
  RooAbsPdf(other,name), x("x",this,other.x), mean("mean",this,other.mean),
  sigma("sigma",this,other.sigma)
{
}


Double_t RooGaussian::evaluate() const
{
  Double_t arg= x - mean;  
  return exp(-0.5*arg*arg/(sigma*sigma)) ;
}



Int_t RooGaussian::getAnalyticalIntegral(RooArgSet& allVars, RooArgSet& analVars, const char* rangeName) const 
{
  if (matchArgs(allVars,analVars,x)) return 1 ;
  return 0 ;
}



Double_t RooGaussian::analyticalIntegral(Int_t code, const char* rangeName) const 
{
  assert(code==1) ;

  static const Double_t root2 = sqrt(2.) ;
  static const Double_t rootPiBy2 = sqrt(atan2(0.0,-1.0)/2.0);
  
  Double_t xscale = root2*sigma;
  return rootPiBy2*sigma*(erf((x.max(rangeName)-mean)/xscale)-erf((x.min(rangeName)-mean)/xscale));
}




Int_t RooGaussian::getGenerator(const RooArgSet& directVars, RooArgSet &generateVars, Bool_t staticInitOK) const
{
  if (matchArgs(directVars,generateVars,x)) return 1 ;  
  return 0 ;
}


void RooGaussian::generateEvent(Int_t code)
{
  assert(code==1) ;
  Double_t xgen ;
  while(1) {    
    xgen = RooRandom::randomGenerator()->Gaus(mean,sigma);
    if (xgen<x.max() && xgen>x.min()) {
      x = xgen ;
      break;
    }
  }
  return;
}


