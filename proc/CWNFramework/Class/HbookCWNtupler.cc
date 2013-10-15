// -*- C++ -*-
//
// Package:     CWNFramework
// Module:      HbookCWNtupler
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
// Revision 1.3  2006/02/24 21:01:06  ponyisi
// Fixes to make hbook files actually work
//
// Revision 1.2  2004/09/24 18:37:10  ponyisi
// Update for coding standards
//

#include "CWNFramework/HbookCWNtupler.h"

#include <algorithm>
#include <string>
#include <cctype>
#include <string.h>

#include "cfortran.h"
#include "packlib.h"

#include <iostream>
using namespace std;

#define PAWC_SIZE 500000
      
typedef struct { float PAW[PAWC_SIZE]; } PAWC_DEF;
#define PAWC COMMON_BLOCK(PAWC,pawc)
COMMON_BLOCK_DEF(PAWC_DEF,PAWC);
PAWC_DEF PAWC;

int HbookCWNtupler::inited = 0;

HbookCWNtupler::HbookCWNtupler() :
   record_size(4*1024),
   ntid(1) { ; }

string& local_toupper(string str) {
   char* temp = new char[str.length() + 1];
   strcpy(temp, str.c_str());
   for (int i = 0; i < str.length(); i++) {
      temp[i] = toupper(temp[i]);
   }
   return *(new string(temp));
}

void HbookCWNtupler::init(string filename, CWNTuple* tupleptr) {
   int istat;

   if (! inited) {
      HLIMIT(PAWC_SIZE);
      inited = 1;
   }
   
   tuple = tupleptr;
//   report( DEBUG, kFacilityString ) << "here in init()1" << endl;
   
   HROPEN(1,const_cast<char*>("example"),
	  const_cast<char*>(filename.c_str()),
	  const_cast<char*>("N"),record_size,istat);
//   report( DEBUG, kFacilityString ) << "here in init()2" << endl;

   HBNT(ntid, const_cast<char*>(tuple->description().c_str()), 
	const_cast<char*>(" "));

   const CWNTuple::BD_vec& blocks = tuple->getVariables();
   for (CWNTuple::BD_vec::const_iterator blIter = blocks.begin();
	blIter != blocks.end(); blIter++) {
      if (tuple->getOptBlockStatus(*blIter)) {
	 string ucblockname = local_toupper(blIter->name);
	 string blockString("");
	 const CWNTuple::VD_vec& vars = blIter->variables;
	 // stupid hack so I can dereference the pointer later.
	 // They're all four bytes anyway.
	 int* firstAddress = (int*) vars[0].address;
	 for(CWNTuple::VD_vec::const_iterator varIter = vars.begin();
	     varIter != vars.end(); varIter++) {
	    if (blockString.length() != 0) {
	       blockString += ",";
	    }
	    string& ucname = local_toupper(varIter->name);
	    string& ucindexvar = local_toupper(varIter->indexvar);
	    if (ucindexvar.length() != 0) {
	       ucindexvar = "(" + ucindexvar + ")";
	    }
 	    const string& leaftype = varIter->type == CWNTuple::INTEGER ?
 	       string(":I") : string(":R");
	    blockString += ucname + ucindexvar + varIter->limits + leaftype;
	 }
	 HBNAME(ntid, const_cast<char*>(ucblockname.c_str()),
		*firstAddress, const_cast<char*>(blockString.c_str()));
      }
   }

   HLDIR(const_cast<char*>("//PAWC"),
	 const_cast<char*>("TA"));

//   report( DEBUG, kFacilityString ) << "here in init()4" << endl;

}

CWNTuple* HbookCWNtupler::getNtuplePtr() {
   return tuple;
}

void HbookCWNtupler::fill() {
   HFNT(ntid);
}

void HbookCWNtupler::finalize() {
   int icycle;
   HROUT(0,icycle,const_cast<char*>(" "));
   HREND(const_cast<char*>("example"));
//   KUCLOS(1,const_cast<char*>(" "),1);
}
