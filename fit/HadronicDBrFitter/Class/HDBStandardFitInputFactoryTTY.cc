// -*- C++ -*-
//
// Package:     <HadronicDBrFitter>
// Module:      HDBStandardFitInputFactoryTTY
// 
// Description: <one line class summary>
//
// Implementation:
//     <Notes on implementation>
//
// Author:      Werner Sun
// Created:     Wed May 26 21:53:41 EDT 2004
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
#include <assert.h>

// user include files
//#include "Experiment/report.h"
#include "HadronicDBrFitter/HDBStandardFitInputFactoryTTY.h"
#include "HadronicDBrFitter/HDBStandardMCInputData.h"

//
// constants, enums and typedefs
//

static const char* const kFacilityString = "HadronicDBrFitter.HDBStandardFitInputFactoryTTY" ;

// ---- cvs-based strings (Id and Tag with which file was checked out)
static const char* const kIdString  = "$Id: skeleton.cc,v 1.7 2004/02/12 02:14:38 pcs Exp $";
static const char* const kTagString = "$Name:  $";

//
// static data member definitions
//

//
// constructors and destructor
//
HDBStandardFitInputFactoryTTY::HDBStandardFitInputFactoryTTY(
   bool aSingleTagsExclusive,
   bool aGenerateMC )
   : HDBStandardFitInputFactory( aSingleTagsExclusive, aGenerateMC )
{
   m_constantsUncorr = HepSymMatrix( kNumParameterTypes, 0 ) ;
   m_constantsUncorr[ kD0 ][ kD0Bar ] = 1. ;
   m_constantsUncorr[ kD0 ][ kDUnflavored ] = 1. ;
   m_constantsUncorr[ kD0 ][ kDNeutral ] = 1. ;
   m_constantsUncorr[ kD0Bar ][ kDUnflavored ] = 1. ;
   m_constantsUncorr[ kD0Bar ][ kDNeutral ] = 1. ;
   m_constantsUncorr[ kDUnflavored ][ kDUnflavored ] = 2. ;
   m_constantsUncorr[ kDUnflavored ][ kDNeutral ] = 2. ;
   m_constantsUncorr[ kDNeutral ][ kDNeutral ] = 2. ;
   m_constantsUncorr[ kDPlus ][ kDMinus ] = 1. ;
   m_constantsUncorr[ kDPlus ][ kDCharged ] = 1. ;
   m_constantsUncorr[ kDMinus ][ kDCharged ] = 1. ;
   m_constantsUncorr[ kDCharged ][ kDCharged ] = 2. ;
   m_constantsUncorr[ kDsPlus ][ kDsMinus ] = 1. ;
   m_constantsUncorr[ kDsPlus ][ kDs ] = 1. ;
   m_constantsUncorr[ kDsMinus ][ kDs ] = 1. ;
   m_constantsUncorr[ kDs ][ kDs ] = 2. ;

   m_numTermsCOdd = HepSymMatrix( kNumParameterTypes, 0 ) ;
   m_numTermsCOdd[ kD0Flavored ][ kD0Flavored ] = 8. ;
   m_numTermsCOdd[ kD0Flavored ][ kD0BarFlavored ] = 4. ;
   m_numTermsCOdd[ kD0Flavored ][ kD0SL ] = 1. ;
   m_numTermsCOdd[ kD0Flavored ][ kD0BarSL ] = 1. ;
   m_numTermsCOdd[ kD0Flavored ][ kCPPlus ] = 3. ;
   m_numTermsCOdd[ kD0Flavored ][ kCPMinus ] = 3. ;
   m_numTermsCOdd[ kD0BarFlavored ][ kD0BarFlavored ] = 8. ;
   m_numTermsCOdd[ kD0BarFlavored ][ kD0SL ] = 1. ;
   m_numTermsCOdd[ kD0BarFlavored ][ kD0BarSL ] = 1. ;
   m_numTermsCOdd[ kD0BarFlavored ][ kCPPlus ] = 3. ;
   m_numTermsCOdd[ kD0BarFlavored ][ kCPMinus ] = 3. ;
   m_numTermsCOdd[ kD0SL ][ kD0SL ] = 2. ;
   m_numTermsCOdd[ kD0SL ][ kD0BarSL ] = 1. ;
   m_numTermsCOdd[ kD0SL ][ kCPPlus ] = 1. ;
   m_numTermsCOdd[ kD0SL ][ kCPMinus ] = 1. ;
   m_numTermsCOdd[ kD0BarSL ][ kD0BarSL ] = 2. ;
   m_numTermsCOdd[ kD0BarSL ][ kCPPlus ] = 1. ;
   m_numTermsCOdd[ kD0BarSL ][ kCPMinus ] = 1. ;
   m_numTermsCOdd[ kCPPlus ][ kCPPlus ] = 0. ;
   m_numTermsCOdd[ kCPPlus ][ kCPMinus ] = 1. ;
   m_numTermsCOdd[ kCPMinus ][ kCPMinus ] = 0. ;

   m_numTermsCEven = HepSymMatrix( kNumParameterTypes, 0 ) ;
   m_numTermsCEven[ kD0Flavored ][ kD0Flavored ] = 5. ;
   m_numTermsCEven[ kD0Flavored ][ kD0BarFlavored ] = 8. ;
   m_numTermsCEven[ kD0Flavored ][ kD0SL ] = 3. ;
   m_numTermsCEven[ kD0Flavored ][ kD0BarSL ] = 3. ;
   m_numTermsCEven[ kD0Flavored ][ kCPPlus ] = 6. ;
   m_numTermsCEven[ kD0Flavored ][ kCPMinus ] = 6. ;
   m_numTermsCEven[ kD0BarFlavored ][ kD0BarFlavored ] = 5. ;
   m_numTermsCEven[ kD0BarFlavored ][ kD0SL ] = 3. ;
   m_numTermsCEven[ kD0BarFlavored ][ kD0BarSL ] = 3. ;
   m_numTermsCEven[ kD0BarFlavored ][ kCPPlus ] = 6. ;
   m_numTermsCEven[ kD0BarFlavored ][ kCPMinus ] = 6. ;
   m_numTermsCEven[ kD0SL ][ kD0SL ] = 2. ;
   m_numTermsCEven[ kD0SL ][ kD0BarSL ] = 1. ;
   m_numTermsCEven[ kD0SL ][ kCPPlus ] = 2. ;
   m_numTermsCEven[ kD0SL ][ kCPMinus ] = 2. ;
   m_numTermsCEven[ kD0BarSL ][ kD0BarSL ] = 2. ;
   m_numTermsCEven[ kD0BarSL ][ kCPPlus ] = 2. ;
   m_numTermsCEven[ kD0BarSL ][ kCPMinus ] = 2. ;
   m_numTermsCEven[ kCPPlus ][ kCPPlus ] = 1. ;
   m_numTermsCEven[ kCPPlus ][ kCPMinus ] = 0. ;
   m_numTermsCEven[ kCPMinus ][ kCPMinus ] = 1. ;

   m_numTermsCBoth = m_numTermsCOdd + m_numTermsCEven ;
   // Remove terms with Rmix or x^2.
//    m_numTermsCBoth[ kD0Flavored ][ kD0Flavored ] =
//       m_numTermsCEven[ kD0Flavored ][ kD0Flavored ] ;
//    m_numTermsCBoth[ kD0BarFlavored ][ kD0BarFlavored ] =
//       m_numTermsCEven[ kD0BarFlavored ][ kD0BarFlavored ] ;
//    m_numTermsCBoth[ kD0SL ][ kD0SL ] = 0. ;
//    m_numTermsCBoth[ kD0BarSL ][ kD0BarSL ] = 0. ;

   m_numCOddTermsCBoth = m_numTermsCOdd ;
   // Remove terms with Rmix or x^2.
//    m_numCOddTermsCBoth[ kD0Flavored ][ kD0Flavored ] = 0. ;
//    m_numCOddTermsCBoth[ kD0BarFlavored ][ kD0BarFlavored ] = 0. ;
//    m_numCOddTermsCBoth[ kD0SL ][ kD0SL ] = 0. ;
//    m_numCOddTermsCBoth[ kD0BarSL ][ kD0BarSL ] = 0. ;
}

// HDBStandardFitInputFactoryTTY::HDBStandardFitInputFactoryTTY( const HDBStandardFitInputFactoryTTY& rhs )
// {
//    // do actual copying here; if you implemented
//    // operator= correctly, you may be able to use just say      
//    *this = rhs;
// }

HDBStandardFitInputFactoryTTY::~HDBStandardFitInputFactoryTTY()
{
}

//
// assignment operators
//
// const HDBStandardFitInputFactoryTTY& HDBStandardFitInputFactoryTTY::operator=( const HDBStandardFitInputFactoryTTY& rhs )
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
HDBStandardFitInputFactoryTTY::makeInputData()
{
   if( m_generateMC )
   {
      getBackgrounds() ;
      getEfficiencies() ;
      getInputYieldsAndErrorsMC() ;
   }
   else
   {
      getInputYieldsAndErrors() ;
      getBackgrounds() ;
      getEfficiencies() ;
   }
}


void
HDBStandardFitInputFactoryTTY::makeFitPredictions()
{
   if( m_fitParametersDefined )
   {
      return ;
   }

   delete m_fitPredictions ;
   m_fitParameterNames.clear() ;
   m_singleTagPredictions.clear() ;
   m_doubleTagPredictions.clear() ;
   m_particleContents.clear() ;


   vector< pair< int, int > > doubleToSingleCrossReference ;
   string singleDouble ;
   SampleType sampleType ;

   // Ask user to enter list of measurements and form an
   // HDBVariableMatrixElement for each one.
   do
   {
//       cout << "New mode type (single/double/end): " ;
      cin >> singleDouble ;

      bool sampleTypeOK ;
      string sampleTypeStr ;

      if( singleDouble == "single" ||
	  singleDouble == "double" )
      {
	 do
	 {
// 	    cout << "Enter sample type (D+D-/Ds+Ds-/D0D0BarUncorrelated/D0D0BarC-/D0D0BarC-WithC+/D0D0BarC+/D0D0BarC+WithC-): " ;
	    cin >> sampleTypeStr ;

	    sampleTypeOK = true ;

	    if( sampleTypeStr == "D+D-" )
	    {
	       sampleType = kDPlusDMinus ;
	    }
	    else if( sampleTypeStr == "Ds+Ds-" )
	    {
	       sampleType = kDsPlusDsMinus ;
	    }
	    else if( sampleTypeStr == "D0D0BarUncorrelated" )
	    {
	       sampleType = kD0D0BarUncorrelated ;
	    }
	    else if( sampleTypeStr == "D0D0BarC-" )
	    {
	       sampleType = kD0D0BarCOdd ;
	    }
	    else if( sampleTypeStr == "D0D0BarC-WithC+" )
	    {
	       sampleType = kD0D0BarCOddWithEven ;
	    }
	    else if( sampleTypeStr == "D0D0BarC+" )
	    {
	       sampleType = kD0D0BarCEven ;
	    }
	    else if( sampleTypeStr == "D0D0BarC+WithC-" )
	    {
	       sampleType = kD0D0BarCEvenWithOdd ;
	    }
	    else
	    {
	       sampleTypeOK = false ;
	    }
	 }
	 while( !sampleTypeOK ) ;
      }

      int nFitParamsBefore = m_fitParameterNames.size() ;

      if( singleDouble == "single" )
      {
         HDBInputInfoHolder inputInfo ;
         HDBVariableMatrixElement matrixElement ;
	 HepVector particleContent ;

         string mode ;
//          cout << "Enter mode: " ;
         cin >> mode ;

         bool knownMode = getInputInfo( mode,
					sampleType,
                                        inputInfo,
					particleContent,
					m_fitParameterNames ) ;

         if( !knownMode )
         {
            cout << "Unknown mode.  Try again." << endl ;
         }
         else if( inputInfo.numberInputs() != 1 )
         {
            cout << "Not a single tag." << endl ;
         }
         else
         {
	    // Fill info in HDBVariableMatrixElement.
            FitParameterType paramType = inputInfo.fitParameterType( 0 ) ;

	    HepVector constants ;
	    HepMatrix powers ;

	    if( sampleType == kDPlusDMinus ||
		sampleType == kDsPlusDsMinus ||
		sampleType == kD0D0BarUncorrelated )
	    {
	       constants = HepVector( 1 ) ;
	       powers = HepMatrix( 1, m_fitParameterNames.size(), 0 ) ;

	       // Set constants.
	       if( paramType == kDUnflavored ||
		   paramType == kDCharged ||
		   paramType == kDs ||
		   paramType == kDNeutral )
	       {
		  constants[ 0 ] = 2. ;
	       }
	       else
	       {
		  constants[ 0 ] = 1. ;
	       }

	       // Set NDDBar parameter.
	       if( sampleType == kDPlusDMinus )
	       {
		  powers[ 0 ][ m_nDPlusDMinusIndex ] = 1. ;
	       }
	       else if( sampleType == kDsPlusDsMinus )
	       {
		  powers[ 0 ][ m_nDsPlusDsMinusIndex ] = 1. ;
	       }
	       else
	       {
		  powers[ 0 ][ m_nD0D0BarIndex ] = 1. ;
	       }

	       // Set branching fraction parameter.
	       powers[ 0 ][ inputInfo.fitParameterNumber( 0 ) ] = 1. ;
	    }
	    else  // Correlated D0D0Bar
	    {
	       int nRows = 1 ;

	       // Determine number of terms.
	       if( paramType == kD0Flavored ||
		   paramType == kD0BarFlavored )
	       {
		  nRows = 3 ;
	       }
	       else if( paramType == kCPPlus ||
			paramType == kCPMinus )
	       {
		  nRows = 2 ;
	       }

	       if( sampleType == kD0D0BarCOddWithEven ||
		   sampleType == kD0D0BarCEvenWithOdd )
	       {
		  nRows *= 2 ;
	       }

	       constants = HepVector( nRows ) ;
	       powers = HepMatrix( nRows, m_fitParameterNames.size(), 0 ) ;

	       // Set ND0D0Bar and branching fraction parameters.
	       for( int i = 0 ; i < nRows ; ++i )
	       {
		  if( sampleType == kD0D0BarCOdd ||
		      sampleType == kD0D0BarCOddWithEven )
		  {
		     powers[ i ][ m_nD0D0BarCOddIndex ] = 1. ;
		  }
		  else
		  {
		     powers[ i ][ m_nD0D0BarCEvenIndex ] = 1. ;
		  }

		  powers[ i ][ inputInfo.fitParameterNumber( 0 ) ] = 1. ;
	       }

	       // Set admixture fractions.
	       if( sampleType == kD0D0BarCOddWithEven ||
		   sampleType == kD0D0BarCEvenWithOdd )
	       {
		  for( int i = nRows/2 ; i < nRows ; ++i )
		  {
		     if( sampleType == kD0D0BarCOddWithEven )
		     {
			powers[ i ][ m_nD0D0BarCOddEvenFracIndex ] = 1. ;
		     }
		     else
		     {
			powers[ i ][ m_nD0D0BarCEvenOddFracIndex ] = 1. ;
		     }
		  }
	       }

	       // Set constants.
	       for( int i = 0 ; i < nRows ; ++i )
	       {
		  if( paramType == kCPPlus ||
		      paramType == kCPMinus )
		  {
		     constants[ i ] = 2. ;
		  }
		  else
		  {
		     constants[ i ] = 1. ;
		  }
	       }

	       // Flip sign of y term for CP+.
	       if( paramType == kCPPlus )
	       {
		  constants[ 1 ] = -2. ;

		  if( sampleType == kD0D0BarCOddWithEven ||
		      sampleType == kD0D0BarCEvenWithOdd )
		  {
		     constants[ 3 ] = -2. ;
		  }
	       }

	       // Set TQCA parameters.
	       if( paramType == kD0Flavored ||
		   paramType == kD0BarFlavored )
	       {
		  powers[ 1 ][ m_r2Index ] = 1. ;
		  powers[ 2 ][ m_rzIndex ] = 1. ;
		  powers[ 2 ][ m_yIndex ] = 1. ;

		  if( sampleType == kD0D0BarCOddWithEven ||
		      sampleType == kD0D0BarCEvenWithOdd )
		  {
		     powers[ 4 ][ m_r2Index ] = 1. ;
		     powers[ 5 ][ m_rzIndex ] = 1. ;
		     powers[ 5 ][ m_yIndex ] = 1. ;
		  }
	       }
	       else if( paramType == kCPPlus ||
			paramType == kCPMinus )
	       {
		  powers[ 1 ][ m_yIndex ] = 1. ;

		  if( sampleType == kD0D0BarCOddWithEven ||
		      sampleType == kD0D0BarCEvenWithOdd )
		  {
		     powers[ 3 ][ m_yIndex ] = 1. ;
		  }
	       }
	    }

            matrixElement.setName( mode ) ;
            matrixElement.setConstantVector( constants ) ;
            matrixElement.setPowerMatrix( powers ) ;
	    matrixElement.setComment3( sampleTypeStr ) ;
            m_singleTagPredictions.push_back( matrixElement ) ;
	    m_particleContents.push_back( particleContent ) ;
         }
      }
      else if( singleDouble == "double" )
      {
         HDBInputInfoHolder inputInfo ;
         HDBVariableMatrixElement matrixElement ;
	 HepVector particleContent1 ;
	 HepVector particleContent2 ;

	 // Get first mode.
         string mode1 ;
//          cout << "Enter first mode: " ;
         cin >> mode1 ;

         bool knownMode1 = getInputInfo( mode1,
					 sampleType,
                                         inputInfo,
                                         particleContent1,
					 m_fitParameterNames ) ;

         if( !knownMode1 )
         {
            cout << "Unknown mode.  Try again." << endl ;
         }
         else
         {
	    // Get second mode.
            string mode2 ;
//             cout << "Enter second mode: " ;
            cin >> mode2 ;

            bool knownMode2 = getInputInfo( mode2,
					    sampleType,
                                            inputInfo,
                                            particleContent2,
					    m_fitParameterNames ) ;

            if( !knownMode2 )
            {
               cout << "Unknown mode.  Try again." << endl ;
            }
            else if( inputInfo.numberInputs() != 2 )
            {
               cout << "Not a double tag." << endl ;
            }
            else
            {
	       // Check that the two modes are a valid combination and
	       // form matrices for HDBVariableMatrixElement.
               bool doubleTagValid = true ;
               FitParameterType paramType1 = inputInfo.fitParameterType( 0 ) ;
               FitParameterType paramType2 = inputInfo.fitParameterType( 1 ) ;

	       HepVector constants ;
	       HepMatrix powers ;

	       if( sampleType == kDPlusDMinus ||
		   sampleType == kDsPlusDsMinus ||
		   sampleType == kD0D0BarUncorrelated )
	       {
		  constants = HepVector( 1 ) ;
		  powers = HepMatrix( 1, m_fitParameterNames.size(), 0 ) ;

		  // Set constants.  Use a symmetric matrix to encode
		  // allowed combinations.
		  if( m_constantsUncorr[ paramType1 ][ paramType2 ] != 0. )
		  {
		     if( inputInfo.fitParameterNumber( 0 ) ==
			 inputInfo.fitParameterNumber( 1 ) )
		     {
			constants[ 0 ] = 1. ;
		     }
		     else
		     {
			constants[ 0 ] =
			   m_constantsUncorr[ paramType1 ][ paramType2 ] ;
		     }


		     // Set NDDBar parameter.
		     if( sampleType == kDPlusDMinus )
		     {
			powers[ 0 ][ m_nDPlusDMinusIndex ] = 1. ;
		     }
		     else if( sampleType == kDsPlusDsMinus )
		     {
			powers[ 0 ][ m_nDsPlusDsMinusIndex ] = 1. ;
		     }
		     else
		     {
			powers[ 0 ][ m_nD0D0BarIndex ] = 1. ;
		     }

		     // Set branching fraction parameters.
		     powers[ 0 ][ inputInfo.fitParameterNumber( 0 ) ] += 1. ;
		     powers[ 0 ][ inputInfo.fitParameterNumber( 1 ) ] += 1. ;
		  }
		  else
		  {
		     doubleTagValid = false ;
		     cout << "Invalid combination of modes.  Try again."
			  << endl ;

		     // Remove the outputs just added.
		     for( int i = 0 ;
			  i < m_fitParameterNames.size() - nFitParamsBefore ;
			  ++i )
		     {
			m_fitParameterNames.pop_back() ;
		     }
		  }
	       }
	       else  // Correlated D0D0Bar
	       {
		  // Figure out number of terms.
		  int nRows ;
		  if( sampleType == kD0D0BarCOdd )
		  {
		     nRows = int( m_numTermsCOdd[ paramType1 ][ paramType2 ] );
		  }
		  else if( sampleType == kD0D0BarCEven )
		  {
		     nRows = int( m_numTermsCEven[ paramType1 ][ paramType2 ]);
		  }
		  else
		  {
		     nRows = int( m_numTermsCBoth[ paramType1 ][ paramType2 ]);
		  }

		  if( nRows != 0 )
		  {
		     constants = HepVector( nRows ) ;
		     powers =
			HepMatrix( nRows, m_fitParameterNames.size(), 0 ) ;

		     // Set ND0D0Bar and branching fraction parameters.
		     for ( int i = 0 ; i < nRows ; ++i )
		     {
			if( sampleType == kD0D0BarCOdd ||
			    sampleType == kD0D0BarCOddWithEven )
			{
			   powers[ i ][ m_nD0D0BarCOddIndex ] = 1. ;
			}
			else
			{
			   powers[ i ][ m_nD0D0BarCEvenIndex ] = 1. ;
			}

			powers[ i ][ inputInfo.fitParameterNumber( 0 ) ] += 1.;
			powers[ i ][ inputInfo.fitParameterNumber( 1 ) ] += 1.;
		     }

		     // Set admixture fractions.
		     int offsetCOdd = 0 ;

		     if( sampleType == kD0D0BarCOddWithEven ||
			 sampleType == kD0D0BarCEvenWithOdd )
		     {
			offsetCOdd = int(
			   m_numCOddTermsCBoth[ paramType1 ][ paramType2 ] ) ;

			if( sampleType == kD0D0BarCOddWithEven )
			{
			   for( int i = offsetCOdd ; i < nRows ; ++i )
			   {
			      powers[ i ][ m_nD0D0BarCOddEvenFracIndex ] = 1. ;
			   }
			}
			else
			{
			   for( int i = 0 ; i < offsetCOdd ; ++i )
			   {
			      powers[ i ][ m_nD0D0BarCEvenOddFracIndex ] = 1. ;
			   }
			}
		     }

		     // Set constants and TQCA parameters.

		     // ff and fbarfbar
		     if( ( paramType1 == kD0Flavored &&
			   paramType2 == kD0Flavored ) ||
			 ( paramType1 == kD0BarFlavored &&
			   paramType2 == kD0BarFlavored ) )
		     {
			if( sampleType == kD0D0BarCOdd )
			{
			   // C-: (y^2+x^2)(1+2r^2-r^2z^2+r^4)/2
			   constants[ 0 ] = 0.5 ;
			   powers[ 0 ][ m_yIndex ] = 2. ;

			   constants[ 1 ] = 1. ;
			   powers[ 1 ][ m_yIndex ] = 2. ;
			   powers[ 1 ][ m_r2Index ] = 1. ;

			   constants[ 2 ] = -0.5 ;
			   powers[ 2 ][ m_yIndex ] = 2. ;
			   powers[ 2 ][ m_rzIndex ] = 2. ;

			   constants[ 3 ] = 0.5 ;
			   powers[ 3 ][ m_yIndex ] = 2. ;
			   powers[ 3 ][ m_r2Index ] = 2. ;

			   constants[ 4 ] = 0.5 ;
			   powers[ 4 ][ m_x2Index ] = 1. ;

			   constants[ 5 ] = 1. ;
			   powers[ 5 ][ m_x2Index ] = 1. ;
			   powers[ 5 ][ m_r2Index ] = 1. ;

			   constants[ 6 ] = -0.5 ;
			   powers[ 6 ][ m_x2Index ] = 1. ;
			   powers[ 6 ][ m_rzIndex ] = 2. ;

			   constants[ 7 ] = 0.5 ;
			   powers[ 7 ][ m_x2Index ] = 1. ;
			   powers[ 7 ][ m_r2Index ] = 2. ;
			}
			else if( sampleType == kD0D0BarCEven )
// 			else
			{
			   // C+: 4(r^2+rzy/2-rwx/2+r^3zy/2+r^3wx/2)
			   constants[ 0 ] = 4. ;
			   powers[ 0 ][ m_r2Index ] = 1. ;

			   constants[ 1 ] = 2. ;
			   powers[ 1 ][ m_rzIndex ] = 1. ;
			   powers[ 1 ][ m_yIndex ] = 1. ;

			   constants[ 2 ] = -2. ;
			   powers[ 2 ][ m_rwxIndex ] = 1. ;

			   constants[ 3 ] = 2. ;
			   powers[ 3 ][ m_r2Index ] = 1. ;
			   powers[ 3 ][ m_rzIndex ] = 1. ;
			   powers[ 3 ][ m_yIndex ] = 1. ;

			   constants[ 4 ] = 2. ;
			   powers[ 4 ][ m_r2Index ] = 1. ;
			   powers[ 4 ][ m_rwxIndex ] = 1. ;

			   if( mode1 == mode2 )
			   {
			      constants *= 0.5 ;
			   }
			}
			else
			{
			   // C+: 4(r^2+rzy/2-rwx/2+r^3zy/2+r^3wx/2)
			   constants[ 8 ] = 4. ;
			   powers[ 8 ][ m_r2Index ] = 1. ;

			   constants[ 9 ] = 2. ;
			   powers[ 9 ][ m_rzIndex ] = 1. ;
			   powers[ 9 ][ m_yIndex ] = 1. ;

			   constants[ 10 ] = -2. ;
			   powers[ 10 ][ m_rwxIndex ] = 1. ;

			   constants[ 11 ] = 2. ;
			   powers[ 11 ][ m_r2Index ] = 1. ;
			   powers[ 11 ][ m_rzIndex ] = 1. ;
			   powers[ 11 ][ m_yIndex ] = 1. ;

			   constants[ 12 ] = 2. ;
			   powers[ 12 ][ m_r2Index ] = 1. ;
			   powers[ 12 ][ m_rwxIndex ] = 1. ;

			   if( mode1 == mode2 )
			   {
			      constants *= 0.5 ;
			   }

			   // C-: (y^2+x^2)(1+2r^2-r^2z^2+r^4)/2
			   constants[ 0 ] = 0.5 ;
			   powers[ 0 ][ m_yIndex ] = 2. ;

			   constants[ 1 ] = 1. ;
			   powers[ 1 ][ m_yIndex ] = 2. ;
			   powers[ 1 ][ m_r2Index ] = 1. ;

			   constants[ 2 ] = -0.5 ;
			   powers[ 2 ][ m_yIndex ] = 2. ;
			   powers[ 2 ][ m_rzIndex ] = 2. ;

			   constants[ 3 ] = 0.5 ;
			   powers[ 3 ][ m_yIndex ] = 2. ;
			   powers[ 3 ][ m_r2Index ] = 2. ;

			   constants[ 4 ] = 0.5 ;
			   powers[ 4 ][ m_x2Index ] = 1. ;

			   constants[ 5 ] = 1. ;
			   powers[ 5 ][ m_x2Index ] = 1. ;
			   powers[ 5 ][ m_r2Index ] = 1. ;

			   constants[ 6 ] = -0.5 ;
			   powers[ 6 ][ m_x2Index ] = 1. ;
			   powers[ 6 ][ m_rzIndex ] = 2. ;

			   constants[ 7 ] = 0.5 ;
			   powers[ 7 ][ m_x2Index ] = 1. ;
			   powers[ 7 ][ m_r2Index ] = 2. ;
			}
		     }

		     // ffbar
		     else if( ( paramType1 == kD0Flavored &&
				paramType2 == kD0BarFlavored ) ||
			      ( paramType1 == kD0BarFlavored &&
				paramType2 == kD0Flavored ) )
		     {
			if( sampleType != kD0D0BarCEven )
			{
			   // C-: 1 + 2r^2 - r^2z^2 + r^4
			   constants[ 0 ] = 1. ;

			   constants[ 1 ] = 2. ;
			   powers[ 1 ][ m_r2Index ] = 1. ;

			   constants[ 2 ] = -1. ;
			   powers[ 2 ][ m_rzIndex ] = 2. ;

			   constants[ 3 ] = 1. ;
			   powers[ 3 ][ m_r2Index ] = 2. ;
			}

			if( sampleType != kD0D0BarCOdd )
			{
			   // C+: 1-2r^2+r^2z^2+r^4+2rzy+2rwx+2r^3zy-2r^3wx
			   constants[ 0 + offsetCOdd ] = 1. ;

			   constants[ 1 + offsetCOdd ] = -2. ;
			   powers[ 1 + offsetCOdd ][ m_r2Index ] = 1. ;

			   constants[ 2 + offsetCOdd ] = 1. ;
			   powers[ 2 + offsetCOdd ][ m_rzIndex ] = 2. ;

			   constants[ 3 + offsetCOdd ] = 1. ;
			   powers[ 3 + offsetCOdd ][ m_r2Index ] = 2. ;

			   constants[ 4 + offsetCOdd ] = 2. ;
			   powers[ 4 + offsetCOdd ][ m_rzIndex ] = 1. ;
			   powers[ 4 + offsetCOdd ][ m_yIndex ] = 1. ;

			   constants[ 5 + offsetCOdd ] = 2. ;
			   powers[ 5 + offsetCOdd ][ m_rwxIndex ] = 1. ;

			   constants[ 6 + offsetCOdd ] = 2. ;
			   powers[ 6 + offsetCOdd ][ m_r2Index ] = 1. ;
			   powers[ 6 + offsetCOdd ][ m_rzIndex ] = 1. ;
			   powers[ 6 + offsetCOdd ][ m_yIndex ] = 1. ;

			   constants[ 7 + offsetCOdd ] = -2. ;
			   powers[ 7 + offsetCOdd ][ m_r2Index ] = 1. ;
			   powers[ 7 + offsetCOdd ][ m_rwxIndex ] = 1. ;
			}
		     }

		     // fl+ and fbarl- (DCS)
		     else if( ( paramType1 == kD0Flavored &&
				paramType2 == kD0SL ) ||
			      ( paramType1 == kD0SL &&
				paramType2 == kD0Flavored ) ||
			      ( paramType1 == kD0BarFlavored &&
				paramType2 == kD0BarSL ) ||
			      ( paramType1 == kD0BarSL &&
				paramType2 == kD0BarFlavored ) )
		     {
			if( sampleType != kD0D0BarCEven )
			{
			   // C-: r^2
			   constants[ 0 ] = 1. ;
			   powers[ 0 ][ m_r2Index ] = 1. ;
			}

			if( sampleType != kD0D0BarCOdd )
			{
			   // C+: r^2 + rzy - rwx
			   constants[ 0 + offsetCOdd ] = 1. ;
			   powers[ 0 + offsetCOdd ][ m_r2Index ] = 1. ;

			   constants[ 1 + offsetCOdd ] = 1. ;
			   powers[ 1 + offsetCOdd ][ m_rzIndex ] = 1. ;
			   powers[ 1 + offsetCOdd ][ m_yIndex ] = 1. ;

			   constants[ 2 + offsetCOdd ] = -1. ;
			   powers[ 2 + offsetCOdd ][ m_rwxIndex ] = 1. ;
			}
		     }

		     // fl- and fbarl+ (CF)
		     else if( ( paramType1 == kD0Flavored &&
				paramType2 == kD0BarSL ) ||
			      ( paramType1 == kD0BarSL &&
				paramType2 == kD0Flavored ) ||
			      ( paramType1 == kD0BarFlavored &&
				paramType2 == kD0SL ) ||
			      ( paramType1 == kD0SL &&
				paramType2 == kD0BarFlavored ) )
		     {
			if( sampleType != kD0D0BarCEven )
			{
			   // C-: 1
			   constants[ 0 ] = 1. ;
			}

			if( sampleType != kD0D0BarCOdd )
			{
			   // C+: 1 + rzy + rwx
			   constants[ 0 + offsetCOdd ] = 1. ;

			   constants[ 1 + offsetCOdd ] = 1. ;
			   powers[ 1 + offsetCOdd ][ m_rzIndex ] = 1. ;
			   powers[ 1 + offsetCOdd ][ m_yIndex ] = 1. ;

			   constants[ 2 + offsetCOdd ] = 1. ;
			   powers[ 2 + offsetCOdd ][ m_rwxIndex ] = 1. ;
			}
		     }

		     // fS+ and fbarS+
		     else if( ( ( paramType1 == kD0Flavored ||
				  paramType1 == kD0BarFlavored ) &&
				paramType2 == kCPPlus ) ||
			      ( paramType1 == kCPPlus &&
				( paramType2 == kD0Flavored ||
				  paramType2 == kD0BarFlavored ) ) )
		     {
			if( sampleType != kD0D0BarCEven )
			{
			   // C-: 1 + r^2 + rz
			   constants[ 0 ] = 1. ;

			   constants[ 1 ] = 1. ;
			   powers[ 1 ][ m_r2Index ] = 1. ;

			   constants[ 2 ] = 1. ;
			   powers[ 2 ][ m_rzIndex ] = 1. ;
			}

			if( sampleType != kD0D0BarCOdd )
			{
			   // C+: ( 1 + r^2 - rz )( 1 - 2y )
			   constants[ 0 + offsetCOdd ] = 1. ;

			   constants[ 1 + offsetCOdd ] = 1. ;
			   powers[ 1 + offsetCOdd ][ m_r2Index ] = 1. ;

			   constants[ 2 + offsetCOdd ] = -1. ;
			   powers[ 2 + offsetCOdd ][ m_rzIndex ] = 1. ;

			   constants[ 3 + offsetCOdd ] = -2. ;
			   powers[ 3 + offsetCOdd ][ m_yIndex ] = 1. ;

			   constants[ 4 + offsetCOdd ] = -2. ;
			   powers[ 4 + offsetCOdd ][ m_yIndex ] = 1. ;
			   powers[ 4 + offsetCOdd ][ m_r2Index ] = 1. ;

			   constants[ 5 + offsetCOdd ] = 2. ;
			   powers[ 5 + offsetCOdd ][ m_yIndex ] = 1. ;
			   powers[ 5 + offsetCOdd ][ m_rzIndex ] = 1. ;
			}
		     }

		     // fS- and fbarS-
		     else if( ( ( paramType1 == kD0Flavored ||
				  paramType1 == kD0BarFlavored ) &&
				paramType2 == kCPMinus ) ||
			      ( paramType1 == kCPMinus &&
				( paramType2 == kD0Flavored ||
				  paramType2 == kD0BarFlavored ) ) )
		     {
			if( sampleType != kD0D0BarCEven )
			{
			   // C-: 1 + r^2 - rz
			   constants[ 0 ] = 1. ;

			   constants[ 1 ] = 1. ;
			   powers[ 1 ][ m_r2Index ] = 1. ;

			   constants[ 2 ] = -1. ;
			   powers[ 2 ][ m_rzIndex ] = 1. ;
			}

			if( sampleType != kD0D0BarCOdd )
			{
			   // C+: ( 1 + r^2 + rz )( 1 + 2y )
			   constants[ 0 + offsetCOdd ] = 1. ;

			   constants[ 1 + offsetCOdd ] = 1. ;
			   powers[ 1 + offsetCOdd ][ m_r2Index ] = 1. ;

			   constants[ 2 + offsetCOdd ] = 1. ;
			   powers[ 2 + offsetCOdd ][ m_rzIndex ] = 1. ;

			   constants[ 3 + offsetCOdd ] = 2. ;
			   powers[ 3 + offsetCOdd ][ m_yIndex ] = 1. ;

			   constants[ 4 + offsetCOdd ] = 2. ;
			   powers[ 4 + offsetCOdd ][ m_yIndex ] = 1. ;
			   powers[ 4 + offsetCOdd ][ m_r2Index ] = 1. ;

			   constants[ 5 + offsetCOdd ] = 2. ;
			   powers[ 5 + offsetCOdd ][ m_yIndex ] = 1. ;
			   powers[ 5 + offsetCOdd ][ m_rzIndex ] = 1. ;
			}
		     }

		     // l+l+ and l-l-
		     else if( ( paramType1 == kD0SL &&
				paramType2 == kD0SL ) ||
			      ( paramType1 == kD0BarSL &&
				paramType2 == kD0BarSL ) )
		     {
			if( sampleType != kD0D0BarCEven )
			{
			   // C-: ( y^2 + x^2 ) / 2
			   constants[ 0 ] = 0.5 ;
			   powers[ 0 ][ m_yIndex ] = 2. ;

			   constants[ 1 ] = 0.5 ;
			   powers[ 1 ][ m_x2Index ] = 1. ;
			}

			if( sampleType != kD0D0BarCOdd )
			{
			   // C+: 3 ( y^2 + x^2 ) / 2
			   constants[ 0 + offsetCOdd ] = 1.5 ;
			   powers[ 0 + offsetCOdd ][ m_yIndex ] = 2. ;

			   constants[ 1 + offsetCOdd ] = 1.5 ;
			   powers[ 1 + offsetCOdd ][ m_x2Index ] = 1. ;
			}

		     }

		     // l+l-
		     else if( ( paramType1 == kD0SL &&
				paramType2 == kD0BarSL ) ||
			      ( paramType1 == kD0BarSL &&
				paramType2 == kD0SL ) )
		     {
			// C- and C+: 1
			constants[ 0 ] = 1. ;

			if( sampleType == kD0D0BarCOddWithEven ||
			    sampleType == kD0D0BarCEvenWithOdd )
			{
			   constants[ 0 + offsetCOdd ] = 1. ;
			}
		     }

		     // l+S+ and l-S+
		     else if( ( ( paramType1 == kD0SL ||
				  paramType1 == kD0BarSL ) &&
				paramType2 == kCPPlus ) ||
			      ( paramType1 == kCPPlus &&
				( paramType2 == kD0SL ||
				  paramType2 == kD0BarSL ) ) )
		     {
			if( sampleType != kD0D0BarCEven )
			{
			   // C-: 1
			   constants[ 0 ] = 1. ;
			}

			if( sampleType != kD0D0BarCOdd )
			{
			   // C+: 1 - 2y
			   constants[ 0 + offsetCOdd ] = 1. ;

			   constants[ 1 + offsetCOdd ] = -2. ;
			   powers[ 1 + offsetCOdd ][ m_yIndex ] = 1. ;
			}
		     }

		     // l+S- and l-S-
		     else if( ( ( paramType1 == kD0SL ||
				  paramType1 == kD0BarSL ) &&
				paramType2 == kCPMinus ) ||
			      ( paramType1 == kCPMinus &&
				( paramType2 == kD0SL ||
				  paramType2 == kD0BarSL ) ) )
		     {
			if( sampleType != kD0D0BarCEven )
			{
			   // C-: 1
			   constants[ 0 ] = 1. ;
			}

			if( sampleType != kD0D0BarCOdd )
			{
			   // C+: 1 + 2y
			   constants[ 0 + offsetCOdd ] = 1. ;

			   constants[ 1 + offsetCOdd ] = 2. ;
			   powers[ 1 + offsetCOdd ][ m_yIndex ] = 1. ;
			}
		     }

		     // S+S-
		     else if( ( paramType1 == kCPPlus &&
				paramType2 == kCPMinus ) ||
			      ( paramType1 == kCPMinus &&
				paramType2 == kCPPlus ) )
		     {
			// C-: 4
			constants[ 0 ] = 4. ;
		     }

		     // S+S+ and S-S-
		     else if( ( paramType1 == kCPPlus &&
				paramType2 == kCPPlus ) ||
			      ( paramType1 == kCPMinus &&
				paramType2 == kCPMinus ) )
		     {
			// C+: 4( 1 -+ 2y )
			constants[ 0 + offsetCOdd ] = 4. ;

			constants[ 1 + offsetCOdd ] =
			   ( paramType1 == kCPPlus ) ? -8. : 8. ;
			powers[ 1 + offsetCOdd ][ m_yIndex ] = 1. ;

			if( mode1 == mode2 )
			{
			   constants *= 0.5 ;
			}
		     }
		  }
		  else
		  {
		     doubleTagValid = false ;
		     cout << "Invalid combination of modes.  Try again."
			  << endl ;

		     // Remove the outputs just added.
		     for( int i = 0 ;
			  i < m_fitParameterNames.size() - nFitParamsBefore ;
			  ++i )
		     {
			m_fitParameterNames.pop_back() ;
		     }
		  }
	       }

               if( doubleTagValid )
               {
                  matrixElement.setName( mode1 + "/" + mode2 ) ;
                  matrixElement.setComment1( mode1 ) ;
                  matrixElement.setComment2( mode2 ) ;
		  matrixElement.setComment3( sampleTypeStr ) ;
                  matrixElement.setConstantVector( constants ) ;
                  matrixElement.setPowerMatrix( powers ) ;
                  m_doubleTagPredictions.push_back( matrixElement ) ;
		  m_particleContents.push_back( particleContent1 +
						particleContent2 ) ;
               }
            }
         }
      }
      else if( singleDouble != "end" )
      {
         cout << "Not a recognized type.  Try again." << endl ;
      }
   }
   while( singleDouble != "end" ) ;

   cout << endl << endl ;

   // Expand power matrices to dimension = number of outputs; fill extra
   // space with zeroes.
   vector< HDBVariableMatrixElement >::iterator inputItr =
      m_singleTagPredictions.begin() ;
   vector< HDBVariableMatrixElement >::iterator inputEnd =
      m_singleTagPredictions.end() ;

   for( ; inputItr != inputEnd ; ++inputItr )
   {
      inputItr->expandPowerMatrix( m_fitParameterNames.size() ) ;

      if( m_printDiagnostics )
      {
	 cout << inputItr->name() << endl
	      << "const" << inputItr->constantVector()
	      << "power" << inputItr->powerMatrix()
	      << endl ;
      }
   }


   inputItr = m_doubleTagPredictions.begin() ;
   inputEnd = m_doubleTagPredictions.end() ;

   for( ; inputItr != inputEnd ; ++inputItr )
   {
      inputItr->expandPowerMatrix( m_fitParameterNames.size() ) ;

      if( m_printDiagnostics )
      {
	 cout << inputItr->name() << endl
	      << "const" << inputItr->constantVector()
	      << "power" << inputItr->powerMatrix()
	      << endl ;
      }
   }


   // If there are only single or double tags for a given charge or if
   // no double tag has two corresponding single tag measurements,
   // then there's not enough information to fit for NDDbar.  In this case,
   // remove it from the list.

   if( m_nDPlusDMinusIndex != -1 )
   {
      // Check if NDDbar needs to be removed.
      int nSingle = 0 ;
      int nDouble = 0 ;
      int nDoubleWithBothSingles = 0 ;

      inputItr = m_singleTagPredictions.begin() ;
      inputEnd = m_singleTagPredictions.end() ;

      for( ; inputItr != inputEnd ; ++inputItr )
      {
	 if( inputItr->powerMatrix()[ 0 ][ m_nDPlusDMinusIndex ] != 0. )
	 {
	    ++nSingle ;
	 }
      }

      inputItr = m_doubleTagPredictions.begin() ;
      inputEnd = m_doubleTagPredictions.end() ;

      for( ; inputItr != inputEnd ; ++inputItr )
      {
	 const HepMatrix powers = inputItr->powerMatrix() ;

	 if( powers[ 0 ][ m_nDPlusDMinusIndex ] != 0. )
	 {
	    ++nDouble ;
	 }

	 // Form list of branching fraction indices for this double tag.
	 vector< int > brs ;
	 for( int i = 0 ; i < m_fitParameterNames.size() ; ++i )
	 {
	    if( i != m_nDPlusDMinusIndex &&
		powers[ 0 ][ i ] != 0. )
	    {
	       brs.push_back( i ) ;
	    }
	 }

	 // Create array of bools for double tag branching fractions.
	 bool brInSingle[ brs.size() ] ;
	 for( int i = 0 ; i < brs.size() ; ++i )
	 {
	    brInSingle[ i ] = false ;
	 }

	 // Loop over single tags, looking for measurements of the double
	 // tag branching fractions.
	 vector< HDBVariableMatrixElement >::iterator inputItr2 =
	    m_singleTagPredictions.begin() ;
	 vector< HDBVariableMatrixElement >::iterator inputEnd2 =
	    m_singleTagPredictions.end() ;

	 for( ; inputItr2 != inputEnd2 ; ++inputItr2 )
	 {
	    const HepMatrix powers = inputItr2->powerMatrix() ;

	    for( int i = 0 ; i < brs.size() ; ++i )
	    {
	       if( powers[ 0 ][ brs[ i ] ] != 0. )
	       {
		  brInSingle[ i ] = true ;
	       }
	    }
	 }

	 // If each double tag branching fraction has a corresponding single
	 // tag, then increment counter.
	 bool doubleHasBothSingles = true ;
	 for( int i = 0 ; i < brs.size() ; ++i )
	 {
	    doubleHasBothSingles = doubleHasBothSingles && brInSingle[ i ] ;
	 }

	 if( doubleHasBothSingles )
	 {
	    ++nDoubleWithBothSingles ;
	 }
      }

      if( nSingle == 0 || nDouble == 0 || nDoubleWithBothSingles == 0 )
      {
	 // Remove columns corresponding to NDDbar from power matrices.
	 inputItr = m_singleTagPredictions.begin() ;
	 inputEnd = m_singleTagPredictions.end() ;

	 for( ; inputItr != inputEnd ; ++inputItr )
	 {
	    inputItr->removeParameter( m_nDPlusDMinusIndex ) ;
	 }

	 inputItr = m_doubleTagPredictions.begin() ;
	 inputEnd = m_doubleTagPredictions.end() ;

	 for( ; inputItr != inputEnd ; ++inputItr )
	 {
	    inputItr->removeParameter( m_nDPlusDMinusIndex ) ;
	 }

	 // Remove NDDbar from m_fitParameterNames ;
	 vector< string > newFitParameterNames ;
	 for( int i = 0 ; i < m_fitParameterNames.size() ; ++i )
	 {
	    if( i != m_nDPlusDMinusIndex )
	    {
	       newFitParameterNames.push_back( m_fitParameterNames[ i ] ) ;
	    }
	 }

	 m_fitParameterNames = newFitParameterNames ;

	 // Adjust m_nDzeroDzerobarIndex if necessary.
         if( m_nDsPlusDsMinusIndex > m_nDPlusDMinusIndex )
         {
            --m_nDsPlusDsMinusIndex ;
         }

	 if( m_nD0D0BarIndex > m_nDPlusDMinusIndex )
	 {
	    --m_nD0D0BarIndex ;
	 }

	 if( m_nD0D0BarCOddIndex > m_nDPlusDMinusIndex )
	 {
	    --m_nD0D0BarCOddIndex ;
	 }

	 if( m_nD0D0BarCOddEvenFracIndex > m_nDPlusDMinusIndex )
	 {
	    --m_nD0D0BarCOddEvenFracIndex ;
	 }

	 if( m_nD0D0BarCEvenIndex > m_nDPlusDMinusIndex )
	 {
	    --m_nD0D0BarCEvenIndex ;
	 }

	 if( m_nD0D0BarCEvenOddFracIndex > m_nDPlusDMinusIndex )
	 {
	    --m_nD0D0BarCEvenOddFracIndex ;
	 }

	 if( m_yIndex > m_nDPlusDMinusIndex )
	 {
	    --m_yIndex ;
	 }

	 if( m_x2Index > m_nDPlusDMinusIndex )
	 {
	    --m_x2Index ;
	 }

	 if( m_r2Index > m_nDPlusDMinusIndex )
	 {
	    --m_r2Index ;
	 }

	 if( m_rzIndex > m_nDPlusDMinusIndex )
	 {
	    --m_rzIndex ;
	 }

	 if( m_rwxIndex > m_nDPlusDMinusIndex )
	 {
	    --m_rwxIndex ;
	 }

	 m_nDPlusDMinusIndex = -1 ;
      }
   }

   if( m_nDsPlusDsMinusIndex != -1 )
   {
      // Check if NDDbar needs to be removed.
      int nSingle = 0 ;
      int nDouble = 0 ;
      int nDoubleWithBothSingles = 0 ;

      inputItr = m_singleTagPredictions.begin() ;
      inputEnd = m_singleTagPredictions.end() ;

      for( ; inputItr != inputEnd ; ++inputItr )
      {
         if( inputItr->powerMatrix()[ 0 ][ m_nDsPlusDsMinusIndex ] != 0. )
         {
            ++nSingle ;
         }
      }

      inputItr = m_doubleTagPredictions.begin() ;
      inputEnd = m_doubleTagPredictions.end() ;

      for( ; inputItr != inputEnd ; ++inputItr )
      {
         const HepMatrix powers = inputItr->powerMatrix() ;

         if( powers[ 0 ][ m_nDsPlusDsMinusIndex ] != 0. )
         {
            ++nDouble ;
         }

         // Form list of branching fraction indices for this double tag.
         vector< int > brs ;
         for( int i = 0 ; i < m_fitParameterNames.size() ; ++i )
         {
            if( i != m_nDsPlusDsMinusIndex &&
                powers[ 0 ][ i ] != 0. )
            {
               brs.push_back( i ) ;
            }
         }

         // Create array of bools for double tag branching fractions.
         bool brInSingle[ brs.size() ] ;
         for( int i = 0 ; i < brs.size() ; ++i )
         {
            brInSingle[ i ] = false ;
         }

         // Loop over single tags, looking for measurements of the double
         // tag branching fractions.
         vector< HDBVariableMatrixElement >::iterator inputItr2 =
            m_singleTagPredictions.begin() ;
         vector< HDBVariableMatrixElement >::iterator inputEnd2 =
            m_singleTagPredictions.end() ;

         for( ; inputItr2 != inputEnd2 ; ++inputItr2 )
         {
            const HepMatrix powers = inputItr2->powerMatrix() ;

            for( int i = 0 ; i < brs.size() ; ++i )
            {
               if( powers[ 0 ][ brs[ i ] ] != 0. )
               {
                  brInSingle[ i ] = true ;
               }
            }
         }

         // If each double tag branching fraction has a corresponding single
         // tag, then increment counter.
         bool doubleHasBothSingles = true ;
         for( int i = 0 ; i < brs.size() ; ++i )
         {
            doubleHasBothSingles = doubleHasBothSingles && brInSingle[ i ] ;
         }

         if( doubleHasBothSingles )
         {
            ++nDoubleWithBothSingles ;
         }
      }

      if( nSingle == 0 || nDouble == 0 || nDoubleWithBothSingles == 0 )
      {
         // Remove columns corresponding to NDDbar from power matrices.
         inputItr = m_singleTagPredictions.begin() ;
         inputEnd = m_singleTagPredictions.end() ;

         for( ; inputItr != inputEnd ; ++inputItr )
         {
            inputItr->removeParameter( m_nDsPlusDsMinusIndex ) ;
         }

         inputItr = m_doubleTagPredictions.begin() ;
         inputEnd = m_doubleTagPredictions.end() ;

         for( ; inputItr != inputEnd ; ++inputItr )
         {
            inputItr->removeParameter( m_nDsPlusDsMinusIndex ) ;
         }

         // Remove NDDbar from m_fitParameterNames ;
         vector< string > newFitParameterNames ;
         for( int i = 0 ; i < m_fitParameterNames.size() ; ++i )
         {
            if( i != m_nDsPlusDsMinusIndex )
            {
               newFitParameterNames.push_back( m_fitParameterNames[ i ] ) ;
            }
         }

         m_fitParameterNames = newFitParameterNames ;

         // Adjust m_nDzeroDzerobarIndex if necessary.
         if( m_nDPlusDMinusIndex > m_nDsPlusDsMinusIndex )
         {
            --m_nDPlusDMinusIndex ;
         }

	 if( m_nD0D0BarIndex > m_nDsPlusDsMinusIndex )
	 {
	    --m_nD0D0BarIndex ;
	 }

	 if( m_nD0D0BarCOddIndex > m_nDsPlusDsMinusIndex )
	 {
	    --m_nD0D0BarCOddIndex ;
	 }

	 if( m_nD0D0BarCOddEvenFracIndex > m_nDsPlusDsMinusIndex )
	 {
	    --m_nD0D0BarCOddEvenFracIndex ;
	 }

	 if( m_nD0D0BarCEvenIndex > m_nDsPlusDsMinusIndex )
	 {
	    --m_nD0D0BarCEvenIndex ;
	 }

	 if( m_nD0D0BarCEvenOddFracIndex > m_nDsPlusDsMinusIndex )
	 {
	    --m_nD0D0BarCEvenOddFracIndex ;
	 }

	 if( m_yIndex > m_nDsPlusDsMinusIndex )
	 {
	    --m_yIndex ;
	 }

	 if( m_x2Index > m_nDsPlusDsMinusIndex )
	 {
	    --m_x2Index ;
	 }

	 if( m_r2Index > m_nDsPlusDsMinusIndex )
	 {
	    --m_r2Index ;
	 }

	 if( m_rzIndex > m_nDsPlusDsMinusIndex )
	 {
	    --m_rzIndex ;
	 }

	 if( m_rwxIndex > m_nDsPlusDsMinusIndex )
	 {
	    --m_rwxIndex ;
	 }

         m_nDsPlusDsMinusIndex = -1 ;
      }
   }

   if( m_nD0D0BarIndex != -1 )
   {
      // Check if NDDbar needs to be removed.
      int nSingle = 0 ;
      int nDouble = 0 ;
      int nDoubleWithBothSingles = 0 ;

      inputItr = m_singleTagPredictions.begin() ;
      inputEnd = m_singleTagPredictions.end() ;

      for( ; inputItr != inputEnd ; ++inputItr )
      {
	 if( inputItr->powerMatrix()[ 0 ][ m_nD0D0BarIndex ] != 0. )
	 {
	    ++nSingle ;
	 }
      }

      inputItr = m_doubleTagPredictions.begin() ;
      inputEnd = m_doubleTagPredictions.end() ;

      for( ; inputItr != inputEnd ; ++inputItr )
      {
	 const HepMatrix powers = inputItr->powerMatrix() ;

	 if( powers[ 0 ][ m_nD0D0BarIndex ] != 0. )
	 {
	    ++nDouble ;
	 }

	 // Form list of branching fraction indices for this double tag.
	 vector< int > brs ;
	 for( int i = 0 ; i < m_fitParameterNames.size() ; ++i )
	 {
	    if( i != m_nD0D0BarIndex &&
		powers[ 0 ][ i ] != 0. )
	    {
	       brs.push_back( i ) ;
	    }
	 }

	 // Create array of bools for double tag branching fractions.
	 bool brInSingle[ brs.size() ] ;
	 for( int i = 0 ; i < brs.size() ; ++i )
	 {
	    brInSingle[ i ] = false ;
	 }

	 // Loop over single tags, looking for measurements of the double
	 // tag branching fractions.
	 vector< HDBVariableMatrixElement >::iterator inputItr2 =
	    m_singleTagPredictions.begin() ;
	 vector< HDBVariableMatrixElement >::iterator inputEnd2 =
	    m_singleTagPredictions.end() ;

	 for( ; inputItr2 != inputEnd2 ; ++inputItr2 )
	 {
	    const HepMatrix powers = inputItr2->powerMatrix() ;

	    for( int i = 0 ; i < brs.size() ; ++i )
	    {
	       if( powers[ 0 ][ brs[ i ] ] != 0. )
	       {
		  brInSingle[ i ] = true ;
	       }
	    }
	 }

	 // If each double tag branching fraction has a corresponding single
	 // tag, then increment counter.
	 bool doubleHasBothSingles = true ;
	 for( int i = 0 ; i < brs.size() ; ++i )
	 {
	    doubleHasBothSingles = doubleHasBothSingles && brInSingle[ i ] ;
	 }

	 if( doubleHasBothSingles )
	 {
	    ++nDoubleWithBothSingles ;
	 }
      }

      if( nSingle == 0 || nDouble == 0 || nDoubleWithBothSingles == 0 )
      {
	 // Remove columns corresponding to NDDbar from power matrices.
	 inputItr = m_singleTagPredictions.begin() ;
	 inputEnd = m_singleTagPredictions.end() ;

	 for( ; inputItr != inputEnd ; ++inputItr )
	 {
	    inputItr->removeParameter( m_nD0D0BarIndex ) ;
	 }

	 inputItr = m_doubleTagPredictions.begin() ;
	 inputEnd = m_doubleTagPredictions.end() ;

	 for( ; inputItr != inputEnd ; ++inputItr )
	 {
	    inputItr->removeParameter( m_nD0D0BarIndex ) ;
	 }

	 // Remove NDDbar from m_fitParameterNames ;
	 vector< string > newFitParameterNames ;
	 for( int i = 0 ; i < m_fitParameterNames.size() ; ++i )
	 {
	    if( i != m_nD0D0BarIndex )
	    {
	       newFitParameterNames.push_back( m_fitParameterNames[ i ] ) ;
	    }
	 }

	 m_fitParameterNames = newFitParameterNames ;

	 // Adjust m_nDzeroDzerobarIndex if necessary.
         if( m_nDsPlusDsMinusIndex > m_nD0D0BarIndex )
         {
            --m_nDsPlusDsMinusIndex ;
         }

	 if( m_nDPlusDMinusIndex > m_nD0D0BarIndex )
	 {
	    --m_nDPlusDMinusIndex ;
	 }

	 if( m_nD0D0BarCOddIndex > m_nD0D0BarIndex )
	 {
	    --m_nD0D0BarCOddIndex ;
	 }

	 if( m_nD0D0BarCOddEvenFracIndex > m_nD0D0BarIndex )
	 {
	    --m_nD0D0BarCOddEvenFracIndex ;
	 }

	 if( m_nD0D0BarCEvenIndex > m_nD0D0BarIndex )
	 {
	    --m_nD0D0BarCEvenIndex ;
	 }

	 if( m_nD0D0BarCEvenOddFracIndex > m_nD0D0BarIndex )
	 {
	    --m_nD0D0BarCEvenOddFracIndex ;
	 }

	 if( m_yIndex > m_nD0D0BarIndex )
	 {
	    --m_yIndex ;
	 }

	 if( m_x2Index > m_nD0D0BarIndex )
	 {
	    --m_x2Index ;
	 }

	 if( m_r2Index > m_nD0D0BarIndex )
	 {
	    --m_r2Index ;
	 }

	 if( m_rzIndex > m_nD0D0BarIndex )
	 {
	    --m_rzIndex ;
	 }

	 if( m_rwxIndex > m_nD0D0BarIndex )
	 {
	    --m_rwxIndex ;
	 }

	 m_nD0D0BarIndex = -1 ;
      }
   }


   // Form HDBVariableVector m_fitPredictions; first single, then double tags.
   int nSingle = m_singleTagPredictions.size() ;
   int nDouble = m_doubleTagPredictions.size() ;

   m_fitPredictions =
      new HDBVariableVector( m_singleTagPredictions.size() +
			     m_doubleTagPredictions.size() ) ;

   // Copy single tag HDBVariableMatrixElements.
   for( int i = 0 ; i < nSingle ; ++i )
   {
      *( m_fitPredictions->element( i ) ) = m_singleTagPredictions[ i ] ;
   }

   // Copy double tag HDBVariableMatrixElements
   // and fill doubleToSingleCrossReference.
   for( int i = 0 ; i < nDouble ; ++i )
   {
      *( m_fitPredictions->element( i + nSingle ) ) =
	 m_doubleTagPredictions[ i ] ;

      pair< int, int > singlePair ;
      singlePair.first = -1 ;
      singlePair.second = -1 ;

      for( int j = 0 ; j < nSingle ; ++j )
      {
         if( m_doubleTagPredictions[ i ].comment1() ==
	     m_singleTagPredictions[ j ].name() &&
	     m_doubleTagPredictions[ i ].comment3() ==
	     m_singleTagPredictions[ j ].comment3() )
         {
            singlePair.first =  j ;
         }

         if( m_doubleTagPredictions[ i ].comment2() ==
	     m_singleTagPredictions[ j ].name()  &&
	     m_doubleTagPredictions[ i ].comment3() ==
	     m_singleTagPredictions[ j ].comment3() )
         {
            singlePair.second =  j ;
         }
      }

      doubleToSingleCrossReference.push_back( singlePair ) ;
   }

   m_fitPredictions->setParameterNames( m_fitParameterNames ) ;
   m_standardInputData->setDoubleToSingleCrossReference(
      doubleToSingleCrossReference,
      m_singleTagPredictions.size(),
      m_doubleTagPredictions.size() ) ;


   // Report back on outputs and measurements.
   if( m_printDiagnostics )
   {
      cout << endl << endl << "Output parameters in fit: " << endl ;
      vector< string >::const_iterator paramItr = m_fitParameterNames.begin() ;
      vector< string >::const_iterator paramEnd = m_fitParameterNames.end() ;
      for( ; paramItr != paramEnd ; ++paramItr )
      {
	 cout << "   " << *paramItr << endl ;
      }

      cout << endl << "Single tag yield measurements to be input: " << endl ;
      inputItr = m_singleTagPredictions.begin() ;
      inputEnd = m_singleTagPredictions.end() ;
      for( ; inputItr != inputEnd ; ++inputItr )
      {
	 cout << "   " << inputItr->name() << endl ;
      }

      cout << endl << "Double tag yield measurements to be input: " << endl ;
      inputItr = m_doubleTagPredictions.begin() ;
      inputEnd = m_doubleTagPredictions.end() ;
      for( ; inputItr != inputEnd ; ++inputItr )
      {
	 cout << "   " << inputItr->name() << " (" << inputItr->comment1()
	      << " vs. " << inputItr->comment2() << ")" << endl ;
      }

      cout << endl ;
   }

   m_fitParametersDefined = true ;
}

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

void
HDBStandardFitInputFactoryTTY::getInputYieldsAndErrors()
{
   if( m_inputYieldsAndErrorsDefined )
   {
      return ;
   }

   if( !m_fitParametersDefined )
   {
      makeFitPredictions() ;
   }

   // Yields and errors
   int nMeas = m_fitPredictions->numberRows() ;
   HepVector measuredYields( nMeas, 0 ) ;
   HepVector measuredYieldErrors( nMeas, 0 ) ;

   for( int i = 0 ; i < nMeas ; ++i )
   {
//       cout << "Enter yield for "
// 	   << m_fitPredictions->element( i )->name() << ": " ;
      cin >> measuredYields[ i ] ;
//       cout << "Enter statistical yield error for "
// 	   << m_fitPredictions->element( i )->name() << ": " ;
      cin >> measuredYieldErrors[ i ] ;
      double tmp ;
//       cout << "Enter systematic yield error for "
// 	   << m_fitPredictions->element( i )->name() << ": " ;
      cin >> tmp ;
      measuredYieldErrors[ i ] = sqrt(
	 measuredYieldErrors[ i ] * measuredYieldErrors[ i ] + tmp * tmp ) ;
   }

   if( m_printDiagnostics )
   {
      cout << endl << "Input yields:" << endl ;
      for( int i = 0 ; i < nMeas ; ++i )
      {
	 cout << measuredYields[ i ] << " +- " << measuredYieldErrors[ i ]
	      << endl ;
      }
      cout << endl ;
   }

   setYieldsAndErrors( measuredYields, measuredYieldErrors ) ;

   m_inputYieldsAndErrorsDefined = true ;
}

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

void
HDBStandardFitInputFactoryTTY::getInputYieldsAndErrorsMC()
{
   if( m_inputYieldsAndErrorsDefined || !m_generateMC )
   {
      return ;
   }

   if( !m_fitParametersDefined )
   {
      makeFitPredictions() ;
   }

   if( !m_backgroundsDefined )
   {
      getBackgrounds() ;
   }

   if( !m_efficienciesDefined )
   {
      getEfficiencies() ;
   }

   // True parameters = seed parameters
   makeSeeds() ;

   // Calculate corrected yields.
   HepVector N = m_fitPredictions->values( m_seedParameters ) ;

   HDBStandardMCInputData* mcInputData =
      dynamic_cast< HDBStandardMCInputData* >( m_standardInputData ) ;
   mcInputData->setTrueCorrectedYields( N ) ;

   // Apply efficiency and add in background to get measured yields.
   HepVector b = m_standardInputData->backgroundValues( m_seedParameters );

   HepVector measuredYields =
      m_standardInputData->signalEfficiencyValues() * N +
      m_standardInputData->backgroundEfficiencyValues() * b ;

   // Get measured yield errors
   int nMeas = measuredYields.num_row() ;
   HepVector measuredYieldErrors( nMeas, 0 ) ;

   for( int i = 0 ; i < nMeas ; ++i )
   {
//       cout << "Enter yield error for "
// 	   << m_fitPredictions->element( i )->name() << ": " ;
      cin >> measuredYieldErrors[ i ] ;
   }

   if( m_printDiagnostics )
   {
      cout << endl << "Input yields: " << measuredYields
	   << "Input yield errors: " << measuredYieldErrors << endl ;
   }

   // measuredYields are temporary -- they are generated in each MC trial.
   setYieldsAndErrors( measuredYields, measuredYieldErrors ) ;

   m_inputYieldsAndErrorsDefined = true ;
}

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

void
HDBStandardFitInputFactoryTTY::makeSeeds()
{
   if( m_seedsDefined )
   {
      return ;
   }

   if( !m_fitParametersDefined )
   {
      makeFitPredictions() ;
   }

   m_seedParameters = HepVector( m_fitParameterNames.size(), 0 ) ;

   if( m_generateMC )
   {
      cout << "Enter true values for fit parameters:" << endl ;
   }
   else
   {
      cout << "Enter seed values for fit parameters:" << endl ;
   }

   for( int i = 0 ; i < m_fitParameterNames.size() ; ++i )
   {
      cout << "   " << m_fitParameterNames[ i ] << ": " ;
      cin >> m_seedParameters[ i ] ;
   }

   m_seedsDefined = true ;
}

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

void
HDBStandardFitInputFactoryTTY::makeExternalData()
{
   if( m_externalDataDefined )
   {
      return ;
   }

   if( !m_fitParametersDefined )
   {
      makeFitPredictions() ;
   }

   m_externalData = new HDBInputData() ;

   string extStr ;
   cout << "Enter external measurements? (y/n)" << endl ;
   cin >> extStr ;

   // Allowed measurements are fit parameters or predefined combinations of
   // fit parameters.
   if( extStr == "y" || extStr == "Y" )
   {
      vector< HDBVariableMatrixElement > externalMatrixElements ;
      HepVector externalValues ;
      HepSymMatrix externalError ;

      string paramStr ;
      HepVector constants ;
      HepMatrix powers ;
      vector< string > parameterNames ;
      vector< double > parameterValuesVec ;
      vector< double > parameterErrorsVec ;

//       bool xSinDeltaDefined = false ;
//       double xSinDelta = 0. ;

//       cout << "Enter parameter to constrain ('end' to finish):" << endl ;
      cin >> paramStr ;

      while( paramStr != "end" )
      {
	 bool paramInList = false ;

	 // If parameter is not a fit parameter, check for other predefined
	 // combinations of fit parameters.
	 //if( !paramInList )
	 {
// 	    if( paramStr == "xSinDelta" )
// 	    {
// 	       if( xSinDeltaDefined )
// 	       {
// 		  cout << "WARNING: REDEFINING XSINDELTA" << endl ;
// 	       }

// 	       // Don't set paramInList to be true.
// 	       xSinDeltaDefined = true ;
// 	       cin >> xSinDelta ;
// 	    }
	    if( paramStr == "RWS" )
	    {
// 	       if( !xSinDeltaDefined )
// 	       {
// 		  cout << "WARNING: XSINDELTA UNDEFINED; USING DEFAULT = 0"
// 		       << endl ;
// 	       }

	       // = r^2 + ry' + RM ~= r^2 + y rz/2 + RM - rwx/2
	       paramInList = true ;
               constants = HepVector( 5 ) ;
               constants[ 0 ] = 1. ;
               constants[ 1 ] = 0.5 ;
               constants[ 2 ] = 0.5 ;
               constants[ 3 ] = 0.5 ;
               constants[ 4 ] = -0.5 ;
               powers = HepMatrix( 5, m_fitParameterNames.size(), 0 ) ;
               powers[ 0 ][ m_r2Index ] = 1. ;
               powers[ 1 ][ m_yIndex ] = 1. ;
               powers[ 1 ][ m_rzIndex ] = 1. ;
               powers[ 2 ][ m_x2Index ] = 1. ;
               powers[ 3 ][ m_yIndex ] = 2. ;
               powers[ 4 ][ m_rwxIndex ] = 1. ;
	    }
	    else if( paramStr == "y'" )
	    {
// 	       if( !xSinDeltaDefined )
// 	       {
// 		  cout << "WARNING: XSINDELTA UNDEFINED; USING DEFAULT = 0"
// 		       << endl ;
// 	       }

	       // = y*cosDelta - x*sinDelta
	       // ~= y rz / sqrt(r^2) / 2 - rwx / sqrt(r^2) / 2.
	       paramInList = true ;
	       constants = HepVector( 2 ) ;
	       constants[ 0 ] = 0.5 ;
	       constants[ 1 ] = -0.5 ;
	       powers = HepMatrix( 2, m_fitParameterNames.size(), 0 ) ;
	       powers[ 0 ][ m_r2Index ] = -0.5 ;
	       powers[ 0 ][ m_yIndex ] = 1. ;
	       powers[ 0 ][ m_rzIndex ] = 1. ;
	       powers[ 1 ][ m_r2Index ] = -0.5 ;
	       powers[ 1 ][ m_rwxIndex ] = 1. ;
	    }
	    else if( paramStr == "xSinDelta" )
	    {
// 	       if( !xSinDeltaDefined )
// 	       {
// 		  cout << "WARNING: XSINDELTA UNDEFINED; USING DEFAULT = 0"
// 		       << endl ;
// 	       }

	       // = rwx / sqrt(r^2) / 2.
	       paramInList = true ;
	       constants = HepVector( 1 ) ;
	       constants[ 0 ] = 0.5 ;
	       powers = HepMatrix( 1, m_fitParameterNames.size(), 0 ) ;
	       powers[ 0 ][ m_r2Index ] = -0.5 ;
	       powers[ 0 ][ m_rwxIndex ] = 1. ;
	    }
	    else if( paramStr == "sinDelta2" )
	    {
	       // = rwx^2 / r2 / x2 / 4.
	       paramInList = true ;
	       constants = HepVector( 1 ) ;
	       constants[ 0 ] = 0.25 ;
	       powers = HepMatrix( 1, m_fitParameterNames.size(), 0 ) ;
	       powers[ 0 ][ m_r2Index ] = -1. ;
	       powers[ 0 ][ m_x2Index ] = -1. ;
	       powers[ 0 ][ m_rwxIndex ] = 2. ;
	    }
	    else if( paramStr == "sinDelta" )
	    {
	       // = rwx / r / x / 2.
	       paramInList = true ;
	       constants = HepVector( 1 ) ;
	       constants[ 0 ] = 0.5 ;
	       powers = HepMatrix( 1, m_fitParameterNames.size(), 0 ) ;
	       powers[ 0 ][ m_r2Index ] = -0.5 ;
	       powers[ 0 ][ m_x2Index ] = -0.5 ;
	       powers[ 0 ][ m_rwxIndex ] = 1. ;
	    }
	    else if( paramStr == "RM" )
	    {
	       paramInList = true ;
	       constants = HepVector( 2 ) ;
	       constants[ 0 ] = 0.5 ;
	       constants[ 1 ] = 0.5 ;
	       powers = HepMatrix( 2, m_fitParameterNames.size(), 0 ) ;
	       powers[ 0 ][ m_x2Index ] = 1. ;
	       powers[ 1 ][ m_yIndex ] = 2. ;
	    }
	    else if( paramStr == "x" )
	    {
	       paramInList = true ;
	       constants = HepVector( 1 ) ;
	       constants[ 0 ] = 1. ;
	       powers = HepMatrix( 1, m_fitParameterNames.size(), 0 ) ;
	       powers[ 0 ][ m_x2Index ] = 0.5 ;
	    }
	    else if( paramStr == "cosDelta" )
	    {
	       paramInList = true ;
	       constants = HepVector( 1 ) ;
	       constants[ 0 ] = 0.5 ;
	       powers = HepMatrix( 1, m_fitParameterNames.size(), 0 ) ;
	       powers[ 0 ][ m_rzIndex ] = 1. ;
	       powers[ 0 ][ m_r2Index ] = -0.5 ;
	    }
	    else if( paramStr == "BrD2KPi" )
	    {
// 	       if( !xSinDeltaDefined )
// 	       {
// 		  cout << "WARNING: XSINDELTA UNDEFINED; USING DEFAULT = 0"
// 		       << endl ;
// 	       }

	       int brIndex = -1 ;

	       for( int i = 0 ; i < m_fitParameterNames.size() ; ++i )
	       {
		  if( m_fitParameterNames[ i ] == paramStr )
		  {
		     brIndex = i ;
		     break ;
		  }
	       }

	       if( brIndex > -1 )
	       {
		  paramInList = true ;

		  constants = HepVector( 3 ) ;
		  constants[ 0 ] = 1. ;
		  constants[ 1 ] = 0.5 ;
		  constants[ 2 ] = 0.5 ;
		  powers = HepMatrix( 3, m_fitParameterNames.size(), 0 ) ;
		  powers[ 0 ][ brIndex ] = 1. ;
		  powers[ 1 ][ brIndex ] = 1. ;
		  powers[ 1 ][ m_yIndex ] = 1. ;
		  powers[ 1 ][ m_rzIndex ] = 1. ;
		  powers[ 2 ][ brIndex ] = 1. ;
		  powers[ 2 ][ m_rwxIndex ] = 1. ;
	       }
	    }
	    else if( paramStr == "BrD2KsPi0" ||
		     paramStr == "BrD2KsEta" ||
		     paramStr == "BrD2KsOmega" )
	    {
	       int brIndex = -1 ;

	       for( int i = 0 ; i < m_fitParameterNames.size() ; ++i )
	       {
		  if( m_fitParameterNames[ i ] == paramStr )
		  {
		     brIndex = i ;
		     break ;
		  }
	       }

	       if( brIndex > -1 )
	       {
		  paramInList = true ;

		  constants = HepVector( 2 ) ;
		  constants[ 0 ] = 1. ;
		  constants[ 1 ] = 1. ;
		  powers = HepMatrix( 2, m_fitParameterNames.size(), 0 ) ;
		  powers[ 0 ][ brIndex ] = 1. ;
		  powers[ 1 ][ brIndex ] = 1. ;
		  powers[ 1 ][ m_yIndex ] = 1. ;
	       }
	    }
	    else if( paramStr == "BrD2K+K-" ||
		     paramStr == "BrD2Pi+Pi-" ||
		     paramStr == "BrD2KsPi0Pi0" ||
		     paramStr == "BrD2KlPi0" )
	    {
	       int brIndex = -1 ;

	       for( int i = 0 ; i < m_fitParameterNames.size() ; ++i )
	       {
		  if( m_fitParameterNames[ i ] == paramStr )
		  {
		     brIndex = i ;
		     break ;
		  }
	       }

	       if( brIndex > -1 )
	       {
		  paramInList = true ;

		  constants = HepVector( 2 ) ;
		  constants[ 0 ] = 1. ;
		  constants[ 1 ] = -1. ;
		  powers = HepMatrix( 2, m_fitParameterNames.size(), 0 ) ;
		  powers[ 0 ][ brIndex ] = 1. ;
		  powers[ 1 ][ brIndex ] = 1. ;
		  powers[ 1 ][ m_yIndex ] = 1. ;
	       }
	    }
	    else if( paramStr == "BrD2K+K-/BrD2KPi" )
	    {
// 	       if( !xSinDeltaDefined )
// 	       {
// 		  cout << "WARNING: XSINDELTA UNDEFINED; USING DEFAULT = 0"
// 		       << endl ;
// 	       }

	       int kkIndex = -1 ;
	       int kpiIndex = -1 ;

	       for( int i = 0 ; i < m_fitParameterNames.size() ; ++i )
	       {
		  if( m_fitParameterNames[ i ] == "BrD2K+K-" )
		  {
		     kkIndex = i ;
		  }
		  else if( m_fitParameterNames[ i ] == "BrD2KPi" )
		  {
		     kpiIndex = i ;
		  }
	       }

	       if( kkIndex > -1 && kpiIndex > -1 )
	       {
		  paramInList = true ;

		  constants = HepVector( 4 ) ;
		  constants[ 0 ] = 1. ;
		  constants[ 1 ] = -1. ;
		  constants[ 2 ] = -0.5 ;
		  constants[ 3 ] = -0.5 ;
		  powers = HepMatrix( 4, m_fitParameterNames.size(), 0 ) ;
		  powers[ 0 ][ kkIndex ] = 1. ;
		  powers[ 0 ][ kpiIndex ] = -1. ;
		  powers[ 1 ][ kkIndex ] = 1. ;
		  powers[ 1 ][ kpiIndex ] = -1. ;
		  powers[ 1 ][ m_yIndex ] = 1. ;
		  powers[ 2 ][ kkIndex ] = 1. ;
		  powers[ 2 ][ kpiIndex ] = -1. ;
		  powers[ 2 ][ m_yIndex ] = 1. ;
		  powers[ 2 ][ m_rzIndex ] = 1. ;
		  powers[ 3 ][ kkIndex ] = 1. ;
		  powers[ 3 ][ kpiIndex ] = -1. ;
		  powers[ 3 ][ m_rwxIndex ] = 1. ;
	       }
	    }
	    else if( paramStr == "BrD2Pi+Pi-/BrD2KPi" )
	    {
// 	       if( !xSinDeltaDefined )
// 	       {
// 		  cout << "WARNING: XSINDELTA UNDEFINED; USING DEFAULT = 0"
// 		       << endl ;
// 	       }

	       int pipiIndex = -1 ;
	       int kpiIndex = -1 ;

	       for( int i = 0 ; i < m_fitParameterNames.size() ; ++i )
	       {
		  if( m_fitParameterNames[ i ] == "BrD2Pi+Pi-" )
		  {
		     pipiIndex = i ;
		  }
		  else if( m_fitParameterNames[ i ] == "BrD2KPi" )
		  {
		     kpiIndex = i ;
		  }
	       }

	       if( pipiIndex > -1 && kpiIndex > -1 )
	       {
		  paramInList = true ;

		  constants = HepVector( 4 ) ;
		  constants[ 0 ] = 1. ;
		  constants[ 1 ] = -1. ;
		  constants[ 2 ] = -0.5 ;
		  constants[ 3 ] = -0.5 ;
		  powers = HepMatrix( 4, m_fitParameterNames.size(), 0 ) ;
		  powers[ 0 ][ pipiIndex ] = 1. ;
		  powers[ 0 ][ kpiIndex ] = -1. ;
		  powers[ 1 ][ pipiIndex ] = 1. ;
		  powers[ 1 ][ kpiIndex ] = -1. ;
		  powers[ 1 ][ m_yIndex ] = 1. ;
		  powers[ 2 ][ pipiIndex ] = 1. ;
		  powers[ 2 ][ kpiIndex ] = -1. ;
		  powers[ 2 ][ m_yIndex ] = 1. ;
		  powers[ 2 ][ m_rzIndex ] = 1. ;
		  powers[ 3 ][ pipiIndex ] = 1. ;
		  powers[ 3 ][ kpiIndex ] = -1. ;
		  powers[ 3 ][ m_rwxIndex ] = 1. ;
	       }
	    }
// 	    else if( paramStr == "ND0D0BarC-*BrD2KlPi0" )
// 	    {
// 	       int klpi0Index = -1 ;

// 	       for( int i = 0 ; i < m_fitParameterNames.size() ; ++i )
// 	       {
// 		  if( m_fitParameterNames[ i ] == "BrD2KlPi0" )
// 		  {
// 		     klpi0Index = i ;
// 		  }
// 	       }

// 	       if( klpi0Index > -1 )
// 	       {
// 		  paramInList = true ;

// 		  constants = HepVector( 1, 1 ) ;
// 		  powers = HepMatrix( 1, m_fitParameterNames.size(), 0 ) ;
// 		  powers[ 0 ][ m_nD0D0BarCOddIndex ] = 1. ;
// 		  powers[ 0 ][ klpi0Index ] = 1. ;
// 	       }
// 	    }
	    else if( paramStr == "ND0D0BarC-*BrD2Xenu" )
	    {
	       int xenuIndex = -1 ;

	       for( int i = 0 ; i < m_fitParameterNames.size() ; ++i )
	       {
		  if( m_fitParameterNames[ i ] == "BrD2Xenu" )
		  {
		     xenuIndex = i ;
		  }
	       }

	       if( xenuIndex > -1 )
	       {
		  paramInList = true ;

		  constants = HepVector( 1, 1 ) ;
		  powers = HepMatrix( 1, m_fitParameterNames.size(), 0 ) ;
		  powers[ 0 ][ m_nD0D0BarCOddIndex ] = 1. ;
		  powers[ 0 ][ xenuIndex ] = 1. ;
	       }
	    }
	 }

	 if( !paramInList )
	 {
	    for( int i = 0 ; i < m_fitParameterNames.size() ; ++i )
	    {
	       if( m_fitParameterNames[ i ] == paramStr )
	       {
		  paramInList = true ;
		  constants = HepVector( 1, 1 ) ;
		  powers = HepMatrix( 1, m_fitParameterNames.size(), 0 ) ;
		  powers[ 0 ][ i ] = 1. ;

		  break ;
	       }
	    }
	 }

	 if( paramInList )
	 {
	    HDBVariableMatrixElement matrixElement ;
	    matrixElement.setName( paramStr ) ;
	    matrixElement.setConstantVector( constants ) ;
	    matrixElement.setPowerMatrix( powers ) ;
	    externalMatrixElements.push_back( matrixElement ) ;

	    parameterNames.push_back( paramStr ) ;

	    double paramValue ;
// 	    cout << "Enter value of " << paramStr << ":" << endl ;
	    cin >> paramValue ;
	    parameterValuesVec.push_back( paramValue ) ;

	    double paramError ;
// 	    cout << "Enter error on " << paramStr << ":" << endl ;
	    cin >> paramError ;
	    parameterErrorsVec.push_back( paramError ) ;
	 }
//	 else if( paramStr != "xSinDelta" )
	 else
	 {
	    cout << "Parameter not in list.  Try again." << endl ;
	 }

// 	 cout << "Enter parameter to constrain ('end' to finish):" << endl ;
	 cin >> paramStr ;
      }

      int nParam = parameterNames.size() ;
      HepVector parameterValues( nParam, 0 ) ;
      HepSymMatrix parameterErrors( nParam, 0 ) ;

      for( int i = 0 ; i < nParam ; ++i )
      {
	 parameterValues[ i ] = parameterValuesVec[ i ] ;
	 parameterErrors[ i ][ i ] =
	    parameterErrorsVec[ i ] * parameterErrorsVec[ i ] ;

	 for( int j = i + 1 ; j < nParam ; ++j )
	 {
	    double corr ;
// 	    cout << "Enter correlation coefficient for "
// 		 << parameterNames[ i ] << "/" << parameterNames[ j ]
// 		 << ":" << endl ;
	    cin >> corr ;
	    parameterErrors[ i ][ j ] =
	       corr * parameterErrorsVec[ i ] * parameterErrorsVec[ j ] ;
	 }
      }

      m_externalData->setValuesAndErrorMatrix( parameterValues,
					       parameterErrors ) ;

      // Copy external HDBVariableMatrixElements.
      m_externalFitPredictions = new HDBVariableVector( nParam ) ;

      for( int i = 0 ; i < nParam ; ++i )
      {
	 *( m_externalFitPredictions->element( i ) ) =
	    externalMatrixElements[ i ] ;

	 if( m_printDiagnostics )
	 {
	    cout << externalMatrixElements[ i ].name() << endl
		 << "const" << externalMatrixElements[ i ].constantVector()
		 << "power" << externalMatrixElements[ i ].powerMatrix()
		 << endl ;
	 }
      }

      m_externalFitPredictions->setParameterNames( m_fitParameterNames ) ;
   }
   else
   {
      m_externalFitPredictions = new HDBVariableVector() ;
   }

   m_externalDataDefined = true ;
}

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

void
HDBStandardFitInputFactoryTTY::getBackgrounds()
{
   if( m_backgroundsDefined )
   {
      return ;
   }

   if( !m_fitParametersDefined )
   {
      makeFitPredictions() ;
   }

   m_backgroundNames.clear() ;


   int nMeas = m_fitPredictions->numberRows() ;
   int nFitParameters = m_fitParameterNames.size() ;

   vector< HDBVariableMatrixElement > backgroundElements ;

   vector< string > backgroundParameterNames ;
   vector< double > backgroundParameters ;
   vector< double > backgroundParameterErrors ;
   string type ;

   do
   {
//       cout << "Enter background type (neutralD/chargedD/Ds/neutralDC-/neutralDC-WithC+/neutralDC+/neutralDC+WithC-/nonD/absolute/end): " ;
      cin >> type ;

      if( type == "neutralD" ||
	  type == "chargedD" ||
	  type == "Ds" ||
	  type == "neutralDC-" ||
	  type == "neutralDC-WithC+" ||
	  type == "neutralDC+" ||
	  type == "neutralDC+WithC-" ||
	  type == "nonD" ||
	  type == "absolute" )
      {
         HepVector probs( nMeas, 0 ) ;

         if( type != "nonD" && type != "absolute" )
         {
	    vector< int > nddIndices ;
	    string ddbarType ;

	    // Two indices at most.  Second index is always admixture fraction.
	    if( type == "neutralD" )
	    {
	       nddIndices.push_back( m_nD0D0BarIndex ) ;
	       ddbarType = "ND+D-" ;
	    }
	    else if( type == "chargedD" )
	    {
	       nddIndices.push_back( m_nDPlusDMinusIndex ) ;
	       ddbarType = "NDs+Ds-" ;
	    }
	    else if( type == "Ds" )
	    {
	       nddIndices.push_back( m_nDsPlusDsMinusIndex ) ;
	       ddbarType = "ND0D0Bar" ;
	    }
	    else if( type == "neutralDC-" )
	    {
	       nddIndices.push_back( m_nD0D0BarCOddIndex ) ;
	       ddbarType = "ND0D0BarC-" ;
	    }
	    else if( type == "neutralDC-WithC+" )
	    {
	       nddIndices.push_back( m_nD0D0BarCOddIndex ) ;
	       nddIndices.push_back( m_nD0D0BarCOddEvenFracIndex ) ;
	       ddbarType = "ND0D0BarC-WithC+" ;
	    }
	    else if( type == "neutralDC+" )
	    {
	       nddIndices.push_back( m_nD0D0BarCEvenIndex ) ;
	       ddbarType = "ND0D0BarC+" ;
	    }
	    else if( type == "neutralDC+WithC-" )
	    {
	       nddIndices.push_back( m_nD0D0BarCEvenIndex ) ;
	       nddIndices.push_back( m_nD0D0BarCEvenOddFracIndex ) ;
	       ddbarType = "ND0D0BarC+WithC-" ;
	    }

            string brFracName ;
//             cout << "Enter branching fraction name: " ;
            cin >> brFracName ;
            m_backgroundNames.push_back( brFracName ) ;

	    // Add NDDbar to parameter list if not fit parameter.
	    vector< int >::const_iterator indexItr = nddIndices.begin() ;
	    vector< int >::const_iterator indexEnd = nddIndices.end() ;
	    bool nddbarInList = true ;

	    for( ; indexItr != indexEnd ; ++indexItr )
	    {
	       if( *indexItr < 0 )
	       {
		  nddbarInList = false ;
		  break ;
	       }
	    }

	    if( !nddbarInList )
	    {
	       nddIndices.clear() ;
	       nddIndices.push_back( nFitParameters +
				     backgroundParameterNames.size() ) ;
	       backgroundParameterNames.push_back( ddbarType ) ;

	       double nddbar ;
// 	       cout << "Enter " << ddbarType << ": " ;
	       cin >> nddbar ;
	       backgroundParameters.push_back( nddbar ) ;
	       double dnddbar ;
// 	       cout << "Enter error on " << ddbarType << ": " ;
	       cin >> dnddbar ;
	       backgroundParameterErrors.push_back( dnddbar ) ;
	    }


	    // Add branching fraction to parameters list.
	    bool brFracInList = false ;
	    int brFracIndex ;

	    for( int i = 0 ; i < backgroundParameterNames.size() ; ++i )
	    {
	       if( backgroundParameterNames[ i ] == brFracName )
	       {
		  brFracInList = true ;
		  brFracIndex = nFitParameters + i ;
	       }
	    }

	    if( !brFracInList )
	    {
	       brFracIndex = nFitParameters + backgroundParameterNames.size() ;
	       backgroundParameterNames.push_back( brFracName ) ;

	       double brfrac ;
// 	       cout << "Enter branching fraction: " ;
	       cin >> brfrac ;
	       backgroundParameters.push_back( brfrac ) ;
	       double dbrfrac ;
// 	       cout << "Enter branching fraction error: " ;
	       cin >> dbrfrac ;
	       backgroundParameterErrors.push_back( dbrfrac ) ;
	    }


            // Add term to input definitions.
            HDBVariableMatrixElement element ;
	    element.setName( brFracName ) ;
	    element.setComment1( ddbarType ) ;
	    element.setComment2( brFracName ) ;
	    element.setConstantVector( HepVector( nddIndices.size(), 1 ) ) ;

	    HepMatrix powers(
	       nddIndices.size(),
	       nFitParameters + backgroundParameterNames.size(),
	       0 ) ;

	    // Set main NDDBar and branching fraction parameters.
	    for( int i = 0 ; i < nddIndices.size() ; ++i )
	    {
	       powers[ i ][ nddIndices[ 0 ] ] = 1. ;
	       powers[ i ][ brFracIndex ] = 1. ;
	    }

	    // Set admixture fraction parameter.
	    if( nddIndices.size() == 2 )
	    {
	       powers[ 1 ][ nddIndices[ 1 ] ] = 1. ;
	    }

	    element.setPowerMatrix( powers ) ;

	    backgroundElements.push_back( element ) ;
         }
         else if( type == "nonD" )
         {
            string xsecName ;
//             cout << "Enter cross section name: " ;
            cin >> xsecName ;
            m_backgroundNames.push_back( xsecName ) ;


	    // Add luminosity and cross section to parameters list.
	    bool lumiInList = false ;
	    int lumiIndex ;
	    bool xsecInList = false ;
	    int xsecIndex ;

	    for( int i = 0 ; i < backgroundParameterNames.size() ; ++i )
	    {
	       if( backgroundParameterNames[ i ] == "luminosity" )
	       {
		  lumiInList = true ;
		  lumiIndex = nFitParameters + i ;
	       }
	       else if( backgroundParameterNames[ i ] == xsecName )
	       {
		  xsecInList = true ;
		  xsecIndex = nFitParameters + i ;
	       }
	    }

	    if( !lumiInList )
	    {
	       lumiIndex = nFitParameters + backgroundParameterNames.size() ;
	       backgroundParameterNames.push_back( "luminosity" ) ;

	       double lumi ;
// 	       cout << "Enter luminosity: " ;
	       cin >> lumi ;
	       backgroundParameters.push_back( lumi ) ;
	       double dlumi ;
// 	       cout << "Enter luminosity error: " ;
	       cin >> dlumi ;
	       backgroundParameterErrors.push_back( dlumi ) ;
	    }

	    if( !xsecInList )
	    {
	       xsecIndex = nFitParameters + backgroundParameterNames.size() ;
	       backgroundParameterNames.push_back( xsecName ) ;

	       double xsec ;
// 	       cout << "Enter cross section: " ;
	       cin >> xsec ;
	       backgroundParameters.push_back( xsec ) ;
	       double dxsec ;
// 	       cout << "Enter cross section error: " ;
	       cin >> dxsec ;
	       backgroundParameterErrors.push_back( dxsec ) ;
	    }


            // Add term to input definitions.
            HDBVariableMatrixElement element ;
	    element.setName( xsecName ) ;
	    element.setComment1( "luminosity" ) ;
	    element.setComment2( xsecName ) ;
	    element.setConstantVector( HepVector( 1, 1 ) ) ;

	    HepMatrix powers(
	       1,
	       nFitParameters + backgroundParameterNames.size(),
	       0 ) ;
	    powers[ 0 ][ lumiIndex ] = 1. ;
	    powers[ 0 ][ xsecIndex ] = 1. ;
	    element.setPowerMatrix( powers ) ;

	    backgroundElements.push_back( element ) ;
         }
         else if( type == "absolute" )
         {
            string bkgName ;
//             cout << "Enter background name: " ;
            cin >> bkgName ;
            m_backgroundNames.push_back( bkgName ) ;

            // Add background to parameters list.
            bool bkgInList = false ;
            int bkgIndex ;

            for( int i = 0 ; i < backgroundParameterNames.size() ; ++i )
            {
               if( backgroundParameterNames[ i ] == bkgName )
               {
                  bkgInList = true ;
                  bkgIndex = nFitParameters + i ;
               }
            }

            if( !bkgInList )
            {
               bkgIndex = nFitParameters + backgroundParameterNames.size() ;
               backgroundParameterNames.push_back( bkgName ) ;

               double bkg ;
//                cout << "Enter background: " ;
               cin >> bkg ;
               backgroundParameters.push_back( bkg ) ;
               double dbkg ;
//                cout << "Enter background error: " ;
               cin >> dbkg ;
               backgroundParameterErrors.push_back( dbkg ) ;
            }

            // Add term to input definitions.
            HDBVariableMatrixElement element ;
            element.setName( bkgName ) ;
            element.setComment1( "absolute" ) ;
            element.setComment2( bkgName ) ;
            element.setConstantVector( HepVector( 1, 1 ) ) ;

            HepMatrix powers(
               1,
               nFitParameters + backgroundParameterNames.size(),
               0 ) ;
            powers[ 0 ][ bkgIndex ] = 1. ;
            element.setPowerMatrix( powers ) ;

            backgroundElements.push_back( element ) ;
         }
      }
      else if( type != "end" )
      {
         cout << "Not a recognized type.  Try again." << endl ;
      }
   }
   while( type != "end" ) ;


   // Finish up

   if( m_printDiagnostics )
   {
      cout << endl << endl << "Background parameters:" << endl ;
   }

   HepVector bkgParams( backgroundParameters.size() ) ;
   HepVector bkgParamErrors( backgroundParameters.size() ) ;
   for( int i = 0 ; i < backgroundParameters.size() ; ++i )
   {
      if( m_printDiagnostics )
      {
	 cout << "   " << backgroundParameterNames[ i ]
	      << ": " << backgroundParameters[ i ]
	      << " +- " << backgroundParameterErrors[ i ]
	      << endl ;
      }

      bkgParams[ i ] = backgroundParameters[ i ] ;
      bkgParamErrors[ i ] = backgroundParameterErrors[ i ] ;
   }

   cout << endl ;

   HDBVariableVector bkgVector( m_backgroundNames.size() ) ;
   for( int i = 0 ; i < m_backgroundNames.size() ; ++i )
   {
      *( bkgVector.element( i ) ) = backgroundElements[ i ] ;
      bkgVector.element( i )->expandPowerMatrix( nFitParameters +
						 bkgParams.num_row() ) ;
   }

   bkgVector.setParameterNames( backgroundParameterNames ) ;
   m_standardInputData->setBackgroundVector( bkgVector ) ;
   m_standardInputData->setBackgroundParameters( bkgParams ) ;
   m_standardInputData->setBackgroundParameterErrors( bkgParamErrors ) ;

   m_backgroundsDefined = true ;
}

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

void
HDBStandardFitInputFactoryTTY::getEfficiencies()
{
   if( m_efficienciesDefined )
   {
      return ;
   }

   if( !m_fitParametersDefined )
   {
      makeFitPredictions() ;
   }

   if( !m_backgroundsDefined )
   {
      getBackgrounds() ;
   }


   int nSingle = m_singleTagPredictions.size() ;
   int nDouble = m_doubleTagPredictions.size() ;
   int nMeas = nSingle + nDouble ;
   int nFitParams = m_fitParameterNames.size() ;

   // ~~~~~~~~~~~~~~ Signal efficiencies ~~~~~~~~~~~~~~~

   HepMatrix sigEffs( nMeas, nMeas, 0 ) ;

   // Single tags.
   for( int i = 0 ; i < nSingle ; ++i )
   {
//       cout << "Enter signal efficiencies for single tag "
// 	   << m_singleTagPredictions[ i ].name()
//            << endl ;

      for( int j = 0 ; j < nSingle ; ++j )
      {
//          cout << "   Probability for " << m_singleTagPredictions[ j ].name()
//               << " --> " << m_singleTagPredictions[ i ].name()
//               << ": " ;
         cin >> sigEffs[ i ][ j ] ;
      }

      if( m_standardInputData->singleTagsExclusive() )
      {
         for( int j = nSingle ; j < nMeas ; ++j )
         {
//             cout << "   Probability for "
// 		 << m_doubleTagPredictions[ j - nSingle ].name()
//                  << " --> " << m_singleTagPredictions[ i ].name()
//                  << ": " ;
//             cin >> sigEffs[ i ][ j ] ;

            // Flip sign of efficiency matrix element.
            sigEffs[ i ][ j ] = -sigEffs[ i ][ j ] ;
         }
      }

      cout << endl ;
   }

   // Double tags.
   for( int i = nSingle ; i < nMeas ; ++i )
   {
//       cout << "Enter signal efficiencies for double tag "
// 	   << m_doubleTagPredictions[ i - nSingle ].name()
//            << endl ;

      for( int j = nSingle ; j < nMeas ; ++j )
      {
//          cout << "   Probability for "	
// 	      << m_doubleTagPredictions[ j - nSingle ].name()
//               << " --> " << m_doubleTagPredictions[ i - nSingle ].name()
//               << ": " ;
         cin >> sigEffs[ i ][ j ] ;
      }

      cout << endl ;
   }

   cout << endl ;

   if( m_printDiagnostics )
   {
      cout << "Signal efficiency matrix: " << sigEffs << endl ;
   }

   // ~~~~~~~~~~~~~~ Background efficiencies ~~~~~~~~~~~~~~~

   int nBkg = m_backgroundNames.size() ;
   HepMatrix bkgEffs( nMeas, nBkg, 0 ) ;

   for( int i = 0 ; i < nMeas ; ++i )
   {
      for( int j = 0 ; j < nBkg ; ++j )
      {
// 	 cout << "Enter background efficiencies for " << m_backgroundNames[ j ]
// 	      << " --> " << m_fitPredictions->element( i )->name()
//               << ": " ;
         cin >> bkgEffs[ i ][ j ] ;
      }

      cout << endl ;
   }

   cout << endl ;

   if( nBkg > 0 && m_printDiagnostics )
   {
      cout << "Background efficiency matrix: " << bkgEffs << endl ;
   }


   //~~~~~~~~~~ Form HDBVariableMatrix for signal and background ~~~~~~~~~~~~

   if( m_particleContents.size() != nMeas )
   {
      cout << "m_particleContents.size() != nMeas" << endl ;
      return ;
   }

   // Efficiency uncertainties included:
   //   - uncorrelated  <- obsolete
   //   - particle content (row-wise)
   //   - fit parameters (column-wise)
   //   - number of D's (i.e. single or double tag) (row-wise)

   // Replaced parameters for uncorrelated errors with
   // HDBVariableMatrixElement::uncorrelatedError().
   //   int nUncorr = nMeas * ( nMeas + nBkg ) ;
   int nUncorr = 0 ;
   int nUncert = nUncorr +
      HDBStandardFitInputFactory::kNumParticleTypes +
      nFitParams +
      1 + // per yield
      1 + // per D
      1 + // per D (fit-parameter-dependent)
      1 + // per single tag
      1 + // per single tag (fit-parameter-dependent)
      1 ; // per double tag

   HDBEfficiencyMatrix sigEffMatrix( nMeas, nMeas ) ;
   HDBEfficiencyMatrix bkgEffMatrix( nMeas, nBkg ) ;
   int modeDepDIndex = -1 ;
   int modeDepSTIndex = -1 ;

   for( int i = 0 ; i < nMeas ; ++i )    // row
   {
      HepVector particleContents = m_particleContents[ i ] ;

      // The power matrix has two rows: one for fractional uncertainties
      // and one for absolute uncertainties.
      //
      // constant      powers          parameter       error
      // -----------------------------------------------------------
      //   eff     particle content        1      fractional uncert.
      //    1      uncorrelated            0       absolute uncert. <- obsolete
      //
      // Order of parameters is: first all the uncorrelated uncertainties
      // for the signal and background efficiency matrices, then the
      // particle types, then the fit parameters, then the number of D's,
      // then single tags, then double tags.
      //
      // The parameters for the fit parameters are meant to account for
      // column-wise correlations, such as resonant substructure, which would
      // be associated with the TRUE decay, not the reconstructed decay.  So,
      // these parameters are needed only for the signal efficiency matrix.

      // Signal
      for( int j = 0 ; j < nMeas ; ++j ) // column
      {
	 HepVector constants( 1, 1 ) ;
	 HepMatrix powers( 1, nUncert, 0 ) ;

	 // Row for fractional uncertainties.

	 // Uncertainties for particle efficiencies.
	 constants[ 0 ] = sigEffs[ i ][ j ] ;
	 int counter = nUncorr ;
	 for( int k=0 ; k<HDBStandardFitInputFactory::kNumParticleTypes ; ++k )
	 {
	    powers[ 0 ][ counter + k ] = particleContents[ k ] ;
	 }
	 counter += HDBStandardFitInputFactory::kNumParticleTypes ;

	 // Uncertainty associated with each fit parameter (column-wise).
	 const HepMatrix& predPowersCol =
	    m_fitPredictions->element( j )->powerMatrix() ;
	 for( int k = 0 ; k < nFitParams ; ++k )
	 {
	    powers[ 0 ][ counter + k ] = predPowersCol[ 0 ][ k ] ;
	 }
	 counter += nFitParams ;

	 // Before 20060928, the following uncertainties were mistakenly
	 // made column-wise instead of row-wise.

	 // Uncertainty per yield.
	 powers[ 0 ][ counter++ ] = 1. ;
	 // Uncertainty per D (row-wise).  Single tags come before double tags.
	 powers[ 0 ][ counter++ ] = i < nSingle ? 1. : 2. ;
	 // Fit-parameter-dependent uncertainty correlated across all
	 // D's (row-wise).  Set these elements of power matrix
	 // after parameter input.
	 if( modeDepDIndex == -1 )
	 {
	    modeDepDIndex = counter ;
	 }
	 else if( modeDepDIndex != counter )
	 {
	    cout << "PROBLEM WITH COUNTING MODEDEPDINDEX" << endl ;
	 }
	 ++counter ;
	 // Uncertainty per single tag (row-wise).
	 powers[ 0 ][ counter++ ] = i < nSingle ? 1. : 0. ;
	 // Fit-parameter-dependent uncertainty correlated across all
	 // single tags (row-wise).  Set these elements of power matrix
	 // after parameter input.
	 if( modeDepSTIndex == -1 )
	 {
	    modeDepSTIndex = counter ;
	 }
	 else if( modeDepSTIndex != counter )
	 {
	    cout << "PROBLEM WITH COUNTING MODEDEPSTINDEX" << endl ;
	 }
	 ++counter ;
	 // Uncertainty per double tag (row-wise).
	 powers[ 0 ][ counter++ ] = i < nSingle ? 0. : 1. ;

	 HDBVariableMatrixElement* element = sigEffMatrix.element( i, j ) ;
	 element->setConstantVector( constants ) ;
	 element->setPowerMatrix( powers ) ;
	 element->setName( "Signal efficiency" ) ;
	 element->setComment1( m_fitPredictions->element( i )->name() ) ;
	 element->setComment2( m_fitPredictions->element( j )->name() ) ;
      }

      // Background
      for( int j = 0 ; j < nBkg ; ++j ) // column
      {
	 HepVector constants( 1, 1 ) ;
	 HepMatrix powers( 1, nUncert, 0 ) ;

	 // Row for fractional uncertainties.

	 // Uncertainties for particle efficiencies.
	 constants[ 0 ] = bkgEffs[ i ][ j ] ;
	 int counter = nUncorr ;
	 for( int k=0 ; k<HDBStandardFitInputFactory::kNumParticleTypes ; ++k )
	 {
	    powers[ 0 ][ counter + k ] = particleContents[ k ] ;
	 }
	 counter += HDBStandardFitInputFactory::kNumParticleTypes ;

	 // Parameters for the fit parameters are not needed for the
	 // background efficiency matrix.
	 counter += nFitParams ;

	 // Before 20060928, the following uncertainties were mistakenly
	 // made column-wise instead of row-wise.

	 // Uncertainty per yield.
	 powers[ 0 ][ counter++ ] = 1. ;
	 // Uncertainty per D (row-wise).  Single tags come before double tags.
	 powers[ 0 ][ counter++ ] = i < nSingle ? 1. : 2. ;
	 // Fit-parameter-dependent uncertainty correlated across all
	 // D's (row-wise).  Set these elements of power matrix
	 // after parameter input.
	 if( modeDepDIndex == -1 )
	 {
	    modeDepDIndex = counter ;
	 }
	 else if( modeDepDIndex != counter )
	 {
	    cout << "PROBLEM WITH COUNTING MODEDEPDINDEX" << endl ;
	 }
	 ++counter ;
	 // Uncertainty per single tag (row-wise).
	 powers[ 0 ][ counter++ ] = i < nSingle ? 1. : 0. ;
	 // Fit-parameter-dependent uncertainty correlated across all
	 // single tags (row-wise).  Set these elements of power matrix
	 // after parameter input.
	 if( modeDepSTIndex == -1 )
	 {
	    modeDepSTIndex = counter ;
	 }
	 else if( modeDepSTIndex != counter )
	 {
	    cout << "PROBLEM WITH COUNTING MODEDEPSTINDEX" << endl ;
	 }
	 ++counter ;
	 // Uncertainty per double tag (row-wise).
	 powers[ 0 ][ counter++ ] = i < nSingle ? 0. : 1. ;

	 HDBVariableMatrixElement* element = bkgEffMatrix.element( i, j ) ;
	 element->setConstantVector( constants ) ;
	 element->setPowerMatrix( powers ) ;
	 element->setName( "Background efficiency" ) ;
	 element->setComment1( m_fitPredictions->element( i )->name() ) ;
	 element->setComment2( m_backgroundNames[ j ] ) ;
      }
   }

   // Get uncertainty for each source.
   HepVector effParams( nUncert, 0 ) ;
   HepVector effParamErrors( nUncert, 0 ) ;
   vector< string > effParamNames ;

   // Uncorrelated signal efficiency.
   for( int i = 0 ; i < nMeas ; ++i )
   {
      for( int j = 0 ; j < nMeas ; ++j )
      {
	 if( ( i < nSingle && j < nSingle ) ||   // single tags
	     ( i >= nSingle && j >= nSingle ) || // double tags
	     ( m_standardInputData->singleTagsExclusive() &&
	       i < nSingle && j >= nSingle ) )
	 {
// 	    cout << "Enter absolute uncertainty on signal efficiency "
// 		 << m_fitPredictions->element( j )->name()
// 		 << " --> " << m_fitPredictions->element( i )->name()
// 		 << ": " ;

	    double err ;
	    cin >> err ;
	    sigEffMatrix.element( i, j )->setUncorrelatedError( err ) ;
	 }
      }
   }

   // Uncorrelated background efficiency.
   for( int i = 0 ; i < nMeas ; ++i )
   {
      for( int j = 0 ; j < nBkg ; ++j )
      {
// 	 cout << "Enter absolute uncertainty for background efficiency "
// 	      << m_backgroundNames[ j ]
// 	      << " --> " << m_fitPredictions->element( i )->name()
// 	      << ": " ;

	 double err ;
	 cin >> err ;
	 bkgEffMatrix.element( i, j )->setUncorrelatedError( err ) ;
      }
   }

   // Particle content.
   cout << "Enter fractional uncertainty for tracks: " ;
   cin >> effParamErrors[ effParamNames.size() +
			HDBStandardFitInputFactory::kTrack ] ;
   cout << "Enter fractional uncertainty for charged pions: " ;
   cin >> effParamErrors[ effParamNames.size() +
			HDBStandardFitInputFactory::kChargedPion ] ;
   cout << "Enter fractional uncertainty for charged kaons: " ;
   cin >> effParamErrors[ effParamNames.size() +
			HDBStandardFitInputFactory::kChargedKaon ] ;
   cout << "Enter fractional uncertainty for electrons: " ;
   cin >> effParamErrors[ effParamNames.size() +
                        HDBStandardFitInputFactory::kElectron ] ;
   cout << "Enter fractional uncertainty for showers: " ;
   cin >> effParamErrors[ effParamNames.size() +
			HDBStandardFitInputFactory::kShower ] ;
   cout << "Enter fractional uncertainty for K0S: " ;
   cin >> effParamErrors[ effParamNames.size() +
			HDBStandardFitInputFactory::kKshort ] ;
   cout << "Enter fractional uncertainty for pi0s: " ;
   cin >> effParamErrors[ effParamNames.size() +
			HDBStandardFitInputFactory::kPi0 ] ;
   cout << "Enter fractional uncertainty for eta(->gammagamma)s: " ;
   cin >> effParamErrors[ effParamNames.size() +
                        HDBStandardFitInputFactory::kEtaToGammaGamma ] ;

   cout << "Enter correction factor for tracks: " ;
   cin >> effParams[ effParamNames.size() +
		   HDBStandardFitInputFactory::kTrack ] ;
   cout << "Enter correction factor for charged pions: " ;
   cin >> effParams[ effParamNames.size() +
		   HDBStandardFitInputFactory::kChargedPion ] ;
   cout << "Enter correction factor for charged kaons: " ;
   cin >> effParams[ effParamNames.size() +
		   HDBStandardFitInputFactory::kChargedKaon ] ;
   cout << "Enter correction factor for electrons: " ;
   cin >> effParams[ effParamNames.size() +
                   HDBStandardFitInputFactory::kElectron ] ;
   cout << "Enter correction factor for showers: " ;
   cin >> effParams[ effParamNames.size() +
		   HDBStandardFitInputFactory::kShower ] ;
   cout << "Enter correction factor for K0S: " ;
   cin >> effParams[ effParamNames.size() +
		   HDBStandardFitInputFactory::kKshort ] ;
   cout << "Enter correction factor for pi0s: " ;
   cin >> effParams[ effParamNames.size() +
		   HDBStandardFitInputFactory::kPi0 ] ;
   cout << "Enter correction factor for eta(->gammagamma)s: " ;
   cin >> effParams[ effParamNames.size() +
                   HDBStandardFitInputFactory::kEtaToGammaGamma ] ;

   for( int i = 0 ; i < HDBStandardFitInputFactory::kNumParticleTypes ; ++i )
   {
      if( i == HDBStandardFitInputFactory::kTrack )
      {
	 effParamNames.push_back( "Track uncertainty" ) ;
      }
      else if( i == HDBStandardFitInputFactory::kChargedPion )
      {
	 effParamNames.push_back( "Charged pion uncertainty" ) ;
      }
      else if( i == HDBStandardFitInputFactory::kChargedKaon )
      {
	 effParamNames.push_back( "Charged kaon uncertainty" ) ;
      }
      else if( i == HDBStandardFitInputFactory::kElectron )
      {
         effParamNames.push_back( "Electron uncertainty" ) ;
      }
      else if( i == HDBStandardFitInputFactory::kShower )
      {
	 effParamNames.push_back( "Shower uncertainty" ) ;
      }
      else if( i == HDBStandardFitInputFactory::kKshort )
      {
	 effParamNames.push_back( "K0S uncertainty" ) ;
      }
      else if( i == HDBStandardFitInputFactory::kPi0 )
      {
	 effParamNames.push_back( "Pi0 uncertainty" ) ;
      }
      else if( i == HDBStandardFitInputFactory::kEtaToGammaGamma )
      {
         effParamNames.push_back( "Eta->gammagamma uncertainty" ) ;
      }
   }

   // Fit parameters (column-wise).
   for( int i = 0 ; i < nFitParams ; ++i )
   {
      cout << "Enter fractional column-wise uncertainty for "
	   << m_fitParameterNames[ i ] << ": " ;
      cin >> effParamErrors[ effParamNames.size() ] ;
      effParams[ effParamNames.size() ] = 1. ;

      effParamNames.push_back( m_fitParameterNames[ i ] + " col" ) ;
   }

   // Per yield.
   cout << "Enter fractional uncertainty per yield: " ;
   cin >> effParamErrors[ effParamNames.size() ] ;
   effParams[ effParamNames.size() ] = 1. ;
   effParamNames.push_back( "Yield" ) ;

   // Per D (row-wise).
   cout << "Enter fractional row-wise uncertainty per D: " ;
   cin >> effParamErrors[ effParamNames.size() ] ;
   effParams[ effParamNames.size() ] = 1. ;
   effParamNames.push_back( "D" ) ;

   // Fit-parameter-dependent D error (row-wise).
   HepVector modeDepDErrors( nFitParams, 0 ) ;
   int firstNonZeroD = -1 ;
   for( int i = 0 ; i < nFitParams ; ++i )
   {
      cout << "Enter fractional row-wise D uncertainty for "
	   << m_fitParameterNames[ i ] << ": " ;
      cin >> modeDepDErrors[ i ] ;

      if( modeDepDErrors[ i ] > 0. && firstNonZeroD == -1 )
      {
	 firstNonZeroD = i ;
      }
   }

   // Set the parameter error to the first non-zero value.
   effParamErrors[ effParamNames.size() ] = modeDepDErrors[ firstNonZeroD ] ;
   effParams[ effParamNames.size() ] = 1. ;
   effParamNames.push_back( "Mode-dependent D" ) ;

   // Normalize modeDepDErrors to first non-zero element.  These will now
   // be used as elements of the power matrix.  I.e. we use fractional
   // powers to adjust the size of the error while keeping the full
   // correlations.  This only works if the parameter is 1.
   modeDepDErrors /= modeDepDErrors[ firstNonZeroD ] ;

   // Set power matrix for fit-parameter-dependent single/double tag errors.
   for( int i = 0 ; i < nMeas ; ++i )    // row
   {
      const HepMatrix& predPowersRow =
	 m_fitPredictions->element( i )->powerMatrix() ;

      // Count the number of parameters for this yield with non-zero
      // mode-dependent errors.  Should be 0, 1, or 2.
      int numNonZeroParams = 0 ;
      double dPower = 0. ;
      for( int k = 0 ; k < nFitParams ; ++k )
      {
	 if( predPowersRow[ 0 ][ k ] * modeDepDErrors[ k ] > 0. )
	 {
	    ++numNonZeroParams ;
	    dPower += predPowersRow[ 0 ][ k ] * modeDepDErrors[ k ] ;
	 }
      }

      if( numNonZeroParams == 1 || numNonZeroParams == 2 )
      {
	 // Signal
	 for( int j = 0 ; j < nMeas ; ++j ) // column
	 {
	    HepMatrix powers = sigEffMatrix.element( i, j )->powerMatrix();
	    powers[ 0 ][ modeDepDIndex ] = dPower ;
	    sigEffMatrix.element( i, j )->setPowerMatrix( powers ) ;
	 }

	 // Background
	 for( int j = 0 ; j < nBkg ; ++j ) // column
	 {
	    HepMatrix powers = bkgEffMatrix.element( i, j )->powerMatrix();
	    powers[ 0 ][ modeDepDIndex ] = dPower ;
	    bkgEffMatrix.element( i, j )->setPowerMatrix( powers ) ;
	 }
      }
   }

   // Per single tag (row-wise).
   cout << "Enter fractional row-wise uncertainty per single tag: " ;
   cin >> effParamErrors[ effParamNames.size() ] ;
   effParams[ effParamNames.size() ] = 1. ;
   effParamNames.push_back( "Single tag" ) ;

   // Fit-parameter-dependent single tag error (row-wise).
   HepVector modeDepSTErrors( nFitParams, 0 ) ;
   int firstNonZero = -1 ;
   for( int i = 0 ; i < nFitParams ; ++i )
   {
      cout << "Enter fractional row-wise single tag uncertainty for "
	   << m_fitParameterNames[ i ] << ": " ;
      cin >> modeDepSTErrors[ i ] ;

      if( modeDepSTErrors[ i ] > 0. && firstNonZero == -1 )
      {
	 firstNonZero = i ;
      }
   }

   // Set the parameter error to the first non-zero value.
   effParamErrors[ effParamNames.size() ] = modeDepSTErrors[ firstNonZero ] ;
   effParams[ effParamNames.size() ] = 1. ;
   effParamNames.push_back( "Mode-dependent single tag" ) ;

   // Normalize modeDepSTErrors to first non-zero element.  These will now
   // be used as elements of the power matrix.  I.e. we use fractional
   // powers to adjust the size of the error while keeping the full
   // correlations.  This only works if the parameter is 1.
   modeDepSTErrors /= modeDepSTErrors[ firstNonZero ] ;

   // Set power matrix for fit-parameter-dependent single tag errors.
   for( int i = 0 ; i < nMeas ; ++i )    // row
   {
      if( i < nSingle )
      {
	 const HepMatrix& predPowersRow =
	    m_fitPredictions->element( i )->powerMatrix() ;

	 // Count the number of parameters for this yield with non-zero
	 // mode-dependent errors.  Should be 0 or 1.
	 int numNonZeroParams = 0 ;
	 double stPower ;
	 for( int k = 0 ; k < nFitParams ; ++k )
	 {
	    if( predPowersRow[ 0 ][ k ] * modeDepSTErrors[ k ] > 0. )
	    {
	       ++numNonZeroParams ;
	       stPower = modeDepSTErrors[ k ] ;
	    }
	 }

	 if( numNonZeroParams == 1 )
	 {
	    // Signal
	    for( int j = 0 ; j < nMeas ; ++j ) // column
	    {
	       HepMatrix powers = sigEffMatrix.element( i, j )->powerMatrix();
	       powers[ 0 ][ modeDepSTIndex ] = stPower ;
	       sigEffMatrix.element( i, j )->setPowerMatrix( powers ) ;
	    }

	    // Background
	    for( int j = 0 ; j < nBkg ; ++j ) // column
	    {
	       HepMatrix powers = bkgEffMatrix.element( i, j )->powerMatrix();
	       powers[ 0 ][ modeDepSTIndex ] = stPower ;
	       bkgEffMatrix.element( i, j )->setPowerMatrix( powers ) ;
	    }
	 }
      }
   }

   // Per double tag (row-wise).
   cout << "Enter fractional row-wise uncertainty per double tag: " ;
   cin >> effParamErrors[ effParamNames.size() ] ;
   effParams[ effParamNames.size() ] = 1. ;
   effParamNames.push_back( "Double tag" ) ;

   sigEffMatrix.setParameterNames( effParamNames ) ;
   bkgEffMatrix.setParameterNames( effParamNames ) ;

   m_standardInputData->setSignalEfficiencyMatrix( sigEffMatrix ) ;
   m_standardInputData->setBackgroundEfficiencyMatrix( bkgEffMatrix ) ;
   m_standardInputData->setEfficiencyParameters( effParams ) ;
   m_standardInputData->setEfficiencyParameterErrors( effParamErrors ) ;

   m_efficienciesDefined = true ;
}

//
// const member functions
//

//
// static member functions
//
