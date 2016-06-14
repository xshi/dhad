#if !defined(HADRONICDBRFITTER_HDBFITITERATOR_H)
#define HADRONICDBRFITTER_HDBFITITERATOR_H
// -*- C++ -*-
//
// Package:     <HadronicDBrFitter>
// Module:      HDBFitIterator
// 
/**\class HDBFitIterator HDBFitIterator.h HadronicDBrFitter/HDBFitIterator.h

 Description: <one line class summary>

 Usage:
    <usage>

*/
//
// Author:      Werner Sun
// Created:     Mon Mar 29 22:35:17 EST 2004
// $Id$
//
// Revision history
//
// $Log$

// system include files

// user include files
#include "HadronicDBrFitter/HDBParameterEstimator.h"

// forward declarations

class HDBFitIterator : public HDBParameterEstimator
{
      // ---------- friend classes and functions ---------------

   public:
      // ---------- constants, enums and typedefs --------------

      // ---------- Constructors and destructor ----------------

      HDBFitIterator( HDBParameterEstimator* aParameterEstimator,
		      int aMaxIterations,
		      bool aExecuteFinalPass = false );
      virtual ~HDBFitIterator();

      // ---------- member functions ---------------------------

      // aFinalPass is ignored in HDBFitIterator classes.
      virtual void estimateParameters( bool aFinalPass = false ) ;
      virtual bool convergenceCriterionMet() = 0 ;

      virtual void resetSeeds( HDBFitInputFactory* aFactory )
      { m_parameterEstimator->resetSeeds( aFactory ) ; }

      virtual void saveFitResultsBeforeFinalPass()
      {	m_fittedParametersBeforeFinalPass = fittedParameters() ; }
      virtual void saveFitResultsBeforeFinalPass2()
      {	m_fittedParametersBeforeFinalPass2 = fittedParameters() ; }

      // ---------- const member functions ---------------------
      virtual const HDBData& fittedParameters() const
      { return m_parameterEstimator->fittedParameters() ; }
      virtual const HDBData& fittedParametersBeforeFinalPass() const
      { return m_fittedParametersBeforeFinalPass ; }
      virtual const HDBData& fittedParametersBeforeFinalPass2() const
      { return m_fittedParametersBeforeFinalPass2 ; }

      virtual HepVector predictedValues() const
      { return m_parameterEstimator->predictedValues() ; }

      virtual HepVector residuals() const
      { return m_parameterEstimator->residuals() ; }
      virtual double residualError( int aMeasIndex ) const
      { return m_parameterEstimator->residualError( aMeasIndex ) ; }

      virtual HepMatrix residualDerivatives() const
      { return m_parameterEstimator->residualDerivatives() ; }

      int numberOfIterations() const { return m_numberIterations ; }

      // ---------- static member functions --------------------

   protected:
      // ---------- protected member functions -----------------
      HDBParameterEstimator* m_parameterEstimator ;
      int m_numberIterations ;
      int m_maxIterations ;
      bool m_executeFinalPass ;

      HDBData m_fittedParametersBeforeFinalPass ;
      HDBData m_fittedParametersBeforeFinalPass2 ;

      // ---------- protected const member functions -----------

   private:
      // ---------- Constructors and destructor ----------------
      HDBFitIterator( const HDBFitIterator& ); // stop default

      // ---------- assignment operator(s) ---------------------
      const HDBFitIterator& operator=( const HDBFitIterator& ); // stop default

      // ---------- private member functions -------------------

      // ---------- private const member functions -------------

      // ---------- data members -------------------------------

      // ---------- static data members ------------------------

};

// inline function definitions

// Uncomment the following lines, if your class is templated 
// and has an implementation file (in the Template directory)
//#if defined(INCLUDE_TEMPLATE_DEFINITIONS)
//# include "HadronicDBrFitter/Template/HDBFitIterator.cc"
//#endif

#endif /* HADRONICDBRFITTER_HDBFITITERATOR_H */
