"""
Module for Cross Feed Study

"""

import os
import sys
import tools
import attr
import ROOT

from attr.modes import modes
from tools.filetools import UserFile
from fit import create_bash_file, load_roofit_lib
from tools import DHadTable, pair_to_str


__author__ = "Xin Shi <xs32@cornell.edu>"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2005-2011 Xin Shi"
__license__ = "GPL"
__revision__ = "$Revision$"


def main(opts, args):
    dt_type = args[0]
    stage = args[1] 
    label = args[2]

    single_modes = get_single_modes(opts.set)
        
    if stage == 'diag':
        for mode, sign in single_modes:
            if opts.set and 'interact' in opts.set:
                stage_diag(dt_type, label, mode, sign, interact=True)
            else:
                submit_batch_job(opts, dt_type, stage, label, mode, sign)

    elif stage == 'nondiag':
        for x, y  in [(x, y) for x in single_modes for y in single_modes if x!=y]:
            if opts.set and 'interact' in opts.set:
                stage_nondiag(dt_type, label, x, y, interact=True)
            else:
                submit_batch_job_nondiag(opts, dt_type, stage, label, x, y)
                
    else:
        raise NameError(stage)

    
def stage_diag(dt_type, label, mode, sign, interact=False):

    if label != '281ipbv0.2':
        load_roofit_lib(dt_type, label)

    ROOT.gROOT.SetBatch(1)
    ROOT.gROOT.SetStyle("Plain")

    sys.stdout.write('Stage 0: Do fits for diagonal. Mode: (%s, %s) \n' %(mode, sign))

    prefix='dir_'+label+'/crossfeeds'

    if sign == 1:
        uname = modes[mode]['uname']
        fname = modes[mode]['fname']
    else:
        uname = modes[mode]['unamebar']
        fname = modes[mode]['fnamebar']

    title  = '%s correct reco' % uname

    bkgname = ('%s_Single_%s_fakes_Single_%s.evt' %(dt_type, fname, fname))
    bkgfile = get_bkgfile(bkgname, label)

    epsname = '%s_Single_%s_fakes_Single_%s.eps' % (dt_type, fname, fname)
    epsfile  = tools.set_file(extbase=attr.figpath, prefix=prefix, comname=epsname)
    
    txtname = '%s_Single_%s_fakes_Single_%s.txt' % (dt_type, fname, fname)
    txtfile  = tools.set_file(extbase=attr.fitpath, prefix=prefix, comname=txtname)

    par_str = '("%s", "%s", "%s", "%s")'
    par_tuple = (title, bkgfile, epsfile, txtfile)
    par = par_str % par_tuple
    
    source = 'crossfeeds.C'
    #if interact:
    source = os.path.join(attr.srcfitpath, source)
        
    tools.print_sep()
    sys.stdout.write('       ROOT macro: %s \n' % source)
    tools.print_sep()

    ROOT.gROOT.Macro(source + par)
    tools.eps2png(epsfile)
    tools.eps2pdf(epsfile)

def stage_nondiag(dt_type, label, x, y, interact=False):
    if label != '281ipbv0.2':
        load_roofit_lib(dt_type, label)

    ROOT.gROOT.SetBatch(1)
    ROOT.gROOT.SetStyle("Plain")

    # STAGE 1: fit for non-diagonal
    sys.stdout.write('Stage 1: fit non-diagonal.\n')

    single_modes = [(pair, sign) for pair in modes for sign in [-1, 1]]

    prefix='dir_'+label+'/crossfeeds'
    
    #for x, y  in [(x, y) for x in single_modes for y in single_modes if x!=y]:
    if x[1] == 1:
        uname = modes[x[0]]['uname']
        fname = modes[x[0]]['fname']
    else:
        uname = modes[x[0]]['unamebar']
        fname = modes[x[0]]['fnamebar']
    if y[1] == 1:
        unameb = modes[y[0]]['uname']
        fnameb = modes[y[0]]['fname']
    else:
        unameb = modes[y[0]]['unamebar']
        fnameb = modes[y[0]]['fnamebar']

    title  = '%s fakes %s' % (uname, unameb)

    bkgname = ('%s_Single_%s_fakes_Single_%s.evt' %(dt_type, fname, fnameb))
    bkgfile = get_bkgfile(bkgname, label)

    epsname = '%s_Single_%s_fakes_Single_%s.eps' % (dt_type, fname, fnameb)
    epsfile  = tools.set_file(extbase=attr.figpath, prefix=prefix, comname=epsname)
    
    txtname = '%s_Single_%s_fakes_Single_%s.txt' % (dt_type, fname, fnameb)
    txtfile  = tools.set_file(extbase=attr.fitpath, prefix=prefix, comname=txtname)
    
    alpha, mass, n, sigma = get_paras(dt_type, label, fnameb)
    
    par_str = '("%s", "%s", "%s", "%s", %s, %s, %s, %s)'
    par_tuple = (title, bkgfile, epsfile, txtfile, alpha, mass, n, sigma)
    par = par_str % par_tuple
    
    source = 'crossfeeds_nondiag.C'
    #if interact:
    source = os.path.join(attr.srcfitpath, source)

    tools.print_sep()
    sys.stdout.write('       ROOT macro: %s \n' % source)
    tools.print_sep()
    ROOT.gROOT.Macro(source + par)
    
    tools.eps2png(epsfile)
    tools.eps2pdf(epsfile)

       

def run_example():
    source = '/home/xs32/local/share/root/tutorials/roofit/rf205_compplot.C'
    ROOT.gROOT.Macro(source)


def create_python_script(opts, dt_type, stage, label, mode, sign):
    if stage not in ['diag'] :
        raise NameError(stage)

    content =  '''#!/usr/bin/env python

from fit import crossfeeds

crossfeeds.stage_%s("%s", "%s", %s, %s)

'''% (stage, dt_type, label, mode, sign)


    filename = 'crossfeeds-%s-%s-%s-%s.py' % (stage, dt_type, mode, sign)
    
    file_ = os.path.join(attr.datpath, dt_type, label, 'src', 'csf', filename)

    verbose = opts.verbose
    if opts.test:
        verbose = 1 
    f = UserFile()
    f.append(content) 
    f.output(file_, verbose=verbose)
    os.chmod(file_, 0755)
    return filename

def create_python_script_nondiag(opts, dt_type, stage, label, x, y):
    if stage not in ['nondiag'] :
        raise NameError(stage)

    content =  '''#!/usr/bin/env python

from fit import crossfeeds

crossfeeds.stage_%s("%s", "%s", %s, %s)

'''% (stage, dt_type, label, x, y)

    xstr = pair_to_str(x)
    ystr = pair_to_str(y)
    
    filename = 'crossfeeds-%s-%s-%s-%s.py' % (stage, dt_type, xstr, ystr)
    file_ = os.path.join(attr.datpath, dt_type, label, 'src', 'csf', filename)

    verbose = opts.verbose
    if opts.test:
        verbose = 1 
    
    f = UserFile()
    f.append(content) 
    f.output(file_, verbose=verbose)
    os.chmod(file_, 0755)
    return filename


def get_paras(dt_type, label, fname):

    prefix='dir_'+label+'/crossfeeds'
        
    tabname = '%s_Single_%s_fakes_Single_%s.txt' % (dt_type, fname, fname)
    tabfile = tools.set_file(extbase=attr.fitpath, prefix=prefix, comname=tabname)

    tab = DHadTable(tabfile)
    mass = tab.cell_get('mass', 'Value')
    sigma = tab.cell_get('sigma', 'Value')
    n = tab.cell_get('n', 'Value')
    alpha = tab.cell_get('alpha', 'Value')

    return  alpha, mass, n, sigma

def get_single_modes(setting):
    
    modeskeys = modes.keys()
    signs = [-1, 1]

    if setting and 'mode' in setting:
        mode = setting.split('mode=')[1].split(':')[0]
        modeskeys = map(int, mode.split(','))
    if setting and 'sign' in setting:
        sign = setting.split('sign=')[1].split(':')[0]
        signs = [int(sign)]
        
    single_modes = [(pair, sign) for pair in modeskeys for sign in signs]

    return single_modes


def submit_batch_job(opts, dt_type, stage, label, mode, sign):

    script = create_python_script(opts, dt_type, stage, label, mode, sign)
    bash_file = create_bash_file(opts, label, dt_type, script,
                                 'fit-crossfeeds-%s.sh' %stage, subdir='csf')

    logfile = tools.set_file(extbase=attr.logpath,
                             prefix='dir_'+label+'/crossfeeds',
                             comname='stage_%s_%s_%s.txt' %(stage, mode, sign))

    qjobname = '%s%s%s' % (stage, mode, sign)
    tools.qsub_jobs(logfile, qjobname, bash_file, opts.test)

    
def submit_batch_job_nondiag(opts, dt_type, stage, label, x, y):
    script = create_python_script_nondiag(opts, dt_type, stage, label, x, y)
    bash_file = create_bash_file(opts, label, dt_type, script,
                                 'fit-crossfeeds-%s.sh' %stage, subdir='csf')

    xstr = pair_to_str(x)
    ystr = pair_to_str(y)

    logfile = tools.set_file(extbase=attr.logpath,
                             prefix='dir_'+label+'/crossfeeds',
                             comname='stage_%s_%s_%s.txt' %(stage, xstr, ystr))

    qjobname = 'x%s%s' % (xstr, ystr)
    tools.qsub_jobs(logfile, qjobname, bash_file, opts.test)
    

def get_bkgfile(bkgname, label):
    bkgpath = os.path.join(attr.bkgpath, label)
    bkgfile = tools.check_and_join(bkgpath, bkgname)
    if not os.access(bkgfile, os.F_OK):
        if '818ipb' in label:
            bkgfile_281ipb = bkgfile.replace('818ipb', '281ipb')
            bkgfile_537ipb = bkgfile.replace('818ipb', '537ipb')
            tools.combine_files(bkgfile_281ipb, bkgfile_537ipb, bkgfile)
        else:
            raise ValueError(bkgfile)

    return bkgfile
    
