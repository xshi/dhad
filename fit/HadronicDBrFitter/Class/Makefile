###################################################
#  Makefile: General library and executable maker 
###################################################

#FFLAG = -O -qextname -qrndsngl -g
FFLAG = -g

# this flag is for debugging my own code
FFLAGDEB = -O1 -static -g


CERNBAG = $(CERNLIB)/cernpatch.o \
          -L$(CERNLIB) -lpacklib


#-----------------
#  Action section 
#-----------------

#HDBFitterMain: HDBFitterMain.o
#	f77 -o /home/wsun/maxl/gamma $(FFLAG) \
#	gamma.o $(CERNBAG) -lUfor -lfor -lFutil -lots -L$(DLIBDIR) -lqqjs73

#-----------------------------
# Additional dependency rules
#-----------------------------
.cc.o:
	$(CXX) -I../HadronicDBrFitter -I/nfs/cleo3/Offline/rel/current/other_sources -c $<
