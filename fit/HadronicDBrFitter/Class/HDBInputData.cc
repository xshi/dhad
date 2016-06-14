// -*- C++ -*-
//
// Package:     <HadronicDBrFitter>
// Module:      HDBInputData
// 
// Description: <one line class summary>
//
// Implementation:
//     <Notes on implementation>
//
// Author:      Werner Sun
// Created:     Tue Mar 30 00:09:24 EST 2004
// $Id$
//
// Revision history
//
// $Log$

//#include "Experiment/Experiment.h"

// system include files
// You may have to uncomment some of these or other stl headers
// depending on what other header files you include (e.g. FrameAccess etc.)!
//#include <string>
#include <vector>
//#include <set>
//#include <map>
//#include <algorithm>
//#include <utility>

// user include files
//#include "Experiment/report.h"
#include "HadronicDBrFitter/HDBInputData.h"


//
// constants, enums and typedefs
//

static const char* const kFacilityString = "HadronicDBrFitter.HDBInputData" ;

// ---- cvs-based strings (Id and Tag with which file was checked out)
static const char* const kIdString  = "$Id: skeleton.cc,v 1.6 2001/01/03 16:25:23 cdj Exp $";
static const char* const kTagString = "$Name:  $";

//
// static data member definitions
//

//
// constructors and destructor
//
HDBInputData::HDBInputData()
{
}

// HDBInputData::HDBInputData( const HDBInputData& rhs )
// {
//    // do actual copying here; if you implemented
//    // operator= correctly, you may be able to use just say      
//    *this = rhs;
// }

HDBInputData::~HDBInputData()
{
}

//
// assignment operators
//
// const HDBInputData& HDBInputData::operator=( const HDBInputData& rhs )
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

void
HDBInputData::initialize( const HepVector& aFitParameters,
			  const HDBVariableVector* aFitPredictions )
{
   m_yieldDerivatives =
      HepMatrix( aFitParameters.num_row(), errorMatrix().num_col(), 0 ) ;

   for( int i = 0 ; i < aFitParameters.num_row() ; ++i )
   {
      m_errorMatrixDerivatives.push_back(
	 HepSymMatrix( aFitPredictions->numberRows(), 0 ) ) ;
//	 HepMatrix( aFitPredictions->numberRows(), aFitPredictions->numberRows(), 0 ) ) ;
   }
}


//
// const member functions
//

//
// static member functions
//
