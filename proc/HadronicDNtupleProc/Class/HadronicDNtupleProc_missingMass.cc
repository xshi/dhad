// -*- C++ -*-
//
// Package:     HadronicDNtupleProc
// Module:      HadronicDNtupleProc_missingMass
// 
// Description: <one line class summary>
//
// Implementation:
//     <Notes on implementation>
//
// Author:      Peter Onyisi
// Created:     Sometime in April 2005
// $Id$
//
// Revision history
//
// $Log$
// Revision 1.1  2010/05/17 17:30:18  xs32
// Add
//
// Revision 1.2  2009/04/29 19:52:54  xs32
// first compile OK.
//
// Revision 1.2  2006/02/01 17:56:58  srs63
// Added missing mass modes: 7 - pi0 from D0->Kspi0pi0, 14 - mode 4 with loose pi0s, 17 - mode 7 with loose pi0s
//
// Revision 1.1  2005/08/30 19:20:54  ponyisi
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
#include "Experiment/Experiment.h"
#include "Experiment/units.h"
#include "Experiment/report.h"

#include "HadronicDNtupleProc/HadronicDNtupleProc.h"
#include "LabNet4Momentum/LabNet4Momentum.h"
#include "PhotonDecays/PhdPi0.h"
#include "Navigation/NavTrack.h"

#include "DChain/List/Template/DCDecayList.cc"
#include "DTag/DTagList.h"
#include "DTag/DTagDecayModes.h"
#include "DTag/DTagUtilities.h"
#include "DDoubleTag/DDoubleTag.h"
#include "DDoubleTag/DDoubleTagList.h"
#include "CleoDChain/CDPi0.h"
#include "CleoDChain/CDKs.h"
#include "CleoDChain/CDEta.h"

static const char* const kFacilityString = "Processor.HadronicDNtupleProc" ;

static DABoolean goodTrack(const NavTrack& track, const DBCandidate::Hypo hypo){

  //FAItem< TRSeedTrackQuality > SeedQual = track.seedQuality();
  //if( (*SeedQual).originUsed() ) return false;
  //if( (*SeedQual).numberHitsExpected() == 0 ) return false;

  FAItem< TRTrackFitQuality > FitQual = track.quality(hypo);
  //if( (*FitQual).fitAbort() ) return false;
  if( (*FitQual).chiSquare() > 100000.0 ) return false;
  //if( (*FitQual).chiSquare() <= 0.0 ) return false;
  //if( (*FitQual).ratioNumberHitsToExpected() < 0.5 ) return false;
  int hits=(*FitQual).numberHits();
  int ehits=(*FitQual).numberHitsExpected();
  float fhits=(float) hits;
  float efhits=(float) ehits;
  float frac=0;
  if(efhits>0){frac=fhits/efhits;}

  if (frac<0.5) return false;

  //FAItem< TDKinematicFit > Fit=track.kinematicFit(hypo);
  //if ( (*Fit).pmag() < 50.0*k_MeV ) return false;
  //if ( (*Fit).pmag() > 2.0*k_GeV ) return false;
  //if ( fabs((*Fit).momentum().cosTheta()) > 0.93 ) return false;

  FAItem< TRHelixFit > Helix=track.helixFit(hypo);
  if ( fabs((*Helix).d0() ) > 5*k_mm ) return false;
  if ( fabs((*Helix).z0() ) > 5*k_cm ) return false;

  return true;
}

DChainBoolean pionSelector( CDChargedPion& iPion ) {

  if (! goodTrack (iPion.track(), iPion.hypo() )) return false;

  return true;

}

DChainBoolean kaonSelector( CDChargedKaon& iKaon ) {

  if (! goodTrack (iKaon.track(), iKaon.hypo() )) return false;

  return true;

}

//DChainBoolean loosePi0Selector( CDPi0& iPi0 )
//{
//	double pi0Mass = iPi0.pi0().unconMass();
//	if ( pi0Mass > m_loosePi0MinMass.value() && pi0Mass < m_loosePi0MaxMass.value() ) return true;
//	else return false;
//}

/*FATable< NavPi0ToGG > TurnPhdPi0sIntoNavPi0ToGGs(FATable< PhdPi0 > loosePi0table)
{
	FAPtrTable< NavPi0ToGG > * pointerTable = new FAPtrTable();
	FATable::const_iterator PhdPi0Itr = loosePi0table.begin();
	for ( ; PhdPi0Itr != loosePi0table.end(); PhdPi0Itr++)
	{
		PhDPi0 thisPhdPi0 = *PhdPi0Itr;
		NavShower* hiEnShower = FindShowerWithIdentifier(thisPhDPi0.hiEnId());
		NavShower* loEnShower = FindShowerWithIdentifier(thisPhDPi0.loEnId());
		pointerTable.insert(new NavPi0ToGG(&thisPhdPi0, hiEnShower, loEnShower);
	}
	return FATable< NavPi0ToGG >(pointerTable);
}*/

class RecoilCandSelector: public DCSelectionFunction< CDDecay >{

 public:
  RecoilCandSelector(int modemin,int modemax,double m2missmin,double m2missmax,int modenumber,const LabNet4Momentum* labmomentum)
  {
    m_modemin=modemin;
    m_modemax=modemax;
    m_m2missmin=m2missmin;
    m_m2missmax=m2missmax;
    m_modenumber=modenumber;
    m_labmomentum=labmomentum;
  }

  bool operator()( CDDecay& aRecoilCand ) {

    //cout << "In selector"<<endl;

    int nrecoilpart=0;

    if (m_modenumber==0) nrecoilpart=1;
    if (m_modenumber==1) nrecoilpart=1;
    if (m_modenumber==2) nrecoilpart=2;
    if (m_modenumber==3) nrecoilpart=2;
    if (m_modenumber==4) nrecoilpart=1;
    if (m_modenumber==14) nrecoilpart=1;
    if (m_modenumber==7) nrecoilpart=2;
    if (m_modenumber==17) nrecoilpart=2;
    if (m_modenumber==5) nrecoilpart=1;
    if (m_modenumber==6) nrecoilpart=2;

    if (m_modenumber==100) nrecoilpart=1;
    if (m_modenumber==101) nrecoilpart=1;
    if (m_modenumber==102) nrecoilpart=2;
    if (m_modenumber==103) nrecoilpart=2;

    assert(nrecoilpart!=0);

    //const CDDecay& recoilCand = aRecoilCand.particle();

    const DTag& tagDecay =
      dynamic_cast<const DTag&>(aRecoilCand.child((DCChildren::Position)nrecoilpart).decay());

    //cout << "decayMode():"<<tagDecay.decayMode()<<endl;

    //cout << "Could leave..."<<endl;

    if (tagDecay.decayMode()>m_modemax) return false;
    if (tagDecay.decayMode()<m_modemin) return false;

    //cout << "Still in..."<<endl;

    HepLorentzVector p4=aRecoilCand.kinematicData().lorentzMomentum()-
      tagDecay.kinematicData().lorentzMomentum();

    double mmissq=DTagUtilities::m2miss(tagDecay,
					p4,
					*m_labmomentum);

    //cout << "mmissq:"<<mmissq<<endl;

    //cout << "Will leave..."<<endl;


    return (mmissq>m_m2missmin)&&(mmissq<m_m2missmax);

  }

 private:

  double m_m2missmin;
  double m_m2missmax;
  int m_modemin;
  int m_modemax;
  int m_modenumber;
  const LabNet4Momentum* m_labmomentum;

};



void HadronicDNtupleProc::makeMissingMassStage1(const DTagList& DTags, const LabNet4Momentum& labMomentum) {

   
      //cout << "Here 1"<<endl;
      if (missingMassObjects.fullyreco == NULL) {
	 missingMassObjects.fullyreco = new vector<CDDecayList*>();
      }
      if (missingMassObjects.recoils == NULL) {
	 missingMassObjects.recoils = new vector<pair<CDDecayList*,int>* >();
      }

      vector<pair<CDDecayList*,int>* >& recoils = *missingMassObjects.recoils;
      vector<CDDecayList*>& fullyreco = *missingMassObjects.fullyreco;

      for (int irecoil=0;irecoil<recoils.size();irecoil++){
	 delete fullyreco[irecoil];
	 delete (*recoils[irecoil]).first;
	 delete recoils[irecoil];
      }

      fullyreco.clear();
      recoils.clear();

      CDDecayList *recoillist;
      CDDecayList *fullyrecolist;

      bool usePID=false;

      //cout << "Will make mode 0"<<endl;

      //mode 0 K+
      RecoilCandSelector Mode0(0,99,-0.5,0.5,0,&labMomentum);
      recoillist=new CDDecayList(Mode0);
      (*recoillist)=missingMassObjects.kaonList->plus()*DTags;
      recoils.push_back(new pair<CDDecayList*,int>(recoillist,0));
      fullyrecolist=new CDDecayList;
      if (usePID){
	(*fullyrecolist)=(*recoillist)*missingMassObjects.pionList->minus();
      }
      else {
	(*fullyrecolist)=(*recoillist)*missingMassObjects.pionListTrkEff->minus();
      }
      fullyreco.push_back(fullyrecolist);

      //cout << "Will make mode 1"<<endl;

      //mode 1 pi-
      RecoilCandSelector Mode1(0,99,-0.5,0.7,1,&labMomentum);
      recoillist=new CDDecayList(Mode1);
      (*recoillist)=missingMassObjects.pionList->minus()*DTags;
      recoils.push_back(new pair<CDDecayList*,int>(recoillist,1));
      fullyrecolist=new CDDecayList;
      if (usePID) {
	(*fullyrecolist)=(*recoillist)*missingMassObjects.kaonList->plus();
      }
      else {
	(*fullyrecolist)=(*recoillist)*missingMassObjects.kaonListTrkEff->plus();
      }
      fullyreco.push_back(fullyrecolist);

      //cout << "Will make mode 2"<<endl;

      //mode 2 K+ pi0
      RecoilCandSelector Mode2(0,99,-0.5,0.5,2,&labMomentum);
      recoillist=new CDDecayList(Mode2);
      (*recoillist)=missingMassObjects.kaonList->plus()*(*missingMassObjects.pi0List)*DTags;
      recoils.push_back(new pair<CDDecayList*,int>(recoillist,2));
      fullyrecolist=new CDDecayList;
      if (usePID){
	(*fullyrecolist)=(*recoillist)*missingMassObjects.pionList->minus();
      }
      else {
	(*fullyrecolist)=(*recoillist)*missingMassObjects.pionListTrkEff->minus();
      }
      fullyreco.push_back(fullyrecolist);

      //cout << "Will make mode 3"<<endl;

      //mode 3 pi- pi0
      RecoilCandSelector Mode3(0,99,-0.5,0.7,3,&labMomentum);
      recoillist=new CDDecayList(Mode3);
      (*recoillist)=missingMassObjects.pionList->minus()*(*missingMassObjects.pi0List)*DTags;
      recoils.push_back(new pair<CDDecayList*,int>(recoillist,3));
      fullyrecolist=new CDDecayList;
      if (usePID) {
	(*fullyrecolist)=(*recoillist)*missingMassObjects.kaonList->plus();
      }
      else {
	(*fullyrecolist)=(*recoillist)*missingMassObjects.kaonListTrkEff->plus();
      }
      fullyreco.push_back(fullyrecolist);

      //cout << "Will make mode 4"<<endl;

      //mode 4 ks
      RecoilCandSelector Mode4(0,99,-0.5,0.5,4,&labMomentum);
      recoillist=new CDDecayList(Mode4);
      (*recoillist)=(*missingMassObjects.ksList)*DTags;
      recoils.push_back(new pair<CDDecayList*,int>(recoillist,4));
      fullyrecolist=new CDDecayList;
      (*fullyrecolist)=(*recoillist)*(*missingMassObjects.pi0List);
      fullyreco.push_back(fullyrecolist);

      //mode 14 ks combined with loose pi0
      RecoilCandSelector Mode14(0,99,-0.5,0.5,14,&labMomentum);
      recoillist=new CDDecayList(Mode14);
      (*recoillist)=(*missingMassObjects.ksList)*DTags;
      recoils.push_back(new pair<CDDecayList*,int>(recoillist,14));
      fullyrecolist=new CDDecayList;
      (*fullyrecolist)=(*recoillist)*(*missingMassObjects.loosePi0List);
      fullyreco.push_back(fullyrecolist);

      //mode 7 ks pi0
      RecoilCandSelector Mode7(0,99,-0.5,0.5,7,&labMomentum);
      recoillist=new CDDecayList(Mode7);
      (*recoillist)=(*missingMassObjects.ksList)*(*missingMassObjects.pi0List)*DTags;
      recoils.push_back(new pair<CDDecayList*,int>(recoillist,7));
      fullyrecolist=new CDDecayList;
      (*fullyrecolist)=(*recoillist)*(*missingMassObjects.pi0List);
      fullyreco.push_back(fullyrecolist);

      //mode 17 ks pi0 combined with loose pi0
      RecoilCandSelector Mode17(0,99,-0.5,0.5,17,&labMomentum);
      recoillist=new CDDecayList(Mode17);
      (*recoillist)=(*missingMassObjects.ksList)*(*missingMassObjects.pi0List)*DTags;
      recoils.push_back(new pair<CDDecayList*,int>(recoillist,17));
      fullyrecolist=new CDDecayList;
      (*fullyrecolist)=(*recoillist)*(*missingMassObjects.loosePi0List);
      fullyreco.push_back(fullyrecolist);

      //cout << "Will make mode 5"<<endl;

      //mode 5 pi0
      RecoilCandSelector Mode5(0,99,-0.5,0.7,5,&labMomentum);
      recoillist=new CDDecayList(Mode5);
      (*recoillist)=(*missingMassObjects.pi0List)*DTags;
      recoils.push_back(new pair<CDDecayList*,int>(recoillist,5));
      fullyrecolist=new CDDecayList;
      (*fullyrecolist)=(*recoillist)*(*missingMassObjects.ksList);
      fullyreco.push_back(fullyrecolist);

      //cout << "Will make mode 6"<<endl;

      //mode 6 pi+ pi-
      RecoilCandSelector Mode6(0,99,-0.5,0.7,6,&labMomentum);
      recoillist=new CDDecayList(Mode6);
      (*recoillist)=missingMassObjects.pionList->plus()*missingMassObjects.pionList->minus()*DTags;
      recoils.push_back(new pair<CDDecayList*,int>(recoillist,6));
      fullyrecolist=new CDDecayList;
      (*fullyrecolist)=(*recoillist)*(*missingMassObjects.ksList);
      fullyreco.push_back(fullyrecolist);

      //cout << "Will make mode 100"<<endl;

      //mode 100 pi-
      RecoilCandSelector Mode100(200,299,-0.5,0.7,100,&labMomentum);
      recoillist=new CDDecayList(Mode100);
      (*recoillist)=missingMassObjects.pionList->minus()*DTags;
      recoils.push_back(new pair<CDDecayList*,int>(recoillist,100));
      fullyrecolist=new CDDecayList;
      (*fullyrecolist)=(*recoillist)*(*missingMassObjects.ksList);
      fullyreco.push_back(fullyrecolist);

      //cout << "Will make mode 101"<<endl;

      //mode 101 ks
      RecoilCandSelector Mode101(200,299,-0.5,0.5,101,&labMomentum);
      recoillist=new CDDecayList(Mode101);
      (*recoillist)=(*missingMassObjects.ksList)*DTags;
      recoils.push_back(new pair<CDDecayList*,int>(recoillist,101));
      fullyrecolist=new CDDecayList;
      if (usePID){
	(*fullyrecolist)=(*recoillist)*missingMassObjects.pionList->plus();
      }
      else{
	(*fullyrecolist)=(*recoillist)*missingMassObjects.pionListTrkEff->plus();
      }
      fullyreco.push_back(fullyrecolist);

      //cout << "Will make mode 102"<<endl;

      //mode 102 pi- pi-
      RecoilCandSelector Mode102(200,299,-0.5,0.7,102,&labMomentum);
      recoillist=new CDDecayList(Mode102);
      (*recoillist)=missingMassObjects.pionList->minus()*missingMassObjects.pionList->minus()*DTags;
      recoils.push_back(new pair<CDDecayList*,int>(recoillist,102));
      fullyrecolist=new CDDecayList;
      if (usePID) {
	(*fullyrecolist)=(*recoillist)*missingMassObjects.kaonList->plus();
      }
      else {
	(*fullyrecolist)=(*recoillist)*missingMassObjects.kaonListTrkEff->plus();
      }
      fullyreco.push_back(fullyrecolist);

      //cout << "Will make mode 103"<<endl;

      //mode 103 K+ pi-
      RecoilCandSelector Mode103(200,299,-0.5,0.5,103,&labMomentum);
      recoillist=new CDDecayList(Mode103);
      (*recoillist)=missingMassObjects.kaonList->plus()*missingMassObjects.pionList->minus()*DTags;
      recoils.push_back(new pair<CDDecayList*,int>(recoillist,103));
      fullyrecolist=new CDDecayList;
      if (usePID) {
	(*fullyrecolist)=(*recoillist)*missingMassObjects.pionList->minus();
      }
      else {
	(*fullyrecolist)=(*recoillist)*missingMassObjects.pionListTrkEff->minus();
      }
      fullyreco.push_back(fullyrecolist);
}

void HadronicDNtupleProc::makeMissingMassStage2(const DTag& tagd, const LabNet4Momentum& labMomentum) {
   if (missingMassObjects.fullyreco == NULL) {
      missingMassObjects.fullyreco = new vector<CDDecayList*>();
      report(EMERGENCY, kFacilityString) 
	 << "fullyreco should already exist at this point" << endl;
   }
   if (missingMassObjects.recoils == NULL) {
      missingMassObjects.recoils = new vector<pair<CDDecayList*,int>* >();
      report(EMERGENCY, kFacilityString) 
	 << "recoils should already exist at this point" << endl;
   }
   
   vector<pair<CDDecayList*,int>* >& recoils = *missingMassObjects.recoils;
   vector<CDDecayList*>& fullyreco = *missingMassObjects.fullyreco;
   
   int irecoil=0;
	 
   for (irecoil=0;irecoil<recoils.size();irecoil++){
      
      CDDecayList& RecoilList=*((*recoils[irecoil]).first);
      int mode=(*recoils[irecoil]).second;
      
      int nrecoilpart=0;
      
      if (mode==0) nrecoilpart=1;
      if (mode==1) nrecoilpart=1;
      if (mode==2) nrecoilpart=2;
      if (mode==3) nrecoilpart=2;
      if (mode==4) nrecoilpart=1;
      if (mode==14) nrecoilpart=1;
      if (mode==7) nrecoilpart=2;
      if (mode==17) nrecoilpart=2;
      if (mode==5) nrecoilpart=1;
      if (mode==6) nrecoilpart=2;

      if (mode==100) nrecoilpart=1;
      if (mode==101) nrecoilpart=1;
      if (mode==102) nrecoilpart=2;
      if (mode==103) nrecoilpart=2;

      assert(nrecoilpart!=0);

	   
      CDDecayList::iterator recoilEnd = RecoilList.particle_end();
      CDDecayList::iterator recoil = RecoilList.particle_begin();
      for( ; recoil != recoilEnd; ++recoil ){

	 const CDDecay& recoilCand = (*recoil).particle();
	 
	 const DTag& tagDecay = 
	    dynamic_cast<const DTag&>(recoilCand.child((DCChildren::Position)nrecoilpart).decay());

	 if ((&tagDecay)!=(&(tagd))) continue;
	     
	 HepLorentzVector p4recoil;

	 int index1=-1;
	 int index2=-1;

	 switch (mode) {
	    case 0:
	    {
	       const NavTrack& kaon = recoilCand.child(DCChildren::First).track();
	       p4recoil=kaon.kaonFit()->lorentzMomentum();
	       index1=indexInTrackBlock(kaon);
	    }
	    break;
	    case 1:
	    {
		 const NavTrack& pion = recoilCand.child(DCChildren::First).track();
		 p4recoil=pion.pionFit()->lorentzMomentum();
		 index1=indexInTrackBlock(pion);
	    }
	    break;
	     case 2:
	     {
		const NavTrack& kaon = recoilCand.child(DCChildren::First).track();
		const NavPi0ToGG& pi0 = recoilCand.child(DCChildren::Second).navPi0();
		p4recoil=kaon.kaonFit()->lorentzMomentum()+
		   pi0.pi0().lorentzMomentum();
		index1=indexInTrackBlock(kaon);
		index2=indexInPi0Block(pi0);
	     }	       
	     break;
	    case 3:
	    {
	       const NavTrack& pion = recoilCand.child(DCChildren::First).track();
	       const NavPi0ToGG& pi0 = recoilCand.child(DCChildren::Second).navPi0();
	       p4recoil=pion.pionFit()->lorentzMomentum()+
		  pi0.pi0().lorentzMomentum();
	       index1=indexInTrackBlock(pion);
	       index2=indexInPi0Block(pi0);
	    }
	    break;
	    case 4:
	    case 14:
	    {
	       const NavKs& ks = recoilCand.child(DCChildren::First).navKshort();
	       p4recoil=ks.kShort().lorentzMomentum();
	       index1=indexInKsBlock(ks);
	    }
		 break;
		 case 7:
	    case 17:
	    {
	       const NavKs& ks = recoilCand.child(DCChildren::First).navKshort();
          const NavPi0ToGG& pi0 = recoilCand.child(DCChildren::Second).navPi0();
	       p4recoil=ks.kShort().lorentzMomentum() + pi0.pi0().lorentzMomentum();
	       index1=indexInKsBlock(ks);
          index2=indexInPi0Block(pi0);
	    }
	    break;
	    case 5:
	    {
	       const NavPi0ToGG& pi0 = recoilCand.child(DCChildren::First).navPi0();
	       p4recoil=pi0.pi0().lorentzMomentum();
	       index1=indexInPi0Block(pi0);
	    }
	    break;
	    case 6:
	    {
	       const NavTrack& pion1 = recoilCand.child(DCChildren::First).track();
	       const NavTrack& pion2 = recoilCand.child(DCChildren::Second).track();
	       p4recoil=pion1.pionFit()->lorentzMomentum()+
		  pion2.pionFit()->lorentzMomentum();
	       index1=indexInTrackBlock(pion1);
	       index2=indexInTrackBlock(pion2);
	    }
	    break;
	    case 100:
	    {
	       const NavTrack& pion = recoilCand.child(DCChildren::First).track();
	       p4recoil=pion.pionFit()->lorentzMomentum();
	       index1=indexInTrackBlock(pion);
	    }
	    break;
	    case 101:
	    {
	       const NavKs& ks = recoilCand.child(DCChildren::First).navKshort();
	       p4recoil=ks.kShort().lorentzMomentum();
	       index1=indexInKsBlock(ks);
	    }
	    break;
	    case 102:
	    {
	       const NavTrack& pion1 = recoilCand.child(DCChildren::First).track();
	       const NavTrack& pion2 = recoilCand.child(DCChildren::Second).track();
	       p4recoil=pion1.pionFit()->lorentzMomentum()+
		  pion2.pionFit()->lorentzMomentum();
	       index1=indexInTrackBlock(pion1);
	       index2=indexInTrackBlock(pion2);
	    }
	    break;
	    case 103:
	    {
	       const NavTrack& kaon = recoilCand.child(DCChildren::First).track();
	       const NavTrack& pion = recoilCand.child(DCChildren::Second).track();
	       p4recoil=kaon.kaonFit()->lorentzMomentum()+
		  pion.pionFit()->lorentzMomentum();
	       index1=indexInTrackBlock(kaon);
	       index2=indexInTrackBlock(pion);
	    }
	    break;
	    default:
	       cout << "mode:"<<mode<<endl;
	       assert(0);
	 }
	 
	 assert(index1!=-1);
	 
	 double mmissq=DTagUtilities::m2miss(tagDecay,
					     p4recoil,
					     labMomentum);
	 
	 
	 double bestmbc=0.0;
	 
	 CDDecayList::iterator fullrecoEnd = fullyreco[irecoil]->particle_end();
	 CDDecayList::iterator fullreco = fullyreco[irecoil]->particle_begin();
	 for( ; fullreco != fullrecoEnd; ++fullreco ){
	    
	    
	    const CDDecay& fullrecoCand = (*fullreco).particle();
	    
	    if (&recoilCand!=&(fullrecoCand.child(DCChildren::First).decay().decay())) continue;
	    
	    
	    HepLorentzVector p4particle;
	    
	    switch (mode) {
	       case 0:
	       case 2:
	       case 101:
	       case 103:
	       {
		  const NavTrack& pion = fullrecoCand.child(DCChildren::Second).track();
		  p4particle=pion.pionFit()->lorentzMomentum();
	       }
	       break;
	       case 1:
	       case 3:
	       case 102:
	       {
		  const NavTrack& kaon = fullrecoCand.child(DCChildren::Second).track();
		  p4particle=kaon.kaonFit()->lorentzMomentum();
	       }
	       break;
	       case 4:
	       case 14:
			 case 7:
			 case 17:
	       {
		  const NavPi0ToGG& pi0 = fullrecoCand.child(DCChildren::Second).navPi0();
		  p4particle=pi0.pi0().lorentzMomentum();
	       }
	       break;
	       case 5:
               case 6:
	       case 100:
	       {
		  const NavKs& ks = fullrecoCand.child(DCChildren::Second).navKshort();
		  p4particle=ks.kShort().lorentzMomentum();
	       }
	       break;
	       
	       default:
		  cout << "Unknown mode:"<<mode<<endl;
		  assert(0);
	    }
	    
	    
	    HepLorentzVector p4D=p4recoil+p4particle;
	    
	    if (fabs(p4D.t()-0.5*labMomentum.t())>0.05) continue;
	    
	    double mbc=sqrt(0.25*labMomentum.t()*labMomentum.t()-p4D.rho()*p4D.rho());
	    
	    if (fabs(mbc-tagDecay.nominalMass())<
		fabs(bestmbc-tagDecay.nominalMass())){
	       bestmbc=mbc;
	    }
	    
	 }
	 
	 tuple.mdcand[tuple.nmiss]=tuple.ndcand;
	 tuple.mmode[tuple.nmiss]=mode;
	 tuple.mtrack1[tuple.nmiss]=index1;
	 tuple.mtrack2[tuple.nmiss]=index2;
	 tuple.mmsq[tuple.nmiss]=mmissq;
	 
	 tuple.mpx[tuple.nmiss]=labMomentum.x()-p4recoil.x()-tagd.kinematicData().lorentzMomentum().x();
	 tuple.mpy[tuple.nmiss]=labMomentum.y()-p4recoil.y()-tagd.kinematicData().lorentzMomentum().y();
	 tuple.mpz[tuple.nmiss]=labMomentum.z()-p4recoil.z()-tagd.kinematicData().lorentzMomentum().z();
	 tuple.me[tuple.nmiss]=labMomentum.t()-p4recoil.t()-tagd.kinematicData().lorentzMomentum().t();
	 tuple.mbestmbc[tuple.nmiss]=bestmbc;
	 
	 tuple.nmiss++;
	 
	 if (tuple.nmiss>=10000) {
	    report( NOTICE, kFacilityString ) 
	       <<"To many missing masses"<<endl;
	    tuple.nmiss=9999;
	 }
	 
      }
      
   }
}
