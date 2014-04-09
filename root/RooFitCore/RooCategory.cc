/*****************************************************************************
 * Project: RooFit                                                           *
 * Package: RooFitCore                                                       *
 *    File: $Id: RooCategory.cc,v 1.24 2005/02/25 14:22:54 wverkerke Exp $
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

// -- CLASS DESCRIPTION [CAT] --
// RooCategory represents a fundamental (non-derived) discrete value object. The class
// has a public interface to define the possible value states.


#include <iostream>
#include <stdlib.h>
#include <string.h>
#include "TTree.h"
#include "TString.h"
#include "TH1.h"
#include "RooFitCore/RooCategory.hh"
#include "RooFitCore/RooArgSet.hh"
#include "RooFitCore/RooStreamParser.hh"
using std::cout;
using std::endl;
using std::istream;
using std::ostream;

ClassImp(RooCategory) 
;


RooCategory::RooCategory(const char *name, const char *title) : 
  RooAbsCategoryLValue(name,title)
{
  // Constructor. Types must be defined using defineType() before variable can be used
  setValueDirty() ;  
  setShapeDirty() ;  
}


RooCategory::RooCategory(const RooCategory& other, const char* name) :
  RooAbsCategoryLValue(other, name)
{
  // Copy constructor
}


RooCategory::~RooCategory()
{
  // Destructor
}



Bool_t RooCategory::setIndex(Int_t index, Bool_t printError) 
{
  // Set value by specifying the index code of the desired state.
  // If printError is set, a message will be printed if
  // the specified index does not represent a valid state.

  const RooCatType* type = lookupType(index,printError) ;
  if (!type) return kTRUE ;
  _value = *type ;
  setValueDirty() ;
  return kFALSE ;
}



Bool_t RooCategory::setLabel(const char* label, Bool_t printError) 
{
  // Set value by specifying the name of the desired state
  // If printError is set, a message will be printed if
  // the specified label does not represent a valid state.

  const RooCatType* type = lookupType(label,printError) ;
  if (!type) return kTRUE ;
  _value = *type ;
  setValueDirty() ;
  return kFALSE ;
}



Bool_t RooCategory::defineType(const char* label) 
{ 
  // Define a state with given name, the lowest available
  // positive integer is assigned as index. Category
  // state labels may not contain semicolons.
  // Error status is return if state with given name
  // is already defined

  if (TString(label).Contains(";")) {
  cout << "RooCategory::defineType(" << GetName() 
       << "): semicolons not allowed in label name" << endl ;
  return kTRUE ;
  }

  return RooAbsCategory::defineType(label)?kFALSE:kTRUE ; 
}


Bool_t RooCategory::defineType(const char* label, Int_t index) 
{
  // Define a state with given name and index. Category
  // state labels may not contain semicolons
  // Error status is return if state with given name
  // or index is already defined

  if (TString(label).Contains(";")) {
  cout << "RooCategory::defineType(" << GetName() 
       << "): semicolons not allowed in label name" << endl ;
  return kTRUE ;
  }

  return RooAbsCategory::defineType(label,index)?kFALSE:kTRUE ; 
}


Bool_t RooCategory::readFromStream(istream& is, Bool_t compact, Bool_t verbose) 
{
  // Read object contents from given stream

  // Read single token
  RooStreamParser parser(is) ;
  TString token = parser.readToken() ;

  return setLabel(token,verbose) ;
}



void RooCategory::writeToStream(ostream& os, Bool_t compact) const
{
  // compact only at the moment
  if (compact) {
    os << getIndex() ;
  } else {
    os << getLabel() ;
  }
}




