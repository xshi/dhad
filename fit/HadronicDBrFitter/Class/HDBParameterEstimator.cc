// -*- C++ -*-
//
// Package:     <HadronicDBrFitter>
// Module:      HDBParameterEstimator
// 
// Description: <one line class summary>
//
// Implementation:
//     <Notes on implementation>
//
// Author:      Werner Sun
// Created:     Mon Mar 29 22:34:00 EST 2004
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
#include <assert.h>

// user include files
//#include "Experiment/report.h"
#include "HadronicDBrFitter/HDBParameterEstimator.h"
#include "HadronicDBrFitter/HDBFitInputFactory.h"


//
// constants, enums and typedefs
//

static const char* const kFacilityString = "HadronicDBrFitter.HDBParameterEstimator" ;

// ---- cvs-based strings (Id and Tag with which file was checked out)
static const char* const kIdString  = "$Id: skeleton.cc,v 1.6 2001/01/03 16:25:23 cdj Exp $";
static const char* const kTagString = "$Name:  $";

//
// static data member definitions
//

//
// constructors and destructor
//
HDBParameterEstimator::HDBParameterEstimator()
   : m_printDiagnostics( false )
{
}

HDBParameterEstimator::HDBParameterEstimator(
   HDBInputData* aInputData,
   HDBInputData* aExternalInputData,
   HDBVariableVector* aFitPredictions,
   HDBVariableVector* aExternalFitPredictions,
   const HDBData& aSeedParameters )
   : m_inputMeasurements( aInputData ),
     m_externalMeasurements( aExternalInputData ),
     m_fitPredictions( aFitPredictions ),
     m_externalFitPredictions( aExternalFitPredictions ),
     m_fittedParameters( aSeedParameters ),
     m_printDiagnostics( false )
{
//    // Fill the external parameter vector and errorInv.
//    if( m_externalInputData )
//    {
//       m_externalInputData->expandedValuesAndErrorInverse(
// 	 m_fitPredictions->parameterNames(),
// 	 m_externalParameters,
// 	 m_externalErrorInverse ) ;
//    }
}

HDBParameterEstimator::HDBParameterEstimator(
   HDBFitInputFactory* aFactory )
   : m_inputMeasurements( aFactory->inputData() ),
     m_fitPredictions( aFactory->fitPredictions() ),
     m_printDiagnostics( false )
{
   resetSeeds( aFactory ) ;

   // Initialize after resetSeeds to keep order of data input the same.
   m_externalMeasurements = aFactory->externalData() ;
   m_externalFitPredictions = aFactory->externalFitPredictions() ;

//    // Fill the external parameter vector and errorInv.
//    m_externalParameterData = aFactory->externalParameterData() ;
//    if( m_externalParameterData )
//    {
//       m_externalParameterData->expandedValuesAndErrorInverse(
// 	 m_fitPredictions->parameterNames(),
// 	 m_externalParameters,
// 	 m_externalErrorInverse ) ;
//    }
}

// HDBParameterEstimator::HDBParameterEstimator( const HDBParameterEstimator& rhs )
// {
//    // do actual copying here; if you implemented
//    // operator= correctly, you may be able to use just say      
//    *this = rhs;
// }

HDBParameterEstimator::~HDBParameterEstimator()
{
}

//
// assignment operators
//
// const HDBParameterEstimator& HDBParameterEstimator::operator=( const HDBParameterEstimator& rhs )
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
HDBParameterEstimator::resetSeeds( HDBFitInputFactory* aFactory )
{
   m_fittedParameters =
      HDBData( aFactory->seedParameters(),
	       HepSymMatrix( aFactory->seedParameters().num_row(), 0 ) ) ;
}
//
// const member functions
//

HepVector
HDBParameterEstimator::predictedValues() const
{
  return m_fitPredictions->values( m_fittedParameters.values() ) ;
}

HepVector
HDBParameterEstimator::residuals() const
{
   return ( m_inputMeasurements->values() - predictedValues() ) ;
}

double
HDBParameterEstimator::residualError( int aMeasIndex ) const
{
   return
      sqrt( m_inputMeasurements->errorMatrix()[ aMeasIndex ][ aMeasIndex ] ) ;
}

HepMatrix
HDBParameterEstimator::residualDerivatives() const
{
   return m_fitPredictions->derivatives( m_fittedParameters.values() ) -
      m_inputMeasurements->yieldDerivatives() ;
}

HepVector
HDBParameterEstimator::predictedExternalValues() const
{
  return m_externalFitPredictions->values( m_fittedParameters.values() ) ;
}

HepVector
HDBParameterEstimator::externalResiduals() const
{
   if( m_externalMeasurements->numberOfValues() == 0 )
   {
      return HepVector( 1, 0 ) ;
   }

   return ( m_externalMeasurements->values() - predictedExternalValues() ) ;
}

double
HDBParameterEstimator::externalResidualError( int aMeasIndex ) const
{
   return
      sqrt( m_externalMeasurements->errorMatrix()[ aMeasIndex ][ aMeasIndex ] ) ;
}

HepMatrix
HDBParameterEstimator::externalResidualDerivatives() const
{
   HepMatrix derivs =
      m_externalFitPredictions->derivatives( m_fittedParameters.values() ) ;

   if( m_externalMeasurements->numberOfValues() > 0 )
   {
      derivs -= m_externalMeasurements->yieldDerivatives() ;
   }

   return derivs ;
}

// HepVector
// HDBParameterEstimator::externalResiduals() const
// {
//    return ( m_externalParameters - m_fittedParameters.values() ) ;
// }


//
// static member functions
//
