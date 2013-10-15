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

#include <iostream>
#include <math.h>
#include <vector>
#include <string>


#include "RooDLineShapeImp.h"
#include "RooDEnergyImp.h"

ClassImp(RooDLineShapeImp)

static const char rcsid[] = "$Id$";




RooDLineShapeImp::RooDLineShapeImp(double mres,double gamma,double r,
				   double sigmaE,double sigmap,
				   double md, double Ebeam, 
				   double mc, int nbin,
				   double mbcmin):
  m_lshape("Mbc dist",nbin,mbcmin,Ebeam){
  m_mres=mres;
  m_gamma=gamma;
  m_r=r;
  m_sigmaE=sigmaE;
  m_sigmap=sigmap;
  m_md=md;
  m_Ebeam=Ebeam;
  m_mc=mc;

  static double pi=4*atan(1.0);

  RooDEnergyImp edist(mres,gamma,r,sigmaE,md,Ebeam,mc);
  
  

  //Now do the momentum convolution for mbc

  for (int i=0;i<nbin;i++){
    //std::cout << "Second:"<<i<<std::endl;
    //cout << "i, nbin:"<<i<<" "<<nbin<<endl;
    double mbc=m_lshape.getX(i);
    double p=sqrt(Ebeam*Ebeam-mbc*mbc);
    //double e=2*sqrt(md*md+p*p);
    //double prob=0.0;

    double ppmin=p-10*m_sigmap;
    double ppmax=p+10*m_sigmap;
    double epmax=2*sqrt(md*md+ppmax*ppmax);
    if (epmax>edist.max()) epmax=2*Ebeam+10*m_sigmaE;
    double epmin=2*md;
    if (ppmin>0.0) epmin=2*sqrt(md*md+ppmin*ppmin);
    if (epmin>epmax) epmin=epmax;
    //std::cout << "emin, emax, epmin, epmax:"<<emin<<" "<<emax<<" "
    //      <<epmin<<" "<<epmax<<std::endl; 
 
    /* 
    int kmax=edist.geti(epmax);
    int kmin=edist.geti(epmin);
    assert(kmax>=kmin);
    //cout << "kmin, kmax:"<<kmin<<" "<<kmax<<endl;
    for (int k=kmin;k<kmax;k++){
      double ep=edist.getX(k);
      double pp=sqrt(ep*ep/4.0-md*md);
      //double mbcp=sqrt(Ebeam*Ebeam-pp*pp);

      if (fabs(p-pp)<10*m_sigmap) {
	double w=p*(exp(-(p-pp)*(p-pp)/(2*m_sigmap*m_sigmap))-
		    exp(-(p+pp)*(p+pp)/(2*m_sigmap*m_sigmap)))/
	  (sqrt(2*pi)*pp*m_sigmap);

	if (pp==0.0||p==0.0) w=0.0;

	assert(w>=0);
	if (w>1e-20) {
	  //std::cout << "p, pp:"<<p<<" "<<pp<<" "<<e<<" "<<ep<<std::endl;
	  //prob+=de*(mbc/e)*edist.getVal(k)*w;
	  prob+=edist.dx()*edist.getVal(k)*w*(mbc/p);
	  
	}
      }

    }
    */

    double probnew=0.0;

    double ppminnew=p-10*m_sigmap;
    double ppmaxnew=p+10*m_sigmap;
   
    if (ppminnew<0) ppminnew=0.0;

    double ppmaxE=sqrt(0.25*edist.max()*edist.max()-md*md);
    
    if (ppmaxnew>ppmaxE) ppmaxnew=ppmaxE;

    int nstep=100;

    double dp=(ppmaxnew-ppminnew)/nstep;

    for(int ii=0;ii<nstep;ii++){
      double pp=ppminnew+dp*(0.5+ii);
      double ep=2*sqrt(md*md+pp*pp);
      
      double w=(exp(-(p-pp)*(p-pp)/(2*m_sigmap*m_sigmap))-
		exp(-(p+pp)*(p+pp)/(2*m_sigmap*m_sigmap)))/ep;

      probnew+=w*edist.getVal(ep);

    }

    probnew*=4.0*dp*mbc/(sqrt(2*pi)*m_sigmap);

    //std::cout << "prob,probnew:"<<prob<<" "<<probnew<<std::endl;

    //if (prob>0.0000000001) std::cout <<probnew/prob
    //				     <<"  "<<edist.getVal(3.771)<<std::endl;

    m_lshape.set(i,probnew);

    //std::cout <<"mbc:"<<mbc<<" "<<prob<<" "<<e<<" "<<std::endl;
    
  }

  /*
  double ep=3.771;

  do {

    std::cout<< "ep:"<<ep<<" "<<edist.getVal(ep)<<std::endl;
    
    ep+=0.00001;

  } while (ep<3.772);
  */



  m_lshape.normalize();

  //std::cout << "Done with second convolution"<<std::endl;


}



double RooDLineShapeImp::evaluate(double mbc){

  return m_lshape.getVal(mbc);

}

