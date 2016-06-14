#if !defined(HADRONICDBRFITTER_HDBINPUTDATA_H)
#define HADRONICDBRFITTER_HDBINPUTDATA_H
// -*- C++ -*-
//
// Package:     <HadronicDBrFitter>
// Module:      HDBInputData
// 
/**\class HDBInputData HDBInputData.h HadronicDBrFitter/HDBInputData.h

 Description: <one line class summary>

 Usage:
    <usage>

*/
//
// Author:      Werner Sun
// Created:     Mon Mar 29 23:06:03 EST 2004
// $Id$
//
// Revision history
//
// $Log$

// system include files
#include <vector>

// user include files
#include "HadronicDBrFitter/HDBData.h"
#include "HadronicDBrFitter/HDBVariableVector.h"
#include "CLHEP/Matrix/Matrix.h"

// forward declarations

class HDBInputData : public HDBData
{
      // ---------- friend classes and functions ---------------

   public:
      // ---------- constants, enums and typedefs --------------

      // ---------- Constructors and destructor ----------------
      HDBInputData();
      virtual ~HDBInputData();

      // ---------- member functions ---------------------------
      virtual void initialize( const HepVector& aFitParameters,
			       const HDBVariableVector* aFitPredictions ) ;
      virtual void update( const HepVector& aFitParameters,
			   const HDBVariableVector* aFitPredictions,
			   bool aFinalPass = false ) {}

      void setPrintDiagnostics( bool aFlag )
      { m_printDiagnostics = aFlag ; }

      // ---------- const member functions ---------------------
      const HepMatrix& yieldDerivatives() const { return m_yieldDerivatives ; }

      const HepSymMatrix& errorMatrixDerivatives( int aFitParameterIndex )
//      const HepMatrix& errorMatrixDerivatives( int aFitParameterIndex )
	 const { return m_errorMatrixDerivatives[ aFitParameterIndex ] ; }

      // ---------- static member functions --------------------

   protected:

      HepMatrix m_yieldDerivatives ;
      vector< HepSymMatrix > m_errorMatrixDerivatives ;
//      vector< HepMatrix > m_errorMatrixDerivatives ;
      bool m_printDiagnostics ;

      // ---------- protected member functions -----------------

      // ---------- protected const member functions -----------

   private:
      // ---------- Constructors and destructor ----------------
//      HDBInputData( const HDBInputData& ); // stop default

      // ---------- assignment operator(s) ---------------------
      const HDBInputData& operator=( const HDBInputData& ); // stop default

      // ---------- private member functions -------------------

      // ---------- private const member functions -------------

      // ---------- data members -------------------------------

      // ---------- static data members ------------------------

};

// inline function definitions

// Uncomment the following lines, if your class is templated 
// and has an implementation file (in the Template directory)
//#if defined(INCLUDE_TEMPLATE_DEFINITIONS)
//# include "HadronicDBrFitter/Template/HDBInputData.cc"
//#endif

#endif /* HADRONICDBRFITTER_HDBINPUTDATA_H */
