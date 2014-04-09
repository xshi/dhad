/*****************************************************************************
 * Project: RooFit                                                           *
 * Package: RooFitCore                                                       *
 *    File: $Id: RooSimGenContext.cc,v 1.19 2005/02/25 14:23:02 wverkerke Exp $
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

// -- CLASS DESCRIPTION [AUX} --
// RooSimGenContext is an efficient implementation of the generator context
// specific for RooSimultaneous PDFs when generating more than one of the
// component pdfs.

#include "RooFitCore/RooSimGenContext.hh"
#include "RooFitCore/RooSimultaneous.hh"
#include "RooFitCore/RooRealProxy.hh"
#include "RooFitCore/RooDataSet.hh"
#include "RooFitCore/Roo1DTable.hh"
#include "RooFitCore/RooCategory.hh"
#include "RooFitCore/RooRandom.hh"
using std::cout;
using std::endl;


ClassImp(RooSimGenContext)
;
  
RooSimGenContext::RooSimGenContext(const RooSimultaneous &model, const RooArgSet &vars, 
				   const RooDataSet *prototype, const RooArgSet* auxProto, Bool_t verbose) :
  RooAbsGenContext(model,vars,prototype,auxProto,verbose), _pdf(&model)
{
  // Constructor. Build an array of generator contexts for each component PDF

  // Determine if we are requested to generate the index category
  RooAbsCategory *idxCat = (RooAbsCategory*) model._indexCat.absArg() ;
  RooArgSet pdfVars(vars) ;

  RooArgSet allPdfVars(pdfVars) ;
  if (prototype) allPdfVars.add(*prototype->get(),kTRUE) ;

  if (!idxCat->isDerived()) {
    pdfVars.remove(*idxCat,kTRUE,kTRUE) ;
    Bool_t doGenIdx = allPdfVars.find(idxCat->GetName())?kTRUE:kFALSE ;

    if (!doGenIdx) {
      cout << "RooSimGenContext::ctor(" << GetName() << ") ERROR: This context must"
	   << " generate the index category" << endl ;
      _isValid = kFALSE ;
      return ;
    }
  } else {
    TIterator* sIter = idxCat->serverIterator() ;
    RooAbsArg* server ;
    Bool_t anyServer(kFALSE), allServers(kTRUE) ;
    while(server=(RooAbsArg*)sIter->Next()) {
      if (vars.find(server->GetName())) {
	anyServer=kTRUE ;
	pdfVars.remove(*server,kTRUE,kTRUE) ;
      } else {
	allServers=kFALSE ;
      }
    }
    delete sIter ;    

    if (anyServer && !allServers) {
      cout << "RooSimGenContext::ctor(" << GetName() << ") ERROR: This context must"
	   << " generate all components of a derived index category" << endl ;
      _isValid = kFALSE ;
      return ;
    }
  }

  // We must either have the prototype or extended likelihood to determined
  // the relative fractions of the components
  _haveIdxProto = prototype ? kTRUE : kFALSE ;
  _idxCatName = idxCat->GetName() ;
  if (!_haveIdxProto && !model.canBeExtended()) {
    cout << "RooSimGenContext::ctor(" << GetName() << ") ERROR: Need either extended mode"
	 << " or prototype data to calculate number of events per category" << endl ;
    _isValid = kFALSE ;
    return ;
  }

  // Initialize fraction threshold array (used only in extended mode)
  _numPdf = model._pdfProxyList.GetSize() ;
  _fracThresh = new Double_t[_numPdf+1] ;
  _fracThresh[0] = 0 ;
  
  // Generate index category and all registered PDFS
  TIterator* iter = model._pdfProxyList.MakeIterator() ;
  RooRealProxy* proxy ;
  RooAbsPdf* pdf ;
  Int_t i(1) ;
  while(proxy=(RooRealProxy*)iter->Next()) {
    pdf=(RooAbsPdf*)proxy->absArg() ;

    // Create generator context for this PDF
    RooAbsGenContext* cx = pdf->genContext(pdfVars,prototype,auxProto,verbose) ;

    // Name the context after the associated state and add to list
    cx->SetName(proxy->name()) ;
    _gcList.Add(cx) ;

    // Fill fraction threshold array
    _fracThresh[i] = _fracThresh[i-1] + (_haveIdxProto?0:pdf->expectedEvents(&allPdfVars)) ;
    i++ ;
  }   
  delete iter ;
    
  // Normalize fraction threshold array
  if (!_haveIdxProto) {
    for(i=0 ; i<_numPdf ; i++) 
      _fracThresh[i] /= _fracThresh[_numPdf] ;
  }
  

  // Clone the index category
  _idxCatSet = (RooArgSet*) RooArgSet(model._indexCat.arg()).snapshot(kTRUE) ;
  if (!_idxCatSet) {
    cout << "RooSimGenContext::RooSimGenContext(" << GetName() << ") Couldn't deep-clone index category, abort," << endl ;
    RooErrorHandler::softAbort() ;
  }
  
  _idxCat = (RooAbsCategoryLValue*) _idxCatSet->find(model._indexCat.arg().GetName()) ;
}



RooSimGenContext::~RooSimGenContext()
{
  // Destructor. Delete all owned subgenerator contexts
  delete[] _fracThresh ;
  delete _idxCatSet ;
  _gcList.Delete() ;
}



void RooSimGenContext::initGenerator(const RooArgSet &theEvent)
{
  // Attach the index category clone to the event
  if (_idxCat->isDerived()) {
    _idxCat->recursiveRedirectServers(theEvent,kTRUE) ;
  } else {
    _idxCat = (RooAbsCategoryLValue*) theEvent.find(_idxCat->GetName()) ;
  }

  // Forward initGenerator call to all components
  RooAbsGenContext* gc ;
  TIterator* iter = _gcList.MakeIterator() ;
  while(gc=(RooAbsGenContext*)iter->Next()){
    gc->initGenerator(theEvent) ;
  }
  delete iter;

}



void RooSimGenContext::generateEvent(RooArgSet &theEvent, Int_t remaining)
{
  // Generate event appropriate for current index state. 
  // The index state is taken either from the prototype
  // or generated from the fraction threshold table.

  if (_haveIdxProto) {

    // Lookup pdf from selected prototype index state
    const char* label = _idxCat->getLabel() ;
    RooAbsGenContext* cx = (RooAbsGenContext*)_gcList.FindObject(label) ;
    if (cx) {      
      cx->generateEvent(theEvent,remaining) ;
    } else {
      cout << "RooSimGenContext::generateEvent: WARNING, no PDF to generate event of type " << label << endl ;
    }    

  
  } else {

    // Throw a random number and select PDF from fraction threshold table
    Double_t rand = RooRandom::uniform() ;
    Int_t i=0 ;
    for (i=0 ; i<_numPdf ; i++) {
      if (rand>_fracThresh[i] && rand<_fracThresh[i+1]) {
	RooAbsGenContext* gen= ((RooAbsGenContext*)_gcList.At(i)) ;
	gen->generateEvent(theEvent,remaining) ;
	_idxCat->setLabel(gen->GetName()) ;
	return ;
      }
    }

  }
}

void RooSimGenContext::setProtoDataOrder(Int_t* lut)
{
  RooAbsGenContext::setProtoDataOrder(lut) ;

  TIterator* iter = _gcList.MakeIterator() ;
  RooAbsGenContext* gc ;
  while(gc=(RooAbsGenContext*)iter->Next()) {
    gc->setProtoDataOrder(lut) ;
  }
  delete iter ;
}
