// -*- C++ -*-
#if !defined(MCDECAYPROC_MCDECAYPROC_H)
#define MCDECAYPROC_MCDECAYPROC_H
//
// Package:     <MCDecayProc>
// Module:      MCDecayProc
//
/**\class MCDecayProc MCDecayProc.h MCDecayProc/MCDecayProc.h
 
 Description: <one line class summary>

 Usage:
    <usage>

*/
//
// Author:      Xin Shi
// Created:     Mon Apr 18 09:39:25 EDT 2011
// $Id$
//
// Revision history
//
// $Log$
// Revision 1.1  2011/04/18 13:43:23  xs32
// add
//
//

// system include files

// user include files
#include "Processor/Processor.h"
#include "HistogramInterface/HistogramPackage.h"

// forward declarations

class MCDecayProc : public Processor
{
      // ------------ friend classes and functions --------------

   public:
      // ------------ constants, enums and typedefs --------------

      // ------------ Constructors and destructor ----------------
      MCDecayProc( void );                      // anal1 
      virtual ~MCDecayProc();                   // anal5 

      // ------------ member functions ---------------------------

      // methods for beginning/end "Interactive"
      virtual void init( void );             // anal1 "Interactive"
      virtual void terminate( void );        // anal5 "Interactive"

      // standard place for booking histograms
      virtual void hist_book( HIHistoManager& );                  

      // methods for binding to streams (anal2-4 etc.)
      virtual ActionBase::ActionResult event( Frame& iFrame );
      //virtual ActionBase::ActionResult beginRun( Frame& iFrame);
      //virtual ActionBase::ActionResult endRun( Frame& iFrame);

      // ------------ const member functions ---------------------

      // ------------ static member functions --------------------

   protected:
      // ------------ protected member functions -----------------

      // ------------ protected const member functions -----------

   private:
      // ------------ Constructors and destructor ----------------
      MCDecayProc( const MCDecayProc& );

      // ------------ assignment operator(s) ---------------------
      const MCDecayProc& operator=( const MCDecayProc& );

      // ------------ private member functions -------------------
      void bind( 
         ActionBase::ActionResult (MCDecayProc::*iMethod)( Frame& ),
	      const Stream::Type& iStream );

      // ------------ private const member functions -------------

      // ------------ data members -------------------------------
      // ------------ static data members ------------------------

};

// inline function definitions

#endif /* MCDECAYPROC_MCDECAYPROC_H */
