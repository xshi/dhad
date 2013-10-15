//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Wed Jun 16 12:18:02 2010 by ROOT version 4.03/04
// from TChain dnt/
//////////////////////////////////////////////////////////

#ifndef DNTClass_h
#define DNTClass_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>

class DNTClass {
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

   // Declaration of leave types
   Int_t           run;
   Int_t           event;
   Float_t         ecm;
   Float_t         xangle;
   Float_t         eneu;
   Float_t         echg;
   Float_t         evtmm2;
   Int_t           l1trig;
   Int_t           nbunch;
   Int_t           bunch;
   Int_t           l1trig2;
   Float_t         pxcm;
   Float_t         pycm;
   Float_t         pzcm;
   Int_t           ntrack;
   Int_t           trident[23];   //[ntrack]
   Float_t         trpie[23];   //[ntrack]
   Float_t         trpipx[23];   //[ntrack]
   Float_t         trpipy[23];   //[ntrack]
   Float_t         trpipz[23];   //[ntrack]
   Float_t         trpip[23];   //[ntrack]
   Float_t         trke[23];   //[ntrack]
   Float_t         trkpx[23];   //[ntrack]
   Float_t         trkpy[23];   //[ntrack]
   Float_t         trkpz[23];   //[ntrack]
   Float_t         trchg[23];   //[ntrack]
   Float_t         trz0[23];   //[ntrack]
   Float_t         trd0[23];   //[ntrack]
   Float_t         trcosth[23];   //[ntrack]
   Float_t         trphi0[23];   //[ntrack]
   Float_t         trdrhitf[23];   //[ntrack]
   Float_t         trzdhitf[23];   //[ntrack]
   Float_t         trhitf[23];   //[ntrack]
   Float_t         trchi2[23];   //[ntrack]
   Int_t           trchi2dof[23];   //[ntrack]
   Float_t         trsigpi[23];   //[ntrack]
   Float_t         trsigk[23];   //[ntrack]
   Float_t         trrichpll[23];   //[ntrack]
   Int_t           trrichpnp[23];   //[ntrack]
   Float_t         trrichkll[23];   //[ntrack]
   Int_t           trrichknp[23];   //[ntrack]
   Int_t           trtaginfo[23];   //[ntrack]
   Int_t           trfabort[23];   //[ntrack]
   Int_t           trrichphp[23];   //[ntrack]
   Int_t           trrichkhp[23];   //[ntrack]
   Float_t         trdb[23];   //[ntrack]
   Float_t         trdpthmu[23];   //[ntrack]
   Float_t         trroceid[23];   //[ntrack]
   Int_t           trtrkman[23];   //[ntrack]
   Int_t           nshow;
   Int_t           sident[44];   //[nshow]
   Float_t         se[44];   //[nshow]
   Float_t         spx[44];   //[nshow]
   Float_t         spy[44];   //[nshow]
   Float_t         spz[44];   //[nshow]
   Float_t         sphi[44];   //[nshow]
   Float_t         scosth[44];   //[nshow]
   Int_t           se9o25uok[44];   //[nshow]
   Int_t           shot[44];   //[nshow]
   Int_t           sdettype[44];   //[nshow]
   Int_t           strmatch[44];   //[nshow]
   Float_t         strme[44];   //[nshow]
   Float_t         strdist[44];   //[nshow]
   Float_t         se9o25[44];   //[nshow]
   Float_t         se9o25u[44];   //[nshow]
   Int_t           npi0;
   Int_t           pi0ident[27];   //[npi0]
   Float_t         pi0mass[27];   //[npi0]
   Float_t         pi0chi2[27];   //[npi0]
   Float_t         pi0e[27];   //[npi0]
   Float_t         pi0px[27];   //[npi0]
   Float_t         pi0py[27];   //[npi0]
   Float_t         pi0pz[27];   //[npi0]
   Float_t         pi0merr[27];   //[npi0]
   Int_t           pi0dau1[27];   //[npi0]
   Int_t           pi0dau2[27];   //[npi0]
   Int_t           pi0istype1[27];   //[npi0]
   Int_t           neta;
   Int_t           etaident[8];   //[neta]
   Float_t         etamass[8];   //[neta]
   Float_t         etachi2[8];   //[neta]
   Float_t         etae[8];   //[neta]
   Float_t         etapx[8];   //[neta]
   Float_t         etapy[8];   //[neta]
   Float_t         etapz[8];   //[neta]
   Float_t         etamerr[8];   //[neta]
   Int_t           etadau1[8];   //[neta]
   Int_t           etadau2[8];   //[neta]
   Int_t           nks;
   Int_t           ksident[11];   //[nks]
   Float_t         ksmass[11];   //[nks]
   Float_t         kse[11];   //[nks]
   Float_t         kspx[11];   //[nks]
   Float_t         kspy[11];   //[nks]
   Float_t         kspz[11];   //[nks]
   Float_t         kschi2[11];   //[nks]
   Float_t         ksrad[11];   //[nks]
   Float_t         ksraderr[11];   //[nks]
   Int_t           ksdau1[11];   //[nks]
   Int_t           ksdau2[11];   //[nks]
   Float_t         ksflsig[11];   //[nks]
   Int_t           ndcand;
   Int_t           dmode[103];   //[ndcand]
   Float_t         dmbc[103];   //[ndcand]
   Float_t         ddeltae[103];   //[ndcand]
   Float_t         ddeltaeerr[103];   //[ndcand]
   Float_t         dmraw[103];   //[ndcand]
   Float_t         dmrawerr[103];   //[ndcand]
   Float_t         dkchi2[103];   //[ndcand]
   Float_t         de[103];   //[ndcand]
   Float_t         dpx[103];   //[ndcand]
   Float_t         dpy[103];   //[ndcand]
   Float_t         dpz[103];   //[ndcand]
   Int_t           ddau1[103];   //[ndcand]
   Int_t           ddau2[103];   //[ndcand]
   Int_t           ddau3[103];   //[ndcand]
   Int_t           ddau4[103];   //[ndcand]
   Int_t           dcsign[103];   //[ndcand]
   Int_t           lepveto[103];   //[ndcand]
   Int_t           ddau5[103];   //[ndcand]
   Int_t           nmiss;
   Int_t           mmode[0];   //[nmiss]
   Int_t           mdcand[0];   //[nmiss]
   Int_t           mtrack1[0];   //[nmiss]
   Int_t           mtrack2[0];   //[nmiss]
   Float_t         mmsq[0];   //[nmiss]
   Float_t         mpx[0];   //[nmiss]
   Float_t         mpy[0];   //[nmiss]
   Float_t         mpz[0];   //[nmiss]
   Float_t         me[0];   //[nmiss]
   Float_t         mbestmbc[0];   //[nmiss]
   Int_t           nddcand;
   Int_t           d[113];   //[nddcand]
   Int_t           dbar[113];   //[nddcand]
   Int_t           ddmode[113];   //[nddcand]
   Float_t         cosangle[113];   //[nddcand]
   Float_t         chi2vd[113];   //[nddcand]
   Float_t         chi2vdb[113];   //[nddcand]
   Float_t         chi2ed[113];   //[nddcand]
   Float_t         chi2edb[113];   //[nddcand]
   Float_t         chi2md[113];   //[nddcand]
   Float_t         chi2mdb[113];   //[nddcand]
   Float_t         chi2vddb[113];   //[nddcand]
   Int_t           mcdmode;
   Int_t           mcdbmode;
   Int_t           mcdmatch[103];   //[ndcand]
   Int_t           nmcpart;
   Int_t           mcident[40];   //[nmcpart]
   Int_t           mcpdgid[40];   //[nmcpart]
   Int_t           mcparent[40];   //[nmcpart]
   Float_t         mce[40];   //[nmcpart]
   Float_t         mcpx[40];   //[nmcpart]
   Float_t         mcpy[40];   //[nmcpart]
   Float_t         mcpz[40];   //[nmcpart]
   Int_t           mctruth[40];   //[nmcpart]

   // List of branches
   TBranch        *b_run;   //!
   TBranch        *b_event;   //!
   TBranch        *b_ecm;   //!
   TBranch        *b_xangle;   //!
   TBranch        *b_eneu;   //!
   TBranch        *b_echg;   //!
   TBranch        *b_evtmm2;   //!
   TBranch        *b_l1trig;   //!
   TBranch        *b_nbunch;   //!
   TBranch        *b_bunch;   //!
   TBranch        *b_l1trig2;   //!
   TBranch        *b_pxcm;   //!
   TBranch        *b_pycm;   //!
   TBranch        *b_pzcm;   //!
   TBranch        *b_ntrack;   //!
   TBranch        *b_trident;   //!
   TBranch        *b_trpie;   //!
   TBranch        *b_trpipx;   //!
   TBranch        *b_trpipy;   //!
   TBranch        *b_trpipz;   //!
   TBranch        *b_trpip;   //!
   TBranch        *b_trke;   //!
   TBranch        *b_trkpx;   //!
   TBranch        *b_trkpy;   //!
   TBranch        *b_trkpz;   //!
   TBranch        *b_trchg;   //!
   TBranch        *b_trz0;   //!
   TBranch        *b_trd0;   //!
   TBranch        *b_trcosth;   //!
   TBranch        *b_trphi0;   //!
   TBranch        *b_trdrhitf;   //!
   TBranch        *b_trzdhitf;   //!
   TBranch        *b_trhitf;   //!
   TBranch        *b_trchi2;   //!
   TBranch        *b_trchi2dof;   //!
   TBranch        *b_trsigpi;   //!
   TBranch        *b_trsigk;   //!
   TBranch        *b_trrichpll;   //!
   TBranch        *b_trrichpnp;   //!
   TBranch        *b_trrichkll;   //!
   TBranch        *b_trrichknp;   //!
   TBranch        *b_trtaginfo;   //!
   TBranch        *b_trfabort;   //!
   TBranch        *b_trrichphp;   //!
   TBranch        *b_trrichkhp;   //!
   TBranch        *b_trdb;   //!
   TBranch        *b_trdpthmu;   //!
   TBranch        *b_trroceid;   //!
   TBranch        *b_trtrkman;   //!
   TBranch        *b_nshow;   //!
   TBranch        *b_sident;   //!
   TBranch        *b_se;   //!
   TBranch        *b_spx;   //!
   TBranch        *b_spy;   //!
   TBranch        *b_spz;   //!
   TBranch        *b_sphi;   //!
   TBranch        *b_scosth;   //!
   TBranch        *b_se9o25uok;   //!
   TBranch        *b_shot;   //!
   TBranch        *b_sdettype;   //!
   TBranch        *b_strmatch;   //!
   TBranch        *b_strme;   //!
   TBranch        *b_strdist;   //!
   TBranch        *b_se9o25;   //!
   TBranch        *b_se9o25u;   //!
   TBranch        *b_npi0;   //!
   TBranch        *b_pi0ident;   //!
   TBranch        *b_pi0mass;   //!
   TBranch        *b_pi0chi2;   //!
   TBranch        *b_pi0e;   //!
   TBranch        *b_pi0px;   //!
   TBranch        *b_pi0py;   //!
   TBranch        *b_pi0pz;   //!
   TBranch        *b_pi0merr;   //!
   TBranch        *b_pi0dau1;   //!
   TBranch        *b_pi0dau2;   //!
   TBranch        *b_pi0istype1;   //!
   TBranch        *b_neta;   //!
   TBranch        *b_etaident;   //!
   TBranch        *b_etamass;   //!
   TBranch        *b_etachi2;   //!
   TBranch        *b_etae;   //!
   TBranch        *b_etapx;   //!
   TBranch        *b_etapy;   //!
   TBranch        *b_etapz;   //!
   TBranch        *b_etamerr;   //!
   TBranch        *b_etadau1;   //!
   TBranch        *b_etadau2;   //!
   TBranch        *b_nks;   //!
   TBranch        *b_ksident;   //!
   TBranch        *b_ksmass;   //!
   TBranch        *b_kse;   //!
   TBranch        *b_kspx;   //!
   TBranch        *b_kspy;   //!
   TBranch        *b_kspz;   //!
   TBranch        *b_kschi2;   //!
   TBranch        *b_ksrad;   //!
   TBranch        *b_ksraderr;   //!
   TBranch        *b_ksdau1;   //!
   TBranch        *b_ksdau2;   //!
   TBranch        *b_ksflsig;   //!
   TBranch        *b_ndcand;   //!
   TBranch        *b_dmode;   //!
   TBranch        *b_dmbc;   //!
   TBranch        *b_ddeltae;   //!
   TBranch        *b_ddeltaeerr;   //!
   TBranch        *b_dmraw;   //!
   TBranch        *b_dmrawerr;   //!
   TBranch        *b_dkchi2;   //!
   TBranch        *b_de;   //!
   TBranch        *b_dpx;   //!
   TBranch        *b_dpy;   //!
   TBranch        *b_dpz;   //!
   TBranch        *b_ddau1;   //!
   TBranch        *b_ddau2;   //!
   TBranch        *b_ddau3;   //!
   TBranch        *b_ddau4;   //!
   TBranch        *b_dcsign;   //!
   TBranch        *b_lepveto;   //!
   TBranch        *b_ddau5;   //!
   TBranch        *b_nmiss;   //!
   TBranch        *b_mmode;   //!
   TBranch        *b_mdcand;   //!
   TBranch        *b_mtrack1;   //!
   TBranch        *b_mtrack2;   //!
   TBranch        *b_mmsq;   //!
   TBranch        *b_mpx;   //!
   TBranch        *b_mpy;   //!
   TBranch        *b_mpz;   //!
   TBranch        *b_me;   //!
   TBranch        *b_mbestmbc;   //!
   TBranch        *b_nddcand;   //!
   TBranch        *b_d;   //!
   TBranch        *b_dbar;   //!
   TBranch        *b_ddmode;   //!
   TBranch        *b_cosangle;   //!
   TBranch        *b_chi2vd;   //!
   TBranch        *b_chi2vdb;   //!
   TBranch        *b_chi2ed;   //!
   TBranch        *b_chi2edb;   //!
   TBranch        *b_chi2md;   //!
   TBranch        *b_chi2mdb;   //!
   TBranch        *b_chi2vddb;   //!
   TBranch        *b_mcdmode;   //!
   TBranch        *b_mcdbmode;   //!
   TBranch        *b_mcdmatch;   //!
   TBranch        *b_nmcpart;   //!
   TBranch        *b_mcident;   //!
   TBranch        *b_mcpdgid;   //!
   TBranch        *b_mcparent;   //!
   TBranch        *b_mce;   //!
   TBranch        *b_mcpx;   //!
   TBranch        *b_mcpy;   //!
   TBranch        *b_mcpz;   //!
   TBranch        *b_mctruth;   //!

   DNTClass(TString inputfile, TString outputfile);
   virtual ~DNTClass();
   virtual Int_t    Cut(Long64_t entry);
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual void     Loop();
   virtual void     Skim(TString skimfile);
   virtual Bool_t   FoundEvent(TString skimfile, Int_t run_, Int_t event_);
   virtual Bool_t   Notify();
   virtual void     Show(Long64_t entry = -1);

   TFile* outputFile_;
   TTree* ts_;
   void CloneTree();

};

#endif

#ifdef DNTClass_cxx
DNTClass::DNTClass(TString inputfile, TString outputfile)
{

   TChain * chain = new TChain("dnt","");
   //chain->Add("Single_Dp_to_Kspi.root/dnt");

   chain->Add(inputfile);
   tree = chain;

   Init(tree);
   outputFile_ = new TFile(outputfile, "recreate");
   CloneTree();

}

DNTClass::~DNTClass()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t DNTClass::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t DNTClass::LoadTree(Long64_t entry)
{
// Set the environment to read one entry
   if (!fChain) return -5;
   Long64_t centry = fChain->LoadTree(entry);
   if (centry < 0) return centry;
   if (fChain->IsA() != TChain::Class()) return centry;
   TChain *chain = (TChain*)fChain;
   if (chain->GetTreeNumber() != fCurrent) {
      fCurrent = chain->GetTreeNumber();
      Notify();
   }
   return centry;
}

void DNTClass::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses of the tree
   // will be set. It is normaly not necessary to make changes to the
   // generated code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running with PROOF.

   // Set branch addresses
   if (tree == 0) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("run",&run);
   fChain->SetBranchAddress("event",&event);
   fChain->SetBranchAddress("ecm",&ecm);
   fChain->SetBranchAddress("xangle",&xangle);
   fChain->SetBranchAddress("eneu",&eneu);
   fChain->SetBranchAddress("echg",&echg);
   fChain->SetBranchAddress("evtmm2",&evtmm2);
   fChain->SetBranchAddress("l1trig",&l1trig);
   fChain->SetBranchAddress("nbunch",&nbunch);
   fChain->SetBranchAddress("bunch",&bunch);
   fChain->SetBranchAddress("l1trig2",&l1trig2);
   fChain->SetBranchAddress("pxcm",&pxcm);
   fChain->SetBranchAddress("pycm",&pycm);
   fChain->SetBranchAddress("pzcm",&pzcm);
   fChain->SetBranchAddress("ntrack",&ntrack);
   fChain->SetBranchAddress("trident",trident);
   fChain->SetBranchAddress("trpie",trpie);
   fChain->SetBranchAddress("trpipx",trpipx);
   fChain->SetBranchAddress("trpipy",trpipy);
   fChain->SetBranchAddress("trpipz",trpipz);
   fChain->SetBranchAddress("trpip",trpip);
   fChain->SetBranchAddress("trke",trke);
   fChain->SetBranchAddress("trkpx",trkpx);
   fChain->SetBranchAddress("trkpy",trkpy);
   fChain->SetBranchAddress("trkpz",trkpz);
   fChain->SetBranchAddress("trchg",trchg);
   fChain->SetBranchAddress("trz0",trz0);
   fChain->SetBranchAddress("trd0",trd0);
   fChain->SetBranchAddress("trcosth",trcosth);
   fChain->SetBranchAddress("trphi0",trphi0);
   fChain->SetBranchAddress("trdrhitf",trdrhitf);
   fChain->SetBranchAddress("trzdhitf",trzdhitf);
   fChain->SetBranchAddress("trhitf",trhitf);
   fChain->SetBranchAddress("trchi2",trchi2);
   fChain->SetBranchAddress("trchi2dof",trchi2dof);
   fChain->SetBranchAddress("trsigpi",trsigpi);
   fChain->SetBranchAddress("trsigk",trsigk);
   fChain->SetBranchAddress("trrichpll",trrichpll);
   fChain->SetBranchAddress("trrichpnp",trrichpnp);
   fChain->SetBranchAddress("trrichkll",trrichkll);
   fChain->SetBranchAddress("trrichknp",trrichknp);
   fChain->SetBranchAddress("trtaginfo",trtaginfo);
   fChain->SetBranchAddress("trfabort",trfabort);
   fChain->SetBranchAddress("trrichphp",trrichphp);
   fChain->SetBranchAddress("trrichkhp",trrichkhp);
   fChain->SetBranchAddress("trdb",trdb);
   fChain->SetBranchAddress("trdpthmu",trdpthmu);
   fChain->SetBranchAddress("trroceid",trroceid);
   fChain->SetBranchAddress("trtrkman",trtrkman);
   fChain->SetBranchAddress("nshow",&nshow);
   fChain->SetBranchAddress("sident",sident);
   fChain->SetBranchAddress("se",se);
   fChain->SetBranchAddress("spx",spx);
   fChain->SetBranchAddress("spy",spy);
   fChain->SetBranchAddress("spz",spz);
   fChain->SetBranchAddress("sphi",sphi);
   fChain->SetBranchAddress("scosth",scosth);
   fChain->SetBranchAddress("se9o25uok",se9o25uok);
   fChain->SetBranchAddress("shot",shot);
   fChain->SetBranchAddress("sdettype",sdettype);
   fChain->SetBranchAddress("strmatch",strmatch);
   fChain->SetBranchAddress("strme",strme);
   fChain->SetBranchAddress("strdist",strdist);
   fChain->SetBranchAddress("se9o25",se9o25);
   fChain->SetBranchAddress("se9o25u",se9o25u);
   fChain->SetBranchAddress("npi0",&npi0);
   fChain->SetBranchAddress("pi0ident",pi0ident);
   fChain->SetBranchAddress("pi0mass",pi0mass);
   fChain->SetBranchAddress("pi0chi2",pi0chi2);
   fChain->SetBranchAddress("pi0e",pi0e);
   fChain->SetBranchAddress("pi0px",pi0px);
   fChain->SetBranchAddress("pi0py",pi0py);
   fChain->SetBranchAddress("pi0pz",pi0pz);
   fChain->SetBranchAddress("pi0merr",pi0merr);
   fChain->SetBranchAddress("pi0dau1",pi0dau1);
   fChain->SetBranchAddress("pi0dau2",pi0dau2);
   fChain->SetBranchAddress("pi0istype1",pi0istype1);
   fChain->SetBranchAddress("neta",&neta);
   fChain->SetBranchAddress("etaident",etaident);
   fChain->SetBranchAddress("etamass",etamass);
   fChain->SetBranchAddress("etachi2",etachi2);
   fChain->SetBranchAddress("etae",etae);
   fChain->SetBranchAddress("etapx",etapx);
   fChain->SetBranchAddress("etapy",etapy);
   fChain->SetBranchAddress("etapz",etapz);
   fChain->SetBranchAddress("etamerr",etamerr);
   fChain->SetBranchAddress("etadau1",etadau1);
   fChain->SetBranchAddress("etadau2",etadau2);
   fChain->SetBranchAddress("nks",&nks);
   fChain->SetBranchAddress("ksident",ksident);
   fChain->SetBranchAddress("ksmass",ksmass);
   fChain->SetBranchAddress("kse",kse);
   fChain->SetBranchAddress("kspx",kspx);
   fChain->SetBranchAddress("kspy",kspy);
   fChain->SetBranchAddress("kspz",kspz);
   fChain->SetBranchAddress("kschi2",kschi2);
   fChain->SetBranchAddress("ksrad",ksrad);
   fChain->SetBranchAddress("ksraderr",ksraderr);
   fChain->SetBranchAddress("ksdau1",ksdau1);
   fChain->SetBranchAddress("ksdau2",ksdau2);
   fChain->SetBranchAddress("ksflsig",ksflsig);
   fChain->SetBranchAddress("ndcand",&ndcand);
   fChain->SetBranchAddress("dmode",dmode);
   fChain->SetBranchAddress("dmbc",dmbc);
   fChain->SetBranchAddress("ddeltae",ddeltae);
   fChain->SetBranchAddress("ddeltaeerr",ddeltaeerr);
   fChain->SetBranchAddress("dmraw",dmraw);
   fChain->SetBranchAddress("dmrawerr",dmrawerr);
   fChain->SetBranchAddress("dkchi2",dkchi2);
   fChain->SetBranchAddress("de",de);
   fChain->SetBranchAddress("dpx",dpx);
   fChain->SetBranchAddress("dpy",dpy);
   fChain->SetBranchAddress("dpz",dpz);
   fChain->SetBranchAddress("ddau1",ddau1);
   fChain->SetBranchAddress("ddau2",ddau2);
   fChain->SetBranchAddress("ddau3",ddau3);
   fChain->SetBranchAddress("ddau4",ddau4);
   fChain->SetBranchAddress("dcsign",dcsign);
   fChain->SetBranchAddress("lepveto",lepveto);
   fChain->SetBranchAddress("ddau5",ddau5);
   fChain->SetBranchAddress("nmiss",&nmiss);
   fChain->SetBranchAddress("mmode",&mmode);
   fChain->SetBranchAddress("mdcand",&mdcand);
   fChain->SetBranchAddress("mtrack1",&mtrack1);
   fChain->SetBranchAddress("mtrack2",&mtrack2);
   fChain->SetBranchAddress("mmsq",&mmsq);
   fChain->SetBranchAddress("mpx",&mpx);
   fChain->SetBranchAddress("mpy",&mpy);
   fChain->SetBranchAddress("mpz",&mpz);
   fChain->SetBranchAddress("me",&me);
   fChain->SetBranchAddress("mbestmbc",&mbestmbc);
   fChain->SetBranchAddress("nddcand",&nddcand);
   fChain->SetBranchAddress("d",d);
   fChain->SetBranchAddress("dbar",dbar);
   fChain->SetBranchAddress("ddmode",ddmode);
   fChain->SetBranchAddress("cosangle",cosangle);
   fChain->SetBranchAddress("chi2vd",chi2vd);
   fChain->SetBranchAddress("chi2vdb",chi2vdb);
   fChain->SetBranchAddress("chi2ed",chi2ed);
   fChain->SetBranchAddress("chi2edb",chi2edb);
   fChain->SetBranchAddress("chi2md",chi2md);
   fChain->SetBranchAddress("chi2mdb",chi2mdb);
   fChain->SetBranchAddress("chi2vddb",chi2vddb);
   fChain->SetBranchAddress("mcdmode",&mcdmode);
   fChain->SetBranchAddress("mcdbmode",&mcdbmode);
   fChain->SetBranchAddress("mcdmatch",mcdmatch);
   fChain->SetBranchAddress("nmcpart",&nmcpart);
   fChain->SetBranchAddress("mcident",mcident);
   fChain->SetBranchAddress("mcpdgid",mcpdgid);
   fChain->SetBranchAddress("mcparent",mcparent);
   fChain->SetBranchAddress("mce",mce);
   fChain->SetBranchAddress("mcpx",mcpx);
   fChain->SetBranchAddress("mcpy",mcpy);
   fChain->SetBranchAddress("mcpz",mcpz);
   fChain->SetBranchAddress("mctruth",mctruth);
   Notify();
}

Bool_t DNTClass::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. Typically here the branch pointers
   // will be retrieved. It is normaly not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed.

   // Get branch pointers
   b_run = fChain->GetBranch("run");
   b_event = fChain->GetBranch("event");
   b_ecm = fChain->GetBranch("ecm");
   b_xangle = fChain->GetBranch("xangle");
   b_eneu = fChain->GetBranch("eneu");
   b_echg = fChain->GetBranch("echg");
   b_evtmm2 = fChain->GetBranch("evtmm2");
   b_l1trig = fChain->GetBranch("l1trig");
   b_nbunch = fChain->GetBranch("nbunch");
   b_bunch = fChain->GetBranch("bunch");
   b_l1trig2 = fChain->GetBranch("l1trig2");
   b_pxcm = fChain->GetBranch("pxcm");
   b_pycm = fChain->GetBranch("pycm");
   b_pzcm = fChain->GetBranch("pzcm");
   b_ntrack = fChain->GetBranch("ntrack");
   b_trident = fChain->GetBranch("trident");
   b_trpie = fChain->GetBranch("trpie");
   b_trpipx = fChain->GetBranch("trpipx");
   b_trpipy = fChain->GetBranch("trpipy");
   b_trpipz = fChain->GetBranch("trpipz");
   b_trpip = fChain->GetBranch("trpip");
   b_trke = fChain->GetBranch("trke");
   b_trkpx = fChain->GetBranch("trkpx");
   b_trkpy = fChain->GetBranch("trkpy");
   b_trkpz = fChain->GetBranch("trkpz");
   b_trchg = fChain->GetBranch("trchg");
   b_trz0 = fChain->GetBranch("trz0");
   b_trd0 = fChain->GetBranch("trd0");
   b_trcosth = fChain->GetBranch("trcosth");
   b_trphi0 = fChain->GetBranch("trphi0");
   b_trdrhitf = fChain->GetBranch("trdrhitf");
   b_trzdhitf = fChain->GetBranch("trzdhitf");
   b_trhitf = fChain->GetBranch("trhitf");
   b_trchi2 = fChain->GetBranch("trchi2");
   b_trchi2dof = fChain->GetBranch("trchi2dof");
   b_trsigpi = fChain->GetBranch("trsigpi");
   b_trsigk = fChain->GetBranch("trsigk");
   b_trrichpll = fChain->GetBranch("trrichpll");
   b_trrichpnp = fChain->GetBranch("trrichpnp");
   b_trrichkll = fChain->GetBranch("trrichkll");
   b_trrichknp = fChain->GetBranch("trrichknp");
   b_trtaginfo = fChain->GetBranch("trtaginfo");
   b_trfabort = fChain->GetBranch("trfabort");
   b_trrichphp = fChain->GetBranch("trrichphp");
   b_trrichkhp = fChain->GetBranch("trrichkhp");
   b_trdb = fChain->GetBranch("trdb");
   b_trdpthmu = fChain->GetBranch("trdpthmu");
   b_trroceid = fChain->GetBranch("trroceid");
   b_trtrkman = fChain->GetBranch("trtrkman");
   b_nshow = fChain->GetBranch("nshow");
   b_sident = fChain->GetBranch("sident");
   b_se = fChain->GetBranch("se");
   b_spx = fChain->GetBranch("spx");
   b_spy = fChain->GetBranch("spy");
   b_spz = fChain->GetBranch("spz");
   b_sphi = fChain->GetBranch("sphi");
   b_scosth = fChain->GetBranch("scosth");
   b_se9o25uok = fChain->GetBranch("se9o25uok");
   b_shot = fChain->GetBranch("shot");
   b_sdettype = fChain->GetBranch("sdettype");
   b_strmatch = fChain->GetBranch("strmatch");
   b_strme = fChain->GetBranch("strme");
   b_strdist = fChain->GetBranch("strdist");
   b_se9o25 = fChain->GetBranch("se9o25");
   b_se9o25u = fChain->GetBranch("se9o25u");
   b_npi0 = fChain->GetBranch("npi0");
   b_pi0ident = fChain->GetBranch("pi0ident");
   b_pi0mass = fChain->GetBranch("pi0mass");
   b_pi0chi2 = fChain->GetBranch("pi0chi2");
   b_pi0e = fChain->GetBranch("pi0e");
   b_pi0px = fChain->GetBranch("pi0px");
   b_pi0py = fChain->GetBranch("pi0py");
   b_pi0pz = fChain->GetBranch("pi0pz");
   b_pi0merr = fChain->GetBranch("pi0merr");
   b_pi0dau1 = fChain->GetBranch("pi0dau1");
   b_pi0dau2 = fChain->GetBranch("pi0dau2");
   b_pi0istype1 = fChain->GetBranch("pi0istype1");
   b_neta = fChain->GetBranch("neta");
   b_etaident = fChain->GetBranch("etaident");
   b_etamass = fChain->GetBranch("etamass");
   b_etachi2 = fChain->GetBranch("etachi2");
   b_etae = fChain->GetBranch("etae");
   b_etapx = fChain->GetBranch("etapx");
   b_etapy = fChain->GetBranch("etapy");
   b_etapz = fChain->GetBranch("etapz");
   b_etamerr = fChain->GetBranch("etamerr");
   b_etadau1 = fChain->GetBranch("etadau1");
   b_etadau2 = fChain->GetBranch("etadau2");
   b_nks = fChain->GetBranch("nks");
   b_ksident = fChain->GetBranch("ksident");
   b_ksmass = fChain->GetBranch("ksmass");
   b_kse = fChain->GetBranch("kse");
   b_kspx = fChain->GetBranch("kspx");
   b_kspy = fChain->GetBranch("kspy");
   b_kspz = fChain->GetBranch("kspz");
   b_kschi2 = fChain->GetBranch("kschi2");
   b_ksrad = fChain->GetBranch("ksrad");
   b_ksraderr = fChain->GetBranch("ksraderr");
   b_ksdau1 = fChain->GetBranch("ksdau1");
   b_ksdau2 = fChain->GetBranch("ksdau2");
   b_ksflsig = fChain->GetBranch("ksflsig");
   b_ndcand = fChain->GetBranch("ndcand");
   b_dmode = fChain->GetBranch("dmode");
   b_dmbc = fChain->GetBranch("dmbc");
   b_ddeltae = fChain->GetBranch("ddeltae");
   b_ddeltaeerr = fChain->GetBranch("ddeltaeerr");
   b_dmraw = fChain->GetBranch("dmraw");
   b_dmrawerr = fChain->GetBranch("dmrawerr");
   b_dkchi2 = fChain->GetBranch("dkchi2");
   b_de = fChain->GetBranch("de");
   b_dpx = fChain->GetBranch("dpx");
   b_dpy = fChain->GetBranch("dpy");
   b_dpz = fChain->GetBranch("dpz");
   b_ddau1 = fChain->GetBranch("ddau1");
   b_ddau2 = fChain->GetBranch("ddau2");
   b_ddau3 = fChain->GetBranch("ddau3");
   b_ddau4 = fChain->GetBranch("ddau4");
   b_dcsign = fChain->GetBranch("dcsign");
   b_lepveto = fChain->GetBranch("lepveto");
   b_ddau5 = fChain->GetBranch("ddau5");
   b_nmiss = fChain->GetBranch("nmiss");
   b_mmode = fChain->GetBranch("mmode");
   b_mdcand = fChain->GetBranch("mdcand");
   b_mtrack1 = fChain->GetBranch("mtrack1");
   b_mtrack2 = fChain->GetBranch("mtrack2");
   b_mmsq = fChain->GetBranch("mmsq");
   b_mpx = fChain->GetBranch("mpx");
   b_mpy = fChain->GetBranch("mpy");
   b_mpz = fChain->GetBranch("mpz");
   b_me = fChain->GetBranch("me");
   b_mbestmbc = fChain->GetBranch("mbestmbc");
   b_nddcand = fChain->GetBranch("nddcand");
   b_d = fChain->GetBranch("d");
   b_dbar = fChain->GetBranch("dbar");
   b_ddmode = fChain->GetBranch("ddmode");
   b_cosangle = fChain->GetBranch("cosangle");
   b_chi2vd = fChain->GetBranch("chi2vd");
   b_chi2vdb = fChain->GetBranch("chi2vdb");
   b_chi2ed = fChain->GetBranch("chi2ed");
   b_chi2edb = fChain->GetBranch("chi2edb");
   b_chi2md = fChain->GetBranch("chi2md");
   b_chi2mdb = fChain->GetBranch("chi2mdb");
   b_chi2vddb = fChain->GetBranch("chi2vddb");
   b_mcdmode = fChain->GetBranch("mcdmode");
   b_mcdbmode = fChain->GetBranch("mcdbmode");
   b_mcdmatch = fChain->GetBranch("mcdmatch");
   b_nmcpart = fChain->GetBranch("nmcpart");
   b_mcident = fChain->GetBranch("mcident");
   b_mcpdgid = fChain->GetBranch("mcpdgid");
   b_mcparent = fChain->GetBranch("mcparent");
   b_mce = fChain->GetBranch("mce");
   b_mcpx = fChain->GetBranch("mcpx");
   b_mcpy = fChain->GetBranch("mcpy");
   b_mcpz = fChain->GetBranch("mcpz");
   b_mctruth = fChain->GetBranch("mctruth");

   return kTRUE;
}

void DNTClass::Show(Long64_t entry)
{
// Print contents of entry.
// If entry is not specified, print current entry
   if (!fChain) return;
   fChain->Show(entry);
}
Int_t DNTClass::Cut(Long64_t entry)
{
// This function may be called from Loop.
// returns  1 if entry is accepted.
// returns -1 otherwise.
   return 1;
}

void DNTClass::CloneTree(){
  fChain->LoadTree(0); //force 1st tree to be loaded
  ts_ = fChain->GetTree()->CloneTree(0);
}

#endif // #ifdef DNTClass_cxx
