// -*- C++ -*-
//
// Package:     <HadronicDBrFitter>
// Module:      HDBData
// 
// Description: <one line class summary>
//
// Implementation:
//     <Notes on implementation>
//
// Author:      Werner Sun
// Created:     Mon Mar 29 16:48:12 EST 2004
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
#include <iostream>
#include <assert.h>

// user include files
//#include "Experiment/report.h"
#include "HadronicDBrFitter/HDBData.h"

using namespace std ;

//
// constants, enums and typedefs
//

static const char* const kFacilityString = "HadronicDBrFitter.HDBData" ;

// ---- cvs-based strings (Id and Tag with which file was checked out)
static const char* const kIdString  = "$Id: skeleton.cc,v 1.6 2001/01/03 16:25:23 cdj Exp $";
static const char* const kTagString = "$Name:  $";

//
// static data member definitions
//

//
// constructors and destructor
//
HDBData::HDBData()
   : m_values(),
     m_errorMatrix(),
     m_hasNullErrorMatrix( true )
{
}

HDBData::HDBData( const HepVector& aVector,
		  const HepSymMatrix& aMatrix )
   : m_values(),
     m_errorMatrix(),
     m_hasNullErrorMatrix( true )
{
   setValuesAndErrorMatrix( aVector, aMatrix ) ;
}

// HDBData::HDBData( const HDBData& rhs )
// {
//    // do actual copying here; if you implemented
//    // operator= correctly, you may be able to use just say      
//    *this = rhs;
// }

HDBData::~HDBData()
{
}

//
// assignment operators
//
// const HDBData& HDBData::operator=( const HDBData& rhs )
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
HDBData::clearValuesAndErrorMatrix()
{
   m_values = HepVector() ;
   m_errorMatrix = HepSymMatrix() ;
   m_hasNullErrorMatrix = true ;
}

void
HDBData::setValuesAndErrorMatrix(
   const HepVector& aValues,
   const HepSymMatrix& aErrorMatrix )
{
   assert( aErrorMatrix.num_row() == aValues.num_row() ) ;

   m_values = aValues ;

   // Check to see if new Matrix is null
   m_hasNullErrorMatrix = true;
   for( unsigned int column = 1 ;
	column <= aErrorMatrix.num_row() ;
	++column )
   {
      for( unsigned int row = column ;
	   row <= aErrorMatrix.num_row() ;
	   ++row )
      {
         if( 0 != aErrorMatrix.fast( row, column ) )
	 {
            m_hasNullErrorMatrix = false;
            break;
         }
      }
   }

   if( !m_hasNullErrorMatrix )
   {
      m_errorMatrix = aErrorMatrix ;
   }
   else
   {
      m_errorMatrix = HepSymMatrix() ;
   }
}

//
// const member functions
//

double
HDBData::value( int aIndex ) const
{
   assert( numberOfValues() > 0 &&
	   aIndex >= 0 && aIndex < numberOfValues() ) ;
   return m_values[ aIndex ] ;
}

const HepSymMatrix&
HDBData::errorMatrix() const
{
   // If the error matrix is null, return filled with zeros.

   if( !hasNullErrorMatrix() && 0 != m_errorMatrix.num_row() )
   {
      return m_errorMatrix ;
   }
   else
   {
      return nullErrorMatrix() ;
   }
}

bool
HDBData::errorMatrixOK() const
{
   if( hasNullErrorMatrix() )
   {
//      return false ;
      return true ;
   }

   return errorMatrixOK( m_errorMatrix ) ;
}

//
// static member functions
//

const HepSymMatrix&
HDBData::nullErrorMatrix()
{
   static const HepSymMatrix null ;
   return null;
}

bool
HDBData::errorMatrixOK( const HepSymMatrix& aMatrix )
{
//    for( int i = 0 ; i < aMatrix.num_row() ; ++i )
//    {
//       if( aMatrix[ i ][ i ] < 0. )
//       {
// 	 cout
//             << "Error matrix diagonal element " << i << " negative." << endl ;
//          return false ;
//       }
//    }

//    for( int j = 0 ; j < aMatrix.num_row() - 1 ; ++j )
//    {
//       for( int k = j + 1 ; k < aMatrix.num_row() ; ++k )
//       {
//          if( aMatrix[ k ][ j ] * aMatrix[ k ][ j ] >
//              aMatrix[ k ][ k ] * aMatrix[ j ][ j ] )
//          {
// 	    cout
//                << "Error matrix element ["
//                << k << "][" << j << "] too large." << endl ;
//             return false ;
//          }
//       }
//    }

   HepSymMatrix tmp( aMatrix.num_row(), 0 ) ;

   for( int i = 0 ; i < aMatrix.num_row() ; ++i )
   {
      for( int j = 0 ; j < i ; ++j )
      {
	 tmp[ j ][ i ] = aMatrix[ i ][ j ] ;

	 for( int n = 0 ; n < j ; ++n )
	 {
	    tmp[ j ][ i ] -= tmp[ n ][ i ] * tmp[ n ][ j ] ;
	 }

	 tmp[ j ][ i ] /= tmp[ j ][ j ] ;
      }

      double dsq = aMatrix[ i ][ i ] ;

      for( int n = 0 ; n < i ; ++n )
      {
	 dsq -= tmp[ n ][ i ] * tmp[ n ][ i ] ;
      }

      if( dsq <= 0. )
      {
	 return false ;
      }

      tmp[ i ][ i ] = sqrt( dsq ) ;
   }

   return true ;
}
