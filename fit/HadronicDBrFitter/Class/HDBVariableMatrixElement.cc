// -*- C++ -*-
//
// Package:     <HadronicDBrFitter>
// Module:      HDBVariableMatrixElement
// 
// Description: <one line class summary>
//
// Implementation:
//     <Notes on implementation>
//
// Author:      Werner Sun
// Created:     Mon Mar 29 18:21:35 EST 2004
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
#include "HadronicDBrFitter/HDBVariableMatrixElement.h"


//
// constants, enums and typedefs
//

static const char* const kFacilityString = "HadronicDBrFitter.HDBVariableMatrixElement" ;

// ---- cvs-based strings (Id and Tag with which file was checked out)
static const char* const kIdString  = "$Id: skeleton.cc,v 1.6 2001/01/03 16:25:23 cdj Exp $";
static const char* const kTagString = "$Name:  $";

//
// static data member definitions
//

//
// constructors and destructor
//
HDBVariableMatrixElement::HDBVariableMatrixElement()
   : m_constants(),
     m_powers(),
//      m_additiveOffset( 0. ),
     m_uncorrelatedError( 0. )
{
}

// HDBVariableMatrixElement::HDBVariableMatrixElement( const HDBVariableMatrixElement& rhs )
// {
//    // do actual copying here; if you implemented
//    // operator= correctly, you may be able to use just say      
//    *this = rhs;
// }

HDBVariableMatrixElement::~HDBVariableMatrixElement()
{
}

//
// assignment operators
//
// const HDBVariableMatrixElement& HDBVariableMatrixElement::operator=( const HDBVariableMatrixElement& rhs )
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
HDBVariableMatrixElement::expandPowerMatrix( int aNumberColumns )
{
   assert( aNumberColumns >= m_powers.num_col() ) ;

   HepMatrix newPowers( m_powers.num_row(), aNumberColumns, 0 ) ;
   newPowers.sub( 1, 1, m_powers ) ;
   m_powers = newPowers ;
}

void
HDBVariableMatrixElement::removeParameter( int aParameterNumber )
{
   assert( aParameterNumber >= 0 && aParameterNumber < m_powers.num_col() ) ;

   // Remove column from m_powers.
   HepMatrix newPowers( m_powers.num_row(), m_powers.num_col() - 1, 0 ) ;

   int newPowersColumn = 1 ;
   for( int i = 0 ; i < m_powers.num_col() ; ++i )
   {
      if( i != aParameterNumber )
      {
	 newPowers.sub( 1, newPowersColumn,
			m_powers.sub( 1, m_powers.num_row(),
				      i + 1, i + 1 ) ) ;
	 ++newPowersColumn ;
      }
   }

   m_powers = newPowers ;
}

//
// const member functions
//

double
HDBVariableMatrixElement::derivative( int aParameterNumber,
				      const HepVector& aParameterVector ) const
{
   assert( m_powers.num_col() == aParameterVector.num_row() ) ;

   double derivative = 0. ;

   double parameter = aParameterVector[ aParameterNumber ] ;

   // Loop over terms in the definition.
   for( int i = 0 ; i < m_constants.num_row() ; ++i )
   {
      double constantsI = m_constants[ i ] ;
      if( constantsI != 0. )
      {
	 double tmp = 0. ;

	 // Check if this term depends on the given parameter.
	 double power = m_powers[ i ][ aParameterNumber ] ;
	 if( power != 0. )
	 {
	    tmp = constantsI * power * pow( parameter, ( power - 1. ) ) ;

	    // Loop over all other parameters.
	    for( int j = 0 ; j < m_powers.num_col() ; ++j )
	    {
	       if( j != aParameterNumber && m_powers[ i ][ j ] != 0. )
	       {
		  tmp *= pow( aParameterVector[ j ], m_powers[ i ][ j ] ) ;
	       }
	    }
	 }

	 derivative += tmp ;
      }
   }

   return derivative ;
}

HepVector
HDBVariableMatrixElement::derivatives(
   const HepVector& aParameterVector ) const
{
   assert( m_powers.num_col() == aParameterVector.num_row() ) ;

   HepVector tmp( aParameterVector.num_row(), 0 ) ;

   for( int i = 0 ; i < aParameterVector.num_row() ; ++i )
   {
      tmp[ i ] = derivative( i, aParameterVector ) ;
   }

   return tmp ;
}

double
HDBVariableMatrixElement::value( const HepVector& aParameterVector ) const
{
   assert( m_powers.num_col() == aParameterVector.num_row() ) ;

   double pred = 0. ;

   // Loop over terms in the definition.
   for( int i = 0 ; i < m_constants.num_row() ; ++i )
   {
      double tmp = m_constants[ i ] ;

      if( tmp != 0. )
      {
	 // Loop over parameters.
	 for( int j = 0 ; j < m_powers.num_col() ; ++j )
	 {
	    if( m_powers[ i ][ j ] != 0. )
	    {
	       tmp *= pow( aParameterVector[ j ], m_powers[ i ][ j ] ) ;
	    }
	 }

	 pred += tmp ;
      }
   }

//    return pred + m_additiveOffset ;
   return pred ;
}

//
// static member functions
//
