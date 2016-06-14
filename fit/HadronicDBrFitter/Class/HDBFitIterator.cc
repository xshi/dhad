// -*- C++ -*-
//
// Package:     <HadronicDBrFitter>
// Module:      HDBFitIterator
// 
// Description: <one line class summary>
//
// Implementation:
//     <Notes on implementation>
//
// Author:      Werner Sun
// Created:     Mon Mar 29 22:35:25 EST 2004
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
#include "HadronicDBrFitter/HDBFitIterator.h"

//
// constants, enums and typedefs
//

static const char* const kFacilityString = "HadronicDBrFitter.HDBFitIterator" ;

// ---- cvs-based strings (Id and Tag with which file was checked out)
static const char* const kIdString  = "$Id: skeleton.cc,v 1.6 2001/01/03 16:25:23 cdj Exp $";
static const char* const kTagString = "$Name:  $";

//
// static data member definitions
//

//
// constructors and destructor
//
HDBFitIterator::HDBFitIterator(
   HDBParameterEstimator* aParameterEstimator,
   int aMaxIterations,
   bool aExecuteFinalPass )
   : m_parameterEstimator( aParameterEstimator ),
     m_maxIterations( aMaxIterations ),
     m_numberIterations( 0 ),
     m_executeFinalPass( aExecuteFinalPass )
{
}

// HDBFitIterator::HDBFitIterator( const HDBFitIterator& rhs )
// {
//    // do actual copying here; if you implemented
//    // operator= correctly, you may be able to use just say      
//    *this = rhs;
// }

HDBFitIterator::~HDBFitIterator()
{
}

//
// assignment operators
//
// const HDBFitIterator& HDBFitIterator::operator=( const HDBFitIterator& rhs )
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

void
HDBFitIterator::estimateParameters( bool aFinalPass )
{
   // aFinalPass is ignored in HDBFitIterator classes.

   m_numberIterations = 0 ;

   HDBParameterEstimator::Status status ;

   if( m_parameterEstimator )
   {
      do
      {
	 ++m_numberIterations ;

	 if( m_printDiagnostics )
	 {
	    cout << "Performing iteration " << m_numberIterations << endl ;
	 }

	 m_parameterEstimator->estimateParameters() ;
	 status = m_parameterEstimator->fitStatus() ;
      }
      while( status == HDBParameterEstimator::kFitSuccessful &&
	     !convergenceCriterionMet() &&
	     m_numberIterations < m_maxIterations ) ;

      if( m_numberIterations == m_maxIterations )
      {
	 m_fitStatus = HDBParameterEstimator::kFitUnsuccessful ;
	 cout << "Fit did not converge." << endl ;
	 return ;
      }

      if( m_executeFinalPass )
      {
	 saveFitResultsBeforeFinalPass() ;
	 m_parameterEstimator->estimateParameters( true ) ;

	 // ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	 saveFitResultsBeforeFinalPass2() ;
	 m_numberIterations = 0 ;
	 do
	 {
	    ++m_numberIterations ;

	    if( m_printDiagnostics )
	    {
	       cout << "Performing iteration2 " << m_numberIterations << endl ;
	    }

	    m_parameterEstimator->estimateParameters( true ) ;
	    status = m_parameterEstimator->fitStatus() ;
	 }
	 while( status == HDBParameterEstimator::kFitSuccessful &&
		!convergenceCriterionMet() &&
		m_numberIterations < m_maxIterations ) ;
	 // ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
      }

      m_fitStatus = m_parameterEstimator->fitStatus() ;
   }
   else
   {
      m_fitStatus = HDBParameterEstimator::kFitUnsuccessful ;
   }
}

//
// static member functions
//
