"""
Module to select Ks sideband candidate events

"""

import os
import sys
import tools
import attr
import sel
from attr import modes
from yld import parse_args, create_bash_file
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

    for mode in modes:
        if opts.set and opts.set == 'interact':
            if tag == 'single':
                single_tag_mode(datatype, mode, label, opts.test)
            else:
                raise ValueError(tag)
            continue

        script, logfile, qjobname = create_script_logfile_jobname(
            datatype, tag, mode, label, opts)

        bash_file = create_bash_file(opts, datatype, label,
                                     script, 'kssideband.sh', 'sel')
        tools.qsub_jobs(logfile, qjobname, bash_file, opts.test)


def create_script_logfile_jobname(datatype, tag, mode, label, opts):
    logname = '%s_%s.log' %(datatype, mode)
    logpath = os.path.join(attr.sellogpath, label, 'kssideband')
    logfile = tools.set_file(extbase=logpath, comname=logname)

    content =  '''#!/usr/bin/env python

from sel import kssideband

kssideband.single_tag_mode("%s", "%s", "%s", test=%s)

'''% (datatype, mode, label, opts.test)

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

    file_ = os.path.join(attr.datpath, datatype, label, 'src', 'sel', filename)

    verbose = opts.verbose
    if opts.test:
        verbose = 1
    f = UserFile()
    f.data.append(content) 
    f.output(file_, verbose=verbose)
    os.chmod(file_, 0755)

    return filename, logfile, qjobname


def single_tag_mode(datatype, mode, label, test=False):
    sys.stdout.write('dhad.sel.kssideband: Processing Mode %s...' % mode)
    sys.stdout.flush()

    datpath = attr.datpath
    rootfile = tools.get_rootfile(datatype, mode, label)
    if test:
        sys.stdout.write('rootfile: %s \n' % rootfile)
    pt = tools.add_rootfile(rootfile)
    selname = '%s_%s.evt' %(datatype, mode)
    if test:
        selname += '.test'

    selpath = os.path.join(attr.datpath, 'evt', label, 'kssideband')
    selfile = tools.check_and_join(selpath, selname)

    nselected, ntotal = output_kssideband(pt, mode, selfile, label, test)
    sys.stdout.write(' selected %s out of %s.\n' % (nselected, ntotal))
    sys.stdout.flush()


def output_kssideband(pt, mode, selfile, label, test=False):
    ntotal = 0
    nselected = 0
    mode_key, sign = tools.get_modekey_sign(mode)
    opt = 'kssideband'
    if '/srs' in label:
        opt += '_srs'
    fo = open(selfile , 'w')
    for pte in pt:
        ntotal += 1
        if test and nselected >= 30:
            break 
        if pte.ecm < 3.7:
            continue
        if sign != None: # single tag
            d = tools.cuts.chooseD(mode_key, pte, sign, opt=opt)
            if d != None:
                mbc = pte.dmbc[d]
                if mbc > 1.83 and mbc < 1.89: 
                    fo.write('%.5f %.5f %d\n' % (mbc, pte.ecm/2, pte.dcsign[d]))
                    nselected = nselected + 1
                    
        else: # double tag
            raise "Not ready!"

    fo.close()
    sys.stdout.write('Saved as %s \n' %selfile)
    pt.Delete()

    return nselected, ntotal


