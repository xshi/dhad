/*****************************************************************************
 * Project: RooFit                                                           *
 * Package: RooFitCore                                                       *
 *    File: $Id: RooBrentRootFinder.cc,v 1.10 2005/02/25 14:22:54 wverkerke Exp $
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

// -- CLASS DESCRIPTION [AUX] --
// Implement the abstract 1-dimensional root finding interface using
// the Brent-Decker method. This implementation is based on the one
// in the GNU scientific library (v0.99).

#include "RooFitCore/RooBrentRootFinder.hh"
#include "RooFitCore/RooAbsFunc.hh"
#include <math.h>
#include <iostream>
using std::cout;
using std::endl;

ClassImp(RooBrentRootFinder)
;


RooBrentRootFinder::RooBrentRootFinder(const RooAbsFunc& function) :
  RooAbsRootFinder(function)
{
}

Bool_t RooBrentRootFinder::findRoot(Double_t &result, Double_t xlo, Double_t xhi, Double_t value) const
{
  // Do the root finding using the Brent-Decker method. Returns a boolean status and
  // loads 'result' with our best guess at the root if true.
  // Prints a warning if the initial interval does not bracket a single
  // root or if the root is not found after a fixed number of iterations.

  Double_t a(xlo),b(xhi);
  Double_t fa= (*_function)(&a) - value;
  Double_t fb= (*_function)(&b) - value;
  if(fb*fa > 0) {
    cout << "RooBrentRootFinder::findRoot: initial interval does not bracket a root: ("
	 << a << "," << b << "), value = " << value << endl;
    return kFALSE;
  }

  Bool_t ac_equal(kFALSE);
  Double_t fc= fb;
  Double_t c(0),d(0),e(0);
  for(Int_t iter= 0; iter <= MaxIterations; iter++) {

    if ((fb < 0 && fc < 0) || (fb > 0 && fc > 0)) {
      // Rename a,b,c and adjust bounding interval d
      ac_equal = kTRUE;
      c = a;
      fc = fa;
      d = b - a;
      e = b - a;
    }
  
    if (fabs (fc) < fabs (fb)) {
      ac_equal = kTRUE;
      a = b;
      b = c;
      c = a;
      fa = fb;
      fb = fc;
      fc = fa;
    }

    Double_t tol = 0.5 * 2.2204460492503131e-16 * fabs(b);
    Double_t m = 0.5 * (c - b);


    if (fb == 0 || fabs(m) <= tol) {
      result= b;
      return kTRUE;
    }
  
    if (fabs (e) < tol || fabs (fa) <= fabs (fb)) {
      // Bounds decreasing too slowly: use bisection
      d = m;
      e = m;
    }
    else {
      // Attempt inverse cubic interpolation
      Double_t p, q, r;
      Double_t s = fb / fa;
      
      if (ac_equal) {
	p = 2 * m * s;
	q = 1 - s;
      }
      else {
	q = fa / fc;
	r = fb / fc;
	p = s * (2 * m * q * (q - r) - (b - a) * (r - 1));
	q = (q - 1) * (r - 1) * (s - 1);
      }
      // Check whether we are in bounds
      if (p > 0) {
	q = -q;
      }
      else {
	p = -p;
      }
      
      Double_t min1= 3 * m * q - fabs (tol * q);
      Double_t min2= fabs (e * q);
      if (2 * p < (min1 < min2 ? min1 : min2)) {
	// Accept the interpolation
	e = d;
	d = p / q;
      }
      else {
	// Interpolation failed: use bisection.
	d = m;
	e = m;
      }
    }
    // Move last best guess to a
    a = b;
    fa = fb;
    // Evaluate new trial root
    if (fabs (d) > tol) {
      b += d;
    }
    else {
      b += (m > 0 ? +tol : -tol);
    }
    fb= (*_function)(&b) - value;

  }
  // Return our best guess if we run out of iterations
  cout << "RooBrentRootFinder::findRoot: maximum iterations exceeded." << endl;
  result= b;
  return kFALSE;
}
