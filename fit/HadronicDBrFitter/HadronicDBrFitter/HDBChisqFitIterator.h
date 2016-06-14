#if !defined(PACKAGE_HDBCHISQFITITERATOR_H)
#define PACKAGE_HDBCHISQFITITERATOR_H
// -*- C++ -*-
//
// Package:     <package>
// Module:      HDBChisqFitIterator
// 
/**\class HDBChisqFitIterator HDBChisqFitIterator.h package/HDBChisqFitIterator.h

 Description: <one line class summary>

 Usage:
    <usage>

*/
//
// Author:      Werner Sun
// Created:     Tue Mar 30 22:50:21 EST 2004
// $Id$
//
// Revision history
//
// $Log$

// system include files

// user include files
#include "HadronicDBrFitter/HDBFitIterator.h"

// forward declarations
class HDBChisqMinimizer ;

class HDBChisqFitIterator : public HDBFitIterator
{
      // ---------- friend classes and functions ---------------

   public:
      // ---------- constants, enums and typedefs --------------

      // ---------- Constructors and destructor ----------------
      HDBChisqFitIterator( HDBChisqMinimizer* aParameterEstimator,
			   int aMaxIterations,
			   double aMaxDeltaChisq );
      virtual ~HDBChisqFitIterator();

      // ---------- member functions ---------------------------
      virtual bool convergenceCriterionMet() ;

      virtual void saveFitResultsBeforeFinalPass()
      {
	 HDBFitIterator::saveFitResultsBeforeFinalPass() ;
	 m_chisqBeforeFinalPass = chisq() ;
      }
      virtual void saveFitResultsBeforeFinalPass2()
      {
	 HDBFitIterator::saveFitResultsBeforeFinalPass2() ;
	 m_chisqBeforeFinalPass2 = chisq() ;
      }

      // ---------- const member functions ---------------------
      double chisq() const ;
      int ndof() const ;

      double chisqBeforeFinalPass() const
      { return m_chisqBeforeFinalPass ; }
      double chisqBeforeFinalPass2() const
      { return m_chisqBeforeFinalPass2 ; }

      // ---------- static member functions --------------------

   protected:
      // ---------- protected member functions -----------------

      // ---------- protected const member functions -----------

   private:
      // ---------- Constructors and destructor ----------------
      HDBChisqFitIterator( const HDBChisqFitIterator& ); // stop default

      // ---------- assignment operator(s) ---------------------
      const HDBChisqFitIterator& operator=( const HDBChisqFitIterator& ); // stop default

      // ---------- private member functions -------------------

      // ---------- private const member functions -------------

      // ---------- data members -------------------------------
      double m_previousChisq ;
      double m_maxDeltaChisqNdof ;

      double m_chisqBeforeFinalPass ;
      double m_chisqBeforeFinalPass2 ;

      // ---------- static data members ------------------------

};

// inline function definitions

// Uncomment the following lines, if your class is templated 
// and has an implementation file (in the Template directory)
//#if defined(INCLUDE_TEMPLATE_DEFINITIONS)
//# include "package/Template/HDBChisqFitIterator.cc"
//#endif

#endif /* PACKAGE_HDBCHISQFITITERATOR_H */
