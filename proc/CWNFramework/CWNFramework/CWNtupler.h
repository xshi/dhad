#if !defined(CWNFRAMEWORK_CWNTUPLER_H)
#define CWNFRAMEWORK_CWNTUPLER_H

// -*- C++ -*-
//
// Package:     CWNFramework
// Module:	CWNtupler
//
// Description: Abstract base class of ntuple fillers
//
// Usage:
//      [class and public member function
//       documentation goes here]
//
// Author:      P. Onyisi
// Created:     24 September 2004
// $Id$
//
// Revision history
//
// $Log$
// Revision 1.1  2010/05/17 17:43:51  xs32
// add
//
// Revision 1.2  2004/09/24 18:37:01  ponyisi
// Update for coding standards
//

#include <string>

class CWNTuple;

class CWNtupler {
 public:
  virtual void init(std::string filename, CWNTuple* tupleptr)=0;
  virtual CWNTuple* getNtuplePtr()=0;
  virtual void finalize()=0;
  virtual void fill()=0;
};


#endif /* HADRONICDNTUPLEPROC_CWNTUPLER_H */
