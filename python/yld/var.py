"""
Module for selected variables study

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

    var = args[0]
    parsed = yld.parse_args(args[1:])

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
            var, datatype, tag, mode, label, opts.test)

        bash_file = yld.create_bash_file(script, 'get_var.sh')
        tools.qsub_jobs(logfile, qjobname, bash_file, opts.test)


def single_tag_mode(var, datatype, mode, label, test=False):
    sys.stdout.write('dhad.yld.var(%s): Processing Mode %s...' %(var,mode))
    sys.stdout.flush()

    datpath = attr.datpath
    rootfile = tools.get_rootfile(datatype, mode, label)
    pt = tools.add_rootfile(rootfile)

    evtname = '%s_%s.evt' %(datatype, mode)
    evtpath = os.path.join(datpath, 'evt', label, 'var', var)
    evtfile = tools.check_and_join(evtpath, evtname)

    if var == 'deltae':
        nselected, ntotal = output_var_deltae(pt, mode, evtfile, label, test)
    else:
        raise NameError(var)
    
    sys.stdout.write(' selected %s out of %s.\n' % (nselected, ntotal))
    sys.stdout.flush()


def output_var_deltae(pt, mode, evtfile, label, test=False):
    nselected = 0 
    ntotal = 0 
    modekey, sign = tools.get_modekey_sign(mode)
    alt_deltae = {'decutl': -1, 'decuth': 1}
    fo = open(evtfile , 'w')
    for pte in pt:
        ntotal += 1
        if sign != None: # single tag 
            d = tools.cuts.chooseD(modekey, pte, sign, alt_deltae=alt_deltae)
            if d != None:
                nselected = nselected + 1
                fo.write('%s\n' % pte.ddeltae[d])
        else: # double tag 
            raise NameError
            
        if test and nselected > 10:
            break
    fo.close()
    return nselected, ntotal


def create_script_logfile_jobname(var, datatype, tag, mode, label, test):
    logname = '%s_%s.log' %(datatype, mode)
    logpath = os.path.join(attr.yldlogpath, label, 'var', var)
    logfile = tools.set_file(extbase=logpath, comname=logname)

    content =  '''#!/usr/bin/env python

from yld import var

var.single_tag_mode("%s", "%s", "%s", "%s", test=%s)

'''% (var, datatype, mode, label, test)

    mode, sign = tools.get_modekey_sign(mode)

    if tag == 'single':
        if sign == 1:
            sign = 'p'
        else:
            sign = 'm'
        filename = 'var-%s-%s-m%s-%s-%s.py' % (datatype, tag, mode, sign, label)
        qjobname = 'var%s,%s' % (mode, sign)
    else:
        filename = 'var-%s-%s-m%s-%s-%s.py' % (datatype, tag, mode[0], mode[1], label)
        qjobname = 'var%s,%s' % (mode[0], mode[1])

    file_ = os.path.join(attr.base, 'src', attr.src, 'yld', filename)

    f = UserFile()
    f.data.append(content) 
    f.output(file_)
    os.chmod(file_, 0755)

    return filename, logfile, qjobname

