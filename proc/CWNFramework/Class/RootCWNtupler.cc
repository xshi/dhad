// -*- C++ -*-
//
// Package:     CWNFramework
// Module:      RootCWNtupler
//
// Description: Fills ROOT column-wise ntuples
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
// Revision 1.3  2005/06/01 22:16:50  ponyisi
// Fix crash on closing files when file number > 0
//
// Revision 1.2  2004/09/24 18:37:10  ponyisi
// Update for coding standards
//

#include "CWNFramework/RootCWNtupler.h"

#include <string>
#include <cctype>

#include "TFile.h"
#include "TTree.h"
#include "TDirectory.h"
#include "TROOT.h"

using namespace std;

int RootCWNtupler::inited = 0;

RootCWNtupler::RootCWNtupler()
{ ; }

string& local_tolower(string str) {
   char* temp = new char[str.length() + 1];
   strcpy(temp, str.c_str());
   for (int i = 0; i < str.length(); i++) {
      temp[i] = tolower(temp[i]);
   }
   return *(new string(temp));
}

void RootCWNtupler::init(std::string filename, CWNTuple* tupleptr) {
   int istat;

   if (! inited) {
      inited = 1;
   }

   tuple = tupleptr;

   file = new TFile(filename.c_str(), "RECREATE");
   tree = new TTree(tuple->shortName().c_str(), tuple->description().c_str(), 1);
   const CWNTuple::BD_vec& blocks = tuple->getVariables();
   for (CWNTuple::BD_vec::const_iterator blIter = blocks.begin();
	blIter != blocks.end(); blIter++) {
      if (tuple->getOptBlockStatus(*blIter)) {
	 const CWNTuple::VD_vec& vars = blIter->variables;
	 for(CWNTuple::VD_vec::const_iterator varIter = vars.begin();
	     varIter != vars.end(); varIter++) {
	    string lcname = local_tolower(varIter->name);
	    string lcindexvar = local_tolower(varIter->indexvar);
	    if (lcindexvar.length() != 0) {
	       lcindexvar = '[' + lcindexvar + ']';
	    }
	    const string& leaftype = varIter->type == 0 ? string("/I") : string("/F");
	    tree->Branch(lcname.c_str(), varIter->address, 
			 (lcname + lcindexvar + leaftype).c_str());
	 }
      }
   }
   tree->Print();
}

CWNTuple* RootCWNtupler::getNtuplePtr() {
   return tuple;
}

void RootCWNtupler::fill() {
   tree->Fill();
}

void RootCWNtupler::finalize() {
   tree->GetCurrentFile()->Write();
   tree->GetCurrentFile()->Close();
}
