#if !defined(HADRONICDBRFITTER_HDBPARAMETERDATA_H)
#define HADRONICDBRFITTER_HDBPARAMETERDATA_H
// -*- C++ -*-
//
// Package:     <HadronicDBrFitter>
// Module:      HDBParameterData
// 
/**\class HDBParameterData HDBParameterData.h HadronicDBrFitter/HDBParameterData.h

 Description: <one line class summary>

 Usage:
    <usage>

*/
//
// Author:      Werner Sun
// Created:     Thu Jan 19 15:39:28 EST 2006
// $Id$
//
// Revision history
//
// $Log$

// system include files
#include <vector>
#include <string>

using namespace std ;

// user include files
#include "HadronicDBrFitter/HDBData.h"

// forward declarations

class HDBParameterData : public HDBData
{
      // ---------- friend classes and functions ---------------

   public:
      // ---------- constants, enums and typedefs --------------

      // ---------- Constructors and destructor ----------------
      HDBParameterData();
      HDBParameterData( const HepVector& aValues,
			const HepSymMatrix& aErrorMatrix,
			const vector< string >& aParameterNames ) ; 
      virtual ~HDBParameterData();

      // ---------- member functions ---------------------------
      virtual void clearValuesAndErrorMatrix() ;

      // Also inverts error matrix and stores it.
      virtual void setValuesAndErrorMatrix(
         const HepVector& aValues,
         const HepSymMatrix& aErrorMatrix,
	 const vector< string >& aParameterNames ) ;

      // ---------- const member functions ---------------------

      // This function expands the values and error matrix inverse to
      // a larger vector and matrix (size = length of vector<string>),
      // and the correspondence between parameters is given by matching
      // names between the internal and external list.  The extra rows
      // and columns are filled with zeros.
      virtual void expandedValuesAndErrorInverse(
	 const vector< string >& aFitParameterNames,
	 HepVector& aValuesToFill,
	 HepSymMatrix& aErrorInverseToFill ) const ;

      // ---------- static member functions --------------------

   protected:
      // ---------- protected member functions -----------------

      // ---------- protected const member functions -----------

   private:
      // ---------- Constructors and destructor ----------------
//      HDBParameterData( const HDBParameterData& ); // stop default

      // ---------- assignment operator(s) ---------------------
      const HDBParameterData& operator=( const HDBParameterData& ); // stop default

      // ---------- private member functions -------------------

      HepSymMatrix m_errorInverse ;
      vector< string > m_parameterNames ;

      // ---------- private const member functions -------------

      // ---------- data members -------------------------------

      // ---------- static data members ------------------------

};

// inline function definitions

// Uncomment the following lines, if your class is templated 
// and has an implementation file (in the Template directory)
//#if defined(INCLUDE_TEMPLATE_DEFINITIONS)
//# include "HadronicDBrFitter/Template/HDBParameterData.cc"
//#endif

#endif /* HADRONICDBRFITTER_HDBPARAMETERDATA_H */
