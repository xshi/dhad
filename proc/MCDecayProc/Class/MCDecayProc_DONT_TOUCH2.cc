// -*- C++ -*-
//
// Package:     MCDecayProc
// Module:      MCDecayProc_DONT_TOUCH2
// 
// Description: DONT TOUCH THIS FILE!
//
//              Factory method to create processor MCDecayProc:
//              creates a new MCDecayProc instance each time 
//              it is called; it is used by Suez 
//              to create a Processor after loading in 
//              the code from a shared library.
//
// Implementation:
//
// Author:      Xin Shi
// Created:     Mon Apr 18 09:39:25 EDT 2011
// $Id$
//
// Revision history
//
// $Log$
// Revision 1.1  2011/04/18 13:42:11  xs32
// add
//
 
#include "Experiment/Experiment.h"

// system include files
#if defined(AMBIGUOUS_STRING_FUNCTIONS_BUG)
#include <string>
#endif             

// user include files
#include "MCDecayProc/MCDecayProc.h"

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
   return new MCDecayProc;
}

const char*
versionString( void )
{
   return kTagString;
}

