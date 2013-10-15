"""
Module for Extracting yields for DHadronic Analysis

"""

import os
import sys
import tools
import attr
import time
import yld

from attr import modes
from itertools import ifilter
from tools import mcstringtodmode
from tools.filetools import UserFile


__author__ = "Xin Shi <xs32@cornell.edu>"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2005-2011 Xin Shi"
__license__ = "GPL"
__revision__ = "$Revision$"


def entry(opts, args):

    parsed = yld.parse_args(args)

    datatype  = parsed[0]
    tag       = parsed[1]
    modes     = parsed[2]
    label     = parsed[3]

    for mode in modes:
        if opts.set and opts.set == 'interact':
            if datatype == 'signal' and tag == 'single':
                process_signal_single_mode(mode, label, opts.test)
            else:
                raise ValueError(tag)
            continue
        
        script, logfile, qjobname = create_script_logfile_jobname(
            opts, datatype, tag, mode, label)

        bash_file = yld.create_bash_file(
            opts, datatype, label, script, 'get_crossfeeds.sh')
        tools.qsub_jobs(logfile, qjobname, bash_file, opts.test)


def process_signal_single_mode(mode, label, test):
    datatype = 'signal'
    prefix = 'dir_'+label
    sys.stdout.write('Processing crossfeeds for %s ...\n' %mode)
    sys.stdout.flush()
    
    files = {}
    for dbarmode in attr.single_mode_list:
        bkgname = '%s_%s_fakes_%s.evt' % (datatype, mode, dbarmode)
        bkgfile  = tools.set_file(
            extbase=attr.bkgpath, prefix=prefix, comname=bkgname)
        files[dbarmode] = open(bkgfile, 'w')

    rootfile = tools.get_rootfile(datatype, mode, label)
    pt = tools.add_rootfile(rootfile)

    modekey, sign = tools.get_modekey_sign(mode)

    t_iterstart = time.time()
    entries = 0
    for pte in ifilter(lambda x: x.ecm > 3.7, pt):
        entries += 1
        if test and entries > 1000:
            break

        otherside = tools.mcDmodeFixRad(tools.makeDDecaySubTree(pte, -sign)[0].mcDmode())
        for dbarmode in attr.single_mode_list:
            dbarmodekey, dbarsign = tools.get_modekey_sign(dbarmode)
            x = (modekey, sign)
            y = (dbarmodekey, dbarsign)
            considerevt = considerThisEvent(x, y, otherside)
            if not considerevt:
                continue
            mbc = 1.84
            d = tools.cuts.chooseD(y[0], pte, y[1])
            passed = False
            if d != None and tools.cuts.passDE(d, pte):
                passed = True; mbc = pte.dmbc[d]
            if x == (1,1) and y == (1,-1) and passed:
                print tools.mcdmodetostring(pte.mcdmode), tools.mcdmodetostring(pte.mcdbmode)

            files[dbarmode].write('%.5f %.5f %d\n' % (mbc, pte.ecm/2, int(passed)))

    pt.Delete()
    for f in files.values():
        f.close()

    dur = tools.duration_human(time.time()-t_iterstart)
    sys.stdout.write(' done %s.\n' %dur)


def considerThisEvent(x, y, otherside):
    
    mode_kmkspip = mcstringtodmode('K- K0 pi+')
    mode_kpkspim = mcstringtodmode('K+ K0 pi-')
    mode_3pipi0p = mcstringtodmode('pi+ pi- pi+ pi0')
    mode_3pipi0m = mcstringtodmode('pi- pi+ pi- pi0')
    mode_5pip = mcstringtodmode('pi+ pi+ pi+ pi- pi-')
    mode_5pim = mcstringtodmode('pi- pi- pi- pi+ pi+')
    mode_kskspip = mcstringtodmode('K0 K0 pi+')
    mode_kskspim = mcstringtodmode('K0 K0 pi-')
    

    if y[1] == 1:
        mcmode = modes[y[0]]['mcdmode']
    else:
        mcmode = modes[y[0]]['mcdbmode']
    considerevt = True
    if y[1]*x[1] == -1:
        # Check to ensure other side is not this decay!
        if otherside == mcmode:
            considerevt = False
        elif y == (3,1) and otherside == mode_kmkspip: # Avoid K- K0 pi+
            considerevt = False
        elif y == (3,-1) and otherside == mode_kpkspim:
            considerevt = False
        elif (y == (203,1) and (otherside == mode_3pipi0p)):
            considerevt = False
        elif y == (203,-1) and otherside == mode_3pipi0m:
            considerevt = False
        elif (y == (204,1) and (otherside == mode_5pip or otherside == mode_kskspip)):
            considerevt = False
        elif (y == (204,-1) and (otherside == mode_5pim or otherside == mode_kskspim)):
            considerevt = False
        
    if y[1]*x[1] == 1 and y[0] < 200:
        # Check if other side is a DCSD decay into this mode
##        print otherside, mcmode
        if otherside == mcmode:
            considerevt = False
        elif y == (3,1) and otherside == mode_kmkspip: # Avoid K- K0 pi+
            considerevt = False
        elif y == (3,-1) and otherside == mode_kpkspim:
            considerevt = False
    return considerevt


def create_script_logfile_jobname(opts, datatype, tag, mode, label):
    prefix = 'dir_'+label
    logname = 'bkg_%s_%s.log' %(datatype, mode)
    logfile = tools.set_file(
        extbase=attr.yldlogpath, prefix=prefix,
        comname=logname)

    content =  '''#!/usr/bin/env python

from yld import crossfeeds

crossfeeds.process_signal_single_mode("%s", "%s", test=%s)

'''% (mode, label, opts.test)

    mode, sign = tools.get_modekey_sign(mode)

    if tag == 'single':
        if sign == 1:
            sign = 'p'
        else:
            sign = 'm'
        filename = 'csf-%s-%s-m%s-%s.py' % (datatype, tag, mode, sign)
        qjobname = 'csf%s,%s' % (mode, sign)
    else:
        filename = 'csf-%s-%s-m%s-%s.py' % (datatype, tag, mode[0], mode[1])
        qjobname = 'csf%s,%s' % (mode[0], mode[1])

    file_ = os.path.join(attr.datpath, datatype, label, 'src', 'yld', filename)
    verbose = opts.verbose
    if opts.test:
        verbose = 1
    f = UserFile()
    f.data.append(content) 
    f.output(file_, verbose=verbose)
    os.chmod(file_, 0755)

    return filename, logfile, qjobname

