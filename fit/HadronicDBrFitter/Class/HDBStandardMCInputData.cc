// -*- C++ -*-
//
// Package:     <HadronicDBrFitter>
// Module:      HDBStandardMCInputData
// 
// Description: <one line class summary>
//
// Implementation:
//     <Notes on implementation>
//
// Author:      Werner Sun
// Created:     Thu Apr  1 02:17:19 EST 2004
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
#include "HadronicDBrFitter/HDBStandardMCInputData.h"

//
// constants, enums and typedefs
//

static const char* const kFacilityString = "HadronicDBrFitter.HDBStandardMCInputData" ;

// ---- cvs-based strings (Id and Tag with which file was checked out)
static const char* const kIdString  = "$Id: skeleton.cc,v 1.6 2001/01/03 16:25:23 cdj Exp $";
static const char* const kTagString = "$Name:  $";

//
// static data member definitions
//

//
// constructors and destructor
//
HDBStandardMCInputData::HDBStandardMCInputData( bool aSingleTagsExclusive )
   : HDBStandardInputData( aSingleTagsExclusive )
{
}

// HDBStandardMCInputData::HDBStandardMCInputData( const HDBStandardMCInputData& rhs )
// {
//    // do actual copying here; if you implemented
//    // operator= correctly, you may be able to use just say      
//    *this = rhs;
// }

HDBStandardMCInputData::~HDBStandardMCInputData()
{
}

//
// assignment operators
//
// const HDBStandardMCInputData& HDBStandardMCInputData::operator=( const HDBStandardMCInputData& rhs )
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
HDBStandardMCInputData::initialize( const HepVector& aFitParameters,
				    const HDBVariableVector* aFitPredictions )
{
   m_generatedEfficiencyParameters =
      smearedVector( m_efficiencyParameters, m_efficiencyParameterErrors ) ;

   HepMatrix generatedSignalEfficiency =
      generatedSignalEfficiencyValues() +
      uncorrelatedSmearMatrix( m_signalEfficiencyMatrix ) ;
   HepMatrix generatedBackgroundEfficiency =
      generatedBackgroundEfficiencyValues() + 
      uncorrelatedSmearMatrix( m_backgroundEfficiencyMatrix ) ;

   m_generatedBackgroundParameters =
      smearedVector( m_backgroundParameters, m_backgroundParameterErrors ) ;

   HepVector generatedBackground =
      generatedBackgroundValues( aFitParameters ) +
      uncorrelatedSmearVector( m_backgroundVector ) ;

   HepVector measuredYields =
      uncorrelatedSmearVector( m_yieldVector ) +
      generatedSignalEfficiency * m_trueCorrectedYields +
      generatedBackgroundEfficiency * generatedBackground ;

   setYieldParameters( measuredYields ) ; // calculates exclusive yields

   if( m_printDiagnostics )
   {
      cout << "SMEARED" << endl
	   << "eff params" << m_generatedEfficiencyParameters
	   << "signal effs" << generatedSignalEfficiency
	   << "true corrected yields" << m_trueCorrectedYields
	   << "measured yields" << measuredYields
	   << "exclusive yields" << m_yieldParameters ;
   }

   m_yieldParameters = smearedVector( m_yieldParameters,
				      m_yieldParameterErrors ) ;

   if( m_printDiagnostics )
   {
      cout << "smeared exclusive yields" << m_yieldParameters << endl ;
   }

   HDBStandardInputData::initialize( aFitParameters, aFitPredictions ) ;

   // After the first MC trial, don't initialize efficiencies and errors.
   m_initializeYieldsOnly = true ;
}

//
// const member functions
//

//
// static member functions
//

double
HDBStandardMCInputData::randomGaussian( double aMean, double aSigma )
{
//    double s, v1 ;

//    do
//    {
//       double u1 = double( rand() ) / double( RAND_MAX ) ;
//       double u2 = double( rand() ) / double( RAND_MAX ) ;
//       v1 = 2. * u1 - 1. ;
//       double v2 = 2. * u2 - 1. ;
//       s  = v1 * v1 + v2 * v2 ;
//    }
//    while( s > 1. || s == 0. ) ;

//    double rgauss = v1 * sqrt( -2. * log( s ) / s ) ;
//    rgauss = aMean + rgauss * aSigma ;
//    return rgauss ;

   double u1 = double( rand() ) / double( RAND_MAX ) ;
   double u2 ;

   do
   {
      u2 = double( rand() ) / double( RAND_MAX ) ;
   }
   while( u2 == 0. ) ;

   return aMean + sin( M_2PI * u1 ) * sqrt( -2. * log( u2 ) ) * aSigma ;
}

HepVector
HDBStandardMCInputData::smearedVector( const HepVector& aTrueValues,
				       const HepVector& aResolutions )
{
   HepVector tmp( aTrueValues.num_row(), 0 ) ;

   for( int i = 0 ; i < aTrueValues.num_row() ; ++i )
   {
      tmp[ i ] = randomGaussian( aTrueValues[ i ], aResolutions[ i ] ) ;
   }

   return tmp ;
}

HepMatrix
HDBStandardMCInputData::uncorrelatedSmearMatrix( HDBEfficiencyMatrix& aMatrix )
{
   if( aMatrix.numberRows() * aMatrix.numberColumns() == 0 )
   {
      int nrow = aMatrix.numberRows() > 0 ? aMatrix.numberRows() : 1 ;
      int ncol = aMatrix.numberColumns() > 0 ? aMatrix.numberColumns() : 1 ;

      return HepMatrix( nrow, ncol, 0 ) ;
   }
   else
   {
      HepMatrix tmp( aMatrix.numberRows(), aMatrix.numberColumns(), 0 ) ;

      for( int i = 0 ; i < aMatrix.numberRows() ; ++i )
      {
	 for( int j = 0 ; j < aMatrix.numberColumns() ; ++j )
	 {
	    double smearWidth = aMatrix.element( i, j )->uncorrelatedError() ;

	    if( smearWidth != 0. )
	    {
	       tmp[ i ][ j ] = randomGaussian( 0., smearWidth ) ;
	    }
	 }
      }

      return tmp ; 
   }
}

HepVector
HDBStandardMCInputData::uncorrelatedSmearVector( HDBVariableVector& aVector )
{
   if( aVector.numberRows() == 0 )
   {
      return HepVector( 1, 0 ) ;
   }
   else
   {
      HepVector tmp( aVector.numberRows(), 0 ) ;

      for( int i = 0 ; i < aVector.numberRows() ; ++i )
      {
	 double smearWidth = aVector.element( i )->uncorrelatedError() ;

	 if( smearWidth != 0. )
	 {
	    tmp[ i ] = randomGaussian( 0., smearWidth ) ;
	 }
      }

      return tmp ;
   }
}
