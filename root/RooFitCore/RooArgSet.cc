/*****************************************************************************
 * Project: RooFit                                                           *
 * Package: RooFitCore                                                       *
 *    File: $Id: RooArgSet.cc,v 1.55 2005/03/22 13:05:14 wverkerke Exp $
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

// -- CLASS DESCRIPTION [CONT] --
// RooArgSet is a container object that can hold multiple RooAbsArg objects.
// The container has set semantics which means that:
//
//  - Every object it contains must have a unique name returned by GetName().
//
//  - Contained objects are not ordered, although the set can be traversed
//    using an iterator returned by createIterator(). The iterator does not
//    necessarily follow the object insertion order.
//
//  - Objects can be retrieved by name only, and not by index.
//
//
// Ownership of contents. 
//
// Unowned objects are inserted with the add() method. Owned objects
// are added with addOwned() or addClone(). A RooArgSet either owns all 
// of it contents, or none, which is determined by the first <add>
// call. Once an ownership status is selected, inappropriate <add> calls
// will return error status. Clearing the list via removeAll() resets the 
// ownership status. Arguments supplied in the constructor are always added 
// as unowned elements.
//
//

#include <iostream>
#include <iomanip>
#include <fstream>
#include "TClass.h"
#include "RooFitCore/RooArgSet.hh"
#include "RooFitCore/RooStreamParser.hh"
#include "RooFitCore/RooFormula.hh"
#include "RooFitCore/RooAbsRealLValue.hh"
#include "RooFitCore/RooAbsCategoryLValue.hh"
#include "RooFitCore/RooStringVar.hh"
#include "RooFitCore/RooTrace.hh"
#include "RooFitCore/RooArgList.hh"
using std::cout;
using std::endl;
using std::fstream;
using std::ifstream;
using std::istream;
using std::ofstream;
using std::ostream;

ClassImp(RooArgSet)
  ;

RooArgSet::RooArgSet() :
  RooAbsCollection()
{
  // Default constructor
}

RooArgSet::RooArgSet(const RooArgList& list) :
  RooAbsCollection(list.GetName())
{
  // Constructor from a RooArgList. If the list contains multiple
  // objects with the same name, only the first is store in the set.
  // Warning messages will be printed for dropped items.

  add(list,kTRUE) ; // verbose to catch duplicate errors
}


RooArgSet::RooArgSet(const char *name) :
  RooAbsCollection(name)
{
  // Empty set constructor
}

RooArgSet::RooArgSet(const RooAbsArg& var1,
		     const char *name) :
  RooAbsCollection(name)
{
  // Constructor for set containing 1 initial object

  add(var1);
}

RooArgSet::RooArgSet(const RooAbsArg& var1, const RooAbsArg& var2,
		     const char *name) :
  RooAbsCollection(name)
{
  // Constructor for set containing 2 initial objects

  add(var1); add(var2);
}

RooArgSet::RooArgSet(const RooAbsArg& var1, const RooAbsArg& var2, 
		     const RooAbsArg& var3,
		     const char *name) :
  RooAbsCollection(name)
{
  // Constructor for set containing 3 initial objects

  add(var1); add(var2); add(var3);
}

RooArgSet::RooArgSet(const RooAbsArg& var1, const RooAbsArg& var2, 
		     const RooAbsArg& var3, const RooAbsArg& var4,
		     const char *name) :
  RooAbsCollection(name)
{
  // Constructor for set containing 4 initial objects

  add(var1); add(var2); add(var3); add(var4);
}

RooArgSet::RooArgSet(const RooAbsArg& var1,
		     const RooAbsArg& var2, const RooAbsArg& var3,
		     const RooAbsArg& var4, const RooAbsArg& var5,
		     const char *name) :
  RooAbsCollection(name)
{
  // Constructor for set containing 5 initial objects

  add(var1); add(var2); add(var3); add(var4); add(var5);
}

RooArgSet::RooArgSet(const RooAbsArg& var1, const RooAbsArg& var2, 
		     const RooAbsArg& var3, const RooAbsArg& var4, 
		     const RooAbsArg& var5, const RooAbsArg& var6,
		     const char *name) :
  RooAbsCollection(name)
{
  // Constructor for set containing 6 initial objects

  add(var1); add(var2); add(var3); add(var4); add(var5); add(var6);
}

RooArgSet::RooArgSet(const RooAbsArg& var1, const RooAbsArg& var2, 
		     const RooAbsArg& var3, const RooAbsArg& var4, 
		     const RooAbsArg& var5, const RooAbsArg& var6, 
		     const RooAbsArg& var7,
		     const char *name) :
  RooAbsCollection(name)
{
  // Constructor for set containing 7 initial objects

  add(var1); add(var2); add(var3); add(var4); add(var5); add(var6); add(var7) ;
}

RooArgSet::RooArgSet(const RooAbsArg& var1, const RooAbsArg& var2, 
		     const RooAbsArg& var3, const RooAbsArg& var4, 
		     const RooAbsArg& var5, const RooAbsArg& var6, 
		     const RooAbsArg& var7, const RooAbsArg& var8,
		     const char *name) :
  RooAbsCollection(name)
{
  // Constructor for set containing 8 initial objects

  add(var1); add(var2); add(var3); add(var4); add(var5); add(var6); add(var7) ;add(var8) ;
}


RooArgSet::RooArgSet(const RooAbsArg& var1, const RooAbsArg& var2, 
		     const RooAbsArg& var3, const RooAbsArg& var4, 
		     const RooAbsArg& var5, const RooAbsArg& var6, 
		     const RooAbsArg& var7, const RooAbsArg& var8,
		     const RooAbsArg& var9, const char *name) :
  RooAbsCollection(name)
{
  // Constructor for set containing 9 initial objects

  add(var1); add(var2); add(var3); add(var4); add(var5); add(var6); add(var7); add(var8); add(var9);
}



RooArgSet::RooArgSet(const TCollection& tcoll, const char* name) :
  RooAbsCollection(name)
{
  // Constructor from a root TCollection. Elements in the collection that
  // do not inherit from RooAbsArg will be skipped. A warning message
  // will be printed for every skipped item.

  TIterator* iter = tcoll.MakeIterator() ;
  TObject* obj ;
  while(obj=iter->Next()) {
    if (!dynamic_cast<RooAbsArg*>(obj)) {
      cout << "RooArgSet::RooArgSet(TCollection) element " << obj->GetName() 
	   << " is not a RooAbsArg, ignored" << endl ;
      continue ;
    }
    add(*(RooAbsArg*)obj) ;
  }
  delete iter ;
}



RooArgSet::RooArgSet(const RooArgSet& other, const char *name) 
  : RooAbsCollection(other,name)
{
  // Copy constructor. Note that a copy of a set is always non-owning,
  // even the source set is owning. To create an owning copy of
  // a set (owning or not), use the snaphot() method.
}



RooArgSet::~RooArgSet() 
{
  // Destructor
}



Bool_t RooArgSet::add(const RooAbsArg& var, Bool_t silent) 
{
  // Add element to non-owning set. The operation will fail if
  // a similarly named object already exists in the set, or
  // the set is specified to own its elements. Eventual error messages
  // can be suppressed with the silent flag
  return checkForDup(var,silent)? kFALSE : RooAbsCollection::add(var,silent) ;
}


Bool_t RooArgSet::addOwned(RooAbsArg& var, Bool_t silent)
{
  // Add element to an owning set. The operation will fail if
  // a similarly named object already exists in the set, or
  // the set is not specified to own its elements. Eventual error messages
  // can be suppressed with the silent flag
  return checkForDup(var,silent)? kFALSE : RooAbsCollection::addOwned(var,silent) ;
}


RooAbsArg* RooArgSet::addClone(const RooAbsArg& var, Bool_t silent) 
{
  // Add clone of specified element to an owning set. If sucessful, the
  // set will own the clone, not the original. The operation will fail if
  // a similarly named object already exists in the set, or
  // the set is not specified to own its elements. Eventual error messages
  // can be suppressed with the silent flag
  return checkForDup(var,silent)? 0 : RooAbsCollection::addClone(var,silent) ;
}



RooAbsArg& RooArgSet::operator[](const char* name) const 
{     
  // Array operator. Named element must exist in set, otherwise
  // code will abort. 
  //
  // When used as lvalue in assignment operations, the element contained in
  // the list will not be changed, only the value of the existing element!
  RooAbsArg* arg = find(name) ;
  if (!arg) {
    cout << "RooArgSet::operator[](" << GetName() << ") ERROR: no element named " << name << " in set" << endl ;
    RooErrorHandler::softAbort() ;
  }
  return *arg ; 
}



Bool_t RooArgSet::checkForDup(const RooAbsArg& var, Bool_t silent) const 
{
  // Check if element with var's name is already in set

  RooAbsArg *other = 0;
  if(other= find(var.GetName())) {
    if(other != &var) {
      if (!silent)
	// print a warning if this variable is not the same one we
	// already have
	cout << ClassName() << "::" << GetName() << "::checkForDup: cannot add second copy of argument \""
	     << var.GetName() << "\"" << endl;
    }
    // don't add duplicates
    return kTRUE;
  }

  return kFALSE ;
}


Double_t RooArgSet::getRealValue(const char* name, Double_t defVal, Bool_t verbose) const
{
  RooAbsArg* raa = find(name) ;
  if (!raa) {
    if (verbose) cout << "RooArgSet::getRealValue(" << GetName() << ") ERROR no object with name '" << name << "' found" << endl ;
    return defVal ;
  }
  RooAbsReal* rar = dynamic_cast<RooAbsReal*>(raa) ;
  if (!rar) {
    if (verbose) cout << "RooArgSet::getRealValue(" << GetName() << ") ERROR object '" << name << "' is not of type RooAbsReal" << endl ;
    return defVal ;
  }
  return rar->getVal() ;
}


Bool_t RooArgSet::setRealValue(const char* name, Double_t newVal, Bool_t verbose) 
{
  RooAbsArg* raa = find(name) ;
  if (!raa) {
    if (verbose) cout << "RooArgSet::setRealValue(" << GetName() << ") ERROR no object with name '" << name << "' found" << endl ;
    return kTRUE ;
  }
  RooAbsRealLValue* rar = dynamic_cast<RooAbsRealLValue*>(raa) ;
  if (!rar) {
    if (verbose) cout << "RooArgSet::setRealValue(" << GetName() << ") ERROR object '" << name << "' is not of type RooAbsRealLValue" << endl ;
    return kTRUE;
  }
  rar->setVal(newVal) ;
  return kFALSE ;
}



const char* RooArgSet::getCatLabel(const char* name, const char* defVal, Bool_t verbose) const
{
  RooAbsArg* raa = find(name) ;
  if (!raa) {
    if (verbose) cout << "RooArgSet::getCatLabel(" << GetName() << ") ERROR no object with name '" << name << "' found" << endl ;
    return defVal ;
  }
  RooAbsCategory* rac = dynamic_cast<RooAbsCategory*>(raa) ;
  if (!rac) {
    if (verbose) cout << "RooArgSet::getCatLabel(" << GetName() << ") ERROR object '" << name << "' is not of type RooAbsCategory" << endl ;
    return defVal ;
  }
  return rac->getLabel() ;
}


Bool_t RooArgSet::setCatLabel(const char* name, const char* newVal, Bool_t verbose) 
{
  RooAbsArg* raa = find(name) ;
  if (!raa) {
    if (verbose) cout << "RooArgSet::setCatLabel(" << GetName() << ") ERROR no object with name '" << name << "' found" << endl ;
    return kTRUE ;
  }
  RooAbsCategoryLValue* rac = dynamic_cast<RooAbsCategoryLValue*>(raa) ;
  if (!rac) {
    if (verbose) cout << "RooArgSet::setCatLabel(" << GetName() << ") ERROR object '" << name << "' is not of type RooAbsCategory" << endl ;
    return kTRUE ;
  }
  rac->setLabel(newVal) ;
  return kFALSE ;
}


Int_t RooArgSet::getCatIndex(const char* name, Int_t defVal, Bool_t verbose) const
{
  RooAbsArg* raa = find(name) ;
  if (!raa) {
    if (verbose) cout << "RooArgSet::getCatLabel(" << GetName() << ") ERROR no object with name '" << name << "' found" << endl ;
    return defVal ;
  }
  RooAbsCategory* rac = dynamic_cast<RooAbsCategory*>(raa) ;
  if (!rac) {
    if (verbose) cout << "RooArgSet::getCatLabel(" << GetName() << ") ERROR object '" << name << "' is not of type RooAbsCategory" << endl ;
    return defVal ;
  }
  return rac->getIndex() ;
}


Bool_t RooArgSet::setCatIndex(const char* name, Int_t newVal, Bool_t verbose) 
{
  RooAbsArg* raa = find(name) ;
  if (!raa) {
    if (verbose) cout << "RooArgSet::setCatLabel(" << GetName() << ") ERROR no object with name '" << name << "' found" << endl ;
    return kTRUE ;
  }
  RooAbsCategoryLValue* rac = dynamic_cast<RooAbsCategoryLValue*>(raa) ;
  if (!rac) {
    if (verbose) cout << "RooArgSet::setCatLabel(" << GetName() << ") ERROR object '" << name << "' is not of type RooAbsCategory" << endl ;
    return kTRUE ;
  }
  rac->setIndex(newVal) ;
  return kFALSE ;
}


const char* RooArgSet::getStringValue(const char* name, const char* defVal, Bool_t verbose) const
{
  RooAbsArg* raa = find(name) ;
  if (!raa) {
    if (verbose) cout << "RooArgSet::getStringValue(" << GetName() << ") ERROR no object with name '" << name << "' found" << endl ;
    return defVal ;
  }
  RooAbsString* ras = dynamic_cast<RooAbsString*>(raa) ;
  if (!ras) {
    if (verbose) cout << "RooArgSet::getStringValue(" << GetName() << ") ERROR object '" << name << "' is not of type RooAbsString" << endl ;
    return defVal ;
  }
  return ras->getVal() ;
}


Bool_t RooArgSet::setStringValue(const char* name, const char* newVal, Bool_t verbose) 
{
  RooAbsArg* raa = find(name) ;
  if (!raa) {
    if (verbose) cout << "RooArgSet::setStringValue(" << GetName() << ") ERROR no object with name '" << name << "' found" << endl ;
    return kTRUE ;
  }
  RooStringVar* ras = dynamic_cast<RooStringVar*>(raa) ;
  if (!ras) {
    if (verbose) cout << "RooArgSet::setStringValue(" << GetName() << ") ERROR object '" << name << "' is not of type RooAbsString" << endl ;
    return kTRUE ;
  }
  ras->setVal(newVal) ;
  return kFALSE ;
}



void RooArgSet::writeToFile(const char* fileName) 
{
  // Write contents of the argset to specified file.
  // See writeToStream() for details
  ofstream ofs(fileName) ;
  if (ofs.fail()) {
    cout << "RooArgSet::writeToFile(" << GetName() << ") error opening file " << fileName << endl ;
    return ;
  }
  writeToStream(ofs,kFALSE) ;
}




Bool_t RooArgSet::readFromFile(const char* fileName, const char* flagReadAtt, const char* section) 
{
  // Read contents of the argset from specified file.
  // See readFromStream() for details
  ifstream ifs(fileName) ;
  if (ifs.fail()) {
    cout << "RooArgSet::readFromFile(" << GetName() << ") error opening file " << fileName << endl ;
    return kTRUE ;
  }
  return readFromStream(ifs,kFALSE,flagReadAtt,section,kTRUE) ;
}



void RooArgSet::writeToStream(ostream& os, Bool_t compact, const char* section) 
{
  // Write the contents of the argset in ASCII form to given stream.
  // 
  // A line is written for each element contained in the form
  // <argName> = <argValue>
  // 
  // The <argValue> part of each element is written by the arguments' 
  // writeToStream() function.

  if (compact) {
    cout << "RooArgSet::writeToStream(" << GetName() << ") compact mode not supported" << endl ;
    return ;
  }

  TIterator *iterator= createIterator();
  RooAbsArg *next = 0;
  while(0 != (next= (RooAbsArg*)iterator->Next())) {
    os << next->GetName() << " = " ;
    next->writeToStream(os,kFALSE) ;
    os << endl ;
  }
  delete iterator;  
}




Bool_t RooArgSet::readFromStream(istream& is, Bool_t compact, const char* flagReadAtt, const char* section, Bool_t verbose) 
{
  // Read the contents of the argset in ASCII form from given stream.
  // 
  // The stream is read to end-of-file and each line is assumed to be
  // of the form
  //
  // <argName> = <argValue>
  // 
  // Lines starting with argNames not matching any element in the list
  // will be ignored with a warning message. In addition limited C++ style 
  // preprocessing and flow control is provided. The following constructions 
  // are recognized:
  //
  // > #include "include.file"       
  // 
  // Include given file, recursive inclusion OK
  // 
  // > if (<boolean_expression>)
  // >   <name> = <value>
  // >   ....
  // > else if (<boolean_expression>)
  //     ....
  // > else
  //     ....
  // > endif
  //
  // All expressions are evaluated by RooFormula, and may involve any of
  // the sets variables. 
  //
  // > echo <Message>
  //
  // Print console message while reading from stream
  //
  // > abort
  //
  // Force termination of read sequence with error status 
  //
  // The value of each argument is read by the arguments readFromStream
  // function.

  if (compact) {
    cout << "RooArgSet::readFromStream(" << GetName() << ") compact mode not supported" << endl ;
    return kTRUE ;
  }

  RooStreamParser parser(is) ;
  parser.setPunctuation("=") ;
  TString token ;
  Bool_t retVal(kFALSE) ;
  
  // Conditional stack and related state variables
  Bool_t anyCondTrue[100] ;
  Bool_t condStack[100] ;
  Bool_t lastLineWasElse=kFALSE ;
  Int_t condStackLevel=0 ;
  condStack[0]=kTRUE ;
  
  // Prepare section processing
  TString sectionHdr("[") ;
  if (section) sectionHdr.Append(section) ;
  sectionHdr.Append("]") ;
  Bool_t inSection(section?kFALSE:kTRUE) ;

  Bool_t reprocessToken = kFALSE ;
  while (1) {

    if (is.eof() || is.fail() || parser.atEOF()) {
      break ;
    }
    
    // Read next token until end of file
    if (!reprocessToken) {
      token = parser.readToken() ;
    }
    reprocessToken = kFALSE ;

    // Skip empty lines 
    if (token.IsNull()) {
      continue ;
    }

    // Process section headers if requested
    if (*token.Data()=='[') {
      TString hdr(token) ;
      const char* last = token.Data() + token.Length() -1 ;
      if (*last != ']') {
	hdr.Append(" ") ;
	hdr.Append(parser.readLine()) ;
      }
//       parser.putBackToken(token) ;
//       token = parser.readLine() ;
      if (section) {
	inSection = !sectionHdr.CompareTo(hdr) ;
      }
      continue ;
    }

    // If section is specified, ignore all data outside specified section
    if (!inSection) {
      parser.zapToEnd() ;
      continue ;
    }

    // Process include directives
    if (!token.CompareTo("include")) {
      if (parser.atEOL()) {
	cout << "RooArgSet::readFromStream(" << GetName() 
	     << "): no filename found after include statement" << endl ;
	return kTRUE ;
      }
      TString filename = parser.readLine() ;
      ifstream incfs(filename) ;
      if (!incfs.good()) {
	cout << "RooArgSet::readFromStream(" << GetName() << "): cannot open include file " << filename << endl ;
	return kTRUE ;
      }
      cout << "RooArgSet::readFromStream(" << GetName() << "): processing include file " 
	   << filename << endl ;
      if (readFromStream(incfs,compact,flagReadAtt,inSection?0:section,verbose)) return kTRUE ;
      continue ;
    }
    
    // Conditional statement evaluation
    if (!token.CompareTo("if")) {
      
      // Extract conditional expressions and check validity
      TString expr = parser.readLine() ;
      RooFormula form(expr,expr,*this) ;
      if (!form.ok()) return kTRUE ;
      
      // Evaluate expression
      Bool_t status = form.eval()?kTRUE:kFALSE ;
      if (lastLineWasElse) {
	anyCondTrue[condStackLevel] |= status ;
	lastLineWasElse=kFALSE ;
      } else {
	condStackLevel++ ;
	anyCondTrue[condStackLevel] = status ;
      }
      condStack[condStackLevel] = status ;
      
      if (verbose) cout << "RooArgSet::readFromStream(" << GetName() 
			<< "): conditional expression " << expr << " = " 
			<< (condStack[condStackLevel]?"true":"false") << endl ;
      continue ; // go to next line
    }
    
    if (!token.CompareTo("else")) {
      // Must have seen an if statement before
      if (condStackLevel==0) {
	cout << "RooArgSet::readFromStream(" << GetName() << "): unmatched 'else'" << endl ;
      }
      
      if (parser.atEOL()) {
	// simple else: process if nothing else was true
	condStack[condStackLevel] = !anyCondTrue[condStackLevel] ; 
	parser.zapToEnd() ;
	continue ;
      } else {
	// if anything follows it should be 'if'
	token = parser.readToken() ;
	if (token.CompareTo("if")) {
	  cout << "RooArgSet::readFromStream(" << GetName() << "): syntax error: 'else " << token << "'" << endl ;
	  return kTRUE ;
	} else {
	  if (anyCondTrue[condStackLevel]) {
	    // No need for further checking, true conditional already processed
	    condStack[condStackLevel] = kFALSE ;
	    parser.zapToEnd() ;
	    continue ;
	  } else {
	    // Process as normal 'if' no true conditional was encountered 
	    reprocessToken = kTRUE ;
	    lastLineWasElse=kTRUE ;
	    continue ;
	  }
	}
      }	
    }
    
    if (!token.CompareTo("endif")) {
      // Must have seen an if statement before
      if (condStackLevel==0) {
	cout << "RooArgSet::readFromStream(" << GetName() << "): unmatched 'endif'" << endl ;
	return kTRUE ;
      }
      
      // Decrease stack by one
      condStackLevel-- ;
      continue ;
    } 
    
    // If current conditional is true
    if (condStack[condStackLevel]) {
      
      // Process echo statements
      if (!token.CompareTo("echo")) {
	TString message = parser.readLine() ;
	cout << "RooArgSet::readFromStream(" << GetName() << "): >> " << message << endl ;
	continue ;
      } 
      
      // Process abort statements
      if (!token.CompareTo("abort")) {
	TString message = parser.readLine() ;
	cout << "RooArgSet::readFromStream(" << GetName() << "): USER ABORT" << endl ;
	return kTRUE ;
      } 
      
      // Interpret the rest as <arg> = <value_expr> 
      RooAbsArg *arg ;

      if ((arg = find(token)) && !arg->getAttribute("Dynamic")) {
	if (parser.expectToken("=",kTRUE)) {
	  parser.zapToEnd() ;
	  retVal=kTRUE ;
	  cout << "RooArgSet::readFromStream(" << GetName() 
	       << "): missing '=' sign: " << arg << endl ;
	  continue ;
	}
	Bool_t argRet = arg->readFromStream(is,kFALSE,verbose) ;	
	if (!argRet && flagReadAtt) arg->setAttribute(flagReadAtt,kTRUE) ;
	retVal |= argRet ;
      } else {
	cout << "RooArgSet::readFromStream(" << GetName() << "): argument " 
	     << token << " not in list, ignored" << endl ;
	parser.zapToEnd() ;
      }
    } else {
      parser.readLine() ;
    }
  }
  
  // Did we fully unwind the conditional stack?
  if (condStackLevel!=0) {
    cout << "RooArgSet::readFromStream(" << GetName() << "): missing 'endif'" << endl ;
    return kTRUE ;
  }
  
  return retVal ;
}



