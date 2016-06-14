// -*- C++ -*-
//
// Package:     <HadronicDBrFitter>
// Module:      HDBVariableVector
// 
// Description: <one line class summary>
//
// Implementation:
//     <Notes on implementation>
//
// Author:      Werner Sun
// Created:     Fri May 21 18:24:33 EDT 2004
// $Id$
//
// Revision history
//
// $Log$

// #include "Experiment/Experiment.h"

// system include files
// You may have to uncomment some of these or other stl headers
// depending on what other header files you include (e.g. FrameAccess etc.)!
//#include <string>
//#include <vector>
//#include <set>
//#include <map>
//#include <algorithm>
//#include <utility>

// user include files
//#include "Experiment/report.h"
#include "HadronicDBrFitter/HDBVariableVector.h"


//
// constants, enums and typedefs
//

static const char* const kFacilityString = "HadronicDBrFitter.HDBVariableVector" ;

// ---- cvs-based strings (Id and Tag with which file was checked out)
static const char* const kIdString  = "$Id: skeleton.cc,v 1.7 2004/02/12 02:14:38 pcs Exp $";
static const char* const kTagString = "$Name:  $";

//
// static data member definitions
//

//
// constructors and destructor
//
HDBVariableVector::HDBVariableVector()
{
}

HDBVariableVector::HDBVariableVector( int aNumberRows )
   : HDBVariableMatrix( aNumberRows, 1 )
{
}

// HDBVariableVector::HDBVariableVector( const HDBVariableVector& rhs )
// {
//    // do actual copying here; if you implemented
//    // operator= correctly, you may be able to use just say      
//    *this = rhs;
// }

HDBVariableVector::~HDBVariableVector()
{
}

//
// assignment operators
//
// const HDBVariableVector& HDBVariableVector::operator=(
//    const HDBVariableVector& rhs )
// {
//    if( this != &rhs )
//    {
//       // do actual copying here, plus:
//       // "SuperClass"::operator=( rhs );
//       HDBVariableMatrix::operator=( rhs ) ;
//    }
//    return *this;
// }

//
// member functions
//

//
// const member functions
//

//
// static member functions
//
