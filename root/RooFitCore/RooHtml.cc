/*****************************************************************************
 * Project: RooFit                                                           *
 * Package: RooFitCore                                                       *
 *    File: $Id: RooHtml.cc,v 1.14 2005/02/28 21:48:20 wverkerke Exp $
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

// -- CLASS DESCRIPTION [MISC] --

#include "RooFitCore/RooHtml.hh"

#include "TDatime.h"
#include "TClassTable.h"
#include "TRegexp.h"
#include "TClass.h"
#include "TSystem.h"
#include "TObjString.h"

#include <ctype.h>
#include <iostream>
#include <fstream>
#include <string.h>

#ifndef _WIN32
#include <strings.h>
using std::cout;
using std::endl;
using std::fstream;
using std::ifstream;
using std::ofstream;
#endif

const Int_t   kSpaceNum      = 1;
const char   *formatStr      = "%12s %5s %s";

ClassImp(RooHtml)
  ;

void RooHtml::WriteHtmlHeader(ofstream &out, const char *title, TClass* cls) {
  // Write a custom html header for RooFit class documentation to the specified output stream.  

  out
    << "<!doctype html public \"-//dtd html 4.0 transitional// en\">" << endl
    << "<html>" << endl
    << "<head>" << endl
    << "  <meta http-equiv=\"Content-Type\" content=\"text/html; charset=iso-8859-1\">" << endl
    << "  <meta name=\"Author\" content=\"David Kirkby & Wouter Verkerke\">" << endl
    << "  <meta name=\"GENERATOR\" content=\"RooHtml Class in ROOT Environment\">" << endl
    << "  <title>";
  ReplaceSpecialChars(out, title);
  out
    << "</title>" << endl
    << "  <meta name=\"rating\" content=\"General\">" << endl
    << "  <meta name=\"objecttype\" content=\"Manual\">" << endl
    << "  <meta name=\"keywords\" content=\"software development, oo, object oriented, "
    << "  unix, x11, windows, c++, html, rene brun, fons rademakers, david kirkby, wouter verkerke\">" << endl
    << "  <meta name=\"description\" content=\"RooFit - A Toolkit for Physics Data Modeling.\">" << endl
    << "</head>" << endl
    << "<body text=\"#000000\" bgcolor=\"#FFFFFF\" link=\"#0000FF\" vlink=\"#FF0000\" alink=\"#000088\">"
    << endl
    << "<a name=\"TopOfPage\"></a>" << endl;
  out
    << "<center><table BORDER=0 CELLSPACING=0 COLS=2 WIDTH=\"100%\" BGCOLOR=\"" << _hfColor << "\" NOSAVE >" << endl
    << "  <tr NOSAVE><td NOSAVE><b><i><font color=\"#000000\">" << endl
    //-------------------------------------------------
    << "    <a href=\"http://roofit.sourceforge.net\"" << endl
    << "      title=\"Visit RooFit Home Page\">" << endl
    << "    RooFit Toolkit for Data Modeling</a>" << endl
    //-------------------------------------------------
    << "  </font></i></b></td>" << endl
    << "  <td><div align=right><b><i><font color=\"#000000\">" << endl
    //-------------------------------------------------
    << "    <a href=\"IndexByTopic.html\"" << endl
    << "      title=\"Visit List of Classes\">" << endl;
  out << getVersion() << " Version</a>" << endl;
  //-------------------------------------------------
  out
    << "  </font></i></b></div></td></tr>" << endl
    << "</table></center>" << endl;
}

void RooHtml::WriteHtmlFooter(ofstream &out, const char *dir, const char *lastUpdate,
			      const char *author, const char *copyright) {
  // Write a custom html footer for RooFit class documentation to the specified output stream.  

  // lastUpdate will be the CVS tag in case of .rdl and .cc files: clean it up a bit

// Matthew D. Langston  <langston@SLAC.Stanford.EDU>
// There is no index function in Windows (nor is there a strings.h).
#ifndef _WIN32
   const char *comma= index(lastUpdate,',');
  TString update = comma ? comma+1 : lastUpdate;
#else
  TString update = lastUpdate;
#endif

  if(update.EndsWith(" Exp $")) update.Remove(update.Length()-6,6);

  out << "<center><table BORDER=0 CELLSPACING=0 COLS=2 WIDTH=\"100%\" BGCOLOR=\"" << _hfColor << "\" NOSAVE >" << endl
      << "<tr NOSAVE>" << endl
      << "<td>Last CVS Update: " << update << "</td>" << endl
      << "<td NOSAVE align=right><b><a href=\"#TopOfPage\">Top</a></b></td>" << endl
      << "</tr></table></center>" << endl
      << "<center>Copyright &copy 2000-2005 University of California, Stanford University</center>" << endl
      << "</body>" << endl ;
}



void RooHtml::MakeIndexNew(const char *filter)
{
  // WVE modified clone of THtml::MakeIndex that subclasses index files
  // based on tag in 'CLASS DESCRIPTION' instead of source file subdirectory

   // It makes an index files
   // by default makes an index of all classes (if filter="*")
   // To generate an index for all classes starting with "XX", do
   //    html.MakeIndex("XX*");

   CreateListOfTypes();

   // get total number of classes
   Int_t numberOfClasses = gClassTable->Classes();


   // allocate memory
   const char **classNames = new const char *[numberOfClasses];
   char       **fileNames  = new       char *[numberOfClasses];

   // start from begining
   gClassTable->Init();

   // get class names
   Int_t len = 0;
   Int_t maxLen = 0;
   Int_t numberOfImpFiles = 0;

   TString reg = filter;
   TRegexp re(reg, kTRUE);
   Int_t nOK = 0;
   
   for( Int_t i = 0; i < numberOfClasses; i++ ) {

      // get class name
      const char *cname = gClassTable->Next();
      TString s = cname;
      if (s.Index(re) == kNPOS) continue;
      classNames[nOK] = cname;
      len    = strlen( classNames[nOK] );
      maxLen = maxLen > len ? maxLen : len;

      // get class & filename
      TClass *classPtr = GetClass( (const char * ) classNames[nOK] );
      const char *impname = classPtr->GetImplFileName();

      if( impname ) {
         fileNames[numberOfImpFiles] = StrDup( impname, 64 );

         char *underline = strchr( fileNames[numberOfImpFiles], '_');
         if( underline )
            strcpy( underline + 1, classNames[nOK] );
         else {
            // WVE modified to use getClassGroup instead of subdir to determine index file
	   char* srcdir = getClassGroup(fileNames[numberOfImpFiles]) ;
	   strcpy( fileNames[nOK], srcdir);
	   strcat( fileNames[nOK], "_" );
	   strcat( fileNames[nOK], classNames[nOK] );
         }
         numberOfImpFiles++;
      }
      else cout << "WARNING class:" << classNames[i] << " has no implementation file name !" << endl;

      nOK++;
   }
   maxLen += kSpaceNum;

   // quick sort
   SortNames( classNames, nOK );
   SortNames( (const char ** ) fileNames,  numberOfImpFiles );

   // create an index
   CreateIndex( classNames, nOK);
   CreateIndexByTopic( fileNames, nOK, maxLen );

   // free allocated memory
   delete [] classNames;
   delete [] fileNames;
}


char* RooHtml::getClassGroup(const char* fileName) 
{
  // Scan file for 'CLASS DESCRIPTION [<tag>]' sequence
  // If found, return <tag>, otherwise return "USER"

  // Initialize buffer to default group name
  static char buffer[1024] = "" ;
  strcpy(buffer,"USER") ;

  const char* fullName = gSystem->Which(fSourceDir, fileName, kReadPermission) ;
  if (!fullName) {
    return buffer ;
  }

  // Scan file contents
  ifstream ifs(fullName) ;

  char line[1024] ;
  while(ifs.good()) {
    ifs.getline(line,sizeof(line),'\n') ;
    
    // Find magic word
    char *ptr ;
    if (ptr = strstr(line,"CLASS DESCRIPTION")) {
      char* start = strchr(ptr,'[') ;
      if (start) {
	// Must have closing bracket to proceed
	if (!strchr(start,']')) break ;

	// Extract keyword between square brackets
	char* group = strtok(start+1,"]") ;

	// Group name must be non-empty
	if (group && strlen(group)) strcpy(buffer,group) ;
      }
      break ;
    }
  }

  return buffer ;
}




void RooHtml::addTopic(const char* tag, const char* description) 
{
  _topicTagList.Add(new TObjString(tag)) ;
  _topicDescList.Add(new TObjString(description)) ;
}




void RooHtml::MakeIndexOfTopics() 
{
  TString idxFileName(fOutputDir) ;
  idxFileName.Append("/") ;
  idxFileName.Append("IndexByTopic.html") ;

  ofstream ofs(idxFileName) ;
  WriteHtmlHeader(ofs,"RooFit Index by Topic") ;

  TIterator* tagIter = _topicTagList.MakeIterator() ;
  TIterator* descIter = _topicDescList.MakeIterator() ;
  TObjString* tag ;
  TObjString* desc ;

  ofs << "<H2>" << endl << "<UL>" << endl ;

  while(tag=(TObjString*)tagIter->Next()) {
    desc=(TObjString*)descIter->Next() ;
    ofs << "<LI> <A HREF=" << tag->String() << "_Index.html>" << desc->String() << "</A>" << endl ;
  }
  ofs << "</UL>" << endl << "</H2>" << endl ;

  TDatime now;
  WriteHtmlFooter(ofs,"",now.AsString()) ;

  delete tagIter ;
  delete descIter ;

  
}

