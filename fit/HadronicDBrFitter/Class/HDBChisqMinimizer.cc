
// -*- C++ -*-
//
// Package:     <HadronicDBrFitter>
// Module:      HDBChisqMinimizer
// 
// Description: <one line class summary>
//
// Implementation:
//     <Notes on implementation>
//
// Author:      Werner Sun
// Created:     Mon Mar 29 22:31:00 EST 2004
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
#include "HadronicDBrFitter/HDBChisqMinimizer.h"


//
// constants, enums and typedefs
//

static const char* const kFacilityString = "HadronicDBrFitter.HDBChisqMinimizer" ;

// ---- cvs-based strings (Id and Tag with which file was checked out)
static const char* const kIdString  = "$Id: skeleton.cc,v 1.6 2001/01/03 16:25:23 cdj Exp $";
static const char* const kTagString = "$Name:  $";

//
// static data member definitions
//

//
// constructors and destructor
//
HDBChisqMinimizer::HDBChisqMinimizer(
   HDBInputData* aInputData,
   HDBInputData* aExternalData,
   HDBVariableVector* aFitPredictions,
   HDBVariableVector* aExternalFitPredictions,
   const HDBData& aSeedParameters )
   : HDBParameterEstimator( aInputData,
			    aExternalData,
			    aFitPredictions,
			    aExternalFitPredictions,
			    aSeedParameters ),
     m_chisq( 0. ),
     m_ndof( 0 )
{
}

HDBChisqMinimizer::HDBChisqMinimizer( HDBFitInputFactory* aFactory )
   : HDBParameterEstimator( aFactory )
{
}

// HDBChisqMinimizer::HDBChisqMinimizer( const HDBChisqMinimizer& rhs )
// {
//    // do actual copying here; if you implemented
//    // operator= correctly, you may be able to use just say      
//    *this = rhs;
// }

HDBChisqMinimizer::~HDBChisqMinimizer()
{
}

//
// assignment operators
//
// const HDBChisqMinimizer& HDBChisqMinimizer::operator=( const HDBChisqMinimizer& rhs )
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
HDBChisqMinimizer::estimateParameters( bool aFinalPass )
{
   if( !m_inputMeasurements->errorMatrixOK() )
   {
      cout << "Something wrong with input error matrix." << endl ;
      m_fitStatus = kFitUnsuccessful ;
      return ;
   }

   if( !m_externalMeasurements->errorMatrixOK() )
   {
      cout << "Something wrong with external error matrix." << endl ;
      m_fitStatus = kFitUnsuccessful ;
      return ;
   }

   if( aFinalPass )
   {
      m_inputMeasurements->update( m_fittedParameters.values(),
				   m_fitPredictions,
				   true ) ;
      m_externalMeasurements->update( m_fittedParameters.values(),
				      m_externalFitPredictions,
				      true ) ;
   }

   // Invert input error matrix.
   int ifail ;
   HepSymMatrix inputErrInv =
      m_inputMeasurements->errorMatrix().inverse( ifail ) ;

   if( ifail )
   {
      cout << "Matrix inversion failed: input error matrix." << endl ;
      m_fitStatus = kFitUnsuccessful ;
      return ;
   }

   // Invert external error matrix.
   HepSymMatrix externalErrInv( 1, 0 ) ;
   if( m_externalMeasurements->numberOfValues() > 0 )
   {
      externalErrInv = m_externalMeasurements->errorMatrix().inverse( ifail ) ;

      if( ifail )
      {
	 cout << "Matrix inversion failed: external error matrix." << endl ;
	 m_fitStatus = kFitUnsuccessful ;
	 return ;
      }
   }

   // Calculate chisq.
   HepVector resids = residuals() ;
   HepVector externalResids = externalResiduals() ;

   double internalChisq = inputErrInv.similarity( resids ) ;
   double externalChisq = externalErrInv.similarity( externalResids ) ;
   m_chisq = internalChisq + externalChisq ;

   m_ndof = m_inputMeasurements->numberOfValues() +
      m_externalMeasurements->numberOfValues() -
      m_fittedParameters.numberOfValues() ;

   // Calculate new fitted parameter error matrix.
   HepMatrix residDerivs = residualDerivatives() ;
   HepMatrix externalResidDerivs = externalResidualDerivatives() ;

   HepSymMatrix outputErrorInv =
      inputErrInv.similarity( residDerivs ) +
      externalErrInv.similarity( externalResidDerivs ) ;
   HepSymMatrix outputError = outputErrorInv.inverse( ifail ) ;

   if( m_printDiagnostics )
   {
      cout << "chisq " << m_chisq << " internal only "
	   << internalChisq << endl
	   << "inputErrInv" << inputErrInv
	   << "extErrInv" << externalErrInv
	   << "input params" << m_fittedParameters.values()
	   << "resids" << resids
	   << "residDerivs" << residDerivs
	   << "extResids" << externalResids
	   << "extResidDerivs" << externalResidDerivs
	   << "outputErrorInv" << outputErrorInv
	   << endl ;
   }

   if( ifail != 0 )
   {
      cout << "Matrix inversion failed: output error matrix." << endl ;
      m_fitStatus = kFitUnsuccessful ;
      return ;
   }

   if( !HDBData::errorMatrixOK( outputError ) )
   {
      cout << "Something wrong with output error matrix." << endl ;
      m_fitStatus = kFitUnsuccessful ;
      return ;
   }

   // Calculate change in fitted parameters.
   HepVector deltaParams = outputError * (
      residDerivs * inputErrInv * resids +
      externalResidDerivs * externalErrInv * externalResids ) ;

   if( m_printDiagnostics )
   {
      HepVector deltaInSigma = deltaParams ;
      for( int i = 0 ; i < deltaInSigma.num_row() ; ++i )
      {
	 deltaInSigma[ i ] /= sqrt( outputError[ i ][ i ] ) ;
      }

      HepVector outputErrors( deltaParams.num_row(), 0 ) ;
      HepVector outputFracErrors( deltaParams.num_row(), 0 ) ;
      for( int i = 0 ; i < deltaParams.num_row() ; ++i )
      {
	 outputErrors[ i ] = sqrt( outputError[ i ][ i ] ) ;
	 outputFracErrors[ i ] = outputErrors[ i ] /
	    ( m_fittedParameters.values() + deltaParams )[ i ] ;
      }

      cout << "outputError" << outputError
	   << "delta/err" << deltaInSigma
	   << "output params" << m_fittedParameters.values() + deltaParams
	   << "output errors" << outputErrors
	   << "output frac errors" << outputFracErrors
	   << endl ;
   }

   // Update fitted parameters.
   m_fittedParameters.setValuesAndErrorMatrix(
      m_fittedParameters.values() + deltaParams,
      outputError ) ;

//   if( !aFinalPass )
   {
      // Update input measurements.
      m_inputMeasurements->update( m_fittedParameters.values(),
				   m_fitPredictions,
				   aFinalPass ) ;
      m_externalMeasurements->update( m_fittedParameters.values(),
				      m_externalFitPredictions,
				      aFinalPass ) ;

      // Update chisq with new residuals and updated input error matrix.
      HepVector newResids = residuals() ;
      HepVector newExternalResids = externalResiduals() ;

      inputErrInv = m_inputMeasurements->errorMatrix().inverse( ifail ) ;

      if( m_externalMeasurements->numberOfValues() > 0 )
      {
	 externalErrInv =
	    m_externalMeasurements->errorMatrix().inverse( ifail ) ;
      }

      if( ifail )
      {
	 cout << "Matrix inversion failed: updated error matrices."
	      << endl ;
	 m_fitStatus = kFitUnsuccessful ;
	 return ;
      }
      else
      {
	 m_chisq = inputErrInv.similarity( newResids ) +
	    externalErrInv.similarity( newExternalResids ) ;

	 if( m_printDiagnostics )
	 {
	    cout << "new chisq " << m_chisq << endl ;
	 }

	 if( m_chisq != m_chisq ) // test for NaN
	 {
	    m_fitStatus = kFitUnsuccessful ;
	    return ;
	 }
      }
   }

   m_fitStatus = kFitSuccessful ;
}

//
// const member functions
//

// aSeeds replaced with new estimate.
bool
HDBChisqMinimizer::solveHouseholder( const HepSymMatrix& aInputErrorInv,
				     const HepVector& aResiduals,
				     const HepMatrix& aResidualDerivatives,
				     HepVector& aSeeds ) const
{
   HepVector inputInvDiff =
      aInputErrorInv * ( aResiduals - aResidualDerivatives.T() * aSeeds ) ;

   HepMatrix residDerivsCorr( aResidualDerivatives.num_row(),
			      aResidualDerivatives.num_col() ) ;
   for( int i = 0 ; i < aResidualDerivatives.num_row() ; ++i )
   {
      residDerivsCorr.sub(
	 i + 1, 1,
	 inputInvDiff.T() *
	 m_inputMeasurements->errorMatrixDerivatives( i ) ) ;
   }

   HepMatrix XInv = ( aResidualDerivatives + residDerivsCorr ) *
      aInputErrorInv * aResidualDerivatives.T() ;

   int ifail ;
   XInv.invert( ifail ) ;

   if( ifail != 0 )
   {
      cout << "Matrix inversion failed: solveHouseholder" << endl ;
      return false ;
   }

   HepMatrix Y =
      ( aResidualDerivatives + 0.5 * residDerivsCorr ) * inputInvDiff ;

   HepMatrix secondOrderCorr( XInv.num_row(), XInv.num_col() ) ;
   HepMatrix tmp = XInv.T() * aResidualDerivatives * aInputErrorInv ;
   for( int i = 0 ; i < XInv.num_row() ; ++i )
   {
      secondOrderCorr.sub(
	 i + 1, 1,
	 0.5 * Y.T() *
	 m_inputMeasurements->errorMatrixDerivatives( i ).similarity( tmp ) ) ;

      // Add unit matrix
      secondOrderCorr[ i ][ i ] += 1. ;
   }

   aSeeds += XInv * secondOrderCorr * Y ;
//   aSeeds += XInv * Y ;
   return true ;
}


// aSeeds replaced with new estimate.
bool
HDBChisqMinimizer::iterateHouseholder( const HepSymMatrix& aOutputErrorInv,
				       const HepSymMatrix& aInputErrorInv,
				       const HepVector& aResiduals,
				       const HepMatrix& aResidualDerivatives,
				       HepVector& aSeeds ) const
{
   int nIter = 0 ;
   double deltaChisqNdof = 
      aOutputErrorInv.similarity( aSeeds ) / aSeeds.num_row() ;
   double deltaChisqNdofOld = 0. ;

   if( m_printDiagnostics )
   {
      cout << "deltaParams before iteration" << aSeeds
	   << "deltaChisqNdof " << deltaChisqNdof << endl ;
   }

   do
   {
      if( !solveHouseholder( aInputErrorInv,
			     aResiduals,
			     aResidualDerivatives,
			     aSeeds ) )
      {
	 return false ;
      }

      ++nIter ;
      deltaChisqNdofOld = deltaChisqNdof ;
      deltaChisqNdof =
	 aOutputErrorInv.similarity( aSeeds ) / aSeeds.num_row() ;

      if( m_printDiagnostics )
      {
	 cout << "delta param iteration " << nIter << endl
	      << "deltaParams" << aSeeds
	      << "deltaChisqNdof " << deltaChisqNdof
	      << endl;
      }
   }
   while( fabs( deltaChisqNdof - deltaChisqNdofOld ) > 0.001 &&
	  nIter < 101 ) ;

   return ( nIter != 101 ) ;
}

//
// static member functions
//
