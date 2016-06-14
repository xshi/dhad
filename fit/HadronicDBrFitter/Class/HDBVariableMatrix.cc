// -*- C++ -*-
//
// Package:     <HadronicDBrFitter>
// Module:      HDBVariableMatrix
// 
// Description: <one line class summary>
//
// Implementation:
//     <Notes on implementation>
//
// Author:      Werner Sun
// Created:     Wed May 19 19:13:45 EDT 2004
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
#include "HadronicDBrFitter/HDBVariableMatrix.h"


//
// constants, enums and typedefs
//

static const char* const kFacilityString = "HadronicDBrFitter.HDBVariableMatrix" ;

// ---- cvs-based strings (Id and Tag with which file was checked out)
static const char* const kIdString  = "$Id: skeleton.cc,v 1.6 2001/01/03 16:25:23 cdj Exp $";
static const char* const kTagString = "$Name:  $";

//
// static data member definitions
//

//
// constructors and destructor
//
HDBVariableMatrix::HDBVariableMatrix( int aNumberRows, int aNumberColumns )
{
   m_numberRows = aNumberRows ;
   m_numberColumns = aNumberColumns; 

   if( m_numberRows != 0 && m_numberColumns != 0 )
   {
      m_elements = new ( HDBVariableMatrixElement* )[ m_numberRows ] ;
      for( int i = 0 ; i < m_numberRows ; ++i )
      {
	 m_elements[ i ] = new HDBVariableMatrixElement[ m_numberColumns ] ;
      }
   }
}

// HDBVariableMatrix::HDBVariableMatrix( const HDBVariableMatrix& rhs )
// {
//    // do actual copying here; if you implemented
//    // operator= correctly, you may be able to use just say      
//    *this = rhs;
// }

HDBVariableMatrix::~HDBVariableMatrix()
{
   if( m_numberRows != 0 && m_numberColumns != 0 )
   {
      for( int i = 0 ; i < m_numberRows ; ++i )
      {
	 delete [] m_elements[ i ] ;
      }

      delete m_elements ;
   }
}

//
// assignment operators
//
const HDBVariableMatrix& HDBVariableMatrix::operator=(
   const HDBVariableMatrix& rhs )
{
   if( this != &rhs )
   {
      // First, delete all current elements.
      if( m_numberRows != 0 && m_numberColumns != 0 )
      {
	 for( int i = 0 ; i < m_numberRows ; ++i )
	 {
	    delete [] m_elements[ i ] ;
	 }

	 delete m_elements ;
      }

      // do actual copying here, plus:
      // "SuperClass"::operator=( rhs );
      m_numberRows = rhs.m_numberRows ;
      m_numberColumns = rhs.m_numberColumns ;
      m_parameterNames = rhs.m_parameterNames ;
//       m_fixedParameters = rhs.m_fixedParameters ;

      if( m_numberRows != 0 && m_numberColumns != 0 )
      {
	 // Allocate new matrix.
	 m_elements = new ( HDBVariableMatrixElement* )[ m_numberRows ] ;
	 for( int i = 0 ; i < m_numberRows ; ++i )
	 {
	    m_elements[ i ] = new HDBVariableMatrixElement[ m_numberColumns ] ;
	 }

	 // Copy elements.
	 for( int i = 0 ; i < m_numberRows ; ++i )
	 {
	    for( int j = 0 ; j < m_numberColumns ; ++j )
	    {
	       m_elements[ i ][ j ] = rhs.m_elements[ i ][ j ] ;
	    }
	 }
      }
   }

   return *this;
}

//
// member functions
//

//
// const member functions
//

HepMatrix
HDBVariableMatrix::derivatives( int aParameterIndex,
				const HepVector& aParameters ) const
{
   if( aParameters.num_row() * m_numberRows * m_numberColumns == 0 )
   {
      int nrow = m_numberRows > 0 ? m_numberRows : 1 ;
      int ncol = m_numberColumns > 0 ? m_numberColumns : 1 ;

      return HepMatrix( nrow, ncol, 0 ) ;
   }
   else
   {
      HepMatrix derivs( m_numberRows, m_numberColumns ) ;

      for( int i = 0 ; i < m_numberRows ; ++i )
      {
	 for( int j = 0 ; j < m_numberColumns ; ++j )
	 {
	    derivs[ i ][ j ] =
	       m_elements[ i ][ j ].derivative( aParameterIndex, aParameters );
	 }
      }

      return derivs ;
   }
}

HepMatrix
HDBVariableMatrix::derivatives( const HepVector& aParameters ) const
{
   if( aParameters.num_row() * m_numberRows * m_numberColumns == 0 )
   {
      int npar = aParameters.num_row() > 0 ? aParameters.num_row() : 1 ;
      int nrow = m_numberRows > 0 ? m_numberRows : 1 ;
      int ncol = m_numberColumns > 0 ? m_numberColumns : 1 ;

      return HepMatrix( npar, nrow * ncol, 0 ) ;
   }
   else
   {
      HepMatrix derivs( aParameters.num_row(),
			m_numberRows * m_numberColumns ) ;

      for( int i = 0 ; i < m_numberRows ; ++i )
      {
	 for( int j = 0 ; j < m_numberColumns ; ++j )
	 {
	    int elementNumber = i * m_numberColumns + j ;

	    derivs.sub( 1, elementNumber + 1,
			m_elements[ i ][ j ].derivatives( aParameters ) ) ;
	 }
      }

//       // Remove fixed parameters: 1 = fixed, 0 = not fixed.
//       if( m_fixedParameters.num_row() == aParameters.num_row() )
//       {
// 	 // Count number of fixed parameters.
// 	 int nFree = 0 ;
// 	 for( int i = 0 ; i < m_fixedParameters.num_row() ; ++i )
// 	 {
// 	    if( m_fixedParameters[ i ] == 0. )
// 	    {
// 	       ++nFree ;
// 	    }
// 	 }

// 	 // Form new matrix with fixed rows removed.
// 	 if( nFree < aParameters.num_row() )
// 	 {
// 	    HepMatrix fixedDerivs( nFree,
// 				   m_numberRows * m_numberColumns ) ;

// 	    int fixedDerivIndex = 0 ;
// 	    for( int i = 0 ; i < m_fixedParameters.num_row() ; ++i )
// 	    {
// 	       if( m_fixedParameters[ i ] == 0. )
// 	       {
// 		  for( int j = 0 ; j < derivs.num_col() ; ++j )
// 		  {
// 		     fixedDerivs[ fixedDerivIndex ][ j ] = derivs[ i ][ j ] ;
// 		  }

// 		  ++fixedDerivIndex ;
// 	       }
// 	    }

// 	    return fixedDerivs ;
// 	 }
//       }

      return derivs ;
   }
}

HepSymMatrix
HDBVariableMatrix::uncorrelatedErrorMatrix() const
{
   // If one or more dimension is zero, make matrix of zeroes.
   if( m_numberRows * m_numberColumns == 0 )
   {
      int nrow = m_numberRows > 0 ? m_numberRows : 1 ;
      int ncol = m_numberColumns > 0 ? m_numberColumns : 1 ;

      return HepSymMatrix( nrow * ncol, 0 ) ;
   }
   else
   {
      HepSymMatrix uncorrError( m_numberRows * m_numberColumns, 0 ) ;

      for( int i = 0 ; i < m_numberRows ; ++i )
      {
	 for( int j = 0 ; j < m_numberColumns ; ++j )
	 {
	    int elementNumber = i * m_numberColumns + j ;

	    double err = m_elements[ i ][ j ].uncorrelatedError() ;
	    uncorrError[ elementNumber ][ elementNumber ] = err * err ;
	 }
      }

      return uncorrError ;
   }
}

HepMatrix
HDBVariableMatrix::values( const HepVector& aParameters ) const
{
   // If one or more dimension is zero, make matrix of zeroes.
   if( m_numberRows * m_numberColumns == 0 )
   {
      int nrow = m_numberRows > 0 ? m_numberRows : 1 ;
      int ncol = m_numberColumns > 0 ? m_numberColumns : 1 ;

      return HepMatrix( nrow, ncol, 0 ) ;
   }
   else
   {
      HepMatrix vals( m_numberRows, m_numberColumns ) ;

      for( int i = 0 ; i < m_numberRows ; ++i )
      {
	 for( int j = 0 ; j < m_numberColumns ; ++j )
	 {
	    vals[ i ][ j ] = m_elements[ i ][ j ].value( aParameters ) ;
	 }
      }

      return vals ;
   }
}
   
HepSymMatrix
HDBVariableMatrix::errorMatrix(
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
	       double paramVariancesK = paramVariances[ k ] ;
	       double derivsKI = derivs[ k ][ i ] ;
	       double derivsKJ = derivs[ k ][ j ] ;

	       if( paramVariancesK != 0. &&
		   derivsKI != 0. &&
		   derivsKJ != 0. )
	       {
		  tmp += paramVariancesK * derivsKI * derivsKJ ;
	       }
	    }
	    errors.fast( j + 1, i + 1 ) = tmp ;
	 }
      }

      // Add uncorrelated errors to diagonal elements.
      errors += uncorrelatedErrorMatrix() ;

      return errors ;
   }
}

HepSymMatrix
HDBVariableMatrix::errorMatrix(
   const HepVector& aParameters,
   const HepSymMatrix& aParameterErrorMatrix ) const
{
   if( aParameterErrorMatrix.num_row() == 0 )
   {
      int nrow = m_numberRows > 0 ? m_numberRows : 1 ;
      int ncol = m_numberColumns > 0 ? m_numberColumns : 1 ;

      return HepSymMatrix( nrow * ncol, 0 ) ;
   }
   else
   {
      return
	 ( aParameterErrorMatrix.similarityT( derivatives( aParameters ) ) +
	   uncorrelatedErrorMatrix() ) ;
   }
}

HepMatrix
HDBVariableMatrix::correlationMatrix(
   const HepVector& aParameters,
   const HepVector& aParameterErrors,
   const HDBVariableMatrix& aOtherMatrix ) const
{
   if( aParameterErrors.num_row() == 0 )
   {
      int nrow = ( m_numberRows > 0 ? m_numberRows : 1 ) *
	 ( m_numberColumns > 0 ? m_numberColumns : 1 ) ;

      int ncol = ( aOtherMatrix.numberRows() > 0 ? m_numberRows : 1 ) *
	 ( aOtherMatrix.numberColumns() > 0 ? m_numberColumns : 1 ) ;

      return HepMatrix( nrow, ncol, 0 ) ;
   }
   else
   {
      // Form diagonal matrix of parameter errors.
      HepVector paramVariances( aParameterErrors.num_row(), 0 ) ;

      for( int i = 0 ; i < aParameterErrors.num_row() ; ++i )
      {
	 paramVariances[ i ] = aParameterErrors[ i ] * aParameterErrors[ i ];
      }

      HepMatrix derivsThis = derivatives( aParameters ) ;
      HepMatrix derivsOther = aOtherMatrix.derivatives( aParameters ) ;

      int nrow = derivsThis.num_col() ;
      int ncol = derivsOther.num_col() ;
      HepMatrix corrs( nrow, ncol, 0 ) ;

      for( int i = 0 ; i < nrow ; ++i )
      {
	 for( int j = 0 ; j < ncol ; ++j )
	 {
	    // Use temporary variable to speed things up -- avoids accessing
	    // matrix element repeatedly.
	    double tmp = 0. ;
	    for( int k = 0 ; k < aParameterErrors.num_row() ; ++k )
	    {
	       double paramVariancesK = paramVariances[ k ] ;
	       double derivsThisKI = derivsThis[ k ][ i ] ;
	       double derivsOtherKJ = derivsOther[ k ][ j ] ;

	       if( paramVariancesK != 0. &&
		   derivsThisKI != 0. &&
		   derivsOtherKJ != 0. )
	       {
		  tmp += paramVariancesK * derivsThisKI * derivsOtherKJ ;
	       }
	    }
	    corrs[ i ][ j ] = tmp ;
	 }
      }

      return corrs ;
   }
}

HepMatrix
HDBVariableMatrix::correlationMatrix(
   const HepVector& aParameters,
   const HepSymMatrix& aParameterErrorMatrix,
   const HDBVariableMatrix& aOtherMatrix ) const
{
   if( aParameterErrorMatrix.num_row() == 0 )
   {
      int nrow = ( m_numberRows > 0 ? m_numberRows : 1 ) *
	 ( m_numberColumns > 0 ? m_numberColumns : 1 ) ;

      int ncol = ( aOtherMatrix.numberRows() > 0 ? m_numberRows : 1 ) *
	 ( aOtherMatrix.numberColumns() > 0 ? m_numberColumns : 1 ) ;

      return HepMatrix( nrow, ncol, 0 ) ;
   }
   else
   {
      return
	 derivatives( aParameters ).T() *
	 aParameterErrorMatrix *
	 aOtherMatrix.derivatives( aParameters ) ;
   }
}

//
// static member functions
//
