# ;-*-Mode: makefile-*-
#=============================================================================
#
# Purpose: Link a Processor/Producer
#
# How to use:
#
#   1.) Copy this file to your build area. (Please don't build code in your
#       source area!)
#
#   2.) This makefile includes "M.tail", which contains all the "meat".
#       (suffix rules, platform dependencies etc.)
#
#   3.) Dependencies (ala makedepend) are done via a ".depend" file 
#       which gets created and include by "M.tail".
#
#   4.) Make sure the environment variable USER_SRC is set to the
#       directory *above* the source code:
#         e.g. "setenv USER_SRC /home/mkl/work/cleo3/cvssrc"
#
#   5.) To link a shared library, do"
#         unix> gmake CXX=<compiler> shared_module
#         e.g. "gmake CXX=cxx shared_module"
#
#   6.) The library will appear by default as "../lib/lib<directory>.a", 
#       and the linked shared library as "../shlib/<directory>.so".
#       If you want the shared library name to have a different name,
#       specify that name with "SHARMODNAME" below.
#
#   7.) To compile and link in debug mode, use "DEBUG=y":
#          e.g. "gmake CXX=cxx DEBUG=y shared_module"
#        This will result in an appended "_g" to library and 
#       shared library names.
#
#   8.) You can OVERRIDE any symbol used in a makefile by specifying the new
#       symbol on the command line, for example, 
#          e.g. "gmake USER_OBJS=myfunc.o"
#       Please remember that this will OVERRIDE any value specified in the 
#       Makefile. If you just which to add extra information to the current
#       makefile value the 'XTRA_????' symbols have been created. Look through
#       this file to see which symbols add to the makefile symbols. 
#
#=============================================================================
SHELL := /bin/sh
USER_LINK := CXX
#
#----------------------------
# name of job and executable
#----------------------------

ifeq "$(JOB)" ""
  WHERE := $(shell pawd)
  JOB := $(notdir $(WHERE))
endif
SHARMODNAME := $(JOB)

#----------------------------------------
# List of subdirectories containing code
#----------------------------------------

DIR_LIST :=	. Class Instantiate $(XTRA_DIR)

#-------------------------------------------------------
# Set up libraries paths:
# (Only uncommented settings are used!)
#-------------------------------------------------------
CLEO3LIB	:= $(C3_LIB)/lib
OTHRLIB		:= $(C3_OTHER)/lib $(shell exec $(C3_OTHER)/Root/bin/root-config --libdir)
#CLEOLIB	:= $(C_LIB)/lib
CERN3LIB 	:= $(CERN3_LIB)/lib
COMMLIB   	:= $(COMM_LIB)/lib
SYSLIB   	:=

#------------------------------------
# USER, CLEO and CERN object modules
#------------------------------------

USER_OBJS :=	$(XTRA_OBJS)
CLEO3_OBJS :=	
OTHR_OBJS :=	
#CLEO_OBJS :=	
CERN_OBJS :=	
COMM_OBJS :=	

#-------------------------------------------------------
# list of include directories:
#   $USER_SRC/include is implicitly included!
#   USER_INCS should be defined with respect to USER_SRC
#   CLEO3_INCS should be defined with respect to C3_INC 
#   CLEO_INCS should be defined with respect to C_CVSSRC
#   CERN_INCS should be defined with respect to CERNSRC
#   COMM_INCS should be defined with respect to COMM_INC
#   OTHR_INCS should be fully specified!
# Only uncommented settings are used!
#-------------------------------------------------------

USER_INCS :=	$(XTRA_INCS) .
CLEO3_INCS:=	.
#CLEO_INCS := 	. 
CERN_INCS :=	../include/cfortran/
#COMM_INCS =	$(CONSTANTS_INCS)
OTHR_INCS :=	$(C3_OTHER)/Root/include/

#---------------------------------------
# USER, CLEO and CERN libraries to load
#---------------------------------------

USER_LIBS  :=
CLEO3_LIBS :=   ProxyBind \
		Processor \
                CommandPattern \
		CleoDChain \
		Navigation \
                VXFit \
                PhotonDecays \
                TrackShowerMatching \
                C3cc \
                TrackDelivery \
                TrackRoot \
                MCInfo \
                KinematicTrajectory \
                ProxyBind \
                HistogramInterface \
                CleoDB \
                StorageManagement \
                DataHandler \
                ToolBox \
                Utility \
                DTagProd \
                DTag \
                CesrCleoComm \
		CleoDB \
		Navigation \
		MCInfo \
		MCCCTagger \
		MCTrackTagger \
		RichAverageAnglesProd \
		C3Rich \
		PhotonDecays \
		VXFitVeeCandidate \
		DedxInfo \
		BeamEnergy \
		RichTrackPrototypesProd \
		RichTrackClusterMatchProd \
		C3Rich \
		C3Mu \
                StorageManagement \
		RichAngles \
                DDoubleTag \
		LabNet4Momentum \
	        CleoDB \
                BeamSpot \
		VFinderQualityObject \
		MagField \
		VXFit \
		TriggerL1Data \
		RawData \
		BunchFinder \
		CWNFramework \
		Trkman \
                CleoDChain \
		EID
#                TagDKaonProd \


OTHR_LIBS  :=	CLHEP
#CLEO_LIBS  :=
#CERN_LIBS  :=
CERN_LIBS  := packlib mathlib                     
#COMM_LIBS  = $(CONSTANTS_LIBS)
SYS_LIBS   :=

#-------------------------------------------------
# list of undefined symbols
#-------------------------------------------------

USER_SYMS 	:= $(XTRA_SYMS)

#--------------------------------------------------------------
# extra compiler/linker flags
#--------------------------------------------------------------

USER_FFLAGS     := $(XTRA_FFLAGS)
USER_CFLAGS     := $(XTRA_CFLAGS)
USER_CXXFLAGS   := $(XTRA_CXXFLAGS) 

USER_LFLAGS	:= $(XTRA_LFLAGS) $(shell exec $(C3_OTHER)/Root/bin/root-config --libs)

#---------------------------------------------
# #define for cpp, define SELECT symbols here
#---------------------------------------------

USER_DEFS 	:= $(XTRA_DEFS)

#--------------------------------------------------------------
# invoke standard tail to Makefile to execute compile and link
#--------------------------------------------------------------

include $(C3_GMAKE)/M.tail

#
# $Id$
#
# DO NOT DELETE

