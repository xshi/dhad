#include "_REPLACE_BY_PROCDIR_/_REPLACE_BY_TUPLENAME_.h"
#include <string.h>

// -*- C++ -*-
//
// Package:     Tracker
// Module:	Helix
//
// Description: Encapsulates a 5-parameter helix.
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
// Revision 1.2  2004/09/24 18:37:18  ponyisi
// Update for coding standards
//

_REPLACE_BY_TUPLENAME_::_REPLACE_BY_TUPLENAME_() {
   clear();
#include "_REPLACE_BY_PROCDIR_/tuple_init.h"
}

void _REPLACE_BY_TUPLENAME_::clear() {
   memset(&run, 0, (&end_marker - &run)*sizeof(int));
}
