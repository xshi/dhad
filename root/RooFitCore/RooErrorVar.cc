/*****************************************************************************
 * Project: RooFit                                                           *
 * Package: RooFitCore                                                       *
 *    File: $Id: RooErrorVar.cc,v 1.13 2005/02/25 14:22:56 wverkerke Exp $
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
// RooErrorVar is an auxilary class that represents the error
// of a RooRealVar as a seperate object. The main reason of
// existence of this class is to facilitate the reuse of existing
// techniques to perform calculations that involve a RooRealVars
// error, such as calculating the pull value.
//

#include "RooFitCore/RooErrorVar.hh"
#include "RooFitCore/RooAbsBinning.hh"
#include "RooFitCore/RooStreamParser.hh"
#include "RooFitCore/RooRangeBinning.hh"
using std::cout;
using std::endl;
using std::istream;
using std::ostream;

ClassImp(RooErrorVar)
;


RooErrorVar::RooErrorVar(const char *name, const char *title, const RooRealVar& input) :
  RooAbsRealLValue(name,title),
  _realVar("realVar","RooRealVar with error",this,(RooAbsReal&)input)
{
  _binning = new RooUniformBinning(-1,1,100) ;
  // Constuctor
}


RooErrorVar::RooErrorVar(const RooErrorVar& other, const char* name) :
  RooAbsRealLValue(other,name),
  _realVar("realVar",this,other._realVar)
{
  _binning = other._binning->clone() ;

  // Copy constructor
  TIterator* iter = other._altBinning.MakeIterator() ;
  RooAbsBinning* binning ;
  while(binning=(RooAbsBinning*)iter->Next()) {
    _altBinning.Add(binning->clone()) ;
  }
  delete iter ;
}



RooErrorVar::~RooErrorVar()
{
  // Destructor 
  delete _binning ;
}



Bool_t RooErrorVar::hasBinning(const char* name) const
{
  return _altBinning.FindObject(name) ? kTRUE : kFALSE ;
}


const RooAbsBinning& RooErrorVar::getBinning(const char* name, Bool_t verbose) const 
{
  return const_cast<RooErrorVar*>(this)->getBinning(name,verbose) ;
}


RooAbsBinning& RooErrorVar::getBinning(const char* name, Bool_t verbose) 
{
  // Return default (normalization) binning and range if no name is specified
  if (name==0) {
    return *_binning ;
  }
  
  // Check if binning with this name has been created already
  RooAbsBinning* binning = (RooAbsBinning*) _altBinning.FindObject(name) ;
  if (binning) {
    return *binning ;
  }

  // Create a new RooRangeBinning with this name with default range
  binning = new RooRangeBinning(getMin(),getMax(),name) ;
  if (verbose) {
    cout << "RooErrorVar::getBinning(" << GetName() << ") new range named '" 
	 << name << "' created with default bounds" << endl ;
  }

  _altBinning.Add(binning) ;

  return *binning ;
}



void RooErrorVar::setBinning(const RooAbsBinning& binning, const char* name) 
{
  if (!name) {
    if (_binning) delete _binning ;
    _binning = binning.clone() ;
  } else {

    // Remove any old binning with this name
    RooAbsBinning* oldBinning = (RooAbsBinning*) _altBinning.FindObject(name) ;
    if (oldBinning) {
      _altBinning.Remove(oldBinning) ;
      delete oldBinning ;
    }

    // Insert new binning in list of alternative binnings
    RooAbsBinning* newBinning = binning.clone() ;
    newBinning->SetName(name) ;
    newBinning->SetTitle(name) ;
    _altBinning.Add(newBinning) ;

  }
  

}


void RooErrorVar::setMin(const char* name, Double_t value) 
{
  // Set new minimum of fit range 
  RooAbsBinning& binning = getBinning(name) ;

  // Check if new limit is consistent
  if (value >= getMax()) {
    cout << "RooErrorVar::setMin(" << GetName() 
	 << "): Proposed new fit min. larger than max., setting min. to max." << endl ;
    binning.setMin(getMax()) ;
  } else {
    binning.setMin(value) ;
  }

  // Clip current value in window if it fell out
  if (!name) {
    Double_t clipValue ;
    if (!inRange(_value,&clipValue)) {
      setVal(clipValue) ;
    }
  }
    
  setShapeDirty() ;
}

void RooErrorVar::setMax(const char* name, Double_t value)
{
  // Set new maximum of fit range 
  RooAbsBinning& binning = getBinning(name) ;

  // Check if new limit is consistent
  if (value < getMin()) {
    cout << "RooErrorVar::setMax(" << GetName() 
	 << "): Proposed new fit max. smaller than min., setting max. to min." << endl ;
    binning.setMax(getMin()) ;
  } else {
    binning.setMax(value) ;
  }

  // Clip current value in window if it fell out
  if (!name) {
    Double_t clipValue ;
    if (!inRange(_value,&clipValue)) {
      setVal(clipValue) ;
    }
  }

  setShapeDirty() ;
}


void RooErrorVar::setRange( const char* name, Double_t min, Double_t max) 
{
  Bool_t exists = name ? (_altBinning.FindObject(name)?kTRUE:kFALSE) : kTRUE ;

  // Set new fit range 
  RooAbsBinning& binning = getBinning(name,kFALSE) ;

  // Check if new limit is consistent
  if (min>max) {
    cout << "RooErrorVar::setRange(" << GetName() 
	 << "): Proposed new fit max. smaller than min., setting max. to min." << endl ;
    binning.setRange(min,min) ;
  } else {
    binning.setRange(min,max) ;
  }

  if (!exists) {
    cout << "RooErrorVar::setRange(" << GetName() 
	 << ") new range named '" << name << "' created with bounds [" 
	 << min << "," << max << "]" << endl ;
  }

  setShapeDirty() ;  
}


Bool_t RooErrorVar::readFromStream(istream& is, Bool_t compact, Bool_t verbose) 
{
  // Read object contents from given stream

  TString token,errorPrefix("RooErrorVar::readFromStream(") ;
  errorPrefix.Append(GetName()) ;
  errorPrefix.Append(")") ;
  RooStreamParser parser(is,errorPrefix) ;
  Double_t value(0) ;

    // Compact mode: Read single token
  if (parser.readDouble(value,verbose)) return kTRUE ;
  if (isValidReal(value,verbose)) {
    setVal(value) ;
    return kFALSE ;
  } else {
    return kTRUE ;
  }
}


void RooErrorVar::writeToStream(ostream& os, Bool_t compact) const
{
  // Write value only
  os << getVal() ;
}
