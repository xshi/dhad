/*****************************************************************************
 * Project: RooFit                                                           *
 * Package: RooFitCore                                                       *
 *    File: $Id: RooAbsIntegrator.cc,v 1.16 2005/02/25 14:22:50 wverkerke Exp $
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

// -- CLASS DESCRIPTION [AUX] --
// RooAbsIntegrator is the abstract interface for integrating real-valued
// functions that implement the RooAbsFunc interface.

#include "RooFitCore/RooAbsIntegrator.hh"
#include "TClass.h"
using std::cout;
using std::endl;

ClassImp(RooAbsIntegrator)
;

RooAbsIntegrator::RooAbsIntegrator() : _function(0), _valid(kFALSE), _printEvalCounter(kFALSE) 
{
}

RooAbsIntegrator::RooAbsIntegrator(const RooAbsFunc& function, Bool_t printEvalCounter) :
  _function(&function), _valid(function.isValid()), _printEvalCounter(printEvalCounter)
{
}

Double_t RooAbsIntegrator::calculate(const Double_t *yvec) 
{
  if (_printEvalCounter) integrand()->resetNumCall() ;
  Double_t ret = integral(yvec) ; 
  if (_printEvalCounter) {
    cout << IsA()->GetName() << "::calculate() number of function calls = " << integrand()->numCall() << endl ;
  }
  return ret ;
}
