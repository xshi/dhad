// -*- C++ -*-
//
// Package:     <HadronicDBrFitter>
// Module:      HDBEfficiencyMatrix
// 
// Description: <one line class summary>
//
// Implementation:
//     <Notes on implementation>
//
// Author:      Werner Sun
// Created:     Tue Jun  8 23:01:14 EDT 2004
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

// user include files
//#include "Experiment/report.h"
#include "HadronicDBrFitter/HDBEfficiencyMatrix.h"

//
// constants, enums and typedefs
//

static const char* const kFacilityString = "HadronicDBrFitter.HDBEfficiencyMatrix" ;

// ---- cvs-based strings (Id and Tag with which file was checked out)
static const char* const kIdString  = "$Id: skeleton.cc,v 1.7 2004/02/12 02:14:38 pcs Exp $";
static const char* const kTagString = "$Name:  $";

//
// static data member definitions
//

//
// constructors and destructor
//
HDBEfficiencyMatrix::HDBEfficiencyMatrix( int aNumberRows, int aNumberColumns )
   : HDBVariableMatrix( aNumberRows, aNumberColumns )
{
}

// HDBEfficiencyMatrix::HDBEfficiencyMatrix( const HDBEfficiencyMatrix& rhs )
// {
//    // do actual copying here; if you implemented
//    // operator= correctly, you may be able to use just say      
//    *this = rhs;
// }

HDBEfficiencyMatrix::~HDBEfficiencyMatrix()
{
}

//
// assignment operators
//
// const HDBEfficiencyMatrix& HDBEfficiencyMatrix::operator=( const HDBEfficiencyMatrix& rhs )
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

HepSymMatrix
HDBEfficiencyMatrix::errorMatrixNonSingular(
   const HepVector& aParameters,
   const HepVector& aParameterErrors ) const
{
   if( aParameterErrors.num_row() == 0 )
   {
      int nrow = m_numberRows > 0 ? m_numberRows : 1 ;
      int ncol = m_numberColumns > 0 ? m_numberColumns : 1 ;

      return HepSymMatrix( nrow * ncol, 0 ) ;
   }
   else
   {
      // Do multiplication by hand for speed.

      // Form vector of parameter variances.
      HepVector paramVariances( aParameterErrors.num_row(), 0 ) ;

      for( int i = 0 ; i < aParameterErrors.num_row() ; ++i )
      {
         paramVariances[ i ] = aParameterErrors[ i ] * aParameterErrors[ i ] ;
      }

      HepMatrix derivs = derivatives( aParameters ) ;

      int dim = derivs.num_col() ;
      HepSymMatrix errors( dim, 0 ) ;

      for( int i = 0 ; i < dim ; ++i )
      {
         for( int j = i ; j < dim ; ++j )
         {
            // Use temporary variable to speed things up -- avoids accessing
            // matrix element repeatedly.
            double tmp = 0. ;
            for( int k = 0 ; k < aParameterErrors.num_row() ; ++k )
            {
	       // Need better way to find singular piece!
               if( aParameters[ k ] == 0. &&
		   paramVariances[ k ] != 0. &&
                   derivs[ k ][ i ] != 0. &&
                   derivs[ k ][ j ] != 0. )
               {
                  tmp += paramVariances[ k ] *
                     derivs[ k ][ i ] * derivs[ k ][ j ] ;
               }
            }
            errors.fast( j+1, i+1 ) = tmp ;
         }
      }

      return errors ;
   }
}

HepSymMatrix
HDBEfficiencyMatrix::errorMatrixSingular(
   const HepVector& aParameters,
   const HepVector& aParameterErrors ) const
{
   if( aParameterErrors.num_row() == 0 )
   {
      int nrow = m_numberRows > 0 ? m_numberRows : 1 ;
      int ncol = m_numberColumns > 0 ? m_numberColumns : 1 ;

      return HepSymMatrix( nrow * ncol, 0 ) ;
   }
   else
   {
      // Do multiplication by hand for speed.

      // Form vector of parameter variances.
      HepVector paramVariances( aParameterErrors.num_row(), 0 ) ;

      for( int i = 0 ; i < aParameterErrors.num_row() ; ++i )
      {
         paramVariances[ i ] = aParameterErrors[ i ] * aParameterErrors[ i ] ;
      }

      HepMatrix derivs = derivatives( aParameters ) ;

      int dim = derivs.num_col() ;
      HepSymMatrix errors( dim, 0 ) ;

      for( int i = 0 ; i < dim ; ++i )
      {
         for( int j = i ; j < dim ; ++j )
         {
            // Use temporary variable to speed things up -- avoids accessing
            // matrix element repeatedly.
            double tmp = 0. ;
            for( int k = 0 ; k < aParameterErrors.num_row() ; ++k )
            {
	       // Need better way to find singular piece!
               if( aParameters[ k ] != 0. &&
		   paramVariances[ k ] != 0. &&
                   derivs[ k ][ i ] != 0. &&
                   derivs[ k ][ j ] != 0. )
               {
                  tmp += paramVariances[ k ] *
                     derivs[ k ][ i ] * derivs[ k ][ j ] ;
               }
            }
            errors.fast( j+1, i+1 ) = tmp ;
         }
      }

      return errors ;
   }
}

//
// static member functions
//
