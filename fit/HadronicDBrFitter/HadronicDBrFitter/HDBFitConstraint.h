#if !defined(PACKAGE_HDBFITCONSTRAINT_H)
#define PACKAGE_HDBFITCONSTRAINT_H
// -*- C++ -*-
//
// Package:     <package>
// Module:      HDBFitConstraint
// 
/**\class HDBFitConstraint HDBFitConstraint.h package/HDBFitConstraint.h

 Description: <one line class summary>

 Usage:
    <usage>

*/
//
// Author:      Werner Sun
// Created:     Tue Mar 30 04:15:51 EST 2004
// $Id$
//
// Revision history
//
// $Log$

// system include files

// user include files

// forward declarations

class HDBFitConstraint
{
      // ---------- friend classes and functions ---------------

   public:
      // ---------- constants, enums and typedefs --------------

      // ---------- Constructors and destructor ----------------
      HDBFitConstraint();
      virtual ~HDBFitConstraint();

      // ---------- member functions ---------------------------

      // ---------- const member functions ---------------------

      // ---------- static member functions --------------------

   protected:
      // ---------- protected member functions -----------------

      // ---------- protected const member functions -----------

   private:
      // ---------- Constructors and destructor ----------------
      HDBFitConstraint( const HDBFitConstraint& ); // stop default

      // ---------- assignment operator(s) ---------------------
      const HDBFitConstraint& operator=( const HDBFitConstraint& ); // stop default

      // ---------- private member functions -------------------

      // ---------- private const member functions -------------

      // ---------- data members -------------------------------

      // ---------- static data members ------------------------

};

// inline function definitions

// Uncomment the following lines, if your class is templated 
// and has an implementation file (in the Template directory)
//#if defined(INCLUDE_TEMPLATE_DEFINITIONS)
//# include "package/Template/HDBFitConstraint.cc"
//#endif

#endif /* PACKAGE_HDBFITCONSTRAINT_H */
