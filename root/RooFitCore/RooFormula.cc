/*****************************************************************************
 * Project: RooFit                                                           *
 * Package: RooFitCore                                                       *
 *    File: $Id: RooFormula.cc,v 1.50 2005/02/25 14:22:57 wverkerke Exp $
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
// RooFormula is the RFC extension of TFormula. It allows to use
// the value of a given list of RooAbsArg objects in the formula
// expression. Reference is done either by the RooAbsArgs name
// or by list ordinal postion ('@0,@1,...'). State information
// of RooAbsCategories can be accessed used the '::' operator,
// e.g. 'tagCat::Kaon' will resolve to the numerical value of
// the Kaon state of the RooAbsCategory object named tagCat.

#include <iostream>
#include <stdlib.h>
#include "TROOT.h"
#include "TClass.h"
#include "TObjString.h"
#include "RooFitCore/RooFormula.hh"
#include "RooFitCore/RooAbsReal.hh"
#include "RooFitCore/RooAbsCategory.hh"
#include "RooFitCore/RooArgList.hh"
using std::cout;
using std::endl;
using std::ostream;

ClassImp(RooFormula)

RooFormula::RooFormula() : TFormula(), _nset(0)
{
  // Dummy constructor
}

RooFormula::RooFormula(const char* name, const char* formula, const RooArgList& list) : 
  TFormula(), _isOK(kTRUE), _compiled(kFALSE)
{
  // Constructor with expression string and list of variables
  SetName(name) ;
  SetTitle(formula) ;

  TIterator* iter = list.createIterator() ;
  RooAbsArg* arg ;
  while (arg=(RooAbsArg*)iter->Next()) {
    _origList.Add(arg) ;
  }
  delete iter ;

  _compiled = kTRUE ;
  if (Compile()) {
    cout << "RooFormula::RooFormula(" << GetName() << "): compile error" << endl ;
    _isOK = kFALSE ;
    return ;
  }
}


RooFormula::RooFormula(const RooFormula& other, const char* name) : 
  TFormula(), _isOK(other._isOK), _compiled(kFALSE) 
{
  // Copy constructor

  SetName(name?name:other.GetName()) ;
  SetTitle(other.GetTitle()) ;

  TIterator* iter = other._origList.MakeIterator() ;
  RooAbsArg* arg ;
  while (arg=(RooAbsArg*)iter->Next()) {
    _origList.Add(arg) ;
  }
  delete iter ;
  
  Compile() ;
  _compiled=kTRUE ;
}



Bool_t RooFormula::reCompile(const char* newFormula) 
{
  // Recompile formula with new expression

  fNval=0 ;
  _useList.Clear() ;  

  TString oldFormula=GetTitle() ;
  if (Compile(newFormula)) {
    cout << "RooFormula::reCompile: new equation doesn't compile, formula unchanged" << endl ;
    reCompile(oldFormula) ;    
    return kTRUE ;
  }

  SetTitle(newFormula) ;
  return kFALSE ;
}



RooFormula::~RooFormula() 
{
  // Destructor
  _labelList.Delete() ;
}



RooArgSet& RooFormula::actualDependents() const
{
  if (!_compiled) {
    _isOK = !((RooFormula*)this)->Compile() ;
    _compiled = kTRUE ;
  }

  // Return list of dependents used in formula expression

  _actual.removeAll();
  
  int i ;
  for (i=0 ; i<_useList.GetSize() ; i++) {
    _actual.add((RooAbsArg&)*_useList.At(i),kTRUE) ;
  }

  return _actual ;
}


void RooFormula::dump() {
  // DEBUG: Dump state information
  int i ;
  cout << "RooFormula::dump()" << endl ;
  cout << "useList:" << endl ;
  for (i=0 ; i<_useList.GetSize() ; i++) {
    cout << "[" << i << "] = " << (void*) _useList.At(i) << " " << _useList.At(i)->GetName() << endl ;
  }
  cout << "labelList:" << endl ;
  for (i=0 ; i<_labelList.GetSize() ; i++) {
    cout << "[" << i << "] = " << (void*) _labelList.At(i) << " " << _labelList.At(i)->GetName() <<  endl ;
  }
  cout << "origList:" << endl ;
  for (i=0 ; i<_origList.GetSize() ; i++) {
    cout << "[" << i << "] = " << (void*) _origList.At(i)  << " " << _origList.At(i)->GetName() <<  endl ;
  }
}


Bool_t RooFormula::changeDependents(const RooAbsCollection& newDeps, Bool_t mustReplaceAll, Bool_t nameChange) 
{
  // Change used variables to those with the same name in given list

  //Change current servers to new servers with the same name given in list
  Bool_t errorStat(kFALSE) ;
  int i ;

  for (i=0 ; i<_useList.GetSize() ; i++) {
    RooAbsReal* replace = (RooAbsReal*) ((RooAbsArg*)_useList.At(i))->findNewServer(newDeps,nameChange) ;
    if (replace) {
      _useList.Replace(_useList.At(i),replace) ;
    } else if (mustReplaceAll) {
      cout << "RooFormula::changeDependents(1): cannot find replacement for " 
	   << _useList.At(i)->GetName() << endl ;
      errorStat = kTRUE ;
    }
  }  

  TIterator* iter = _origList.MakeIterator() ;
  RooAbsArg* arg ;
  while (arg=(RooAbsArg*)iter->Next()) {
    RooAbsReal* replace = (RooAbsReal*) arg->findNewServer(newDeps,nameChange) ;
    if (replace) {
      _origList.Replace(arg,replace) ;
    } else if (mustReplaceAll) {
      errorStat = kTRUE ;
    }
  }
  delete iter ;

  return errorStat ;
}


Double_t RooFormula::eval(const RooArgSet* nset)
{ 
  // Return current value of formula  
  if (!_compiled) {
    _isOK = !Compile() ;
    _compiled = kTRUE ;
  }

  // WVE sanity check should go here
  if (!_isOK) {
    cout << "RooFormula::eval(" << GetName() << "): Formula doesn't compile: " << GetTitle() << endl ;
    return 0. ;
  }

  // Pass current dataset pointer to DefinedValue
  _nset = (RooArgSet*) nset ;

  return EvalPar(0,0) ; 
}


Double_t
RooFormula::DefinedValue(Int_t code) {
  // Return current value for variable indicated by internal reference code
  if (code>=_useList.GetSize()) return 0 ;
  RooAbsArg* arg=(RooAbsArg*)_useList.At(code) ;

  const RooAbsReal *absReal= dynamic_cast<const RooAbsReal*>(arg);  
  if(0 != absReal) {
    return absReal->getVal(_nset) ;
  } else {
    const RooAbsCategory *absCat= dynamic_cast<const RooAbsCategory*>(arg);
    if(0 != absCat) {
      TString& label=((TObjString*)_labelList.At(code))->String() ;
      if (label.IsNull()) {
	return absCat->getIndex() ;
      } else {
	return absCat->lookupType(label)->getVal() ; // DK: why not call getVal(_nset) here also?
      }
    }
  }
  assert(0) ;
  return 0 ;
}


Int_t 
RooFormula::DefinedVariable(TString &name, int& action)
{
  Int_t ret = DefinedVariable(name) ;
  if (ret>=0) {

#if ROOT_VERSION_CODE >= ROOT_VERSION(4,0,1)
     action = kDefinedVariable;
#endif

  }
  return ret ;
}


Int_t 
RooFormula::DefinedVariable(TString &name) {
  // Check if a variable with given name is available
  char argName[1024];
  strcpy(argName,name.Data()) ;

  // Find :: operator and split string if found
  char *labelName = strstr(argName,"::") ;
  if (labelName) {
    *labelName = 0 ;
    labelName+= 2 ;
  }

  // Defined internal reference code for given named variable 
  RooAbsArg *arg = 0;
  if (argName[0] == '@') {
    // Access by ordinal number
    Int_t index = atoi(argName+1) ;
    if (index>=0 && index<_origList.GetSize()) {
      arg = (RooAbsArg*) _origList.At(index) ;
    } else {
      cout << "RooFormula::DefinedVariable(" << GetName() 
	   << ") ERROR: ordinal variable reference " << name 
	   << " out of range (0 - " << _origList.GetSize()-1 << ")" << endl ;
    }
  } else {
    // Access by name
    arg= (RooAbsArg*) _origList.FindObject(argName) ;
  }

  // Check that arg exists
  if (!arg) return -1 ;

  // Check that optional label corresponds to actual category state
  if (labelName) {
    RooAbsCategory* cat = dynamic_cast<RooAbsCategory*>(arg) ;
    if (!cat) {
      cout << "RooFormula::DefinedVariable(" << GetName() << ") ERROR: " 
	   << arg->GetName() << "' is not a RooAbsCategory" << endl ;
      return -1 ;
    }

    if (!cat->lookupType(labelName)) {
      cout << "RooFormula::DefinedVariable(" << GetName() << ") ERROR '" 
	   << labelName << "' is not a state of " << arg->GetName() << endl ;
      return -1 ;
    }

  }


  // Check if already registered
  Int_t i ;
  for(i=0 ; i<_useList.GetSize() ; i++) {
    RooAbsArg* var = (RooAbsArg*) _useList.At(i) ;
    Bool_t varMatch = !TString(var->GetName()).CompareTo(arg->GetName()) ;

    if (varMatch) {
      TString& lbl= ((TObjString*) _labelList.At(i))->String() ;
      Bool_t lblMatch(kFALSE) ;
      if (!labelName && lbl.IsNull()) {
	lblMatch=kTRUE ;
      } else if (labelName && !lbl.CompareTo(labelName)) {
	lblMatch=kTRUE ;
      }

      if (lblMatch) {
	// Label and variable name match, recycle entry
//  	cout << "DefinedVariable " << arg->GetName() ;
//  	if (labelName) cout << "::" << labelName ;
//  	cout << " previously registered with code " << i << endl ;
	return i ;
      }
    }
  }

  // Register new entry ;
  _useList.Add(arg) ;
  if (!labelName) {
    _labelList.Add(new TObjString("")) ;
  } else {
    _labelList.Add(new TObjString(labelName)) ;
  }

//    cout << "DefinedVariable " << arg->GetName() ;
//    if (labelName) cout << "::" << labelName ;
//    cout << " registered with code " << _useList.GetSize()-1 << endl ;

   return (_useList.GetSize()-1) ;
}


void RooFormula::printToStream(ostream& os, PrintOption opt, TString indent) const {
  // Print info about this argument set to the specified stream.
  //
  //   OneLine: use RooPrintable::oneLinePrint()
  //  Standard: our formula
  //   Verbose: formula and list of actual dependents

  if(opt == Standard) {
    os << indent << GetTitle() << endl;
  }
  else {
    oneLinePrint(os,*this);
    if(opt == Verbose) {
      os << indent << "--- RooFormula ---" << endl;
      os << indent << "  Formula: \"" << GetTitle() << "\"" << endl;
      indent.Append("  ");
      os << indent;
      actualDependents().printToStream(os,lessVerbose(opt),indent);
    }
  }
}
