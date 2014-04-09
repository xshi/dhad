/*****************************************************************************
 * Project: RooFit                                                           *
 * Package: RooFitCore                                                       *
 *    File: $Id: RooHist.cc,v 1.28 2005/02/25 14:22:57 wverkerke Exp $
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
// A RooHist is a graphical representation of binned data based on the
// TGraphAsymmErrors class. Error bars are calculated using either Poisson
// or Binomial statistics.

#include "RooFitCore/RooHist.hh"
#include "RooFitCore/RooHistError.hh"
#include "RooFitCore/RooCurve.hh"

#include "TH1.h"
#include <iostream>
#include <iomanip>
#include <math.h>
using std::cout;
using std::endl;
using std::ostream;
using std::setw;

ClassImp(RooHist)

RooHist::RooHist(Double_t nominalBinWidth, Double_t nSigma, Double_t xErrorFrac) :
  TGraphAsymmErrors(), _nominalBinWidth(nominalBinWidth), _nSigma(nSigma), _rawEntries(-1)
{
  // Create an empty histogram that can be filled with the addBin()
  // and addAsymmetryBin() methods. Use the optional parameter to
  // specify the confidence level in units of sigma to use for
  // calculating error bars. The nominal bin width specifies the
  // default used by addBin(), and is used to set the relative
  // normalization of bins with different widths.

  initialize();
}

RooHist::RooHist(const TH1 &data, Double_t nominalBinWidth, Double_t nSigma, RooAbsData::ErrorType etype, Double_t xErrorFrac) :
  TGraphAsymmErrors(), _nominalBinWidth(nominalBinWidth), _nSigma(nSigma), _rawEntries(-1)
{
  // Create a histogram from the contents of the specified TH1 object
  // which may have fixed or variable bin widths. Error bars are
  // calculated using Poisson statistics. Prints a warning and rounds
  // any bins with non-integer contents. Use the optional parameter to
  // specify the confidence level in units of sigma to use for
  // calculating error bars. The nominal bin width specifies the
  // default used by addBin(), and is used to set the relative
  // normalization of bins with different widths. If not set, the
  // nominal bin width is calculated as range/nbins.

  initialize();
  // copy the input histogram's name and title
  SetName(data.GetName());
  SetTitle(data.GetTitle());
  // calculate our nominal bin width if necessary
  if(_nominalBinWidth == 0) {
    const TAxis *axis= ((TH1&)data).GetXaxis();
    if(axis->GetNbins() > 0) _nominalBinWidth= (axis->GetXmax() - axis->GetXmin())/axis->GetNbins();
  }
  // TH1::GetYaxis() is not const (why!?)
  setYAxisLabel(const_cast<TH1&>(data).GetYaxis()->GetTitle());
  
  // initialize our contents from the input histogram's contents
  Int_t nbin= data.GetNbinsX();
  for(Int_t bin= 1; bin <= nbin; bin++) {
    Axis_t x= data.GetBinCenter(bin);
    Stat_t y= data.GetBinContent(bin);
    Stat_t dy = data.GetBinError(bin) ;
    if (etype==RooAbsData::Poisson) {
      addBin(x,roundBin(y),data.GetBinWidth(bin),xErrorFrac);
    } else {
      addBinWithError(x,y,dy,dy,data.GetBinWidth(bin),xErrorFrac);
    }
  }
  // add over/underflow bins to our event count
  _entries+= data.GetBinContent(0) + data.GetBinContent(nbin+1);
}



RooHist::RooHist(const TH1 &data1, const TH1 &data2, Double_t nominalBinWidth, Double_t nSigma, Double_t xErrorFrac) :
  TGraphAsymmErrors(), _nominalBinWidth(nominalBinWidth), _nSigma(nSigma), _rawEntries(-1)
{
  // Create a histogram from the asymmetry between the specified TH1 objects
  // which may have fixed or variable bin widths, but which must both have
  // the same binning. The asymmetry is calculated as (1-2)/(1+2). Error bars are
  // calculated using Binomial statistics. Prints a warning and rounds
  // any bins with non-integer contents. Use the optional parameter to
  // specify the confidence level in units of sigma to use for
  // calculating error bars. The nominal bin width specifies the
  // default used by addAsymmetryBin(), and is used to set the relative
  // normalization of bins with different widths. If not set, the
  // nominal bin width is calculated as range/nbins.

  initialize();
  // copy the first input histogram's name and title
  SetName(data1.GetName());
  SetTitle(data1.GetTitle());
  // calculate our nominal bin width if necessary
  if(_nominalBinWidth == 0) {
    const TAxis *axis= ((TH1&)data1).GetXaxis();
    if(axis->GetNbins() > 0) _nominalBinWidth= (axis->GetXmax() - axis->GetXmin())/axis->GetNbins();
  }
  setYAxisLabel(Form("Asymmetry (%s - %s)/(%s + %s)",
		     data1.GetName(),data2.GetName(),data1.GetName(),data2.GetName()));
  // initialize our contents from the input histogram contents
  Int_t nbin= data1.GetNbinsX();
  if(data2.GetNbinsX() != nbin) {
    cout << "RooHist::RooHist: histograms have different number of bins" << endl;
    return;
  }
  for(Int_t bin= 1; bin <= nbin; bin++) {
    Axis_t x= data1.GetBinCenter(bin);
    if(fabs(data2.GetBinCenter(bin)-x)>1e-10) {
      cout << "RooHist::RooHist: histograms have different centers for bin " << bin << endl;
    }
    Stat_t y1= data1.GetBinContent(bin);
    Stat_t y2= data2.GetBinContent(bin);
    addAsymmetryBin(x,roundBin(y1),roundBin(y2),data1.GetBinWidth(bin),xErrorFrac);
  }
  // we do not have a meaningful number of entries
  _entries= -1;
}


RooHist::RooHist(const RooHist& hist1, const RooHist& hist2, Double_t wgt1, Double_t wgt2, RooAbsData::ErrorType etype, Double_t xErrorFrac) : _rawEntries(-1){
  // Create histogram as sum of two existing histograms. If Poisson errors are selected the histograms are
  // added and Poisson confidence intervals are calculated for the summed content. If wgt1 and wgt2 are not
  // 1 in this mode, a warning message is printed. If SumW2 errors are selectd the histograms are added
  // and the histograms errors are added in quadrature, taking the weights into account.

  // Initialize the histogram
  initialize() ;
     
  // Copy all non-content properties from hist1
  SetName(hist1.GetName()) ;
  SetTitle(hist1.GetTitle()) ;  
  _nominalBinWidth=hist1._nominalBinWidth ;
  _nSigma=hist1._nSigma ;
  setYAxisLabel(hist1.getYAxisLabel()) ;

  if (!hist1.hasIdenticalBinning(hist2)) {
    cout << "RooHist::RooHist input histograms have incompatible binning, combined histogram will remain empty" << endl ;
    return ;
  }

  if (etype==RooAbsData::Poisson) {
    // Add histograms with Poisson errors

    // Issue warning if weights are not 1
    if (wgt1!=1.0 || wgt2 != 1.0) {
      cout << "RooHist::RooHist: WARNING: Poisson errors of weighted sum of two histograms is not well defined! " << endl
	   << "                  Summed histogram bins will rounded to nearest integer for Poisson confidence interval calculation" << endl ;
    }

    // Add histograms, calculate Poisson confidence interval on sum value
    Int_t i,n=hist1.GetN() ;
    for(i=0 ; i<n ; i++) {
      Double_t x1,y1,x2,y2,dx1 ;
      hist1.GetPoint(i,x1,y1) ;
      dx1 = hist1.GetErrorX(i) ;
      hist2.GetPoint(i,x2,y2) ;
      addBin(x1,roundBin(wgt1*y1+wgt2*y2),2*dx1/xErrorFrac,xErrorFrac) ;
    }    

  } else {
    // Add histograms with SumW2 errors

    // Add histograms, calculate combined sum-of-weights error
    Int_t i,n=hist1.GetN() ;
    for(i=0 ; i<n ; i++) {
      Double_t x1,y1,x2,y2,dx1,dy1,dy2 ;
      hist1.GetPoint(i,x1,y1) ;
      dx1 = hist1.GetErrorX(i) ;
      dy1 = hist1.GetErrorY(i) ;
      dy2 = hist2.GetErrorY(i) ;
      hist2.GetPoint(i,x2,y2) ;
      Double_t dy = sqrt(wgt1*wgt1*dy1*dy1+wgt2*wgt2*dy2*dy2) ;
      addBinWithError(x1,wgt1*y1+wgt2*y2,dy,dy,2*dx1/xErrorFrac,xErrorFrac) ;
    }       
  }

}

void RooHist::initialize() {
  // Perform common initialization for all constructors.

  SetMarkerStyle(8);
  _entries= 0;
}

Double_t RooHist::getFitRangeNEvt() const {
  return (_rawEntries==-1 ? _entries : _rawEntries) ;
}

Double_t RooHist::getFitRangeBinW() const {
  return _nominalBinWidth ;
}


Int_t RooHist::roundBin(Double_t y) {
  // Return the nearest positive integer to the input value
  // and print a warning if an adjustment is required.

  if(y < 0) {
    cout << fName << "::roundBin: rounding negative bin contents to zero: " << y << endl;
    return 0;
  }
  Int_t n= (Int_t)(y+0.5);
  if(fabs(y-n)>1e-6) {
    cout << fName << "::roundBin: rounding non-integer bin contents: " << y << endl;
  }
  return n;
}

void RooHist::addBin(Axis_t binCenter, Int_t n, Double_t binWidth, Double_t xErrorFrac) {
  // Add a bin to this histogram with the specified integer bin contents
  // and using an error bar calculated with Poisson statistics. The bin width
  // is used to set the relative scale of bins with different widths.

  Double_t scale= 1;
  if(binWidth > 0) {
    scale= _nominalBinWidth/binWidth;
  }  
  _entries+= n;
  Int_t index= GetN();

  // calculate Poisson errors for this bin
  Double_t ym,yp,dx(0.5*binWidth);
  if(!RooHistError::instance().getPoissonInterval(n,ym,yp,_nSigma)) {
    cout << "RooHist::addBin: unable to add bin with " << n << " events" << endl;
    return;
  }

  SetPoint(index,binCenter,n*scale);
  SetPointError(index,dx*xErrorFrac,dx*xErrorFrac,scale*(n-ym),scale*(yp-n));
  updateYAxisLimits(scale*yp);
  updateYAxisLimits(scale*ym);
}



void RooHist::addBinWithError(Axis_t binCenter, Double_t n, Double_t elow, Double_t ehigh, Double_t binWidth, Double_t xErrorFrac) 
{
  // Add a bin to this histogram with the specified bin contents
  // and error. The bin width is used to set the relative scale of 
  // bins with different widths.

  Double_t scale= 1;
  if(binWidth > 0) {
    scale= _nominalBinWidth/binWidth;
  }  
  _entries+= n;
  Int_t index= GetN();

  Double_t dx(0.5*binWidth) ;
  SetPoint(index,binCenter,n*scale);
  SetPointError(index,dx*xErrorFrac,dx*xErrorFrac,elow*scale,ehigh*scale);
  updateYAxisLimits(scale*(n-elow));
  updateYAxisLimits(scale*(n+ehigh));
}






void RooHist::addAsymmetryBin(Axis_t binCenter, Int_t n1, Int_t n2, Double_t binWidth, Double_t xErrorFrac) {
  // Add a bin to this histogram with the value (n1-n2)/(n1+n2)
  // using an error bar calculated with Binomial statistics.

  Double_t scale= 1;
  if(binWidth > 0) scale= _nominalBinWidth/binWidth;
  Int_t index= GetN();

  // calculate Binomial errors for this bin
  Double_t ym,yp,dx(0.5*binWidth);
  if(!RooHistError::instance().getBinomialInterval(n1,n2,ym,yp,_nSigma)) {
    cout << "RooHist::addAsymmetryBin: unable to calculate binomial error for bin with " << n1 << "," << n2 << " events" << endl;
    return;
  }

  Double_t a= (Double_t)(n1-n2)/(n1+n2);
  SetPoint(index,binCenter,a);
  SetPointError(index,dx*xErrorFrac,dx*xErrorFrac,(a-ym),(yp-a));
  updateYAxisLimits(scale*yp);
  updateYAxisLimits(scale*ym);
}


RooHist::~RooHist() { }


Bool_t RooHist::hasIdenticalBinning(const RooHist& other) const 
{
  // First check if number of bins is the same
  if (GetN() != other.GetN()) {
    return kFALSE ;
  }

  // Next require that all bin centers are the same
  Int_t i ;
  for (i=0 ; i<GetN() ; i++) {
    Double_t x1,x2,y1,y2 ;
    
    GetPoint(i,x1,y1) ;
    other.GetPoint(i,x2,y2) ;

    if (fabs(x1-x2)>1e-10) {
      return kFALSE ;
    }

  }

  return kTRUE ;
}


void RooHist::printToStream(ostream& os, PrintOption opt, TString indent) const {
  // Print info about this histogram to the specified output stream.
  //
  //   Standard: number of entries
  //      Shape: error CL and maximum value
  //    Verbose: print our bin contents and errors

  oneLinePrint(os,*this);
  RooPlotable::printToStream(os,opt,indent);
  if(opt >= Standard) {
    os << indent << "--- RooHist ---" << endl;
    Int_t n= GetN();
    os << indent << "  Contains " << n << " bins" << endl;
    if(opt >= Shape) {
      os << indent << "  Errors calculated at" << _nSigma << "-sigma CL" << endl;
      if(opt >= Verbose) {
	os << indent << "  Bin Contents:" << endl;
	for(Int_t i= 0; i < n; i++) {
	  os << indent << setw(3) << i << ") x= " <<  fX[i];
	  if(fEXhigh[i] > 0 || fEXlow[i] > 0) {
	    os << " +" << fEXhigh[i] << " -" << fEXlow[i];
	  }
	  os << " , y = " << fY[i] << " +" << fEYhigh[i] << " -" << fEYlow[i] << endl;
	}
      }
    }
  }
}



RooHist* RooHist::makePullHist(const RooCurve& curve) const {
  // Make histogram of pulls w.r.t to given curve

  // Copy all non-content properties from hist1
  RooHist* pullHist = new RooHist(_nominalBinWidth) ;
  pullHist->SetName(Form("pull_%s_s",GetName(),curve.GetName())) ;
  pullHist->SetTitle(Form("Pull of %s and %s",GetTitle(),curve.GetTitle())) ;  

  // Determine range of curve 
  Double_t xstart,xstop,y ;
  curve.GetPoint(0,xstart,y) ;
  curve.GetPoint(curve.GetN()-1,xstop,y) ;
  
  // Add histograms, calculate Poisson confidence interval on sum value
  Int_t i,n=GetN() ;
  for(i=0 ; i<n ; i++) {    

    Double_t x,dyl,dyh,y,cy ;
    GetPoint(i,x,y) ;

    // Only calculate pull for bins inside curve range
    if (x<xstart || x>xstop) continue ;

    dyl = GetEYlow()[i] ;
    dyh = GetEYhigh()[i] ;

    cy = curve.interpolate(x) ;

    Double_t pull = y-cy ;
    if (pull>0) {
      pull /= dyl ;
    } else {
      pull /= dyh ;
    }

    pullHist->addBinWithError(x,0,pull<0?-pull:0,pull>0?pull:0,0,0) ;
  }    
  
  return pullHist ;
}
