#if !defined(HADRONICDBRFITTER_HDBVARIABLEVECTOR_H)
#define HADRONICDBRFITTER_HDBVARIABLEVECTOR_H
// -*- C++ -*-
//
// Package:     <HadronicDBrFitter>
// Module:      HDBVariableVector
// 
/**\class HDBVariableVector HDBVariableVector.h HadronicDBrFitter/HDBVariableVector.h

 Description: Vector (single column) case of HDBVariableMatrix

 Usage:
    <usage>

*/
//
// Author:      Werner Sun
// Created:     Fri May 21 18:05:41 EDT 2004
// $Id$
//
// Revision history
//
// $Log$

// system include files

// user include files
#include "HadronicDBrFitter/HDBVariableMatrix.h"

// forward declarations

class HDBVariableVector : public HDBVariableMatrix
{
      // ---------- friend classes and functions ---------------

   public:
      // ---------- constants, enums and typedefs --------------

      // ---------- Constructors and destructor ----------------
      HDBVariableVector() ;
      HDBVariableVector( int aNumberRows ) ;
      virtual ~HDBVariableVector();

      // ---------- member functions ---------------------------
      HDBVariableMatrixElement* element( int aRow )
      { return HDBVariableMatrix::element( aRow, 0 ) ; }

      // ---------- const member functions ---------------------
      virtual HepVector values( const HepVector& aParameters ) const
      { return HepVector( HDBVariableMatrix::values( aParameters ) ) ; }

      // ---------- static member functions --------------------

   protected:
      // ---------- protected member functions -----------------

      // ---------- protected const member functions -----------

   private:
      // ---------- Constructors and destructor ----------------
      HDBVariableVector( const HDBVariableVector& ); // stop default

      // ---------- assignment operator(s) ---------------------
      // const HDBVariableVector& operator=( const HDBVariableVector& ); // stop default

      // ---------- private member functions -------------------

      // ---------- private const member functions -------------

      // ---------- data members -------------------------------

      // ---------- static data members ------------------------

};

// inline function definitions

// Uncomment the following lines, if your class is templated 
// and has an implementation file (in the Template directory)
//#if defined(INCLUDE_TEMPLATE_DEFINITIONS)
//# include "HadronicDBrFitter/Template/HDBVariableVector.cc"
//#endif

#endif /* HADRONICDBRFITTER_HDBVARIABLEVECTOR_H */
