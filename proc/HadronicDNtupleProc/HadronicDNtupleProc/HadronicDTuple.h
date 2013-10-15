#if !defined(HADRONICDNTUPLEPROC_HADRONICDTUPLE_H)
#define HADRONICDNTUPLEPROC_HADRONICDTUPLE_H

// -*- C++ -*-
//
// Package:     HadronicDNtupleProc
// Module:      HadronicDTuple
//
// Description: The HadronicDNtupleProc tuple class
//
// Usage:
//      [class and public member function
//       documentation goes here]
//
// Author:      P. Onyisi
// Created:     Early 2004
// $Id$
//
// Revision history
//
// $Log$
// Revision 1.1  2010/05/17 17:30:24  xs32
// Add
//
// Revision 1.4  2004/09/24 17:24:19  ponyisi
// Split ntupling framework off to CWNFramework
//
// Revision 1.3  2004/03/30 19:44:24  ponyisi
// Eliminate the define 'MAXDCAND'
//
// Revision 1.2  2004/03/20 23:33:04  ryd
// Correct path so that Linux finds header file
//
// Revision 1.1.1.1  2004/03/12 18:43:50  ponyisi
// import source of HadronicDNtupleProc
//

//#include "C++Std/fwd_ostream.h"
//#include <iosfwd>

#include "CWNFramework/CWNTuple.h"

class HadronicDTuple : public CWNTuple {
  public:
   HadronicDTuple();
   void clear();

#include "HadronicDNtupleProc/tuple_cxx_structure.h"

};

#endif /* HADRONICDNTUPLEPROC_HADRONICDNTUPLE_H */
