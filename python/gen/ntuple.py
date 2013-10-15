"""
Generate NTuple

"""

import os
import sys
import commands
import subprocess
from sets import Set
import attr
import cleog
from tools.filetools import UserFile, TCLFile
from tools import qsub_jobs, backup_and_remove, \
     set_file, parse_opts_set
from gen import parse_for_modes_tasks
from attr import get_runs_range


__author__ = "Xin Shi <xs32@cornell.edu>"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2005-2011 Xin Shi"
__license__ = "GPL"
__revision__ = "$Revision$"


def main(opts, args):
    sys.stdout.write('dhad.gen: Processing NTuple ...\n')

    if args[0] == 'data':
        ntuple_data(args[1:])
    elif args[0] == 'generic':
        ntuple_generic(opts, args[1:])
    else:
        modes, label, tasks = parse_for_modes_tasks(args)

        if label in ['281ipbv12', '537ipbv12']:
            proc_version = '10.1.10'
        else:
            raise NameError(label)
    
        create_sh(opts, 'dtuple-generic-array.sh', label, proc_version)
        
        for mode in modes:
            ntuple_mode(opts, mode, tasks, label, proc_version)

        
def ntuple_data(args):

    opt = None
    if len(args) > 1:
        opt = args[1]
    
    label = args[0]
    if '281ipb' in label:
	numbers = ['31', '32_1', '32_2', '33', '35', '36', '37_1', '37_2']
        if opt == 'skim':
            numbers = ['31', '32', '33', '35', '36', '37']

    elif '537ipb' in label:
	numbers = ['43_1', '43_2', '44_1', '44_2', '44_3', '45_1', '45_2',
		   '46_1', '46_2']
    else:
	raise NameError(label)

    datasets = []
    for num in numbers:
        dataset = 'data' + num
        datasets.append(dataset)


    for dataset in datasets:
        bash_file =  create_bash_dtuple_data(dataset, label, opt)
        command = 'qsub ' + bash_file
        if opts.test:
            sys.stdout.write(bash_file + '\n')
            continue
        output = commands.getoutput(command)
        sys.stdout.write(output+ '\n')

def ntuple_generic(opts, args):
    grade = args[0]
    skim = args[1]
    label = args[2]

    datasets = []
    if 'data' in label:
        datasets.append(label)
        
    elif '281ipb' in label:
        numbers = ['31', '32', '33', '35', '36', '37']
        for num in numbers:
            dataset = 'data' + num
            datasets.append(dataset)

    elif '537ipb' in label:
        numbers = ['43', '44', '45', '46']
        for num in numbers:
            dataset = 'data' + num
            datasets.append(dataset)
    else:
        raise NameError(label)

    for dataset in datasets:
        if not opts.set or 'jobs' not in opts.set:
            update_dataselection_tcl('generic', dataset, grade, skim)
            logfile, qjobname, bash_file = create_bash_dtuple_generic(
                dataset, grade, skim, label)
            qsub_jobs(logfile, qjobname, bash_file, _test)
            continue

        njobs = parse_opts_set(opts.set, 'njobs')

        update_dataselection_tcl('generic', dataset, grade, skim, njobs)

        for job in range(njobs):
            subdataset = '%s_%s_%s' %(dataset, njobs, job+1)
            logfile, qjobname, bash_file = create_bash_dtuple_generic(
                subdataset, grade, skim, label)
            qsub_jobs(logfile, qjobname, bash_file, _test)


def ntuple_mode(opts, mode, tasks, label, proc_version):
    sys.stdout.write('dhad.gen: Mode %s, %s \n' % (mode, label))
    cleog.edit_fix_single_mode_list(opts, mode, label)

    create_filelist(opts, mode, tasks, label)
    jobtype = 'ntuple'

    if opts.set == 'interact':
        bash_file, logfile = create_bash_interact(opts, mode, label, proc_version)
        if opts.test:
            sys.stdout.write(bash_file + '\n')
        else:
            subprocess.Popen(bash_file)
        return 

    if opts.set == 'bg':
        bash_file, logfile = create_bash_interact(opts, mode, label, proc_version)
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
        return
    
    bash_file = cleog.create_bash_fix_mc_job(jobtype, label=label)
    if opts.test:
        sys.stdout.write(bash_file + '\n')
        return

    output = commands.getoutput(bash_file)
    sys.stdout.write(output+ '\n')

       

#--------------------------------------------------
# Functions 
#--------------------------------------------------

def create_bash_dtuple_data(dataset, label, opt):
    data_dir = os.path.join(attr.base, 'dat/data', attr.src)
    log_dir = data_dir
    outputdir = data_dir
    logfile_name = 'dtuple-' + dataset + '.txt'
    code_dir = os.path.join(attr.base, 'src', attr.src, 'proc')

    SKIM_DATA = ''
    if opt != None:
        if opt == 'skim':
            logfile_name = 'dtuple-' + dataset + '-skim.txt'
            outputdir = os.path.join(data_dir, 'skim')
            SKIM_DATA = 'export SKIM_DATA=1'
            create_data_skim_tcl(dataset, label)
        else:
            raise NameError(opt)
        
    logfile = os.path.join(log_dir, logfile_name)

    backup_and_remove(logfile)

    inputdata = dataset + '_dskim_evtstore'

    if not os.access(outputdir, os.F_OK) :
        sys.stdout.write('Creating dir %s...'  % outputdir)
        os.makedirs(outputdir)
        sys.stdout.write(' done.\n')
    fname = dataset + '_dskim'

    bash_file_name = dataset + '.sh'

    bash_file = os.path.join(attr.genpath, bash_file_name)

    bash_content =  '''#!/bin/sh
# request Bourne shell as shell for job
#$ -S /usr/local/bin/bash
#$ -o %s
#$ -j y
#$ -m ea
#$ -M xs32@cornell.edu

# print date and time
date
hostname

. /nfs/cleo3/Offline/scripts/cleo3logins
. /nfs/cleo3/Offline/scripts/cleo3defs

cd %s
. local_setup

export INPUTDATA=%s
export OUTPUTDIR=%s
export FNAME=%s
export USE_SETUP_ANALYSIS=1
%s
suez -f HadronicDNtupleProc/Test/loadHadronicDNtupleProc.tcl
# print date and time again
date

''' % (logfile, code_dir, inputdata, outputdir, fname, SKIM_DATA)
    
    fo = open(bash_file, 'w')
    fo.write(bash_content)

    return bash_file

def create_sh(opts, filename, label, proc_version):
    code_dir = os.path.join(attr.base, 'src', proc_version, 'proc')
    outputdir = os.path.join(attr.datpath, 'signal', label,
                             'dtuple_'+attr.cleog+'_'+attr.pass2)

    if not os.access(outputdir, os.F_OK) :
        sys.stdout.write('Creating dir %s ...\n'  % outputdir)
        os.makedirs(outputdir)

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

cd %s
. local_setup

export INDIR=$TOPDIR/dskim$SUFFIX

export INPUTDATA=USERLOCALMC_SKIMMED
export USE_SETUP_ANALYSIS=1

export OUTPUTDIR=$TOPDIR/dtuple$SUFFIX

export FILELIST=$SCRIPTDIR/pds_files/dt-$1
export FNAME=$1
suez -f HadronicDNtupleProc/Test/loadHadronicDNtupleProc.tcl

date
''' % code_dir 
    
    sh_file = os.path.join(attr.datpath, 'signal', label, 'src', filename)
    f = UserFile()
    f.append(sh_content)
    verbose = opts.verbose
    if opts.test:
        verbose = 1
    f.output(sh_file, verbose=verbose)

def create_filelist(opts, mode, tasks, label):
    filelistpath = os.path.join(attr.datpath, 'signal', label, 'src',
                                'pds_files')
    filelistname = 'dt-%s' %mode
    filelist_ = os.path.join(filelistpath, filelistname)
    
    filelist = UserFile()
    filelist.append('source_format sel PDSSourceFormat\n')
    filelist.append('source create myChain\n')

    for task in tasks:
        inputname = 'dskim_%s_%s.pds' %(mode, task)
        inputpath = os.path.join(
            attr.datpath, 'signal', label,
            'dskim_'+attr.cleog+'_'+attr.pass2)
        inputfile = os.path.join(inputpath, inputname)
        filelist.append('file add myChain %s\n' % inputfile)
        
    filelist.append('source act myChain beginrun startrun event endrun\n')

    verbose = opts.verbose
    if opts.test:
        verbose = 1
    filelist.output(filelist_, verbose=verbose)


def create_data_skim_tcl(dataset, label):

    if _debug:
        sys.stdout.write('\ndebug: dataset %s\n' %dataset)

    tclname = 'HadronicDNtupleProc/Test/DataSkim_%s.tcl' %dataset
    tclfile = os.path.join(attr.srcprocpath, tclname)
    sys.stdout.write('Writing %s...' %tclfile)
    
    datatype = 'data'
    run_event_set = Set([])
    for mode in attr.single_mode_list:
        evtname = '%s_%s_unqiue_%s.evt' %(datatype, mode, label)
        evtpath = os.path.join(attr.datpath, 'evt', label, 'events')
        unique_file = os.path.join(evtpath, evtname)
        f = UserFile(unique_file)
        events = Set(f.data)
        run_event_set.update(events)

    events = sorted(list(run_event_set))
    fo = UserFile()
    for event in events:
        run = int(event.split(' ')[0])
        if dataset == attr.get_dataset_by_run(run):
            fo.data.append('goto %sgo 1\n' %event)

    fo.output(tclfile)
    sys.stdout.write(' done.\n')



def create_bash_dtuple_generic(dataset, grade, skim, label):
    generic_dir = os.path.join(attr.base, 'dat/generic', attr.src)
    log_dir = generic_dir
    outputdir = generic_dir

    comname =  'generic_%s_%s_%s' %(grade, skim, dataset)

    logfile_name =  comname+'.txt' 
    code_dir = os.path.join(attr.base, 'src', attr.src, 'proc')
    logfile = os.path.join(log_dir, logfile_name)

    qjobname = 'g%s%s' % (skim.replace('lumi', ''),
                         dataset.replace('data', 'd'))

    if  len(qjobname) > 7:
        qjobname = dataset.replace('data', 'g')
        items = qjobname.split('_')
        if len(items) > 2:
            qjobname = '_'.join([items[0], items[-1]])

    inputdata =  comname

    backup_and_remove(logfile)

    if _debug:
        sys.stdout.write('\ndebug: outputdir %s\n' %generic_dir)
        sys.stdout.write('\ndebug: logfile %s\n' %logfile)
        sys.stdout.write('\ndebug: inputdata %s\n' %inputdata)
        sys.stdout.write('\ndebug: qjobname %s\n' %qjobname)
        
    if not os.access(outputdir, os.F_OK) :
        sys.stdout.write('Creating dir %s...'  % outputdir)
        os.makedirs(outputdir)
        sys.stdout.write(' done.\n')

    fname = comname

    bash_file_name = comname + '.sh'

    bash_file = os.path.join(attr.genpath, bash_file_name)

    bash_content =  '''#!/bin/sh
# request Bourne shell as shell for job
#$ -S /usr/local/bin/bash
#$ -j y
#$ -m ea
#$ -M xs32@cornell.edu

# print date and time
date
hostname

. /nfs/cleo3/Offline/scripts/cleo3logins
. /nfs/cleo3/Offline/scripts/cleo3defs

cd %s
. local_setup

export INPUTDATA=%s
export OUTPUTDIR=%s
export FNAME=%s
export USE_SETUP_ANALYSIS=1

suez -f HadronicDNtupleProc/Test/loadHadronicDNtupleProc.tcl
# print date and time again
date

''' % (code_dir, inputdata, outputdir, fname)

    f = UserFile()
    f.append(bash_content) 
    f.output(bash_file)

    return logfile, qjobname, bash_file

def update_dataselection_tcl(datatype, dataset, grade, skim, njobs=None):
    datasetname = '%s_%s_%s_%s' %(datatype, grade, skim, dataset)

    if datatype == 'generic':
        date = '20080728'
        skim = ''
        setskim = 'yes'
        if '-generic' in grade:
            setskim = 'no'
    else:
        raise NameError(inputdata)

    section_content = [
        'set skim %s \n' % setskim, 
        'set preliminaryPass2 no \n',
        'set millionMC no \n',
        'set mc yes \n',
        'set use_setup_analysis yes \n',
        'module sel EventStoreModule \n']

    tclname = 'HadronicDNtupleProc/Test/dataselection.tcl'
    tclfile = os.path.join(attr.srcprocpath, tclname)
    f = TCLFile(tclfile)
    init_data_length = len(f.data)

    if njobs != None:
        run_low, run_high = get_runs_range(datasetname)
        step = int((run_high - run_low)/float(njobs))
        
        for job in range(njobs):
            low = run_low + step*job
            high = low + step -1
            if job == njobs - 1 :
                high = run_high

            inputdata = '%s_%s_%s' %(datasetname, njobs, job+1)
            if inputdata in f.inputdata.keys():
                continue

            tmpline = 'if { ( $env(INPUTDATA) == "%s" ) } {\n' % inputdata
            evtstore = 'eventstore in %s %s %s runs %s %s \n}\n\n' %(
                date, grade, skim, low, high) 
            f.append(tmpline)
            f.data.extend(section_content)
            f.append(evtstore)

    else:
        inputdata = datasetname
        if inputdata not in f.inputdata.keys():
            tmpline = 'if { ( $env(INPUTDATA) == "%s" ) } {\n' % inputdata
            evtstore = 'eventstore in %s %s %s dataset %s \n}\n\n' %(
                date, grade, skim, dataset)

            f.append(tmpline)
            f.data.extend(section_content)
            f.append(evtstore)

    if len(f.data) > init_data_length:
        sys.stdout.write('Updating %s...' %tclfile)
        f.output(tclfile)
        sys.stdout.write(' done.\n')


def create_bash_interact(opts, mode, label, proc_version):
    bashname = 'dtuple-interact.sh' 

    CGRELEASE= attr.cleog
    P2RELEASE= attr.pass2
    DSKIMRELEASE = attr.dskim
    CGSUFFIX = '_'+ CGRELEASE
    SUFFIX   = CGSUFFIX + '_' + P2RELEASE
    TOPDIR   = os.path.join(attr.base, 'dat/signal', label)
    SCRIPTDIR = os.path.join(TOPDIR, 'src')

    logname = 'dtuple-%s.txt' % mode
    logpath = os.path.join(TOPDIR, 'log%s' %SUFFIX)
    logfile = set_file(extbase=logpath, comname=logname)

    code_dir = os.path.join(attr.base, 'src', proc_version, 'proc')
    outputdir = os.path.join(attr.base, 'dat/signal', label,
                             'dtuple_'+attr.cleog+'_'+attr.pass2)

    if not os.access(outputdir, os.F_OK) :
        sys.stdout.write('Creating dir %s ...\n'  % outputdir)
        os.makedirs(outputdir)

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

cd %s
. local_setup

STRING="%s"

if [ ! -e $SCRIPTDIR/tmp ] ; then mkdir -p $SCRIPTDIR/tmp; fi
if [ ! -e $TOPDIR/dtuple$SUFFIX ] ; then mkdir $TOPDIR/dtuple$SUFFIX ; fi

export INDIR=$TOPDIR/dskim$SUFFIX

export INPUTDATA=USERLOCALMC_SKIMMED
export USE_SETUP_ANALYSIS=1

export OUTPUTDIR=$TOPDIR/dtuple$SUFFIX/$LABEL
export FILELIST=$SCRIPTDIR/pds_files/dt-$STRING
export FNAME=$STRING
suez -f HadronicDNtupleProc/Test/loadHadronicDNtupleProc.tcl

date
''' %  (CGRELEASE, P2RELEASE, DSKIMRELEASE, CGSUFFIX, SUFFIX, TOPDIR, 
       SCRIPTDIR, code_dir, mode)

    bash_file = os.path.join(attr.datpath, 'signal', label, 'src', bashname)
    f = UserFile()
    f.append(bash_content)

    verbose = opts.verbose
    if opts.test:
        verbose = 1
    f.output(bash_file, verbose=verbose)
    os.chmod(bash_file, 0755)

    return bash_file, logfile
    

        
