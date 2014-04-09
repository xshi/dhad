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


#include "RooFitModels/RooDLineShapeImp2D.hh"
#include "RooFitModels/RooDEnergyImp.hh"

ClassImp(RooDLineShapeImp2D)

static const char rcsid[] = "$Id: RooCBShape.cc,v 1.7 2004/04/05 22:38:34 wverkerke Exp $";




RooDLineShapeImp2D::RooDLineShapeImp2D(double mres,
				       double gamma,
                                       double r,
				       double sigmaE, 
				       double sigmap1, 
				       double sigmap1a, 
				       double sigmap1b, 
				       double f1a, 
				       double f1b, 
				       double sigmap2,
				       double sigmap2a, 
				       double sigmap2b, 
				       double f2a, 
				       double f2b, 
				       double md, 
				       double Ebeam, 
				       double nonres, 
				       int nbin,
				       double mbcmin){
  m_mres=mres;
  m_gamma=gamma;
  m_r=r;
  m_sigmaE=sigmaE;
  m_sigmap1=sigmap1;
  m_sigmap1a=sigmap1a;
  m_sigmap1b=sigmap1b;
  m_f1a=f1a;
  m_f1b=f1b;
  m_sigmap2=sigmap2;
  m_sigmap2a=sigmap2a;
  m_sigmap2b=sigmap2b;
  m_f2a=f2a;
  m_f2b=f2b;
  m_md=md;
  m_Ebeam=Ebeam;
  m_nonres=nonres;


  //Convolve h and BE 
  m_edist=new RooDEnergyImp(m_mres,m_gamma,m_r,m_sigmaE,m_md,m_Ebeam,m_nonres);

  
  return; 



}

double RooDLineShapeImp2D::evalInt2(double mbc1){

  static double pi=4*atan(1.0);


  //Now do the momentum convolution for mbc

  if (mbc1>=m_Ebeam) return 0.0;


  double p1=sqrt(m_Ebeam*m_Ebeam-mbc1*mbc1);
  //double e1=2*sqrt(m_md*m_md+p1*p1);

  double sigmap1=m_sigmap1;

  if (m_f1a>0&&m_sigmap1a>sigmap1) sigmap1=m_sigmap1a;
  if (m_f1b>0&&m_sigmap1b>sigmap1) sigmap1=m_sigmap1b;

  double ppmin1=p1-10*sigmap1;
  double ppmax1=p1+10*sigmap1;
  double epmax1=2*sqrt(m_md*m_md+ppmax1*ppmax1);
  if (epmax1>m_edist->max()) epmax1=2*m_Ebeam+10*m_sigmaE;
  double epmin1=2*m_md;
  if (ppmin1>0.0) epmin1=2*sqrt(m_md*m_md+ppmin1*ppmin1);
  if (epmin1>epmax1) epmin1=epmax1;
  int kmax1=m_edist->geti(epmax1);
  int kmin1=m_edist->geti(epmin1);
  assert(kmax1>=kmin1);


  double prob=0.0;
  for (int k=kmin1;k<kmax1;k++){
    double ep=m_edist->getX(k);
    double pp=sqrt(ep*ep/4.0-m_md*m_md);

    if ( (fabs(p1-pp)<10.0*sigmap1) && pp!=0.0 ) {
      double w1=(1.0-m_f1a-m_f1b)*p1*
	(exp(-(p1-pp)*(p1-pp)/(2*m_sigmap1*m_sigmap1))-
	 exp(-(p1+pp)*(p1+pp)/(2*m_sigmap1*m_sigmap1)))/
	(sqrt(2*pi)*pp*m_sigmap1);
      if (m_f1a>0.0) w1+=m_f1a*p1*
	(exp(-(p1-pp)*(p1-pp)/(2*m_sigmap1a*m_sigmap1a))-
	 exp(-(p1+pp)*(p1+pp)/(2*m_sigmap1a*m_sigmap1a)))/
	(sqrt(2*pi)*pp*m_sigmap1a);
      if (m_f1b>0.0) w1+=m_f1b*p1*
	(exp(-(p1-pp)*(p1-pp)/(2*m_sigmap1b*m_sigmap1b))-
	 exp(-(p1+pp)*(p1+pp)/(2*m_sigmap1b*m_sigmap1b)))/
	(sqrt(2*pi)*pp*m_sigmap1b);

      if (!(w1>=0)) {
	std::cout << "w1, p1, pp, m_sigmap1:"
		  <<w1<<" "<<p1<<" "<<pp<<" "<<m_sigmap1<<std::endl;
      }

      assert(w1>=0);

      if (w1>1e-20) {
	    //std::cout << "p, pp:"<<p<<" "<<pp<<" "<<e<<" "<<ep<<std::endl;
	prob+=m_edist->dx()*m_edist->getVal(k)*w1*mbc1/p1;
	    
      }
    }
	
  }

  return prob;

}


double RooDLineShapeImp2D::evalInt1(double mbc2){

  static double pi=4*atan(1.0);


  //Now do the momentum convolution for mbc

  if (mbc2>=m_Ebeam) return 0.0;


  double p2=sqrt(m_Ebeam*m_Ebeam-mbc2*mbc2);
  //double e2=2*sqrt(m_md*m_md+p2*p2);

  double sigmap2=m_sigmap2;

  if (m_f2a>0&&m_sigmap2a>sigmap2) sigmap2=m_sigmap2a;
  if (m_f2b>0&&m_sigmap2b>sigmap2) sigmap2=m_sigmap2b;

  double ppmin2=p2-10*sigmap2;
  double ppmax2=p2+10*sigmap2;
  double epmax2=2*sqrt(m_md*m_md+ppmax2*ppmax2);
  if (epmax2>m_edist->max()) epmax2=2*m_Ebeam+10*m_sigmaE;
  double epmin2=2*m_md;
  if (ppmin2>0.0) epmin2=2*sqrt(m_md*m_md+ppmin2*ppmin2);
  if (epmin2>epmax2) epmin2=epmax2;
  int kmax2=m_edist->geti(epmax2);
  int kmin2=m_edist->geti(epmin2);
  assert(kmax2>=kmin2);


  double prob=0.0;
  for (int k=kmin2;k<kmax2;k++){
    double ep=m_edist->getX(k);
    double pp=sqrt(ep*ep/4.0-m_md*m_md);

    if ( (fabs(p2-pp)<10.0*sigmap2) && pp!=0.0 ) {
      double w2=(1.0-m_f2a-m_f2b)*p2*
	(exp(-(p2-pp)*(p2-pp)/(2*m_sigmap2*m_sigmap2))-
	 exp(-(p2+pp)*(p2+pp)/(2*m_sigmap2*m_sigmap2)))/
	(sqrt(2*pi)*pp*m_sigmap2);
      if (m_f2a>0.0) {
	//std::cout << "In a"<< std::endl;
	w2+=m_f2a*p2*
	(exp(-(p2-pp)*(p2-pp)/(2*m_sigmap2a*m_sigmap2a))-
	 exp(-(p2+pp)*(p2+pp)/(2*m_sigmap2a*m_sigmap2a)))/
	(sqrt(2*pi)*pp*m_sigmap2a);
      }
      if (m_f2b>0.0) {
	//std::cout << "In b"<< std::endl;
	w2+=m_f2b*p2*
	(exp(-(p2-pp)*(p2-pp)/(2*m_sigmap2b*m_sigmap2b))-
	 exp(-(p2+pp)*(p2+pp)/(2*m_sigmap2b*m_sigmap2b)))/
	  (sqrt(2*pi)*pp*m_sigmap2b);
      }

      if (!(w2>=0)) {
	std::cout << "w2, p2, pp, m_sigmap2:"
		  <<w2<<" "<<p2<<" "<<pp<<" "<<m_sigmap2<<std::endl;
	std::cout << m_f2a<<" "<<m_f2b<<" "<<m_sigmap2a<<" "<<m_sigmap2b<<std::endl;
      }

      assert(w2>=0);

      if (w2>1e-20) {
	    //std::cout << "p, pp:"<<p<<" "<<pp<<" "<<e<<" "<<ep<<std::endl;
	prob+=m_edist->dx()*m_edist->getVal(k)*w2*mbc2/p2;
	    
      }
    }
	
  }

  return prob;

}



double RooDLineShapeImp2D::evaluate(double mbc1, double mbc2){

  static double pi=4*atan(1.0);

  if (!(m_sigmap1a>0.002)) std::cout << "m_sigmap1a:"<<m_sigmap1a<<std::endl;
  if (!(m_sigmap1b>0.002)) std::cout << "m_sigmap1b:"<<m_sigmap1b<<std::endl;
  if (!(m_sigmap2a>0.002)) std::cout << "m_sigmap2a:"<<m_sigmap2a<<std::endl;
  if (!(m_sigmap2b>0.002)) std::cout << "m_sigmap2b:"<<m_sigmap2b<<std::endl;

  assert(m_sigmap1a>0.002);
  assert(m_sigmap1b>0.002);
  assert(m_sigmap2a>0.002);
  assert(m_sigmap2b>0.002);

  //Now do the momentum convolution for mbc

  if (mbc1>=m_Ebeam) return 0.0;
  if (mbc2>=m_Ebeam) return 0.0;


  double p1=sqrt(m_Ebeam*m_Ebeam-mbc1*mbc1);
  //double e1=2*sqrt(m_md*m_md+p1*p1);

  double sigmap1=m_sigmap1;

  if (m_f1a>0&&m_sigmap1a>sigmap1) sigmap1=m_sigmap1a;
  if (m_f1b>0&&m_sigmap1b>sigmap1) sigmap1=m_sigmap1b;

  double ppmin1=p1-10*sigmap1;
  double ppmax1=p1+10*sigmap1;
  double epmax1=2*sqrt(m_md*m_md+ppmax1*ppmax1);
  if (epmax1>m_edist->max()) epmax1=2*m_Ebeam+10*m_sigmaE;
  double epmin1=2*m_md;
  if (ppmin1>0.0) epmin1=2*sqrt(m_md*m_md+ppmin1*ppmin1);
  if (epmin1>epmax1) epmin1=epmax1;
  int kmax1=m_edist->geti(epmax1);
  int kmin1=m_edist->geti(epmin1);
  assert(kmax1>=kmin1);

  double p2=sqrt(m_Ebeam*m_Ebeam-mbc2*mbc2);
  //double e2=2*sqrt(m_md*m_md+p2*p2);

  double sigmap2=m_sigmap2;

  if (m_f2a>0&&m_sigmap2a>sigmap2) sigmap2=m_sigmap2a;
  if (m_f2b>0&&m_sigmap2b>sigmap2) sigmap2=m_sigmap2b;
      

  double ppmin2=p2-10*sigmap2;
  double ppmax2=p2+10*sigmap2;
  double epmax2=2*sqrt(m_md*m_md+ppmax2*ppmax2);
  if (epmax2>m_edist->max()) epmax2=2*m_Ebeam+10*m_sigmaE;
  double epmin2=2*m_md;
  if (ppmin2>0.0) epmin2=2*sqrt(m_md*m_md+ppmin2*ppmin2);
  if (epmin2>epmax2) epmin2=epmax2;

  int kmax2=m_edist->geti(epmax2);
  int kmin2=m_edist->geti(epmin2);
  assert(kmax2>=kmin2);

  int kmax=(kmax1<kmax2)?kmax1:kmax2;
  int kmin=(kmin1>kmin2)?kmin1:kmin2;

  double prob=0.0;
  for (int k=kmin;k<kmax;k++){
    double ep=m_edist->getX(k);
    double pp=sqrt(ep*ep/4.0-m_md*m_md);

    if ( (fabs(p1-pp)<10.0*sigmap1) &&
	 (fabs(p2-pp)<10.0*sigmap2) && pp!=0.0 ) {

      double w1=(1.0-m_f1a-m_f1b)*p1*
	(exp(-(p1-pp)*(p1-pp)/(2*m_sigmap1*m_sigmap1))-
	 exp(-(p1+pp)*(p1+pp)/(2*m_sigmap1*m_sigmap1)))/
	(sqrt(2*pi)*pp*m_sigmap1);
      if (m_f1a>0.0) w1+=m_f1a*p1*
	(exp(-(p1-pp)*(p1-pp)/(2*m_sigmap1a*m_sigmap1a))-
	 exp(-(p1+pp)*(p1+pp)/(2*m_sigmap1a*m_sigmap1a)))/
	(sqrt(2*pi)*pp*m_sigmap1a);
      if (m_f1b>0.0) w1+=m_f1b*p1*
	(exp(-(p1-pp)*(p1-pp)/(2*m_sigmap1b*m_sigmap1b))-
	 exp(-(p1+pp)*(p1+pp)/(2*m_sigmap1b*m_sigmap1b)))/
	(sqrt(2*pi)*pp*m_sigmap1b);

      if (!(w1>=0)) {
	std::cout << "w1, p1, pp, m_sigmap1:"
		  <<w1<<" "<<p1<<" "<<pp<<" "<<m_sigmap1<<std::endl;
      }

      assert(w1>=0);

      double w2=(1.0-m_f2a-m_f2b)*p2*
	(exp(-(p2-pp)*(p2-pp)/(2*m_sigmap2*m_sigmap2))-
	 exp(-(p2+pp)*(p2+pp)/(2*m_sigmap2*m_sigmap2)))/
	(sqrt(2*pi)*pp*m_sigmap2);
      //std::cout << "w2:"<<w2<<std::endl; 
      if (m_f2a>0.0) {
	w2+=m_f2a*p2*
	(exp(-(p2-pp)*(p2-pp)/(2*m_sigmap2a*m_sigmap2a))-
	 exp(-(p2+pp)*(p2+pp)/(2*m_sigmap2a*m_sigmap2a)))/
	(sqrt(2*pi)*pp*m_sigmap2a);
	//std::cout << "In a:"<<m_f2a<<" "<<m_sigmap2a<<std::endl;
	//std::cout << "w2:"<<w2<<std::endl; 
      }
      if (m_f2b>0.0) {
	w2+=m_f2b*p2*
	(exp(-(p2-pp)*(p2-pp)/(2*m_sigmap2b*m_sigmap2b))-
	 exp(-(p2+pp)*(p2+pp)/(2*m_sigmap2b*m_sigmap2b)))/
	(sqrt(2*pi)*pp*m_sigmap2b);
	//std::cout << "In b:"<<m_f2b<<" "<<m_sigmap2b<<std::endl;
	//std::cout << "w2:"<<w2<<std::endl; 
      }

      if (!(w2>=0)) {
	std::cout << "w2, p2, pp, m_sigmap2:"
		  <<w2<<" "<<p2<<" "<<pp<<" "<<m_sigmap2<<std::endl;
      } 
	  
      assert(w2>=0);
      
      if (w1*w2>1e-20) {
	    //std::cout << "p, pp:"<<p<<" "<<pp<<" "<<e<<" "<<ep<<std::endl;
	prob+=m_edist->dx()*m_edist->getVal(k)*w1*w2*mbc1*mbc2/(p1*p2);
	    
      }
    }
	
  }

  return prob;

}



