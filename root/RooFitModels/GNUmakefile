
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
# *                                                                           *
# * !!! NOTE: This is the makefile for the BaBar SoftRelTools framework       *
# * !!!       if you are _not_ a member of BaBar, use GNUMakefile.standalone  *
# *                                                                           *
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *


# Please see SoftRelTools/HOWTO-GNUmakefile for documentation
# $Id: GNUmakefile,v 1.9 2004/04/05 22:26:20 wverkerke Exp $
#################################################################
#++ library products				[build it with 'lib']

LIBREMOVEFILES := 
LIBTMPLFILES :=
LIBDDLORDERED :=

#################################################################
#++ extra binary products	[not in production, build it with extrabin]

EXTRABINS :=

$(addprefix $(bindir),$(EXTRABINS)): $(bindir)% : %.o

#################################################################
#++ binary products				[build it with 'bin']

#CXXFLAGS += -pg 
#LDFLAGS += -pg
#CXXFLAGS += -Wall -Wno-parentheses
ROOTONLYLIBS += -lHtml
BINS := 
BINCCFILES := 
# $(EXTRABINS:=.cc)

#++ Binary rules		 [in production, build it with 'bin']

$(addprefix $(bindir),$(BINS)): $(bindir)% : %.o

#++ shell script products.. 			[build it with 'bin']
BINSCRIPTS := 

#################################################################
#++ regression test scripts			[build it with 'test']

#################################################################
#++ include standard makefile from SoftRelTools.
include SoftRelTools/standard.mk
