// -*- C++ -*-
//
// Package:     HadronicDNtupleProc
// Module:      HadronicDNtupleProc_DONT_TOUCH2
// 
// Description: DONT TOUCH THIS FILE!
//
//              Factory method to create processor HadronicDNtupleProc:
//              creates a new HadronicDNtupleProc instance each time 
//              it is called; it is used by Suez 
//              to create a Processor after loading in 
//              the code from a shared library.
//
// Implementation:
//
// Author:      Peter Onyisi
// Created:     Fri Feb 27 16:35:43 EST 2004
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
#endif             

// user include files
#include "HadronicDNtupleProc/HadronicDNtupleProc.h"

// STL classes
#include <string>

//
// constants, enums and typedefs
//
// ---- cvs-based strings (Id and Tag with which file was checked out)
static const char* const kIdString  = "$Id$";
static const char* const kTagString = "$Name$";

//
// function definitions
//

extern "C" {
   Processor* makeProcessor( void );
   const char* versionString( void );
}

Processor*
makeProcessor( void )
{
   return new HadronicDNtupleProc;
}

const char*
versionString( void )
{
   return kTagString;
}

