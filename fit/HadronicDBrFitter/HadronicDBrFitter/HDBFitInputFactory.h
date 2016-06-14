#if !defined(HADRONICDBRFITTER_HDBFITINPUTFACTORY_H)
#define HADRONICDBRFITTER_HDBFITINPUTFACTORY_H
// -*- C++ -*-
//
// Package:     <HadronicDBrFitter>
// Module:      HDBFitInputFactory
// 
/**\class HDBFitInputFactory HDBFitInputFactory.h HadronicDBrFitter/HDBFitInputFactory.h

 Description: <one line class summary>

 Usage:
    <usage>

*/
//
// Author:      Werner Sun
// Created:     Wed May 26 21:35:34 EDT 2004
// $Id$
//
// Revision history
//
// $Log$

// system include files

// user include files
#include "HadronicDBrFitter/HDBVariableVector.h"
#include "HadronicDBrFitter/HDBInputData.h"
#include "HadronicDBrFitter/HDBParameterData.h"

// forward declarations

class HDBFitInputFactory
{
      // ---------- friend classes and functions ---------------

   public:
      // ---------- constants, enums and typedefs --------------

      // ---------- Constructors and destructor ----------------
      HDBFitInputFactory();
      virtual ~HDBFitInputFactory();

      // ---------- member functions ---------------------------
      virtual void makeFitPredictions() = 0 ;
      virtual void makeInputData() = 0 ;

      // makes both m_externalFitPredictions and m_externalData
      virtual void makeExternalData() = 0 ;

      virtual void makeSeeds() = 0 ;

      HDBVariableVector* fitPredictions()
      { makeFitPredictions() ; return m_fitPredictions ; }

      HDBInputData* inputData()
      { makeInputData() ; return m_inputData ; }

      int numberInputYields()
      { return fitPredictions()->numberRows() ; }

      HDBVariableVector* externalFitPredictions()
      { makeExternalData() ; return m_externalFitPredictions ; }

      HDBInputData* externalData()
      { makeExternalData() ; return m_externalData ; }

      int numberExternalMeasurements()
      { return externalFitPredictions()->numberRows() ; }

      const HepVector& seedParameters()
      { makeSeeds() ; return m_seedParameters ; }

      int numberFitParameters()
      { return seedParameters().num_row() ; }

      void initializeInputData()
      {
	 inputData()->initialize( seedParameters(),
				  fitPredictions() ) ;
	 externalData()->initialize( seedParameters(),
				     externalFitPredictions() ) ;
      }

      void setPrintDiagnostics( bool aFlag )
      {
	 m_printDiagnostics = aFlag ;
	 inputData()->setPrintDiagnostics( aFlag ) ;
	 externalData()->setPrintDiagnostics( aFlag ) ;
      }

      // ---------- const member functions ---------------------

      // ---------- static member functions --------------------

   protected:
      // ---------- protected member functions -----------------

      // These are pointers so subclasses can be used.
      HDBVariableVector* m_fitPredictions ;
      HDBInputData* m_inputData ;

      HDBVariableVector* m_externalFitPredictions ;
      HDBInputData* m_externalData ;

//       HDBParameterData* m_externalParameterData ;

      HepVector m_seedParameters ;

      bool m_printDiagnostics ;

      // ---------- protected const member functions -----------

   private:
      // ---------- Constructors and destructor ----------------
      HDBFitInputFactory( const HDBFitInputFactory& ); // stop default

      // ---------- assignment operator(s) ---------------------
      const HDBFitInputFactory& operator=( const HDBFitInputFactory& ); // stop default

      // ---------- private member functions -------------------

      // ---------- private const member functions -------------

      // ---------- data members -------------------------------

      // ---------- static data members ------------------------

};

// inline function definitions

// Uncomment the following lines, if your class is templated 
// and has an implementation file (in the Template directory)
//#if defined(INCLUDE_TEMPLATE_DEFINITIONS)
//# include "HadronicDBrFitter/Template/HDBFitInputFactory.cc"
//#endif

#endif /* HADRONICDBRFITTER_HDBFITINPUTFACTORY_H */
