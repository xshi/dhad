// -*- C++ -*-
//
// Package:     <HadronicDBrFitter>
// Module:      HDBFitInputFactory
// 
// Description: <one line class summary>
//
// Implementation:
//     <Notes on implementation>
//
// Author:      Werner Sun
// Created:     Wed May 26 21:37:27 EDT 2004
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
#include "HadronicDBrFitter/HDBFitInputFactory.h"


//
// constants, enums and typedefs
//

static const char* const kFacilityString = "HadronicDBrFitter.HDBFitInputFactory" ;

// ---- cvs-based strings (Id and Tag with which file was checked out)
static const char* const kIdString  = "$Id: skeleton.cc,v 1.7 2004/02/12 02:14:38 pcs Exp $";
static const char* const kTagString = "$Name:  $";

//
// static data member definitions
//

//
// constructors and destructor
//
HDBFitInputFactory::HDBFitInputFactory()
   : m_fitPredictions( 0 ),
     m_inputData( 0 ),
     m_externalFitPredictions( 0 ),
     m_externalData( 0 ),
     m_printDiagnostics( false )
{
}

// HDBFitInputFactory::HDBFitInputFactory( const HDBFitInputFactory& rhs )
// {
//    // do actual copying here; if you implemented
//    // operator= correctly, you may be able to use just say      
//    *this = rhs;
// }

HDBFitInputFactory::~HDBFitInputFactory()
{
   delete m_fitPredictions ;
   delete m_inputData ;
   delete m_externalFitPredictions ;
   delete m_externalData ;
}

//
// assignment operators
//
// const HDBFitInputFactory& HDBFitInputFactory::operator=( const HDBFitInputFactory& rhs )
// {
//   if( this != &rhs ) {
//      // do actual copying here, plus:
//      // "SuperClass"::operator=( rhs );
//   }
//
//   return *this;
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
