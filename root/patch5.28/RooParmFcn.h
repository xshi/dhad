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
#ifndef ROO_PARMFCN
#define ROO_PARMFCN

#include "TNamed.h"
#include <vector>
#include <string>
#include <assert.h>

class RooParmFcn: public TNamed{

public:

  RooParmFcn(std::string name, int nbin,double xmin,double xmax);

  double getVal(double x);

  double getVal(int i);
  
  double getX(int i);

  double max() { return m_xmax; }

  double dx() { return m_dx; }

  int geti(double );
  
  void set(int i, double val);

  void print();

  void normalize();

private:
  
  std::string m_name;
  int m_nbin;
  double m_xmin;
  double m_xmax;
  double m_dx;

  std::vector<double> m_val;
  std::vector<double> m_a;
  std::vector<double> m_b;
  std::vector<double> m_c;
  std::vector<double> m_d;

  std::vector<bool> m_cache;

  ClassDef(RooParmFcn,0) 

};


#endif
