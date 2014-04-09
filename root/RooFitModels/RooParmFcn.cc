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


#include "RooFitModels/RooParmFcn.hh"

ClassImp(RooParmFcn)

static const char rcsid[] =
"$Id: RooCBShape.cc,v 1.7 2004/04/05 22:38:34 wverkerke Exp $";



void RooParmFcn::normalize(){

  //move to integral method

    
  double dm=(m_xmax-m_xmin)/m_nbin;
    
  double sum=0.5*(m_val[0]+m_val[m_nbin]);
  

  for(int i=1;i<m_nbin;i++){
    sum+=m_val[i];
    //std::cout << "Norm:"<<i<<" : "<<m_val[i]<<" "<<getVal(m_xmin+i*dm)<<std::endl;
  }

  //std::cout << "Normalization:"<<sum<<std::endl;

  sum*=dm;
  
  double invsum=1.0/sum;

  for(int i=0;i<m_nbin+1;i++){
    m_val[i]*=invsum;
  }

}


void RooParmFcn::print(){

  for(int i=0;i<m_nbin;i++){
    std::cout << "E:"<<getX(i)<<" "<<getVal(i)<<std::endl;
  }

}


RooParmFcn::RooParmFcn(std::string name, int nbin,double xmin,double xmax){

  m_name=name;
  m_nbin=nbin;
  m_xmin=xmin;
  m_xmax=xmax;
  m_dx=(m_xmax-m_xmin)/nbin;
  m_val.resize(nbin+1);
  m_a.resize(nbin+1);
  m_b.resize(nbin+1);
  m_c.resize(nbin+1);
  m_d.resize(nbin+1);
  m_cache.resize(nbin+1);
  for(int i=0;i<nbin+1;i++){
    m_cache[i]=false;
  }
  

}


int RooParmFcn::geti(double x){

  if (!(x<=m_xmax)) std::cout <<"x, m_xmax:"<<x<<" "<<m_xmax<<std::endl;

  assert(x<=m_xmax);
  assert(x>=m_xmin);

  int i=(int)((x-m_xmin)/m_dx);

  assert(i>=0);
  assert(i<=m_nbin);

  return i;

}

double RooParmFcn::getVal(double x){

  if (x>m_xmax){
    static int count=0;
    count++;
    if (count<100){
      std::cout << "Warning evaluating beyond endpoint, x, m_xmax:"
		<<x<<" "<<m_xmax<<std::endl;
    }
    return 0.0;
  }

  assert(x<=m_xmax);

  if (x<m_xmin) {
    std::cout <<"x, m_xmin, m_xmax:"<<x<<" "<<m_xmin<<" "<<m_xmax<<std::endl;
    std::cout <<"x-m_xmin:"<<x-m_xmin<<std::endl;
  }
  assert(x>=m_xmin);

  int i1=(int)((x-m_xmin)/m_dx);
  int i2=i1+1;


  double x1=getX(i1);
  if (i2>m_nbin) return m_val[i1];
  double x2=getX(i2);

  assert(x>=x1);
  assert(x<=x2);

  assert(i1<m_nbin+1);
  assert(i2<m_nbin+1);

  assert(i1>=0);
  assert(i2>=0);

  //linear interpolation

  int i0=i1-1;
  int i3=i2+1;

  if (i0<0||i3>m_nbin){
    //linear interpolation
    double val1=m_val[i1]+(m_val[i2]-m_val[i1])*(x-x1)/m_dx;
    return val1;
  }    

  if (!m_cache[i1]){

    double x0=getX(i0);
    //double x3=getX(i3);
    
    double y0=m_val[i0];
    double y1=m_val[i1];
    double y2=m_val[i2];
    double y3=m_val[i3];
    
    double d=(3.0*y1+y3-y0-3.0*y2)/(6.0*m_dx*m_dx*m_dx);
    double c=(y0-2.0*y1+y2-d*6.0*m_dx*m_dx*x1)/(2.0*m_dx*m_dx);
    double b=-(y0-y1-c*(x0*x0-x1*x1)-d*(x0*x0*x0-x1*x1*x1))/m_dx;
    double a=y0-b*x0-c*x0*x0-d*x0*x0*x0;
    m_a[i1]=a;
    m_b[i1]=b;
    m_c[i1]=c;
    m_d[i1]=d;
    m_cache[i1]=true;
  }

  //double val=m_a[i1]+x*(m_b[i1]+x*(m_c[i1]+x*m_d[i1]));
  double val=m_a[i1]+x*m_b[i1]+x*x*m_c[i1]+x*x*x*m_d[i1];

  //std::cout << "x,val1, val:"<<x<<" "<<val1<<" "<<val<<" "<<val1-val<<std::endl;

  return val;

}

double RooParmFcn::getVal(int i){

  assert(i>=0);
  assert(i<=m_nbin);

  double val=m_val[i];

  return val;
    
}


double RooParmFcn::getX(int i){
  assert(i>=0);

  if (!(i<=m_nbin)) std::cout << "i,m_nbin:"<<i<<" "<<m_nbin<<std::endl;

  assert(i<=m_nbin);
  return m_xmin+i*m_dx;
}
  
void RooParmFcn::set(int i, double val){
  assert(i>=0);
  assert(i<=m_nbin);
  m_val[i]=val;
}





