// -*- C++ -*-
#if !defined(HADRONICDBRFITTER_HDBSTANDARDFITINPUTFACTORY_H)
#define HADRONICDBRFITTER_HDBSTANDARDFITINPUTFACTORY_H
//
// Package:     <HadronicDBrFitter>
// Module:      HDBStandardFitInputFactory
// 
/**\class HDBStandardFitInputFactory HDBStandardFitInputFactory.h HadronicDBrFitter/HDBStandardFitInputFactory.h

 Description: <one line class summary>

 Usage:
    <usage>

*/
//
// Author:      Werner Sun
// Created:     Wed May 26 21:50:23 EDT 2004
// $Id$
//
// Revision history
//
// $Log$

// system include files

// user include files
#include "HadronicDBrFitter/HDBFitInputFactory.h"

// forward declarations
class HDBStandardInputData ;

class HDBStandardFitInputFactory : public HDBFitInputFactory
{
      // ---------- friend classes and functions ---------------

   public:
      // ---------- constants, enums and typedefs --------------

      enum ParticleTypes {
         kTrack,
         kChargedPion,
         kChargedKaon,
         kElectron,
         kShower,
         kKshort,
         kPi0,
	 kEtaToGammaGamma,
         kNumParticleTypes } ;

      enum FitParameterType{
	 kD0,
	 kD0Bar,
	 kDUnflavored,
	 kDPlus,
	 kDMinus,
	 kDsPlus,
	 kDsMinus,
	 kDNeutral,
	 kDCharged,
	 kDs,
	 kD0Flavored,
	 kD0BarFlavored,
	 kD0SL,
	 kD0BarSL,
	 kCPPlus,
	 kCPMinus,
	 kNumParameterTypes
      } ;

      enum SampleType{
	 kDPlusDMinus,
	 kDsPlusDsMinus,
	 kD0D0BarUncorrelated,
	 kD0D0BarCOdd,
	 kD0D0BarCOddWithEven,
	 kD0D0BarCEven,
	 kD0D0BarCEvenWithOdd
      } ;

      // ---------- Constructors and destructor ----------------
      HDBStandardFitInputFactory( bool aSingleTagsExclusive,
				  bool aGenerateMC );
      virtual ~HDBStandardFitInputFactory();

      // ---------- member functions ---------------------------

      // ---------- const member functions ---------------------

      // ---------- static member functions --------------------

   protected:

      class HDBInputInfoHolder
      {
         public:
            HDBInputInfoHolder()
               : m_numberInputs( 0 )
            {}

            virtual ~HDBInputInfoHolder() {}

            int numberInputs() const { return m_numberInputs ; }

            int fitParameterNumber( int i ) const
            { return m_fitParameterNumbers[ i ] ; }

            FitParameterType fitParameterType( int i ) const
            { return m_fitParameterTypes[ i ] ; }

            void addFitParameterNumberAndType( int aNumber,
					       FitParameterType aType )
            {
               if( m_numberInputs == 2 ) return ;
               m_fitParameterNumbers[ m_numberInputs ] = aNumber ;
               m_fitParameterTypes[ m_numberInputs ] = aType ;
               ++m_numberInputs ;
            }

            void reset()
            {
               m_numberInputs = 0 ;
            }

         private:
            int m_numberInputs ;
            int m_fitParameterNumbers[ 2 ] ;
            FitParameterType m_fitParameterTypes[ 2 ] ;
      } ;

      // ---------- protected member functions -----------------

      bool getInputInfo( const string& aMode,
			 SampleType aSampleType,
                         HDBInputInfoHolder& aInputInfo,
			 HepVector& aParticleContent,
			 vector< string >& aFitParameterNames ) ;

      void setYieldsAndErrors( const HepVector& aMeasuredYields,
			       const HepVector& aMeasuredYieldErrors ) ;

      bool m_generateMC ;
      HDBStandardInputData* m_standardInputData ; // = m_inputData

      bool m_fitParametersDefined ;
      vector< string > m_fitParameterNames ;

      vector< HDBVariableMatrixElement > m_singleTagPredictions ;
      vector< HDBVariableMatrixElement > m_doubleTagPredictions ;

      int m_nDPlusDMinusIndex ;
      int m_nDsPlusDsMinusIndex ;
      int m_nD0D0BarIndex ;
      int m_nD0D0BarCOddIndex ;
      int m_nD0D0BarCOddEvenFracIndex ;
      int m_nD0D0BarCEvenIndex ;
      int m_nD0D0BarCEvenOddFracIndex ;
      int m_yIndex ;
      int m_x2Index ;
      int m_r2Index ;
      int m_rzIndex ;
      int m_rwxIndex ;

      bool m_inputYieldsAndErrorsDefined ;
      bool m_seedsDefined ;
      bool m_externalDataDefined ;

      bool m_efficienciesDefined ;
      vector< HepVector > m_particleContents ;

      bool m_backgroundsDefined ;
      vector< string > m_backgroundNames ;

      // ---------- protected const member functions -----------

   private:
      // ---------- Constructors and destructor ----------------
      HDBStandardFitInputFactory( const HDBStandardFitInputFactory& ); // stop default

      // ---------- assignment operator(s) ---------------------
      const HDBStandardFitInputFactory& operator=( const HDBStandardFitInputFactory& ); // stop default

      // ---------- private member functions -------------------
      virtual void getInputYieldsAndErrors() = 0 ;
      virtual void getInputYieldsAndErrorsMC() = 0 ;
      virtual void getBackgrounds() = 0 ;
      virtual void getEfficiencies() = 0 ;

      // ---------- private const member functions -------------

      // ---------- data members -------------------------------

      // ---------- static data members ------------------------

};

// inline function definitions

// Uncomment the following lines, if your class is templated 
// and has an implementation file (in the Template directory)
//#if defined(INCLUDE_TEMPLATE_DEFINITIONS)
//# include "HadronicDBrFitter/Template/HDBStandardFitInputFactory.cc"
//#endif

#endif /* HADRONICDBRFITTER_HDBSTANDARDFITINPUTFACTORY_H */
