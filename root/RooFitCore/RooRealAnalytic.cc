/*****************************************************************************
 * Project: RooFit                                                           *
 * Package: RooFitCore                                                       *
 *    File: $Id: RooRealAnalytic.cc,v 1.13 2005/02/25 14:23:01 wverkerke Exp $
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
// Lightweight interface adaptor that binds an analytic integral of a
// RooAbsReal object (specified by a code) to a set of dependent variables.


#include "RooFitCore/RooRealAnalytic.hh"
#include "RooFitCore/RooAbsReal.hh"

#include <assert.h>

ClassImp(RooRealAnalytic)
;

Double_t RooRealAnalytic::operator()(const Double_t xvector[]) const {
  // Evaluate our analytic integral at the specified values of the dependents.
  assert(isValid());
  loadValues(xvector);  
  _ncall++ ;
  return _code?_func->analyticalIntegralWN(_code,_nset,_rangeName?_rangeName->GetName():0):_func->getVal(_nset) ;
}
