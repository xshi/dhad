/*****************************************************************************
 * Project: RooFit                                                           *
 * Package: RooFitCore                                                       *
 *    File: $Id: makedocs.cc,v 1.18 2005/02/28 21:48:22 wverkerke Exp $
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

void makedocs(const char *version="Development", const char *where= "./html", Bool_t doTutorial=kFALSE) 
{

  TString sourceDir(".:../RooFitCore:../RooFitCore/tmp/RooFitCore/include:../RooFitModels:../RooFitModels/tmp/RooFitModels") ;
  gEnv->SetValue("Unix.*.Root.Html.SourceDir",sourceDir.Data());
  gEnv->SetValue("Unix.*.Root.Html.OutputDir",where);
  gEnv->SetValue("Unix.*.Root.Html.Description","// -- CLASS DESCRIPTION");
  gEnv->SetValue("Unix.*.Root.Html.LastUpdate"," *    File: $Id: ");

  RooHtml docMaker(version);
  docMaker.setHeaderColor("#FFFFFF") ;

  if (doTutorial) {
    docMaker.Convert("intro1.cc","Elementary operations on a gaussian PDF") ;
    docMaker.Convert("intro2.cc","Building more complex PDFs via addition") ;
    docMaker.Convert("intro3.cc","Adding more dimensions, multiplying PDFs") ;
    docMaker.Convert("intro4.cc","Extend PDFs via composition") ;
    docMaker.Convert("intro5.cc","Discrete variables") ;
    docMaker.Convert("intro6.cc","Convoluted PDFs") ;
    docMaker.Convert("intro7.cc","Extended likelihood PDFs") ;
    docMaker.Convert("intro8.cc","Dataset operations") ;
    docMaker.Convert("intro9.cc","Observables vs parameters") ;
    docMaker.Convert("plot1.cc","Using variable binning") ;
    docMaker.Convert("plot2.cc","Plotting a PDF projection on a subset of the event sample") ;
    docMaker.Convert("plot3.cc","Plotting with a cut on the projected likelihood") ;
    docMaker.Convert("plot4.cc","Plotting slices of simultaneous PDFs") ;
    docMaker.Convert("mgmt1.cc","BMixing with per-event errors") ;
    docMaker.Convert("mgmt2.cc","Using RooSimPdfBuilder to replicate and customize PDFs") ;
    docMaker.Convert("mgmt3.cc","Blinding parameters") ;
    docMaker.Convert("fitgen1.cc","Interactive MINUIT") ;
    docMaker.Convert("fitgen2.cc","Adding penalty functions/Langrange multipliers") ;
    docMaker.Convert("fitgen3.cc","NLL versus Chi2 fits") ;
  }

  docMaker.MakeAll(kTRUE,"Roo*");
  docMaker.MakeIndexNew("Roo*");  

  docMaker.addTopic("PDF","Probability Density functions") ;
  docMaker.addTopic("REAL","Real valued functions") ;
  docMaker.addTopic("CAT","Discrete valued functions") ;
  docMaker.addTopic("DATA","Unbinned and binned data") ;
  docMaker.addTopic("PLOT","Plotting and tabulating") ;
  docMaker.addTopic("CONT","Container classes") ;
  docMaker.addTopic("MISC","Miscellaneous") ;
  docMaker.addTopic("USER","Other user classes") ;
  docMaker.addTopic("AUX","Auxiliary classes for internal use") ;
  docMaker.MakeIndexOfTopics() ;
}
 
