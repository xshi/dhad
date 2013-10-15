// -*- C++ -*-
//
// Package:     HadronicDNtupleProc
// Module:      HadronicDNtupleProc
// 
// Description: <one line class summary>
//
// Implementation:
//     <Notes on implementation>
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
// Revision 1.1  2010/05/17 17:30:18  xs32
// Add
//
// Revision 1.6  2010/03/16 20:18:25  xs32
// freez the 10.1.3
//
// Revision 1.5  2009/05/06 18:12:35  xs32
// static_cast to eliminate warnings
//
// Revision 1.4  2009/05/05 20:00:21  xs32
// miminal fix
//
// Revision 1.1  2009/04/29 14:50:01  xs32
// add from tag ponyisi060929
//
// Revision 1.36  2006/02/01 17:56:58  srs63
// Added missing mass modes: 7 - pi0 from D0->Kspi0pi0, 14 - mode 4 with loose pi0s, 17 - mode 7 with loose pi0s
//
// Revision 1.35  2005/08/30 19:20:54  ponyisi
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
// Revision 1.34  2005/04/29 15:29:48  ponyisi
// Add LabNet4Momentum information
// Add shower e9/e25 and e9/e25 unfolded
//
// Revision 1.33  2005/04/14 18:23:28  ponyisi
// Store beamspot-corrected d0 (trdb)
//
// Revision 1.32  2005/01/10 21:26:17  srs63
// fixed bugs in missing mass modes 102 and 103
//
// Revision 1.31  2004/11/03 22:15:04  ponyisi
// Allow a fifth D daughter
//
// Revision 1.30  2004/09/24 17:24:06  ponyisi
// Split ntupling framework off to CWNFramework
//
// Revision 1.29  2004/07/28 18:38:50  ponyisi
// Fix usePID assignment for Steve
//
// Revision 1.28  2004/07/28 14:42:04  ponyisi
// Add trigger word for test board
//
// Revision 1.27  2004/07/19 17:38:35  ryd
// Added bunch decission to ntuple
//
// Revision 1.26  2004/07/15 16:29:58  ponyisi
// Fix Linux breakage of truth matching (fabs -> abs)
//
// Revision 1.25  2004/07/14 22:03:43  ponyisi
// Add trigger information
//
// Revision 1.24  2004/07/08 14:45:46  chengp
// added Monte Carlo match to DTag
//
// Revision 1.23  2004/06/29 21:34:34  ponyisi
// Add new RICH variables (was hypothesis analyzed?); add code to shut the
// ntupler up when reading D decay modes with etas; first stab at MC truth
// matching for low level objects; fix bug whereby particles (Ks, pi0) decayed
// by cleog didn't have their daughters stored; add two helper functions; other
// cleanup
//
// Revision 1.22  2004/06/25 17:57:46  ponyisi
// D Tag extract call now protected against DAException for unavailable modes
//
// Revision 1.21  2004/06/23 13:32:31  ryd
// Corrections to track eff studies
//
// Revision 1.20  2004/06/22 03:58:35  ryd
// Added D0->Kspi+pi- as a mode for KS eff. studies
//
// Revision 1.19  2004/06/19 03:23:09  ryd
// Rewrote the code for tracking eff. studies.
//
// Revision 1.18  2004/05/26 14:46:29  ponyisi
// Do not fill per-detector track hit fractions until necessary accessors are
// available from TrackFitQuality; fill overall track hit fraction; fill
// Kshort flight significance
//
// Revision 1.17  2004/05/18 23:02:17  ponyisi
// Fill track chi^2, ndof, hit fraction variables; add track fit abort variable;
// fix Kshort rad and raderr variables to report xy distance and error (not 3d
// distance as before)
//
// Revision 1.16  2004/05/13 15:00:45  ryd
// Added lepton veto variables to ntuple
//
// Revision 1.15  2004/05/12 19:27:43  ryd
// Further changes to handle the K-pi tracking eff. studies.
//
// Revision 1.14  2004/05/07 02:26:19  ponyisi
// Change "mcdmode" and "mcdbmode" so that intermediate resonances are
// ignored and only "stable" final state particles are counted.  Also
// leptons have a mode number assignment.
//
// Revision 1.13  2004/05/07 02:17:52  ryd
// added M2miss block to measure pi0 eff. and K and pi tracking eff. in the Kpipi0 mode
//
// Revision 1.12  2004/04/20 18:24:57  ponyisi
// MC block now larger, also diagnostics will be printed if block size
// exceeded
//
// Revision 1.11  2004/04/06 05:37:56  ponyisi
// Changes to add MC particle truth block.  No MC-to-detected matching yet.
//
// Revision 1.10  2004/04/04 21:23:46  ryd
// Changed to use DTagUtilities::m2miss
//
// Revision 1.9  2004/04/01 21:01:05  ryd
// Fixes to the M2miss calculation
//
// Revision 1.8  2004/04/01 20:11:31  ponyisi
// Change "dkchg" to "dcsign": new variable is the sign of the charm quark if the
// decay determines it, and is 0 for D0 self conjugate modes
//
// Revision 1.7  2004/03/30 19:44:14  ponyisi
// Eliminate the define 'MAXDCAND'
//
// Revision 1.6  2004/03/25 00:31:27  wsun
// Added chi2vddb to double tag block.
//
// Revision 1.5  2004/03/24 23:44:24  wsun
// Added DDoubleTag block to ntuple.
//
// Revision 1.4  2004/03/22 19:24:43  ponyisi
// Added track tag info (you can now check if TagD*Prod thinks the track is
// 	a K or a pi)
// Added pi0 daughter shower link
// Added D four-vector
// Changed D0/D0bar distinction method: dmode is now always nonnegative.  Now,
// 	the variable dkchg stores the charge of the kaon.
//
// Revision 1.3  2004/03/20 23:34:58  ryd
// Fix Linux compilation problems
//
// Revision 1.2  2004/03/17 17:10:39  ryd
// Added block for missing mass
//
// Revision 1.1.1.1  2004/03/12 18:43:51  ponyisi
// import source of HadronicDNtupleProc
//
//

#include "Experiment/Experiment.h"

// system include files
#include <stdlib.h>

// user include files
#include "HadronicDNtupleProc/HadronicDNtupleProc.h"
#include "Experiment/report.h"
#include "Experiment/units.h"  // for converting to/from standard CLEO units

#include "DataHandler/Record.h"
#include "DataHandler/Frame.h"
#include "FrameAccess/extract.h"
#include "FrameAccess/FAItem.h"
#include "FrameAccess/FATable.h"

#include "Navigation/NavTrack.h"
#include "TrackRoot/TRHelixFit.h"
#include "TrackRoot/TRTrackFitQuality.h"
#include "TrackRoot/TRSeedTrackQuality.h"
#include "TrackDelivery/TDKinematicFit.h"

#include "Navigation/NavShower.h"
#include "Navigation/NavPi0ToGG.h"
#include "Navigation/NavEtaToGG.h"
#include "Navigation/NavKs.h"
#include "Navigation/NavTkShMatch.h"
#include "Navigation/NavMuonId.h"
#include "C3cc/CcShowerAttributes.h"
#include "PhotonDecays/PhdPi0.h"
#include "PhotonDecays/PhdEtaToGG.h"
#include "DedxInfo/DedxInfo.h"
#include "Navigation/NavRich.h"
#include "CleoDChain/CDChargedKaonList.h"
#include "CleoDChain/CDChargedPionList.h"
#include "CleoDChain/CDKs.h"
#include "CleoDChain/CDKsList.h"
#include "CleoDChain/CDPi0.h"
#include "CleoDChain/CDPi0List.h"
#include "CleoDChain/CDEta.h"
#include "CleoDChain/CDEtaList.h"
#include "CleoDChain/CDDecayList.h"

#include "DChain/List/Template/DCDecayList.cc"
#include "DTag/DTagList.h"
#include "DTag/DTagDecayModes.h"
#include "DTag/DTagUtilities.h"
#include "DDoubleTag/DDoubleTag.h"
#include "DDoubleTag/DDoubleTagList.h"

#include "MCInfo/MCDecayTree/MCDecayTree.h"
#include "MCTrackTagger/MCTrackTagsByMCParticle.h"
#include "MCCCTagger/MCCCTagsByMCParticle.h"
#include "Navigation/MCTKShortTagger.h"
#include "Navigation/MCCCPi0Tagger.h"
#include "Navigation/MCCCEtaTagger.h"

#include "CesrCleoComm/CesrCrossingAngle.h"
#include "BeamEnergy/BeamEnergy.h"
#include "TriggerL1Data/TriggerL1Data.h"
#include "LabNet4Momentum/LabNet4Momentum.h"
#include "VFinderQualityObject/KsQuality.h"
#include "BunchFinder/BunchDecision.h"
#include "EID/EIDS.h"
#include "Trkman/TrkmanInfo.h"
#include "MagField/MagneticField.h"

//#include "cfortran.h"
//#include "packlib.h"

// STL classes
// You may have to uncomment some of these or other stl headers 
// depending on what other header files you include (e.g. FrameAccess etc.)!
//#include <string>
#include <vector>
//#include <set>
//#include <map>
//#include <algorithm>
#include <utility>

//
// constants, enums and typedefs
//
static const char* const kFacilityString = "Processor.HadronicDNtupleProc" ;

// ---- cvs-based strings (Id and Tag with which file was checked out)
static const char* const kIdString  = "$Id$";
static const char* const kTagString = "$Name$";


//
// static data member definitions
//


//
// Forward defs
//

DChainBoolean pionSelector( CDChargedPion& iPion );

DChainBoolean kaonSelector( CDChargedKaon& iKaon );

//DChainBoolean loosePi0Selector( CDPi0& iPi0 );
class Pi0Selector: public DCSelectionFunction< CDPi0 >{

	public:
	Pi0Selector(double minMass, double maxMass)
	{
		m_minMass = minMass;
		m_maxMass = maxMass;
	}

	bool operator()( CDPi0& iPi0 )
	{
		double pi0Mass = iPi0.pi0().unconMass();
		if ( pi0Mass > m_minMass && pi0Mass < m_maxMass ) return true;
		else return false;
	}

	private:
	double m_minMass;
	double m_maxMass;

};

NavPi0ToGG* TurnPhdPi0IntoNavPi0ToGG( const PhdPi0& input, const FATable<NavShower>& showerTable )
{
	const NavShower* hiEnShower = &(*(showerTable.find( input.hiEnId() )));
	const NavShower* loEnShower = &(*(showerTable.find( input.loEnId() )));
	return new NavPi0ToGG( &input, hiEnShower, loEnShower);
}

FATable< NavPi0ToGG > TurnPhdPi0sIntoNavPi0ToGGs(const FATable< PhdPi0 >& PhdPi0Table, const FATable<NavShower>& showerTable )
{
	FAPtrTable< NavPi0ToGG > *  NavPi0ToGGPtrTable = new FAPtrTable< NavPi0ToGG > ();
	FATable<PhdPi0>::const_iterator PhdPi0TableEnd = PhdPi0Table.end();
   for (FATable<PhdPi0>::const_iterator PhdPi0TableItr = PhdPi0Table.begin();
			PhdPi0TableItr != PhdPi0TableEnd;
			PhdPi0TableItr++)
	{
		NavPi0ToGG* NavPi0ToGGPtr = TurnPhdPi0IntoNavPi0ToGG( *PhdPi0TableItr, showerTable );
		NavPi0ToGGPtrTable->insert(NavPi0ToGGPtr);
	}
	return FATable< NavPi0ToGG > ( NavPi0ToGGPtrTable );
}

//
// constructors and destructor
//
HadronicDNtupleProc::HadronicDNtupleProc( void )               // anal1
   : Processor( "HadronicDNtupleProc" ),
     m_makeHbookNtuple("makeHbookNtuple", this, true),
     m_makeRootNtuple("makeRootNtuple", this, true),
     m_makeMCblock("makeMCblock", this, false),
     m_hbookFilename("hbookFilename", this, "dntuple.rzn"),
     m_rootFilename("rootFilename", this, "dntuple.root"),
	  m_loosePi0MinMass("loosePi0MinMass", this, 0.080),
	  m_loosePi0MaxMass("loosePi0MaxMass", this, 0.180)
{
   report( DEBUG, kFacilityString ) << "here in ctor()" << endl;

   // ---- bind a method to a stream -----
   // These lines ARE VERY IMPORTANT! If you don't bind the 
   // code you've just written (the "action") to a stream, 
   // your code won't get executed!

   bind( &HadronicDNtupleProc::event,    Stream::kEvent );
   //bind( &HadronicDNtupleProc::beginRun, Stream::kBeginRun );
   //bind( &HadronicDNtupleProc::endRun,   Stream::kEndRun );

   // do anything here that needs to be done at creation time
   // (e.g. allocate resources etc.)
   m_makeHbookNtuple.setHelpString("Set to true to make a HBOOK-format ntuple");
   m_makeRootNtuple.setHelpString("Set to true to make a ROOT-format ntuple");
   m_makeMCblock.setHelpString("Set to true to make MC truth variables.  Do NOT set this for data.");
   m_hbookFilename.setHelpString("Sets the location of the HBOOK-format output file (if any)");
   m_rootFilename.setHelpString("Sets the location of the ROOT-format output file (if any)");

	m_loosePi0MinMass.setHelpString("Low end of mass cut for loose pi0's");
	m_loosePi0MaxMass.setHelpString("High end of mass cut for loose pi0's");
}

HadronicDNtupleProc::~HadronicDNtupleProc()                    // anal5
{
   report( DEBUG, kFacilityString ) << "here in dtor()" << endl;
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}

//
// member functions
//

// ------------ methods for beginning/end "Interactive" ------------
// --------------------------- init method -------------------------
void
HadronicDNtupleProc::init( void )          // anal1 "Interactive"
{

   // do any initialization here based on Parameter Input by User
   // (e.g. run expensive algorithms that are based on parameters
   //  specified by user at run-time)

   tuple.setOptBlockStatus("MC", m_makeMCblock.value());
   if (m_makeHbookNtuple.value()) {
      hbntupler.init(m_hbookFilename.value(), &tuple);
   }
   if (m_makeRootNtuple.value()) {
      roontupler.init(m_rootFilename.value(), &tuple);
   }

}

// -------------------- terminate method ----------------------------
void
HadronicDNtupleProc::terminate( void )     // anal5 "Interactive"
{
   report( DEBUG, kFacilityString ) << "here in terminate()" << endl;

   // do anything here BEFORE New Parameter Change
   // (e.g. write out result based on parameters from user-input)

   if (m_makeHbookNtuple.value())
      hbntupler.finalize();
   if (m_makeRootNtuple.value())
      roontupler.finalize();
}


// ---------------- standard place to book histograms ---------------
void
HadronicDNtupleProc::hist_book( HIHistoManager& iHistoManager )
{
   report( DEBUG, kFacilityString ) << "here in hist_book()" << endl;

   // book your histograms here

}

// --------------------- methods bound to streams -------------------
ActionBase::ActionResult
HadronicDNtupleProc::event( Frame& iFrame )          // anal3 equiv.
{
   report( DEBUG, kFacilityString ) << "here in event()" << endl;

   tuple.clear();

   tuple.run = iFrame.syncValue().runNumber();
   tuple.event = iFrame.syncValue().eventNumber();


   FAItem< BeamEnergy > beamenergy;
   extract( iFrame.record( Stream::kStartRun ) , beamenergy );
   assert(beamenergy.valid());
   tuple.ecm = 2*beamenergy->value();

   FAItem<TriggerL1Data> triggerL1;
   extract( iFrame.record( Stream::kEvent ) , triggerL1 );
   tuple.l1trig = triggerL1->getTriggerLines(TriggerL1Data::kBoard2Number);
   tuple.l1trig2 = triggerL1->getTriggerLines(TriggerL1Data::kBoard1Number);

   FAItem< BunchDecision > m_bunch;
   
   // Extract the bunch decision info
   extract( iFrame.record(Stream::kEvent), m_bunch );
                                                                                
   // Bunch info
   tuple.nbunch = m_bunch->numberOfTestedBunches();
   tuple.bunch = m_bunch->bestBunchNumber();



   FAItem<LabNet4Momentum> labMomentum;
   extract(iFrame.record(Stream::kStartRun), labMomentum);
   tuple.pxcm = (*labMomentum).px();
   tuple.pycm = (*labMomentum).py();
   tuple.pzcm = (*labMomentum).pz();

   FAItem<CesrCrossingAngle> xingangle;
   try {
      extract( iFrame.record( Stream::kStartRun ) , xingangle );
      tuple.xangle = xingangle->value();
   } catch (const DAExceptionBase& e) {
      tuple.xangle = asin(-(*labMomentum).px()/tuple.ecm);
   } 

//   CDChargedKaonList kaonList;
   missingMassObjects.kaonList = new CDChargedKaonList();
   FATable< NavTrack> kaonListTmp;
   extract(iFrame.record(Stream::kEvent), kaonListTmp, "TagDKaon");
   *missingMassObjects.kaonList=kaonListTmp;

//   CDChargedPionList pionList;
   missingMassObjects.pionList = new CDChargedPionList();
   FATable< NavTrack > pionListTmp;
   extract(iFrame.record(Stream::kEvent), pionListTmp, "TagDPion");
   *missingMassObjects.pionList=pionListTmp;


   FATable< NavTrack > tracks;
   extract( iFrame.record( Stream::kEvent ) , tracks );
   assert(tracks.valid());

//   CDChargedPionList pionListTrkEff(pionSelector);
   missingMassObjects.pionListTrkEff = new CDChargedPionList(pionSelector);
   *missingMassObjects.pionListTrkEff=tracks;

//   CDChargedKaonList kaonListTrkEff(kaonSelector);
   missingMassObjects.kaonListTrkEff = new CDChargedKaonList(kaonSelector);
   *missingMassObjects.kaonListTrkEff=tracks;

   FATable< EIDS > eidsTable;
   extract( iFrame.record( Stream::kEvent ) , eidsTable );

   FATable<NavTrack>::const_iterator trend = tracks.end();
   for (FATable<NavTrack>::const_iterator trit = tracks.begin();
	trit != trend && tuple.ntrack < MAXNTRACK; trit++) {
      tuple.trident[tuple.ntrack] = (*trit).identifier();
      FAItem<TDKinematicFit> pionFit = (*trit).pionFit();
      assert(pionFit.valid());
      tuple.trpie[tuple.ntrack] = (*pionFit).energy();
      tuple.trpipx[tuple.ntrack] = (*pionFit).px();
      tuple.trpipy[tuple.ntrack] = (*pionFit).py();
      tuple.trpipz[tuple.ntrack] = (*pionFit).pz();
      tuple.trpip[tuple.ntrack] = (*pionFit).pmag();
      FAItem<TDKinematicFit> kaonFit = (*trit).kaonFit();
      assert(kaonFit.valid());
      tuple.trke[tuple.ntrack] = (*kaonFit).energy();
      tuple.trkpx[tuple.ntrack] = (*kaonFit).px();
      tuple.trkpy[tuple.ntrack] = (*kaonFit).py();
      tuple.trkpz[tuple.ntrack] = (*kaonFit).pz();
      tuple.trchg[tuple.ntrack] = (*kaonFit).charge();
      FAItem<TRHelixFit> pionHelix = (*trit).pionHelix();
      assert(pionHelix.valid());
      tuple.trz0[tuple.ntrack] = (*pionHelix).z0();
      tuple.trd0[tuple.ntrack] = (*pionHelix).d0();
      tuple.trdb[tuple.ntrack] = (*trit).signedDCABeamSpot(*pionHelix);
      tuple.trcosth[tuple.ntrack] = (*pionFit).momentum().cosTheta();
      tuple.trphi0[tuple.ntrack] = (*pionHelix).phi0();
      TRTrackFitQuality pionQual = *((*trit).pionQuality());
      tuple.trchi2[tuple.ntrack] = pionQual.chiSquare();
      tuple.trchi2dof[tuple.ntrack] = pionQual.degreesOfFreedom();
/*
      tuple.trdrhitf[tuple.ntrack] = (float) (pionQual.numberSubdetectorHitLayers(TRSubdetectorLists::kDR3Axial) +
					      pionQual.numberSubdetectorHitLayers(TRSubdetectorLists::kDR3Stereo))/47.;
      tuple.trzdhitf[tuple.ntrack] = (float) (pionQual.numberSubdetectorHitLayers(TRSubdetectorLists::kZD))/6.;
*/
      tuple.trhitf[tuple.ntrack] = pionQual.ratioNumberHitsToExpected();
      tuple.trfabort[tuple.ntrack] = pionQual.fitAbort();
      FAItem<DedxInfo> dedx = (*trit).dedxInfo();
      if (dedx.valid()) {
	 tuple.trsigpi[tuple.ntrack] = (*dedx).piSigma();
	 tuple.trsigk[tuple.ntrack] = (*dedx).kSigma();
      } else {
	 tuple.trsigpi[tuple.ntrack] = 1e6;
	 tuple.trsigk[tuple.ntrack] = 1e6;
      }
      FAItem<NavRich> rich = (*trit).richInfo();
      if (rich.valid()) {
	 tuple.trrichpll[tuple.ntrack] = (*rich).pionLogLikelihood();
	 tuple.trrichpnp[tuple.ntrack] = (*rich).pionNumberOfPhotonsInAverage();
	 tuple.trrichphp[tuple.ntrack] = (*rich).pionHypWasAnalyzed();
	 tuple.trrichkll[tuple.ntrack] = (*rich).kaonLogLikelihood();
	 tuple.trrichknp[tuple.ntrack] = (*rich).kaonNumberOfPhotonsInAverage();
	 tuple.trrichkhp[tuple.ntrack] = (*rich).kaonHypWasAnalyzed();
      } else {
	 tuple.trrichpll[tuple.ntrack] = 0;
	 tuple.trrichpnp[tuple.ntrack] = 0;
	 tuple.trrichphp[tuple.ntrack] = 0;
	 tuple.trrichkll[tuple.ntrack] = 0;
	 tuple.trrichknp[tuple.ntrack] = 0;
	 tuple.trrichkhp[tuple.ntrack] = 0;
      }
      int tagvalue = 0;
      FAItem<NavTrack> temptr;
      int trident = tuple.trident[tuple.ntrack];
      temptr = pionListTmp.find(trident);
      if (temptr.valid()) {
	 tagvalue += 1<<0;
      }
      temptr = kaonListTmp.find(trident);
      if (temptr.valid()) {
	 tagvalue += 1<<1;
      }
      tuple.trtaginfo[tuple.ntrack] = tagvalue;
      tuple.trdpthmu[tuple.ntrack] = (*trit).muonId().depth();
      tuple.trroceid[tuple.ntrack] = eidsTable[(*trit).identifier()].F_with_rich();
      tuple.trtrkman[tuple.ntrack] = (*(*trit).trkmanInfo()).classificationCode();
      tuple.ntrack++;
   }
   if (tuple.ntrack >= MAXNTRACK) {
     report( NOTICE, kFacilityString ) 
	<< "Hard limit on number of track candidates exceeded" << endl;
   }


   FATable< NavShower > showtable;
   extract( iFrame.record( Stream::kEvent ) , showtable );
   FATable<NavShower>::const_iterator showend = showtable.end();

   for(FATable<NavShower>::const_iterator sit = showtable.begin();
       sit != showend; sit++) {
      tuple.sident[tuple.nshow] = (*sit).identifier();
      const CcShowerAttributes& att = (*sit).attributes();
      tuple.se[tuple.nshow] = att.energy();
      const Hep3Vector& mom = att.momentum();
      tuple.spx[tuple.nshow] = mom.x();
      tuple.spy[tuple.nshow] = mom.y();
      tuple.spz[tuple.nshow] = mom.z();
      tuple.sphi[tuple.nshow] = mom.phi();
      tuple.scosth[tuple.nshow] = cos(att.theta());
      tuple.se9o25uok[tuple.nshow] = att.e9oe25UnfOK();
      tuple.se9o25[tuple.nshow] = att.e9oe25();
      tuple.se9o25u[tuple.nshow] = att.e9oe25Unf();
      tuple.shot[tuple.nshow] = att.hot();
      ShDetType dettype;
      if (att.goodBarrel()) {
	 dettype = GOODBARREL;
      } else if (att.goodEndcap()) {
	 dettype = GOODENDCAP;
      } else if (att.innerEndcap()) {
	 dettype = INNERENDCAP;
      } else if (att.endcap() && att.transition()) {
	 dettype = TRANSENDCAP;
      } else {
	 dettype = TRANSBARREL;
      }
      tuple.sdettype[tuple.nshow] = dettype;
      FATable< NavTkShMatch > trmatches = (*sit).trackMatches();
      if (trmatches.empty()) {
	 tuple.strmatch[tuple.nshow] = -1;
	 tuple.strme[tuple.nshow] = 0;
	 tuple.strdist[tuple.nshow] = -1;
      } else {
	 // find highest momentum track
	 int index = -1;
	 float distance = -1;
	 float mom = -1; 
	 tuple.strme[tuple.nshow] = 0;
	 for (FATable<NavTkShMatch>::const_iterator tmit = trmatches.begin();
	      tmit != trmatches.end(); tmit++) {
	    if ((*(*tmit).navTrack().pionFit()).pmag() > mom) {
	       mom = (*(*tmit).navTrack().pionFit()).pmag();
	       index = indexInTrackBlock((*tmit).navTrack());
	       distance = (*tmit).distance();
	    }
	    tuple.strme[tuple.nshow] += (*tmit).matchedEnergy();
	 }
	 tuple.strmatch[tuple.nshow] = index;
	 tuple.strdist[tuple.nshow] = distance;
      }
      tuple.nshow++;
   }


   if (tuple.nshow >= MAXNSHOW) {
     report( NOTICE, kFacilityString ) 
	<< "Hard limit on number of showers exceeded" << endl;
   }

   FATable< NavPi0ToGG > pi0table;
   extract( iFrame.record( Stream::kEvent ) , pi0table, "TagDPi0" );

//   CDPi0List pi0List;
   missingMassObjects.pi0List = new CDPi0List();
   *missingMassObjects.pi0List=pi0table;

   // loose pi0 list
	FATable< PhdPi0 > loosePi0table;
	extract( iFrame.record( Stream::kEvent ) , loosePi0table, "", "loosePi0");
	Pi0Selector loosePi0Selector(m_loosePi0MinMass.value(), m_loosePi0MaxMass.value() );
   missingMassObjects.loosePi0List = new CDPi0List(loosePi0Selector);
   //	*missingMassObjects.loosePi0List = TurnPhdPi0sIntoNavPi0ToGGs(loosePi0table, showtable);
   //   xs32: avoide the memory leak, only used for the missing mass calculation
   
   

   FATable<NavPi0ToGG>::const_iterator pi0end = pi0table.end();

   for (FATable<NavPi0ToGG>::const_iterator pi0it = pi0table.begin();
	pi0it != pi0end && tuple.npi0 < MAXNPI0; pi0it++) {
      const PhdPi0& pi0((*pi0it).pi0());
      if (!pi0.fit()) {
	 report( NOTICE, kFacilityString ) << "Pi0 fit failed" << endl;
	 continue;
      }
      tuple.pi0ident[tuple.npi0] = pi0.identifier();
      tuple.pi0mass[tuple.npi0] = pi0.unconMass();
      tuple.pi0chi2[tuple.npi0] = pi0.chisq();
      tuple.pi0e[tuple.npi0] = pi0.energy();
      tuple.pi0px[tuple.npi0] = pi0.px();
      tuple.pi0py[tuple.npi0] = pi0.py();
      tuple.pi0pz[tuple.npi0] = pi0.pz();
      tuple.pi0merr[tuple.npi0] = pi0.errUnconMass();
      tuple.pi0dau1[tuple.npi0] = indexInShowerBlock((*pi0it).hiEnShower());
      tuple.pi0dau2[tuple.npi0] = indexInShowerBlock((*pi0it).loEnShower());
      tuple.pi0istype1[tuple.npi0] = isType1Pi0(*pi0it);
      tuple.npi0++;
   }
   if (tuple.npi0 >= MAXNPI0) {
     report( NOTICE, kFacilityString ) 
	<< "Hard limit on number of pi0 candidates exceeded" << endl;
   }

   FATable< NavEtaToGG > etatable;
   extract( iFrame.record( Stream::kEvent ) , etatable, "TagDEta" );

   missingMassObjects.etaList = new CDEtaList();
   *missingMassObjects.etaList=etatable;

   FATable<NavEtaToGG>::const_iterator etaend = etatable.end();

   for (FATable<NavEtaToGG>::const_iterator etait = etatable.begin();
	etait != etaend && tuple.neta < MAXNETA; etait++) {
      const PhdEtaToGG& eta((*etait).eta());
      if (!eta.fit()) {
	 report( NOTICE, kFacilityString ) << "Eta fit failed" << endl;
	 continue;
      }
      tuple.etaident[tuple.neta] = eta.identifier();
      tuple.etamass[tuple.neta] = eta.unconMass();
      tuple.etachi2[tuple.neta] = eta.chisq();
      tuple.etae[tuple.neta] = eta.energy();
      tuple.etapx[tuple.neta] = eta.px();
      tuple.etapy[tuple.neta] = eta.py();
      tuple.etapz[tuple.neta] = eta.pz();
      tuple.etamerr[tuple.neta] = eta.errUnconMass();
      tuple.etadau1[tuple.neta] = indexInShowerBlock((*etait).hiEnShower());
      tuple.etadau2[tuple.neta] = indexInShowerBlock((*etait).loEnShower());
      tuple.neta++;
   }
   if (tuple.neta >= MAXNETA) {
     report( NOTICE, kFacilityString ) 
	<< "Hard limit on number of eta candidates exceeded" << endl;
   }

   FATable< NavKs > kstable;
   extract( iFrame.record( Stream::kEvent ), kstable, "TagDKShort" );

   FATable<KsQuality> ksqual;
   try {
      extract( iFrame.record( Stream::kEvent ), ksqual );
   } catch (const DAExceptionBase& e) { } 
   missingMassObjects.ksList = new CDKsList();
   *missingMassObjects.ksList = kstable;

   FATable<NavKs>::const_iterator ksend = kstable.end();
   for (FATable<NavKs>::const_iterator ksit = kstable.begin();
	ksit != ksend && tuple.nks < MAXNKS; ksit++) {
      tuple.ksident[tuple.nks] = (*ksit).identifier();
      const VXFitVeeKShort& vee = (*ksit).kShort();
      tuple.ksmass[tuple.nks] = vee.mass();
      tuple.kse[tuple.nks] = vee.energy();
      tuple.kspx[tuple.nks] = vee.px();
      tuple.kspy[tuple.nks] = vee.py();
      tuple.kspz[tuple.nks] = vee.pz();
      tuple.kschi2[tuple.nks] = vee.fitChiSquare();
      tuple.ksrad[tuple.nks] = vee.rxy();
      tuple.ksraderr[tuple.nks] = vee.rxyErr();
      tuple.ksdau1[tuple.nks] = indexInTrackBlock((*ksit).piPlus());
      tuple.ksdau2[tuple.nks] = indexInTrackBlock((*ksit).piMinus());
      assert(tuple.ksdau1[tuple.nks] >= 0);
      assert(tuple.ksdau2[tuple.nks] >= 0);

//      tuple.ksflsig[tuple.nks] = -1;
      if (ksqual.valid()) {
	 FATable<KsQuality>::const_iterator this_qual = ksqual.find((*ksit).identifier());
	 if (this_qual != ksqual.end()) {
	    tuple.ksflsig[tuple.nks] = (*this_qual).flightDistanceSignificanceEnhanced2D();
	 }
      }

      tuple.nks++;
   }

   if (tuple.nks >= MAXNKS) {
     report( NOTICE, kFacilityString ) 
	<< "Hard limit on number of Kshort candidates exceeded" << endl;
   }

   FAItem<DTagList> iDListItem;

   report( DEBUG, kFacilityString ) << "tuple.ndcand=" << tuple.ndcand << endl;
   assert(tuple.ndcand == 0);

   // Used to match DDoubleTag daughters to entries in DTag list.
   STL_VECTOR( CDFootPrint ) footPrintArray ;

   for(DTagDecayModes::const_iterator itMode = 
	  DTag::modes().begin();
       itMode != DTag::modes().end();
       //       itMode == DTag::modes().begin();
       itMode++) {
      try {
         extract(iFrame.record(Stream::kEvent),
                 iDListItem, itMode->second.name() );
      } catch (const DAExceptionBase& e) { }
      if (! iDListItem.valid()) {
	 continue;
      }
   
      //      makeMissingMassStage1(*iDListItem, *labMomentum);

      DTagList::const_iterator tagdEnd = (*iDListItem).particle_end();
      DTagList::const_iterator tagd = (*iDListItem).particle_begin();
      for( ; tagd != tagdEnd && tuple.ndcand < MAXNDCAND; ++tagd )
      {
	 const DTag& tagDecay = dynamic_cast<const DTag&>((*tagd).particle());
	 // Fill tuple.mcdmatch[] with MC particle idetifier at this moment,
	 // because we don't have the MC block right now
	 if (m_makeMCblock.value()) {
	   tuple.mcdmatch[tuple.ndcand] = -1;       // Default value
	   if (tagDecay.hasMatchedMCParticle()) {
	     const MCParticle& mcParticle = tagDecay.matchedMCParticle();
	     PDG_id pdgid = mcParticle.properties().PDGId();
	     if (abs(pdgid) == 411 || abs(pdgid) == 421) {
	       tuple.mcdmatch[tuple.ndcand] = mcParticle.identifier();
	     }
	   }
	   else {
	   }
	 }

	 //	 makeMissingMassStage2(tagDecay, *labMomentum);

	 footPrintArray.push_back( tagDecay.footPrint() ) ;

	 tuple.dmode[tuple.ndcand] = tagDecay.decayMode();
	 tuple.dmbc[tuple.ndcand] = tagDecay.beamConstrainedMass();
	 tuple.ddeltae[tuple.ndcand] = tagDecay.deltaE();
	 tuple.ddeltaeerr[tuple.ndcand] = -1;
	 tuple.dmraw[tuple.ndcand] = tagDecay.mass();
	 tuple.dmrawerr[tuple.ndcand] = -1;
	 tuple.dkchi2[tuple.ndcand] = -1;
	 const KTKinematicData& ktdata = tagDecay.kinematicData();
	 tuple.dcsign[tuple.ndcand] = tagDecay.charm();
/*
	 // Is D charged? Then charm sign is same as D charge
	 if (ktdata.charge() != 0) {
	    tuple.dcsign[tuple.ndcand] =(int) ktdata.charge();
	 } else {
	    // charm sign is minus the sign of the kaon
	    tuple.dcsign[tuple.ndcand] = -1*(int)tagDecay.child(DCChildren::First).charge();
	 }
*/
	 tuple.lepveto[tuple.ndcand] = 1+DTagUtilities::numberOfUnmatchedOtherSideShowersAbove50MeV(tagDecay,showtable);
         if (DTagUtilities::primaryTracksInDTagPassLeptonVeto(tagDecay)) tuple.lepveto[tuple.ndcand] *= -1;
	 tuple.de[tuple.ndcand] = ktdata.energy();
	 tuple.dpx[tuple.ndcand] = ktdata.px();
	 tuple.dpy[tuple.ndcand] = ktdata.py();
	 tuple.dpz[tuple.ndcand] = ktdata.pz();
	 int nDau = tagDecay.numberChildren();
	 //	 const STL_VECTOR(DCReferenceHolder<CDCandidate>) & vect = tagDecay.children();
	 const STL_VECTOR(dchain::ReferenceHolder<CDCandidate>) & vect = tagDecay.children();
	 assert(nDau <= 5);
	 for (int dau = 0; dau < nDau; dau++) {
	    const CDCandidate& cddau = *(vect[dau]);
//	    const CDCandidate* cddau = &tagDecay.child(dau);
	    int index = -1;
	    if (cddau.builtFromCDKs()) {
	       index = indexInKsBlock(cddau.navKshort());
	       assert(index >= 0);
	    } else if (cddau.builtFromCDPi0()) {
	       index = indexInPi0Block(cddau.navPi0());
	       assert(index >= 0);
	    } else if (cddau.builtFromTrack()) {
	       index = indexInTrackBlock(cddau.track());
	       assert(index >= 0);
	    } else if (cddau.builtFromCDEta()) {
	       index = indexInEtaBlock(cddau.navEta());
	       assert(index >= 0);
	       report( DEBUG, kFacilityString )
		  << "While finding D daughters: Eta daughters trying!"
		  << endl;
	    } else {
	       report( NOTICE, kFacilityString )
		  << "While finding D daughters: unknown daughter mode"
		  << endl;
	    }
	    switch(dau) {
	       case 0:
		  tuple.ddau1[tuple.ndcand] = index;
		  break;
	       case 1:
		  tuple.ddau2[tuple.ndcand] = index;
		  break;
	       case 2:
		  tuple.ddau3[tuple.ndcand] = index;
		  break;
	       case 3:
		  tuple.ddau4[tuple.ndcand] = index;
		  break;
	       case 4:
		  tuple.ddau5[tuple.ndcand] = index;
		  break;
	       default:
		  DABoolean D_daughter_out_of_range = false;
		  assert(D_daughter_out_of_range);
	    }
	 }
	 tuple.ndcand++;
      }
   }
   if (tuple.ndcand >= MAXNDCAND) {
     report( NOTICE, kFacilityString ) 
	<< "Hard limit on number of D candidates exceeded" << endl;
   }

   //   assert(tuple.ndcand == footPrintArray.size());
   assert(static_cast<unsigned int>(tuple.ndcand) == footPrintArray.size());

   // now we need magfield for Werner's changes
   FAItem<MagneticField> magField;
   extract( iFrame.record( Stream::kStartRun ), magField );
   
  // wsun 03-19-04: extract DDoubleTagList
  for( SmallCount i = 0 ; i < DDoubleTag::kNumOfDDbarModes ; ++i )
  {
     FAItem< DDoubleTagList > doubleTagList ;
     extract( iFrame.record( Stream::kEvent ),
	      doubleTagList,
	      DDoubleTag::kUsageTag[ i ].c_str() ) ;

     DDoubleTagList::const_iterator ttItr = doubleTagList->particle_begin() ;
     DDoubleTagList::const_iterator ttEnd = doubleTagList->particle_end() ;

     for( ; ttItr != ttEnd && tuple.nddcand < MAXNDDCAND ; ++ttItr )
     {
       //const DDoubleTag& doubleTag = dynamic_cast< const DDoubleTag& >(( *ttItr ).particle() ) ;
	DDoubleTag doubleTag = ( *ttItr ).particle() ;
	report(DEBUG, kFacilityString) << doubleTag << endl;

	// Find index of matching D and Dbar in D block.
	tuple.d[tuple.nddcand] = -1 ;
	tuple.dbar[tuple.nddcand] = -1 ;

	for( int j = 0 ; j < tuple.ndcand ; ++j )
	{
	   if (//&doubleTag.taggedD().footPrint() == NULL ||
//	       &doubleTag.taggedD().footPrint() == NULL ||
	       &footPrintArray[j] == NULL ) {
	      cout << "Unexpected NULL" << endl;
	   }
	   if( doubleTag.taggedD().footPrint() == footPrintArray[ j ]
	       && doubleTag.taggedD().decayMode() == tuple.dmode[ j ] )
	   {
	      tuple.d[tuple.nddcand] = j ;
	   }
	   else if( doubleTag.taggedDbar().footPrint() == footPrintArray[ j ]
		    && doubleTag.taggedDbar().decayMode() == tuple.dmode[ j ] )
	   {
	      tuple.dbar[tuple.nddcand] = j ;
	   }
	}
	if (tuple.d[tuple.nddcand] < 0 || tuple.dbar[tuple.nddcand] < 0) {
	   report( WARNING, kFacilityString ) 
	      << "Failed to match double tag to D candidates" << endl;
	}

// 	tuple.ddmode[tuple.nddcand] = i ;
// 	tuple.cosangle[tuple.nddcand] = doubleTag.cosThetaFit() ;
// 	tuple.chi2vd[tuple.nddcand] = doubleTag.chi2VertexD() ;
// 	tuple.chi2vdb[tuple.nddcand] = doubleTag.chi2VertexDbar() ;
// 	tuple.chi2ed[tuple.nddcand] = doubleTag.chi2EnergyD() ;
// 	tuple.chi2edb[tuple.nddcand] = doubleTag.chi2EnergyDbar() ;
// 	tuple.chi2md[tuple.nddcand] = doubleTag.chi2MassD() ;
// 	tuple.chi2mdb[tuple.nddcand] = doubleTag.chi2MassDbar() ;
// 	tuple.chi2vddb[tuple.nddcand] = doubleTag.chi2VertexDDbar() ;

	tuple.cosangle[tuple.nddcand] = doubleTag.cosThetaFit(&*magField, &*labMomentum) ;
	tuple.chi2vd[tuple.nddcand] = doubleTag.chi2VertexD(&*magField, &*labMomentum) ;
	tuple.chi2vdb[tuple.nddcand] = doubleTag.chi2VertexDbar(&*magField, &*labMomentum) ;
	tuple.chi2ed[tuple.nddcand] = doubleTag.chi2EnergyD(&*magField, &*labMomentum) ;
	tuple.chi2edb[tuple.nddcand] = doubleTag.chi2EnergyDbar(&*magField, &*labMomentum) ;
	tuple.chi2md[tuple.nddcand] = doubleTag.chi2MassD(&*magField, &*labMomentum) ;
	tuple.chi2mdb[tuple.nddcand] = doubleTag.chi2MassDbar(&*magField, &*labMomentum) ;
	tuple.chi2vddb[tuple.nddcand] = doubleTag.chi2VertexDDbar(&*magField, &*labMomentum) ;

	++tuple.nddcand ;
     }
  }
  if( tuple.nddcand >= MAXNDDCAND )
  {
     report( NOTICE, kFacilityString ) 
	<< "Hard limit on number of DD candidates exceeded" << endl;
  }

   if (m_makeMCblock.value()) {
      FAItem< MCDecayTree > decaytree;
      extract( iFrame.record( Stream::kEvent ), decaytree );

      FATable< MCTrackTagsByMCParticle > trackTagsByParticle;
      extract( iFrame.record( Stream::kEvent ), trackTagsByParticle );

      FATable< MCCCTagsByMCParticle > showerTagsByParticle;
      extract( iFrame.record( Stream::kEvent ), showerTagsByParticle );

      MCCCPi0Tagger pi0Tagger(iFrame);
      MCCCEtaTagger etaTagger(iFrame);
      MCTKShortTagger kshortTagger(iFrame);

//      std::cout << *decaytree << std::endl;
      MCDecayTree::const_pIterator pEnd = (*decaytree).pEnd();
      for (MCDecayTree::const_pIterator pit = (*decaytree).pBegin();
	   pit != pEnd && tuple.nmcpart < MAXNMCPART; pit++) {
	 // We will store this particle if 
	 // (1) it had no production vertex
	 // (2) it arose from a decay (vertex type is kiDecay)
	 DABoolean usePart = false;
	 const MCVertex* prodVtx = (*pit).productionVertex();
	 if (! prodVtx) {
	    usePart = true;
	 } else if (prodVtx->type() == kiDecay) {
	    usePart = true;
	 } else if (prodVtx->type() == kiCleoIIGeantCompleteDecay) {
	    const HepPoint3D& decaypoint = prodVtx->position();
	    double radius = decaypoint.perp();
	    double z = decaypoint.z();
	    // A very cheap way of asking for a decay in the DR
	    if (radius < 0.79 && fabs(z) < 1.2) {
	       usePart = true;
	    }
	 }
	 if (! usePart) continue;
	 tuple.mcident[tuple.nmcpart] = (*pit).identifier();
	 tuple.mcpdgid[tuple.nmcpart] = (*pit).properties().PDGId();
	 if (prodVtx) {
	    tuple.mcparent[tuple.nmcpart] = indexInMCBlock(prodVtx->parent());
	 } else {
	    tuple.mcparent[tuple.nmcpart] = -1;
	 }
	 tuple.mce[tuple.nmcpart] = (*pit).energy();
	 tuple.mcpx[tuple.nmcpart] = (*pit).px();
	 tuple.mcpy[tuple.nmcpart] = (*pit).py();
	 tuple.mcpz[tuple.nmcpart] = (*pit).pz();
	 const std::string& partname = (*pit).properties().name();
	 tuple.mctruth[tuple.nmcpart] = -1;

	 if ((*pit).properties().charge() != 0) {
	    FATable< MCTrackTagsByMCParticle >::const_iterator trackTags = 
	       trackTagsByParticle.find((*pit).identifier());

	    // Tag object found
	    if (trackTags != trackTagsByParticle.end()) {
	       // There is a match
	       if (trackTags->isMatched()) {
		  // Grab the best-matched track  
		  Count trackId = trackTags->bestTrackID();
		  tuple.mctruth[tuple.nmcpart] = 
		     indexInTrackBlock(trackId);
	       }
	    }
	 } else if (partname == "gamma") {
	    FATable< MCCCTagsByMCParticle >::const_iterator showerTags = 
	       showerTagsByParticle.find((*pit).identifier());

	    // Tag object found
	    if (showerTags != showerTagsByParticle.end()) {
	       // There is a match
	       if (showerTags->isMatched()) {
		  // Grab the best-matched track  
		  Count showerId = showerTags->bestShowerId();
		  tuple.mctruth[tuple.nmcpart] = 
		     indexInShowerBlock(showerId);
	       }
	    }
	 } else if (partname == "pi0") {
	    const NavPi0ToGG* pi0ptr = pi0Tagger.matchNavPi0ToMCPi0(*pit);
	    if (pi0ptr) {
	       tuple.mctruth[tuple.nmcpart] = 
		  indexInPi0Block(*pi0ptr);
	    }
	 } else if (partname == "K_S0") {
	    const NavKs* ksptr = kshortTagger.matchNavKsToMCKs(*pit);
	    if (ksptr) {
	       tuple.mctruth[tuple.nmcpart] = 
		  indexInKsBlock(*ksptr);
	    }
	 }
	 tuple.nmcpart++;

	 if ((*pit).properties().name() == "D0" || 
	     (*pit).properties().name() == "D+") {
	    tuple.mcdmode = constructMCDmode(*pit);
	 }
	 if ((*pit).properties().name() == "anti-D0" || 
	     (*pit).properties().name() == "D-") {
	    tuple.mcdbmode = constructMCDmode(*pit);
	 }
      }
      if( tuple.nmcpart >= MAXNMCPART ) {
	 report( NOTICE, kFacilityString ) 
	    << "Hard limit on number of MC particles exceeded" << endl
	    << (*decaytree) ;
      }

      // Convert MC particle identifer in tuple.mcdmatch[] to MC block index
      for (SmallCount i = 0; i < tuple.ndcand; ++i) {
	if (tuple.mcdmatch[i] >= 0) {
	  const MCParticle& mcPart = decaytree->getParticle(tuple.mcdmatch[i]);
	  tuple.mcdmatch[i] = indexInMCBlock(mcPart);
	}
      }
   }

   // delete missing mass info
   if (missingMassObjects.pionList != NULL)
      delete missingMassObjects.pionList;
   if (missingMassObjects.pionListTrkEff != NULL)
      delete missingMassObjects.pionListTrkEff;
   if (missingMassObjects.kaonList != NULL)
      delete missingMassObjects.kaonList;
   if (missingMassObjects.kaonListTrkEff != NULL)
      delete missingMassObjects.kaonListTrkEff;
   if (missingMassObjects.pi0List != NULL)
      delete missingMassObjects.pi0List;
//   if (loosePi0table.getContents() != NULL) // Make sure this FATable is deleted.
//      delete loosePi0table.getContents();
   if (missingMassObjects.loosePi0List != NULL)
      delete missingMassObjects.loosePi0List;
   if (missingMassObjects.etaList != NULL)
      delete missingMassObjects.etaList;
   if (missingMassObjects.ksList != NULL)
      delete missingMassObjects.ksList;

   if (m_makeHbookNtuple.value())
      hbntupler.fill();
   if (m_makeRootNtuple.value())
      roontupler.fill();

   return ActionBase::kPassed;
}

int HadronicDNtupleProc::indexInKsBlock(const NavKs& kshort) {
   for (int i = 0; i < tuple.nks; i++) {
     //      if (kshort.identifier() == tuple.ksident[i]) {
     if (kshort.identifier() == static_cast<unsigned int>(tuple.ksident[i])) {
       return i;
     }
   }
   return -1;
}

int HadronicDNtupleProc::indexInPi0Block(const NavPi0ToGG& pi0) {
   for (int i = 0; i < tuple.npi0; i++) {
      if (pi0.identifier() == tuple.pi0ident[i]) {
	 return i;
      }
   }
   return -1;
}

int HadronicDNtupleProc::indexInEtaBlock(const NavEtaToGG& eta) {
   for (int i = 0; i < tuple.neta; i++) {
      if (eta.identifier() == tuple.etaident[i]) {
	 return i;
      }
   }
   return -1;
}

int HadronicDNtupleProc::indexInTrackBlock(const NavTrack& track) {
   for (int i = 0; i < tuple.ntrack; i++) {
     //      if (track.identifier() == tuple.trident[i]) {
     if (track.identifier() == static_cast<unsigned int>(tuple.trident[i])) {
	 return i;
      }
   }
   return -1;
}

int HadronicDNtupleProc::indexInTrackBlock(int trackid) {
   for (int i = 0; i < tuple.ntrack; i++) {
      if (trackid == tuple.trident[i]) {
	 return i;
      }
   }
   return -1;
}

int HadronicDNtupleProc::indexInShowerBlock(const NavShower& show) {
   for (int i = 0; i < tuple.nshow; i++) {
      if (show.identifier() == tuple.sident[i]) {
	 return i;
      }
   }
   return -1;
}

int HadronicDNtupleProc::indexInShowerBlock(int showid) {
   for (int i = 0; i < tuple.nshow; i++) {
      if (showid == tuple.sident[i]) {
	 return i;
      }
   }
   return -1;
}
int HadronicDNtupleProc::indexInMCBlock(const MCParticle& mcpart) {
   for (int i = 0; i < tuple.nmcpart; i++) {
       //      if (mcpart.identifier() == tuple.mcident[i]) {
     if (mcpart.identifier() == static_cast<unsigned int>(tuple.mcident[i])) {
	 return i;
      }
   }
   return -1;
}

int HadronicDNtupleProc::constructMCDmode(const MCParticle& mcpart) {
// definition of decay mode:
// 1*(#K-) + 10*(#K+) + 100*(#K0) + 1000*(#pi-) + 10000*(#pi+)
// + 100000*(#pi0) + 1000000*(#gamma)
// + 10000000*(#leptons) + 100000000*(#anything else)
   int retval = 0;
   const std::string& partname = mcpart.properties().name();
   if (partname == "K-") {
      retval += 1;
   } else if (partname == "K+") {
      retval += 10;
   } else if (partname == "K_S0" ||
	      partname == "K_L0") {
      retval += 100;
   } else if (partname == "pi-") {
      retval += 1000;
   } else if (partname == "pi+") {
      retval += 10000;
   } else if (partname == "pi0") {
      retval += 100000;
   } else if (partname == "gamma") {
      retval += 1000000;
   } else {
      if (mcpart.properties().lepton() || mcpart.properties().neutrino()) {
	 retval += 10000000;
      } else {
	 const MCVertex* deathVtx = mcpart.deathVertex();
	 assert (deathVtx != NULL);
	 if (deathVtx->type() != kiDecay) {
	    retval += 100000000;
	 } else {
	    MCVertex::const_pIterator vpEnd = (*deathVtx).pEnd();
	    for (MCVertex::const_pIterator vpit = (*deathVtx).pBegin();
		 vpit != vpEnd; vpit++) {
	       retval += constructMCDmode(*vpit);
	    }
	 }
      }
   }
   return retval;
}


bool HadronicDNtupleProc::isType1Pi0(const NavPi0ToGG& pi0) {
   const NavShower& hishower = pi0.hiEnShower();
   const NavShower& loshower = pi0.loEnShower();
   if (hishower.distance(loshower) < 0.25*k_m) {
      return (hishower.attributes().e9oe25UnfOK() &&
	      loshower.attributes().e9oe25UnfOK());
   } else {
      return (hishower.attributes().e9oe25OK() &&
	      loshower.attributes().e9oe25OK());
   }
}


/*
ActionBase::ActionResult
HadronicDNtupleProc::beginRun( Frame& iFrame )       // anal2 equiv.
{
   report( DEBUG, kFacilityString ) << "here in beginRun()" << endl;

   return ActionBase::kPassed;
}
*/

/*
ActionBase::ActionResult
HadronicDNtupleProc::endRun( Frame& iFrame )         // anal4 equiv.
{
   report( DEBUG, kFacilityString ) << "here in endRun()" << endl;

   return ActionBase::kPassed;
}
*/

//
// const member functions
//

//
// static member functions
//
