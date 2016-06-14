// -*- C++ -*-
//
// Package:     <HadronicDBrFitter>
// Module:      HDBParameterData
// 
// Description: <one line class summary>
//
// Implementation:
//     <Notes on implementation>
//
// Author:      Werner Sun
// Created:     Thu Jan 19 15:43:11 EST 2006
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
#include "HadronicDBrFitter/HDBParameterData.h"


//
// constants, enums and typedefs
//

static const char* const kFacilityString = "HadronicDBrFitter.HDBParameterData" ;

// ---- cvs-based strings (Id and Tag with which file was checked out)
static const char* const kIdString  = "$Id: skeleton.cc,v 1.7 2004/02/12 02:14:38 pcs Exp $";
static const char* const kTagString = "$Name:  $";

//
// static data member definitions
//

//
// constructors and destructor
//
HDBParameterData::HDBParameterData()
   : HDBData(),
     m_errorInverse(),
     m_parameterNames()
{
}

HDBParameterData::HDBParameterData( const HepVector& aValues,
				    const HepSymMatrix& aErrorMatrix,
				    const vector< string >& aParameterNames )
{
   setValuesAndErrorMatrix( aValues, aErrorMatrix, aParameterNames ) ;
}

// HDBParameterData::HDBParameterData( const HDBParameterData& rhs )
// {
//    // do actual copying here; if you implemented
//    // operator= correctly, you may be able to use just say      
//    *this = rhs;
// }

HDBParameterData::~HDBParameterData()
{
}

//
// assignment operators
//
// const HDBParameterData& HDBParameterData::operator=( const HDBParameterData& rhs )
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
HDBParameterData::clearValuesAndErrorMatrix()
{
   HDBData::clearValuesAndErrorMatrix() ;

   m_errorInverse = HepSymMatrix() ;
   m_parameterNames.clear() ;
}

void
HDBParameterData::setValuesAndErrorMatrix(
   const HepVector& aValues,
   const HepSymMatrix& aErrorMatrix,
   const vector< string >& aParameterNames )
{
   HDBData::setValuesAndErrorMatrix( aValues, aErrorMatrix ) ;
   m_parameterNames = aParameterNames ;

   assert( m_parameterNames.size() == aValues.num_row() ) ;

   int ierr = 0 ;

   if( !hasNullErrorMatrix() )
   {
      m_errorInverse = errorMatrix().inverse( ierr ) ;
   }

   if( ierr != 0 )
   {
      cout << "HDBParameterData: Unable to invert error matrix!" << endl ;
      m_errorInverse = HepSymMatrix() ;
   }
}

//
// const member functions
//

void
HDBParameterData::expandedValuesAndErrorInverse(
   const vector< string >& aFitParameterNames,
   HepVector& aValuesToFill,
   HepSymMatrix& aErrorInverseToFill ) const
{
   int nData = m_parameterNames.size() ;
   int nParams = aFitParameterNames.size() ;

   assert( nParams >= nData ) ;

   aValuesToFill = HepVector( nParams, 0 ) ;
   aErrorInverseToFill = HepSymMatrix( nParams, 0 ) ;

   if( nData == 0 )
   {
      return ;
   }

   // The map gives the parameter index for each datum.
   int map[ nData ] ;
   for( int i = 0 ; i < nData ; ++i )
   {
      map[ i ] = -1 ;

      for( int j = 0 ; j < nParams ; ++j )
      {
	 if( m_parameterNames[ i ] == aFitParameterNames[ j ] )
	 {
	    map[ i ] = j ;
	    break ;
	 }
      }

      assert( map[ i ] != -1 ) ;
   }


   for( int i = 0 ; i < nData ; ++i )
   {
      int index0 = map[ i ] ;
      aValuesToFill[ index0 ] = value( i ) ;

      for( int j = i ; j < nData ; ++j )
      {
         int index1 = map[ j ] ;
         aErrorInverseToFill[ index0 ][ index1 ] = m_errorInverse[ i ][ j ] ;
      }
   }

   return ;
}

//
// static member functions
//
