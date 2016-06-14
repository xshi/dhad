#if !defined(HADRONICDBRFITTER_HDBSTANDARDMCINPUTDATA_H)
#define HADRONICDBRFITTER_HDBSTANDARDMCINPUTDATA_H
// -*- C++ -*-
//
// Package:     <HadronicDBrFitter>
// Module:      HDBStandardMCInputData
// 
/**\class HDBStandardMCInputData HDBStandardMCInputData.h HadronicDBrFitter/HDBStandardMCInputData.h

 Description: <one line class summary>

 Usage:
    <usage>

*/
//
// Author:      Werner Sun
// Created:     Wed Mar 31 16:08:04 EST 2004
// $Id$
//
// Revision history
//
// $Log$

// system include files

// user include files
#include "HadronicDBrFitter/HDBStandardInputData.h"

// forward declarations

class HDBStandardMCInputData : public HDBStandardInputData
{
      // ---------- friend classes and functions ---------------

   public:
      // ---------- constants, enums and typedefs --------------

      // ---------- Constructors and destructor ----------------
      HDBStandardMCInputData( bool aSingleTagsExclusive = false );
      virtual ~HDBStandardMCInputData();

      // ---------- member functions ---------------------------
      virtual void initialize( const HepVector& aFitParameters,
			       const HDBVariableVector* aFitPredictions ) ;

      virtual void setEfficiencyParameters( const HepVector& aVector )
      {
	 m_generatedEfficiencyParameters = aVector ;
	 HDBStandardInputData::setEfficiencyParameters( aVector ) ;
      }

      virtual void setBackgroundParameters( const HepVector& aVector )
      {
	 m_generatedBackgroundParameters = aVector ;
	 HDBStandardInputData::setBackgroundParameters( aVector ) ;
      }

      void setTrueCorrectedYields( const HepVector& aCorrectedYields )
      { m_trueCorrectedYields = aCorrectedYields ; }

      // ---------- const member functions ---------------------
      HepMatrix generatedSignalEfficiencyValues() const
      {
	 return m_signalEfficiencyMatrix.values(
	    m_generatedEfficiencyParameters ) ;
      }

      HepMatrix generatedBackgroundEfficiencyValues() const
      {
	 return m_backgroundEfficiencyMatrix.values(
	    m_generatedEfficiencyParameters ) ;
      }

      HepVector generatedBackgroundValues( const HepVector& aFitParameters )
	 const
      {
	 return backgroundValues( m_generatedBackgroundParameters,
				  aFitParameters ) ;
      }

      // ---------- static member functions --------------------
      static double randomGaussian( double aMean, double aSigma ) ;
      static HepVector smearedVector( const HepVector& aTrueValues,
				      const HepVector& aResolutions ) ;
      static HepMatrix uncorrelatedSmearMatrix( HDBEfficiencyMatrix& aMatrix );
      static HepVector uncorrelatedSmearVector( HDBVariableVector& aVector ) ;

   protected:
      // ---------- protected member functions -----------------

      // ---------- protected const member functions -----------

   private:
      // ---------- Constructors and destructor ----------------
      HDBStandardMCInputData( const HDBStandardMCInputData& ); // stop default

      // ---------- assignment operator(s) ---------------------
      const HDBStandardMCInputData& operator=( const HDBStandardMCInputData& ); // stop default

      // ---------- private member functions -------------------

      // ---------- private const member functions -------------

      // ---------- data members -------------------------------
      HepVector m_trueCorrectedYields ;
      HepVector m_generatedEfficiencyParameters ;
      HepVector m_generatedBackgroundParameters ;

      // ---------- static data members ------------------------

};

// inline function definitions

// Uncomment the following lines, if your class is templated 
// and has an implementation file (in the Template directory)
//#if defined(INCLUDE_TEMPLATE_DEFINITIONS)
//# include "HadronicDBrFitter/Template/HDBStandardMCInputData.cc"
//#endif

#endif /* HADRONICDBRFITTER_HDBSTANDARDMCINPUTDATA_H */
