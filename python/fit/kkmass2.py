"""
Module to fit KK mass with Gaussian 

"""

import os
import sys
import ROOT
import attr
import tools

from yld import parse_args
from tools import parse_opts_set
from tools.fits import mbc_gau_che, mbc_dline_che
from tools.filetools import UserFile
from fit import (load_roofit_lib, get_common_parameters, get_resolution_paras,
                 create_bash_file, init_paras_single)

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

    binbase = parse_opts_set(opts.set, 'binbase')
    binwidth =  parse_opts_set(opts.set, 'binwidth')
    numbins = parse_opts_set(opts.set, 'numbins')

    for i in xrange(numbins):
        lowmass = binbase+i*binwidth
        highmass = binbase+(i+1)*binwidth
        
        for mode in modes:
            if opts.set and 'interact' in opts.set:
                fit_single_mode(datatype, mode, label,
                                lowmass, highmass, opts.test)
            else:
                submit_batch_job(datatype, mode, label, lowmass,
                                 highmass, opts)


def fit_single_mode(datatype, mode, label, lowmass, highmass, test):
    evtpath = os.path.join(attr.datpath, 'sel', label, 'kkmass')
    modekey = tools.get_modekey(mode)
    tag = 'single'
    evtfile = tools.set_file('evt', datatype, modekey, tag,  prefix='',
                             forceCombine=1, extbase=evtpath)
    
    load_roofit_lib(datatype, label)
    cuts = '%f<kkmass && kkmass<%f' % (lowmass, highmass)
    #err_type = 'ASYM'
    err_type = 'SYMM'
    setGamma, setMres, setR, mc = get_common_parameters(datatype, label)
    Sigma, Fa, Fb, Sa, Sb = get_resolution_paras(modekey, label)

    N1, N2, Nbkgd1, Nbkgd2, md, p, sigmap1, xi = init_paras_single(
        label, datatype, 's', modekey)

    title1 = '%s : %s < KK mass < %s ' %(attr.modes[modekey]['uname'],
                                         lowmass, highmass)
    title2 = '%s : %s < KK mass < %s ' %(attr.modes[modekey]['unamebar'],
                                         lowmass, highmass)
    prefix='dir_%s/kkmass2/%s_%s' % (label, lowmass, highmass)
    epsfile = tools.set_file('eps', datatype, modekey, tag,
                             prefix=prefix, extbase=attr.figpath)
    txtfile = tools.set_file('txt', datatype, modekey, tag,
                             prefix=prefix, extbase=attr.fitpath)

    #mbc_gau_che(evtfile, mc, setMres, setGamma, setR, sigmap1, Sa, Sb, Fa,
    mbc_dline_che(evtfile, mc, setMres, setGamma, setR, sigmap1, Sa, Sb, Fa,
                  Fb, md, p, xi, N1, N2, Nbkgd1, Nbkgd2, title1, title2,
                  epsfile, txtfile, cuts=cuts, err_type=err_type, test=test)
    
    if not test:
        tools.eps2png(epsfile)
        tools.eps2pdf(epsfile)


def submit_batch_job(datatype, mode, label, lowmass, highmass, opts):
    script = create_python_script(opts, datatype, mode, label, lowmass, highmass)

    mode_sign = tools.get_modekey_sign(mode)
    ms = tools.pair_to_str(mode_sign)

    bash_file_name = 'fit-%s.sh' % ms
    bash_file = create_bash_file(opts, label, datatype, script, bash_file_name,
                                 subdir='kkmass2/%s_%s' % (lowmass, highmass))

    logname = '%s_%s.txt' %(datatype.replace('/', '_'), mode)
    
    prefix='dir_%s/kkmass2/%s_%s' % (label, lowmass, highmass)
    logfile = tools.set_file(extbase=attr.logpath, prefix=prefix, comname=logname)
    qjobname = 'kkm%s' % ms
    tools.qsub_jobs(logfile, qjobname, bash_file, opts.test)

    
def create_python_script(opts, datatype, mode, label, lowmass, highmass):
    content =  '''#!/usr/bin/env python

from fit import kkmass2

kkmass2.fit_single_mode("%s", "%s", "%s", %s, %s, %s)

'''% (datatype, mode, label, lowmass, highmass, opts.test)

    mode_sign = tools.get_modekey_sign(mode)

    ms = tools.pair_to_str(mode_sign)

    filename = 'fit-%s.py' % ms

    filename = filename.replace('/', '-')
    
    file_ = os.path.join(attr.datpath, datatype, label, 'src',
                         'kkmass2/%s_%s' % (lowmass, highmass) , filename)

    verbose = opts.verbose
    if opts.test:
        verbose = 1
        
    f = UserFile()
    f.append(content) 
    f.output(file_, verbose=verbose)
    os.chmod(file_, 0755)
    return filename
