/*****************************************************************************
 * Project: RooFit                                                           *
 * Package: RooFitCore                                                       *
 *    File: $Id: Roo1DTable.cc,v 1.21 2005/02/25 14:22:48 wverkerke Exp $
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

// -- CLASS DESCRIPTION [PLOT] --
// Roo1DTable implements a one-dimensional table. A table is the category
// equivalent of a plot. To create a table use the RooDataSet::table method.

#include <iostream>
#include <iomanip>
#include "TString.h"
#include "RooFitCore/Roo1DTable.hh"
using std::cout;
using std::endl;
using std::ostream;
using std::setfill;
using std::setw;

ClassImp(Roo1DTable)


Roo1DTable::Roo1DTable(const char *name, const char *title, const RooAbsCategory& cat) : 
  RooTable(name,title), _total(0), _nOverflow(0)
{
  // Create an empty table from abstract category. The number of table entries and 
  // their names are taken from the category state labels at the time of construction,
  // but not reference to the category is retained after the construction phase.
  // Use fill() to fill the table.

  //Take types from reference category
  Int_t nbin(0) ;
  TIterator* tIter = cat.typeIterator() ;
  RooCatType* type ;
  while (type = (RooCatType*)tIter->Next()) {
    _types.Add(new RooCatType(*type)) ;
    nbin++ ;
  }
  delete tIter ;

  // Create counter array and initialize
  _count = new Double_t[nbin] ;
  for (int i=0 ; i<nbin ; i++) _count[i] = 0 ;
}



Roo1DTable::Roo1DTable(const Roo1DTable& other) : 
  RooTable(other), _total(other._total), _nOverflow(other._nOverflow)
{  
  // Copy constructor

  // Take types from reference category
  Int_t nbin(0) ;

  int i;
  for (i=0 ; i<other._types.GetEntries() ; i++) {
    _types.Add(new RooCatType(*(RooCatType*)other._types.At(i))) ;
    nbin++ ;
  }

  // Create counter array and initialize
  _count = new Double_t[nbin] ;
  for (i=0 ; i<nbin ; i++) _count[i] = other._count[i] ;
}


Roo1DTable::~Roo1DTable()
{
  // Destructor

  // We own the contents of the object array
  _types.Delete() ;
  delete[] _count ;
}


void Roo1DTable::fill(RooAbsCategory& cat, Double_t weight) 
{
  // Increment the counter of the table slot with
  // the name corresponding to that of the current 
  // category state. If the current category state
  // matches no table slot name, the table overflow
  // counter is incremented.

  if (weight==0) return ;

  _total += weight ;

  //Bool_t found(kFALSE) ;
  for (int i=0 ; i<_types.GetEntries() ; i++) {
    RooCatType* entry = (RooCatType*) _types.At(i) ;
    if (cat.getIndex()==entry->getVal()) {
      _count[i] += weight ; ;
      //found=kTRUE ;
      return;
    }
  }  

  //if (!found) {
  _nOverflow += weight ;
  //}
}



void Roo1DTable::printToStream(ostream& os, PrintOption opt, TString indent) const 
{
  // Print the formateed table contents on the given stream

  os << endl ;
  os << "  Table " << GetName() << " : " << GetTitle() << endl ;

  // Determine maximum label and count width
  Int_t labelWidth(0) ;
  Double_t maxCount(1) ;

  int i;
  for (i=0 ; i<_types.GetEntries() ; i++) {
    RooCatType* entry = (RooCatType*) _types.At(i) ;

    // Disable warning about a signed/unsigned mismatch by MSCV 6.0 by
    // using the lwidth temporary.
    Int_t lwidth = strlen(entry->GetName());
    labelWidth = lwidth > labelWidth ? lwidth : labelWidth;
    maxCount=_count[i]>maxCount?_count[i]:maxCount ;
  }
  // Adjust formatting if overflow field will be present
  if (_nOverflow>0) {
    labelWidth=labelWidth>8?labelWidth:8 ;
    maxCount=maxCount>_nOverflow?maxCount:_nOverflow ;
  }

  // Header
  Int_t countWidth=((Int_t)log10(maxCount))+1 ;
  os << "  +-" << setw(labelWidth) << setfill('-') << "-" << "-+-" << setw(countWidth) << "-" << "-+" << endl ;
  os << setfill(' ') ;

  // Contents
  for (i=0 ; i<_types.GetEntries() ; i++) {
    RooCatType* entry = (RooCatType*) _types.At(i) ;
    if (_count[i]>0 || opt>=Verbose) {
      os << "  | " << setw(labelWidth) << entry->GetName() << " | " << setw(countWidth) << _count[i] << " |" << endl ;
    }
  }

  // Overflow field
  if (_nOverflow) {
    os << "  +-" << setw(labelWidth) << setfill('-') << "-" << "-+-" << setw(countWidth) << "-" << "-+" << endl ;
    os << "  | " << "Overflow" << " | " << setw(countWidth) << _nOverflow << " |" << endl ;    
  }

  // Footer
  os << "  +-" << setw(labelWidth) << setfill('-') << "-" << "-+-" << setw(countWidth) << "-" << "-+" << endl ;
  os << setfill(' ') ;
  os << endl ;
}


Double_t Roo1DTable::get(const char* label, Bool_t silent) const 
{
  // Return the table entry named 'label'. Zero is returned
  // if given label doesn't occur in table. 
  TObject* cat = _types.FindObject(label) ;
  if (!cat) {
    if (!silent) {
      cout << "Roo1DTable::get: ERROR: no such entry: " << label << endl ;
    }
    return 0 ;
  }
  return _count[_types.IndexOf(cat)] ;
}


Double_t Roo1DTable::getOverflow() const 
{
  // Return the number of overflow entries in the table.
  return _nOverflow ;
}


Double_t Roo1DTable::getFrac(const char* label, Bool_t silent) const 
{
  // Return the fraction of entries in the table contained in the slot named 'label'. 
  // The normalization includes the number of overflows.
  // Zero is returned if given label doesn't occur in table.   
  if (_total) {
    return get(label,silent) / _total ;
  } else {
    if (!silent) cout << "Roo1DTable::getFrac: WARNING table empty, returning 0" << endl ;
    return 0. ;
  }
}
