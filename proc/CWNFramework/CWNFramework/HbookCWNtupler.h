#if !defined(CWNFRAMEWORK_HBOOKCWNTUPLER_H_)
#define CWNFRAMEWORK_HBOOKCWNTUPLER_H_

// -*- C++ -*-
//
// Package:     CWNFramework
// Module:	HbookCWNtupler
//
// Description: Fills HBOOK column-wise ntuples
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

#include "Experiment/types.h"
#include "CWNFramework/CWNtupler.h"
#include "CWNFramework/CWNTuple.h"

class HbookCWNtupler : public CWNtupler {
  public:
   HbookCWNtupler();
   
   void init(std::string filename, CWNTuple* tupleptr);
   CWNTuple* getNtuplePtr();
   void fill();
   void finalize();
   
  private:
   CWNTuple* tuple;
   static int inited;
   int record_size;
   int ntid;
};

#endif /* CWNFRAMEWORK_HBOOKCWNTUPLER_H_ */
