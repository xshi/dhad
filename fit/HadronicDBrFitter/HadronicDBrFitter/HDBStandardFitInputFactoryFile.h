#if !defined(HADRONICDBRFITTER_HDBSTANDARDFITINPUTFACTORYFILE_H)
#define HADRONICDBRFITTER_HDBSTANDARDFITINPUTFACTORYFILE_H
// -*- C++ -*-
//
// Package:     <HadronicDBrFitter>
// Module:      HDBStandardFitInputFactoryFile
// 
/**\class HDBStandardFitInputFactoryFile HDBStandardFitInputFactoryFile.h HadronicDBrFitter/HDBStandardFitInputFactoryFile.h

 Description: <one line class summary>

 Usage:
    <usage>

*/
//
// Author:      Werner Sun
// Created:     Wed Dec  1 16:12:06 EST 2004
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

class HDBStandardFitInputFactoryFile : public HDBStandardFitInputFactory
{
      // ---------- friend classes and functions ---------------

   public:
      // ---------- constants, enums and typedefs --------------

      // ---------- Constructors and destructor ----------------
      HDBStandardFitInputFactoryFile( bool aSingleTagsExclusive,
				      bool aGenerateMC );
      virtual ~HDBStandardFitInputFactoryFile();

      // ---------- member functions ---------------------------
      virtual void makeFitPredictions() ; // instantiates m_fitPredictions.
      virtual void makeInputData() ;
      virtual void makeSeeds() ;

      // ---------- const member functions ---------------------

      // ---------- static member functions --------------------

   protected:
      // ---------- protected member functions -----------------

      // ---------- protected const member functions -----------

   private:
      // ---------- Constructors and destructor ----------------
      HDBStandardFitInputFactoryFile( const HDBStandardFitInputFactoryFile& ); // stop default

      // ---------- assignment operator(s) ---------------------
      const HDBStandardFitInputFactoryFile& operator=( const HDBStandardFitInputFactoryFile& ); // stop default

      // ---------- private member functions -------------------
      virtual void getInputYieldsAndErrors() ;
      virtual void getInputYieldsAndErrorsMC() ;
      virtual void getBackgrounds() ;
      virtual void getEfficiencies() ;

      // ---------- private const member functions -------------

      // ---------- data members -------------------------------

      // ---------- static data members ------------------------

};

// inline function definitions

// Uncomment the following lines, if your class is templated 
// and has an implementation file (in the Template directory)
//#if defined(INCLUDE_TEMPLATE_DEFINITIONS)
//# include "HadronicDBrFitter/Template/HDBStandardFitInputFactoryFile.cc"
//#endif

#endif /* HADRONICDBRFITTER_HDBSTANDARDFITINPUTFACTORYFILE_H */
