#if !defined(HADRONICDBRFITTER_HDBDATA_H)
#define HADRONICDBRFITTER_HDBDATA_H
// -*- C++ -*-
//
// Package:     <HadronicDBrFitter>
// Module:      HDBData
// 
/**\class HDBData HDBData.h HadronicDBrFitter/HDBData.h

 Description: <one line class summary>

 Usage:
    <usage>

*/
//
// Author:      Werner Sun
// Created:     Mon Mar 29 16:42:34 EST 2004
// $Id$
//
// Revision history
//
// $Log$

// system include files

// user include files
#include "CLHEP/Matrix/SymMatrix.h"
#include "CLHEP/Matrix/Vector.h"

// forward declarations

class HDBData
{
      // ---------- friend classes and functions ---------------

   public:
      // ---------- constants, enums and typedefs --------------

      // ---------- Constructors and destructor ----------------
      HDBData();
      HDBData( const HepVector& aValues,
	       const HepSymMatrix& aErrorMatrix ) ; 
      virtual ~HDBData();

      // ---------- member functions ---------------------------
      virtual void clearValuesAndErrorMatrix() ;

      virtual void setValuesAndErrorMatrix(
	 const HepVector& aVector,
	 const HepSymMatrix& aMatrix ) ;

      // ---------- const member functions ---------------------

      double value( int aIndex ) const ;
      const HepVector& values() const { return m_values ; }

      bool hasNullErrorMatrix() const { return m_hasNullErrorMatrix ; }
      const HepSymMatrix& errorMatrix() const ;

      int numberOfValues() const { return m_values.num_row() ; }

      bool errorMatrixOK() const ;

      // ---------- static member functions --------------------

      static bool errorMatrixOK( const HepSymMatrix& aMatrix ) ;

   protected:
      // ---------- protected member functions -----------------
      HepVector m_values ;

      // ---------- protected const member functions -----------

   private:
      // ---------- Constructors and destructor ----------------
//      HDBData( const HDBData& ); // stop default

      // ---------- assignment operator(s) ---------------------
//      const HDBData& operator=( const HDBData& ); // stop default

      // ---------- private member functions -------------------
      static const HepSymMatrix& nullErrorMatrix() ;

      // ---------- private const member functions -------------

      // ---------- data members -------------------------------
      HepSymMatrix m_errorMatrix ;
      bool m_hasNullErrorMatrix ;

      // ---------- static data members ------------------------

};

// inline function definitions

// Uncomment the following lines, if your class is templated 
// and has an implementation file (in the Template directory)
//#if defined(INCLUDE_TEMPLATE_DEFINITIONS)
//# include "HadronicDBrFitter/Template/HDBData.cc"
//#endif

#endif /* HADRONICDBRFITTER_HDBDATA_H */
