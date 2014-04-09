/*****************************************************************************
 * Project: RooFit                                                           *
 * Package: RooFitCore                                                       *
 *    File: $Id: RooAbsString.cc,v 1.28 2005/02/25 14:22:52 wverkerke Exp $
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

// -- CLASS DESCRIPTION [MISC] --
// RooAbsString is the common abstract base class for objects that represent a
// string value
// 
// Implementation of RooAbsString may be derived, there no interface
// is provided to modify the contents
// 

#include <iostream>
#include "TObjString.h"
#include "TH1.h"
#include "TTree.h"

#include "RooFitCore/RooArgSet.hh"
#include "RooFitCore/RooAbsString.hh"
#include "RooFitCore/RooStringVar.hh"
using std::cout;
using std::endl;
using std::istream;
using std::ostream;

ClassImp(RooAbsString) 
;


RooAbsString::RooAbsString() : RooAbsArg(), _len(128) , _value(new char[128])
{
}


RooAbsString::RooAbsString(const char *name, const char *title, Int_t bufLen) : 
  RooAbsArg(name,title), _len(bufLen), _value(new char[bufLen]) 
{
  // Constructor
  setValueDirty() ;
  setShapeDirty() ;
}



RooAbsString::RooAbsString(const RooAbsString& other, const char* name) : 
  RooAbsArg(other, name), _len(other._len), _value(new char[other._len])
{
  // Copy constructor
  strcpy(_value,other._value) ;
}



RooAbsString::~RooAbsString()
{
  delete[] _value ;
  // Destructor
}


const char* RooAbsString::getVal() const
{
  // Return value of object. Calculated if dirty, otherwise cached value is returned.
  if (isValueDirty()) {
    clearValueDirty() ;
    strcpy(_value,traceEval()) ;
  } 
  
  return _value ;
}



Bool_t RooAbsString::operator==(const char* value) const
{
  // Equality operator comparing with a TString
  return !TString(getVal()).CompareTo(value) ;
}



Bool_t RooAbsString::operator==(const RooAbsArg& other) 
{
  const RooAbsString* otherString = dynamic_cast<const RooAbsString*>(&other) ;
  return otherString ? operator==(otherString->getVal()) : kFALSE ;
}




Bool_t RooAbsString::readFromStream(istream& is, Bool_t compact, Bool_t verbose) 
{
  //Read object contents from stream (dummy for now)
  return kFALSE ;
} 

void RooAbsString::writeToStream(ostream& os, Bool_t compact) const
{
  //Write object contents to stream (dummy for now)
}


void RooAbsString::printToStream(ostream& os, PrintOption opt, TString indent) const
{
  //Print object contents
  os << "RooAbsString: " << GetName() << " = " << getVal();
  os << " : \"" << fTitle << "\"" ;

  printAttribList(os) ;
  os << endl ;
}



Bool_t RooAbsString::isValid() const 
{
  // Check if current value is valid
  return isValidString(getVal()) ;
}


Bool_t RooAbsString::isValidString(const char* value, Bool_t printError) const 
{
  // Check if given value is valid

  // Protect against string overflows
  if (TString(value).Length()>_len) return kFALSE ;

  return kTRUE ;
}



const char* RooAbsString::traceEval() const
{
  // Calculate current value of object, with error tracing wrapper
  const char* value = evaluate() ;
  
  //Standard tracing code goes here
  if (!isValidString(value)) {
    cout << "RooAbsString::traceEval(" << GetName() << "): new output too long (>" << _len << " chars): " << value << endl ;
  }

  //Call optional subclass tracing code
  traceEvalHook(value) ;

  return value ;
}



void RooAbsString::copyCache(const RooAbsArg* source) 
{
  // Copy cache of another RooAbsArg to our cache

  // Warning: This function copies the cached values of source,
  //          it is the callers responsibility to make sure the cache is clean

  RooAbsString* other = dynamic_cast<RooAbsString*>(const_cast<RooAbsArg*>(source)) ;
  assert(other!=0) ;

  strcpy(_value,other->_value) ;
  setValueDirty() ;
}



void RooAbsString::attachToTree(TTree& t, Int_t bufSize)
{
  // Attach object to a branch of given TTree

  // First determine if branch is taken
  TBranch* branch ;
  if (branch = t.GetBranch(GetName())) {
    t.SetBranchAddress(GetName(),_value) ;
    if (branch->GetCompressionLevel()<0) {
      cout << "RooAbsString::attachToTree(" << GetName() << ") Fixing compression level of branch " << GetName() << endl ;
      branch->SetCompressionLevel(1) ;
    }
  } else {
    TString format(GetName());
    format.Append("/C");
    branch = t.Branch(GetName(), _value, (const Text_t*)format, bufSize);
    branch->SetCompressionLevel(1) ;
  }
}
 


void RooAbsString::fillTreeBranch(TTree& t) 
{
  // First determine if branch is taken
  TBranch* branch = t.GetBranch(GetName()) ;
  if (!branch) { 
    cout << "RooAbsString::fillTreeBranch(" << GetName() << ") ERROR: not attached to tree" << endl ;
    assert(0) ;
  }
  branch->Fill() ;  
}



void RooAbsString::setTreeBranchStatus(TTree& t, Bool_t active) 
{
  // (De)Activate associate tree branch
  TBranch* branch = t.GetBranch(GetName()) ;
  if (branch) { 
    t.SetBranchStatus(GetName(),active?1:0) ;
  }
}



RooAbsArg *RooAbsString::createFundamental(const char* newname) const {
  // Create a RooStringVar fundamental object with our properties.

  RooStringVar *fund= new RooStringVar(newname?newname:GetName(),GetTitle(),"") ; 
  return fund;
}
