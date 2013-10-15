"""
Module to select multple candidate events

"""

import os
import sys
import tools
import attr
import sel
from attr import modes
#from yld import parse_args, create_bash_file
from tools.cuts import chooseD, passDE, countDcand
from tools.filetools import UserFile 
from tools import parse_args, create_bash_file_pyline


__author__ = "Xin Shi <xs32@cornell.edu>"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2005-2011 Xin Shi"
__license__ = "GPL"
__revision__ = "$Revision$"


def main(opts, args):
    parsed = parse_args(args)
    datatype  = parsed[0]
    tag       = parsed[1]
    modes     = parsed[2]
    label     = parsed[3]

    for mode in modes:
        if opts.set and opts.set == 'interact':
            if tag == 'single' or tag == 'double':
                single_tag_mode(datatype, mode, label, opts.test)
            else:
                raise ValueError(tag)
        else:
            submit_batch_job(datatype, tag, mode, label, opts)

        # script, logfile, qjobname = create_script_logfile_jobname(
        #     datatype, tag, mode, label, opts.test)

        # bash_file = create_bash_file(script, 'multcand.sh', 'sel')
        # tools.qsub_jobs(logfile, qjobname, bash_file, opts.test)


def create_script_logfile_jobname(datatype, tag, mode, label, test):
    logname = '%s_%s.log' %(datatype, mode)
    logpath = os.path.join(attr.sellogpath, label, 'multcand')
    logfile = tools.set_file(extbase=logpath, comname=logname)

    content =  '''#!/usr/bin/env python

from sel import multcand

multcand.single_tag_mode("%s", "%s", "%s", test=%s)

'''% (datatype, mode, label, test)

    mode, sign = tools.get_modekey_sign(mode)

    if tag == 'single':
        if sign == [-1, 1]:
            filename = 'sel-%s-%s-m%s-%s.py' % (datatype, tag, mode, label)
            qjobname = 'sel%s' % mode 
        else:
            if sign == 1:
                sign = 'p'
            else: 
                sign = 'm'
            filename = 'sel-%s-%s-m%s-%s-%s.py' % (
                datatype, tag, mode, sign, label)
            qjobname = 'sel%s,%s' % (mode, sign)
            
    else:
        filename = 'sel-%s-%s-m%s-%s-%s.py' % (
            datatype, tag, mode[0], mode[1], label)
        qjobname = 'sel%s,%s' % (mode[0], mode[1])

    file_ = os.path.join(attr.base, 'src', attr.src, 'sel', filename)

    f = UserFile()
    f.data.append(content) 
    f.output(file_)
    os.chmod(file_, 0755)

    return filename, logfile, qjobname


def single_tag_mode(datatype, mode, label, test=False):
    sys.stdout.write('dhad.sel.multcand: Processing Mode %s...' % mode)
    sys.stdout.flush()

    datpath = attr.datpath
    rootfile = tools.get_rootfile(datatype, mode, label)

    pt = tools.add_rootfile(rootfile)
    selname = '%s_%s.evt' %(datatype, mode)

    if test:
        selname += '.test'
        
    nselected, ntotal = output_multcand(pt, mode, selname, label, test)
    
    sys.stdout.write(' selected %s out of %s.\n' % (nselected, ntotal))

    sys.stdout.flush()


def output_multcand(pt, mode, selname, label, test=False):
    selpath_single = os.path.join(attr.datpath, 'evt', label,
                                  'single_candidate')
    selfile_single = tools.check_and_join(selpath_single, selname)

    selpath_multiple = os.path.join(attr.datpath, 'evt', label,
                             'multiple_candidate')
    selfile_multiple = tools.check_and_join(selpath_multiple, selname)

    modekey, sign = tools.get_modekey_sign(mode)

    if sign == None:
        if not isinstance(modekey, tuple):
            raise ValueError(modekey)
        if modekey[0] in [0, 200]:
            signs = [-1]            
            if modekey[1] in [0, 200]:
                signs = [1, -1]
            modekey = modekey[1]

        elif modekey[1] in [0, 200]:
            signs = [1]
            modekey = modekey[0]            

        else:
            raise ValueError(modekey)
    else:
        signs = [sign]
        
    outf_s = open(selfile_single, 'w')
    outf_m = open(selfile_multiple, 'w')

    ntotal = 0
    nselected = 0

    for pte in pt:
        ntotal += 1
        if test and nselected >= 30:
            break 
            
        if pte.ecm < 3.7:
            continue
        for sign in signs:
            choice = chooseD(modekey, pte, sign)
            if choice != None and passDE(choice, pte):
                if pte.dmbc[choice] < 1.83:
                    continue
                dictchoice = outf_s
                if countDcand(modekey, pte, sign) >= 2:
                    dictchoice = outf_m
                dictchoice.write('%s %s %s\n' % (pte.dmbc[choice],
                                                 pte.ecm/2,
                                                 sign))
                nselected += 1

    outf_s.close()
    outf_m.close()

    sys.stdout.write('Saved as %s \n' %selfile_single)
    sys.stdout.write('Saved as %s \n' %selfile_multiple)
    
    return nselected, ntotal

def submit_batch_job(datatype, tag, mode, label, opts):
    mode_sign = tools.get_modekey_sign(mode)
    ms = tools.pair_to_str(mode_sign)
    pyline = 'from sel import multcand; multcand.%s_tag_mode("%s", "%s", "%s", test=%s)'% (tag, datatype, mode, label, opts.test)

    bash_file_name = 'multcand-%s.sh' % ms 
    bash_file = create_bash_file_pyline(opts, label, datatype, pyline,
                                        bash_file_name, subdir='sel')
    logname = '%s_%s.txt' %(datatype.replace('/', '_'), mode)
    logpath = os.path.join(attr.logpath, label, 'multcand')
    logfile = tools.set_file(extbase=logpath, comname=logname)
    qjobname = 'sel%s' % ms

    tools.qsub_jobs(logfile, qjobname, bash_file, opts.test)


