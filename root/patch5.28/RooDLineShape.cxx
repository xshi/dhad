
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


#include "RooDLineShape.h"
#include "RooDLineShapeImp.h"
#include "RooDEnergyImp.h"
#include "RooParmFcn.h"
#include "RooAbsReal.h"
#include "RooRealVar.h"
#include "RooArgSet.h"

ClassImp(RooDLineShape)

static const char rcsid[] =
"$Id$";


RooDLineShape::RooDLineShape(const char *name, const char *title, 
			     int npointEbeam, 
			     RooAbsReal& _mbc,
			     RooAbsReal& _Ebeam,
			     RooAbsReal& _mres,
			     RooAbsReal& _gamma, 
			     RooAbsReal& _r, 
			     RooAbsReal& _sigmaE, 
			     RooAbsReal& _sigmap, 
			     RooAbsReal& _md, 
			     RooAbsReal& _mc
) :
  RooAbsPdf(name, title),
  mbc("mbc", "Dependent", this, _mbc),
  mres("mres", "mres", this, _mres),
  Ebeam("Ebeam", "Ebeam", this, _Ebeam),
  gamma("gamma", "gamma", this, _gamma),
  r("r", "r", this, _r),
  sigmaE("sigmaE", "sigmaE", this, _sigmaE),
  sigmap("sigmap", "sigmap", this, _sigmap),
  md("md", "md", this, _md),
  mc("mc", "mc", this, _mc),
  m_npointEbeam(npointEbeam)

{
}

RooDLineShape::RooDLineShape(const RooDLineShape& other, const char* name) :
  RooAbsPdf(other, name), 
  mbc("mbc", this, other.mbc), 
  mres("mres", this, other.mres),
  Ebeam("Ebeam", this, other.Ebeam),
  gamma("gamma", this, other.gamma),
  r("r", this, other.r),
  sigmaE("sigmaE", this, other.sigmaE), 
  sigmap("sigmap", this, other.sigmap),md("md", this, other.md),
  mc("mc", this, other.mc),
  m_npointEbeam(other.m_npointEbeam)
{
}

Double_t RooDLineShape::evaluate() const {

  int newval=(mres_save!=mres)|| 
    (gamma_save!=gamma)||
    (r_save!=r)||
    (sigmaE_save!=sigmaE)||
    (sigmap_save!=sigmap)||
    (md_save!=md);


  if (shapes.size()==0||newval){

    for (unsigned int i=0;i<shapes.size();i++){
      delete shapes[i];
    }
    
    shapes.clear();

    //std::cout <<"New evaluation:"<<std::endl;
    //std::cout <<"  md="<<md<<std::endl;
    //std::cout <<"  gamma="<<gamma<<std::endl;
    //std::cout <<"  sigmaE="<<sigmaE<<std::endl;
    //std::cout <<"  sigmap="<<sigmap<<std::endl;

    mres_save=mres; 
    gamma_save=gamma;
    r_save=r;
    sigmaE_save=sigmaE;
    sigmap_save=sigmap;
    md_save=md;

    assert(m_npointEbeam>0);

    for(int i=0;i<m_npointEbeam;i++){

      double ebeam;

      if (m_npointEbeam==1) {
	ebeam=0.5*(Ebeam.min()+Ebeam.max());
	if (Ebeam.max()>1e10) ebeam=Ebeam;
      }
      else{
	ebeam=Ebeam.min()+i*(Ebeam.max()-Ebeam.min())/(m_npointEbeam-1.0);
      }
     
      
      shapes.push_back(new RooDLineShapeImp(mres,gamma,r,sigmaE,sigmap,md,
				   ebeam,mc)); 

    }
    
  }


  if (mbc>Ebeam.max()) return 1e-10;

  if (m_npointEbeam==1){

    double ebeam=0.5*(Ebeam.min()+Ebeam.max());

    if (Ebeam.max()>1e10) ebeam=Ebeam;

    if (mbc>ebeam) {
      //std::cout << "mbc, ebeam:"<<mbc<<" "<<ebeam<<std::endl;
      return 1e-10;
    }

    double retval=shapes[0]->evaluate(mbc); 

    if (retval<0.0&&retval>-1e-4) retval=0.0;

    if (!(retval>=0.0)) {
      std::cout << "mbc, retval, Ebeam:"<<mbc<<" "<<retval<<" "<<Ebeam<<std::endl;
    }

    assert(retval>=0.0);

    return retval;
  } 

  double DeltaEbeam=(Ebeam.max()-Ebeam.min())/(m_npointEbeam-1.0);
  
  unsigned int i1=(int)((Ebeam-Ebeam.min())/DeltaEbeam);
  unsigned int i2=i1+1;

  //std::cout << "Ebeam, Ebeam.min(), mbc, i1:"<<Ebeam<<" "<<Ebeam.min()<<" "<<
  //  mbc<<" "<<i1<<std::endl;

  //due to rounding...
  assert(i2<1+shapes.size());
  if (i2==shapes.size()) i2=shapes.size()-1;

  double Ebeam1=Ebeam.min()+i1*DeltaEbeam;
  double Ebeam2=Ebeam.min()+i2*DeltaEbeam;

  //std::cout << "Ebeam1, Ebeam2, DeltaEbeam:"<<Ebeam1<<" "<<Ebeam2<<" "<<DeltaEbeam<<endl;

  assert(Ebeam1<=Ebeam); 
  assert(Ebeam2>=Ebeam); 

  //if (mbc>Ebeam2) return shapes[i2]->evaluate(mbc); 

  double w=(Ebeam2-Ebeam)/DeltaEbeam;
  
  //return shapes[2]->evaluate(mbc);

  double v1=shapes[i1]->evaluate(mbc);
  double v2=shapes[i2]->evaluate(mbc);

  if (v1<-1e-4) {
    std::cout << "Negative: v1, i1, Ebeam1:"<<v1<<" "<<i1<<" "<<Ebeam1<<" "<<Ebeam1-1.88<<std::endl;
  }

  if (v2<-1e-4) {
    std::cout << "Negative: v2, i2, Ebeam2:"<<v2<<" "<<i2<<" "<<Ebeam2<<" "<<Ebeam2-1.88<<std::endl;
  }
	
  double retval=v1*w+v2*(1.0-w);

  if (retval<0) {
    if (retval<-1e-4){
      std::cout << "Negative:"<<shapes[i1]->evaluate(mbc)<<" "
		<<shapes[i2]->evaluate(mbc)<<" "<<w<<std::endl;
    }
    retval=0.0;
  }

  assert(retval>=0.0);

  return retval;

}


Int_t RooDLineShape::getAnalyticalIntegral(RooArgSet& allVars, RooArgSet& analVars, const char*) const
{

  //std::cout << "Asking to do integral in RooDLineShape"<<std::endl;

  if (matchArgs(allVars,analVars,mbc)) return 1 ;

  return 0 ;

}


Double_t RooDLineShape::analyticalIntegral(Int_t code, const char*) const
{
  //assert(0);

  //std::cout << "Returning 1 in RooDLineShape"<<std::endl;

  return 1.0;

}
