#!/bin/sh
# request Bourne shell as shell for job
#$ -S /usr/local/bin/bash
#$ -j y
#$ -m a
#$ -M xs32@cornell.edu
date
hostname
. /nfs/cleo3/Offline/scripts/cleo3logins
. /nfs/cleo3/Offline/scripts/cleo3defs

c3rel $CGRELEASE
echo $SHELL
cd $SCRIPTDIR

export BATCH=$SGE_TASK_ID
export NUMEVT=`cat $SCRIPTDIR/tag_numbers/$1`
export RUNNUMBER=`nl -s " " $SCRIPTDIR/runlist | grep " $SGE_TASK_ID " | awk '{ print $2 }'`
export DECAYTITLE=$1
export UDECAY=$SCRIPTDIR/tag_decfiles/$1.dec
export OUTDIR=$TOPDIR/cleog$CGSUFFIX

suez -f genmc.tcl
date

