"""
Module for Extracting yields from Backgrounds 

"""

import os
import sys
import tools
import attr
import yld
import time
from attr.modes import modes
from tools.filetools import UserFile 

__author__ = "Xin Shi <xs32@cornell.edu>"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2005-2010 Xin Shi"
__license__ = "GPL"
__revision__ = "$Revision$"


def main(opts, args):

    if args[0] == 'peak':
        process_peak(opts, args[1:])
        return

    parsed = yld.parse_args(args)
    datatype  = parsed[0]
    tag       = parsed[1]
    modes     = parsed[2]
    label     = parsed[3]

    for mode in modes:
        if opts.set and opts.set == 'interact':
            if 'generic' in datatype and tag == 'single':
                process_generic_single_mode(datatype, mode, label, opts.test)
            else:
                raise ValueError(tag)
            continue
        
        script, logfile, qjobname = create_script_logfile_jobname(
            datatype, tag, mode, label, opts.test)

        bash_file = yld.create_bash_file(script, 'get_backgrounds.sh')
        tools.qsub_jobs(logfile, qjobname, bash_file, opts.test)

def process_generic_single_mode(datatype, mode, label, test):
    prefix = 'dir_'+label
    sys.stdout.write('Processing backgrounds for %s ...\n' %mode)
    sys.stdout.flush()
    
    files = {}

    inputlabel = label
    if 'noxfeed' in label:
        inputlabel = label.split('/')[0]

    rootfile = tools.get_rootfile(datatype, mode, inputlabel)

    if test:
        sys.stdout.write('\ntest: rootfile %s\n' % rootfile)
    pt = tools.add_rootfile(rootfile)

    bkgname = '%s_%s.evt' %(datatype, mode)
    bkgname = bkgname.replace('/', '_')
    
    bkgfile = tools.set_file(
        extbase=attr.bkgpath(), prefix=prefix, comname=bkgname)

    t_iterstart = time.time()
    nfaked, npassed, ntotal = output_mbc_ebeam(
        pt, mode, label, bkgfile, test)
    dur = tools.duration_human(time.time()-t_iterstart)

    sys.stdout.write('faked %s , passed %s , total %s. done in %s.\n'
                     %(nfaked, npassed, ntotal, dur))
    sys.stdout.flush()



def output_mbc_ebeam(pt, mode, label, bkgfile, test):
    cut_opt = 'nosig'
    if 'noxfeed' in label:
        cut_opt += '_noxfeed'

    modekey, sign = tools.get_modekey_sign(mode)

    ntotal = 0
    npassed = 0 
    nfaked = 0

    fakemodes = {}
    modefile = bkgfile.replace('.evt', '.txt')
    
    if test:
        bkgfile = '%s.test' % bkgfile
        modefile = '%s.test' % modefile
        sys.stdout.write('\ntest: bkgfile %s\n' %bkgfile)
        sys.stdout.write('\ntest: modefile %s\n' %modefile)

    fo = open(bkgfile , 'w')

    for pte in pt:
        ntotal += 1
        if sign != None: # single tag 
            d = tools.cuts.chooseD(modekey, pte, sign)
            if d != None:
                npassed +=  1
            d = tools.cuts.chooseD(modekey, pte, sign, opt=cut_opt)
            if d != None:
                nfaked += 1
                mbc = tools.cuts.get_mBC(modekey, pte, d, opt = '')                
                fo.write('%.5f %.5f %d\n' % (mbc, pte.ecm/2, pte.dcsign[d]))
                count_fakemodes(fakemodes, pte.mcdmode, pte.mcdbmode)
        else: 
            raise NameError(sign)

        if test and ntotal > 1000:
            break

    fo.close()
    pt.Delete()
    output_fakemodes(fakemodes, modefile)
    
    return nfaked, npassed, ntotal



def create_script_logfile_jobname(datatype, tag, mode, label, test):
    prefix = 'dir_'+label
    logname = 'bkg_%s_%s.log' %(datatype, mode)
    logname = logname.replace('/', '_')
    
    logfile = tools.set_file(
        extbase=attr.yldlogpath, prefix=prefix,
        comname=logname)

    content =  '''#!/usr/bin/env python

from yld import backgrounds

backgrounds.process_generic_single_mode("%s", "%s", "%s", test=%s)

'''% (datatype, mode, label, test)

    mode, sign = tools.get_modekey_sign(mode)

    if tag == 'single':
        if sign == 1:
            sign = 'p'
        else:
            sign = 'm'
        filename = 'bkg-%s-%s-m%s-%s-%s.py' % (
            datatype, tag, mode, sign, label)
        qjobname = 'bkg%s%s' % (mode, sign)
    else:
        filename = 'bkg-%s-%s-m%s-%s-%s.py' % (
            datatype, tag, mode[0], mode[1], label)
        qjobname = 'bkg%s,%s' % (mode[0], mode[1])

    file_ = os.path.join(attr.base, 'src', attr.src, 'yld', filename)
    
    f = UserFile()
    f.data.append(content) 
    f.output(file_)
    os.chmod(file_, 0755)

    return filename, logfile, qjobname

def count_fakemodes(fakemodes, mcdmode, mcdbmode):
    mcdmode = tools.cuts.remove_gamma(mcdmode)
    mcdbmode = tools.cuts.remove_gamma(mcdbmode)
    modepair = '%s,%s' %(mcdmode, mcdbmode)

    if modepair in fakemodes:
        fakemodes[modepair] += 1
    else:
        fakemodes[modepair] =1
        
def output_fakemodes(fakemodes, modefile):
    f = UserFile()
    f.data.append('Mode || Number \n')
    for k, v in fakemodes.items():
        f.data.append('%s | %s \n' %(k, v))
    f.output(modefile)
                 

def process_peak(opts, args):
    parsed = yld.parse_args(args)
    datatype  = parsed[0]
    tag       = parsed[1]
    modes     = parsed[2]
    label     = parsed[3]

    for mode in modes:
        if opts.set and opts.set == 'interact':
            process_peak_generic_single_mode(datatype, mode, label, opts.test)
            continue

    script, logfile, qjobname = create_peak_script_logfile_jobname(
        datatype, tag, mode, label, opts.test)
    
    bash_file = yld.create_bash_file(script, 'get_backgrounds_peak.sh')
    tools.qsub_jobs(logfile, qjobname, bash_file, opts.test)

    

def process_peak_generic_single_mode(datatype, mode, label, test):
    prefix = 'dir_'+label
    sys.stdout.write('Processing backgrounds peak for %s ...\n' %mode)
    sys.stdout.flush()
    
    files = {}

    rootname = '*.root'
    rootfile = os.path.join(attr.datpath, datatype, label, rootname)

    if test:
        sys.stdout.write('\ntest: rootfile %s\n' % rootfile)
    pt = tools.add_rootfile(rootfile)

    bkgname = 'peak_%s_%s.evt' %(datatype, mode)
    bkgname = bkgname.replace('/', '_')
    
    bkgfile = tools.set_file(
        extbase=attr.bkgpath(), prefix=prefix, comname=bkgname)

    t_iterstart = time.time()
    npeak, nfaked, npassed, ntotal = output_peak_mbc_ebeam(
        pt, mode, bkgfile, test)
    dur = tools.duration_human(time.time()-t_iterstart)

    sys.stdout.write('peak %s, faked %s , passed %s , total %s. done in %s.\n'
                     %(npeak, nfaked, npassed, ntotal, dur))
    sys.stdout.flush()


def output_peak_mbc_ebeam(pt, mode, bkgfile, test):
    modekey, sign = tools.get_modekey_sign(mode)

    ntotal = 0
    npassed = 0 
    nfaked = 0
    npeak = 0 

    fakemodes = {}
    modefile = bkgfile.replace('.evt', '.txt')
    
    if test:
        bkgfile = '%s.test' % bkgfile
        modefile = '%s.test' % modefile
        sys.stdout.write('\ntest: bkgfile %s\n' %bkgfile)
        sys.stdout.write('\ntest: modefile %s\n' %modefile)

    fo = open(bkgfile , 'w')

    for pte in pt:
        ntotal += 1
        if sign != None: # single tag 
            d = tools.cuts.chooseD(modekey, pte, sign)
            if d != None:
                npassed +=  1
            d = tools.cuts.chooseD(modekey, pte, sign, opt='nosig')
            if d != None:
                nfaked += 1
                mbc = tools.cuts.get_mBC(modekey, pte, d, opt = '')
                if mbc < 1.86 or mbc > 1.87:
                    continue
                npeak += 1
                fo.write('%.5f %.5f %d\n' % (mbc, pte.ecm/2, pte.dcsign[d]))
                count_fakemodes(fakemodes, pte.mcdmode, pte.mcdbmode)
        else: 
            raise NameError(sign)

        if test and ntotal > 10000:
            break

    fo.close()
    pt.Delete()
    output_fakemodes(fakemodes, modefile)
    
    return npeak, nfaked, npassed, ntotal


def create_peak_script_logfile_jobname(datatype, tag, mode, label, test):
    prefix = 'dir_'+label
    logname = 'peak_bkg_%s_%s.log' %(datatype, mode)
    logname = logname.replace('/', '_')
    
    logfile = tools.set_file(
        extbase=attr.yldlogpath, prefix=prefix,
        comname=logname)

    content =  '''#!/usr/bin/env python

from yld import backgrounds

backgrounds.process_peak_generic_single_mode("%s", "%s", "%s", test=%s)

'''% (datatype, mode, label, test)

    mode, sign = tools.get_modekey_sign(mode)

    if tag == 'single':
        if sign == 1:
            sign = 'p'
        else:
            sign = 'm'
        filename = 'peak-bkg-%s-%s-m%s-%s-%s.py' % (
            datatype, tag, mode, sign, label)
        qjobname = 'bkg%s%s' % (mode, sign)
    else:
        filename = 'peak-bkg-%s-%s-m%s-%s-%s.py' % (
            datatype, tag, mode[0], mode[1], label)
        qjobname = 'bkg%s,%s' % (mode[0], mode[1])

    file_ = os.path.join(attr.base, 'src', attr.src, 'yld', filename)
    
    f = UserFile()
    f.data.append(content) 
    f.output(file_)
    os.chmod(file_, 0755)

    return filename, logfile, qjobname


        
