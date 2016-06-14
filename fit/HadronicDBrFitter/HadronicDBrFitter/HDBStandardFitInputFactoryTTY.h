#if !defined(HADRONICDBRFITTER_HDBSTANDARDFITINPUTFACTORYTTY_H)
#define HADRONICDBRFITTER_HDBSTANDARDFITINPUTFACTORYTTY_H
// -*- C++ -*-
//
// Package:     <HadronicDBrFitter>
// Module:      HDBStandardFitInputFactoryTTY
// 
/**\class HDBStandardFitInputFactoryTTY HDBStandardFitInputFactoryTTY.h HadronicDBrFitter/HDBStandardFitInputFactoryTTY.h

 Description: <one line class summary>

 Usage:
    <usage>

*/
//
// Author:      Werner Sun
// Created:     Wed May 26 21:47:25 EDT 2004
// $Id$
//
// Revision history
//
// $Log$

// system include files
#include <utility>

// user include files
#include "HadronicDBrFitter/HDBStandardFitInputFactory.h"

// forward declarations

class HDBStandardFitInputFactoryTTY : public HDBStandardFitInputFactory
{
      // ---------- friend classes and functions ---------------

   public:
      // ---------- constants, enums and typedefs --------------

      // ---------- Constructors and destructor ----------------
      HDBStandardFitInputFactoryTTY( bool aSingleTagsExclusive,
				     bool aGenerateMC );
      virtual ~HDBStandardFitInputFactoryTTY();

      // ---------- member functions ---------------------------
      virtual void makeFitPredictions() ; // instantiates m_fitPredictions.
      virtual void makeInputData() ;
      virtual void makeSeeds() ;
      virtual void makeExternalData() ;

      // ---------- const member functions ---------------------

      // ---------- static member functions --------------------

   protected:
      // ---------- protected member functions -----------------

      // ---------- protected const member functions -----------

   private:
      // ---------- Constructors and destructor ----------------
      HDBStandardFitInputFactoryTTY( const HDBStandardFitInputFactoryTTY& ); // stop default

      // ---------- assignment operator(s) ---------------------
      const HDBStandardFitInputFactoryTTY& operator=( const HDBStandardFitInputFactoryTTY& ); // stop default

      // ---------- private member functions -------------------
      virtual void getInputYieldsAndErrors() ;
      virtual void getInputYieldsAndErrorsMC() ;
      virtual void getBackgrounds() ;
      virtual void getEfficiencies() ;

      // ---------- private const member functions -------------

      // ---------- data members -------------------------------
      HepSymMatrix m_constantsUncorr ;
      HepSymMatrix m_numTermsCOdd ;
      HepSymMatrix m_numTermsCEven ;
      HepSymMatrix m_numTermsCBoth ;
      HepSymMatrix m_numCOddTermsCBoth ;

      // ---------- static data members ------------------------

};

// inline function definitions

// Uncomment the following lines, if your class is templated 
// and has an implementation file (in the Template directory)
//#if defined(INCLUDE_TEMPLATE_DEFINITIONS)
//# include "HadronicDBrFitter/Template/HDBStandardFitInputFactoryTTY.cc"
//#endif

#endif /* HADRONICDBRFITTER_HDBSTANDARDFITINPUTFACTORYTTY_H */
