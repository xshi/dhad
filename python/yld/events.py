"""
Module for selected events study

"""

import os
import sys
import tools
import attr
import yld
from attr import modes
from tools.filetools import UserFile 

__author__ = "Xin Shi <xs32@cornell.edu>"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2005-2010 Xin Shi"
__license__ = "GPL"
__revision__ = "$Revision$"


def main(opts, args):

    parsed = yld.parse_args(args)

    datatype  = parsed[0]
    tag       = parsed[1]
    modes     = parsed[2]
    label     = parsed[3]

    for mode in modes:
        if opts.set and opts.set == 'interact':
            if tag == 'single':
                single_tag_mode(datatype, mode, label, opts.test)
            else:
                raise ValueError(tag)
            continue

        script, logfile, qjobname = create_script_logfile_jobname(
            datatype, tag, mode, label, opts.test)

        bash_file = yld.create_bash_file(script, 'get_events.sh')
        tools.qsub_jobs(logfile, qjobname, bash_file, opts.test)


def single_tag_mode(datatype, mode, label, test=False):

    sys.stdout.write('dhad.yld.events: Processing Mode %s...' % mode)
    sys.stdout.flush()

    datpath = attr.datpath
    if datatype == 'signal':
        rootname = mode + '.root'
    elif datatype == 'data':
        rootname = '*.root'
    else:
        raise NameError(datatype)

    rootfile = os.path.join(datpath, datatype, label, rootname)

    pt = tools.add_rootfile(rootfile)

    evtname = datatype + '_' + mode + '.evt'
    evtpath = os.path.join(datpath, 'evt', label, 'events')
    evtfile = tools.check_and_join(evtpath, evtname)

    nselected, ntotal = output_run_event(pt, mode, evtfile, label, test)
    sys.stdout.write(' selected %s out of %s.\n' % (nselected, ntotal))
    sys.stdout.flush()

def output_run_event(pt, mode, evtfile, label, test=False):
    nselected = 0 
    ntotal = 0 
    mode_key, sign = tools.get_modekey_sign(mode)

    fo = open(evtfile , 'w')
    for pte in pt:
        ntotal += 1

        if sign != None: # single tag 
            d = tools.cuts.chooseD(mode_key, pte, sign, opt = label)
            if d != None:
                nselected = nselected + 1
                fo.write('%s %s\n' % (pte.run, pte.event))
        else: # double tag 
            raise NameError
            
        if test and nselected > 10:
            break
    fo.close()
    return nselected, ntotal


def create_script_logfile_jobname(datatype, tag, mode, label, test):
    prefix = 'dir_'+label
    logname = 'events_%s_%s.log' %(datatype, mode)
    logfile = tools.set_file(
        extbase=attr.yldlogpath, prefix=prefix,
        comname=logname)

    content =  '''#!/usr/bin/env python

from yld import events

events.single_tag_mode("%s", "%s", "%s", test=%s)

'''% (datatype, mode, label, test)

    mode, sign = tools.get_modekey_sign(mode)

    if tag == 'single':
        if sign == 1:
            sign = 'p'
        else:
            sign = 'm'
        filename = 'evt-%s-%s-m%s-%s-%s.py' % (datatype, tag, mode, sign, label)
        qjobname = 'evt%s,%s' % (mode, sign)
    else:
        filename = 'evt-%s-%s-m%s-%s-%s.py' % (datatype, tag, mode[0], mode[1], label)
        qjobname = 'evt%s,%s' % (mode[0], mode[1])

    file_ = os.path.join(attr.base, 'src', attr.src, 'yld', filename)

    f = UserFile()
    f.data.append(content) 
    f.output(file_)
    os.chmod(file_, 0755)

    return filename, logfile, qjobname

