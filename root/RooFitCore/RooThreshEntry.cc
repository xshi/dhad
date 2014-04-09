/*****************************************************************************
 * Project: RooFit                                                           *
 * Package: RooFitCore                                                       *
 *    File: $Id: RooThreshEntry.cc,v 1.9 2005/02/25 14:23:03 wverkerke Exp $
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

#include "TClass.h"
#include "RooFitCore/RooThreshEntry.hh"

ClassImp(RooThreshEntry)
;

RooThreshEntry::RooThreshEntry(Double_t thresh, const RooCatType& cat) : 
  _thresh(thresh), _cat(cat) 
{
}


RooThreshEntry::RooThreshEntry(const RooThreshEntry& other) : 
  TObject(other), _thresh(other._thresh), _cat(other._cat) 
{
}


Int_t RooThreshEntry::Compare(const TObject* other) const 
{
  // Can only compare objects of same type
  if (!other->IsA()->InheritsFrom(RooThreshEntry::Class())) return 0 ;

  RooThreshEntry* otherTE = (RooThreshEntry*) other ;
  return (_thresh < otherTE->_thresh) ? -1 : 1 ;
}


