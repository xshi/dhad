/*****************************************************************************
 * Project: RooFit                                                           *
 * Package: RooFitModels                                                     *
 *    File: $Id: RooBDecay.cc,v 1.8 2005/02/25 14:25:04 wverkerke Exp $
 * Authors:                                                                  *
 *   PL, Parker C Lund,   UC Irvine                                          *
 *   DK, David Kirkby,    UC Irvine,         dkirkby@uci.edu                 *
 *   WV, Wouter Verkerke, UC Santa Barbara, verkerke@slac.stanford.edu       *
 *                                                                           *
 * Copyright (c) 2000-2005, Regents of the University of California          *
 *                          and Stanford University. All rights reserved.    *
 *                                                                           *
 * Redistribution and use in source and binary forms,                        *
 * with or without modification, are permitted according to the terms        *
 * listed in LICENSE (http://roofit.sourceforge.net/license.txt)             *
 *****************************************************************************/



#include <iostream>
#include "RooFitModels/RooBDecay.hh"
#include "RooFitCore/RooRealVar.hh"
#include "RooFitCore/RooRandom.hh"
using std::cout;
using std::endl;

ClassImp(RooBDecay);

RooBDecay::RooBDecay(const char *name, const char* title, 
	       RooRealVar& t, RooAbsReal& tau, RooAbsReal& dgamma,
	       RooAbsReal& f0, RooAbsReal& f1, RooAbsReal& f2, RooAbsReal& f3, 
	       RooAbsReal& dm, const RooResolutionModel& model, DecayType type) :
  RooAbsAnaConvPdf(name, title, model, t),
  _t("t", "time", this, t),
  _tau("tau", "Average Decay Time", this, tau),
  _dgamma("dgamma", "Delta Gamma", this, dgamma),
  _f0("f0", "Cosh Coefficient", this, f0),
  _f1("f1", "Sinh Coefficient", this, f1),
  _f2("f2", "Cos Coefficient", this, f2),
  _f3("f3", "Sin Coefficient", this, f3),
  _dm("dm", "Delta Mass", this, dm),
  _type(type)

{
  //Constructor
  switch(type)
    {
    case SingleSided:
      _basisCosh = declareBasis("exp(-@0/@1)*cosh(@0*@2/2)", RooArgList(tau,dgamma));
      _basisSinh = declareBasis("exp(-@0/@1)*sinh(@0*@2/2)", RooArgList(tau,dgamma));
      _basisCos = declareBasis("exp(-@0/@1)*cos(@0*@2)",RooArgList(tau, dm));
      _basisSin = declareBasis("exp(-@0/@1)*sin(@0*@2)",RooArgList(tau, dm));
      break;
    case Flipped:
      _basisCosh = declareBasis("exp(@0/@1)*cosh(@0*@2/2)", RooArgList(tau,dgamma));
      _basisSinh = declareBasis("exp(@0/@1)*sinh(@0*@2/2)", RooArgList(tau,dgamma));
      _basisCos = declareBasis("exp(@0/@1)*cos(@0*@2)",RooArgList(tau, dm));
      _basisSin = declareBasis("exp(@0/@1)*sin(@0*@2)",RooArgList(tau, dm));
      break;
    case DoubleSided:
      _basisCosh = declareBasis("exp(-abs(@0)/@1)*cosh(@0*@2/2)", RooArgList(tau,dgamma));
      _basisSinh = declareBasis("exp(-abs(@0)/@1)*sinh(@0*@2/2)", RooArgList(tau,dgamma));
      _basisCos = declareBasis("exp(-abs(@0)/@1)*cos(@0*@2)",RooArgList(tau, dm));
      _basisSin = declareBasis("exp(-abs(@0)/@1)*sin(@0*@2)",RooArgList(tau, dm));
      break;
    }
}
RooBDecay::RooBDecay(const RooBDecay& other, const char* name) :
  RooAbsAnaConvPdf(other, name),
  _t("t", this, other._t),
  _tau("tau", this, other._tau),
  _dgamma("dgamma", this, other._dgamma),
  _f0("f0", this, other._f0),
  _f1("f1", this, other._f1),
  _f2("f2", this, other._f2),
  _f3("f3", this, other._f3),
  _dm("dm", this, other._dm),
  _basisCosh(other._basisCosh),
  _basisSinh(other._basisSinh),
  _basisCos(other._basisCos),
  _basisSin(other._basisSin),
  _type(other._type)
{
  //Copy constructor
}


RooBDecay::~RooBDecay()
{
  //Destructor
}

Double_t RooBDecay::coefficient(Int_t basisIndex) const
{
  if(basisIndex == _basisCosh)
    {  
      return _f0;
    }
  if(basisIndex == _basisSinh)
    {
      return _f1;
    }
  if(basisIndex == _basisCos)
    {
      return _f2;
    }
  if(basisIndex == _basisSin)
    {
      return _f3;
    }

  return 0 ;
}

Int_t RooBDecay::getGenerator(const RooArgSet& directVars, RooArgSet &generateVars, Bool_t staticInitOK) const
{
  if (matchArgs(directVars, generateVars, _t)) return 1;
  return 0;
}

void RooBDecay::generateEvent(Int_t code)
{
  assert(code==1);
  //Generate delta-t dependent
  while(1) {
    Double_t rand = RooRandom::uniform();
    Double_t rand2 = RooRandom::uniform();
    Double_t rand3 = RooRandom::uniform();
    Double_t tval(0);
    Double_t y;
    Double_t f;
    Double_t w;
    Double_t gammamin = 1/_tau-fabs(_dgamma)/2;

 
    // used rejection method with comparison function: w = (1+sqrt(f2*f2+f3*f3))exp(-abs(t)*gammamin)
    // see Numerical Recipes in C for explanation of rejection method

    switch(_type)
      {
      case SingleSided:
	tval = -1/gammamin*log(rand);
	break;
      case Flipped:
	tval = 1/gammamin*log(rand);
	break;
      case DoubleSided:
	if(rand3 > 0.5)
	  {
	    tval = -1/gammamin*log(rand);
	    break;
	  }
	
	if (rand3 <= 0.5)
	  {
	    tval = 1/gammamin*log(rand);
	    break;
	  }
      }
    Double_t dgt = _dgamma*tval/2;
    Double_t dmt = _dm*tval;
    Double_t ftval = fabs(tval);
    
       w = (_f0+sqrt(_f2*_f2+_f3*_f3))*exp(-ftval*gammamin);
    y = w*rand2;
    f = exp(-ftval/_tau)*(_f0*cosh(dgt)+_f1*sinh(dgt)+_f2*cos(dmt)+_f3*sin(dmt));
    if (tval<_t.max() && tval>_t.min())
    {
	if(w < f)
	  {
	    cout << "Error!!!! Comparison function less than f(x)" << endl;
	if(f < 0)
	  {
	    cout << "Error!!!! PDF less than Zero" << endl;
	  }
	  }
	if(w >= f)
	  {
	    if(y < f)
	      {
		_t = tval;
		break;
	      }
	  }
    }
    
  }
}
















































