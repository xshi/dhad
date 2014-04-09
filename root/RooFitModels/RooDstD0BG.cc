/*****************************************************************************
 * Project: RooFit                                                           *
 * Package: RooFitModels                                                     *
 *    File: $Id: RooDstD0BG.cc,v 1.14 2005/02/25 14:25:04 wverkerke Exp $
 * Authors:                                                                  *
 *   UE, Ulrik Egede,     RAL,               U.Egede@rl.ac.uk                *
 *   MT, Max Turri,       UC Santa Cruz      turri@slac.stanford.edu         *
 *   CC, Chih-hsiang Cheng, Stanford         chcheng@slac.stanford.edu       *
 *   DK, David Kirkby,    UC Irvine,         dkirkby@uci.edu                 *
 *                                                                           *
 * Copyright (c) 2000-2005, Regents of the University of California          *
 *                          RAL and Stanford University. All rights reserved.*
 *                                                                           *
 * Redistribution and use in source and binary forms,                        *
 * with or without modification, are permitted according to the terms        *
 * listed in LICENSE (http://roofit.sourceforge.net/license.txt)             *
 *****************************************************************************/

// -- CLASS DESCRIPTION [PDF] --

#include <iostream>
#include <math.h>

#include "RooFitModels/RooDstD0BG.hh"
#include "RooFitCore/RooAbsReal.hh"
#include "RooFitCore/RooRealVar.hh"
#include "RooFitCore/RooIntegrator1D.hh"
#include "RooFitCore/RooAbsFunc.hh"

ClassImp(RooDstD0BG) 

static const char rcsid[] =
"$Id: RooDstD0BG.cc,v 1.14 2005/02/25 14:25:04 wverkerke Exp $";

RooDstD0BG::RooDstD0BG(const char *name, const char *title,
		       RooAbsReal& _dm, RooAbsReal& _dm0,
		       RooAbsReal& _c, RooAbsReal& _a, RooAbsReal& _b) :
  RooAbsPdf(name,title),
  dm("dm","Dstar-D0 Mass Diff",this, _dm),
  dm0("dm0","Threshold",this, _dm0),
  c("c","Shape Parameter",this, _c),
  a("a","Shape Parameter 2",this, _a),
  b("b","Shape Parameter 3",this, _b)
{
}

RooDstD0BG::RooDstD0BG(const RooDstD0BG& other, const char *name) :
  RooAbsPdf(other,name), dm("dm",this,other.dm), dm0("dm0",this,other.dm0),
  c("c",this,other.c), a("a",this,other.a), b("b",this,other.b)
{
}

Double_t RooDstD0BG::evaluate() const
{
  Double_t arg= dm- dm0;
  if (arg <= 0 ) return 0;
  Double_t ratio= dm/dm0;
  Double_t val= (1- exp(-arg/c))* pow(ratio, a) + b*(ratio-1);

  return (val > 0 ? val : 0) ;
}

Int_t RooDstD0BG::getAnalyticalIntegral(RooArgSet& allVars, RooArgSet& analVars, const char* rangeName) const 
{
  // if (matchArgs(allVars,analVars,dm)) return 1 ;
  return 0 ;
}

Double_t RooDstD0BG::analyticalIntegral(Int_t code, const char* rangeName) const 
{
  switch(code) {
  case 1: 
    {
      Double_t min= dm.min(rangeName);
      Double_t max= dm.max(rangeName);
      if (max <= dm0 ) return 0;
      else if (min < dm0) min = dm0;

      Bool_t doNumerical= kFALSE;
      if ( a != 0 ) doNumerical= kTRUE;
      else if (b < 0) {
	// If b<0, pdf can be negative at large dm, the integral should
	// only up to where pdf hits zero. Better solution should be
	// solve the zero and use it as max. 
	// Here we check this whether pdf(max) < 0. If true, let numerical
	// integral take care of. ( kind of ugly!)
	if ( 1- exp(-(max-dm0)/c) + b*(max/dm0 -1) < 0) doNumerical= kTRUE;
      }
      if ( ! doNumerical ) {
	return (max-min)+ c* exp(dm0/c)* (exp(-max/c)- exp(-min/c)) +
	  b* (0.5* (max*max - min*min)/dm0 - (max- min));
      } else {
	// In principle the integral for a!=0  can be done analytically. 
	// It involves incomplete Gamma function, TMath::Gamma(a+1,m/c), 
	// which is not defined for a < -1. And the whole expression is 
	// not stable for m/c >> 1.
	// Do numerical integral
	RooArgSet vset(dm.arg(),"vset");
	RooAbsFunc *func= bindVars(vset);
	RooIntegrator1D integrator(*func,min,max);
	return integrator.integral();
      }
    }
  }
  
  assert(0) ;
  return 0 ;
}
