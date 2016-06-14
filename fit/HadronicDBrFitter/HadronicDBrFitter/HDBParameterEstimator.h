#if !defined(HADRONICDBRFITTER_HDBPARAMETERESTIMATOR_H)
#define HADRONICDBRFITTER_HDBPARAMETERESTIMATOR_H
// -*- C++ -*-
//
// Package:     <HadronicDBrFitter>
// Module:      HDBParameterEstimator
// 
/**\class HDBParameterEstimator HDBParameterEstimator.h HadronicDBrFitter/HDBParameterEstimator.h

 Description: <one line class summary>

 Usage:
    <usage>

*/
//
// Author:      Werner Sun
// Created:     Mon Mar 29 22:34:07 EST 2004
// $Id$
//
// Revision history
//
// $Log$

// system include files

// user include files
#include "HadronicDBrFitter/HDBInputData.h"
#include "HadronicDBrFitter/HDBParameterData.h"
#include "HadronicDBrFitter/HDBVariableVector.h"

// forward declarations
class HDBFitInputFactory ;

class HDBParameterEstimator
{
      // ---------- friend classes and functions ---------------

   public:
      // ---------- constants, enums and typedefs --------------
      enum Status { kNotFitted,
		    kFitSuccessful,
		    kFitUnsuccessful } ;

      // ---------- Constructors and destructor ----------------

      HDBParameterEstimator() ;
      HDBParameterEstimator(
	 HDBInputData* aInputData,
	 HDBInputData* aExternalData,
	 HDBVariableVector* aFitPredictions,
	 HDBVariableVector* aExternalFitPredictions,
	 const HDBData& aSeedParameters ) ;
      HDBParameterEstimator( HDBFitInputFactory* aFactory ) ;
      virtual ~HDBParameterEstimator();

      // ---------- member functions ---------------------------
//       virtual void estimateParameters() = 0 ;
      virtual void estimateParameters( bool aFinalPass = false ) = 0 ;

      void setPrintDiagnostics( bool aFlag )
      { m_printDiagnostics = aFlag ; }

      virtual void resetSeeds( HDBFitInputFactory* aFactory ) ;

      // ---------- const member functions ---------------------
      virtual const HDBData& fittedParameters() const
      { return m_fittedParameters ; }

      Status fitStatus() const { return m_fitStatus ; }

      virtual HepVector predictedValues() const ;
      virtual HepVector residuals() const ;
      virtual double residualError( int aMeasIndex ) const ;
      virtual HepMatrix residualDerivatives() const ;

      virtual HepVector predictedExternalValues() const ;
      virtual HepVector externalResiduals() const ;
      virtual double externalResidualError( int aMeasIndex ) const ;
      virtual HepMatrix externalResidualDerivatives() const ;

//       virtual int numberOfExternalParameters() const
//       { return m_externalParameterData->numberOfValues() ; }

//       virtual const HepVector& externalParameters() const
//       { return m_externalParameters ; }

//       virtual const HepSymMatrix& externalErrorInverse() const
//       { return m_externalErrorInverse ; }

//       virtual HepVector externalResiduals() const ;

      // ---------- static member functions --------------------

   protected:
      // ---------- protected member functions -----------------
      HDBInputData* m_inputMeasurements ;
      HDBVariableVector* m_fitPredictions ;
      HDBData m_fittedParameters ;

      // for constraining fit parameters to external measurements.
      HDBInputData* m_externalMeasurements ;
      HDBVariableVector* m_externalFitPredictions ;
//       HepVector m_externalParameters ; // zeros if no external.
//       HepSymMatrix m_externalErrorInverse ; // zeros if no external.

      Status m_fitStatus ;
      bool m_printDiagnostics ;

      // ---------- protected const member functions -----------

   private:
      // ---------- Constructors and destructor ----------------
      HDBParameterEstimator( const HDBParameterEstimator& ); // stop default

      // ---------- assignment operator(s) ---------------------
      const HDBParameterEstimator& operator=( const HDBParameterEstimator& ); // stop default

      // ---------- private member functions -------------------

      // ---------- private const member functions -------------

      // ---------- data members -------------------------------

      // ---------- static data members ------------------------

};

// inline function definitions

// Uncomment the following lines, if your class is templated 
// and has an implementation file (in the Template directory)
//#if defined(INCLUDE_TEMPLATE_DEFINITIONS)
//# include "HadronicDBrFitter/Template/HDBParameterEstimator.cc"
//#endif

#endif /* HADRONICDBRFITTER_HDBPARAMETERESTIMATOR_H */
