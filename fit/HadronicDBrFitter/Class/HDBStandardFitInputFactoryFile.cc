// -*- C++ -*-
//
// Package:     <HadronicDBrFitter>
// Module:      HDBStandardFitInputFactoryFile
// 
// Description: <one line class summary>
//
// Implementation:
//     <Notes on implementation>
//
// Author:      Werner Sun
// Created:     Wed Dec  1 16:12:06 EST 2004
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
#include <fstream>

// user include files
//#include "Experiment/report.h"
#include "HadronicDBrFitter/HDBStandardFitInputFactoryFile.h"
#include "HadronicDBrFitter/HDBStandardMCInputData.h"

//
// constants, enums and typedefs
//

static const char* const kFacilityString = "HadronicDBrFitter.HDBStandardFitInputFactoryFile" ;

// ---- cvs-based strings (Id and Tag with which file was checked out)
static const char* const kIdString  = "$Id: skeleton.cc,v 1.7 2004/02/12 02:14:38 pcs Exp $";
static const char* const kTagString = "$Name:  $";

//
// static data member definitions
//

//
// constructors and destructor
//
HDBStandardFitInputFactoryFile::HDBStandardFitInputFactoryFile(
   bool aSingleTagsExclusive,
   bool aGenerateMC )
   : HDBStandardFitInputFactory( aSingleTagsExclusive, aGenerateMC )
{
}

// HDBStandardFitInputFactoryFile::HDBStandardFitInputFactoryFile( const HDBStandardFitInputFactoryFile& rhs )
// {
//    // do actual copying here; if you implemented
//    // operator= correctly, you may be able to use just say      
//    *this = rhs;
// }

HDBStandardFitInputFactoryFile::~HDBStandardFitInputFactoryFile()
{
}

//
// assignment operators
//
// const HDBStandardFitInputFactoryFile& HDBStandardFitInputFactoryFile::operator=( const HDBStandardFitInputFactoryFile& rhs )
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
HDBStandardFitInputFactoryFile::readParameterFile( const ifstream& aInput)
{
   // Set up temporary vectors and matrices.

   // Yields and errors
   int nYields = m_fitPredictions->numberRows() ;
   HepVector measuredYields( nYields, 0 ) ;
   HepVector measuredYieldErrors( nYields, 0 ) ;

   int nParams = m_fitParameterNames.size() ;

   int nBkgParams = m_backgroundParameterNames.size() ;
   HepVector backgroundParameters( nBkgParams, 0 ) ;
   HepVector backgroundParameterErrors( nBkgParams, 0 ) ;

   HepMatrix sigEffs( nYields, nYields, 0 ) ;
   HepMatrix sigEffErrors( nYields, nYields, 0 ) ;

   int nBkgs = m_backgroundNames.size() ;
   HepMatrix bkgEffs( nYields, nBkgs, 0 ) ;
   HepMatrix bkgEffErrors( nYields, nBkgs, 0 ) ;

   while( !aInput.eof() )
   {
      char testChar ;
      aInput.get( testChar ) ;
      aInput.putback( testChar ) ;

      if( testChar == '#' )
      {
	 char comment[ 99999 ] ;
	 aInput.getline( comment, 99999 ) ;
	 cout << comment << endl ;
      }
      else
      {
	 string key ;
	 aInput >> key ;
	 cout << "key = " << key << endl ;

	 if( key == 'Yield' && !m_generateMC )
	 {
	    string yieldName ;
	    aInput >> yieldName ;
	    bool yieldFound = false ;

	    for( int i = 0 ; i < nYields && !yieldFound ; ++i )
	    {
	       if( yieldName == m_fitPredictions->element( i )->name() )
	       {
		  yieldFound = true ;

		  double yield ;
		  aInput >> yield ;
		  if( aInput.good() )
		  {
		     measuredYields[ i ] = yield ;
		  }
		  else
		  {
		     cout << "Problem reading yield for "
			  << yieldName << endl ;
		  }

		  double statError, systError ;
		  aInput >> statError >> systError ;
		  if( aInput.good() )
		  {
		     measuredYieldErrors[ i ] = sqrt(
			statError * statError + systError * systError ) ;
		  }
		  else
		  {
		     cout << "Problem reading yield errors for "
			  << yieldName << endl ;
		  }
	       }
	    }

	    if( !yieldFound )
	    {
	       cout << "No yield found with the name " << yieldName << endl ;
	    }
	 }
	 else if( key == 'YieldErrorMC' && m_generateMC )
	 {
	    string yieldName ;
	    aInput >> yieldName ;
	    bool yieldFound = false ;

	    for( int i = 0 ; i < nYields && !yieldFound ; ++i )
	    {
	       if( yieldName == m_fitPredictions->element( i )->name() )
	       {
		  yieldFound = true ;

		  double yieldError ;
		  aInput >> yieldError ;
		  if( aInput.good() )
		  {
		     measuredYieldErrors[ i ] = yieldError ;
		  }
		  else
		  {
		     cout << "Problem reading yield error for "
			  << yieldName << endl ;
		  }
	       }
	    }

	    if( !yieldFound )
	    {
	       cout << "No yield found with the name " << yieldName << endl ;
	    }
	 }
	 else if( key == 'BackgroundParameter' )
	 {
	    string bkgParamName ;
	    aInput >> bkgParamName ;
	    bool bkgParamFound = false ;

	    for( int i = 0 ; i < nBkgs && !bkgParamFound ; ++i )
	    {
	       if( bkgParamName == m_backgroundParameterNames[ i ] )
	       {
		  bkgParamFound = true ;

		  double bkgParam ;
		  aInput >> bkgParam ;
		  if( aInput.good() )
		  {
		     bkgParams[ i ] = bkgParam ;
		  }
		  else
		  {
		     cout << "Problem reading background parameter for "
			  << bkgParamName << endl ;
		  }

		  double bkgParamError ;
		  aInput >> bkgParamError ;
		  if( aInput.good() )
		  {
		     bkgParamErrors[ i ] = bkgParamError;
		  }
		  else
		  {
		     cout << "Problem reading background parameter error for "
			  << bkgParamName << endl ;
		  }
	       }
	    }

	    if( !bkgParamFound )
	    {
	       cout << "No background parameter found with the name "
		    << bkgParamName << endl ;
	    }
	 }
	 else if( key == 'SignalEfficiency' )
	 {
	    string rowName ;
	    aInput >> rowName ;
	    int rowIndex = -1 ;

	    for( int i = 0 ; i < nYields && !rowFound ; ++i )
	    {
	       if( rowName == m_fitPredictions->element( i )->name() )
	       {
		  rowIndex = i ;
	       }
	    }

	    if( rowIndex == -1 )
	    {
	       cout << "No yield found with the name " << rowName << endl ;
	    }

	    string colName ;
	    aInput >> colName ;
	    int colIndex = -1 ;

	    for( int i = 0 ; i < nYields && !colFound ; ++i )
	    {
	       if( colName == m_fitPredictions->element( i )->name() )
	       {
		  colIndex = i ;
	       }
	    }

	    if( colIndex == -1 )
	    {
	       cout << "No yield found with the name " << colName << endl ;
	    }

	    if( rowIndex > -1 && colIndex > -1 )
	    {
	       double eff ;
	       aInput >> eff ;
	       if( aInput.good() )
	       {
		  sigEffs[ rowIndex ][ colIndex ] = eff ;
	       }
	       else
	       {
		  cout << "Problem reading signal efficiency for "
		       << rowName << ", " << colName << endl ;
	       }

	       double effErr ;
	       aInput >> effErr ;
	       if( aInput.good() )
	       {
		  sigEffErrors[ rowIndex ][ colIndex ] = effErr ;
	       }
	       else
	       {
		  cout << "Problem reading signal efficiency error for "
		       << rowName << ", " << colName << endl ;
	       }
	    }
	 }
	 else if( key == 'BackgroundEfficiency' )
	 {
	    string rowName ;
	    aInput >> rowName ;
	    int rowIndex = -1 ;

	    for( int i = 0 ; i < nYields && !rowFound ; ++i )
	    {
	       if( rowName == m_fitPredictions->element( i )->name() )
	       {
		  rowIndex = i ;
	       }
	    }

	    if( rowIndex == -1 )
	    {
	       cout << "No yield found with the name " << rowName << endl ;
	    }

	    string colName ;
	    aInput >> colName ;
	    int colIndex = -1 ;

	    for( int i = 0 ; i < nBkgs && !colFound ; ++i )
	    {
	       if( colName == m_backgroundNames[ i ] )
	       {
		  colIndex = i ;
	       }
	    }

	    if( colIndex == -1 )
	    {
	       cout << "No background found with the name " << colName << endl;
	    }

	    if( rowIndex > -1 && colIndex > -1 )
	    {
	       double eff ;
	       aInput >> eff ;
	       if( aInput.good() )
	       {
		  bkgEffs[ rowIndex ][ colIndex ] = eff ;
	       }
	       else
	       {
		  cout << "Problem reading background efficiency for "
		       << rowName << ", " << colName << endl ;
	       }

	       double effErr ;
	       aInput >> effErr ;
	       if( aInput.good() )
	       {
		  bkgEffErrors[ rowIndex ][ colIndex ] = effErr ;
	       }
	       else
	       {
		  cout << "Problem reading background efficiency error for "
		       << rowName << ", " << colName << endl ;
	       }
	    }
	 }
	 else if( key == 'EfficiencySystematic' )
	 {
	 }
	 else if( ( key == 'SeedParameter' && !m_generateMC ) ||
	    ( key == 'TrueParameter' && m_generateMC ) )
	 {
	    string parameterName ;
	    aInput >> parameterName ;
	    bool parameterFound = false ;

	    for( int i = 0 ; i < nParams && !parameterFound ; ++i )
	    {
	       if( parameterName == m_fitParametersNames[ i ] )
	       {
		  parameterFound = true ;

		  double seedParam ;
		  aInput >> seedParam ;
		  if( aInput.good() )
		  {
		     m_seedParameters[ i ] = seedParam ;
		  }
		  else
		  {
		     cout << "Problem reading "
			  << ( m_generateMC ? "true" : "seed" )
			  << " value for "
			  << parameterName << endl ;
		  }
	       }
	    }

	    if( !parameterFound )
	    {
	       cout << "No parameter found with the name " << parameterName
		    << endl ;
	    }
	 }
	 else
	 {
	    cout << "Unknown key: " << key << ".  Ignoring rest of line."
		 << endl ;
	    char unknown[ 99999 ] ;
	    aInput.getline( unknown, 99999 ) ;
	 }
      }
   }

   if( m_generateMC )
   {
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
   }

   setYieldsAndErrors( measuredYields, measuredYieldErrors ) ;
   m_inputYieldsAndErrorsDefined = true ;

   m_standardInputData->setBackgroundParameters( bkgParams ) ;
   m_standardInputData->setBackgroundParameterErrors(
      backgroundParamErrors ) ;
   m_backgroundsDefined = true ;
}

bool
HDBStandardFitInputFactoryFile::inIgnoreList( const string& aLabel )
{
   vector< string >::const_iterator ignoreItr = m_ignoreList.begin() ;
   vector< string >::const_iterator ignoreEnd = m_ignoreList.end() ;

   for( ; ignoreItr != ignoreEnd ; ++ignoreItr )
   {
      if( aLabel == *ignoreItr )
      {
	 return true ;
      }
   }

   return false ;
}

void
HDBStandardFitInputFactoryFile::makeInputData()
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
HDBStandardFitInputFactoryFile::makeFitPredictions()
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
   string type ;

   // Ask user to enter list of measurements and form an
   // HDBVariableMatrixElement for each one.
   do
   {
      cout << "New mode type (single/double/end): " ;
      cin >> type ;

      int nFitParamsBefore = m_fitParameterNames.size() ;

      if( type == "single" )
      {
         HDBInputInfoHolder inputInfo ;
         HDBVariableMatrixElement matrixElement ;
	 HepVector particleContent ;

         string mode ;
         cout << "Enter mode: " ;
         cin >> mode ;

         bool knownMode = getInputInfo( mode,
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
            HepVector constant( 1 ) ;
            HepMatrix powers( 1, m_fitParameterNames.size(), 0 ) ;

            FitParameterType type = inputInfo.fitParameterType( 0 ) ;

	    if( type == kDUnflavored ||
		type == kDCharged ||
		type == kDNeutral )
	    {
	       constant[ 0 ] = 2. ;
	    }
	    else
	    {
	       constant[ 0 ] = 1. ;
	    }

	    // Remove this block for alternate parametrization.
            if( type == kDplus || type == kDminus || type == kDCharged )
            {
               powers[ 0 ][ m_nDplusDminusIndex ] = 1. ;
            }
            else
            {
               powers[ 0 ][ m_nDzeroDzerobarIndex ] = 1. ;
            }

            powers[ 0 ][ inputInfo.fitParameterNumber( 0 ) ] = 1. ;

            matrixElement.setName( mode ) ;
            matrixElement.setConstantVector( constant ) ;
            matrixElement.setPowerMatrix( powers ) ;
            m_singleTagPredictions.push_back( matrixElement ) ;
	    m_particleContents.push_back( particleContent ) ;
         }
      }
      else if( type == "double" )
      {
         HDBInputInfoHolder inputInfo ;
         HDBVariableMatrixElement matrixElement ;

	 // Get first mode.
         string mode1 ;
         cout << "Enter first mode: " ;
         cin >> mode1 ;

	 HepVector particleContent1 ;
	 HepVector particleContent2 ;
         bool knownMode1 = getInputInfo( mode1,
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
            cout << "Enter second mode: " ;
            cin >> mode2 ;

            bool knownMode2 = getInputInfo( mode2,
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
               HepVector constant( 1 ) ;
               HepMatrix powers( 1, m_fitParameterNames.size(), 0 ) ;

               bool doubleTagValid = true ;
               FitParameterType type1 = inputInfo.fitParameterType( 0 ) ;
               FitParameterType type2 = inputInfo.fitParameterType( 1 ) ;

               if( ( type1==kD0 && ( type2==kD0bar || type2==kDUnflavored ) )||
                   ( type1==kD0bar && ( type2==kD0 || type2==kDUnflavored ) )||
                   ( type2==kDUnflavored && ( type2==kD0 || type2==kD0bar ) ) )
               {
                  constant[ 0 ] = 1. ;

		  powers[ 0 ][ m_nDzeroDzerobarIndex ] = 1. ;
                  powers[ 0 ][ inputInfo.fitParameterNumber( 0 ) ] += 1. ;
                  powers[ 0 ][ inputInfo.fitParameterNumber( 1 ) ] += 1. ;
               }
               else if( ( ( type1 == kDUnflavored || type1 == kDNeutral ) &&
			  ( type2 == kDUnflavored || type2 == kDNeutral ) ) ||
			( type1 == kDCharged && type2 == kDCharged ) )
               {
                  if( inputInfo.fitParameterNumber( 0 ) ==
                      inputInfo.fitParameterNumber( 1 ) )
                  {
                     constant[ 0 ] = 1. ;
                  }
                  else
                  {
                     constant[ 0 ] = 2. ;
                  }

		  if( type1 == kDCharged )
		  {
		     powers[ 0 ][ m_nDplusDminusIndex ] = 1. ;
		  }
		  else
		  {
 		     powers[ 0 ][ m_nDzeroDzerobarIndex ] = 1. ;
		  }
                  powers[ 0 ][ inputInfo.fitParameterNumber( 0 ) ] += 1. ;
                  powers[ 0 ][ inputInfo.fitParameterNumber( 1 ) ] += 1. ;
               }
               else if( ( type1 == kDplus && type2 == kDminus ) ||
                        ( type1 == kDminus && type2 == kDplus ) )
               {
                  constant[ 0 ] = 1. ;
		  powers[ 0 ][ m_nDplusDminusIndex ] = 1. ;
                  powers[ 0 ][ inputInfo.fitParameterNumber( 0 ) ] += 1. ;
                  powers[ 0 ][ inputInfo.fitParameterNumber( 1 ) ] += 1. ;
               }
               else
               {
                  doubleTagValid = false ;
                  cout << "Invalid combination of modes.  Try again." << endl ;

                  // Remove the outputs just added.
                  for( int i = 0 ;
                       i < m_fitParameterNames.size() - nFitParamsBefore ;
                       ++i )
                  {
                     m_fitParameterNames.pop_back() ;
                  }
               }

               if( doubleTagValid )
               {
                  matrixElement.setName( mode1 + "/" + mode2 ) ;
                  matrixElement.setComment1( mode1 ) ;
                  matrixElement.setComment2( mode2 ) ;
                  matrixElement.setConstantVector( constant ) ;
                  matrixElement.setPowerMatrix( powers ) ;
                  m_doubleTagPredictions.push_back( matrixElement ) ;
		  m_particleContents.push_back( particleContent1 +
						particleContent2 ) ;
               }
            }
         }
      }
      else if( type != "end" )
      {
         cout << "Not a recognized type.  Try again." << endl ;
      }
   }
   while( type != "end" ) ;


   // Expand power matrices to dimension = number of outputs; fill extra
   // space with zeroes.
   vector< HDBVariableMatrixElement >::iterator inputItr =
      m_singleTagPredictions.begin() ;
   vector< HDBVariableMatrixElement >::iterator inputEnd =
      m_singleTagPredictions.end() ;

   for( ; inputItr != inputEnd ; ++inputItr )
   {
      inputItr->expandPowerMatrix( m_fitParameterNames.size() ) ;
   }


   inputItr = m_doubleTagPredictions.begin() ;
   inputEnd = m_doubleTagPredictions.end() ;

   for( ; inputItr != inputEnd ; ++inputItr )
   {
      inputItr->expandPowerMatrix( m_fitParameterNames.size() ) ;
   }


   // If there are only single or double tags for a given charge or if
   // no double tag has two corresponding single tag measurements,
   // then there's not enough information to fit for NDDbar.  In this case,
   // remove it from the list.

   if( m_nDplusDminusIndex != -1 )
   {
      // Check if NDDbar needs to be removed.
      int nSingle = 0 ;
      int nDouble = 0 ;
      int nDoubleWithBothSingles = 0 ;

      inputItr = m_singleTagPredictions.begin() ;
      inputEnd = m_singleTagPredictions.end() ;

      for( ; inputItr != inputEnd ; ++inputItr )
      {
	 if( inputItr->powerMatrix()[ 0 ][ m_nDplusDminusIndex ] != 0. )
	 {
	    ++nSingle ;
	 }
      }

      inputItr = m_doubleTagPredictions.begin() ;
      inputEnd = m_doubleTagPredictions.end() ;

      for( ; inputItr != inputEnd ; ++inputItr )
      {
	 const HepMatrix powers = inputItr->powerMatrix() ;

	 if( powers[ 0 ][ m_nDplusDminusIndex ] != 0. )
	 {
	    ++nDouble ;
	 }

	 // Form list of branching fraction indices for this double tag.
	 vector< int > brs ;
	 for( int i = 0 ; i < m_fitParameterNames.size() ; ++i )
	 {
	    if( i != m_nDplusDminusIndex &&
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
	    inputItr->removeParameter( m_nDplusDminusIndex ) ;
	 }

	 inputItr = m_doubleTagPredictions.begin() ;
	 inputEnd = m_doubleTagPredictions.end() ;

	 for( ; inputItr != inputEnd ; ++inputItr )
	 {
	    inputItr->removeParameter( m_nDplusDminusIndex ) ;
	 }

	 // Remove NDDbar from m_fitParameterNames ;
	 vector< string > newFitParameterNames ;
	 for( int i = 0 ; i < m_fitParameterNames.size() ; ++i )
	 {
	    if( i != m_nDplusDminusIndex )
	    {
	       newFitParameterNames.push_back( m_fitParameterNames[ i ] ) ;
	    }
	 }

	 m_fitParameterNames = newFitParameterNames ;

	 // Adjust m_nDzeroDzerobarIndex if necessary.
	 if( m_nDzeroDzerobarIndex > m_nDplusDminusIndex )
	 {
	    --m_nDzeroDzerobarIndex ;
	 }

	 m_nDplusDminusIndex = -1 ;
      }
   }

   if( m_nDzeroDzerobarIndex != -1 )
   {
      // Check if NDDbar needs to be removed.
      int nSingle = 0 ;
      int nDouble = 0 ;
      int nDoubleWithBothSingles = 0 ;

      inputItr = m_singleTagPredictions.begin() ;
      inputEnd = m_singleTagPredictions.end() ;

      for( ; inputItr != inputEnd ; ++inputItr )
      {
	 if( inputItr->powerMatrix()[ 0 ][ m_nDzeroDzerobarIndex ] != 0. )
	 {
	    ++nSingle ;
	 }
      }

      inputItr = m_doubleTagPredictions.begin() ;
      inputEnd = m_doubleTagPredictions.end() ;

      for( ; inputItr != inputEnd ; ++inputItr )
      {
	 const HepMatrix powers = inputItr->powerMatrix() ;

	 if( powers[ 0 ][ m_nDzeroDzerobarIndex ] != 0. )
	 {
	    ++nDouble ;
	 }

	 // Form list of branching fraction indices for this double tag.
	 vector< int > brs ;
	 for( int i = 0 ; i < m_fitParameterNames.size() ; ++i )
	 {
	    if( i != m_nDzeroDzerobarIndex &&
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
	    inputItr->removeParameter( m_nDzeroDzerobarIndex ) ;
	 }

	 inputItr = m_doubleTagPredictions.begin() ;
	 inputEnd = m_doubleTagPredictions.end() ;

	 for( ; inputItr != inputEnd ; ++inputItr )
	 {
	    inputItr->removeParameter( m_nDzeroDzerobarIndex ) ;
	 }

	 // Remove NDDbar from m_fitParameterNames ;
	 vector< string > newFitParameterNames ;
	 for( int i = 0 ; i < m_fitParameterNames.size() ; ++i )
	 {
	    if( i != m_nDzeroDzerobarIndex )
	    {
	       newFitParameterNames.push_back( m_fitParameterNames[ i ] ) ;
	    }
	 }

	 m_fitParameterNames = newFitParameterNames ;

	 m_nDzeroDzerobarIndex = -1 ;
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
	     m_singleTagPredictions[ j ].name() )
         {
            singlePair.first =  j ;
         }

         if( m_doubleTagPredictions[ i ].comment2() ==
	     m_singleTagPredictions[ j ].name() )
         {
            singlePair.second =  j ;
         }
      }

      if( singlePair.first != -1 || singlePair.second != -1 )
      {
	 doubleToSingleCrossReference.push_back( singlePair ) ;
      }
   }

   m_fitPredictions->setParameterNames( m_fitParameterNames ) ;
   m_standardInputData->setDoubleToSingleCrossReference(
      doubleToSingleCrossReference,
      m_singleTagPredictions.size(),
      m_doubleTagPredictions.size() ) ;


   // Report back on outputs and measurements.
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

   m_fitParametersDefined = true ;
}

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

void
HDBStandardFitInputFactoryFile::getBackgrounds()
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
   string type ;

   do
   {
      cout << "Enter background type (neutralD/chargedD/nonD/end): " ;
      cin >> type ;

      if( type == "neutralD" || type == "chargedD" || type == "nonD" )
      {
         HepVector probs( nMeas, 0 ) ;

         if( type == "neutralD" || type == "chargedD" )
         {
	    int nddIndex = type == "chargedD" ?
	       m_nDplusDminusIndex : m_nDzeroDzerobarIndex ;
	    string ddbarType = type == "chargedD" ? "ND+D-" : "ND0D0bar" ;

            string brFracName ;
            cout << "Enter branching fraction name: " ;
            cin >> brFracName ;
            m_backgroundNames.push_back( brFracName ) ;


	    // Add NDDbar to parameter list if not fit parameter.
	    if( nddIndex < 0 )
	    {
	       nddIndex = nFitParameters + backgroundParameterNames.size() ;
	       backgroundParameterNames.push_back( ddbarType ) ;
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
	    }


            // Add term to input definitions.
            HDBVariableMatrixElement element ;
	    element.setName( brFracName ) ;
	    element.setComment1( ddbarType ) ;
	    element.setComment2( brFracName ) ;
	    element.setConstantVector( HepVector( 1, 1 ) ) ;

	    HepMatrix powers(
	       1,
	       nFitParameters + backgroundParameterNames.size(),
	       0 ) ;
	    powers[ 0 ][ nddIndex ] = 1. ;
	    powers[ 0 ][ brFracIndex ] = 1. ;
	    element.setPowerMatrix( powers ) ;

	    backgroundElements.push_back( element ) ;
         }
         else if( type == "nonD" )
         {
            string xsecName ;
            cout << "Enter cross section name: " ;
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
	    }

	    if( !xsecInList )
	    {
	       xsecIndex = nFitParameters + backgroundParameterNames.size() ;
	       backgroundParameterNames.push_back( xsecName ) ;
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
      }
      else if( type != "end" )
      {
         cout << "Not a recognized type.  Try again." << endl ;
      }
   }
   while( type != "end" ) ;


   // Finish up

   cout << endl << endl << "Background parameters:" << endl ;

   HepVector bkgParams( backgroundParameters.size() ) ;
   HepVector bkgParamErrors( backgroundParameters.size() ) ;
   for( int i = 0 ; i < backgroundParameters.size() ; ++i )
   {
      cout << "   " << backgroundParameterNames[ i ]
// 	   << ": " << backgroundParameters[ i ]
// 	   << " +- " << backgroundParameterErrors[ i ]
	   << endl ;

//       bkgParams[ i ] = backgroundParameters[ i ] ;
//       bkgParamErrors[ i ] = backgroundParameterErrors[ i ] ;
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
}

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

void
HDBStandardFitInputFactoryFile::getEfficiencies()
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
      cout << "Enter signal efficiencies for single tag "
	   << m_singleTagPredictions[ i ].name()
           << endl ;

      for( int j = 0 ; j < nSingle ; ++j )
      {
         cout << "   Probability for " << m_singleTagPredictions[ j ].name()
              << " --> " << m_singleTagPredictions[ i ].name()
              << ": " ;
         cin >> sigEffs[ i ][ j ] ;
      }

      if( m_standardInputData->singleTagsExclusive() )
      {
         for( int j = nSingle ; j < nMeas ; ++j )
         {
            cout << "   Probability for "
		 << m_doubleTagPredictions[ j - nSingle ].name()
                 << " --> " << m_singleTagPredictions[ i ].name()
                 << ": " ;
            cin >> sigEffs[ i ][ j ] ;

            // Flip sign of efficiency matrix element.
            sigEffs[ i ][ j ] = -sigEffs[ i ][ j ] ;
         }
      }

      cout << endl ;
   }

   // Double tags.
   for( int i = nSingle ; i < nMeas ; ++i )
   {
      cout << "Enter signal efficiencies for double tag "
	   << m_doubleTagPredictions[ i - nSingle ].name()
           << endl ;

      for( int j = nSingle ; j < nMeas ; ++j )
      {
         cout << "   Probability for "	
      << m_doubleTagPredictions[ j - nSingle ].name()
              << " --> " << m_doubleTagPredictions[ i - nSingle ].name()
              << ": " ;
         cin >> sigEffs[ i ][ j ] ;
      }

      cout << endl ;
   }

   cout << endl ;
   cout << "Signal efficiency matrix: " << sigEffs << endl ;


   // ~~~~~~~~~~~~~~ Background efficiencies ~~~~~~~~~~~~~~~

   int nBkg = m_backgroundNames.size() ;
   HepMatrix bkgEffs( nMeas, nBkg, 0 ) ;

   for( int i = 0 ; i < nMeas ; ++i )
   {
      for( int j = 0 ; j < nBkg ; ++j )
      {
	 cout << "Enter background efficiencies for " << m_backgroundNames[ j ]
	      << " --> " << m_fitPredictions->element( i )->name()
              << ": " ;
         cin >> bkgEffs[ i ][ j ] ;
      }

      cout << endl ;
   }

   cout << endl ;

   if( nBkg > 0 )
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
   //   - uncorrelated
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
      1 + // per D
      1 + // per single tag
      1 ; // per double tag

   HDBEfficiencyMatrix sigEffMatrix( nMeas, nMeas ) ;
   HDBEfficiencyMatrix bkgEffMatrix( nMeas, nBkg ) ;

   for( int i = 0 ; i < nMeas ; ++i )    // row
   {
      HepVector particleContents = m_particleContents[ i ] ;

      // The power matrix has two rows: one for fractional uncertainties
      // and one for absolute uncertainties.
      //
      // constant      powers          parameter       error
      // -----------------------------------------------------------
      //   eff     particle content        1      fractional uncert.
      //    1      uncorrelated            0       absolute uncert.
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
	 for( int k=0 ; k<HDBStandardFitInputFactory::kNumParticleTypes ; ++k )
	 {
	    powers[ 0 ][ nUncorr + k ] = particleContents[ k ] ;
	 }

	 // Uncertainty associated with each fit parameter.
	 const HepMatrix& predPowers =
	    m_fitPredictions->element( j )->powerMatrix() ;
	 for( int k = 0 ; k < nFitParams ; ++k )
	 {
	    powers[ 0 ][ nUncorr +
		       HDBStandardFitInputFactory::kNumParticleTypes + k ] =
	       predPowers[ 0 ][ k ] ;
	 }

	 int counter = nUncorr +
	    HDBStandardFitInputFactory::kNumParticleTypes + nFitParams ;

	 // Uncertainty per D.  Single tags come before double tags.
	 powers[ 0 ][ counter++ ] = j < nSingle ? 1. : 2. ;
	 // Uncertainty per single tag.
	 powers[ 0 ][ counter++ ] = j < nSingle ? 1. : 0. ;
	 // Uncertainty per double tag.
	 powers[ 0 ][ counter++ ] = j < nSingle ? 0. : 1. ;

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
	 for( int k=0 ; k<HDBStandardFitInputFactory::kNumParticleTypes ; ++k )
	 {
	    powers[ 0 ][ nUncorr + k ] = particleContents[ k ] ;
	 }

	 // Parameters for the fit parameters are not needed for the
	 // background efficiency matrix.

	 int counter = nUncorr +
	    HDBStandardFitInputFactory::kNumParticleTypes + nFitParams ;

	 // Uncertainty per D.  Single tags come before double tags.
	 powers[ 0 ][ counter++ ] = j < nSingle ? 1. : 2. ;
	 // Uncertainty per single tag.
	 powers[ 0 ][ counter++ ] = j < nSingle ? 1. : 0. ;
	 // Uncertainty per double tag.
	 powers[ 0 ][ counter++ ] = j < nSingle ? 0. : 1. ;

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
	    cout << "Enter absolute uncertainty on signal efficiency "
		 << m_fitPredictions->element( j )->name()
		 << " --> " << m_fitPredictions->element( i )->name()
		 << ": " ;

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
	 cout << "Enter absolute uncertainty for background efficiency "
	      << m_backgroundNames[ j ]
	      << " --> " << m_fitPredictions->element( i )->name()
	      << ": " ;

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
   cout << "Enter fractional uncertainty for showers: " ;
   cin >> effParamErrors[ effParamNames.size() +
			HDBStandardFitInputFactory::kShower ] ;
   cout << "Enter fractional uncertainty for K0S: " ;
   cin >> effParamErrors[ effParamNames.size() +
			HDBStandardFitInputFactory::kKshort ] ;
   cout << "Enter fractional uncertainty for pi0s: " ;
   cin >> effParamErrors[ effParamNames.size() +
			HDBStandardFitInputFactory::kPi0 ] ;

   cout << "Enter correction factor for tracks: " ;
   cin >> effParams[ effParamNames.size() +
		   HDBStandardFitInputFactory::kTrack ] ;
   cout << "Enter correction factor for charged pions: " ;
   cin >> effParams[ effParamNames.size() +
		   HDBStandardFitInputFactory::kChargedPion ] ;
   cout << "Enter correction factor for charged kaons: " ;
   cin >> effParams[ effParamNames.size() +
		   HDBStandardFitInputFactory::kChargedKaon ] ;
   cout << "Enter correction factor for showers: " ;
   cin >> effParams[ effParamNames.size() +
		   HDBStandardFitInputFactory::kShower ] ;
   cout << "Enter correction factor for K0S: " ;
   cin >> effParams[ effParamNames.size() +
		   HDBStandardFitInputFactory::kKshort ] ;
   cout << "Enter correction factor for pi0s: " ;
   cin >> effParams[ effParamNames.size() +
		   HDBStandardFitInputFactory::kPi0 ] ;

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

   // Per D (row-wise).
   cout << "Enter fractional row-wise uncertainty per D: " ;
   cin >> effParamErrors[ effParamNames.size() ] ;
   effParams[ effParamNames.size() ] = 1. ;
   effParamNames.push_back( "D" ) ;

   // Per single tag (row-wise).
   cout << "Enter fractional row-wise uncertainty per single tag: " ;
   cin >> effParamErrors[ effParamNames.size() ] ;
   effParams[ effParamNames.size() ] = 1. ;
   effParamNames.push_back( "Single tag" ) ;

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
