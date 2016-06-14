#if !defined(HADRONICDBRFITTER_HDBSTANDARDINPUTDATA_H)
#define HADRONICDBRFITTER_HDBSTANDARDINPUTDATA_H
// -*- C++ -*-
//
// Package:     <HadronicDBrFitter>
// Module:      HDBStandardInputData
// 
/**\class HDBStandardInputData HDBStandardInputData.h HadronicDBrFitter/HDBStandardInputData.h

 Description: E^-1 ( n - Fb )

 Usage:
    <usage>

*/
//
// Author:      Werner Sun
// Created:     Fri May 21 19:09:24 EDT 2004
// $Id$
//
// Revision history
//
// $Log$

// system include files

// user include files
#include "HadronicDBrFitter/HDBInputData.h"
#include "HadronicDBrFitter/HDBVariableVector.h"
#include "HadronicDBrFitter/HDBEfficiencyMatrix.h"

// forward declarations

class HDBStandardInputData : public HDBInputData
{
      // ---------- friend classes and functions ---------------

   public:
      // ---------- constants, enums and typedefs --------------

      // ---------- Constructors and destructor ----------------
      HDBStandardInputData( bool aSingleTagsExclusive = false ) ;
      virtual ~HDBStandardInputData();

      // ---------- member functions ---------------------------
      virtual void initialize( const HepVector& aFitParameters,
			       const HDBVariableVector* aFitPredictions ) ;
      virtual void update( const HepVector& aFitParameters,
			   const HDBVariableVector* aFitPredictions,
			   bool aFinalPass = false ) ;

      virtual void setDoubleToSingleCrossReference(
	 const vector< pair< int, int > >& aCrossReference,
	 int aNumberSingleTagYields,
	 int aNumberDoubleTagYields )
      {
	 m_doubleToSingleCrossReference = aCrossReference ;
	 m_numberSingleTagYields = aNumberSingleTagYields ;
	 m_numberDoubleTagYields = aNumberDoubleTagYields ;
      }

      virtual void setYieldVector( const HDBVariableVector& aVector )
      { m_yieldVector = aVector ; }

      // These two functions calculate the exclusive yield and errors.
      virtual void setYieldParameters( const HepVector& aVector ) ;
      virtual void setYieldParameterErrors( const HepVector& aVector ) ;

      virtual void setSignalEfficiencyMatrix(
 	 const HDBEfficiencyMatrix& aMatrix )
      { m_signalEfficiencyMatrix = aMatrix ; }
      virtual void setBackgroundEfficiencyMatrix(
	 const HDBEfficiencyMatrix& aMatrix )
      { m_backgroundEfficiencyMatrix = aMatrix ; }
      virtual void setEfficiencyParameters( const HepVector& aVector )
      { m_efficiencyParameters = aVector ; }
      virtual void setEfficiencyParameterErrors( const HepVector& aVector )
      { m_efficiencyParameterErrors = aVector ; }

      virtual void setBackgroundVector( const HDBVariableVector& aVector )
      { m_backgroundVector = aVector ; }
      virtual void setBackgroundParameters( const HepVector& aVector )
      { m_backgroundParameters = aVector ; }
      virtual void setBackgroundParameterErrors( const HepVector& aVector )
      { m_backgroundParameterErrors = aVector ; }

      // ---------- const member functions ---------------------
      bool singleTagsExclusive() const
      { return m_singleTagsExclusive ; }

      const vector< pair< int, int > >& doubleToSingleCrossReference() const
      { return m_doubleToSingleCrossReference ; }
      int numberSingleTagYields() const
      { return m_numberSingleTagYields ; }
      int numberDoubleTagYields() const
      { return m_numberDoubleTagYields ; }

      virtual HepVector yieldValues() const
      { return m_yieldVector.values( m_yieldParameters ) ; }
      virtual HepSymMatrix yieldErrorMatrix() const
      { return m_yieldVector.errorMatrix( m_yieldParameters,
					  m_yieldParameterErrors ) ; }
      virtual HepVector yieldDerivatives() const
      { return m_yieldVector.derivatives( m_yieldParameters ) ; }

      virtual HepMatrix signalEfficiencyValues() const
      { return m_signalEfficiencyMatrix.values( m_efficiencyParameters ) ; }
      virtual HepSymMatrix signalEfficiencyErrorMatrix() const
      { return m_signalEfficiencyMatrix.errorMatrix(
	 m_efficiencyParameters,
	 m_efficiencyParameterErrors ) ; }
      virtual HepSymMatrix signalEfficiencyErrorMatrixSingular() const
      { return m_signalEfficiencyMatrix.errorMatrixSingular(
	 m_efficiencyParameters,
	 m_efficiencyParameterErrors ) ; }
      virtual HepSymMatrix signalEfficiencyErrorMatrixNonSingular() const
      { return m_signalEfficiencyMatrix.errorMatrixNonSingular(
	 m_efficiencyParameters,
	 m_efficiencyParameterErrors ) ; }
      virtual HepMatrix signalEfficiencyDerivatives() const
      { return m_signalEfficiencyMatrix.derivatives(
	 m_efficiencyParameters ) ; }

      virtual HepMatrix backgroundEfficiencyValues() const
      { return m_backgroundEfficiencyMatrix.values( m_efficiencyParameters ) ;}
      virtual HepSymMatrix backgroundEfficiencyErrorMatrix() const
      { return m_backgroundEfficiencyMatrix.errorMatrix(
	 m_efficiencyParameters,
	 m_efficiencyParameterErrors ) ; }
      virtual HepSymMatrix backgroundEfficiencyErrorMatrixSingular() const
      { return m_backgroundEfficiencyMatrix.errorMatrixSingular(
	 m_efficiencyParameters,
	 m_efficiencyParameterErrors ) ; }
      virtual HepSymMatrix backgroundEfficiencyErrorMatrixNonSingular() const
      { return m_backgroundEfficiencyMatrix.errorMatrixNonSingular(
	 m_efficiencyParameters,
	 m_efficiencyParameterErrors ) ; }
      virtual HepMatrix backgroundEfficiencyDerivatives() const
      { return m_backgroundEfficiencyMatrix.derivatives(
	 m_efficiencyParameters ) ;}

      virtual HepMatrix signalBackgroundEfficiencyCorrelationMatrix() const
      { return  m_signalEfficiencyMatrix.correlationMatrix(
	 m_efficiencyParameters,
	 m_efficiencyParameterErrors,
	 m_backgroundEfficiencyMatrix ) ; }

      virtual HepVector backgroundValues(
	 const HepVector& aBackgroundParameters,
	 const HepVector& aFitParameters ) const ;
      virtual HepVector backgroundValues(
	 const HepVector& aFitParameters ) const ;
      virtual HepSymMatrix backgroundErrorMatrix(
	 const HepVector& aFitParameters ) const ;
      virtual HepMatrix backgroundDerivatives(
	 const HepVector& aFitParameters ) const;

      // ---------- static member functions --------------------

   protected:

      // n, parameter names = variable vector element names.
      HDBVariableVector m_yieldVector ;
      HepVector m_yieldParameters ;
      HepVector m_yieldParameterErrors ;
      HepVector m_n ; // yields

      // E, F -- only signal efficiency needs special smearing because it
      // gets inverted whereas the background efficiency matrix doesn't.
      HDBEfficiencyMatrix m_signalEfficiencyMatrix ;
      HDBEfficiencyMatrix m_backgroundEfficiencyMatrix ;
      HepVector m_efficiencyParameters ;
      HepVector m_efficiencyParameterErrors ;

      // b, not including fitted parameters
      HDBVariableVector m_backgroundVector ;
      HepVector m_backgroundParameters ;
      HepVector m_backgroundParameterErrors ;

      bool m_initializeYieldsOnly ; // needed to speed up MC.

      // ---------- protected member functions -----------------

      // ---------- protected const member functions -----------

   private:
      // ---------- Constructors and destructor ----------------
      HDBStandardInputData( const HDBStandardInputData& ); // stop default

      // ---------- assignment operator(s) ---------------------
      const HDBStandardInputData& operator=( const HDBStandardInputData& ); // stop default

      // ---------- private member functions -------------------

      // ---------- private const member functions -------------

      // ---------- data members -------------------------------

      // Constant throughout fit.
      HepSymMatrix m_Vn ; // yield error matrix

      HepMatrix m_E ; // signal efficiencies
      HepMatrix m_EInv ; // E^-1
      // signal efficiency error matrix
      HepSymMatrix m_VESingular ;
      HepSymMatrix m_VENonSingular ;
      HepSymMatrix m_VE ;

      HepMatrix m_F ; // background efficiencies
      // background efficiency error matrix
      HepSymMatrix m_VFSingular ;
      HepSymMatrix m_VFNonSingular ;
      HepSymMatrix m_VF ;

      HepMatrix m_CEF ; // signal/background efficiency correlation matrix

      // { VE  CEF }
      // { CEF  VF }
      HepSymMatrix m_totalEfficiencyVariance ;


      bool m_fitInputsInitialized ;
      bool m_singleTagsExclusive ;

      // For each double tag in m_doubleTagDefinitions,
      // keep track of single tag indices.
      vector< pair< int, int > > m_doubleToSingleCrossReference ;
      int m_numberSingleTagYields ;
      int m_numberDoubleTagYields ;

      // ---------- static data members ------------------------

};

// inline function definitions

// Uncomment the following lines, if your class is templated 
// and has an implementation file (in the Template directory)
//#if defined(INCLUDE_TEMPLATE_DEFINITIONS)
//# include "HadronicDBrFitter/Template/HDBStandardInputData.cc"
//#endif

#endif /* HADRONICDBRFITTER_HDBSTANDARDINPUTDATA_H */
