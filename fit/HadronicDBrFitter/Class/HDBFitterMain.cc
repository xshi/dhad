// -*- C++ -*-
//
// Package:     <HadronicDBrFitter>
// Module:      HDBFitterMain
// 
// Description: <one line class summary>
//
// Implementation:
//     <Notes on implementation>
//
// Author:      Werner Sun
// Created:     Tue Apr 13 15:13:29 EDT 2004
// $Id$
//
// Revision history
//
// $Log$

#include <iostream>
#include <string>
#include "HadronicDBrFitter/HDBStandardFitInputFactoryTTY.h"
#include "HadronicDBrFitter/HDBChisqMinimizer.h"
#include "HadronicDBrFitter/HDBChisqFitIterator.h"
#include "HadronicDBrFitter/HDBStandardMCInputData.h"

using namespace std ;

void printResults( const HDBParameterEstimator& aParameterEstimator,
		   HDBStandardFitInputFactory& aFactory,
		   const HepVector& aSeedErrorVector,// tells which params
		   const HepSymMatrix& aSeedErrorMatrix ) ;    // to ignore

string itoa( int ) ;

extern "C"
{
   extern float prob_( const float&, const int& ) ;
   extern void  hropen_( const int&, const char*, const char*, const char*,
			 const int&, const int&,
			 const int, const int, const int ) ;
   extern void  hbookn_( const int&, const char*, const int&, const char*,
			 const int&, const char*,
			 const int, const int, const int ) ;
   extern void  hfn_( const int&, const float* ) ;
   extern void  hrout_( const int&, const int&, const char*, const int ) ;
   extern void  hrend_( const char*, const int ) ;
   extern void  hbookinit_( void ) ;
   extern void  closelun_( const int& ) ;
}


int main()
{
   cout << endl ;
   cout << "HADRONIC D BRANCHING FRACTION FITTER" << endl ;
   cout << "------------------------------------" << endl << endl ;

   string exclusiveStr ;
   cout << "Are single tags exclusive (y/n)? " ;
   cin >> exclusiveStr ;
   bool exclusiveSingleTags = exclusiveStr == "y" || exclusiveStr == "Y" ;

   string genMCStr ;
   cout << "Generate toy MC (y/n)? " ;
   cin >> genMCStr ;
   bool genMC = genMCStr == "y" || genMCStr == "Y" ;

   HDBStandardFitInputFactoryTTY inputFactory( exclusiveSingleTags, genMC ) ;

   int numberNtupleFields = 0 ;

   int nTrials = 1 ;
   string hbookFilename ;
   if( genMC )
   {
      cout << "Number of trials: " ;
      cin >> nTrials ;
      cout << "HBOOK file name: " ;
      cin >> hbookFilename ;

      // Initialize random seed.
      srandom( 3 ) ;

      // Initialize HBOOK and book ntuple.
      hbookinit_() ;

      int istat ;
      hropen_( 80, "output", hbookFilename.data(), "N", 1024, istat,
	       6, hbookFilename.length(), 1 ) ;

      // Construct string with field names.
      vector< string > fieldNames ;

      fieldNames.push_back( "trial" ) ;
      fieldNames.push_back( "chisq" ) ;
      fieldNames.push_back( "ndof" ) ;
      fieldNames.push_back( "cl" ) ;
      fieldNames.push_back( "niter" ) ;


      int maxLength = 5 ;
      for( int i = 1 ; i <= inputFactory.numberFitParameters() ; ++i )
      {
	 string nameString = "par" + itoa( i ) ;

	 if( nameString.length() + 1 > maxLength )
	 {
	    maxLength = nameString.length() + 1 ;
	 }

	 fieldNames.push_back( nameString ) ;
	 fieldNames.push_back( "d" + nameString ) ;
      }

      for( int i = 1 ; i <= inputFactory.numberInputYields() ; ++i )
      {
	 string nameString = "yield" + itoa( i ) ;

	 if( nameString.length() > maxLength )
	 {
	    maxLength = nameString.length() ;
	 }

	 fieldNames.push_back( nameString ) ;
      }

      for( int i = 1 ; i <= inputFactory.numberInputYields() ; ++i )
      {
	 string nameString = "eff" + itoa( i ) ;

	 if( nameString.length() > maxLength )
	 {
	    maxLength = nameString.length() ;
	 }

	 fieldNames.push_back( nameString ) ;
      }

      for( int i = 1 ; i <= inputFactory.numberInputYields() ; ++i )
      {
	 string nameString = "cyield" + itoa( i ) ;

	 if( nameString.length() > maxLength )
	 {
	    maxLength = nameString.length() ;
	 }

	 fieldNames.push_back( nameString ) ;
      }

      // All the tags must be contained in a single string, with the same
      // number of characters for each field, so pad field names with
      // spaces as necessary.
      vector< string >::const_iterator nameItr = fieldNames.begin() ;
      vector< string >::const_iterator nameEnd = fieldNames.end() ;
      string tags ;
      for( ; nameItr != nameEnd ; ++nameItr )
      {
	 tags += *nameItr ;

	 for( int i = nameItr->length() ; i < maxLength ; ++i )
	 {
	    tags += " " ;
	 }
      }

      numberNtupleFields = fieldNames.size() ;
      hbookn_( 1, "stuff", numberNtupleFields, " ", 30000, tags.data(),
	       5, 1, maxLength ) ;

      cout << "Ntuple has " << numberNtupleFields << " fields:" << endl
	   << tags << endl ;
   }

   // ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   HDBChisqMinimizer chisqMinimizer( &inputFactory ) ;

   HDBChisqFitIterator fitIterator(
      &chisqMinimizer,
      10,       // max iterations
      0.001 ) ;  // max delta chisq
   cout << "Using iterated least squares minimization." << endl ;

//    HepVector ext( 5, 0 ) ;
//    ext[ 0 ] = 0.00374 ;
//    ext[ 1 ] = 0.0391 ;
//    ext[ 2 ] = 0.02417 ;
//    ext[ 3 ] = 0.03770 ;
//    ext[ 4 ] = 0.035 ;

//    HepSymMatrix extErr( 5, 0 ) ;
//    extErr[ 0 ][ 0 ] = 0.00018 * 0.00018 ;
//    extErr[ 1 ][ 1 ] = 0.0009 * 0.0009 ;
//    extErr[ 2 ][ 2 ] = 0.00416 * 0.00416 ;
//    extErr[ 3 ][ 3 ] = 0.00246 * 0.00246 ;
//    extErr[ 4 ][ 4 ] = 0.0005 * 0.0005 ;

//    vector< int > map ;
//    map.push_back( 2 ) ;
//    map.push_back( 5 ) ;
//    map.push_back( 6 ) ;
//    map.push_back( 7 ) ;
//    map.push_back( 10 ) ;

//    chisqMinimizer.setExternalParameters( HDBData( ext, extErr ), map ) ;

   // ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   if( !genMC )
   {
      inputFactory.setPrintDiagnostics( true ) ;
      chisqMinimizer.setPrintDiagnostics( true ) ;
//       inputFactory.setPrintDiagnostics( false ) ;
//       chisqMinimizer.setPrintDiagnostics( false ) ;
      inputFactory.initializeInputData() ;
      fitIterator.estimateParameters() ;

      const vector< string >& fitParameterNames =
	 inputFactory.fitPredictions()->parameterNames() ;
      int nParams = fitParameterNames.size() ;

      HepSymMatrix seedErrorMatrix( nParams, 0 ) ;
      HepVector seedErrors( nParams, 0 ) ;
      string enterSeedErrors ;
      cout << "Enter seed errors? (y/n): " << endl ;
      cin >> enterSeedErrors ;
      if( enterSeedErrors == "y" || enterSeedErrors == "Y" )
      {
	 for( int i = 0 ; i < nParams ; ++i )
	 {
	    cout << "Enter error on " << fitParameterNames[ i ]
		 << " seed (negative errors remove parameter from chi2): "
		 << endl ;
	    cin >> seedErrors[ i ] ;
	 }

	 for( int i = 0 ; i < nParams ; ++i )
	 {
	    // Diagonal element
	    seedErrorMatrix[ i ][ i ] = seedErrors[ i ] > 0. ?
	       seedErrors[ i ] * seedErrors[ i ] : 1.e30 ;

	    // Off-diagonal elements
	    for( int j = i + 1 ; j < nParams ; ++j )
	    {
	       cout << "Enter correlation coefficient between "
		    << fitParameterNames[ i ] << " and "
		    << fitParameterNames[ j ] << endl ;
	       cin >> seedErrorMatrix[ i ][ j ] ;
	       seedErrorMatrix[ i ][ j ] *=
		  ( seedErrors[ i ] > 0. && seedErrors[ j ] > 0. ) ?
		  seedErrors[ i ] * seedErrors[ j ] : 0. ;
	    }
	 }
      }

      cout << "Number of iterations: " << fitIterator.numberOfIterations()
	   << endl ;

      if( fitIterator.fitStatus() !=
	  HDBParameterEstimator::kFitSuccessful )
      {
	 cout << "Fit failed!" << endl ;
      }
      else
      {
	 cout << "Fit successful." << endl
	      << "chisq " << fitIterator.chisq()
	      << " ndof " << fitIterator.ndof()
	      << " prob " << prob_( float( fitIterator.chisq() ),
				    int( fitIterator.ndof() ) )
	      << endl
	      << "CHISQ " << fitIterator.chisq() << " 0.0001"
	      << endl << endl ;
      }

      printResults( fitIterator, inputFactory, seedErrors, seedErrorMatrix ) ;

      // Calculate branching fractions and NDDbar mode by mode.
      HDBStandardInputData* inputData =
	 dynamic_cast< HDBStandardInputData* >( inputFactory.inputData() ) ;

//       cout << "Corrected efficiencies" << endl; 
//       HepMatrix effs = inputData->signalEfficiencyValues() ;
//       HepSymMatrix deffs = inputData->signalEfficiencyErrorMatrix() ;
//       int neffs = effs.num_row() ;
//       for( int i = 0 ; i < neffs ; ++i )
//       {
// 	 cout << effs[ i ][ i ] << " +- "
// 	      << sqrt( deffs[ i * ( neffs + 1 ) ][ i * ( neffs + 1 ) ] )
// 	      << endl;
//       }

      const HepVector& yields = inputData->values() ;
      const HepSymMatrix& errors = inputData->errorMatrix() ;

      int nSingle = inputData->numberSingleTagYields() ;
      int nDouble = inputData->numberDoubleTagYields() ;
      const vector< pair< int, int > >& xrefs =
	 inputData->doubleToSingleCrossReference() ;

      vector< HDBVariableMatrixElement > brs ;
      vector< HDBVariableMatrixElement > ndds ;
      for( int i = 0 ; i < nDouble ; ++i )
      {
	 int doubleIndex = i + nSingle ;

	 int singleIndex1 = xrefs[ i ].first ;
	 if( singleIndex1 != -1 )
	 {
	    HDBVariableMatrixElement element ;

	    element.setConstantVector( HepVector( 1, 1 ) ) ;

	    HepMatrix powers( 1, yields.num_row(), 0 ) ;
	    powers[ 0 ][ doubleIndex ] = 1. ;
	    powers[ 0 ][ singleIndex1 ] = -1. ;
	    element.setPowerMatrix( powers ) ;

	    element.setName(
	       "(" +
	       inputFactory.fitPredictions()->element( doubleIndex )->name() +
	       ") / (" +
	       inputFactory.fitPredictions()->element( singleIndex1 )->name() +
	       ")");

	    brs.push_back( element ) ;
	 }

	 int singleIndex2 = xrefs[ i ].second ;
	 if( singleIndex2 != -1 )
	 {
	    HDBVariableMatrixElement element ;

	    element.setConstantVector( HepVector( 1, 1 ) ) ;

	    HepMatrix powers( 1, yields.num_row(), 0 ) ;
	    powers[ 0 ][ doubleIndex ] = 1. ;
	    powers[ 0 ][ singleIndex2 ] = -1. ;
	    element.setPowerMatrix( powers ) ;

	    element.setName(
	       "(" +
	       inputFactory.fitPredictions()->element( doubleIndex )->name() +
	       ") / (" +
	       inputFactory.fitPredictions()->element( singleIndex2 )->name() +
	       ")");

	    brs.push_back( element ) ;
	 }

	 if( singleIndex1 != -1 && singleIndex2 != -1 )
	 {
	    HDBVariableMatrixElement element ;

	    element.setConstantVector( HepVector( 1, 1 ) ) ;

	    HepMatrix powers( 1, yields.num_row(), 0 ) ;
	    powers[ 0 ][ doubleIndex ] = -1. ;
	    powers[ 0 ][ singleIndex1 ] = 1. ;
	    powers[ 0 ][ singleIndex2 ] = 1. ;
	    element.setPowerMatrix( powers ) ;

	    element.setName(
	       "(" +
	       inputFactory.fitPredictions()->element( singleIndex1 )->name() +
	       " * " +
	       inputFactory.fitPredictions()->element( singleIndex2 )->name() +
	       ") / (" +
	       inputFactory.fitPredictions()->element( doubleIndex )->name() +
	       ")");

	    ndds.push_back( element ) ;
	 }
      }

      // Calculate NDDs and print them out.

      HDBVariableVector nddVector( ndds.size() ) ;
      for( int i = 0 ; i < ndds.size() ; ++i )
      {
	 *( nddVector.element( i ) ) = ndds[ i ] ;
      }

      HepVector nddValues = nddVector.values( yields ) ;
      HepSymMatrix nddErrors = nddVector.errorMatrix( yields, errors ) ;

      cout << endl << "NDD mode by mode:" << endl << endl ;
      for( int i = 0 ; i < ndds.size() ; ++i )
      {
	 cout << nddVector.element( i )->name() << " = "
	      << nddValues[ i ] << " +- "
	      << sqrt( nddErrors[ i ][ i ] )
	      << endl ;
      }

      HepSymMatrix corrCoeffs = nddErrors ;
      for( int j = 0 ; j < ndds.size() ; ++j )
      {
	 for( int k = j ; k < ndds.size() ; ++k )
	 {
	    corrCoeffs[ j ][ k ] /=
	       sqrt( nddErrors[ j ][ j ] * nddErrors[ k ][ k ] ) ;
	 }
      }

      // Calculate branching fractions and print them out.

      HDBVariableVector brVector( brs.size() ) ;
      for( int i = 0 ; i < brs.size() ; ++i )
      {
	 *( brVector.element( i ) ) = brs[ i ] ;
      }

      HepVector brValues = brVector.values( yields ) ;
      HepSymMatrix brErrors = brVector.errorMatrix( yields, errors ) ;

      cout << endl << "Branching fractions mode by mode:" << endl << endl ;
      for( int i = 0 ; i < brs.size() ; ++i )
      {
	 cout << brVector.element( i )->name() << " = "
	      << brValues[ i ] << " +- "
	      << sqrt( brErrors[ i ][ i ] )
	      << endl ;
      }

      corrCoeffs = brErrors ;
      for( int j = 0 ; j < brs.size() ; ++j )
      {
	 for( int k = j ; k < brs.size() ; ++k )
	 {
	    corrCoeffs[ j ][ k ] /=
	       sqrt( brErrors[ j ][ j ] * brErrors[ k ][ k ] ) ;
	 }
      }
   }
   else
   {
      HepVector means( inputFactory.numberFitParameters(), 0 ) ;
      HepSymMatrix error( inputFactory.numberFitParameters(), 0 ) ;

      int nyield = inputFactory.numberInputYields() ;
      HepVector yieldMeans( nyield, 0 ) ;
      HepSymMatrix yieldErrors( nyield, 0 ) ;

      int nyield2 = nyield * nyield ;
      HepMatrix effMeans( nyield, nyield, 0 ) ;
      HepSymMatrix effErrors( nyield2, 0 ) ;

      for( int i = 0 ; i < nTrials ; ++i )
      {
	 chisqMinimizer.resetSeeds( &inputFactory ) ;

	 cout << "MC trial " << i << endl ;

 	 if( i == 4 )
	 {
	    inputFactory.setPrintDiagnostics( true ) ;
	    chisqMinimizer.setPrintDiagnostics( true ) ;
	    fitIterator.setPrintDiagnostics( true ) ;
	 }
	 else
	 {
	    inputFactory.setPrintDiagnostics( false ) ;
	    chisqMinimizer.setPrintDiagnostics( false ) ;
	    fitIterator.setPrintDiagnostics( false ) ;
	 }

	 inputFactory.initializeInputData() ; // generate MC
	 fitIterator.estimateParameters() ;

	 if( fitIterator.fitStatus() ==
	     HDBParameterEstimator::kFitSuccessful )
	 {
	    const HepVector& fittedParams =
	       fitIterator.fittedParameters().values() ;
	    const HepSymMatrix& fittedError =
	       fitIterator.fittedParameters().errorMatrix() ;

	    // Fill ntuple.
	    int index = 0 ;
	    float array[ numberNtupleFields ] ;
	    array[ index++ ] = i ;
	    array[ index++ ] = fitIterator.chisq() ;
	    array[ index++ ] = fitIterator.ndof() ;
	    if( fitIterator.ndof() > 0 )
	    {
	       array[ index++ ] = prob_( float( fitIterator.chisq() ),
					 int( fitIterator.ndof() ) ) ;
	    }
	    else
	    {
	       index++ ;
	    }
	    array[ index++ ] = fitIterator.numberOfIterations() ;

	    // Fitted parameters and errors.
	    for( int i = 0 ; i < fittedParams.num_row() ; ++i )
	    {
	       array[ index++ ] = fittedParams[ i ] ;
	       array[ index++ ] = ( fittedError[ i ][ i ] > 0. ?
				    sqrt( fittedError[ i ][ i ] ) : 0. ) ;
	    }

	    HDBStandardMCInputData* inputData =
	       dynamic_cast< HDBStandardMCInputData* >(
		  inputFactory.inputData() ) ;
	    HepVector yields = inputData->yieldValues() ;

	    // Generated uncorrected yields.
	    for( int i = 0 ; i < inputFactory.numberInputYields() ; ++i )
	    {
	       array[ index++ ] = yields[ i ] ;
	    }

	    // Generated efficiencies (diagonal only).
	    HepMatrix effs = inputData->generatedSignalEfficiencyValues() ;

	    for( int i = 0 ; i < inputFactory.numberInputYields() ; ++i )
	    {
	       array[ index++ ] = effs[ i ][ i ] ;
	    }

	    // Generated corrected yields (efficiency and background).
	    for( int i = 0 ; i < inputFactory.numberInputYields() ; ++i )
	    {
	       array[ index++ ] = inputFactory.inputData()->value( i ) ;
	    }

	    // Fill ntuple.
	    hfn_( 1, array ) ;

	    // Accumulate means and error (assume all trials succeed).
	    means += fittedParams / nTrials ;
	    yieldMeans += yields / nTrials ;
	    effMeans += effs / nTrials ;

	    for( int j = 0 ; j < inputFactory.numberFitParameters() ; ++j )
	    {
	       for( int k = j ; k < inputFactory.numberFitParameters() ; ++k )
	       {
		  error[ j ][ k ] +=
		     fittedParams[ j ] * fittedParams[ k ] / nTrials ;
	       }
	    }

	    for( int j = 0 ; j < nyield ; ++j )
	    {
	       for( int k = j ; k < nyield ; ++k )
	       {
		  yieldErrors[ j ][ k ] +=
		     yields[ j ] * yields[ k ] / nTrials ;
	       }
	    }

	    int row1 = 0 ;
	    int col1 = 0 ;

	    for( int j = 0 ; j < nyield2 ; ++j )
	    {
	       int row2 = row1 ;
	       int col2 = col1 ;

	       for( int k = j ; k < nyield2 ; ++k )
	       {
		  effErrors[ j ][ k ] +=
		     effs[ row1 ][ col1 ] * effs[ row2 ][ col2 ] / nTrials ;

		  if( ++col2 == nyield )
		  {
		     ++row2 ;
		     col2 = 0 ;
		  }
	       }

	       if( ++col1 == nyield )
	       {
		  ++row1 ;
		  col1 = 0 ;
	       }
	    }
	 }
      }

      // Finish error matrix.
      for( int j = 0 ; j < inputFactory.numberFitParameters() ; ++j )
      {
	 for( int k = j ; k < inputFactory.numberFitParameters() ; ++k )
	 {
	    error[ j ][ k ] -= means[ j ] * means[ k ] ;
	 }
      }

      HepSymMatrix corrCoeffs = error ;
      for( int j = 0 ; j < inputFactory.numberFitParameters() ; ++j )
      {
	 for( int k = j ; k < inputFactory.numberFitParameters() ; ++k )
	 {
	    corrCoeffs[ j ][ k ] /= sqrt( error[ j ][ j ] * error[ k ][ k ] ) ;
	 }
      }

      for( int j = 0 ; j < nyield ; ++j )
      {
	 for( int k = j ; k < nyield ; ++k )
	 {
	    yieldErrors[ j ][ k ] -= yieldMeans[ j ] * yieldMeans[ k ] ;
	 }
      }

      int row1 = 0 ;
      int col1 = 0 ;

      for( int j = 0 ; j < nyield2 ; ++j )
      {
	 int row2 = row1 ;
	 int col2 = col1 ;

	 for( int k = j ; k < nyield2 ; ++k )
	 {
	    effErrors[ j ][ k ] -=
	       effMeans[ row1 ][ col1 ] * effMeans[ row2 ][ col2 ] ;

	    if( ++col2 == nyield )
	    {
	       ++row2 ;
	       col2 = 0 ;
	    }
	 }

	 if( ++col1 == nyield )
	 {
	    ++row1 ;
	    col1 = 0 ;
	 }
      }

      cout << endl
	   << "Trial means" << endl ;

      const vector< string >& fitParameterNames =
	 inputFactory.fitPredictions()->parameterNames() ;

      for( int i = 0 ; i < inputFactory.numberFitParameters() ; ++i )
      {
	 cout << fitParameterNames[ i ]
	      << " = " << means[ i ] << " +- "
	      << sqrt( error[ i ][ i ] ) << endl ;
      }

      cout << endl << "Trial error" << error << endl
	   << "Trial correlation coefficients" << corrCoeffs << endl ;

      int icycle ;
      hrout_( 0, icycle, " ", 1 ) ;
      hrend_( "output", 6 ) ;
      closelun_( 80 ) ;
   }
}


// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

void
printResults( const HDBParameterEstimator& aParameterEstimator,
	      HDBStandardFitInputFactory& aFactory,
	      const HepVector& aSeedErrorVector, //tells which params to ignore
	      const HepSymMatrix& aSeedErrorMatrix )
{
   HepVector fittedParams =
      aParameterEstimator.fittedParameters().values() ;
   HepSymMatrix fittedError =
      aParameterEstimator.fittedParameters().errorMatrix() ;

   vector< string > fitParameterNames =
      aFactory.fitPredictions()->parameterNames() ;
   int nParams = fitParameterNames.size() ;

   if( fittedParams.num_row() != nParams )
   {
      cout << "Incorrect number of fitted parameters." << endl ;
      return ;
   }

   cout << "Fitted parameters:" << endl ;
   for( int i = 0 ; i < nParams ; ++i )
   {
      cout << fitParameterNames[ i ]
	   << " = " << fittedParams[ i ] << " +- "
	   << sqrt( fittedError[ i ][ i ] )
	   << " (" << 100. * sqrt( fittedError[ i ][ i ] ) / fittedParams[ i ]
	   << "%)" << endl ;
   }

   cout << endl << "Difference from seeds:" << endl ;
   const HepVector& seeds = aFactory.seedParameters() ;
   HepVector deltaSeeds( nParams ) ;
   for( int i = 0 ; i < nParams ; ++i )
   {
      deltaSeeds[ i ] = fittedParams[ i ] - seeds[ i ] ;

      double seedErrsq =
	 aSeedErrorVector[ i ] > 0. ? aSeedErrorMatrix[ i ][ i ] : 0. ;
      cout << fitParameterNames[ i ] << ": "
	   << deltaSeeds[ i ] / seeds[ i ] * 100. << "% or "
	   << deltaSeeds[ i ] / sqrt( fittedError[ i ][ i ] + seedErrsq )
	   << " sigma from " << seeds[ i ]
	   << " +- " << sqrt( seedErrsq )
	   << " (" << 100. * sqrt( seedErrsq ) / seeds[ i ]
	   << "%)" << endl ;
   }

   cout << endl << "Seed error matrix:" << aSeedErrorMatrix << endl ;

   int ierr ;
   HepSymMatrix fittedErrorInv = fittedError.inverse( ierr ) ;
   HepSymMatrix seedDiffErrorInv =
      ( fittedError + aSeedErrorMatrix ).inverse( ierr ) ;

   // Remove parameters with negative error from chi2.
   int ndof = 0 ;
   for( int i = 0 ; i < nParams ; ++i )
   {
      if( aSeedErrorVector[ i ] < 0. )
      {
	 deltaSeeds[ i ] = 0. ;
      }
      else
      {
	 ++ndof ;
      }
   }

   double chisqSeeds = seedDiffErrorInv.similarity( deltaSeeds ) ;
   double probSeeds = prob_( float( chisqSeeds ), int( ndof ) ) ;
   cout << endl << "Overall difference from seeds: chisq " << chisqSeeds
	<< " ndof " << ndof << " prob " << probSeeds << endl ;

   cout << endl << "Error matrix:" << fittedError << endl ;

   HepSymMatrix corrCoeffs = fittedError ;
   HepVector globalCorrs( nParams, 0 ) ;
   for( int j = 0 ; j < nParams ; ++j )
   {
      for( int k = j ; k < nParams ; ++k )
      {
	 corrCoeffs[ j ][ k ] /=
	    sqrt( fittedError[ j ][ j ] * fittedError[ k ][ k ] ) ;
      }

      globalCorrs[ j ] =
	 sqrt( 1. - 1./( fittedError[ j ][ j ] * fittedErrorInv[ j ][ j ] ) ) ;
   }

   cout << "Correlation coefficients:" << corrCoeffs << endl ;
   cout << "Global correlation coefficients:" << globalCorrs << endl ;

//    string constrainStr ;
//    cout << "Constrain parameters? (y/n)" << endl ;
//    cin >> constrainStr ;

//    if( constrainStr == "y" || constrainStr == "Y" )
//    {
//       int nCons = 0 ;
//       HepSymMatrix externalErrorInv( nParams, 0 ) ;
//       HepVector externalParams( nParams, 0 ) ;

//       string paramStr ;
//       do
//       {
// 	 cout << "Parameter to constrain: " << endl ;
// 	 cin >> paramStr ;

// 	 if( paramStr != "end" )
// 	 {
// 	    int paramIndex = -1 ;
// 	    for( int i = 0 ; i < nParams ; ++i )
// 	    {
// 	       if( fitParameterNames[ i ] == paramStr )
// 	       {
// 		  paramIndex = i ;
// 	       }
// 	    }

// 	    if( paramIndex > -1 )
// 	    {
// 	       ++nCons ;

// 	       double externalMeas ;
// 	       cout << "Enter external measurement of " << paramStr
// 		    << ":" << endl ;
// 	       cin >> externalMeas ;

// 	       double externalError ;
// 	       cout << "Enter external error on " << paramStr
// 		    << ":" << endl ;
// 	       cin >> externalError ;

// 	       externalErrorInv[ paramIndex ][ paramIndex ] =
// 		  1. / ( externalError * externalError ) ;
// 	       externalParams[ paramIndex ] = externalMeas ;
// 	    }
// 	    else
// 	    {
// 	       cout << "No such parameter." << endl ;
// 	    }
// 	 }
//       } while( paramStr != "end" ) ;

//       int ierrtmp ;
//       fittedError = ( fittedErrorInv + externalErrorInv ).inverse( ierrtmp ) ;
//       HepVector fittedParamsCons = fittedError *
// 	 ( fittedErrorInv * fittedParams +
// 	   externalErrorInv * externalParams ) ;

//       double consChi2 =
// 	 fittedErrorInv.similarity( fittedParams - fittedParamsCons ) +
// 	 externalErrorInv.similarity( externalParams - fittedParamsCons ) ;

//       fittedParams = fittedParamsCons ;
//       fittedErrorInv += externalErrorInv ;

//       cout << endl << "Fitted parameters with constraints:" << endl ;
//       cout << "chi2 = " << consChi2 << "/" << nCons << endl ;
//       for( int i = 0 ; i < nParams ; ++i )
//       {
// 	 cout << fitParameterNames[ i ]
// 	      << " = " << fittedParams[ i ] << " +- "
// 	      << sqrt( fittedError[ i ][ i ] )
// 	      << " ("
// 	      << 100. * sqrt( fittedError[ i ][ i ] ) / fittedParams[ i ]
// 	      << "%)" << endl ;
//       }

//       cout << endl ;

//       corrCoeffs = fittedError ;
//       for( int j = 0 ; j < nParams ; ++j )
//       {
// 	 for( int k = j ; k < nParams ; ++k )
// 	 {
// 	    corrCoeffs[ j ][ k ] /=
// 	       sqrt( fittedError[ j ][ j ] * fittedError[ k ][ k ] ) ;
// 	 }

// 	 globalCorrs[ j ] =
// 	    sqrt( 1. - 1./( fittedError[ j ][ j ] *
// 			    fittedErrorInv[ j ][ j ] ) ) ;
//       }

//       cout << "Correlation coefficients with constraints:"
// 	   << corrCoeffs << endl ;
//       cout << "Global correlation coefficients with constraints:"
// 	   << globalCorrs << endl ;
//    }


   // Process TQCA parameters.
   int r2Index = -1 ;
   int rzIndex = -1 ;
   int rwxIndex = -1 ;
   int yIndex = -1 ;
   int x2Index = -1 ;
   int kpiIndex = -1 ;
   int kkIndex = -1 ;
   int pipiIndex = -1 ;
   int kspi0pi0Index = -1 ;
   int kspi0Index = -1 ;
   int ksetaIndex = -1 ;
   int ksomegaIndex = -1 ;
   int klpi0Index = -1 ;

   for( int i = 0 ; i < nParams ; ++i )
   {
      if( fitParameterNames[ i ] == "r2" )
      {
	 r2Index = i ;
      }
      else if( fitParameterNames[ i ] == "rz" )
      {
	 rzIndex = i ;
      }
      else if( fitParameterNames[ i ] == "rwx" )
      {
	 rwxIndex = i ;
      }
      else if( fitParameterNames[ i ] == "y" )
      {
	 yIndex = i ;
      }
      else if( fitParameterNames[ i ] == "x2" )
      {
	 x2Index = i ;
      }
      else if( fitParameterNames[ i ] == "BrD2KPi" )
      {
         kpiIndex = i ;
      }
      else if( fitParameterNames[ i ] == "BrD2K+K-" )
      {
         kkIndex = i ;
      }
      else if( fitParameterNames[ i ] == "BrD2Pi+Pi-" )
      {
         pipiIndex = i ;
      }
      else if( fitParameterNames[ i ] == "BrD2KsPi0Pi0" )
      {
         kspi0pi0Index = i ;
      }
      else if( fitParameterNames[ i ] == "BrD2KsPi0" )
      {
         kspi0Index = i ;
      }
      else if( fitParameterNames[ i ] == "BrD2KsEta" )
      {
         ksetaIndex = i ;
      }
      else if( fitParameterNames[ i ] == "BrD2KsOmega" )
      {
         ksomegaIndex = i ;
      }
      else if( fitParameterNames[ i ] == "BrD2KlPi0" )
      {
         klpi0Index = i ;
      }
   }

   if( r2Index > -1 )
   {
      HDBVariableVector newFitParams( nParams ) ;

      for( int i = 0 ; i < nParams ; ++i )
      {
	 HDBVariableMatrixElement* matrixElement =
	    newFitParams.element( i ) ;

	 matrixElement->setName( fitParameterNames[ i ] ) ;

	 HepVector constants( 1, 1 ) ;

	 HepMatrix powers( 1, nParams, 0 ) ;
	 powers[ 0 ][ i ] = 1. ;

	 if( i == rzIndex ) // rz --> rz/sqrt(r2)/2
	 {
	    constants[ 0 ] = 0.5 ;
	    matrixElement->setName( "r*cosDelta" ) ;
	 }

	 if( i == x2Index )
	 {
	    constants = HepVector( 2 ) ;
	    constants[ 0 ] = 0.5 ;
	    constants[ 1 ] = 0.5 ;

	    powers = HepMatrix( 2, nParams, 0 ) ;
	    powers[ 0 ][ i ] = 1. ;
	    powers[ 1 ][ yIndex ] = 2. ;

	    matrixElement->setName( "RM" ) ;
	 }

         if( i == kpiIndex ) //Br --> Br * ( 1 + y rz/2 + rwx/2 + y^2/2-x^2/2 )
         {
            if( rwxIndex == -1 )
            {
               constants = HepVector( 4, 1 ) ;
               powers = HepMatrix( 4, nParams, 0 ) ;
            }
            else
            {
               constants = HepVector( 5, 1 ) ;
               constants[ 4 ] = 0.5 ;

               powers = HepMatrix( 5, nParams, 0 ) ;
               powers[ 4 ][ i ] = 1. ;
               powers[ 4 ][ rwxIndex ] = 1. ;
            }

            constants[ 0 ] = 1. ;
            constants[ 1 ] = 0.5 ;
            constants[ 2 ] = 0.5 ;
            constants[ 3 ] = -0.5 ;

            powers[ 0 ][ i ] = 1. ;
            powers[ 1 ][ i ] = 1. ;
            powers[ 1 ][ yIndex ] = 1. ;
            powers[ 1 ][ rzIndex ] = 1. ;
            powers[ 2 ][ i ] = 1. ;
            powers[ 2 ][ yIndex ] = 2. ;
            powers[ 3 ][ i ] = 1. ;
            powers[ 3 ][ x2Index ] = 1. ;

            matrixElement->setName( fitParameterNames[ i ] ) ;
         }

         if( i == kkIndex || i == pipiIndex ||
             i == kspi0pi0Index || i == klpi0Index ) // Br --> Br * (1-y)
         {
            constants = HepVector( 2, 1 ) ;
            constants[ 1 ] = -1. ;

            powers = HepMatrix( 2, nParams, 0 ) ;
            powers[ 0 ][ i ] = 1. ;
            powers[ 1 ][ i ] = 1. ;
            powers[ 1 ][ yIndex ] = 1. ;

            matrixElement->setName( fitParameterNames[ i ] ) ;
         }

         if( i == kspi0Index || i == ksetaIndex ||
             i == ksomegaIndex ) // Br --> Br * (1+y)
         {
            constants = HepVector( 2, 1 ) ;

            powers = HepMatrix( 2, nParams, 0 ) ;
            powers[ 0 ][ i ] = 1. ;
            powers[ 1 ][ i ] = 1. ;
            powers[ 1 ][ yIndex ] = 1. ;

            matrixElement->setName( fitParameterNames[ i ] ) ;
         }

	 matrixElement->setConstantVector( constants ) ;
	 matrixElement->setPowerMatrix( powers ) ;
      }

      // Convert error first because it needs the original parameters.
      fittedError = newFitParams.errorMatrix( fittedParams, fittedError ) ;
      fittedParams = newFitParams.values( fittedParams ) ;
      fittedErrorInv = fittedError.inverse( ierr ) ;

      fitParameterNames.clear() ;
      for( int i = 0 ; i < nParams ; ++i )
      {
	 fitParameterNames.push_back( newFitParams.element( i )->name() ) ;
      }

      cout << "New fitted parameters:" << endl ;
      for( int i = 0 ; i < nParams ; ++i )
      {
	 cout << fitParameterNames[ i ]
	      << " = " << fittedParams[ i ] << " +- "
	      << sqrt( fittedError[ i ][ i ] )
	      << " ("
	      << 100. * sqrt( fittedError[ i ][ i ] ) / fittedParams[ i ]
	      << "%)" << endl ;
      }

      cout << endl ;

//       cout << "Errors only:" << endl ;
//       for( int i = 0 ; i < nParams ; ++i )
//       {
// 	 cout << sqrt( fittedError[ i ][ i ] )
// 	      << endl ;
//       }

      cout << "Frac errors only (absolute for y, cosDelta, x*sinDelta):"
	   << endl ;
      for( int i = 0 ; i < nParams ; ++i )
      {
	 if( fitParameterNames[ i ] == "y" ||
	     fitParameterNames[ i ] == "cosDelta" ||
	     fitParameterNames[ i ] == "x * sinDelta" ||
	     fitParameterNames[ i ] == "r*cosDelta" ||
	     fitParameterNames[ i ] == "rwx" )
	 {
	    cout << sqrt( fittedError[ i ][ i ] )
		 << endl ;
	 }
	 else
	 {
	    cout << sqrt( fittedError[ i ][ i ] ) / fabs( fittedParams[ i ] )
		 << endl ;
	 }
      }

      cout << endl ;

      corrCoeffs = fittedError ;
      for( int j = 0 ; j < nParams ; ++j )
      {
	 for( int k = j ; k < nParams ; ++k )
	 {
	    corrCoeffs[ j ][ k ] /=
	       sqrt( fittedError[ j ][ j ] * fittedError[ k ][ k ] ) ;
	 }

	 globalCorrs[ j ] =
	    sqrt( 1. - 1./( fittedError[ j ][ j ] *
			    fittedErrorInv[ j ][ j ] ) ) ;
      }

      cout << "New correlation coefficients:" << corrCoeffs << endl ;
      cout << "New global correlation coefficients:"
	   << globalCorrs << endl ;
   }

//    HepVector statErrors( nParams, 0 ) ;
//    string enterStat ;
//    cout << endl << "Enter statistical errors? (y/n):" << endl ;
//    cin >> enterStat ;
//    if( enterStat == "y" || enterStat == "Y" )
//    {
//       for( int i = 0 ; i < nParams ; ++i )
//       {
// 	 cout << "Enter statistical error for " << fitParameterNames[ i ]
// 	      << endl ;
// 	 cin >> statErrors[ i ] ;
//       }

//       cout << endl << "Statistical and systematic errors:" << endl ;
//       for( int i = 0 ; i < nParams ; ++i )
//       {
// 	 double syst =
// 	    sqrt( fittedError[ i ][ i ] - statErrors[ i ] * statErrors[ i ] ) ;
// 	 cout << fitParameterNames[ i ] << ": "
// 	      << statErrors[ i ]
// 	      << " (" << 100. * statErrors[ i ] / fittedParams[ i ]
// 	      << "%) stat "
// 	      << syst
// 	      << " (" << 100. * syst / fittedParams[ i ]
// 	      << "%) syst" << endl ;
//       }
//    }

   HepVector fracSystErrors( nParams, 0 ) ;
   string enterSyst ;
   cout << endl << "Enter frac systematic errors? (y/n):" << endl ;
   cin >> enterSyst ;
   if( enterSyst == "y" || enterSyst == "Y" )
   {
      for( int i = 0 ; i < nParams ; ++i )
      {
	 cout << "Enter frac systematic error for " << fitParameterNames[ i ]
	      << endl ;
	 cin >> fracSystErrors[ i ] ;
      }

      cout << endl << "Statistical and systematic errors:" << endl ;
      for( int i = 0 ; i < nParams ; ++i )
      {
	 if( fitParameterNames[ i ] == "y" ||
	     fitParameterNames[ i ] == "cosDelta" ||
	     fitParameterNames[ i ] == "x * sinDelta" ||
	     fitParameterNames[ i ] == "r*cosDelta" ||
	     fitParameterNames[ i ] == "rwx" )
	 {
	    double stat = sqrt( fittedError[ i ][ i ] -
				fracSystErrors[ i ] * fracSystErrors[ i ] ) ;
	    cout << fitParameterNames[ i ] << ": "
		 << stat
		 << " (" << 100. * stat / fittedParams[ i ]
		 << "%) stat "
		 << fracSystErrors[ i ]
		 << " (" << 100. * fracSystErrors[ i ] / fittedParams[ i ]
		 << "%) syst" << endl ;
	 }
	 else
	 {
	    double fracTot = sqrt( fittedError[ i ][ i ] ) /
	       fabs( fittedParams[ i ] ) ;
	    double fracStat = sqrt( fracTot * fracTot - 
				    fracSystErrors[ i ]*fracSystErrors[ i ] );
	    cout << fitParameterNames[ i ] << ": "
		 << fracStat * fabs( fittedParams[ i ] )
		 << " (" << 100. * fracStat
		 << "%) stat "
		 << fracSystErrors[ i ] * fabs( fittedParams[ i ] )
		 << " (" << 100. * fracSystErrors[ i ]
		 << "%) syst" << endl ;
	 }
      }
   }

   cout << endl ;

   HepVector resids = aParameterEstimator.residuals() ;

   cout << "Residuals:" << endl ;
   for( int i = 0 ; i < aFactory.numberInputYields() ; ++i )
   {
      double chi = resids[ i ] / aParameterEstimator.residualError( i ) ;

      cout << aFactory.fitPredictions()->element( i )->name() << ": "
	   << resids[ i ] << " +- "
	   << aParameterEstimator.residualError( i ) << ", chi2 = "
	   << chi * chi << endl ;
   }


   // Compute branching fraction ratios.
   string computeRatios ;
   cout << endl ;
//    cout << "Compute ratios of parameters? (y/n):" << endl ;
   cin >> computeRatios ;
   if( computeRatios == "y" || computeRatios == "Y" )
   {
      bool stop = false ;

      do
      {
	 int numer ;
// 	 cout << "Enter numerator index (from 0), -1 to end:"
// 	      << endl ;
	 cin >> numer ;

	 if( numer >= 0 )
	 {
	    int denom ;
// 	    cout << "Enter denominator index (from 0), -1 to end:"
// 		 << endl ;
	    cin >> denom ;

	    if( denom >= 0 )
	    {
	       double ratio = fittedParams[ numer ] / fittedParams[ denom ] ;
	       double error = ratio * sqrt(
		  fittedError[ numer ][ numer ] /
		  fittedParams[ numer ] / fittedParams[ numer ] +
		  fittedError[ denom ][ denom ] /
		  fittedParams[ denom ] / fittedParams[ denom ] -
		  2. * fittedError[ numer ][ denom ] /
		  fittedParams[ numer ] / fittedParams[ denom ] ) ;

	       double ratioCompare ;
// 	       cout << "Enter central value to compare: " << endl ;
	       cin >> ratioCompare ;
	       double errorCompare ;
// 	       cout << "Enter error to compare: " << endl ;
	       cin >> errorCompare ;
	       double diffSigma = ( ratio - ratioCompare ) /
		  sqrt( error * error + errorCompare * errorCompare ) ;

	       string enterRatioStat ;
// 	       cout << "Enter statistical error for ratio? (y/n)" << endl ;
	       cin >> enterRatioStat ;
	       if( enterRatioStat == "y" || enterRatioStat == "Y" )
	       {
		  double stat ;
// 		  cout << "Enter statistical error: " << endl ;
		  cin >> stat ;
		  double syst = sqrt( error * error - stat * stat ) ;

		  cout << fitParameterNames[ numer ] << " / "
		       << fitParameterNames[ denom ] << " = "
		       << ratio << " +- " << stat << " (stat) +- "
		       << syst << " (syst)" << endl
		       << "     " << diffSigma << " sigma from "
		       << ratioCompare << " +- " << errorCompare
		       << endl ;
	       }
	       else
	       {
		  cout << fitParameterNames[ numer ] << " / "
		       << fitParameterNames[ denom ] << " = "
		       << ratio << " +- " << error << endl
		       << "     " << diffSigma << " sigma from "
		       << ratioCompare << " +- " << errorCompare
		       << endl ;
	       }
	    }
	    else
	    {
	       stop = true ;
	    }
	 }
	 else
	 {
	    stop = true ;
	 }
      }
      while( !stop ) ;
   }

   // Compute cross sections.
   string computeXsec ;
   cout << endl ;
   cin >> computeXsec ;
   if( computeXsec == "y" || computeXsec == "Y" )
   {
      int neutralNDDbar ; // starts from 0; -1 = does not exist
      cin >> neutralNDDbar ;
      int chargedNDDbar ;
      cin >> chargedNDDbar ;

      double lumi ;
      cin >> lumi ;
      double dlumi ;
      cin >> dlumi ;
      double lumiErrFracSq = dlumi * dlumi / lumi / lumi ;

      double neutralErrFracSq = 0. ;
      double neutralXsec = 0. ;
      double neutralDXsec = 0. ;
      double neutralSystUncorrFracSq = 0. ;
      if( neutralNDDbar >= 0 )
      {
	 // Uncorrelated fractional systematic error.
	 cin >> neutralSystUncorrFracSq ;
	 neutralSystUncorrFracSq *= neutralSystUncorrFracSq ;

	 neutralErrFracSq = neutralSystUncorrFracSq +
	    fittedError[ neutralNDDbar ][ neutralNDDbar ] /
	    fittedParams[ neutralNDDbar ] / fittedParams[ neutralNDDbar ] ;
	 neutralXsec = fittedParams[ neutralNDDbar ] / lumi ;
	 neutralDXsec = neutralXsec * sqrt( neutralErrFracSq + lumiErrFracSq );

	 string enterXsecStat ;
	 cin >> enterXsecStat ;
	 if( enterXsecStat == "y" || enterXsecStat == "Y" )
	 {
	    double dxsecStat ;
	    cin >> dxsecStat ;
	    cout << "sigma(D0D0bar) = " << neutralXsec << " +- " << dxsecStat
		 << " (stat) +- "
		 << sqrt( neutralDXsec * neutralDXsec - dxsecStat * dxsecStat )
		 << " (syst)" << endl ;
	 }
	 else
	 {
	    cout << "sigma(D0D0bar) = " << neutralXsec << " +- "
		 << neutralDXsec << endl ;
	 }
      }

      double chargedErrFracSq = 0. ;
      double chargedXsec = 0. ;
      double chargedDXsec = 0. ;
      double chargedSystUncorrFracSq = 0. ;
      if( chargedNDDbar >= 0 )
      {
	 // Uncorrelated fractional systematic error.
	 cin >> chargedSystUncorrFracSq ;
	 chargedSystUncorrFracSq *= chargedSystUncorrFracSq ;

	 chargedErrFracSq = chargedSystUncorrFracSq +
	    fittedError[ chargedNDDbar ][ chargedNDDbar ] /
	    fittedParams[ chargedNDDbar ] / fittedParams[ chargedNDDbar ] ;
	 chargedXsec = fittedParams[ chargedNDDbar ] / lumi ;
	 chargedDXsec = chargedXsec * sqrt( chargedErrFracSq + lumiErrFracSq );

	 string enterXsecStat ;
	 cin >> enterXsecStat ;
	 if( enterXsecStat == "y" || enterXsecStat == "Y" )
	 {
	    double dxsecStat ;
	    cin >> dxsecStat ;
	    cout << "sigma(D+D-) = " << chargedXsec << " +- " << dxsecStat
		 << " (stat) +- "
		 << sqrt( chargedDXsec * chargedDXsec - dxsecStat * dxsecStat )
		 << " (syst)" << endl ;
	 }
	 else
	 {
	    cout << "sigma(D+D-) = " << chargedXsec << " +- "
		 << chargedDXsec << endl ;
	 }
      }


      if( neutralNDDbar >= 0 && chargedNDDbar >= 0 )
      {
	 double neutralChargedCovFrac =
	    fittedError[ neutralNDDbar ][ chargedNDDbar ] /
	    fittedParams[ neutralNDDbar ] / fittedParams[ chargedNDDbar ] ;
	 double neutralChargedCov = neutralXsec * chargedXsec *
	    ( neutralChargedCovFrac + lumiErrFracSq ) ;
	 cout << "Correlation coeff between sigma(D0D0bar) and sigma(D+D-): "
	      << neutralChargedCov / neutralDXsec / chargedDXsec << endl ;

	 double sumNDDbar =
	    fittedParams[ neutralNDDbar ] + fittedParams[ chargedNDDbar ] ;
	 double xsecTot = sumNDDbar / lumi ;
	 double dxsecTot = xsecTot *
	    sqrt( lumiErrFracSq +
		  ( neutralSystUncorrFracSq * fittedParams[ neutralNDDbar ] *
		    fittedParams[ neutralNDDbar ] +
		    chargedSystUncorrFracSq * fittedParams[ chargedNDDbar ] *
		    fittedParams[ chargedNDDbar ] +
		    fittedError[ neutralNDDbar ][ neutralNDDbar ] +
		    fittedError[ chargedNDDbar ][ chargedNDDbar ] +
		    2. * fittedError[ neutralNDDbar ][ chargedNDDbar ] ) /
		  sumNDDbar / sumNDDbar ) ;

	 string enterXsecStat ;
	 cin >> enterXsecStat ;
	 if( enterXsecStat == "y" || enterXsecStat == "Y" )
	 {
	    double dxsecStat ;
	    cin >> dxsecStat ;
	    cout << "sigma(DDbar) = " << xsecTot << " +- " << dxsecStat
		 << " (stat) +- "
		 << sqrt( dxsecTot * dxsecTot - dxsecStat * dxsecStat )
		 << " (syst)" << endl ;
	 }
	 else
	 {
	    cout << "sigma(DDbar) = " << xsecTot << " +- "
		 << dxsecTot << endl ;
	 }


	 double chargedNeutralRatio = 
	    fittedParams[ chargedNDDbar ] / fittedParams[ neutralNDDbar ] ;
	 double dratio = chargedNeutralRatio *
	    sqrt( neutralErrFracSq + chargedErrFracSq -
		  2. * neutralChargedCovFrac ) ;

	 string enterRatioStat ;
	 cin >> enterRatioStat ;
	 if( enterRatioStat == "y" || enterRatioStat == "Y" )
	 {
	    double dratioStat ;
	    cin >> dratioStat ;
	    cout << "chg/neu = " << chargedNeutralRatio << " +- " << dratioStat
		 << " (stat) +- "
		 << sqrt( dratio * dratio - dratioStat * dratioStat )
		 << " (syst)" << endl ;
	 }
	 else
	 {
	    cout << "chg/neu = " << chargedNeutralRatio << " +- "
		 << dratio << endl ;
	 }
      }
   }

   cout << endl << endl ;
}


string
itoa( int aInt )
{
   int numberTmp = aInt ;
   int ndigits = 0 ;

   do
   {
      ++ndigits ;
      numberTmp = int( numberTmp / 10 ) ;
   }
   while( numberTmp ) ;

   double power = pow( 10., ndigits-1 ) ;
   string numberString ;
   double numberTmp2 = aInt ;
   for( int i = 0 ; i < ndigits ; ++i )
   {
      int digit = int( numberTmp2 / power ) ;
      numberTmp2 -= digit * power ;
      power /= 10 ;

      if( digit == 0 )
      {
	 numberString += "0" ;
      }
      else if( digit == 1 )
      {
	 numberString += "1" ;
      }
      else if( digit == 2 )
      {
	 numberString += "2" ;
      }
      else if( digit == 3 )
      {
	 numberString += "3" ;
      }
      else if( digit == 4 )
      {
	 numberString += "4" ;
      }
      else if( digit == 5 )
      {
	 numberString += "5" ;
      }
      else if( digit == 6 )
      {
	 numberString += "6" ;
      }
      else if( digit == 7 )
      {
	 numberString += "7" ;
      }
      else if( digit == 8 )
      {
	 numberString += "8" ;
      }
      else if( digit == 9 )
      {
	 numberString += "9" ;
      }
   }

   return numberString ;
}
