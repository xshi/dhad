#if !defined(HADRONICDBRFITTER_HDBVARIABLEMATRIX_H)
#define HADRONICDBRFITTER_HDBVARIABLEMATRIX_H
// -*- C++ -*-
//
// Package:     <HadronicDBrFitter>
// Module:      HDBVariableMatrix
// 
/**\class HDBVariableMatrix HDBVariableMatrix.h HadronicDBrFitter/HDBVariableMatrix.h

 Description: <one line class summary>

 Usage:
    <usage>

*/
//
// Author:      Werner Sun
// Created:     Wed May 19 17:50:16 EDT 2004
// $Id$
//
// Revision history
//
// $Log$

// system include files
#include <vector>

// user include files
#include "HadronicDBrFitter/HDBVariableMatrixElement.h"
#include "CLHEP/Matrix/SymMatrix.h"

// forward declarations
class HDBVariableMatrixElement ;

class HDBVariableMatrix
{
      // ---------- friend classes and functions ---------------

   public:
      // ---------- constants, enums and typedefs --------------

      // ---------- Constructors and destructor ----------------
      HDBVariableMatrix( int aNumberRows = 0, int aNumberColumns = 0 );
      virtual ~HDBVariableMatrix();

      const HDBVariableMatrix& operator=( const HDBVariableMatrix& );

      // ---------- member functions ---------------------------
      HDBVariableMatrixElement* element( int aRow, int aColumn )
      { return &( m_elements[ aRow ][ aColumn ] ) ; }

      void setParameterNames( const vector< string >& aNames )
      { m_parameterNames = aNames ; }

      // ---------- const member functions ---------------------
      int numberRows() const { return m_numberRows ; }
      int numberColumns() const { return m_numberColumns ; }
      const vector< string >& parameterNames() const
      { return m_parameterNames ; }

      // Derivatives of matrix elements wrt a given parameter (row vector).
      HepMatrix derivatives( int aParameterIndex,
			     const HepVector& aParameters ) const ;

      // Derivatives of matrix elements wrt parameters.
      // # rows = # parameters, # columns = # matrix elements
      HepMatrix derivatives( const HepVector& aParameters ) const ;

      // Evaluate matrix elements using given parameters.
      HepMatrix values( const HepVector& aParameters ) const ;

      // Form matrix with uncorrelated variances of elements.
      HepSymMatrix uncorrelatedErrorMatrix() const ;

      // Variance matrix of elements, with dimension = # rows * # columns.
      // The two dimensions of the value matrix are mapped onto one dimension
      // of the variance matrix.
      HepSymMatrix errorMatrix(
	 const HepVector& aParameters,
	 const HepVector& aParameterErrors ) const ; // errors NOT variances

      // Use this function if the parameters are not independent.
      HepSymMatrix errorMatrix(
	 const HepVector& aParameters,
	 const HepSymMatrix& aParameterErrorMatrix ) const ;

      // # rows = # elements in this matrix
      // # cols = # elements in other matrix
      HepMatrix correlationMatrix(
	 const HepVector& aParameters,
	 const HepVector& aParameterErrors,  // errors NOT variances
	 const HDBVariableMatrix& aOtherMatrix ) const ;

      // Use this function of the parameters are not independent.
      HepMatrix correlationMatrix(
	 const HepVector& aParameters,
	 const HepSymMatrix& aParameterErrorMatrix,
	 const HDBVariableMatrix& aOtherMatrix ) const ;

      // ---------- static member functions --------------------

   protected:
      int m_numberRows ;
      int m_numberColumns ;
      HDBVariableMatrixElement** m_elements ;
      vector< string > m_parameterNames ;

      // ---------- protected member functions -----------------

      // ---------- protected const member functions -----------

   private:
      // ---------- Constructors and destructor ----------------
      HDBVariableMatrix( const HDBVariableMatrix& ); // stop default

      // ---------- assignment operator(s) ---------------------
      // const HDBVariableMatrix& operator=( const HDBVariableMatrix& ); // stop default

      // ---------- private member functions -------------------

      // ---------- private const member functions -------------

      // ---------- data members -------------------------------

      // ---------- static data members ------------------------

};

// inline function definitions

// Uncomment the following lines, if your class is templated 
// and has an implementation file (in the Template directory)
//#if defined(INCLUDE_TEMPLATE_DEFINITIONS)
//# include "HadronicDBrFitter/Template/HDBVariableMatrix.cc"
//#endif

#endif /* HADRONICDBRFITTER_HDBVARIABLEMATRIX_H */
