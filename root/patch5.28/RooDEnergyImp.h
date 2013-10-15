/*****************************************************************************
 * Project: RooFit                                                           *
 * Package: RooFitModels                                                     *
 *    File: $$                                                               *
 * Authors:                                                                  *
 *   WV, Wouter Verkerke, UC Santa Barbara, verkerke@slac.stanford.edu       *
 *   DK, David Kirkby,    UC Irvine,         dkirkby@uci.edu                 *
 *   AR, Anders Ryd,      Cornell U.,        ryd@lepp.cornell.edu            *
 *                                                                           *
 * Copyright (c) 2000-2004, Regents of the University of California          *
 *                          and Stanford University. All rights reserved.    *
 * Copyright (c) 2004,      Cornell University                               *
 *                                                                           *
 * Redistribution and use in source and binary forms,                        *
 * with or without modification, are permitted according to the terms        *
 * listed in LICENSE (http://roofit.sourceforge.net/license.txt)             *
 *****************************************************************************/
#ifndef ROO_DENERGYIMP
#define ROO_DENERGYIMP

#include "TNamed.h"
#include "RooAbsPdf.h"
#include "RooRealProxy.h"
#include "RooParmFcn.h"
#include <vector>

class RooRealVar;


class RooDEnergyImp: public TNamed{

public:

  RooDEnergyImp(double mres, double gamma,double r,
		double sigmaE, double md, double Ebeam,
		double mc, int nbin=1000);

  // mres is psi'' mass ~3.77 GeV
  // gamma is psi'' width ~0.023 GeV
  // r is the interaction radius		
  // Ebeam is the beam energy ~1.885 GeV
  // sigmaE is beamenergy spread ~0.001 GeV
  // md is actuall D mass ~1.869 GeV
  // mc is 0 means data, 1 means MC and -1 means mc for the lineshape
  // nbin is number of bins

  ~RooDEnergyImp();

  double evaluate(double ecm);
	
  int geti(double e) { return edist->geti(e); }
  double getX(int i) { return edist->getX(i); }
  double getVal(int i) { return edist->getVal(i); }
  double getVal(double e) { return edist->getVal(e); }
  double max() { return edist->max(); }
  double dx() { return edist->dx(); 
}
private:

  double BW(double e);

  double h(double emin,double emax,
	   double A, double B, double C);

  void BE(double e, double& A, double& B, double& C);

  double G(double dp);

  double m_mres;
  double m_gamma;
  double m_r;
  double m_sigmaE;
  double m_Ebeam;
  double m_md;
  double m_mc;

  RooParmFcn* edist;

  ClassDef(RooDEnergyImp,0) // Special shape for mBC dist. in psi(3770) decays

};

#endif
