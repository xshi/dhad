/*****************************************************************************
 * Project: RooFit                                                           *
 * Package: RooFitCore                                                       *
 *    File: $Id: RooPlot.cc,v 1.41 2005/03/16 15:19:46 wverkerke Exp $
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

// -- CLASS DESCRIPTION [PLOT] --
// A RooPlot is a plot frame and a container for graphics objects
// within that frame. As a frame, it provides the TH1 public interface
// for settting plot ranges, configuring axes, etc. As a container, it
// holds an arbitrary set of objects that might be histograms of data,
// curves representing a fit model, or text labels. Use the Draw()
// method to draw a frame and the objects it contains. Use the various
// add...() methods to add objects to be drawn.  In general, the
// add...() methods create a private copy of the object you pass them
// and return a pointer to this copy. The caller owns the input object
// and this class owns the returned object.


#include "RooFitCore/RooPlot.hh"
#include "RooFitCore/RooAbsReal.hh"
#include "RooFitCore/RooAbsRealLValue.hh"
#include "RooFitCore/RooPlotable.hh"
#include "RooFitCore/RooArgSet.hh"
#include "RooFitCore/RooCurve.hh"
#include "RooFitCore/RooHist.hh"

#include "TAttLine.h"
#include "TAttFill.h"
#include "TAttMarker.h"
#include "TAttText.h"

#include <iostream>
#include <string.h>
#include <assert.h>
using std::cout;
using std::endl;
using std::ostream;

ClassImp(RooPlot)
;

RooPlot::RooPlot(Double_t xmin, Double_t xmax) :
  TH1(histName(),"A RooPlot",100,xmin,xmax), 
  _items(), _plotVarClone(0), _plotVarSet(0), 
  _defYmin(1e-5), _defYmax(1)
{
  // Create an empty frame with the specified x-axis limits.
  initialize();
}


RooPlot::RooPlot(Double_t xmin, Double_t xmax, Double_t ymin, Double_t ymax) :
  TH1(histName(),"A RooPlot",100,xmin,xmax), _items(), _plotVarClone(0), 
  _plotVarSet(0), _defYmin(1e-5), _defYmax(0)
{
  // Create an empty frame with the specified x- and y-axis limits.
  SetMinimum(ymin);
  SetMaximum(ymax);
  initialize();
}

RooPlot::RooPlot(const RooAbsRealLValue &var1, const RooAbsRealLValue &var2) :
  TH1(histName(),"A RooPlot",100,var1.getMin(),var1.getMax()), _items(),
  _plotVarClone(0), _plotVarSet(0), _defYmin(1e-5), _defYmax(0)
{
  // Create an empty frame with the specified x- and y-axis limits
  // and with labels determined by the specified variables.

  if(!var1.hasMin() || !var1.hasMax()) {
    cout << "RooPlot::RooPlot: cannot create plot for variable without finite limits: "
	 << var1.GetName() << endl;
    return;
  }
  if(!var2.hasMin() || !var2.hasMax()) {
    cout << "RooPlot::RooPlot: cannot create plot for variable without finite limits: "
	 << var1.GetName() << endl;
    return;
  }
  SetMinimum(var2.getMin());
  SetMaximum(var2.getMax());
  SetXTitle(var1.getTitle(kTRUE));
  SetYTitle(var2.getTitle(kTRUE));
  initialize();
}

RooPlot::RooPlot(const RooAbsRealLValue &var1, const RooAbsRealLValue &var2,
		 Double_t xmin, Double_t xmax, Double_t ymin, Double_t ymax) :
  TH1(histName(),"A RooPlot",100,xmin,xmax), _items(), _plotVarClone(0), 
  _plotVarSet(0), _defYmin(1e-5), _defYmax(0)
{
  // Create an empty frame with the specified x- and y-axis limits
  // and with labels determined by the specified variables.

  SetMinimum(ymin);
  SetMaximum(ymax);
  SetXTitle(var1.getTitle(kTRUE));
  SetYTitle(var2.getTitle(kTRUE));
  initialize();
}

RooPlot::RooPlot(const char* name, const char* title, const RooAbsRealLValue &var, Double_t xmin, Double_t xmax, Int_t nbins) :
  TH1(name,title,nbins,xmin,xmax), _items(), 
  _plotVarClone(0), _plotVarSet(0), _defYmin(1e-5), _defYmax(1)
{
  // Create an empty frame with its title and x-axis range and label taken
  // from the specified real variable. We keep a clone of the variable
  // so that we do not depend on its lifetime and are decoupled from
  // any later changes to its state.

  // plotVar can be a composite in case of a RooDataSet::plot, need deepClone
  _plotVarSet = (RooArgSet*) RooArgSet(var).snapshot() ;
  _plotVarClone= (RooAbsRealLValue*)_plotVarSet->find(var.GetName()) ;
  
  TString xtitle= var.getTitle(kTRUE);
  SetXTitle(xtitle.Data());

  initialize();

  _normBinWidth = (xmax-xmin)/nbins ; 
}

RooPlot::RooPlot(const RooAbsRealLValue &var, Double_t xmin, Double_t xmax, Int_t nbins) :
  TH1(histName(),"RooPlot",nbins,xmin,xmax), _items(), 
  _plotVarClone(0), _plotVarSet(0), _defYmin(1e-5), _defYmax(1)
{
  // Create an empty frame with its title and x-axis range and label taken
  // from the specified real variable. We keep a clone of the variable
  // so that we do not depend on its lifetime and are decoupled from
  // any later changes to its state.

  // plotVar can be a composite in case of a RooDataSet::plot, need deepClone
  _plotVarSet = (RooArgSet*) RooArgSet(var).snapshot() ;
  _plotVarClone= (RooAbsRealLValue*)_plotVarSet->find(var.GetName()) ;
  
  TString xtitle= var.getTitle(kTRUE);
  SetXTitle(xtitle.Data());

  TString title("A RooPlot of \"");
  title.Append(var.getTitle());
  title.Append("\"");
  SetTitle(title.Data());
  initialize();

  _normBinWidth = (xmax-xmin)/nbins ; 
}

void RooPlot::initialize() {
  // Perform initialization that is common to all constructors.

  // We hold 1D plot objects
  fDimension=1 ;
  // We do not have useful stats of our own
  SetStats(kFALSE);
  // Default vertical padding of our enclosed objects
  setPadFactor(0.05);
  // We don't know our normalization yet
  _normNumEvts= 0;
  _normBinWidth = 0;
  _normVars= 0;
  // Create an iterator over our enclosed objects
  _iterator= _items.MakeIterator();
  assert(0 != _iterator);
}


TString RooPlot::histName() const 
{
  return TString(Form("frame(%08x)",this)) ;
}

RooPlot::~RooPlot() {
  // Delete the items in our container and our iterator.

  _items.Delete();
  delete _iterator;
  if(_plotVarSet) delete _plotVarSet;
  if(_normVars) delete _normVars;
}

void RooPlot::updateNormVars(const RooArgSet &vars) {
  if(0 == _normVars) _normVars= (RooArgSet*) vars.snapshot(kTRUE);
}

Stat_t RooPlot::GetBinContent(Int_t i) const {
  // A plot object is a frame without any bin contents of its own so this
  // method always returns zero.
  return 0;
}

Stat_t RooPlot::GetBinContent(Int_t, Int_t) const
{
  // A plot object is a frame without any bin contents of its own so this
  // method always returns zero.
  return 0;
}

Stat_t RooPlot::GetBinContent(Int_t, Int_t, Int_t) const
{
  // A plot object is a frame without any bin contents of its own so this
  // method always returns zero.
  return 0;
}


void RooPlot::addObject(TObject *obj, Option_t *drawOptions, Bool_t invisible) {
  // Add a generic object to this plot. The specified options will be
  // used to Draw() this object later. The caller transfers ownership
  // of the object with this call, and the object will be deleted
  // when its containing plot object is destroyed.

  if(0 == obj) {
    cout << fName << "::addObject: called with a null pointer" << endl;
    return;
  }
  DrawOpt opt(drawOptions) ;
  opt.invisible = invisible ;
  _items.Add(obj,opt.rawOpt());
}

void RooPlot::addTH1(TH1 *hist, Option_t *drawOptions, Bool_t invisible) {
  // Add a TH1 histogram object to this plot. The specified options
  // will be used to Draw() this object later. "SAME" will be added to
  // the options if they are not already present. Note that histograms
  // should probably not be drawn with error bars since they will not
  // be calculated correctly for bins with low statistics, and will
  // not be accounted for in the automatic y-axis range adjustment. To
  // histogram data in a RooDataSet without these problems, use
  // RooDataSet::plotOn(). The caller transfers ownership of the
  // object with this call, and the object will be deleted when its
  // containing plot object is destroyed.

  if(0 == hist) {
    cout << fName << "::addTH1: called with a null pointer" << endl;
    return;
  }
  // check that this histogram is really 1D
  if(1 != hist->GetDimension()) {
    cout << fName << "::addTH1: cannot plot histogram with "
	 << hist->GetDimension() << " dimensions" << endl;
    return;
  }

  // add option "SAME" if necessary
  TString options(drawOptions);
  options.ToUpper();
  if(!options.Contains("SAME")) options.Append("SAME");

  // update our y-axis label and limits
  updateYAxis(hist->GetMinimum(),hist->GetMaximum(),hist->GetYaxis()->GetTitle());

  // use this histogram's normalization if necessary
  updateFitRangeNorm(hist);

  // add the histogram to our list
  addObject(hist,options.Data(),invisible);
}

void RooPlot::addPlotable(RooPlotable *plotable, Option_t *drawOptions, Bool_t invisible, Bool_t refreshNorm) {
  // Add the specified plotable object to our plot. Increase our y-axis
  // limits to fit this object if necessary. The default lower-limit
  // is zero unless we are plotting an object that takes on negative values.
  // This call transfers ownership of the plotable object to this class.
  // The plotable object will be deleted when this plot object is deleted.

  // update our y-axis label and limits
  updateYAxis(plotable->getYAxisMin(),plotable->getYAxisMax(),plotable->getYAxisLabel());

  // use this object's normalization if necessary
  updateFitRangeNorm(plotable,refreshNorm) ;

  // add this element to our list and remember its drawing option
  TObject *obj= plotable->crossCast();
  if(0 == obj) {
    cout << fName << "::add: cross-cast to TObject failed (nothing added)" << endl;
  }
  else {
    DrawOpt opt(drawOptions) ;
    opt.invisible = invisible ;
    _items.Add(obj,opt.rawOpt());
  }
}

void RooPlot::updateFitRangeNorm(const TH1* hist) {
  // Update our plot normalization over our plot variable's fit range,
  // which will be determined by the first suitable object added to our plot.

  const TAxis* xa = ((TH1*)hist)->GetXaxis() ;
  _normBinWidth = (xa->GetXmax()-xa->GetXmin())/hist->GetNbinsX() ;
  _normNumEvts = hist->GetEntries()/_normBinWidth ;
}

void RooPlot::updateFitRangeNorm(const RooPlotable* rp, Bool_t refreshNorm) {
  // Update our plot normalization over our plot variable's fit range,
  // which will be determined by the first suitable object added to our plot.


  if (_normNumEvts != 0) {

    // If refresh feature is disabled stop here
    if (!refreshNorm) return ;

    Double_t corFac(1.0) ;
    if (dynamic_cast<const RooHist*>(rp)) corFac = _normBinWidth/rp->getFitRangeBinW() ;
    
    
    cout << "RooPlot::updateFitRangeNorm: New event count of " << rp->getFitRangeNEvt()/corFac 
	 << " will supercede previous event count of " << _normNumEvts << " for normalization of PDF projections" << endl ;

    // Nominal bin width (i.e event density) is already locked in by previously drawn histogram
    // scale this histogram to match that density
    _normNumEvts = rp->getFitRangeNEvt()/corFac ;
    //cout << "correction factor = " << _normBinWidth << "/" << rp->getFitRangeBinW() << endl ;
    //cout << "updating numevts to " << _normNumEvts << endl ;
    
  } else {

    _normNumEvts = rp->getFitRangeNEvt() ;
    _normBinWidth = rp->getFitRangeBinW() ;

    //cout << "updating numevts to " << _normNumEvts << endl ;    
  }

}


void RooPlot::updateYAxis(Double_t ymin, Double_t ymax, const char *label) {
  // Update our y-axis limits to accomodate an object whose spread
  // in y is (ymin,ymax). Use the specified y-axis label if we don't
  // have one assigned already.

  // force an implicit lower limit of zero if appropriate
  if(GetMinimum() == 0 && ymin > 0) ymin= 0;

  // calculate padded values
  Double_t ypad= getPadFactor()*(ymax-ymin);
  ymax+= ypad;
  if(ymin < 0) ymin-= ypad;

  // update our limits if necessary
  if(GetMaximum() < ymax) {
    _defYmax = ymax ;
    SetMaximum(ymax);
  }
  if(GetMinimum() > ymin) {
    _defYmin = ymin ;
    SetMinimum(ymin);
  }

  // use the specified y-axis label if we don't have one already
  if(0 == strlen(GetYaxis()->GetTitle())) SetYTitle(label);
}

void RooPlot::Draw(Option_t *options) {
  // Draw this plot and all of the elements it contains. The specified options
  // only apply to the drawing of our frame. The options specified in our add...()
  // methods will be used to draw each object we contain.

  TH1::Draw(options);
  _iterator->Reset();
  TObject *obj = 0;
  while(obj= _iterator->Next()) {
    DrawOpt opt(_iterator->GetOption()) ;
    if (!opt.invisible) {
      obj->Draw(opt.drawOptions);
    }
  }

  TH1::Draw("AXISSAME");
}



void RooPlot::printToStream(ostream& os, PrintOption opt, TString indent) const {
  // Print info about this plot object to the specified stream.
  //
  //  Standard: plot variable and number of contained objects
  //     Shape: list of our contained objects

  oneLinePrint(os,*this);
  if(opt >= Standard) {
    TString deeper(indent);
    deeper.Append("    ");
    if(0 != _plotVarClone) {
      os << indent << "  Plotting ";
      _plotVarClone->printToStream(os,OneLine,deeper);
    }
    else {
      os << indent << "  No plot variable specified" << endl;
    }
    os << indent << "  Plot contains " << _items.GetSize() << " object(s)" << endl;
    if(opt >= Shape) {
      _iterator->Reset();
      TObject *obj = 0;
      while(obj= _iterator->Next()) {
	os << deeper << "(Options=\"" << _iterator->GetOption() << "\") ";
	// Is this a printable object?
	if(obj->IsA()->InheritsFrom(RooPrintable::Class())) {
	  ostream& oldDefault= RooPrintable::defaultStream(&os);
	  obj->Print("1");
	  RooPrintable::defaultStream(&oldDefault);
	}
	// is it a TNamed subclass?
	else if(obj->IsA()->InheritsFrom(TNamed::Class())) {
	  oneLinePrint(os,(const TNamed&)(*obj));
	}
	// at least it is a TObject
	else {
	  os << obj->ClassName() << "::" << obj->GetName() << endl;
	}
      }
    }
  }
}


const char* RooPlot::nameOf(Int_t idx) const 
{
  // Return the name of the object at slot 'idx' in this RooPlot.
  // If the given index is out of range, return a null pointer
  
  TObject* obj = _items.At(idx) ;
  if (!obj) {
    cout << "RooPlot::nameOf(" << GetName() << ") index " << idx << " out of range" << endl ;
    return 0 ;
  }
  return obj->GetName() ;
}


TObject* RooPlot::getObject(Int_t idx) const 
{
  // Return the name of the object at slot 'idx' in this RooPlot.
  // If the given index is out of range, return a null pointer
  
  TObject* obj = _items.At(idx) ;
  if (!obj) {
    cout << "RooPlot::getObject(" << GetName() << ") index " << idx << " out of range" << endl ;
    return 0 ;
  }
  return obj ;
}



TAttLine *RooPlot::getAttLine(const char *name) const {
  // Return a pointer to the line attributes of the named object in this plot,
  // or zero if the named object does not exist or does not have line attributes.

  return dynamic_cast<TAttLine*>(findObject(name));
}

TAttFill *RooPlot::getAttFill(const char *name) const {
  // Return a pointer to the fill attributes of the named object in this plot,
  // or zero if the named object does not exist or does not have fill attributes.

  return dynamic_cast<TAttFill*>(findObject(name));
}

TAttMarker *RooPlot::getAttMarker(const char *name) const {
  // Return a pointer to the marker attributes of the named object in this plot,
  // or zero if the named object does not exist or does not have marker attributes.

  return dynamic_cast<TAttMarker*>(findObject(name));
}

TAttText *RooPlot::getAttText(const char *name) const {
  // Return a pointer to the text attributes of the named object in this plot,
  // or zero if the named object does not exist or does not have text attributes.

  return dynamic_cast<TAttText*>(findObject(name));
}


RooCurve* RooPlot::getCurve(const char* name) const  {
  // Return a RooCurve pointer of the named object in this plot,
  // or zero if the named object does not exist or is not a RooCurve

  return dynamic_cast<RooCurve*>(findObject(name)) ;
}

RooHist* RooPlot::getHist(const char* name) const {
  // Return a RooCurve pointer of the named object in this plot,
  // or zero if the named object does not exist or is not a RooCurve

  return dynamic_cast<RooHist*>(findObject(name)) ;
}

Bool_t RooPlot::drawBefore(const char *before, const char *target) {
  // Change the order in which our contained objects are drawn so that
  // the target object is drawn just before the specified object.
  // Returns kFALSE if either object does not exist.

  return _items.moveBefore(before, target, caller("drawBefore"));
}

Bool_t RooPlot::drawAfter(const char *after, const char *target) {
  // Change the order in which our contained objects are drawn so that
  // the target object is drawn just after the specified object.
  // Returns kFALSE if either object does not exist.

  return _items.moveAfter(after, target, caller("drawAfter"));
}

TObject *RooPlot::findObject(const char *name, const TClass* clas) const {
  // Find the named object in our list of items and return a pointer
  // to it. Return zero and print a warning message if the named
  // object cannot be found. If no name is supplied the last object
  // added is returned.
  //
  // Note that the returned pointer is to a
  // TObject and so will generally need casting. Use the getAtt...()
  // methods to change the drawing style attributes of a contained
  // object directly.

  TObject *obj = 0;
  TObject *ret = 0;

  TIterator* iter = _items.MakeIterator() ;
  while(obj=iter->Next()) {
    if ((!name || !TString(name).CompareTo(obj->GetName())) && 
	(!clas || (obj->IsA()==clas))) {
      ret = obj ;
    }
  }
  delete iter ;
  
  if (ret==0) {
    cout << "RooPlot::findObject(" << GetName() << ") cannot find object " << (name?name:"<last>") << endl ;
  }
  return ret ;
}

TString RooPlot::getDrawOptions(const char *name) const {
  // Return the Draw() options registered for the named object. Return
  // an empty string if the named object cannot be found.

  TObjOptLink *link= _items.findLink(name,caller("getDrawOptions"));
  DrawOpt opt(0 == link ? "" : link->GetOption()) ;
  return TString(opt.drawOptions) ;
}

Bool_t RooPlot::setDrawOptions(const char *name, TString options) {
  // Register the specified drawing options for the named object.
  // Return kFALSE if the named object cannot be found.

  TObjOptLink *link= _items.findLink(name,caller("setDrawOptions"));
  if(0 == link) return kFALSE;

  DrawOpt opt(link->GetOption()) ;
  strcpy(opt.drawOptions,options) ;
  link->SetOption(opt.rawOpt());
  return kTRUE;
}

Bool_t RooPlot::getInvisible(const char* name) const 
{
  TObjOptLink *link= _items.findLink(name,caller("getInvisible"));
  if(0 == link) return kFALSE;

  return DrawOpt(link->GetOption()).invisible ;
}

void RooPlot::setInvisible(const char* name, Bool_t flag) 
{
  TObjOptLink *link= _items.findLink(name,caller("getInvisible"));

  DrawOpt opt ;

  if(link) {
    opt.initialize(link->GetOption()) ;
  }

  opt.invisible = flag ;
  link->SetOption(opt.rawOpt()) ;
}


TString RooPlot::caller(const char *method) const {
  TString name(fName);
  if(strlen(method)) {
    name.Append("::");
    name.Append(method);
  }
  return name;
}


void RooPlot::SetMaximum(Double_t maximum) 
{
  TH1::SetMaximum(maximum==-1111?_defYmax:maximum) ;
}


void RooPlot::SetMinimum(Double_t minimum) 
{
  TH1::SetMinimum(minimum==-1111?_defYmin:minimum) ;
}


Double_t RooPlot::chiSquare(const char* curvename, const char* histname, Int_t nFitParam) const 
{
  // Find curve object
  RooCurve* curve = (RooCurve*) findObject(curvename,RooCurve::Class()) ;
  if (!curve) {
    cout << "RooPlot::chiSquare(" << GetName() << ") cannot find curve" << endl ;
    return -1. ;
  }

  // Find histogram object
  RooHist* hist = (RooHist*) findObject(histname,RooHist::Class()) ;
  if (!hist) {
    cout << "RooPlot::chiSquare(" << GetName() << ") cannot find histogram" << endl ;
    return -1. ;
  }

  return curve->chiSquare(*hist,nFitParam) ;
}

RooHist* RooPlot::pullHist(const char* histname, const char* curvename) const 
{
  // Find curve object
  RooCurve* curve = (RooCurve*) findObject(curvename,RooCurve::Class()) ;
  if (!curve) {
    cout << "RooPlot::pullHist(" << GetName() << ") cannot find curve" << endl ;
    return 0 ;
  }

  // Find histogram object
  RooHist* hist = (RooHist*) findObject(histname,RooHist::Class()) ;
  if (!hist) {
    cout << "RooPlot::pullHist(" << GetName() << ") cannot find histogram" << endl ;
    return 0 ;
  }  

  return hist->makePullHist(*curve) ;
}


void RooPlot::DrawOpt::initialize(const char* rawOpt) 
{
  if (!rawOpt) {
    drawOptions[0] = 0 ;
    invisible=kFALSE ;
    return ;
  }
  strcpy(drawOptions,rawOpt) ;
  strtok(drawOptions,":") ;
  const char* extraOpt = strtok(0,":") ;
  if (extraOpt) {
    invisible =  (extraOpt[0]=='I') ;
  }
}

const char* RooPlot::DrawOpt::rawOpt() const 
{
  static char buf[128] ;
  strcpy(buf,drawOptions) ;
  if (invisible) {
    strcat(buf,":I") ;
  }
  return buf ;
}

