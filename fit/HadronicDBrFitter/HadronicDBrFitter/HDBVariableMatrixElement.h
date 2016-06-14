#if !defined(HADRONICDBRFITTER_HDBVARIABLEMATRIXELEMENT_H)
#define HADRONICDBRFITTER_HDBVARIABLEMATRIXELEMENT_H
// -*- C++ -*-
//
// Package:     <HadronicDBrFitter>
// Module:      HDBVariableMatrixElement
// 
/**\class HDBVariableMatrixElement HDBVariableMatrixElement.h HadronicDBrFitter/HDBVariableMatrixElement.h

 Description: <one line class summary>

 Usage:
    <usage>

*/
//
// Author:      Werner Sun
// Created:     Mon Mar 29 18:21:23 EST 2004
// $Id$
//
// Revision history
//
// $Log$

// system include files
#include <string>

using namespace std ;

// user include files
#include "CLHEP/Matrix/Matrix.h"
#include "CLHEP/Matrix/Vector.h"

// forward declarations

class HDBVariableMatrixElement
{
      // ---------- friend classes and functions ---------------

   public:
      // ---------- constants, enums and typedefs --------------

      // ---------- Constructors and destructor ----------------
      HDBVariableMatrixElement();
      virtual ~HDBVariableMatrixElement();

      // ---------- member functions ---------------------------

      void setName( const string& aString ) { m_name = aString ; }
      void setComment1( const string& aString ) { m_comment1 = aString ; }
      void setComment2( const string& aString ) { m_comment2 = aString ; }
      void setComment3( const string& aString ) { m_comment3 = aString ; }

      void setConstantVector( const HepVector& aVector )
      { m_constants = aVector ; }
      void setPowerMatrix( const HepMatrix& aMatrix )
      { m_powers = aMatrix ; }

      void expandPowerMatrix( int aNumberColumns ) ;
      void removeParameter( int aParameterNumber ) ;

//       // This offset is added to the value of the element.
//       void setAdditiveOffset( double aOffset ) { m_additiveOffset = aOffset ; }

      // Error, not variance.  This error does not depend on the parameters
      // and is uncorrelated with any other matrix elements.  It gets added
      // in quadrature with the errors calculated by
      // HDBVariableMatrix::errorMatrix() ;
      //
      // This data member was added for the efficiency matrices, each element
      // of which has an uncorrelated uncertainty.  Without this data member,
      // there would be as many parameters as there are matrix elements
      // (which grows as the number of yields to the fourth power), and
      // evaluating the error matrix of the efficiency matrix becomes very
      // time consuming.
      void setUncorrelatedError( double aError )
      { m_uncorrelatedError = aError ; }

      // ---------- const member functions ---------------------

      const string& name() const { return m_name ; }
      const string& comment1() const { return m_comment1 ; }
      const string& comment2() const { return m_comment2 ; }
      const string& comment3() const { return m_comment3 ; }

      // Derivative with respect to a given variable.  Index starts at 0.
      double derivative( int aParameterNumber,
			 const HepVector& aParameterVector ) const ;

      // Vector of derivatives, same dimension as input vector.
      HepVector derivatives( const HepVector& aParameterVector ) const ;

      // The value of this variable, given a set of input parameters
      virtual double value( const HepVector& aParameterVector ) const ;

      const HepVector& constantVector() const { return m_constants ; }
      const HepMatrix& powerMatrix() const { return m_powers ; }

//       const double& additiveOffset() const { return m_additiveOffset ; }
      const double& uncorrelatedError() const { return m_uncorrelatedError ; }

      // ---------- static member functions --------------------

   protected:

      string m_name ;
      string m_comment1 ;
      string m_comment2 ;
      string m_comment3 ;

      // # rows = # of terms in the definition
      HepVector m_constants ;

      // # rows = # of terms in the definition
      // # columns = # of output parameters in fit
      HepMatrix m_powers ;

      // ---------- protected member functions -----------------

      // ---------- protected const member functions -----------

   private:
      // ---------- Constructors and destructor ----------------
//      HDBVariableMatrixElement( const HDBVariableMatrixElement& ); // stop default

      // ---------- assignment operator(s) ---------------------
//      const HDBVariableMatrixElement& operator=( const HDBVariableMatrixElement& ); // stop default

      // ---------- private member functions -------------------

      // ---------- private const member functions -------------

      // ---------- data members -------------------------------
//       double m_additiveOffset ;
      double m_uncorrelatedError ;

      // ---------- static data members ------------------------

};

// inline function definitions

// Uncomment the following lines, if your class is templated 
// and has an implementation file (in the Template directory)
//#if defined(INCLUDE_TEMPLATE_DEFINITIONS)
//# include "HadronicDBrFitter/Template/HDBVariableMatrixElement.cc"
//#endif

#endif /* HADRONICDBRFITTER_HDBVARIABLEMATRIXELEMENT_H */
