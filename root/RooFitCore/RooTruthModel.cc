/*****************************************************************************
 * Project: RooFit                                                           *
 * Package: RooFitCore                                                       *
 *    File: $Id: RooTruthModel.cc,v 1.25 2005/02/25 14:23:03 wverkerke Exp $
 * Authors:                                                                  *
 *   WV, Wouter Verkerke, UC Santa Barbara, verkerke@slac.stanford.edu       *
 *   DK, David Kirkby,    UC Irvine,         dkirkby@uci.edu                 *
 *                                                                           *
 * Copyright (c) 2000-2005, Regents of the University of California          *
 *                          and Stanford University. All rights reserved.    *
 *                                                                           *
 * Redistribution and use in source and binary forms,                        *
 * with or without modification, are permitted according to the terms        *
 * listed in LICENSE (http://roofit.sourceforge.net/license.txt)             *
 *****************************************************************************/

// -- CLASS DESCRIPTION [PDF] --
// RooTruthModel is the delta-function resolution model
//
// The truth model supports all basis functions because it evaluates each basis function as  
// as a RooFormulaVar.  The 6 basis functions used in B mixing and decay and 2 basis
// functions used in D mixing have been hand coded for speed.

#include <iostream>
#include "RooFitCore/RooTruthModel.hh"

ClassImp(RooTruthModel) 
;


RooTruthModel::RooTruthModel(const char *name, const char *title, RooRealVar& x) : 
  RooResolutionModel(name,title,x)
{  
  // Constructor

}


RooTruthModel::RooTruthModel(const RooTruthModel& other, const char* name) : 
  RooResolutionModel(other,name)
{
  // Copy constructor
}


RooTruthModel::~RooTruthModel()
{
  // Destructor
}


Int_t RooTruthModel::basisCode(const char* name) const 
{
  // Check for optimized basis functions
  if (!TString("exp(-@0/@1)").CompareTo(name)) return expBasisPlus ;
  if (!TString("exp(@0/@1)").CompareTo(name)) return expBasisMinus ;
  if (!TString("exp(-abs(@0)/@1)").CompareTo(name)) return expBasisSum ;
  if (!TString("exp(-@0/@1)*sin(@0*@2)").CompareTo(name)) return sinBasisPlus ;
  if (!TString("exp(@0/@1)*sin(@0*@2)").CompareTo(name)) return sinBasisMinus ;
  if (!TString("exp(-abs(@0)/@1)*sin(@0*@2)").CompareTo(name)) return sinBasisSum ;
  if (!TString("exp(-@0/@1)*cos(@0*@2)").CompareTo(name)) return cosBasisPlus ;
  if (!TString("exp(@0/@1)*cos(@0*@2)").CompareTo(name)) return cosBasisMinus ;
  if (!TString("exp(-abs(@0)/@1)*cos(@0*@2)").CompareTo(name)) return cosBasisSum ;
  if (!TString("(@0/@1)*exp(-@0/@1)").CompareTo(name)) return linBasisPlus ;
  if (!TString("(@0/@1)*(@0/@1)*exp(-@0/@1)").CompareTo(name)) return quadBasisPlus ;
  if (!TString("exp(-@0/@1)*cosh(@0*@2/2)").CompareTo(name)) return coshBasisPlus;
  if (!TString("exp(@0/@1)*cosh(@0*@2/2)").CompareTo(name)) return coshBasisMinus;
  if (!TString("exp(-abs(@0)/@1)*cosh(@0*@2/2)").CompareTo(name)) return coshBasisSum;
  if (!TString("exp(-@0/@1)*sinh(@0*@2/2)").CompareTo(name)) return sinhBasisPlus;
  if (!TString("exp(@0/@1)*sinh(@0*@2/2)").CompareTo(name)) return sinhBasisMinus;
  if (!TString("exp(-abs(@0)/@1)*sinh(@0*@2/2)").CompareTo(name)) return sinhBasisSum;

  // Truth model is delta function, i.e. convolution integral
  // is basis function, therefore we can handle any basis function
  return genericBasis ;
}




void RooTruthModel::changeBasis(RooFormulaVar* basis) 
{
  // Process change basis function. Since we actually
  // evaluate the basis function object, we need to
  // adjust our client-server links to the basis function here

  // Remove client-server link to old basis
  if (_basis) {
    removeServer(*_basis) ;
  }

  // Change basis pointer and update client-server link
  _basis = basis ;
  if (_basis) {
    addServer(*_basis,kTRUE,kFALSE) ;
  }

  _basisCode = basis?basisCode(basis->GetTitle()):0 ;
}





Double_t RooTruthModel::evaluate() const 
{
  // Evaluate the truth model: a delta function when used as PDF,
  // The basis function itself, when convoluted with a basis function.

  // No basis: delta function
  if (_basisCode == noBasis) {
    if (x==0) return 1 ;
    return 0 ;
  }

  // Generic basis: evaluate basis function object
  if (_basisCode == genericBasis) {
    return basis().getVal() ;
  }

  // Precompiled basis functions
  BasisType basisType = (BasisType)( (_basisCode == 0) ? 0 : (_basisCode/10) + 1 );
  BasisSign basisSign = (BasisSign)( _basisCode - 10*(basisType-1) - 2 ) ;

  // Enforce sign compatibility
  if ((basisSign==Minus && x>0) || 
      (basisSign==Plus  && x<0)) return 0 ;


  Double_t tau = ((RooAbsReal*)basis().getParameter(1))->getVal() ;
  // Return desired basis function
  switch(basisType) {    
  case expBasis: {
    return exp(-fabs(x)/tau) ;
  }
  case sinBasis: {
    Double_t dm = ((RooAbsReal*)basis().getParameter(2))->getVal() ; 
    return exp(-fabs(x)/tau)*sin(x*dm) ;
  }
  case cosBasis: {
    Double_t dm = ((RooAbsReal*)basis().getParameter(2))->getVal() ; 
    return exp(-fabs(x)/tau)*cos(x*dm) ;
  }
  case linBasis: {
    Double_t tscaled = fabs(x)/tau;
    return exp(-tscaled)*tscaled ;
  }
  case quadBasis: {
    Double_t tscaled = fabs(x)/tau;
    return exp(-tscaled)*tscaled*tscaled;
  }  
  case sinhBasis: {
    Double_t dg = ((RooAbsReal*)basis().getParameter(2))->getVal() ; 
    return exp(-fabs(x)/tau)*sinh(x*dg/2) ;
  }
  case coshBasis: {
    Double_t dg = ((RooAbsReal*)basis().getParameter(2))->getVal() ; 
    return exp(-fabs(x)/tau)*cosh(x*dg/2) ;
  }
  default:
    assert(0) ;
  }

  return 0 ;
}



Int_t RooTruthModel::getAnalyticalIntegral(RooArgSet& allVars, RooArgSet& analVars, const char* rangeName) const 
{
  switch(_basisCode) {

  // Analytical integration capability of raw PDF
  case noBasis:
    if (matchArgs(allVars,analVars,convVar())) return 1 ;
    break ;

  // Analytical integration capability of convoluted PDF
  case expBasisPlus: 
  case expBasisMinus:
  case expBasisSum:
  case sinBasisPlus:
  case sinBasisMinus:
  case sinBasisSum:
  case cosBasisPlus:
  case cosBasisMinus:
  case cosBasisSum:
  case linBasisPlus:
  case quadBasisPlus:
  case sinhBasisPlus:
  case sinhBasisMinus:
  case sinhBasisSum:
  case coshBasisPlus:
  case coshBasisMinus:
  case coshBasisSum:
    if (matchArgs(allVars,analVars,convVar())) return 1 ;
    break ;
  }

  return 0 ;
}


Double_t RooTruthModel::analyticalIntegral(Int_t code, const char* rangeName) const 
{
  // Code must be 1
  assert(code==1) ;

  // Unconvoluted PDF
  if (_basisCode==noBasis) return 1 ;

  // Precompiled basis functions
  BasisType basisType = (BasisType)( (_basisCode == 0) ? 0 : (_basisCode/10) + 1 );
  BasisSign basisSign = (BasisSign)( _basisCode - 10*(basisType-1) - 2 ) ;
  //cout << " calling RooTruthModel::analyticalIntegral with basisType " << basisType << endl; 

  Double_t tau = ((RooAbsReal*)basis().getParameter(1))->getVal() ;
  switch (basisType) {
  case expBasis:
    {
      Double_t result(0) ;
      if (tau==0) return 1 ;
      if (basisSign != Minus) result += tau*(1-exp(-x.max(rangeName)/tau)) ;
      if (basisSign != Plus) result += tau*(1-exp(x.min(rangeName)/tau)) ;
      return result ;
    }
  case sinBasis:
    {
      Double_t result(0) ;
      if (tau==0) return 0 ;
      Double_t dm = ((RooAbsReal*)basis().getParameter(2))->getVal() ;
      //if (basisSign != Minus) result += exp(-x.max(rangeName)/tau)*(-1/tau*sin(dm*x.max(rangeName)) - dm*cos(dm*x.max(rangeName))) + 1/tau;
      //if (basisSign != Plus)  result -= exp( x.min(rangeName)/tau)*(-1/tau*sin(dm*(-x.min(rangeName))) - dm*cos(dm*(-x.min(rangeName)))) + 1/tau ;
      if (basisSign != Minus) result += exp(-x.max(rangeName)/tau)*(-1/tau*sin(dm*x.max(rangeName)) - dm*cos(dm*x.max(rangeName))) + dm;  // fixed FMV 08/29/03
      if (basisSign != Plus)  result -= exp( x.min(rangeName)/tau)*(-1/tau*sin(dm*(-x.min(rangeName))) - dm*cos(dm*(-x.min(rangeName)))) + dm ;  // fixed FMV 08/29/03
      return result / (1/(tau*tau) + dm*dm) ;
    }
  case cosBasis:
    {
      Double_t result(0) ;
      if (tau==0) return 1 ;
      Double_t dm = ((RooAbsReal*)basis().getParameter(2))->getVal() ;
      if (basisSign != Minus) result += exp(-x.max(rangeName)/tau)*(-1/tau*cos(dm*x.max(rangeName)) + dm*sin(dm*x.max(rangeName))) + 1/tau ;
      //if (basisSign != Plus)  result += exp( x.min(rangeName)/tau)*(-1/tau*cos(dm*(-x.min(rangeName))) - dm*sin(dm*(-x.min(rangeName)))) + 1/tau ;
      if (basisSign != Plus)  result += exp( x.min(rangeName)/tau)*(-1/tau*cos(dm*(-x.min(rangeName))) + dm*sin(dm*(-x.min(rangeName)))) + 1/tau ; // fixed FMV 08/29/03
      return result / (1/(tau*tau) + dm*dm) ;
    }
  case linBasis:
    {
      if (tau==0) return 0 ;
      Double_t t_max = x.max(rangeName)/tau ;
      return tau*( 1 - (1 + t_max)*exp(-t_max) ) ;
    }
  case quadBasis:
    {
      if (tau==0) return 0 ;
      Double_t t_max = x.max(rangeName)/tau ;
      return tau*( 2 - (2 + (2 + t_max)*t_max)*exp(-t_max) ) ;
    }
  case sinhBasis:
    {
      Double_t result(0) ;
      if (tau==0) return 0 ;
      Double_t dg = ((RooAbsReal*)basis().getParameter(2))->getVal() ;
      Double_t taup = 2*tau/(2-tau*dg);
      Double_t taum = 2*tau/(2+tau*dg);
      if (basisSign != Minus) result += 0.5*( taup*(1-exp(-x.max(rangeName)/taup)) - taum*(1-exp(-x.max(rangeName)/taum)) ) ;
      if (basisSign != Plus)  result -= 0.5*( taup*(1-exp( x.min(rangeName)/taup)) - taum*(1-exp( x.min(rangeName)/taum)) ) ;
      return result ;
    }
  case coshBasis:
    {
      Double_t result(0) ;
      if (tau==0) return 1 ;
      Double_t dg = ((RooAbsReal*)basis().getParameter(2))->getVal() ;
      Double_t taup = 2*tau/(2-tau*dg);
      Double_t taum = 2*tau/(2+tau*dg);
      if (basisSign != Minus) result += 0.5*( taup*(1-exp(-x.max(rangeName)/taup)) + taum*(1-exp(-x.max(rangeName)/taum)) ) ;
      if (basisSign != Plus)  result += 0.5*( taup*(1-exp( x.min(rangeName)/taup)) + taum*(1-exp( x.min(rangeName)/taum)) ) ;
      return result ;
    }
  default:
    assert(0) ;
  }

  assert(0) ;
  return 0 ;
}



Int_t RooTruthModel::getGenerator(const RooArgSet& directVars, RooArgSet &generateVars, Bool_t staticInitOK) const
{
  if (matchArgs(directVars,generateVars,x)) return 1 ;  
  return 0 ;
}


void RooTruthModel::generateEvent(Int_t code)
{
  assert(code==1) ;
  Double_t zero(0.) ;
  x = zero ;
  return;
}
