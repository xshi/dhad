/*****************************************************************************
 * Project: RooFit                                                           *
 * Package: RooFitCore                                                       *
 *    File: $Id: RooCategoryProxy.cc,v 1.14 2005/02/25 14:22:54 wverkerke Exp $
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
// RooCategoryProxy is the concrete proxy for RooAbsCategory objects
// A RooCategoryProxy is the general mechanism to store references
// to RooAbsCategoriess inside a RooAbsArg
//
// RooCategoryProxy provides a cast operator to Int_t and 'const char*', allowing
// the proxy to functions a Int_t/'const char*' on the right hand side of expressions.


#include "RooFitCore/RooCategoryProxy.hh"

ClassImp(RooCategoryProxy)
;

RooCategoryProxy::RooCategoryProxy(const char* name, const char* desc, RooAbsArg* owner, RooAbsCategory& ref,
				   Bool_t valueServer, Bool_t shapeServer, Bool_t ownArg) : 
  RooArgProxy(name, desc, owner, ref, valueServer, shapeServer, ownArg)
{
  // Constructor with owner and proxied category object
}


RooCategoryProxy::RooCategoryProxy(const char* name, RooAbsArg* owner, const RooCategoryProxy& other) : 
  RooArgProxy(name, owner, other) 
{
  // Copy constructor
}


RooCategoryProxy::~RooCategoryProxy() 
{
  // Destructor
}
