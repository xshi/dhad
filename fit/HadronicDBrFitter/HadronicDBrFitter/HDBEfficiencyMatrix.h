#if !defined(HADRONICDBRFITTER_HDBEFFICIENCYMATRIX_H)
#define HADRONICDBRFITTER_HDBEFFICIENCYMATRIX_H
// -*- C++ -*-
//
// Package:     <HadronicDBrFitter>
// Module:      HDBEfficiencyMatrix
// 
/**\class HDBEfficiencyMatrix HDBEfficiencyMatrix.h HadronicDBrFitter/HDBEfficiencyMatrix.h

 Description: <one line class summary>

 Usage:
    <usage>

*/
//
// Author:      Werner Sun
// Created:     Tue Jun  8 22:59:23 EDT 2004
// $Id$
//
// Revision history
//
// $Log$

// system include files

// user include files
#include "HadronicDBrFitter/HDBVariableMatrix.h"

// forward declarations

class HDBEfficiencyMatrix : public HDBVariableMatrix
{
      // ---------- friend classes and functions ---------------

   public:
      // ---------- constants, enums and typedefs --------------

      // ---------- Constructors and destructor ----------------
      HDBEfficiencyMatrix( int aNumberRows = 0, int aNumberColumns = 0 );
      virtual ~HDBEfficiencyMatrix();

      // const HDBEfficiencyMatrix& operator=( const HDBEfficiencyMatrix& );

      // ---------- member functions ---------------------------
      // Variance matrix of elements, with dimension = # rows * # columns.
      // The two dimensions of the value matrix are mapped onto one dimension
      // of the variance matrix.

      // Only parameters with values of 0 are used.
      HepSymMatrix errorMatrixNonSingular(
         const HepVector& aParameters,
         const HepVector& aParameterErrors ) const ; // errors NOT variances

      // Only parameters with values of 1 are used.
      HepSymMatrix errorMatrixSingular(
         const HepVector& aParameters,
         const HepVector& aParameterErrors ) const ; // errors NOT variances

      // The sum of errorMatrixNonSingular() and errorMatrixSingular()
      // is errorMatrix().


      // ---------- const member functions ---------------------

      // ---------- static member functions --------------------

   protected:
      // ---------- protected member functions -----------------

      // ---------- protected const member functions -----------

   private:
      // ---------- Constructors and destructor ----------------
      HDBEfficiencyMatrix( const HDBEfficiencyMatrix& ); // stop default

      // ---------- assignment operator(s) ---------------------
      // const HDBEfficiencyMatrix& operator=( const HDBEfficiencyMatrix& ); // stop default

      // ---------- private member functions -------------------

      // ---------- private const member functions -------------

      // ---------- data members -------------------------------

      // ---------- static data members ------------------------

};

// inline function definitions

// Uncomment the following lines, if your class is templated 
// and has an implementation file (in the Template directory)
//#if defined(INCLUDE_TEMPLATE_DEFINITIONS)
//# include "HadronicDBrFitter/Template/HDBEfficiencyMatrix.cc"
//#endif

#endif /* HADRONICDBRFITTER_HDBEFFICIENCYMATRIX_H */
