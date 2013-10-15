"""
CLEOG 

"""


import sys
import os
import commands
import subprocess

import attr
import gen
import tools

from tools.filetools import UserFile, BASHFile
from tab.parse import tag_fragments


__author__ = "Xin Shi <xs32@cornell.edu>"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2005-2011 Xin Shi"
__license__ = "GPL"
__revision__ = "$Revision$"



def main(opts, args):
    sys.stdout.write('dhad.gen: Processing CLEOG ...\n')
    modes, label, tasks = gen.parse_for_modes_tasks(args)
    for mode in modes:
        cleog_mode(opts, mode, label, tasks)

	
def cleog_mode(opts, mode, label, tasks=[1]):
    sys.stdout.write('dhad.gen: Mode %s \n' %mode )
    sys.stdout.write('dhad.gen: Label %s \n' %label)
    sys.stdout.write('dhad.gen: Task %s \n' %tasks)

    check_decfile(opts, mode, label)
    check_and_copy_file(opts, label, 'genmc.tcl')
    check_and_copy_file(opts, label, 'runlist')
    check_and_copy_file(opts, label, 'cleog-generic-array.sh')

    jobtype = 'cleog'
    seeds = tools.parse_opts_set(opts.set, 'seeds')
    
    edit_fix_single_mode_list(opts, mode, label)

    create_tag_numbers_file(opts, mode, label)

    for task_id in tasks:
        if  opts.set and 'interact' in opts.set:
            bash_file, logfile = create_bash_interact(
                jobtype, mode, task_id, label=label, seeds=seeds)
            if opts.test:
                sys.stdout.write(bash_file + '\n')
            else:
                subprocess.Popen(bash_file)
            continue

        if opts.set and 'bg' in opts.set:
            bash_file, logfile = create_bash_interact(
                jobtype, mode, task_id, label=label, seeds=seeds)
            if opts.test:
                sys.stdout.write(bash_file + '\n')
                sys.stdout.write(logfile + '\n')                
            else:
                sys.stdout.write('Save log as %s.\n' %logfile)
                process = subprocess.Popen(bash_file, stdout=subprocess.PIPE,
                                                stderr=subprocess.STDOUT)
                f = UserFile()
                f.append(process.communicate()[0])
                f.output(logfile)

            continue

        bash_file = create_bash_fix_mc_job(jobtype, label, task_id, seeds=seeds)

        if opts.test:
            sys.stdout.write(bash_file + '\n')
            continue

        output = commands.getoutput(bash_file)
        sys.stdout.write(output+ '\n')


# --------------------
# Misc Functions
# --------------------

def create_bash_interact(jobtype, mode, task_id=1,
                         label='', seeds=None, verbose=0):
    bashname = '%s_task_%s.sh' %(jobtype, task_id)

    CGRELEASE= attr.cleog
    P2RELEASE= attr.pass2
    DSKIMRELEASE = attr.dskim
    CGSUFFIX = '_'+ CGRELEASE
    SUFFIX   = CGSUFFIX + '_' + P2RELEASE
    TOPDIR   = os.path.join(attr.base, 'dat/signal', label)
    SCRIPTDIR = os.path.join(TOPDIR, 'src')

    logname = '%s-%s-%s.txt' %(jobtype, mode, task_id)
    logpath = os.path.join(TOPDIR, 'log%s' %SUFFIX)
    logfile = tools.set_file(extbase=logpath, comname=logname)

    core_content = attr.gen_core_content[jobtype]

    if jobtype == 'cleog' and seeds != None:
        randomseeds = 'export RANDOMSEEDS=%s' % seeds
        core_content = randomseeds + core_content

    bash_content =  '''#!/usr/local/bin/bash
date
hostname

. /nfs/cleo3/Offline/scripts/cleo3logins
. /nfs/cleo3/Offline/scripts/cleo3defs

export CGRELEASE=%s
export P2RELEASE=%s
export DSKIMRELEASE=%s
export CGSUFFIX=%s
export SUFFIX=%s
export TOPDIR=%s
export SCRIPTDIR=%s
LOGDIR=$TOPDIR/log$SUFFIX

STRING="%s"
SGE_TASK_ID=%s

if [ ! -e $TOPDIR ] ; then mkdir -p $TOPDIR ; fi
if [ ! -e $LOGDIR ] ; then mkdir -p $LOGDIR ; fi

cd $SCRIPTDIR

export BATCH=$SGE_TASK_ID
export DECAYTITLE=$STRING
export UDECAY=$SCRIPTDIR/tag_decfiles/$STRING.dec

%s

# print date and time again
date



''' % (CGRELEASE, P2RELEASE, DSKIMRELEASE, CGSUFFIX, SUFFIX, TOPDIR, 
       SCRIPTDIR, mode, task_id, core_content)
    
    bash_file = os.path.join(SCRIPTDIR, bashname)

    f = UserFile()
    f.data.append(bash_content) 
    f.output(bash_file, verbose)
    os.chmod(bash_file, 0755)
    return bash_file, logfile
    

def create_bash_fix_mc_job(jobtype, label, task_id='1', seeds=None, verbose=0):
    
    CGRELEASE= attr.cleog
    P2RELEASE= attr.pass2
    DSKIMRELEASE = attr.dskim
    CGSUFFIX = '_'+ CGRELEASE
    SUFFIX   = CGSUFFIX + '_' + P2RELEASE
    TOPDIR   = os.path.join(attr.base, 'dat/signal', label)
    SCRIPTDIR = os.path.join(TOPDIR, 'src')

    DODECAYTREE='0'
    DOCLEOG='0'
    DOPASS2='0'
    DODSKIM='0'
    DONTUPLE='0'

    if jobtype == 'decaytree':
        DODECAYTREE='1'
    elif jobtype == 'cleog':
        DOCLEOG='1'
        if seeds != None:
            randomseeds = 'export RANDOMSEEDS=%s' % seeds
            create_sh('cleog-generic-array.sh', randomseeds)

    elif jobtype == 'pass2':
        DOPASS2='1'
    elif jobtype == 'dskim':
        DODSKIM='1'
    elif jobtype == 'ntuple':
        DONTUPLE='1'
    else:
        sys.stdout.write('\nUnknow jobtype: %s\n' % jobtype)
        sys.exit()
        

    bash_content =  '''#!/usr/local/bin/bash
export CGRELEASE=%s
export P2RELEASE=%s
export DSKIMRELEASE=%s
export CGSUFFIX=%s
export SUFFIX=%s
export TOPDIR=%s
export SCRIPTDIR=%s
LOGDIR=$TOPDIR/log$SUFFIX

DODECAYTREE=%s
DOCLEOG=%s
DOPASS2=%s
DODSKIM=%s
DONTUPLE=%s

FIXTASKID=%s

FILELISTINGS="fix_single_mode_list"

if [ ! -e $TOPDIR ] ; then mkdir -p $TOPDIR ; fi
if [ ! -e $LOGDIR ] ; then mkdir -p $LOGDIR ; fi

cd $SCRIPTDIR

for STRING in `cat $FILELISTINGS` ; do

if [[ $DODECAYTREE == 1 ]] ; then 
if [ ! -e $TOPDIR/decaytree$CGSUFFIX ] ; then mkdir $TOPDIR/decaytree$CGSUFFIX ; fi
qsub -l arch=lx24-x86 -o $LOGDIR/decaytree-$STRING-\$TASK_ID.txt \
-N decaytree-$STRING -t $FIXTASKID \
-v CGSUFFIX,TOPDIR,SCRIPTDIR,CGRELEASE \
decaytree-generic-array.sh $STRING
fi


if [[ $DOCLEOG == 1 ]] ; then 
if [ ! -e $TOPDIR/cleog$CGSUFFIX ] ; then mkdir $TOPDIR/cleog$CGSUFFIX ; fi
qsub -l arch=lx24-x86 -o $LOGDIR/cleog-$STRING-\$TASK_ID.txt \
-N cleog-$STRING -t $FIXTASKID \
-v CGSUFFIX,TOPDIR,SCRIPTDIR,CGRELEASE \
cleog-generic-array.sh $STRING
fi


if [[ $DOPASS2  == 1 ]] ; then
if [ ! -e $TOPDIR/pass2$SUFFIX ] ; then mkdir $TOPDIR/pass2$SUFFIX ; fi
qsub -l arch=lx24-x86 -o $LOGDIR/pass2-$STRING-\$TASK_ID.txt \
-N pass2-$STRING -hold_jid cleog-$STRING \
-t $FIXTASKID \
-v SUFFIX,CGSUFFIX,TOPDIR,SCRIPTDIR,P2RELEASE \
pass2-generic-array.sh $STRING
fi


if [[ $DODSKIM == 1 ]] ; then
if [ ! -e $TOPDIR/dskim$SUFFIX ] ; then mkdir $TOPDIR/dskim$SUFFIX ; fi
qsub -l arch=lx24-x86 -o $LOGDIR/dskim-$STRING-\$TASK_ID.txt \
-N dskim-$STRING -hold_jid pass2-$STRING \
-t $FIXTASKID \
-v SUFFIX,CGSUFFIX,TOPDIR,SCRIPTDIR,DSKIMRELEASE \
dskim-generic-array.sh $STRING
fi



if [[ $DONTUPLE == 1 ]] ; then
if [ ! -e $SCRIPTDIR/tmp ] ; then mkdir -p $SCRIPTDIR/tmp; fi
if [ ! -e $TOPDIR/dtuple$SUFFIX ] ; then mkdir $TOPDIR/dtuple$SUFFIX ; fi
qsub -l arch=lx24-x86 -o $LOGDIR/dtuple-$STRING.txt \
-N dtuple-$STRING -hold_jid dskim-$STRING -v SUFFIX,TOPDIR,SCRIPTDIR \
dtuple-generic-array.sh $STRING
fi
done


''' % (CGRELEASE, P2RELEASE, DSKIMRELEASE, CGSUFFIX, SUFFIX, TOPDIR , 
SCRIPTDIR, DODECAYTREE, DOCLEOG, DOPASS2 , DODSKIM, DONTUPLE, task_id)
    
    bash_file = os.path.join(SCRIPTDIR, 'fix_mc_job.sh')

    f = UserFile()
    f.data.append(bash_content) 
    f.output(bash_file, verbose)
    os.chmod(bash_file, 0755)
    return bash_file
    

def create_tag_numbers_file(opts, mode, label):
    tag_numbers = tools.parse_opts_set(opts.set, 'tag_numbers')
    if tag_numbers == None:
        tag_numbers = attr.get_tag_numbers(mode)        

    tag_numbers_file = os.path.join(attr.datpath, 'signal', label,
                                    'src', 'tag_numbers', mode)
    f = UserFile()
    f.data.append(str(tag_numbers))

    verbose = opts.verbose
    if opts.test:
        verbose = 1

    f.output(tag_numbers_file, verbose=verbose)


def edit_fix_single_mode_list(opts, mode, label):
    list_file = os.path.join(attr.datpath, 'signal', label, 'src',
                             'fix_single_mode_list')

    verbose = opts.verbose
    if opts.test:
        verbose = 1
    li = BASHFile()
    li.data = [mode]
    li.output(list_file, verbose=verbose)
    
  
def create_sh(filename, randomseeds=''):
    code_dir = os.path.join(attr.base, 'src', attr.src, 'gen')
    sh_file = tools.set_file(extbase=code_dir, comname=filename)

    sh_content =  '''#!/bin/sh
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

%s

export BATCH=$SGE_TASK_ID
export NUMEVT=`cat $SCRIPTDIR/tag_numbers/$1`
export RUNNUMBER=`nl -s " " $SCRIPTDIR/runlist | grep " $SGE_TASK_ID " | awk '{ print $2 }'`
export DECAYTITLE=$1
export UDECAY=$SCRIPTDIR/tag_decfiles/$1.dec
export OUTDIR=$TOPDIR/cleog$CGSUFFIX

suez -f genmc.tcl
date

''' % (randomseeds)
    
    f = UserFile()
    f.append(sh_content) 
    f.output(sh_file)

    
def check_decfile(opts, mode, label):
    toppath = os.path.join(attr.datpath, 'signal', label, 'src')
    decpath = os.path.join(toppath, 'tag_decfiles')
    decname = '%s.dec' % mode
    decfile = tools.check_and_join(decpath, decname)

    if 'Single' in mode:
        headername = mode.split('to')[0] + 'header'
        modename = mode.replace('Single_', '')
        check_decfile_single(opts, label, toppath, decfile, headername, modename)
        
    elif 'Double' in mode:
        headername = mode.split('to')[0] + 'header'
        if '_Dp_' in headername:
            headername = headername.replace('_Dp_', '_DpDm_')
        elif '_D0_' in headername:
            headername = headername.replace('_D0_', '_D0D0B_')
        else:
            raise NameError(headername)
        modename = mode.replace('Double_', '')
        check_decfile_double(opts, label, toppath, decfile, headername, modename)
        

    else:
        raise NameError(mode)

def check_decfile_single(opts, label, toppath, decfile, headername, modename):
    headerfile = os.path.join(toppath, 'tag_fragments', headername)
    fragfile = os.path.join(toppath, 'tag_fragments', modename)

    try:
        frag = open(fragfile, 'r')
    except IOError:
        tag_fragments(opts, [label])
        frag = open(fragfile, 'r')
         
    f = UserFile()
    fin = open(headerfile, 'r')
    f.extend(fin.readlines())
    f.extend(frag.readlines())
    f.append('End\n')

    verbose = opts.verbose
    if opts.test:
        verbose = 1
    
    f.output(decfile, verbose=verbose)
    fin.close()
    frag.close()


def check_decfile_double(opts, label, toppath, decfile, headername, modename):
    headerfile = os.path.join(toppath, 'tag_fragments', headername)
    modenames = modename.split('__')
    fragfile = os.path.join(toppath, 'tag_fragments', modenames[0])
    
    try:
        frag = open(fragfile, 'r')
    except IOError:
        tag_fragments(opts, [label])
        frag = open(fragfile, 'r')
         
    f = UserFile()
    fin = open(headerfile, 'r')
    f.extend(fin.readlines())
    f.extend(frag.readlines())
    fin.close()
    frag.close()

    fragfile2 = os.path.join(toppath, 'tag_fragments', modenames[1])
    frag2 = open(fragfile2, 'r')
    f.extend(frag2.readlines())
    frag2.close()
    
    f.append('End\n')
    verbose = opts.verbose
    if opts.test:
        verbose = 1
    
    f.output(decfile, verbose=verbose)
    frag2.close()


def check_and_copy_file(opts, label, filename):
    file_src = os.path.join(attr.genpath, filename)
    file_dst = os.path.join(attr.datpath, 'signal', label, 'src', filename)

    verbose = opts.verbose
    if opts.test:
        verbose = 1
    tools.check_and_copy(file_src, file_dst, verbose=verbose)
