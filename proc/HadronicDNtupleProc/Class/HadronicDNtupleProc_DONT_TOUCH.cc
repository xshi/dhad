// -*- C++ -*-
//
// Package:     HadronicDNtupleProc
// Module:      HadronicDNtupleProc_DONT_TOUCH
// 
// Description: DONT TOUCH THIS FILE
//
//              Definition of bind action
//
// Implementation:
//
// Author:      Peter Onyisi
// Created:     Fri Feb 27 16:35:44 EST 2004
// $Id$
//
// Revision history
//
// $Log$
// Revision 1.1  2010/05/17 17:30:18  xs32
// Add
//
// Revision 1.1.1.1  2004/03/12 18:43:51  ponyisi
// import source of HadronicDNtupleProc
//
 
#include "Experiment/Experiment.h"

// system include files
#if defined(AMBIGUOUS_STRING_FUNCTIONS_BUG)
#include <string>
#endif /* AMBIGUOUS_STRING_FUNCTIONS_BUG */            

// user include files
#include "HadronicDNtupleProc/HadronicDNtupleProc.h"
#include "Processor/Action.h"                

// STL classes

//
// constants, enums and typedefs
//
// ---- cvs-based strings (Id and Tag with which file was checked out)
static const char* const kIdString  = "$Id$";
static const char* const kTagString = "$Name$";

//
// function definitions
//

//
// static data member definitions
//

//
// member functions
//
// ---------------- binding method to stream -------------------
void
HadronicDNtupleProc::bind(
   ActionBase::ActionResult (HadronicDNtupleProc::*iMethod)( Frame& ),
   const Stream::Type& iStream )
{
   bindAction( iStream, new Action<HadronicDNtupleProc>( iMethod, this ) );
}

//
// const member functions
//

//
// static member functions
//
