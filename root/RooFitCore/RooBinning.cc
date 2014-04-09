/*****************************************************************************
 * Project: RooFit                                                           *
 * Package: RooFitCore                                                       *
 *    File: $Id: RooBinning.cc,v 1.14 2005/02/25 14:22:54 wverkerke Exp $
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
// Class RooBinning is an implements RooAbsBinning in terms of
// an array of boundary values, posing no constraints on the
// choice of binning, thus allowing variable bin sizes. Various
// methods allow the user to add single bin boundaries, mirrored pairs,
// or sets of uniformly spaced boundaries.

#include <iostream>
#include "RooFitCore/RooBinning.hh"
#include "RooFitCore/RooDouble.hh"
#include "RooFitCore/RooAbsPdf.hh"
#include "RooFitCore/RooRealVar.hh"
#include "RooFitCore/RooNumber.hh"
using std::cout;
using std::endl;

ClassImp(RooBinning)
;


RooBinning::RooBinning(Double_t xlo, Double_t xhi, const char* name) : 
  RooAbsBinning(name), 
  _ownBoundLo(kTRUE), 
  _ownBoundHi(kTRUE), 
  _array(0)
{
  _bIter = binIterator() ;

  setRange(xlo,xhi) ;
}



RooBinning::RooBinning(Int_t nbins, Double_t xlo, Double_t xhi, const char* name) : 
  RooAbsBinning(name), 
  _ownBoundLo(kTRUE), 
  _ownBoundHi(kTRUE), 
  _array(0)
{
  _bIter = binIterator() ;

  // Uniform bin size constructor
  setRange(xlo,xhi) ;
  addUniform(nbins,xlo,xhi) ;
}




RooBinning::RooBinning(Int_t nbins, const Double_t* boundaries, const char* name) : 
  RooAbsBinning(name),
  _ownBoundLo(kTRUE), 
  _ownBoundHi(kTRUE), 
  _array(0)
{
  _bIter = binIterator() ;

  // Variable bin size constructor
  setRange(boundaries[0],boundaries[nbins]) ;
  while(nbins--) addBoundary(boundaries[nbins]) ;
}



RooBinning::RooBinning(const RooBinning& other, const char* name) : 
  RooAbsBinning(name),
  _array(0)
{ 
  // Copy constructor
  _boundaries.Delete() ;
  _bIter = binIterator();

  other._bIter->Reset() ;
  RooDouble* boundary ;
  while (boundary=(RooDouble*)other._bIter->Next()) {
    addBoundary((Double_t)*boundary) ;
  }

  _xlo = other._xlo ;
  _xhi = other._xhi ;
  _ownBoundLo = other._ownBoundLo ;
  _ownBoundHi = other._ownBoundHi ;
  _nbins = other._nbins ;
}



RooBinning::~RooBinning() 
{
  // Destructor
  delete _bIter ;
  if (_array) delete[] _array ;

  _boundaries.Delete() ;
}


Bool_t RooBinning::addBoundary(Double_t boundary) 
{  
  // Check if boundary already exists 
  if (hasBoundary(boundary)) {
    // If boundary previously existed as range delimiter, 
    //                    convert to regular boundary now
    if (boundary==_xlo) _ownBoundLo = kFALSE ;
    if (boundary==_xhi) _ownBoundHi = kFALSE ;
    return kFALSE ;
  }

  // Add a new boundary
  _boundaries.Add(new RooDouble(boundary)) ;
  _boundaries.Sort() ;
  updateBinCount() ;
  return kTRUE ;
}


void RooBinning::addBoundaryPair(Double_t boundary, Double_t mirrorPoint) 
{
  // Add mirrored pair of boundaries
  addBoundary(boundary) ;
  addBoundary(2*mirrorPoint-boundary) ;
}


Bool_t RooBinning::removeBoundary(Double_t boundary)
{
  // Remove boundary at given value
  _bIter->Reset() ;
  RooDouble* b ;
  while(b=(RooDouble*)_bIter->Next()) {
    if (((Double_t)(*b))==boundary) {

      // If boundary is also range delimiter don't delete
      if (boundary!= _xlo && boundary != _xhi) {
	_boundaries.Remove(b) ;
	delete b ;
      }

      return kFALSE ;
    }
  }
  // Return error status - no boundary found
  return kTRUE ;
}




Bool_t RooBinning::hasBoundary(Double_t boundary)
{
  // Check if boundary exists at given value
  _bIter->Reset() ;
  RooDouble* b ;
  while(b=(RooDouble*)_bIter->Next()) {
    if (((Double_t)(*b))==boundary) {
      return kTRUE ;
    }
  }
  return kFALSE ;
}



void RooBinning::addUniform(Int_t nbins, Double_t xlo, Double_t xhi)
{
  // Add array of uniform bins
  Int_t i ;
  Double_t binw = (xhi-xlo)/nbins ;
  for (i=0 ; i<=nbins ; i++) 
    addBoundary(xlo+i*binw) ;  
}


Int_t RooBinning::binNumber(Double_t x) const
{
  // Determine sequential bin number for given value
  Int_t n(0) ;
  _bIter->Reset() ;
  RooDouble* b ;
  while(b=(RooDouble*)_bIter->Next()) {
    Double_t val = (Double_t)*b ;

    if (x<val) {
      return n ;
    }

    // Only increment counter in valid range
    if (val> _xlo && n<_nbins-1) n++ ;
  }
  return n;
}


Int_t RooBinning::rawBinNumber(Double_t x) const 
{
  // Determine 'raw' bin number (i.e counting all defined boundaries) for given value
  Int_t n(0) ;
  _bIter->Reset() ;

  RooDouble* b ;
  while(b=(RooDouble*)_bIter->Next()) {
    Double_t val = (Double_t)*b ;
    if (x<val) return n>0?n-1:0 ;
    n++ ;
  }
  return n-1;
}


Double_t RooBinning::nearestBoundary(Double_t x) const 
{
  Int_t bn = binNumber(x) ;
  if (fabs(binLow(bn)-x)<fabs(binHigh(bn)-x)) {
    return binLow(bn) ;
  } else {
    return binHigh(bn) ;
  }
}


TIterator* RooBinning::binIterator() const
{
  // Return iterator over sorted boundaries
  return _boundaries.MakeIterator() ;
}


Double_t* RooBinning::array() const
{
  if (_array) delete[] _array ;
  _array = new Double_t[numBoundaries()] ;

  _bIter->Reset() ;
  RooDouble* boundary ;  
  Int_t i(0) ;
  while(boundary=(RooDouble*)_bIter->Next()) {
    Double_t bval = (Double_t)*boundary ;
    if (bval>=_xlo && bval <=_xhi) {
      _array[i++] = bval ;
    }
  }

  return _array ;
}



void RooBinning::setRange(Double_t xlo, Double_t xhi) 
{
  if (xlo>xhi) {
    cout << "RooUniformBinning::setRange: ERROR low bound > high bound" << endl ;
    return ;
  }
  
  // Remove previous boundaries 
  _bIter->Reset() ;
  RooDouble* b ;
  while(b=(RooDouble*)_bIter->Next()) {    
    if (((Double_t)*b == _xlo && _ownBoundLo) ||
	((Double_t)*b == _xhi && _ownBoundHi)) {
      _boundaries.Remove(b) ;
      delete b ;
    }
  }

  // Insert boundaries at range delimiter, if necessary 
  _ownBoundLo = kFALSE ;
  _ownBoundHi = kFALSE ;
  if (!hasBoundary(xlo)) {
    addBoundary(xlo) ;
    _ownBoundLo = kTRUE ;
  }
  if (!hasBoundary(xhi)) {
    addBoundary(xhi) ;
    _ownBoundHi = kTRUE ;
  }

  _xlo = xlo ;
  _xhi = xhi ;
  
  // Count number of bins with new range 
  updateBinCount() ;
}



// OK
void RooBinning::updateBinCount()
{
  _bIter->Reset() ;
  RooDouble* boundary ;  
  Int_t i(-1) ;
  while(boundary=(RooDouble*)_bIter->Next()) {
    Double_t bval = (Double_t)*boundary ;
    if (bval>=_xlo && bval <=_xhi) {
      i++ ;
    }
  }  
  _nbins = i ;
}


// not OK
Bool_t RooBinning::binEdges(Int_t bin, Double_t& xlo, Double_t& xhi) const 
{
  if (bin<0 || bin>= _nbins) {
    cout << "RooBinning::binEdges ERROR: bin number must be in range (0," << _nbins << ")" << endl ; 
    return kTRUE ;
  }
  
  // Determine sequential bin number for given value
  Int_t n(0) ;
  _bIter->Reset() ;
  RooDouble* b ;
  while(b=(RooDouble*)_bIter->Next()) {
    Double_t val = (Double_t)*b ;

    if (n==bin && val>=_xlo) {
      xlo = val ;
      b = (RooDouble*)_bIter->Next() ;
      xhi = *b ;
      return kFALSE ;
    }

    // Only increment counter in valid range
    if (val>= _xlo && n<_nbins-1) n++ ;
  }

  return kTRUE ;
}


Double_t RooBinning::binCenter(Int_t bin) const 
{
  Double_t xlo,xhi ;
  if (binEdges(bin,xlo,xhi)) return 0 ;
  return (xlo+xhi)/2 ;
}


Double_t RooBinning::binWidth(Int_t bin) const 
{
  Double_t xlo,xhi ;
  if (binEdges(bin,xlo,xhi)) return 0 ;
  return (xhi-xlo);
}


Double_t RooBinning::binLow(Int_t bin) const 
{
  Double_t xlo,xhi ;
  if (binEdges(bin,xlo,xhi)) return 0 ;
  return xlo ;
}


Double_t RooBinning::binHigh(Int_t bin) const  
{
  Double_t xlo,xhi ;
  if (binEdges(bin,xlo,xhi)) return  0 ;
  return xhi ;
}

