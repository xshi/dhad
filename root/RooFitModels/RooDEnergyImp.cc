/*****************************************************************************
 * Project: RooFit                                                           *
 * Package: RooFitModels                                                     *
 *    File: $$
 * Authors:                                                                  *
 *   WV, Wouter Verkerke, UC Santa Barbara, verkerke@slac.stanford.edu       *
 *   DK, David Kirkby,    UC Irvine,         dkirkby@uci.edu                 *
 *   AR, Anders Ryd,      Cornell U.,        ryd@lepp.cornell.edu            *
 *                                                                           *
 * Copyright (c) 2000-2004, Regents of the University of California          *
 *                          and Stanford University. All rights reserved.    *
 * copyright (c) 2004       Cornell University
 *                                                                           *
 * Redistribution and use in source and binary forms,                        *
 * with or without modification, are permitted according to the terms        *
 * listed in LICENSE (http://roofit.sourceforge.net/license.txt)             *
 *****************************************************************************/

// -- CLASS DESCRIPTION [PDF] --

//#include "BaBar/BaBar.hh"
#include <iostream>
#include <math.h>
#include <vector>
#include <string>


#include "RooFitModels/RooDEnergyImp.hh"
#include "RooFitModels/RooParmFcn.hh"
#include "RooFitCore/RooAbsReal.hh"
#include "RooFitCore/RooRealVar.hh"
#include "RooFitCore/RooArgSet.hh"

ClassImp(RooDEnergyImp)

static const char rcsid[] =
"$Id: RooDEnergyImp.cc,v 1.3 2007/05/09 12:54:37 xs32 Exp $";




RooDEnergyImp::RooDEnergyImp(double mres,double gamma,double r,
			     double sigmaE,
			     double md, double Ebeam, double mc, int nbin){
  m_mres=mres;
  m_gamma=gamma;
  m_r=r;
  m_sigmaE=sigmaE;
  m_md=md;
  m_Ebeam=Ebeam;
  m_mc=mc;


  //kludge as there are to few bins in the momentum convolution integral
  //nbin*=5;

  //static double pi=4*atan(1.0);

  
  //First convolve h and BE 
  //function of E

  //E here is the energy of the psi''

  double emin=2*md;
  double emax=2*Ebeam+20*sigmaE;

  //std::cout << "Ebeam, sigmaE:"<<Ebeam<<" "<<sigmaE<<std::endl;


  //double de=(emax-emin)/nbin;

  edist=new RooParmFcn("Epsi(3770)",nbin,emin,emax);


  for (int i=0;i<nbin+1;i++){
    //std::cout << "First:"<<i<<std::endl;
    double e=edist->getX(i);

    int nintbin=200;
    double nsigma=10.0;

    double eintmax=2*Ebeam+nsigma*sigmaE;
    double eintmin=2*Ebeam-nsigma*sigmaE;
    double prob=0.0;

    double deint=(eintmax-eintmin)/nintbin;

    double eintlow=eintmin;
    double einthigh=eintlow+deint;

    while(einthigh<eintmax){
      double A,B,C;
      BE(0.5*(eintlow+einthigh),A,B,C);
      prob+=h(eintlow-e,einthigh-e,A,B,C);
      assert(prob==prob);
      //std::cout << "h :"<<eint<<" "<<prob<<std::endl;
      eintlow=einthigh;
      einthigh+=deint;
    }

    //if (prob*BW(e)>100000){
    //  std::cout << "prob BW(e):"<<prob<<" "<<BW(e)<<std::endl;
    //  assert(0);
    //}
    
    edist->set(i,prob*BW(e));

    //std::cout <<"E:"<< e << " " << edist[i]<<" "<<prob<<" "<<BW(e)<<std::endl;
  }

  edist->normalize();

  //std::cout << "Done with first convolution"<<std::endl;

  //edist->print();
  

}

RooDEnergyImp::~RooDEnergyImp(){
  delete edist;
}


void RooDEnergyImp::BE(double e,double& A, double& B, double& C){

  static double sqrt2pi=sqrt(8.0*atan(1.0));

  double ecm=2.0*m_Ebeam;

  A=exp(-(e-ecm)*(e-ecm)/(2*m_sigmaE*m_sigmaE))/(sqrt2pi*m_sigmaE);
  B=-A*(e-ecm)/(m_sigmaE*m_sigmaE);
  C=-A/(m_sigmaE*m_sigmaE)+(e-ecm)*(e-ecm)*A/
    (m_sigmaE*m_sigmaE*m_sigmaE*m_sigmaE);

  //return exp(-(e-m_mres)*(e-m_mres)/(2*m_sigmaE*m_sigmaE))/(sqrt2pi*m_sigmaE);

}

double RooDEnergyImp::h(double emin,double emax, 
			   double A, double B, double C){

  //return integral from egamma-degamma/2 to egamma+degamma/2

  assert(emin<emax);

  double egamma=0.5*(emin+emax);


  if (emax<=0.0) return 0.0;

  if (emin<=0.0) emin=0.0;

  static double pi=4*atan(1.0);

  static double beta=2*(2*log(3770/0.511)-1)/(pi*137);

  double a=A-B*egamma+0.5*C*egamma*egamma;
  double b=B-C*egamma;

  if (0&&emax<0.001) {

    std::cout << "Int:"<<emin<<" "<<emax<<" "<<A<<" "
	    <<pow(emax,beta)*(a/beta+b*emax/(beta+1)+C*emax*emax/(2*beta+4))
	    <<" "
	    <<pow(emin,beta)*(a/beta+b*emin/(beta+1)+C*emin*emin/(2*beta+4))
            <<" "
	    <<
    pow(emax,beta)*(a/beta+b*emax/(beta+1)+C*emax*emax/(2*beta+4))-
    pow(emin,beta)*(a/beta+b*emin/(beta+1)+C*emin*emin/(2*beta+4))
	    <<std::endl;

  }

 
  
  return pow(emax,beta)*(a/beta+b*emax/(beta+1)+C*emax*emax/(2*beta+4))-
         pow(emin,beta)*(a/beta+b*emin/(beta+1)+C*emin*emin/(2*beta+4));

}


double RooDEnergyImp::BW(double e){

  static int first=1;
  if (first<10){
    std::cout << "In RooDEnergyImp::BW m_mc="<<m_mc<<std::endl;
    first++;
  }


  if (e<2.0*m_md) return 0.0;

  double p=sqrt(e*e/4.0-m_md*m_md);

  double m_d0=1.865;
  double m_dp=1.869;
  

  double pp=0.0;
  if (e/2.0>m_dp) pp=sqrt(e*e/4.0-m_dp*m_dp);
  double pn=0.0;
  if (e/2.0>m_d0) pn=sqrt(e*e/4.0-m_d0*m_d0);

  double pp0=sqrt(m_mres*m_mres/4.0-m_dp*m_dp);
  double pn0=sqrt(m_mres*m_mres/4.0-m_d0*m_d0);

  

  //MC shape for broken MC
  if (fabs(m_mc+1.0)<0.5){
    static int first=1;
    if (first<10){
      std::cout << "Shape to use for old broken MC"<<std::endl;
      first++;
    }

    if (e/2<=1.87) return 0.0;
    double pmc=sqrt(e*e/4.0-1.87*1.87);
    return pmc*pmc*pmc;
    //return pp*pp*pp+pn*pn*pn;
  }
 
  if (fabs(m_mc)<0.5) {
    //static double r=12.7/5.0; // 1/GeV
    //double r=0.0; // 1/GeV
    //cout << "gamma:"<<m_gamma<<endl;
    //double gamma=m_gamma;
    static int first=1;
    if (first<10){
      std::cout << "Modified MARK III shape that uses D0D0 vs DpDm br. fr. gamma:"<<m_gamma<<std::endl;
      first++;
    }
    double gamma=m_gamma*(0.43*pp*pp*pp/(1.0+(m_r*pp)*(m_r*pp))+0.57*pn*pn*pn/(1.0+(m_r*pn)*(m_r*pn)))/
      (0.43*pp0*pp0*pp0/(1.0+(m_r*pp0)*(m_r*pp0))+0.57*pn0*pn0*pn0/(1.0+(m_r*pn0)*(m_r*pn0)));
    return (p*p*p/(1.0+(m_r*p)*(m_r*p)))/((e*e-m_mres*m_mres)*(e*e-m_mres*m_mres)+e*e*gamma*gamma);
  }

  //MARK III shape
  if (fabs(m_mc-1.0)<0.5) {
    //double r=12.7; // 1/GeV
    //double r=12.7/5.0; // 1/GeV
    //double r=25.0; // 1/GeV
    static int first=1;
    if (first<10){
      std::cout << "MARK III gamma:"<<m_gamma<<std::endl;
      first++;
    }
    //double gamma=m_gamma;
    double gamma=m_gamma*(pp*pp*pp/(1.0+(m_r*pp)*(m_r*pp))+pn*pn*pn/(1.0+(m_r*pn)*(m_r*pn)))/
      (pp0*pp0*pp0/(1.0+(m_r*pp0)*(m_r*pp0))+pn0*pn0*pn0/(1.0+(m_r*pn0)*(m_r*pn0)));
    return (p*p*p/(1.0+(m_r*p)*(m_r*p)))/((e-m_mres)*(e-m_mres)+gamma*gamma/4.0);
  }

  
  if (fabs(m_mc-2.0)<0.5){

    static int first=1;
    if (first<10){
      std::cout << "p^3 lineshape..."<<std::endl;
      first++;
    }


    //double p=sqrt(e*e/4-m_md*m_md);
    return p*p*p;
    //return p*p*p/((e*e-m_mres*m_mres)*(e*e-m_mres*m_mres)+e*e*m_gamma*m_gamma);
    //return p*p*p*m_gamma*m_gamma/((e-m_mres)*(e-m_mres)+m_gamma*m_gamma/4.0);
  }


  //BES 2007 paper
  if (fabs(m_mc-3)<0.5) {


    static int first=1;
    if (first<10){
      std::cout << "Implementation of the BES2006 lineshape hepex/0612056"<<std::endl;
      first++;
    }


    double B00=0.57;
    double Bpm=1-B00;

    double GammaD0D0=m_gamma*B00*pn*pn*pn*(1+(m_r*pn0)*(m_r*pn0))/
      (pn0*pn0*pn0*(1+(m_r*pn)*(m_r*pn)));

    double GammaDpDm=m_gamma*Bpm*pp*pp*pp*(1+(m_r*pp0)*(m_r*pp0))/
      (pp0*pp0*pp0*(1+(m_r*pp)*(m_r*pp)));

    double gamma=GammaD0D0+GammaDpDm;

    // Bug found by Steve

    //     return gamma/( (e*e-m_mres*m_mres)*(e*e-m_mres*m_mres)+m_mres*m_mres*gamma*gamma);


// Steve's FIX:
    double numerator;
    if (m_md < 1.867) numerator = GammaD0D0;
    else numerator = GammaDpDm;
    return numerator/(
		      (e*e-m_mres*m_mres)*(e*e-m_mres*m_mres)+m_mres*m_mres*gamma*gamma);
    
  }


  assert(0);

}



double RooDEnergyImp::evaluate(double ecm){


  return edist->getVal(ecm);

}


