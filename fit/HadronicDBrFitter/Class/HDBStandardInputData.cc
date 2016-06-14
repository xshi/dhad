// -*- C++ -*-
//
// Package:     <HadronicDBrFitter>
// Module:      HDBStandardInputData
// 
// Description: <one line class summary>
//
// Implementation:
//     <Notes on implementation>
//
// Author:      Werner Sun
// Created:     Fri May 21 19:35:05 EDT 2004
// $Id$
//
// Revision history
//
// $Log$

// #include "Experiment/Experiment.h"

// system include files
// You may have to uncomment some of these or other stl headers
// depending on what other header files you include (e.g. FrameAccess etc.)!
//#include <string>
//#include <vector>
//#include <set>
//#include <map>
//#include <algorithm>
//#include <utility>

#include <time.h>
#include <iostream>
#include <iomanip>

// user include files
//#include "Experiment/report.h"
#include "HadronicDBrFitter/HDBStandardInputData.h"


//
// constants, enums and typedefs
//

static const char* const kFacilityString = "HadronicDBrFitter.HDBStandardInputData" ;

// ---- cvs-based strings (Id and Tag with which file was checked out)
static const char* const kIdString  = "$Id: skeleton.cc,v 1.7 2004/02/12 02:14:38 pcs Exp $";
static const char* const kTagString = "$Name:  $";

//
// static data member definitions
//

//
// constructors and destructor
//
HDBStandardInputData::HDBStandardInputData( bool aSingleTagsExclusive )
   : m_fitInputsInitialized( false ),
     m_singleTagsExclusive( aSingleTagsExclusive ),
     m_numberSingleTagYields( 0 ),
     m_numberDoubleTagYields( 0 ),
     m_initializeYieldsOnly( false )
{
}

// HDBStandardInputData::HDBStandardInputData( const HDBStandardInputData& rhs )
// {
//    // do actual copying here; if you implemented
//    // operator= correctly, you may be able to use just say      
//    *this = rhs;
// }

HDBStandardInputData::~HDBStandardInputData()
{
}

//
// assignment operators
//
// const HDBStandardInputData& HDBStandardInputData::operator=( const HDBStandardInputData& rhs )
// {
//   if( this != &rhs ) {
//      // do actual copying here, plus:
//      // "SuperClass"::operator=( rhs );
//   }
//
//   return *this;
// }

//
// member functions
//

void
HDBStandardInputData::setYieldParameterErrors( const HepVector& aVector )
{
   // If single tags are exclusive, the yield error matrix can be used as is.
   // Otherwise, calculate the uncorrelated yield errors.
   int nMeas = aVector.num_row() ;
   m_yieldParameterErrors = aVector ;

   if( !m_singleTagsExclusive )
   {
      // Square the errors.
      for( int i = 0 ; i < nMeas ; ++i )
      {
	 m_yieldParameterErrors[ i ] *= m_yieldParameterErrors[ i ] ;
      }

      // Loop over all double tags and subtract double tag variances
      // from corresponding single tag variances.
      for( int i = 0 ;
	   i < m_doubleToSingleCrossReference.size() ;
	   ++i )
      {
	 int doubleIndex = i + m_numberSingleTagYields ;
	 int singleIndex1 = m_doubleToSingleCrossReference[ i ].first ;
	 int singleIndex2 = m_doubleToSingleCrossReference[ i ].second ;

	 // Single errors for this double tag.
	 double doubleErr = m_yieldParameterErrors[ doubleIndex ] ;

	 if( singleIndex1 >= 0 )
	 {
	    m_yieldParameterErrors[ singleIndex1 ] -= doubleErr ;
	    if( m_yieldParameterErrors[ singleIndex1 ] < 0. )
	    {
	       cout << "True exclusive yield error^2 " << singleIndex1
		    << " negative." << endl ;
	    }
	 }

	 if( singleIndex2 >= 0 )
	 {
	    m_yieldParameterErrors[ singleIndex2 ] -= doubleErr ;
	    if( m_yieldParameterErrors[ singleIndex2 ] < 0. )
	    {
	       cout << "True exclusive yield error^2 " << singleIndex2
		    << " negative." << endl ;
	    }
	 }

	 // If double tag has identical modes, double the subtraction.
	 if( singleIndex1 == singleIndex2 && singleIndex1 >= 0 )
	 {
	    m_yieldParameterErrors[ singleIndex1 ] -= 2. * doubleErr ;
	 }
      }

      // Take square root of variances.
      for( int i = 0 ; i < m_yieldParameterErrors.num_row() ; ++i )
      {
	 m_yieldParameterErrors[ i ] = sqrt( m_yieldParameterErrors[ i ] ) ;
      }
   }

   if( m_printDiagnostics )
   {
      cout << "Exclusive input yield errors: " << m_yieldParameterErrors
	   << endl ;
   }
}

void
HDBStandardInputData::setYieldParameters( const HepVector& aVector )
{
   // If single tags are exclusive, the yield error matrix can be used as is.
   // Otherwise, calculate the uncorrelated yields.
   int nMeas = aVector.num_row() ;
   m_yieldParameters = aVector ;

   if( !m_singleTagsExclusive )
   {
      // Loop over all double tags and subtract double tag yields
      // from corresponding single tag yields.
      for( int i = 0 ;
	   i < m_doubleToSingleCrossReference.size() ;
	   ++i )
      {
	 int doubleIndex = i + m_numberSingleTagYields ;
	 int singleIndex1 = m_doubleToSingleCrossReference[ i ].first ;
	 int singleIndex2 = m_doubleToSingleCrossReference[ i ].second ;

	 // Single yields for this double tag.
	 double doubleYield = m_yieldParameters[ doubleIndex ] ;

	 if( singleIndex1 >= 0 )
	 {
	    m_yieldParameters[ singleIndex1 ] -= doubleYield ;
	    if( m_yieldParameters[ singleIndex1 ] < 0. )
	    {
	       cout << "True exclusive yield " << singleIndex1
		    << " negative." << endl ;
	    }
	 }

	 if( singleIndex2 >= 0 )
	 {
	    m_yieldParameters[ singleIndex2 ] -= doubleYield ;
	    if( m_yieldParameters[ singleIndex2 ] < 0. )
	    {
	       cout << "True exclusive yield " << singleIndex2
		    << " negative." << endl ;
	    }
	 }
      }
   }

   if( m_printDiagnostics )
   {
      cout << "Exclusive input yields: " << m_yieldParameters << endl ;
   }
}

void
HDBStandardInputData::initialize( const HepVector& aFitParameters,
				  const HDBVariableVector* aFitPredictions )
{
   HDBInputData::initialize( aFitParameters, aFitPredictions ) ;

   // Calculate all quantities that are constant throughout fit.
   m_n = yieldValues() ;

   if( !m_initializeYieldsOnly )
   {
      m_E = signalEfficiencyValues() ;
      m_F = backgroundEfficiencyValues() ;

      int ierr ;
      m_EInv = m_E.inverse( ierr ) ;
      if( ierr )
      {
	 cout << "Could not invert signal efficiency matrix." << endl ;
      }

      m_Vn = yieldErrorMatrix() ;
//       m_VESingular = signalEfficiencyErrorMatrixSingular() ;
//       m_VFSingular = backgroundEfficiencyErrorMatrixSingular() ;
//       m_VENonSingular = signalEfficiencyErrorMatrixNonSingular() ;
//       m_VFNonSingular = backgroundEfficiencyErrorMatrixNonSingular() ;

      cout << "Calculating signal efficiency error matrix." << endl ;
      m_VE = signalEfficiencyErrorMatrix() ;
      cout << "Calculating background efficiency error matrix." << endl ;
      m_VF = backgroundEfficiencyErrorMatrix() ;
      cout << "Calculating signal/background correlation matrix." << endl ;
      m_CEF = signalBackgroundEfficiencyCorrelationMatrix() ;
      cout << "Done calculating efficiency error matrices." << endl ;

      // Construct total efficiency variance matrix.
      HepMatrix tmpEfficiencyVariance(
	 m_VE.num_row() + m_VF.num_row(),
	 m_VE.num_row() + m_VF.num_row() ) ;
// 	 m_VESingular.num_row() + m_VFSingular.num_row(),
// 	 m_VESingular.num_row() + m_VFSingular.num_row() ) ;
//      int boundaryIndex = m_VESingular.num_row() + 1 ;
      int boundaryIndex = m_VE.num_row() + 1 ;
      tmpEfficiencyVariance.sub( 1, 1,
				 HepMatrix( m_VE ) );
//				 HepMatrix( m_VESingular + m_VENonSingular ) );
      tmpEfficiencyVariance.sub( 1, boundaryIndex,
				 m_CEF ) ;
      tmpEfficiencyVariance.sub( boundaryIndex, 1,
				 m_CEF.T() ) ;
      tmpEfficiencyVariance.sub( boundaryIndex, boundaryIndex,
				 HepMatrix( m_VF ) );
//				 HepMatrix( m_VFSingular + m_VFNonSingular ) );

      m_totalEfficiencyVariance.assign( tmpEfficiencyVariance ) ;
   }

   if( m_printDiagnostics )
   {
      cout << "n" << m_n
	   << "E" << m_E
// 	   << "F" << m_F
	   << "EInv" << m_EInv
	   << "Vn" << m_Vn
// 	   << "CEF" << m_CEF
	   << endl ;
   }

   m_fitInputsInitialized = false ;
   update( aFitParameters, aFitPredictions ) ;
   m_fitInputsInitialized = true ;
}


void
HDBStandardInputData::update( const HepVector& aFitParameters,
			      const HDBVariableVector* aFitPredictions,
			      bool aFinalPass )
{
   // Update only if there are backgrounds to subtract or if m_derivatives is
   // uninitialized.
//    if( !aFinalPass &&
//        m_fitInputsInitialized && m_backgroundParameters.num_row() == 0 )
//    {
//       return ;
//    }

   // Update yields.
   HepVector b = backgroundValues( aFitParameters ) ;
   HepVector N = m_EInv * ( m_n - m_F * b ) ;

   // Update error matrix.
   HepSymMatrix Vb = backgroundErrorMatrix( aFitParameters ) ;

//   HepMatrix dpdE( m_VENonSingular.num_row(), N.num_row(), 0 ) ;
   HepMatrix dpdE( m_VE.num_row(), N.num_row(), 0 ) ;

//   if( m_fitInputsInitialized )
   {
      HepVector yieldsPred = aFitPredictions->values( aFitParameters ) ;
      for( int i = 0 ; i < yieldsPred.num_row() ; ++i )
      {
	 dpdE.sub( i * yieldsPred.num_row() + 1,
		   i + 1,
		   yieldsPred ) ;
      }
   }
//    else
//    {
//       for( int i = 0 ; i < N.num_row() ; ++i )
//       {
// 	 dpdE.sub( i * N.num_row() + 1,
// 		   i + 1,
// 		   N ) ;
//       }
//    }


//   HepMatrix dNdF( m_VFNonSingular.num_row(), N.num_row(), 0 ) ;
   HepMatrix dNdF( m_VF.num_row(), N.num_row(), 0 ) ;
   for( int i = 0 ; i < N.num_row() ; ++i )
   {
      for( int j = 0 ; j < N.num_row() ; ++j )
      {
	 dNdF.sub( i * b.num_row() + 1,
		   j + 1,
		   -m_EInv[ j ][ i ] * b ) ;
      }
   }

   // Construct total efficiency derivative matrix:
   // { dN/dE } = { -dp/dE (E^-1)^T }
   // { dN/dF }   {      dN/dF      }
   HepMatrix dNdEfficiency( dpdE.num_row() + dNdF.num_row(),
			    N.num_row() ) ;
   dNdEfficiency.sub( 1, 1, ( -dpdE * m_EInv.T() ) ) ;
   dNdEfficiency.sub( dpdE.num_row() + 1, 1, dNdF ) ;

   // Doing the similarity transformation in steps is faster than
   // m_totalEfficiencyVariance.similarityT( dNdEfficiency )!
   // This is because if m_totalEfficiencyVariance is n^2 x n^2 and
   // dNdEfficiency is n^2 x n, then the similarity transformation takes
   // ~n^6 operations (each element of m_totalEfficiencyVariance contributes
   // to each element of the output matrix).  But if the calculation is
   // split up, the first step takes n^5 operations, resulting in an
   // n^2 x n matrix that gets multiplied by an n x n^2 matrix, which takes
   // n^4 operations.  The whole thing takes only n^4(n+1) ~ n^5 operations.
   // In other words, the sooner the dimensionality can be reduced, the better.
   //
//    HepMatrix dNdEffTVEff = dNdEfficiency.T() * m_totalEfficiencyVariance ;
//    HepSymMatrix effTerm ;
//    effTerm.assign( dNdEffTVEff * dNdEfficiency ) ;
   //
   // On top of this, these tend to be sparse matrices, so we can, in
   // principle, speed things up even more by checking for zero elements first.

//    HepMatrix dNdEffTVEff( dNdEfficiency.num_col(),
// 			  m_totalEfficiencyVariance.num_col(), 0 ) ;
//    for( int i = 0 ; i < dNdEfficiency.num_col() ; ++i )
//    {
//       for( int j = 0 ; j < m_totalEfficiencyVariance.num_col() ; ++j )
//       {
// 	 double tmp = 0. ;

// 	 for( int k = 0 ; k < m_totalEfficiencyVariance.num_col() ; ++k )
// 	 {
// 	    if( dNdEfficiency[ k ][ i ] != 0. &&
// 		m_totalEfficiencyVariance[ k ][ j ] != 0. )
// 	    tmp +=
// 	       dNdEfficiency[ k ][ i ] * m_totalEfficiencyVariance[ k ][ j ] ;
// 	 }

// 	 dNdEffTVEff[ i ][ j ] = tmp ;
//       }
//    }

//    HepSymMatrix effTerm( dNdEfficiency.num_col(), 0 ) ;
//    for( int i = 0 ; i < dNdEfficiency.num_col() ; ++i )
//    {
//       for( int j = 0 ; j <= i ; ++j )
//       {
// 	 double tmp = 0. ;

// 	 for( int k = 0 ; k < m_totalEfficiencyVariance.num_col() ; ++k )
// 	 {
// 	    if( dNdEffTVEff[ i ][ k ] != 0. &&
// 		dNdEfficiency[ k ][ j ] != 0. )
// 	    tmp += dNdEffTVEff[ i ][ k ] * dNdEfficiency[ k ][ j ] ;
// 	 }

// 	 effTerm.fast( i + 1, j + 1 ) = tmp ;
//       }
//    }

   // Turns out this is MUCH faster: do similarity transformation all at once
   // with ~n^6 operations.  But because we can make fewer zero checks, there
   // is less matrix element access, which I think is the limiting factor
   // above.

   HepSymMatrix effTerm( N.num_row(), 0 ) ;
   int nEff = m_totalEfficiencyVariance.num_row() ;

   // Loop over elements of m_totalEfficiencyVariance.
   for( int i = 1 ; i <= nEff ; ++i )
   {
      // Diagonal
      double elementVN = m_totalEfficiencyVariance.fast( i, i ) ;

      if( elementVN != 0. )
      {
	 // Loop over elements of effTerm.
	 for( int k = 1 ; k <= N.num_row() ; ++k )
	 {
  	    double derivsIK = dNdEfficiency( i, k ) ;

  	    if( derivsIK != 0. )
	    {
	       // Diagonal
	       effTerm.fast( k, k ) += elementVN * derivsIK * derivsIK ;

	       // Off-diagonal
	       for( int m = 1 ; m < k ; ++m )
	       {
		  effTerm.fast( k, m ) += elementVN *
  		     derivsIK * dNdEfficiency( i, m ) ;
	       }
	    }
	 }
      }

      // Off-diagonal
      for( int j = 1 ; j < i ; ++j )
      {
	 elementVN = m_totalEfficiencyVariance.fast( i, j ) ;

  	 if( elementVN != 0. )
	 {
	    // Loop over elements of effTerm.
	    for( int k = 1 ; k <= N.num_row() ; ++k )
	    {
   	       double derivsIK = dNdEfficiency( i, k ) ;
   	       double derivsJK = dNdEfficiency( j, k ) ;

  	       if( derivsIK != 0. && derivsJK != 0. )
	       {
		  // Diagonal
		  effTerm.fast( k, k ) +=
		     2. * elementVN * derivsIK * derivsJK ;
	       }

  	       if( derivsIK != 0. || derivsJK != 0. )
	       {
		  // Off-diagonal
		  for( int m = 1 ; m < k ; ++m )
		  {
		     effTerm.fast( k, m ) += elementVN *
   			( derivsIK * dNdEfficiency( j, m ) +
   			  dNdEfficiency( i, m ) * derivsJK ) ;
		  }
	       }
	    }
	 }
      }
   }

   HepSymMatrix VN =
      ( m_Vn + Vb.similarity( m_F ) ).similarity( m_EInv ) + effTerm ;

   setValuesAndErrorMatrix( N, VN ) ;


   // Update yield derivatives.

   // Only keep portion of matrix with fit parameter derivatives.
   // Background matrix is a vector, so number elements = number rows.
   HepMatrix dbdm =
      ( backgroundDerivatives( aFitParameters ) ).sub(
	 1, aFitParameters.num_row(),  // min/max row
	 1, b.num_row()                // min/max col
	 ) ;

   m_yieldDerivatives = -dbdm * m_F.T() * m_EInv.T() ;


//    // Update error matrix derivatives.

//    HepMatrix yieldsPredDerivsT =
//       ( aFitPredictions->derivatives( aFitParameters ) ).T() ;
//    HepMatrix dbdmT = dbdm.T() ;

//    m_errorMatrixDerivatives.clear() ;
//    for( int k = 0 ; k < aFitParameters.num_row() ; ++k )
//    {
//       HepMatrix yieldsPredDerivsTk =
// 	 yieldsPredDerivsT.sub( 1, N.num_row(),    // min/max row
// 				k + 1, k + 1 ) ;   // min/max col

//       HepMatrix dpdEDerivs( m_VENonSingular.num_row(),
// 			    N.num_row(), 0 ) ;
//       for( int i = 0 ; i < N.num_row() ; ++i )
//       {
// 	 dpdEDerivs.sub( i * N.num_row() + 1,
// 			 i + 1,
// 			 yieldsPredDerivsTk ) ;
//       }

//       HepMatrix dbdmTk = dbdmT.sub( 1, b.num_row(),   // min/max row
// 				    k + 1, k + 1 ) ;  // min/max col

//       HepMatrix dNdFDerivs( m_VFNonSingular.num_row(), N.num_row(), 0 ) ;
//       for( int i = 0 ; i < N.num_row() ; ++i )
//       {
// 	 for( int j = 0 ; j < N.num_row() ; ++j )
// 	 {
// 	    dNdFDerivs.sub( i * b.num_row() + 1,
// 			    j + 1,
// 			    -m_EInv[ j ][ i ] * dbdmTk ) ;
// 	 }
//       }

//       // Construct total efficiency derivative matrix:
//       // { dN/dE } = { -dp/dE (E^-1)^T }
//       // { dN/dF }   {      dN/dF      }
//       HepMatrix dNdEfficiencyDerivs(
// 	 dpdEDerivs.num_row() + dNdFDerivs.num_row(), N.num_row() ) ;
//       dNdEfficiencyDerivs.sub( 1, 1, ( -dpdEDerivs * m_EInv.T() ) ) ;
//       dNdEfficiencyDerivs.sub( dpdEDerivs.num_row() + 1, 1, dNdFDerivs ) ;

//       HepMatrix dVdmk = dNdEffTVEff * dNdEfficiencyDerivs ;
//       HepSymMatrix dVdmkSym ;
//       dVdmkSym.assign( dVdmk + dVdmk.T() ) ;

//       if( m_printDiagnostics )
//       {
// 	 cout << "error derivs " << k << dVdmk ;
//       }

//       m_errorMatrixDerivatives.push_back( dVdmkSym ) ;
//    }


   if( m_printDiagnostics )
   {
      cout << "b" << b ;
//	   << "Fb" << m_F * b ;

      HepSymMatrix bkgErr = Vb.similarity( m_F ) ;
      HepVector bkgYield = m_F * b ;
      cout << "Fb" << endl ;
      for( int i = 0 ; i < m_n.num_row() ; ++i )
      {
	 cout << bkgYield[ i ]
	      << " +- " << sqrt( bkgErr[ i ][ i ] )
	      << " (" << bkgYield[ i ] / m_n[ i ] << ")" << endl ;
      }
      cout << endl ;

      HepSymMatrix VNCorrs = VN ;
      cout << "Eff-corrected, bkg-subt yields (N)" << endl ;
      for( int i = 0 ; i < N.num_row() ; ++i )
      {
	 cout << N[ i ] << " +- "
	      << sqrt( VN[ i ][ i ] ) << endl ;

	 for( int j = i ; j < N.num_row() ; ++j )
	 {
	    VNCorrs[ i ][ j ] /=
	       sqrt( VN[ i ][ i ] * VN[ j ][ j ] ) ;
	 }
      }
      cout << endl ;

//      cout << "N" << N
//  	   << "VENonSing term" << m_VENonSingular.similarityT( dpdE )
      cout << "VE term"
//	   << ( m_VENonSingular + m_VESingular ).similarityT( dpdE )
	   << endl
	   << "VN" << VN
	   << "VNCorrs" << VNCorrs
 	   << endl << "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
	   << endl ;

//       // ~~~~~~~~~~~ For noqcCompare ~~~~~~~~~~~~~~

//       // Add N(KlPi0) and ND0D0bar and RWS measurements
//       double ndd = 1.01475e+06 ; // from DHad 281 w/o KPi ST, KPi/KPi DT
//       int indd = 66 ;
//       double bklpi0 = 0.00992 ; // from Ks/Kl 281 w/o KPi tags
//       int iklpi0 = 67 ;
//       double rws = 0.00380 ; // time-dep and time-indep WS KPi
//       int irws = 68 ;
//       HepVector M( N.num_row() + 3 ) ;
//       M.sub( 1, N ) ;
//       M[ indd ] = ndd ;
//       M[ iklpi0 ] = 2. * ndd * bklpi0 ;
//       M[ irws ] = rws ;

//       HepSymMatrix VM( VN.num_row() + 3 ) ;
//       VM.sub( 1, VN ) ;
//       VM[ indd ][ indd ] = sqr( 10747.2 ) ; // stat only, neglect syst
//       VM[ iklpi0 ][ iklpi0 ] = sqr( 548.0 ) ; // dB = 0.027%
//       VM[ irws ][ irws ] = sqr( 0.000080 ) ;

//       // approximate off-diag elements using derivatives w.r.t. the quantites
//       // that were used to calculate N(KlPi0)
//       int ikspi0 = 5 ;
//       VM[ iklpi0 ][ ikspi0 ] =
// 	 -0.672 * VM[ ikspi0 ][ ikspi0 ] ; // dN(KlPi0)/dN(KsPi0) = -0.672
//       VM[ iklpi0 ][ indd ] =
// 	 0.0375 * VM[ indd ][ indd ] ; // dN(KlPi0)/dNDDbar = 0.0375

//       cout << "NoQCCompare" << endl ;

//       int nstkpi = 2 ;
//       int stkpi[ 2 ] ;
//       stkpi[ 0 ] = 0 ;
//       stkpi[ 1 ] = 1 ;
//       double nkpi = 0 ;
//       for( int i = 0 ; i < nstkpi ; ++i ) nkpi += M[ stkpi[ i ] ] ;
//       cout << "nkpi " << nkpi << endl ;

//       int nstcpp = 4 ;
//       int stcpp[ 4 ] ;
//       stcpp[ 0 ] = 2 ;
//       stcpp[ 1 ] = 3 ;
//       stcpp[ 2 ] = 4 ;
//       stcpp[ 3 ] = iklpi0 ;
//       double ncpp = 0 ;
//       for( int i = 0 ; i < nstcpp ; ++i ) ncpp += M[ stcpp[ i ] ] ;
//       cout << "ncpp " << ncpp << endl ;

//       int nstcpp_nokl = 3 ;
//       int stcpp_nokl[ 3 ] ;
//       stcpp_nokl[ 0 ] = 2 ;
//       stcpp_nokl[ 1 ] = 3 ;
//       stcpp_nokl[ 2 ] = 4 ;
//       double ncpp_nokl = 0 ;
//       for( int i = 0 ; i < nstcpp_nokl ; ++i )
// 	 ncpp_nokl += M[ stcpp_nokl[ i ] ] ;
//       cout << "ncpp_nokl " << ncpp_nokl << endl ;

//       int nstcpm = 3 ;
//       int stcpm[ 3 ] ;
//       stcpm[ 0 ] = 5 ;
//       stcpm[ 1 ] = 6 ;
//       stcpm[ 2 ] = 7 ;
//       double ncpm = 0 ;
//       for( int i = 0 ; i < nstcpm ; ++i ) ncpm += M[ stcpm[ i ] ] ;
//       cout << "ncpm " << ncpm  << endl ;

//       cout << endl ;

//       {
// 	 cout << "CP+/CP+" << endl ;

// 	 int ndt = 9 ;
// 	 int dt[ 9 ] ;
// 	 dt[ 0 ] = 23 ;
// 	 dt[ 1 ] = 24 ;
// 	 dt[ 2 ] = 25 ;
// 	 dt[ 3 ] = 29 ;
// 	 dt[ 4 ] = 30 ;
// 	 dt[ 5 ] = 34 ;
// 	 dt[ 6 ] = 60 ;
// 	 dt[ 7 ] = 61 ;
// 	 dt[ 8 ] = 62 ;
// 	 double n = 0 ;
// 	 for( int i = 0 ; i < ndt ; ++i ) n += M[ dt[ i ] ] ;
// 	 cout << "n " << n << endl ;

// 	 double n_norm = 4. * n * ndd / ncpp / ncpp_nokl ;

// 	 HepVector derivs( M.num_row(), 0 ) ;
// 	 derivs[ indd ] = n_norm / ndd ;
// 	 for( int i = 0 ; i < ndt ; ++i )
// 	    derivs[ dt[ i ] ] = n_norm / n ;
// 	 for( int i = 0 ; i < nstcpp_nokl ; ++i )
// 	    derivs[ stcpp_nokl[ i ] ] = -n_norm / ncpp - n_norm / ncpp_nokl ;
// 	 derivs[ iklpi0 ] = -n_norm / ncpp ;
// 	 double d_n_norm = sqrt( VM.similarity( derivs ) ) ;
// 	 cout << "n_norm " << n_norm
// 	      << " +- " << d_n_norm << endl << endl ;
//       }

//       {
// 	 cout << "CP-/CP-" << endl ;

// 	 int ndt = 6 ;
// 	 int dt[ 6 ] ;
// 	 dt[ 0 ] = 38 ;
// 	 dt[ 1 ] = 39 ;
// 	 dt[ 2 ] = 40 ;
// 	 dt[ 3 ] = 41 ;
// 	 dt[ 4 ] = 42 ;
// 	 dt[ 5 ] = 43 ;
// 	 double n = 0 ;
// 	 for( int i = 0 ; i < ndt ; ++i ) n += M[ dt[ i ] ] ;
// 	 cout << "n " << n << endl ;

// 	 double n_norm = 4. * n * ndd / sqr( ncpm ) ;

// 	 HepVector derivs( M.num_row(), 0 ) ;
// 	 derivs[ indd ] = n_norm / ndd ;
// 	 for( int i = 0 ; i < ndt ; ++i )
// 	    derivs[ dt[ i ] ] = n_norm / n ;
// 	 for( int i = 0 ; i < nstcpm ; ++i )
// 	    derivs[ stcpm[ i ] ] = -2. * n_norm / ncpm ;
// 	 double d_n_norm = sqrt( VM.similarity( derivs ) ) ;
// 	 cout << "n_norm " << n_norm
// 	      << " +- " << d_n_norm << endl << endl ;
//       }

//       {
// 	 cout << "CP+/CP-" << endl ;

// 	 int ndt = 12 ;
// 	 int dt[ 12 ] ;
// 	 dt[ 0 ] = 26 ;
// 	 dt[ 1 ] = 27 ;
// 	 dt[ 2 ] = 28 ;
// 	 dt[ 3 ] = 31 ;
// 	 dt[ 4 ] = 32 ;
// 	 dt[ 5 ] = 33 ;
// 	 dt[ 6 ] = 35 ;
// 	 dt[ 7 ] = 36 ;
// 	 dt[ 8 ] = 37 ;
// 	 dt[ 9 ] = 63 ;
// 	 dt[ 10 ] = 64 ;
// 	 dt[ 11 ] = 65 ;
// 	 double n = 0 ;
// 	 for( int i = 0 ; i < ndt ; ++i ) n += M[ dt[ i ] ] ;
// 	 cout << "n " << n << endl ;

// 	 double n_norm = 2. * n * ndd / ncpp / ncpm ;

// 	 HepVector derivs( M.num_row(), 0 ) ;
// 	 derivs[ indd ] = n_norm / ndd ;
// 	 for( int i = 0 ; i < ndt ; ++i )
// 	    derivs[ dt[ i ] ] = n_norm / n ;
// 	 for( int i = 0 ; i < nstcpp ; ++i )
// 	    derivs[ stcpp[ i ] ] = -n_norm / ncpp ;
// 	 for( int i = 0 ; i < nstcpm ; ++i )
// 	    derivs[ stcpm[ i ] ] = -n_norm / ncpm ;
// 	 double d_n_norm = sqrt( VM.similarity( derivs ) ) ;
// 	 cout << "n_norm " << n_norm
// 	      << " +- " << d_n_norm << endl << endl ;
//       }

//       {
// 	 cout << "Same-sign KPi" << endl ;

// 	 int ndt = 2 ;
// 	 int dt[ 2 ] ;
// 	 dt[ 0 ] = 8 ;
// 	 dt[ 1 ] = 16 ;
// 	 double n = 0 ;
// 	 for( int i = 0 ; i < ndt ; ++i ) n += M[ dt[ i ] ] ;
// 	 cout << "n " << n << endl ;

// 	 double n_norm = 2. * n * ndd / sqr( nkpi ) * sqr( 1 + rws ) / rws ;

// 	 HepVector derivs( M.num_row(), 0 ) ;
// 	 derivs[ indd ] = n_norm / ndd ;
// 	 for( int i = 0 ; i < ndt ; ++i )
// 	    derivs[ dt[ i ] ] = n_norm / n ;
// 	 for( int i = 0 ; i < nstkpi ; ++i )
// 	    derivs[ stkpi[ i ] ] = -2. * n_norm / nkpi ;
// 	 derivs[ irws ] = 2. * n_norm / ( 1 + rws ) - n_norm / rws ;
// 	 double d_n_norm = sqrt( VM.similarity( derivs ) ) ;
// 	 cout << "n_norm " << n_norm
// 	      << " +- " << d_n_norm << endl << endl ;
//       }

//       {
// 	 cout << "Opposite-sign KPi" << endl ;

// 	 int ndt = 1 ;
// 	 int dt[ 1 ] ;
// 	 dt[ 0 ] = 9 ;
// 	 double n = 0 ;
// 	 for( int i = 0 ; i < ndt ; ++i ) n += M[ dt[ i ] ] ;
// 	 cout << "n " << n << endl ;

// 	 double n_norm = 4. * n * ndd / sqr( nkpi ) * sqr( 1 + rws ) /
// 	    ( 1 + sqr( rws ) ) ;

// 	 HepVector derivs( M.num_row(), 0 ) ;
// 	 derivs[ indd ] = n_norm / ndd ;
// 	 for( int i = 0 ; i < ndt ; ++i )
// 	    derivs[ dt[ i ] ] = n_norm / n ;
// 	 for( int i = 0 ; i < nstkpi ; ++i )
// 	    derivs[ stkpi[ i ] ] = -2. * n_norm / nkpi ;
// 	 derivs[ irws ] = 2. * n_norm / ( 1 + rws ) -
// 	    2. * rws * n_norm / ( 1 + sqr( rws ) )  ;
// 	 double d_n_norm = sqrt( VM.similarity( derivs ) ) ;
// 	 cout << "n_norm " << n_norm
// 	      << " +- " << d_n_norm << endl << endl ;
//       }

//       {
// 	 cout << "KPi/CP+" << endl ;

// 	 int ndt = 8 ;
// 	 int dt[ 8 ] ;
// 	 dt[ 0 ] = 10 ;
// 	 dt[ 1 ] = 11 ;
// 	 dt[ 2 ] = 12 ;
// 	 dt[ 3 ] = 17 ;
// 	 dt[ 4 ] = 18 ;
// 	 dt[ 5 ] = 19 ;
// 	 dt[ 6 ] = 58 ;
// 	 dt[ 7 ] = 59 ;
// 	 double n = 0 ;
// 	 for( int i = 0 ; i < ndt ; ++i ) n += M[ dt[ i ] ] ;
// 	 cout << "n " << n << endl ;

// 	 double n_norm = 2. * n * ndd / nkpi / ncpp ;

// 	 HepVector derivs( M.num_row(), 0 ) ;
// 	 derivs[ indd ] = n_norm / ndd ;
// 	 for( int i = 0 ; i < ndt ; ++i )
// 	    derivs[ dt[ i ] ] = n_norm / n ;
// 	 for( int i = 0 ; i < nstkpi ; ++i )
// 	    derivs[ stkpi[ i ] ] = -n_norm / nkpi ;
// 	 for( int i = 0 ; i < nstcpp ; ++i )
// 	    derivs[ stcpp[ i ] ] = -n_norm / ncpp ;
// 	 double d_n_norm = sqrt( VM.similarity( derivs ) ) ;
// 	 cout << "n_norm " << n_norm
// 	      << " +- " << d_n_norm << endl << endl ;
//       }

//       {
// 	 cout << "KPi/CP-" << endl ;

// 	 int ndt = 6 ;
// 	 int dt[ 6 ] ;
// 	 dt[ 0 ] = 13 ;
// 	 dt[ 1 ] = 14 ;
// 	 dt[ 2 ] = 15 ;
// 	 dt[ 3 ] = 20 ;
// 	 dt[ 4 ] = 21 ;
// 	 dt[ 5 ] = 22 ;
// 	 double n = 0 ;
// 	 for( int i = 0 ; i < ndt ; ++i ) n += M[ dt[ i ] ] ;
// 	 cout << "n " << n << endl ;

// 	 double n_norm = 2. * n * ndd / nkpi / ncpm ;

// 	 HepVector derivs( M.num_row(), 0 ) ;
// 	 derivs[ indd ] = n_norm / ndd ;
// 	 for( int i = 0 ; i < ndt ; ++i )
// 	    derivs[ dt[ i ] ] = n_norm / n ;
// 	 for( int i = 0 ; i < nstkpi ; ++i )
// 	    derivs[ stkpi[ i ] ] = -n_norm / nkpi ;
// 	 for( int i = 0 ; i < nstcpm ; ++i )
// 	    derivs[ stcpm[ i ] ] = -n_norm / ncpm ;
// 	 double d_n_norm = sqrt( VM.similarity( derivs ) ) ;
// 	 cout << "n_norm " << n_norm
// 	      << " +- " << d_n_norm << endl << endl ;
//       }

//       cout << endl ;

//       // ~~~~~~~~ Print correlation matrix for yields ~~~~~~~~

//       int n0 = 0 ;
//       int n1 = 23 ;
//       int n2 = 44 ;
//       int n3 = 66 ;

//       for( int i = n0 ; i < n1 ; ++i ) // row
//       {
// 	 for( int j = n0 ; j < i ; ++j ) // column
// 	 {
// 	    cout << " &" ;
// 	 }
// 	 cout << " & ---" ;
// 	 for( int j = i + 1 ; j < n1 ; ++j )
// 	 {
// 	    cout << " & $" ;
// 	    cout << fixed ;
// 	    cout << setprecision(0) << VNCorrs[ i ][ j ]*100. ;
// 	    cout << "$" ;
// 	 }
// 	 cout << " \\\\" << endl ;
//       }

//       cout << "=====" << endl ;

//       for( int i = n0 ; i < n1 ; ++i ) // row
//       {
// 	 for( int j = n1 ; j < n2 ; ++j ) // column
// 	 {
// 	    cout << " & $" ;
// 	    cout << fixed ;
// 	    cout << setprecision(0) << VNCorrs[ i ][ j ]*100. ;
// 	    cout << "$" ;
// 	 }
// 	 cout << " \\\\" << endl ;
//       }

//       cout << "=====" << endl ;

//       for( int i = n0 ; i < n1 ; ++i ) // row
//       {
// 	 for( int j = n2 ; j < n3 ; ++j ) // column
// 	 {
// 	    cout << " & $" ;
// 	    cout << fixed ;
// 	    cout << setprecision(0) << VNCorrs[ i ][ j ]*100. ;
// 	    cout << "$" ;
// 	 }
// 	 cout << " \\\\" << endl ;
//       }

//       cout << "=====" << endl ;

//       for( int i = n1 ; i < n2 ; ++i ) // row
//       {
// 	 for( int j = n1 ; j < i ; ++j ) // column
// 	 {
// 	    cout << " &" ;
// 	 }
// 	 cout << " & ---" ;
// 	 for( int j = i + 1 ; j < n2 ; ++j )
// 	 {
// 	    cout << " & $" ;
// 	    cout << fixed ;
// 	    cout << setprecision(0) << VNCorrs[ i ][ j ]*100. ;
// 	    cout << "$" ;
// 	 }
// 	 cout << " \\\\" << endl ;
//       }

//       cout << "=====" << endl ;

//       for( int i = n1 ; i < n2 ; ++i ) // row
//       {
// 	 for( int j = n2 ; j < n3 ; ++j ) // column
// 	 {
// 	    cout << " & $" ;
// 	    cout << fixed ;
// 	    cout << setprecision(0) << VNCorrs[ i ][ j ]*100. ;
// 	    cout << "$" ;
// 	 }
// 	 cout << " \\\\" << endl ;
//       }

//       cout << "=====" << endl ;

//       for( int i = n2 ; i < n3 ; ++i ) // row
//       {
// 	 for( int j = n2 ; j < i ; ++j ) // column
// 	 {
// 	    cout << " &" ;
// 	 }
// 	 cout << " & ---" ;
// 	 for( int j = i + 1 ; j < n3 ; ++j )
// 	 {
// 	    cout << " & $" ;
// 	    cout << fixed ;
// 	    cout << setprecision(0) << VNCorrs[ i ][ j ]*100. ;
// 	    cout << "$" ;
// 	 }
// 	 cout << " \\\\" << endl ;
//       }

   }
}


//
// const member functions
//

HepVector
HDBStandardInputData::backgroundValues( const HepVector& aBackgroundParameters,
					const HepVector& aFitParameters ) const
{
   HepVector backgroundParameters( aFitParameters.num_row() +
		  aBackgroundParameters.num_row(), 0 ) ;
   backgroundParameters.sub( 1, aFitParameters ) ;
   backgroundParameters.sub( aFitParameters.num_row() + 1,
			     aBackgroundParameters ) ;

   return m_backgroundVector.values( backgroundParameters ) ;
}

HepVector
HDBStandardInputData::backgroundValues( const HepVector& aFitParameters ) const
{
   return backgroundValues( m_backgroundParameters, aFitParameters ) ;
}

HepSymMatrix
HDBStandardInputData::backgroundErrorMatrix(
   const HepVector& aFitParameters ) const
{
   HepVector backgroundParameters( aFitParameters.num_row() +
		  m_backgroundParameters.num_row(), 0 ) ;
   backgroundParameters.sub( 1, aFitParameters ) ;
   backgroundParameters.sub( aFitParameters.num_row() + 1,
			     m_backgroundParameters ) ;

   HepVector backgroundParameterErrors( aFitParameters.num_row() +
		  m_backgroundParameters.num_row(), 0 ) ;
   // Fitted parameters have no errors.
   backgroundParameterErrors.sub( aFitParameters.num_row() + 1,
				  m_backgroundParameterErrors ) ;

   return m_backgroundVector.errorMatrix(
      backgroundParameters,
      backgroundParameterErrors ) ;
}

HepMatrix
HDBStandardInputData::backgroundDerivatives(
   const HepVector& aFitParameters ) const
{
   HepVector backgroundParameters( aFitParameters.num_row() +
		  m_backgroundParameters.num_row(), 0 ) ;
   backgroundParameters.sub( 1, aFitParameters ) ;
   backgroundParameters.sub( aFitParameters.num_row() + 1,
			     m_backgroundParameters ) ;

   return m_backgroundVector.derivatives( backgroundParameters ) ;
}

//
// static member functions
//
