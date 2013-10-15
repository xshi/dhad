"""
Module for selected variables study

"""

import os
import sys
import tools
import attr
import sel
from attr import modes
from tools.filetools import UserFile 
from yld import parse_args, create_bash_file
from tools import count_mcdmodes, output_modedict
from tools.cuts import chooseD, invmass


__author__ = "Xin Shi <xs32@cornell.edu>"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2005-2011 Xin Shi"
__license__ = "GPL"
__revision__ = "$Revision$"


def main(opts, args):
    var = args[0]
    parsed = parse_args(args[1:])
    datatype  = parsed[0]
    tag       = parsed[1]
    modes     = parsed[2]
    label     = parsed[3]

    for mode in modes:
        if opts.set and opts.set == 'interact':
            if tag == 'single':
                single_tag_mode(var, datatype, mode, label, opts.test)
            else:
                raise ValueError(tag)
            continue

        script, logfile, qjobname = create_script_logfile_jobname(
            var, datatype, tag, mode, label, opts)

        bash_file = create_bash_file(opts, datatype, label, script,
                                     'sel_var.sh', 'sel')
        tools.qsub_jobs(logfile, qjobname, bash_file, opts.test)


def single_tag_mode(var, datatype, mode, label, test=False):
    sys.stdout.write('dhad.sel.var(%s): Processing Mode %s...' %(var,mode))
    sys.stdout.flush()

    datpath = attr.datpath
    rootfile = tools.get_rootfile(datatype, mode, label)
    pt = tools.add_rootfile(rootfile)

    evtfile = get_evtfile(datatype, mode, label, var, test=test)
    if var == 'pi0mass':
        nselected, ntotal = output_var_pi0mass(pt, mode, evtfile, label, test)
    elif var == 'mctruth':
        nselected, ntotal = output_var_mctruth(pt, mode, evtfile, label, test)
    elif var == 'mass_kk':
        nselected, ntotal = output_var_mass_kk(pt, mode, evtfile, label, test)
    else:
        raise NameError(var)
    
    sys.stdout.write(' selected %s out of %s.\n' % (nselected, ntotal))
    sys.stdout.write('Saved as %s \n' %evtfile)
    sys.stdout.flush()


def output_var_pi0mass(pt, mode, evtfile, label, test=False):
    nselected = 0 
    ntotal = 0 
    modekey, sign = tools.get_modekey_sign(mode)
    alt_deltae = None
    opt = ''
    if '/desideband' in label:
        side = label.split('/desideband_')[1]
        alt_deltae = attr.desideband(modekey, side)

    fo = open(evtfile , 'w')
    for pte in pt:
        if test and nselected > 10:
            break

        ntotal += 1
        if sign != None: # single tag 
            d = chooseD(modekey, pte, sign,
                        alt_deltae=alt_deltae, opt=opt)
            if d != None:
                nselected += 1
                if modekey == 1 or modekey == 203:
                    npi0 = pte.ddau3[d]
                if modekey == 201:
                    npi0 = pte.ddau4[d]

                pi0mass = pte.pi0mass[npi0]
                fo.write('%s\n' % pi0mass)
        else: # double tag 
            raise NameError
    fo.close()
    return nselected, ntotal


def output_var_mctruth(pt, mode, evtfile, label, test=False):
    nselected = 0 
    ntotal = 0 
    modekey, sign = tools.get_modekey_sign(mode)
    alt_deltae = None
    opt = ''
    if '/desideband' in label:
        side = label.split('/desideband_')[1]
        alt_deltae = attr.desideband(modekey, side)

    if '/kssideband' in label:
        opt = 'kssideband'
        
    modedict = {}
    for pte in pt:
        if test and nselected > 10:
            break

        ntotal += 1
        if sign != None: # single tag 
            d = chooseD(modekey, pte, sign,
                        alt_deltae=alt_deltae, opt=opt)
            if d != None:
                nselected += 1
                count_mcdmodes(modedict, pte.mcdmode, pte.mcdbmode)

        else: # double tag 
            raise NameError

    pt.Delete()
    output_modedict(modedict, evtfile)
    return nselected, ntotal

def output_var_mass_kk(pt, mode, evtfile, label, test=False):
    nselected = 0 
    ntotal = 0 
    modekey, sign = tools.get_modekey_sign(mode)
    alt_deltae = None
    opt = ''

    modedict = {}
    fo = open(evtfile , 'w')
    for pte in pt:
        if test and nselected > 10:
            break

        ntotal += 1
        if sign == None:
            raise ValueError(sign)
        
        d = chooseD(modekey, pte, sign,
                    alt_deltae=alt_deltae, opt=opt)
        if d != None:
            nselected += 1
            kaons = [pte.ddau1[d], pte.ddau2[d]]
            
            fourvecs = []
            for index in kaons:
                fourvecs.append([pte.trke[index], pte.trkpy[index],
                                 pte.trkpy[index], pte.trkpz[index]])

            kkmass = invmass(fourvecs[0], fourvecs[1])
            fo.write('%s\n' % kkmass)

    fo.close()
    pt.Delete()
    return nselected, ntotal


def create_script_logfile_jobname(var, datatype, tag, mode, label, opts):
    logname = '%s_%s.log' %(datatype, mode)
    logpath = os.path.join(attr.sellogpath, label, 'var', var)
    logfile = tools.set_file(extbase=logpath, comname=logname)

    content =  '''#!/usr/bin/env python

from sel import var

var.single_tag_mode("%s", "%s", "%s", "%s", test=%s)

'''% (var, datatype, mode, label, opts.test)

    mode, sign = tools.get_modekey_sign(mode)

    if tag == 'single':
        if sign == 1:
            sign = 'p'
        else: 
            sign = 'm'
        filename = 'sel-%s-%s-m%s-%s-%s.py' % (datatype, tag, mode, sign, label)
        qjobname = 'sel%s,%s' % (mode, sign)
    else:
        filename = 'sel-%s-%s-m%s-%s-%s.py' % (datatype, tag, mode[0], mode[1], label)
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


def get_evtfile(datatype, mode, label, var, test=False):
    evtname = '%s_%s.evt' %(datatype, mode)
    if test:
        evtname += '.test'
        
    evtpath = os.path.join(attr.datpath, 'evt', label, 'var', var)
    evtfile = tools.check_and_join(evtpath, evtname)
    return evtfile


