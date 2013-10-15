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
#ifndef ROO_DLINESHAPEIMP
#define ROO_DLINESHAPEIMP

#include "TNamed.h"
#include <vector>
#include <string>

#include "RooDEnergyImp.h"


class RooDLineShapeImp: public TNamed{

public:

  RooDLineShapeImp(double mres,double gamma,double r,
		double sigmaE,double sigmap,
		double md, double Ebeam, double mc, int nbin=500,
		double mbcmin=1.83);

  // mres is psi'' mass ~3.77 GeV
  // gamma is psi'' width ~0.023 GeV
  // r is the interaction radius
  // sigmaE is beamenergy spread ~0.001 GeV
  // sigmap is momentum resolution ~0.01 geV
  // md is actuall D mass ~1.869 GeV
  // Ebeam is the energy used in calculation of mBC ~ 1.885 GeV
  // mc is 0 means data, 1 means MC and -1 means mc
  // nbin is number of bins
  // mbcmin is minimum mBC, maximum mbc is Ebeam.

  double evaluate(double mbc);


private:


  double m_mres;
  double m_gamma;
  double m_r;
  double m_sigmaE;
  double m_sigmap;
  double m_md;
  double m_Ebeam;
  double m_mc;

  RooParmFcn m_lshape;

  ClassDef(RooDLineShapeImp,0) 

};


#endif
