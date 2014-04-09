/*****************************************************************************
 * Project: RooFit                                                           *
 * Package: RooFitCore                                                       *
 *    File: $Id: RooSuperCategory.cc,v 1.22 2005/02/25 14:23:03 wverkerke Exp $
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
// RooSuperCategory consolidates several RooAbsCategoryLValue objects into
// a single category. The states of the super category consist of all the permutations
// of the input categories. The super category is an lvalue itself and a modification
// of its state will back propagate into a modification of its input categories.
//
// RooSuperCategory state are automatically defined and updated whenever an input
// category modifies its list of states

#include <iostream>
#include <stdlib.h>
#include <stdio.h>
#include "TString.h"
#include "RooFitCore/RooSuperCategory.hh"
#include "RooFitCore/RooStreamParser.hh"
#include "RooFitCore/RooArgSet.hh"
#include "RooFitCore/RooMultiCatIter.hh"
#include "RooFitCore/RooAbsCategoryLValue.hh"
using std::cout;
using std::endl;
using std::istream;
using std::ostream;

ClassImp(RooSuperCategory)
;

RooSuperCategory::RooSuperCategory(const char *name, const char *title, const RooArgSet& inputCatList) :
  RooAbsCategoryLValue(name, title), _catSet("catSet","Input category set",this,kTRUE,kTRUE)
{  
  // Constructor from list of input categories

  // Copy category list
  TIterator* iter = inputCatList.createIterator() ;
  RooAbsArg* arg ;
  while (arg=(RooAbsArg*)iter->Next()) {
    if (!arg->IsA()->InheritsFrom(RooAbsCategoryLValue::Class())) {
      cout << "RooSuperCategory::RooSuperCategory(" << GetName() << "): input category " << arg->GetName() 
	   << " is not an lvalue" << endl ;
    }
    _catSet.add(*arg) ;
  }
  delete iter ;
  
  updateIndexList() ;
}


RooSuperCategory::RooSuperCategory(const RooSuperCategory& other, const char *name) :
  RooAbsCategoryLValue(other,name), _catSet("catSet",this,other._catSet)
{
  // Copy constructor

  updateIndexList() ;
  setIndex(other.getIndex()) ;
}



RooSuperCategory::~RooSuperCategory() 
{
  // Destructor
}



TIterator* RooSuperCategory::MakeIterator() const 
{
  // Make an iterator over all state permutations of 
  // the input categories of this supercategory
  return new RooMultiCatIter(_catSet) ;
}



void RooSuperCategory::updateIndexList()
{
  // Update the list of super-category states 
  clearTypes() ;
//   RooArgSet* catListClone = (RooArgSet*) _catSet.snapshot(kTRUE) ;

  RooMultiCatIter mcIter(_catSet) ;
  TObjString* obj ;
  Int_t i(0) ;
  while(obj = (TObjString*) mcIter.Next()) {
    // Register composite label
    defineTypeUnchecked(obj->String(),i++) ;
  }
//   _catSet = *catListClone ;
//   delete catListClone ;

  // Renumbering will invalidate cache
  setValueDirty() ;
}


TString RooSuperCategory::currentLabel() const
{
  // Return the name of the current state, 
  // constructed from the state names of the input categories

  TIterator* lIter = _catSet.createIterator() ;

  // Construct composite label name
  TString label ;
  RooAbsCategory* cat ;
  Bool_t first(kTRUE) ;
  while(cat=(RooAbsCategory*) lIter->Next()) {
    label.Append(first?"{":";") ;
    label.Append(cat->getLabel()) ;      
    first=kFALSE ;
  }
  label.Append("}") ;  
  delete lIter ;

  return label ;
}


RooCatType
RooSuperCategory::evaluate() const
{
  // Calculate the current value 
  if (isShapeDirty()) {
    const_cast<RooSuperCategory*>(this)->updateIndexList() ;
  }
  const RooCatType* ret = lookupType(currentLabel(),kTRUE) ;
  if (!ret) {
    cout << "RooSuperCat::evaluate(" << this << ") error: current state not defined: '" << currentLabel() << "'" << endl ;
    Print("v") ;
  }
  return *ret ;
}


Bool_t RooSuperCategory::setIndex(Int_t index, Bool_t printError) 
{
  // Set the value of the super category by specifying the state index code
  // Indirectly sets the values of the input categories
  const RooCatType* type = lookupType(index,kTRUE) ;
  if (!type) return kTRUE ;
  return setType(type) ;
}


Bool_t RooSuperCategory::setLabel(const char* label, Bool_t printError) 
{
  // Set the value of the super category by specifying the state name
  // Indirectly sets the values of the input categories
  const RooCatType* type = lookupType(label,kTRUE) ;
  if (!type) return kTRUE ;
  return setType(type) ;
}


Bool_t RooSuperCategory::setType(const RooCatType* type, Bool_t printError)
{
  // Set the value of the super category by specifying the state object
  // Indirectly sets the values of the input categories

  char buf[1024] ;
  strcpy(buf,type->GetName()) ;

  TIterator* iter = _catSet.createIterator() ;
  RooAbsCategoryLValue* arg ;
  Bool_t error(kFALSE) ;

  // Parse composite label and set label of components to their values  
  char* ptr=buf+1 ;
  char* token = ptr ;
  while (arg=(RooAbsCategoryLValue*)iter->Next()) {

    // Delimit name token for this category
    if (*ptr=='{') {
      // Token is composite itself, terminate at matching '}'
      Int_t nBrak(1) ;
      while(*(++ptr)) {
	if (nBrak==0) {
	  *ptr = 0 ;
	  break ;
	}
	if (*ptr=='{') {
	  nBrak++ ;
	} else if (*ptr=='}') {
	  nBrak-- ;
	}
      }	
    } else {
      // Simple token, terminate at next semi-colon
      ptr = strtok(ptr,";}") ;
      ptr += strlen(ptr) ;
    }

    error |= arg->setLabel(token) ;
    token = ++ptr ;
  }
  
  delete iter ;
  return error ;
}



void RooSuperCategory::printToStream(ostream& os, PrintOption opt, TString indent) const
{
  // Print the state of this object to the specified output stream.

  RooAbsCategory::printToStream(os,opt,indent) ;
  
  if (opt>=Verbose) {     
    os << indent << "--- RooSuperCategory ---" << endl;
    os << indent << "  Input category list:" << endl ;
    TString moreIndent(indent) ;
    moreIndent.Append("   ") ;
    _catSet.printToStream(os,Standard,moreIndent.Data()) ;
  }
}


Bool_t RooSuperCategory::readFromStream(istream& is, Bool_t compact, Bool_t verbose) 
{
  // Read object contents from given stream
  return kTRUE ;
}



void RooSuperCategory::writeToStream(ostream& os, Bool_t compact) const
{
  // Write object contents to given stream
  RooAbsCategory::writeToStream(os,compact) ;
}
