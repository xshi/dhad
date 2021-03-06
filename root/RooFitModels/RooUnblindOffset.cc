/*****************************************************************************
 * Project: RooFit                                                           *
 * Package: RooFitModels                                                     *
 *    File: $Id: RooUnblindOffset.cc,v 1.9 2005/02/25 14:25:06 wverkerke Exp $
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

// -- CLASS DESCRIPTION [REAL] --
//
// Implementation of BlindTools' offset blinding method
// A RooUnblindOffset object is a real valued function
// object, constructed from a blind value holder and a 
// set of unblinding parameters. When supplied to a PDF
// in lieu of a regular parameter, the blind value holder
// supplied to the unblinder objects will in a fit be minimized 
// to blind value corresponding to the actual minimum of the
// parameter. The transformation is chosen such that the
// the error on the blind parameters is indentical to that
// of the unblind parameter

#include "RooFitCore/RooArgSet.hh"
#include "RooFitModels/RooUnblindOffset.hh"


ClassImp(RooUnblindOffset)
;


RooUnblindOffset::RooUnblindOffset() : _blindEngine("") 
{
  // Default constructor
}


RooUnblindOffset::RooUnblindOffset(const char *name, const char *title,
					 const char *blindString, Double_t scale, RooAbsReal& cpasym)
  : RooAbsHiddenReal(name,title), 
  _value("value","Offset blinded value",this,cpasym),
  _blindEngine(blindString,RooBlindTools::full,0.,scale) 
{  
  // Constructor from a given RooAbsReal (to hold the blind value) and a set of blinding parameters
}

RooUnblindOffset::RooUnblindOffset(const char *name, const char *title,
				   const char *blindString, Double_t scale, RooAbsReal& cpasym,
				   RooAbsCategory& blindState)
  : RooAbsHiddenReal(name,title,blindState),
    _value("value","Offset blinded value",this,cpasym), 
    _blindEngine(blindString,RooBlindTools::full,0.,scale)
{  
  // Constructor from a given RooAbsReal (to hold the blind value) and a set of blinding parameters
}


RooUnblindOffset::RooUnblindOffset(const RooUnblindOffset& other, const char* name) : 
  RooAbsHiddenReal(other, name), 
  _value("asym",this,other._value),
  _blindEngine(other._blindEngine) 
{
  // Copy constructor

}


RooUnblindOffset::~RooUnblindOffset() 
{
  // Destructor
}


Double_t RooUnblindOffset::evaluate() const
{
  // Evaluate RooBlindTools unhide-offset method on blind value

  if (isHidden()) {
    // Blinding is active for this event
    return _blindEngine.UnHideOffset(_value);
  } else {
    // Blinding is not active for this event
    return _value ;
  }
}





