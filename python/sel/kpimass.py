"""
Module for K pi mass Study

"""

import os
import sys
import ROOT
import attr
import tools

from yld import parse_args
from tools import set_file, DHadTable, ptobj, trkFourTuple, invmass,\
     create_bash_file_pyline
from tools.cuts import chooseD
from tools.filetools import UserFile 


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

    debug = opts.debug
    test = opts.test
    
    for mode in modes:
        if opts.set and opts.set == 'interact':
            single_tag_mode(datatype, mode, label, test)
        else:
            submit_batch_job(datatype, mode, label, opts)


def single_tag_mode(datatype, mode, label, test):
    rootfile = tools.get_rootfile(datatype, mode, label)
    if test:
        sys.stdout.write('rootfile: %s \n' %rootfile)

    pt = tools.add_rootfile(rootfile)

    evtfile = get_evtfile(datatype, mode, label, 'kpimass', test=test)

    nselected = 0 
    ntotal = 0 
    modekey, sign = tools.get_modekey_sign(mode)
    if sign == None:
        raise ValueError(sign)

    sys.stdout.write('Saving %s ...' %evtfile)
    sys.stdout.flush()
    
    fo = open(evtfile , 'w')
    for pte in pt:
        ntotal += 1
        if test and nselected > 100:
            break

        d = chooseD(modekey, pte, sign)
        
        if d != None:
            dcand = ptobj(pte, d)
            mbc = dcand.dmbc
            if mbc > 1.83 and mbc < 1.89:

                k1 = trkFourTuple(ptobj(pte, dcand.ddau1), 'k')
                k2 = trkFourTuple(ptobj(pte, dcand.ddau2), 'k')
                pi = trkFourTuple(ptobj(pte, dcand.ddau3), 'pi')

                kpimass = invmass(k1, pi)
                
                fo.write('%.5f %.5f %.5f %d\n' % (mbc, pte.ecm/2,
                                                  kpimass, pte.dcsign[d]))
                nselected += 1

    fo.close()

    sys.stdout.write(' selected %s out of %s.\n' % (nselected, ntotal))


def get_evtfile(datatype, mode, label, var, test=False):
    evtname = '%s_%s.evt' %(datatype, mode)
    if test:
        evtname += '.test'
        
    evtpath = os.path.join(attr.datpath, 'sel', label, var)
    evtfile = tools.check_and_join(evtpath, evtname)
    return evtfile


def submit_batch_job(datatype, mode, label, opts):
    mode_sign = tools.get_modekey_sign(mode)
    ms = tools.pair_to_str(mode_sign)

    pyline = 'from sel import kpimass; kpimass.single_tag_mode("%s", "%s", "%s", test=%s)'% (datatype, mode, label, opts.test)

    bash_file_name = 'kpimass-%s.sh' % ms
    bash_file = create_bash_file_pyline(opts, label, datatype, pyline,
                                        bash_file_name, subdir='sel')
    logname = '%s_%s.txt' %(datatype.replace('/', '_'), mode)
    logpath = os.path.join(attr.logpath, label, 'sel', 'kpimass')
    logfile = tools.set_file(extbase=logpath, comname=logname)
    qjobname = 'sel%s' % ms

    tools.qsub_jobs(logfile, qjobname, bash_file, opts.test)


