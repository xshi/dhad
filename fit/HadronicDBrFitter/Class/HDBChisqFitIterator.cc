// -*- C++ -*-
//
// Package:     <HadronicDBrFitter>
// Module:      HDBChisqFitIterator
// 
// Description: <one line class summary>
//
// Implementation:
//     <Notes on implementation>
//
// Author:      Werner Sun
// Created:     Tue Mar 30 22:55:25 EST 2004
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
//#include <vector>
//#include <set>
//#include <map>
//#include <algorithm>
//#include <utility>

// user include files
//#include "Experiment/report.h"
#include "HadronicDBrFitter/HDBChisqFitIterator.h"
#include "HadronicDBrFitter/HDBChisqMinimizer.h"

//
// constants, enums and typedefs
//

static const char* const kFacilityString = "HadronicDBrFitter.HDBChisqFitIterator" ;

// ---- cvs-based strings (Id and Tag with which file was checked out)
static const char* const kIdString  = "$Id: skeleton.cc,v 1.6 2001/01/03 16:25:23 cdj Exp $";
static const char* const kTagString = "$Name:  $";

//
// static data member definitions
//

//
// constructors and destructor
//
HDBChisqFitIterator::HDBChisqFitIterator(
   HDBChisqMinimizer* aParameterEstimator,
   int aMaxIterations,
   double aMaxDeltaChisqNdof )
   : HDBFitIterator( aParameterEstimator,
		     aMaxIterations,
//		     true ), // execute final pass
		     false ), // execute final pass
     m_previousChisq( 0. ),
     m_maxDeltaChisqNdof( aMaxDeltaChisqNdof )
{
}

// HDBChisqFitIterator::HDBChisqFitIterator( const HDBChisqFitIterator& rhs )
// {
//    // do actual copying here; if you implemented
//    // operator= correctly, you may be able to use just say      
//    *this = rhs;
// }

HDBChisqFitIterator::~HDBChisqFitIterator()
{
}

//
// assignment operators
//
// const HDBChisqFitIterator& HDBChisqFitIterator::operator=( const HDBChisqFitIterator& rhs )
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

bool
HDBChisqFitIterator::convergenceCriterionMet()
{
   HDBChisqMinimizer* chisqMinimizer =
      ( HDBChisqMinimizer* ) m_parameterEstimator ;

   if( m_numberIterations == 1 )
   {
      m_previousChisq = chisqMinimizer->chisq() ;
      return false ;
   }

   double ndof = chisqMinimizer->ndof() ;
   if( ndof == 0. )
   {
      ndof = 1. ;
   }

   double deltaChisqNdof =
      ( chisqMinimizer->chisq() - m_previousChisq ) / ndof ;
   m_previousChisq = chisqMinimizer->chisq() ;

   if( m_printDiagnostics )
   {
      cout << "deltaChisqNdof " << deltaChisqNdof
	   << " max " << m_maxDeltaChisqNdof << endl ;
   }

   if( deltaChisqNdof <= 1.e-6 &&
       fabs( deltaChisqNdof ) < fabs( m_maxDeltaChisqNdof ) )
   {      
      return true ;
   }

   return false ;
}

//
// const member functions
//

double
HDBChisqFitIterator::chisq() const
{
   return ( ( HDBChisqMinimizer* ) m_parameterEstimator )->chisq() ;
}

int
HDBChisqFitIterator::ndof() const
{
   return ( ( HDBChisqMinimizer* ) m_parameterEstimator )->ndof() ;
}

//
// static member functions
//
