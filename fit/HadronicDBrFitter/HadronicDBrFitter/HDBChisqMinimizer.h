#if !defined(HADRONICDBRFITTER_HDBCHISQMINIMIZER_H)
#define HADRONICDBRFITTER_HDBCHISQMINIMIZER_H
// -*- C++ -*-
//
// Package:     <HadronicDBrFitter>
// Module:      HDBChisqMinimizer
// 
/**\class HDBChisqMinimizer HDBChisqMinimizer.h HadronicDBrFitter/HDBChisqMinimizer.h

 Description: <one line class summary>

 Usage:
    <usage>

*/
//
// Author:      Werner Sun
// Created:     Mon Mar 29 22:30:46 EST 2004
// $Id$
//
// Revision history
//
// $Log$

// system include files

// user include files
#include "HadronicDBrFitter/HDBParameterEstimator.h"

// forward declarations

class HDBChisqMinimizer : public HDBParameterEstimator
{
      // ---------- friend classes and functions ---------------

   public:
      // ---------- constants, enums and typedefs --------------

      // ---------- Constructors and destructor ----------------
      HDBChisqMinimizer(
	 HDBInputData* aInputData,
	 HDBInputData* aExternalData,
	 HDBVariableVector* aFitPredictions,
	 HDBVariableVector* aExternalFitPredictions,
	 const HDBData& aSeedParameters ) ;
      HDBChisqMinimizer( HDBFitInputFactory* aFactory ) ;

      virtual ~HDBChisqMinimizer();

      // ---------- member functions ---------------------------
      virtual void estimateParameters( bool aFinalPass = false ) ;

      // ---------- const member functions ---------------------
      double chisq() const { return m_chisq ; }
      int ndof() const { return m_ndof ; }

      // ---------- static member functions --------------------

   protected:
      // ---------- protected member functions -----------------

      // ---------- protected const member functions -----------

   private:
      // ---------- Constructors and destructor ----------------
      HDBChisqMinimizer( const HDBChisqMinimizer& ); // stop default

      // ---------- assignment operator(s) ---------------------
      const HDBChisqMinimizer& operator=( const HDBChisqMinimizer& ); // stop default

      // ---------- private member functions -------------------
      bool solveHouseholder( const HepSymMatrix& aInputErrorInv,
			     const HepVector& aResiduals,
			     const HepMatrix& aResidualDerivatives,
			     HepVector& aSeeds ) const ;

      bool iterateHouseholder( const HepSymMatrix& aOutputErrorInv,
			       const HepSymMatrix& aInputErrorInv,
			       const HepVector& aResiduals,
			       const HepMatrix& aResidualDerivatives,
			       HepVector& aSeeds ) const ;

      // ---------- private const member functions -------------

      // ---------- data members -------------------------------
      double m_chisq ;
      int m_ndof ;

      // ---------- static data members ------------------------

};

// inline function definitions

// Uncomment the following lines, if your class is templated 
// and has an implementation file (in the Template directory)
//#if defined(INCLUDE_TEMPLATE_DEFINITIONS)
//# include "HadronicDBrFitter/Template/HDBChisqMinimizer.cc"
//#endif

#endif /* HADRONICDBRFITTER_HDBCHISQMINIMIZER_H */
