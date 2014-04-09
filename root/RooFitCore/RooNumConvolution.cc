/*****************************************************************************
 * Project: RooFit                                                           *
 * Package: RooFitCore                                                       *
 *    File: $Id: RooNumConvolution.cc,v 1.2 2005/02/25 14:23:00 wverkerke Exp $
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
// Numeric 1-dimensional convolution operator PDF. This class can convolve any PDF
// with any other PDF
//
// This class should not be used blindly as numeric convolution is computing
// intensive and prone to stability fitting problems. If an analytic convolution
// can be calculated, you should use that or implement it if not available.
// RooNumConvolution implements reasonable defaults that should convolve most
// functions reasonably well, but results strongly depend on the shape of your
// input PDFS so always check your result.
//
// The default integration engine for the numeric convolution is the
// adaptive Gauss-Kronrod method, which empirically seems the most robust
// for this task. You can override the convolution integration settings via
// the RooNumIntConfig object reference returned by the convIntConfig() member
// function
//
// By default the numeric convolution is integrated from -infinity to
// +infinity through a x -> 1/x coordinate transformation of the
// tails. For convolution with a very small bandwidth it may be
// advantageous (for both CPU consumption and stability) if the
// integration domain is limited to a finite range. The function
// setConvolutionWindow(mean,width,scale) allows to set a sliding
// window around the x value to be calculated taking a RooAbsReal
// expression for an offset and a width to be taken around the x
// value. These input expression can be RooFormulaVars or other
// function objects although the 3d 'scale' argument 'scale'
// multiplies the width RooAbsReal expression given in the 2nd
// argument, allowing for an appropriate window definition for most
// cases without need for a RooFormulaVar object: e.g. a Gaussian
// resolution PDF do setConvolutionWindow(gaussMean,gaussSigma,5)
// Note that for a 'wide' Gaussian the -inf to +inf integration
// may converge more quickly than that over a finite range!
//
// The default numeric precision is 1e-7, i.e. the global default for
// numeric integration but you should experiment with this value to
// see if it is sufficient for example by studying the number of function
// calls that MINUIT needs to fit your function as function of the
// convolution precision. 

#include <iostream>
#include "TH2F.h"
#include "RooFitCore/RooNumConvolution.hh"
#include "RooFitCore/RooArgList.hh"
#include "RooFitCore/RooRealVar.hh"
#include "RooFitCore/RooFormulaVar.hh"
#include "RooFitCore/RooCustomizer.hh"
#include "RooFitCore/RooConvIntegrandBinding.hh"
#include "RooFitCore/RooNumIntFactory.hh"
#include "RooFitCore/RooGenContext.hh"
#include "RooFitCore/RooConvGenContext.hh"

using std::cout ;
using std::endl ;


ClassImp(RooNumConvolution)
;


RooNumConvolution::RooNumConvolution(const char *name, const char *title, RooRealVar& convVar, RooAbsReal& pdf, RooAbsReal& resmodel, const RooNumConvolution* proto) : 
  RooAbsReal(name,title), 
  _init(kFALSE),
  _convIntConfig(RooNumIntConfig::defaultConfig()),
  _integrand(0),
  _integrator(0),
  _origVar("origVar","Original Convolution variable",this,convVar),
  _origPdf("origPdf","Original Input PDF",this,pdf),
  _origModel("origModel","Original Resolution model",this,resmodel),
  _ownedClonedPdfSet("ownedClonePdfSet"),
  _ownedClonedModelSet("ownedCloneModelSet"),
  _cloneVar(0),
  _clonePdf(0),
  _cloneModel(0),
  _useWindow(kFALSE),
  _windowScale(1),
  _windowParam("windowParam","Convolution window parameter",this,kFALSE),
  _verboseThresh(2000),
  _doProf(kFALSE),
  _callHist(0)
{
  // Constructor of convolution operator PDF
  // 
  // convVar  :  convolution variable (on which both pdf and resmodel should depend)
  // pdf      :  input 'physics' pdf
  // resmodel :  input 'resultion' pdf
  //
  // output is pdf(x) (X) resmodel(x) = Int [ pdf(x') resmodel (x-x') ] dx'
  //

  // Use Adaptive Gauss-Kronrod integration by default for the convolution integral
  _convIntConfig.method1D().setLabel("RooAdaptiveGaussKronrodIntegrator1D") ;
  _convIntConfig.method1DOpen().setLabel("RooAdaptiveGaussKronrodIntegrator1D") ;

  if (proto) {
    convIntConfig() = proto->convIntConfig() ;
    if (proto->_useWindow) {
      setConvolutionWindow((RooAbsReal&)*proto->_windowParam.at(0),(RooAbsReal&)*proto->_windowParam.at(1),proto->_windowScale) ;
    }
  }
}



RooNumConvolution::RooNumConvolution(const RooNumConvolution& other, const char* name) :
  RooAbsReal(other,name),
  _init(kFALSE),
  _convIntConfig(other._convIntConfig),
  _integrand(0),
  _integrator(0),
  _origVar("origVar",this,other._origVar),
  _origPdf("origPdf",this,other._origPdf),
  _origModel("origModel",this,other._origModel),
  _ownedClonedPdfSet("ownedClonePdfSet"),
  _ownedClonedModelSet("ownedCloneModelSet"),
  _cloneVar(0),
  _clonePdf(0),
  _cloneModel(0),
  _useWindow(other._useWindow),
  _windowScale(other._windowScale),
  _windowParam("windowParam",this,other._windowParam),
  _verboseThresh(other._verboseThresh),
  _doProf(other._doProf),
  _callHist(other._callHist)
{
  // Copy constructor
}


void RooNumConvolution::initialize() const
{
  // Initialization function -- create clone of convVar (x') and deep-copy clones of pdf and
  // model that are connected to x' rather than x (convVar)

  // Start out clean 
  _ownedClonedPdfSet.removeAll() ;
  _ownedClonedModelSet.removeAll() ;

  if (_cloneVar) delete _cloneVar ;

  // Customize a copy of origPdf that is connected to x' rather than x
  // store all cloned components in _clonePdfSet as well as x' itself
  _cloneVar = new RooRealVar(Form("%s_prime",_origVar.arg().GetName()),"Convolution Variable",0) ;

  RooCustomizer mgr1(pdf(),"NumConv_PdfClone") ;
  mgr1.setCloneBranchSet(_ownedClonedPdfSet) ;
  mgr1.replaceArg(var(),*_cloneVar) ;
  _clonePdf = (RooAbsReal*) mgr1.build() ;

  RooCustomizer mgr2(model(),"NumConv_ModelClone") ;
  mgr2.setCloneBranchSet(_ownedClonedModelSet) ;
  mgr2.replaceArg(var(),*_cloneVar) ;
  _cloneModel = (RooAbsReal*) mgr2.build() ;

  // Change name back to original name
  _cloneVar->SetName(var().GetName()) ;
  
  // Create Convolution integrand
  _integrand = new RooConvIntegrandBinding(*_clonePdf,*_cloneModel,*_cloneVar,var(),0) ;
 
  // Instantiate integrator for convolution integrand
  _integrator = RooNumIntFactory::instance().createIntegrator(*_integrand,_convIntConfig,1) ;
  _integrator->setUseIntegrandLimits(kFALSE) ;

  _init = kTRUE ;
}
 



RooNumConvolution::~RooNumConvolution() 
{
  // Destructor
}


Double_t RooNumConvolution::evaluate() const 
{
  // Calculate convolution integral

  // Check if deferred initialization has occurred
  if (!_init) initialize() ;

  // Retrieve current value of convolution variable
  Double_t x = _origVar ;

  // Propagate current normalization set to integrand
  _integrand->setNormalizationSet(_origVar.nset()) ;

  // Adjust convolution integration window
  if (_useWindow) {
    Double_t center = ((RooAbsReal*)_windowParam.at(0))->getVal() ;
    Double_t width = _windowScale * ((RooAbsReal*)_windowParam.at(1))->getVal() ;
    _integrator->setLimits(x-center-width,x-center+width) ;
  } else {
    _integrator->setLimits(-RooNumber::infinity,RooNumber::infinity) ;
  }
  
  // Calculate convolution for present x
  if (_doProf) _integrand->resetNumCall() ;
  Double_t ret = _integrator->integral(&x) ;
  if (_doProf) {
    _callHist->Fill(x,_integrand->numCall()) ;
    if (_integrand->numCall()>_verboseThresh) {
      cout << "RooNumConvolution::eveluate(" << GetName() << ") WARNING convolution integral at x=" << x 
	   << " required " << _integrand->numCall() << " function evaluations" << endl ;
    }
  }

  return ret ;
}


Bool_t RooNumConvolution::redirectServersHook(const RooAbsCollection& newServerList, Bool_t mustReplaceAll, Bool_t nameChange, Bool_t isRecursive) 
{
  // Intercept server redirects. Throw away cache, as figuring out redirections on the cache is an unsolvable problem.   
  _init = kFALSE ;
  return kFALSE ;
}


void RooNumConvolution::clearConvolutionWindow() 
{
  // Removes previously defined convolution window, reverting to convolution from -inf to +inf
  _useWindow = kFALSE ;
  _windowParam.removeAll() ;
}


void RooNumConvolution::setConvolutionWindow(RooAbsReal& centerParam, RooAbsReal& widthParam, Double_t widthScaleFactor) 
{
  // Restrict convolution integral to finite range [ x - C - S*W, x - C + S*W ] 
  // where x is current value of convolution variablem, C = centerParam, W=widthParam and S = widthScaleFactor
  // Inputs centerParam and withParam can be function expressions (RooAbsReal, RooFormulaVar) etc.

  _useWindow = kTRUE ;
  _windowParam.removeAll() ;
  _windowParam.add(centerParam) ;
  _windowParam.add(widthParam) ;
  _windowScale = widthScaleFactor ;
}


void RooNumConvolution::setCallWarning(Int_t threshold) 
{
  // Activate warning messages if number of function calls needed for evaluation of convolution integral 
  // exceeds given threshold

  if (threshold<0) {
    cout << "RooNumConvolution::setCallWarning(" << GetName() << ") ERROR: threshold must be positive, value unchanged" << endl ;
    return ;
  }
  _verboseThresh = threshold ;
}

void RooNumConvolution::setCallProfiling(Bool_t flag, Int_t nbinX, Int_t nbinCall, Int_t nCallHigh) 
{
  // Activate call profile if flag is set to true. A 2-D histogram is kept that stores the required number
  // of function calls versus the value of x, the convolution variable
  //
  // All clones of RooNumConvolution objects will keep logging to the histogram of the original class
  // so that performance of temporary object clones, such as used in e.g. fitting, plotting and generating
  // are all logged in a single place.
  // 
  // Function caller should take ownership of profiling histogram as it is not deleted at the RooNumConvolution dtor
  //
  // Calling this function with flag set to false will deactivate call profiling and delete the profiling histogram

  if (flag) {
    if (_doProf) {
      delete _callHist ;
    }
    _callHist = new TH2F(Form("callHist_%s",GetName()),Form("Call Profiling of RooNumConvolution %s",GetTitle()),
			 nbinX,_origVar.min(),_origVar.max(),
			 nbinCall,0,nCallHigh) ;
    _doProf=kTRUE ;

  } else if (_doProf) {

    delete _callHist ;
    _callHist = 0 ;
    _doProf = kFALSE ;
  }

}


void RooNumConvolution::printCompactTreeHook(ostream& os, const char* indent) 
{
  // Hook function to intercept printCompactTree() calls so that it can print out
  // the content of its private cache in the print sequence
  os << indent << "RooNumConvolution begin cache" << endl ;

  if (_init) {
    _cloneVar->printCompactTree(os,Form("%s[Var]",indent)) ;
    _clonePdf->printCompactTree(os,Form("%s[Pdf]",indent)) ;
    _cloneModel->printCompactTree(os,Form("%s[Mod]",indent)) ;
  }

  os << indent << "RooNumConvolution end cache" << endl ;
}


