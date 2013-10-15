#!/bin/sh
# request Bourne shell as shell for job
#$ -S /usr/local/bin/bash
#$ -j y
#$ -m a
#$ -M xs32@cornell.edu
date
hostname
unset USER_SRC USER_SHLIB
. /nfs/cleo3/Offline/scripts/cleo3logins
. /nfs/cleo3/Offline/scripts/cleo3defs

c3rel $DSKIMRELEASE


echo $SHELL
cd $SCRIPTDIR

export BATCH=$SGE_TASK_ID

export DECAYTITLE=$1
export INDIR=$TOPDIR/pass2$SUFFIX
export OUTDIR=$TOPDIR/dskim$SUFFIX
ls $C3_INFO/data/runinfo.runinfo > /dev/null

suez -f dskim.tcl

date

