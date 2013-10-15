#if !defined(CWNFRAMEWORK_CWNTUPLE_H)
#define CWNFRAMEWORK_CWNTUPLE_H

// -*- C++ -*-
//
// Package:     CWNFramework
// Module:	CWNTuple
//
// Description: Abstract base class of column-wise ntuples
//
// Usage:
//      [class and public member function
//       documentation goes here]
//
// Author:      A. Trackfinder
// Created:     Thu Jan  1 00:00:01 EST 1996
// $Id$
//
// Revision history
//
// $Log$
// Revision 1.1  2010/05/17 17:43:51  xs32
// add
//
// Revision 1.3  2006/02/24 21:00:52  ponyisi
// Prettify
//
// Revision 1.2  2004/09/24 18:37:01  ponyisi
// Update for coding standards
//

//#include "C++Std/fwd_ostream.h"
//#include <iosfwd>

#include "Experiment/types.h"
#include <string>
#include <vector>
#include <map>

class VarDescriptor {
 public:
  VarDescriptor(char* in_name, char* in_indexvar, char* in_limits,
		void* in_address, int in_type);
  std::string name;
  std::string indexvar; // empty if no index; "var" if index
  std::string limits; // purely a hbook thing; empty if no limits, [a,b] if limits
  void * address;
  int type; // 0 = integer, 1 = real
};

class BlockDescriptor {
  public:
  BlockDescriptor(std::string in_name);
  std::string name;
  std::vector<VarDescriptor> variables;
  void addVar(VarDescriptor& var);
};

struct dummycomp {
  bool operator()(const BlockDescriptor& s1, const BlockDescriptor& s2) const {
    return s1.name < s2.name;
  }
};

class CWNTuple
{
 public:
  typedef std::vector<BlockDescriptor> BD_vec;
  typedef std::vector<VarDescriptor> VD_vec;
  typedef std::map<BlockDescriptor, DABoolean, dummycomp> OptBlockMap;
  enum { INTEGER = 0, FLOAT = 1 };

  CWNTuple();
  virtual void clear()=0;
  virtual BD_vec& getVariables();
  std::string shortName();
  std::string description();
  void setOptBlockStatus(const BlockDescriptor& block, DABoolean status);
  void setOptBlockStatus(const char* blockname, DABoolean status);
  DABoolean getOptBlockStatus(const BlockDescriptor& block);
  
 protected:
  std::string m_shortName;
  std::string m_description;
  BD_vec varList;
  OptBlockMap optBlocks;
};

#endif /* CWNFRAMEWORK_CWNTUPLE_H */
