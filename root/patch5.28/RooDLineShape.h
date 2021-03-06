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
#ifndef ROO_DLINESHAPE
#define ROO_DLINESHAPE

#include "RooAbsPdf.h"
#include "RooRealProxy.h"
#include <vector>

class RooDLineShapeImp;
class RooRealVar;

class RooDLineShape : public RooAbsPdf {
public:
  RooDLineShape(const char *name, const char *title,
		int npointEbeam, 
		RooAbsReal& _mbc,
		RooAbsReal& _Ebeam,
		RooAbsReal& _mres,
	     	RooAbsReal& _gamma, 
	     	RooAbsReal& _r, 
	     	RooAbsReal& _sigmaE, 
	     	RooAbsReal& _sigmap, 
	     	RooAbsReal& _md, 
		RooAbsReal& _mc);

  RooDLineShape(const RooDLineShape& other, const char* name = 0);
  virtual TObject* clone(const char* newname) const { return new RooDLineShape(*this,newname); }

  inline virtual ~RooDLineShape() { }

  Int_t getAnalyticalIntegral(RooArgSet& allVars, RooArgSet& analVars, const char* rangeName=0) const ;
  Double_t analyticalIntegral(Int_t code, const char* rangeName=0) const ;

protected:

  RooRealProxy mbc;
  RooRealProxy mres;	
  RooRealProxy Ebeam;
  RooRealProxy gamma;
  RooRealProxy r;
  RooRealProxy sigmaE;
  RooRealProxy sigmap;
  RooRealProxy md;
  RooRealProxy mc;

  int m_npointEbeam;

  mutable std::vector<RooDLineShapeImp*> shapes;


  mutable double mres_save, gamma_save, r_save, sigmaE_save, sigmap_save, 
	md_save;

  Double_t evaluate() const;

private:

  ClassDef(RooDLineShape,0) // Special shape for mBC dist. in psi(3770) decays
};

#endif
