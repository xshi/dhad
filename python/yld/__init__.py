"""
Module for Extracting yields for DHadronic Analysis

"""

import os
import sys
import commands

import attr
import tools
from tools import cuts, parse_args, create_bash_file_pyline
from tools.filetools import UserFile
from attr.modes import set_modes_attr

__author__ = "Xin Shi <xs32@cornell.edu>"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2005-2011 Xin Shi"
__license__ = "GPL"
__revision__ = "$Revision$"


def main(opts, args):

    if args[0] == 'crossfeeds':
        import crossfeeds
        crossfeeds.entry(opts, args[1:])
        return

    if args[0] == 'events':
        import events
        events.main(opts, args[1:])
        return

    if args[0] == 'backgrounds':
        import backgrounds
        backgrounds.main(opts, args[1:])
        return

    if args[0] == 'var':
        import var
        var.main(opts, args[1:])
        return

    parsed = parse_args(args)

    datatype  = parsed[0]
    tag       = parsed[1]
    modes     = parsed[2]
    label     = parsed[3]

    for mode in modes:
        if opts.set and opts.set == 'interact':
            if tag == 'single':
                single_tag_mode(datatype, mode, label, opts.test)
            elif tag == 'double':
                double_tag_mode(datatype, mode, label, opts.test)
            else:
                raise ValueError(tag)
        else:
            submit_batch_job(datatype, tag, mode, label, opts)

        # script, logfile, qjobname = create_script_logfile_jobname(
        #     opts, datatype, tag, mode, label, opts.test)
        # bash_file = create_bash_file(opts, datatype, label, script)
        # tools.qsub_jobs(logfile, qjobname, bash_file, opts.test)


def create_bash_file(opts, datatype, label, script,
                     bashname='get-yields.sh',
                     subdir='yld',  optcommand=''):
    script_dir = os.path.join(
        attr.datpath, datatype, label, 'src', subdir)

    bash_content =  '''#!/bin/sh
#$ -S /usr/local/bin/bash
#$ -j y
#$ -m a
#$ -M xs32@cornell.edu

date
hostname

.  ~/.bashrc
setdhad %s 

%s

cd %s
./%s

date

''' % (attr.version, optcommand, script_dir, script)
    
    bash_file = os.path.join(script_dir, bashname)

    verbose = opts.verbose
    if opts.test:
        verbose = 1
    f = UserFile()
    f.append(bash_content) 
    f.output(bash_file, verbose=verbose)
    os.chmod(bash_file, 0755)
    return bash_file


def create_script_logfile_jobname(opts, datatype, tag, mode, label, test):
    logfile = tools.set_file('log', datatype, mode, tag,
                             prefix='dir_'+label, extbase=attr.yldlogpath)

    content =  '''#!/usr/bin/env python

import yld

yld.%s_tag_mode("%s", "%s", "%s", test=%s)

'''% (tag, datatype, mode, label, test)

    mode, sign = tools.get_modekey_sign(mode)

    if tag == 'single':
        if sign == 1:
            sign = 'p'
        else:
            sign = 'm'
        filename = '%s-%s-m%s-%s.py' % (datatype, tag, mode, sign)
        qjobname = 'yld%s,%s' % (mode, sign)
    else:
        filename = '%s-%s-m%s-%s.py' % (datatype, tag, mode[0], mode[1])
        qjobname = 'yld%s,%s' % (mode[0], mode[1])

    file_ = os.path.join(attr.datpath, datatype, label, 'src', 'yld', filename)
    verbose = opts.verbose
    if opts.test:
        verbose = 1
        sys.stdout.write('logfile: %s\n' %logfile)
    f = UserFile()
    f.data.append(content) 
    f.output(file_, verbose=verbose)
    os.chmod(file_, 0755)

    return filename, logfile, qjobname


def single_tag_mode(datatype, mode, label, test=False):
    sys.stdout.write('dhad.yield: Processing Mode %s...' % mode)
    sys.stdout.flush()

    set_modes_attr(label)
    
    rootfile = tools.get_rootfile(datatype, mode, label)
    pt = tools.add_rootfile(rootfile)

    evtname = datatype + '_' + mode + '.evt'
    evtpath = os.path.join(attr.datpath, 'evt', label)
    evtfile = tools.check_and_join(evtpath, evtname)

    logname = datatype + '_' + mode + '.log'
    logpath = os.path.join(attr.logpath, 'evt', label)
    logfile = tools.check_and_join(logpath, logname)

    if test:
        sys.stdout.write('\ntest: rootfile %s \n' % rootfile)
        evtfile = evtfile + '.test'
        sys.stdout.write('\ntest: evtfile %s\n' %evtfile)
        logfile = logfile + '.test'
        sys.stdout.write('\ntest: logfile %s\n' %logfile)

    nselected, ntotal = output_mbc_ebeam(pt, mode, evtfile, logfile, label, test)
    sys.stdout.write(' selected %s out of %s.\n' % (nselected, ntotal))
    sys.stdout.flush()



def output_mbc_ebeam(pt, mode, evtfile, logfile, label, test=False):
    nselected = 0 
    ntotal = 0 
    mode_key, sign = tools.get_modekey_sign(mode)

    alt_deltae = None
    opt = ''
    mbc_opt = ''
    
    if '/nofsr' in label:
        fsr_no = 0

    if '/trig' in label:
        opt = 'trig'

    if '/trig2' in label:
        opt = 'trig2'

    if '/desideband' in label:
        side = label.split('/desideband_')[1]
        alt_deltae = attr.desideband(mode_key, side)

    fo = open(evtfile , 'w')
    for pte in pt:
        ntotal += 1

        if sign != None: # single tag
            if '/nofsr' in label:
                mcdmode  = attr.modes[mode_key]['mcdmode']
                mcdbmode = attr.modes[mode_key]['mcdbmode']

                if (sign == 1 and pte.mcdmode != mcdmode) or \
                        (sign == -1 and pte.mcdbmode != mcdbmode):
                    fsr_no+=1
                    continue

            d = tools.cuts.chooseD(mode_key, pte, sign,
                                   alt_deltae=alt_deltae, opt=opt)
            if d != None:
                mbc = tools.cuts.get_mBC(mode_key, pte, d, opt=mbc_opt)
                if mbc > 1.83 and mbc < 1.89: 
                    fo.write('%.5f %.5f %d\n' % (mbc, pte.ecm/2, pte.dcsign[d]))
                    nselected = nselected + 1

        else: # double tag
            if '/nofsr' in label:
                mcdmode  = attr.modes[mode_key[0]]['mcdmode']
                mcdbmode = attr.modes[mode_key[1]]['mcdbmode']
                if pte.mcdmode != mcdmode or pte.mcdbmode != mcdbmode:
                    fsr_no+=1
                    continue
  
            dd = tools.cuts.chooseDD(mode_key[0], mode_key[1], pte, opt=opt)
            if dd != None:
                d = pte.d[dd]
                dbar = pte.dbar[dd]
                if pte.dmbc[d] > 1.83 and pte.dmbc[d] < 1.89 and \
                   pte.dmbc[dbar] > 1.83 and pte.dmbc[dbar] < 1.89:
                    fo.write('%f %f %f\n' % (
                        pte.dmbc[d], pte.dmbc[dbar], pte.ecm/2))
                    nselected = nselected + 1
                    
        if test and nselected > 10:
            break
    fo.close()

    log = open(logfile , 'w')
    log.write('Name \t|| Value \n')
    log.write('Mode \t| %s\n' % mode)
    log.write('Total \t| %s\n' % ntotal)
    log.write('Select \t| %s\n' % nselected)
    try:
        eff = float(nselected)/ntotal
    except ZeroDivisionError:
        eff = 'INF' 

    if '/nofsr' in label:
        log.write('FSR  \t| %s\n' % fsr_no)
        eff = float(nselected)/(ntotal - fsr_no)

    log.write('Eff \t| %s\n' % eff)
    log.close()

    return nselected, ntotal

def double_tag_mode(datatype, mode, label, test=False):
    sys.stdout.write('dhad.yield: Processing Mode %s...' % mode)
    sys.stdout.flush()

    set_modes_attr(label)

    rootfile = tools.get_rootfile(datatype, mode, label)
    pt = tools.add_rootfile(rootfile)

    evtname = datatype + '_' + mode + '.evt'
    evtpath = os.path.join(attr.datpath, 'evt', label)
    evtfile = tools.check_and_join(evtpath, evtname)

    logname = datatype + '_' + mode + '.log'
    logpath = os.path.join(attr.logpath, 'evt', label)
    logfile = tools.check_and_join(logpath, logname)

    if test:
        sys.stdout.write('\ntest: rootfile %s \n' % rootfile)
        evtfile = evtfile + '.test'
        sys.stdout.write('\ntest: evtfile %s\n' %evtfile)
        logfile = logfile + '.test'
        sys.stdout.write('\ntest: logfile %s\n' %logfile)

    opt = label 
    nselected, ntotal = output_mbc_ebeam(pt, mode, evtfile, logfile, label, test)
    sys.stdout.write(' selected %s out of %s.\n' % (nselected, ntotal))
    sys.stdout.flush()


def output_run_event(pt, mode, test=False):

    run_event_list = []
    mode_key, sign = tools.get_modekey_sign(mode)
    nselected = 0
    for pte in pt:
        if sign != None: # single tag 
            d = tools.cuts.chooseD(mode_key, pte, sign, opt = '')
            if d != None:
                nselected += 1
                run_event_list.append('%s:%s' %(pte.run, pte.event))
        else:
            raise NameError

        if test and nselected > 10:
            break

    return run_event_list

    
def submit_batch_job(datatype, tag, mode, label, opts):
    mode_sign = tools.get_modekey_sign(mode)
    ms = tools.pair_to_str(mode_sign)

    pyline = 'import yld; yld.%s_tag_mode("%s", "%s", "%s", test=%s)'% (
        tag, datatype, mode, label, opts.test)

    bash_file_name = 'get-yld.sh' 
    bash_file = create_bash_file_pyline(opts, label, datatype, pyline,
                                        bash_file_name)
    logname = '%s_%s.txt' %(datatype.replace('/', '_'), mode)
    logpath = os.path.join(attr.logpath, label, 'yld')
    logfile = tools.set_file(extbase=logpath, comname=logname)
    qjobname = 'sel%s' % ms

    tools.qsub_jobs(logfile, qjobname, bash_file, opts.test)

