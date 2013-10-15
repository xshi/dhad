// -*- C++ -*-
#if !defined(HADRONICDNTUPLEPROC_HADRONICDNTUPLEPROC_H)
#define HADRONICDNTUPLEPROC_HADRONICDNTUPLEPROC_H
//
// Package:     <HadronicDNtupleProc>
// Module:      HadronicDNtupleProc
//
/**\class HadronicDNtupleProc HadronicDNtupleProc.h HadronicDNtupleProc/HadronicDNtupleProc.h
 
 Description: <one line class summary>

 Usage:
    <usage>

*/
//
// Author:      Peter Onyisi
// Created:     Fri Feb 27 16:35:43 EST 2004
// $Id$
//
// Revision history
//
// $Log$
// Revision 1.2  2010/05/21 19:30:44  xs32
// add isType1Pi0 info
//
// Revision 1.1  2010/05/17 17:30:24  xs32
// Add
//
// Revision 1.8  2006/02/01 17:56:59  srs63
// Added missing mass modes: 7 - pi0 from D0->Kspi0pi0, 14 - mode 4 with loose pi0s, 17 - mode 7 with loose pi0s
//
// Revision 1.7  2005/08/30 19:20:55  ponyisi
// Update to current state.  New features:
//
// New eta block parallels pi0s;
// New lepton ID variables (dpthmu, Rochester EID f_with_rich);
// Trkman info;
// Missing mass information filled in separate functions;
// dataselection.tcl has new input data types, allowing information to be
//   specified by another tcl;
// Will use setup_analysis if requested
//
// Revision 1.6  2004/09/24 17:24:19  ponyisi
// Split ntupling framework off to CWNFramework
//
// Revision 1.5  2004/08/20 20:38:47  ponyisi
// Make constructMCDmode a public static member
//
// Revision 1.4  2004/06/25 20:25:17  ponyisi
// Add TRRICHPHP and TRRICHKHP variables; add helper functions to
// HadronicDNtupleProc class
//
// Revision 1.3  2004/04/06 05:38:02  ponyisi
// Changes to add MC particle truth block.  No MC-to-detected matching yet.
//
// Revision 1.2  2004/03/22 19:25:02  ponyisi
// Added track tag info (you can now check if TagD*Prod thinks the track is
// 	a K or a pi)
// Added pi0 daughter shower link
// Added D four-vector
// Changed D0/D0bar distinction method: dmode is now always nonnegative.  Now,
// 	the variable dkchg stores the charge of the kaon.
//
// Revision 1.1.1.1  2004/03/12 18:43:50  ponyisi
// import source of HadronicDNtupleProc
//
//

// system include files

// user include files
#include "Processor/Processor.h"
#include "HistogramInterface/HistogramPackage.h"
#include "CommandPattern/Parameter.h"
#include "HadronicDNtupleProc/HadronicDTuple.h"
#include "CWNFramework/HbookCWNtupler.h"
#include "CWNFramework/RootCWNtupler.h"
#include "DTag/DTagList.h"

#include "CleoDChain/CDChargedPionList.h"
#include "CleoDChain/CDChargedKaonList.h"
#include "CleoDChain/CDPi0List.h"
#include "CleoDChain/CDEtaList.h"
#include "CleoDChain/CDKsList.h"

#if defined (__linux__)
#define f2cFortran 1
#endif

// forward declarations
class NavKs;
class NavPi0ToGG;
class NavEtaToGG;
class NavTrack;
class NavShower;
class MCParticle;
class LabNet4Momentum;

class HadronicDNtupleProc : public Processor
{
      // ------------ friend classes and functions --------------

   public:
      // ------------ constants, enums and typedefs --------------
      enum ShDetType { GOODBARREL, GOODENDCAP, INNERENDCAP,
		       TRANSENDCAP, TRANSBARREL };
      // ------------ Constructors and destructor ----------------
      HadronicDNtupleProc( void );                      // anal1 
      virtual ~HadronicDNtupleProc();                   // anal5 

      // ------------ member functions ---------------------------

      // methods for beginning/end "Interactive"
      virtual void init( void );             // anal1 "Interactive"
      virtual void terminate( void );        // anal5 "Interactive"

      // standard place for booking histograms
      virtual void hist_book( HIHistoManager& );                  

      // methods for binding to streams (anal2-4 etc.)
      virtual ActionBase::ActionResult event( Frame& iFrame );
      //virtual ActionBase::ActionResult beginRun( Frame& iFrame);
      //virtual ActionBase::ActionResult endRun( Frame& iFrame);

      // ------------ const member functions ---------------------

      // ------------ static member functions --------------------
      static int constructMCDmode(const MCParticle& mcpart);

   protected:
      // ------------ protected member functions -----------------

      // ------------ protected const member functions -----------

   private:
      // ------------ Constructors and destructor ----------------
      HadronicDNtupleProc( const HadronicDNtupleProc& );

      // ------------ assignment operator(s) ---------------------
      const HadronicDNtupleProc& operator=( const HadronicDNtupleProc& );

      // ------------ private member functions -------------------
      void bind( 
         ActionBase::ActionResult (HadronicDNtupleProc::*iMethod)( Frame& ),
	      const Stream::Type& iStream );

      int indexInKsBlock(const NavKs& kshort);
      int indexInPi0Block(const NavPi0ToGG& pi0);
      int indexInEtaBlock(const NavEtaToGG& eta);
      int indexInTrackBlock(const NavTrack& track);
      int indexInTrackBlock(int trackid);
      int indexInShowerBlock(const NavShower& show);
      int indexInShowerBlock(int showid);
      int indexInMCBlock(const MCParticle& mcpart);

      void makeMissingMassStage1(const DTagList& DTags, const LabNet4Momentum& labMomentum);
      void makeMissingMassStage2(const DTag& tagd, const LabNet4Momentum& labMomentum);

      bool isType1Pi0(const NavPi0ToGG& pi0);

      // ------------ private const member functions -------------

      // ------------ data members -------------------------------
      HadronicDTuple tuple;
      HbookCWNtupler hbntupler;
      RootCWNtupler roontupler;

      Parameter<DABoolean> m_makeHbookNtuple;
      Parameter<DABoolean> m_makeRootNtuple;
      Parameter<DABoolean> m_makeMCblock;
      Parameter<std::string> m_hbookFilename;
      Parameter<std::string> m_rootFilename;

      Parameter<float> m_loosePi0MinMass;
      Parameter<float> m_loosePi0MaxMass;

      struct { CDChargedPionList* pionList;
	    CDChargedPionList* pionListTrkEff;
	    CDChargedKaonList* kaonList;
	    CDChargedKaonList* kaonListTrkEff;
	    CDPi0List* pi0List;
		 CDPi0List* loosePi0List;
	    CDEtaList* etaList;
	    CDKsList* ksList;
	    std::vector<CDDecayList*>* fullyreco;
	    std::vector<pair<CDDecayList*,int>* >* recoils;
      } missingMassObjects;
      // ------------ static data members ------------------------
};

// inline function definitions

#endif /* HADRONICDNTUPLEPROC_HADRONICDNTUPLEPROC_H */
