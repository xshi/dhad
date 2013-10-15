// -*- C++ -*-
//
// Package:     MCDecayProc
// Module:      MCDecayProc_DONT_TOUCH
// 
// Description: DONT TOUCH THIS FILE
//
//              Definition of bind action
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
// Revision 1.1  2011/04/18 13:42:10  xs32
// add
//
 
#include "Experiment/Experiment.h"

// system include files
#if defined(AMBIGUOUS_STRING_FUNCTIONS_BUG)
#include <string>
#endif /* AMBIGUOUS_STRING_FUNCTIONS_BUG */            

// user include files
#include "MCDecayProc/MCDecayProc.h"
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
MCDecayProc::bind(
   ActionBase::ActionResult (MCDecayProc::*iMethod)( Frame& ),
   const Stream::Type& iStream )
{
   bindAction( iStream, new Action<MCDecayProc>( iMethod, this ) );
}

//
// const member functions
//

//
// static member functions
//
