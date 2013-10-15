#=============================================================================
#
# Purpose: Build a user library with name <name>
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
#   5.) To compile the library, do"
#         unix> gmake CXX=<compiler>
#         e.g. "gmake CXX=cxx"
#
#   6.) The library will appear by default as "../lib/lib<directory>.a", 
#
#   7.) To compile and link in debug mode, use "DEBUG=y":
#          e.g. "gmake CXX=cxx DEBUG=y"
#        This will result in an appended "_g" to the library name.
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
  WHERE := $(shell pwd)
  JOB := $(notdir $(WHERE))
endif
EXE = 

#----------------------------------------
# List of subdirectories containing code
#----------------------------------------

DIR_LIST := Class \
	$(XTRA_DIR)

#-------------------------------------------------------
# list of include directories
# USER_INCS should be defined with respect to USER_SRC
# CLEO3_INCS should be set to C3_INC; $USER_SRC/include is implicitly included
# OTHR_INCS should be defined with respect to C3_OTHER
# CLEO_INCS should be defined with respect to C_CVSSRC
# CERN_INCS should be defined with respect to CERNSRC
# (don't forget to leave the "." in the CLEO_INCS list)
#-------------------------------------------------------

USER_INCS  :=	$(XTRA_INCS) . 
CLEO3_INCS :=	$(C3_INC)
OTHR_INCS  :=	$(C3_OTHER)/Root/include/
CLEO_INCS  :=	.
CERN_INCS  :=	../include/cfortran

#--------------------------------------------------------------
# extra compiler flags
#--------------------------------------------------------------

USER_FFLAGS   := $(XTRA_FFLAGS)
USER_CFLAGS   := $(XTRA_CFLAGS)
USER_CXXFLAGS := $(XTRA_CXXFLAGS)

#---------------------------------------------
# #define for cpp, define SELECT symbols here
#---------------------------------------------

USER_DEFS :=	$(XTRA_DEFS)

#--------------------------------------------------------------
# invoke standard tail to Makefile to execute compile and link
#--------------------------------------------------------------

include $(C3_GMAKE)/M.tail

# --------------------------------------------------------------------
# if you need something special done for a particular file, put here:
#
#$(LIBRARY)(special_file.o) : $(USER_SRC)/<Library>/Class/special_file.cc
#	$(CXX) $(CXXFLAGS) $(GUNG_FIX) $(CLEO_DEFS) $(LIST_INCS) $(CXX_INCS) -c $<
#	@$(AR) r $@ $%
#	@$(RM) $%
# --------------------------------------------------------------------

# $Id$
#
# DO NOT DELETE
