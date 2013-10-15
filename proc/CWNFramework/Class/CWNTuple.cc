// -*- C++ -*-
//
// Package:     CWNFramework
// Module:	CWNtuple
//
// Description: Abstract base class of column-wise ntuples
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
// Revision 1.2  2004/09/24 18:37:10  ponyisi
// Update for coding standards
//

#include "CWNFramework/CWNTuple.h"


VarDescriptor::VarDescriptor(char* in_name, char* in_indexvar, char* in_limits,
			     void* in_address, int in_type) :
    name(in_name),
    indexvar(in_indexvar),
    limits(in_limits),
    address(in_address),
    type(in_type) { ; }

BlockDescriptor::BlockDescriptor(std::string in_name) :
   name(in_name) { ; }

void BlockDescriptor::addVar(VarDescriptor& var) {
   variables.push_back(var);
}

CWNTuple::CWNTuple() :
   m_shortName("ntuple"),
   m_description("default description") { ; }

std::string CWNTuple::shortName() {
   return m_shortName;
}

std::string CWNTuple::description() {
   return m_description;
}

CWNTuple::BD_vec& CWNTuple::getVariables() {
   return varList;
}

void CWNTuple::setOptBlockStatus(const BlockDescriptor& block, DABoolean status) {
   optBlocks[block] = status;
}

void CWNTuple::setOptBlockStatus(const char* blockname, DABoolean status) {
   for (BD_vec::const_iterator it = varList.begin();
	it != varList.end(); it++) {
      if (it->name == blockname) {
	 setOptBlockStatus(*it, status);
      }
   }
}

DABoolean CWNTuple::getOptBlockStatus(const BlockDescriptor& block) {
   OptBlockMap::const_iterator it = optBlocks.find(block);
   if (it == optBlocks.end()) {
      return true; // If it isn't specified, make it
   } else {
      return it->second;
   }
}
