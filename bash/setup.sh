#!/bin/bash

#----------------------------------------------------------------------
# Release Parameters
#----------------------------------------------------------------------

CLEOSW=20080228_FULL

#----------------------------------------------------------------------
# CLEO Software settings
#----------------------------------------------------------------------
export dhad=$HOME/work/CLEO/analysis/DHad
export PATH=$dhad/bin:$PATH
export rel=$rel
export src=$dhad/src/$rel


. /nfs/cleo3/Offline/scripts/cleo3logins
. /nfs/cleo3/Offline/scripts/cleo3defs

c3rel $CLEOSW

export CLEO3DEF_SILENT=1
export USER_SRC=$dhad/src/$rel/proc
export USER_BUILD=${USER_SRC}/build
export USER_SHLIB=${USER_BUILD}/Linux/shlib

c3rel $C3LIB


#ln -sf $dhad/src/$rel/python/dhad.py $dhad/bin/dhad-$rel
#ln -sf $dhad/bin/dhad-$rel $dhad/bin/dhad

#----------------------------------------------------------------------
# For ROOT and python 
#----------------------------------------------------------------------
# CLEO default ROOT and Python
setpyroot c

# Local Python and ROOT 
#setpyroot l

# Hacked ROOT with SQRT scale support  
#setpyroot h

# Redirect the C3_DATA // should be used in testing case only!
#export C3_DATA=${USER_SRC}/data
