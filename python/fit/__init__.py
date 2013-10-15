"""
Module for Fitting 

"""

import os
import sys
import ROOT
import attr
import tools
from tools import DHadTable, combine_files, get_modekey, \
     parse_args, create_bash_file_pyline
from tools.filetools import UserFile


__author__ = "Xin Shi <xs32@cornell.edu>"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2005-2011 Xin Shi"
__license__ = "GPL"
__revision__ = "$Revision$"


def main(opts, args):
    if args[0] == 'crossfeeds':
        import crossfeeds
        crossfeeds.main(opts, args[1:])
        return

    if args[0] == 'backgrounds':
        import backgrounds
        backgrounds.main(opts, args[1:])
        return

    if args[0] == 'sidebands':
        import sidebands
        sidebands.main(opts, args[1:])
        return

    if args[0] == 'kkmass':
        import kkmass
        kkmass.main(opts, args[1:])
        return
    
    if args[0] == 'kkmass2':
        import kkmass2
        kkmass2.main(opts, args[1:])
        return

    if args[0] == 'kpimass':
        import kpimass
        kpimass.main(opts, args[1:])
        return
    
    ROOT.gROOT.SetBatch(1)
    ROOT.gROOT.SetStyle("Plain")

    parsed = parse_args(args)
    dt_type = parsed[0]
    tag  = parsed[1]
    modes = parsed[2]
    label = parsed[3]

    if modes == ['double_all_d0s']:
        mode = modes[0]
        if opts.set and opts.set == 'interact':
            double_all_d0s(dt_type, mode, label, test=opts.test)
        else:
            pyline = 'import fit; fit.%s("%s", "%s", "%s", test=%s)'% (
                mode, dt_type, mode, label, opts.test)
        
            bash_file_name = 'fit-mbc.sh' 
            bash_file = create_bash_file_pyline(opts, label, dt_type, pyline,
                                                bash_file_name)
            logfile = tools.set_file('txt', dt_type, mode, tag,
                                     prefix='dir_'+label, extbase=attr.logpath)
            qjobname = 'fitd0s'
            tools.qsub_jobs(logfile, qjobname, bash_file, opts.test)

        return

    if modes == ['double_all_dps']:
        mode = modes[0]
        if opts.set and opts.set == 'interact':
            double_all_dps(dt_type, mode, label, test=opts.test)
        else:
            pyline = 'import fit; fit.%s("%s", "%s", "%s", test=%s)'% (
                mode, dt_type, mode, label, opts.test)
        
            bash_file_name = 'fit-mbc.sh' 
            bash_file = create_bash_file_pyline(opts, label, dt_type, pyline,
                                                bash_file_name)
            logfile = tools.set_file('txt', dt_type, mode, tag,
                                     prefix='dir_'+label, extbase=attr.logpath)
            qjobname = 'fitdps'
            tools.qsub_jobs(logfile, qjobname, bash_file, opts.test)

        return


    for mode in modes:
        if opts.set and opts.set == 'interact':

            if tag == 'single':
                single_tag_mode(dt_type, mode, label, interact=True,
                                test=opts.test)
            elif tag == 'double':
                double_tag_mode(dt_type, mode, label, interact=True,
                                test=opts.test)
            else:
                raise ValueError(tag)
            continue

        else:
            submit_batch_job(dt_type, tag, mode, label, opts)

        # script = create_python_script(opts, dt_type, tag, mode, label)
        # bash_file = create_bash_file(opts, label, dt_type, script)
        # logfile = tools.set_file('txt', dt_type, mode, tag,
        #                          prefix='dir_'+label, extbase=attr.logpath)
        # if tag == 'single':
        #     qjobname = 'fit-m%s' % mode
        # else:
        #     qjobname = 'fit%s,%s' % (mode[0], mode[1])
        # tools.qsub_jobs(logfile, qjobname, bash_file, opts.test)


def submit_batch_job(datatype, tag, mode, label, opts):
    mode_sign = tools.get_modekey_sign(mode)
    if mode_sign[1] == None:
        ms = '%s_%s' %(mode_sign[0])
    else:
        ms = tools.pair_to_str(mode_sign)

    pyline = 'import fit; fit.%s_tag_mode("%s", "%s", "%s", test=%s)'% (
        tag, datatype, mode, label, opts.test)

    bash_file_name = 'fit-mbc.sh' 
    bash_file = create_bash_file_pyline(opts, label, datatype, pyline,
                                        bash_file_name)
    #logname = '%s_%s.txt' %(datatype.replace('/', '_'), mode)
    #logpath = os.path.join(attr.logpath, label)#, 'yld')
    #logfile = tools.set_file(extbase=logpath, comname=logname)
    logfile = tools.set_file('txt', datatype, mode_sign[0], tag,
                             prefix='dir_'+label, extbase=attr.logpath)
    qjobname = 'fit%s' % ms
    tools.qsub_jobs(logfile, qjobname, bash_file, opts.test)


def single_tag_mode(dt_type, mode, label, interact=False, test=False):
    mode = get_modekey(mode)
    tag = 'single'
    prefix = 'dir_' + label
    evtprefix = get_evtprefix(dt_type, label)
    Gamma, Mres, R, mc = get_common_parameters(dt_type, label)
    Sigma, Fa, Fb, Sa, Sb = get_resolution_paras(mode, label)
    N1, N2, Nbkgd1, Nbkgd2, md, p, sigmap1, xi = init_paras_single(
        label, dt_type, tag, mode)
    # ------------------- Parameters for the fit ----------
    title1 = attr.modes[mode]['uname']
    title2 = attr.modes[mode]['unamebar']
    num_fcn  = 3  # : 0 for only background
    xi_side  = 0.0
    p_side   = 0.0
    int_d    = 1
    optstr   = 'p'  # To plot,  f : fast, w: fixwidth
    floatwidth = 0 
    Min      = 0.5
    options  = ""
    MINUIT   = "ermh4"
    # -------------------------------------------------

    if '/p/0.5' in label:
        p_side = 0.5

    if '/argus' in label:
        options = 'fix_xi,fix_p'
        xi, p = get_argus_paras_single(label, dt_type, tag, mode)

    if '/fix_sigmap1' in label:
        options = 'fix_sigmap1'
        if '/kssideband' in label:
            sys.stdout.write('Fixing the sigmap1 as %s ...\n' %Sigma)
            sigmap1 = Sigma 

    if '/fix_n1n2' in label and '/desideband' in label:
        options = 'fix_n1n2'
        N1 = 1
        N2 = 1
        
    if dt_type == 'signal' and mode in [0, 200, 202]:
        p_side = 0.5
        tools.print_sep()

    forceCombine = 1
    epsfile =  tools.set_file('eps', dt_type, mode, tag,
                              prefix=prefix, extbase=attr.figpath)
    fitpath = attr.fitpath 
    outfile =  tools.set_file('txt', dt_type, mode, tag,
                              prefix=prefix, extbase=fitpath)
    evtpath = attr.evtpath
    evtfile =  tools.set_file('evt', dt_type, mode, tag, prefix=evtprefix,
                              forceCombine=forceCombine, extbase=evtpath)
    tools.print_sep()
    par_str = '( "%s", "%s", "%s", "%s", "%s", %d, %d, %f, %f, %f, %f, \
    %f, %f, %f, %d, "%s", %f, %d, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, \
    %f, "%s", "%s" )'
    par_tuple = (title1, title2, evtfile, epsfile, outfile, mc, num_fcn,
                 xi_side, p_side, Sigma, Sa, Sb, Fa, Fb, int_d, optstr,
                 Gamma, floatwidth, R, Mres, N1, N2, Nbkgd1, Nbkgd2, md,
                 p, sigmap1, xi, Min, options, MINUIT)
    par = par_str % par_tuple
    print_paras(par_tuple)
    load_roofit_lib(dt_type, label)
    sourcename = 'mbc_singletag_3s.C'
    #if interact:
    source = os.path.join(attr.srcfitpath, sourcename)
    tools.print_sep()
    sys.stdout.write('       ROOT macro: %s \n' % source)
    tools.print_sep()
    if test:
        return
    ROOT.gROOT.Macro( source + par)

    if test:
        evtfile = evtfile + '.test'
        epsfile = epsfile + '.test'
        outfile = outfile + '.test'

    # fit_mbc_single(title1, title2, evtfile, epsfile, outfile, mc, num_fcn,
    #                xi_side, p_side, Sigma, Sa, Sb, Fa, Fb, int_d, optstr,
    #                Gamma, floatwidth, R, Mres, N1, N2, Nbkgd1, Nbkgd2, md,
    #                p, sigmap1, xi, Min, options, MINUIT)

    sys.stdout.write('Save output in %s\n'  % outfile)
    if not test:
        tools.eps2png(epsfile)
        tools.eps2pdf(epsfile)


def get_common_parameters(dt_type, label):
    Gamma = 0.0252
    Mres  = 3.7724
    R = 12.7

    if '818ipbv13' in label: 
        Mres = 3.7722
        sys.stdout.write('Using the new fitting paras M = %s GeV.\n' % Mres)        
    if label in ['537ipbv0', '281ipbv10', '281ipbv11']:
        sys.stdout.write('Using the original fitting paras.\n')
        Gamma = 0.0286
        Mres  = 3.7718
        R = 12.3

    if '/gamma/' in label:
        Gamma = float(label.split('/gamma/')[-1])

    if '/mass/' in label:
        Mres = float(label.split('/mass/')[-1])

    if '/r/' in label:
        R = float(label.split('/r/')[-1])

    if dt_type == 'signal' or dt_type == 'generic':
        mc = 1 # MARK III
    elif dt_type == 'data':
        mc = 3 # Using the BES2006 lineshape
    else:
        raise ValueError(dt_type)
    return Gamma, Mres, R, mc


def get_resolution_paras(mode, label):
    if 'resolution' in label:
        Sigma = 0.005
        Fa = 0.05
        Fb = 0.05
        Sa = 2.0
        Sb = 2.0

    else:
        tab_name='para_momentum_resolution'
        short_label = label.split('/')[0] 
        if short_label in ['281ipbv0', '281ipbv12', '537ipbv12',
                           '818ipbv12', '818ipbv13']:
            tab_name = '%s/%s' % (short_label, tab_name)
        else:
            raise NameError(label)

        tab_prefix = ''
        tab_opt_sigma  = 'value'
        tab_opt_fa     = 'value'
        tab_opt_fb     = 'value'
        tab_opt_sa     = 'value'
        tab_opt_sb     = 'value'

        tabfile = tools.set_file(
            extbase=attr.tabpath, prefix=tab_prefix, 
            comname=tab_name, ext='txt')
        sys.stdout.write('Loading lineshape parameters from %s... \n' %tabfile)
        tab = DHadTable(tabfile)
        line_no = attr.mode_line_dict[mode]
        Sigma = float(tab.cell_get(line_no, 'sigma (MeV)',tab_opt_sigma))/1000
        Fa    = float(tab.cell_get(line_no, 'fa', tab_opt_fa))
        Fb    = float(tab.cell_get(line_no, 'fb', tab_opt_fb))
        Sa    = float(tab.cell_get(line_no, 'sa', tab_opt_sa))
        Sb    = float(tab.cell_get(line_no, 'sb', tab_opt_sb))
        
    return Sigma, Fa, Fb, Sa, Sb


def init_paras_single(label, dt_type, tag, mode):

    if '281ipb' in label:
        init_para_prefix = 'dir_281ipbv12'
    elif '537ipb' in label:
        init_para_prefix = 'dir_537ipbv12'
    elif '818ipb' in label:
        init_para_prefix = 'dir_818ipbv12'
    else:
        raise ValueError(label)

    init_para_base = attr.fitpath

    if dt_type == 'generic':
        if label in ['281ipbv7', '537ipbv7', '818ipbv7']:
            dt_type = 'signal'
    
    tabfile =  tools.set_file('txt', dt_type, mode, tag,
                              prefix=init_para_prefix,
                              extbase=init_para_base)

    sys.stdout.write('Loading init paras from %s ... \n' %tabfile)
    tab     = DHadTable(tabfile)
    
    N1      = float(tab.cell_get('N1', 'Value'))
    N2      = float(tab.cell_get('N2', 'Value'))
    Nbkgd1  = float(tab.cell_get('Nbkgd1', 'Value'))
    Nbkgd2  = float(tab.cell_get('Nbkgd2', 'Value'))
    md      = float(tab.cell_get('md', 'Value'))
    p       = float(tab.cell_get('p', 'Value'))
    sigmap1 = float(tab.cell_get('sigmap1', 'Value'))
    xi      = float(tab.cell_get('xi', 'Value'))

    return N1, N2, Nbkgd1, Nbkgd2, md, p, sigmap1, xi


def create_bash_file(opts, label, dt_type, script,
                     bashname='fit-mbc.sh', optcommand='',
                     subdir=''):
    script_dir =  os.path.join(attr.datpath, dt_type, label, 'src', subdir)

    bash_content =  '''#!/bin/sh
#$ -S /usr/local/bin/bash
#$ -j y
#$ -m a
#$ -M xs32@cornell.edu

date
hostname

.  ~/.bashrc
setdhad %s 

%s

cd %s
./%s

date

''' % (attr.version, optcommand, script_dir, script)
    
    bash_file = os.path.join(script_dir, bashname)

    verbose = opts.verbose
    if opts.test:
        verbose = 1
    f = UserFile()
    f.append(bash_content) 
    f.output(bash_file, verbose=verbose)
    os.chmod(bash_file, 0755)
    return bash_file


def create_python_script(opts, dt_type, tag, mode, label):

    if tag not in ['single', 'double'] :
        raise NameError(tag)

    content =  '''#!/usr/bin/env python

import fit

fit.%s_tag_mode("%s", %s, "%s")

'''% (tag, dt_type, mode, label)

    if tag == 'single':
        filename = '%s-%s-m%s-%s.py' % (dt_type, tag, mode, label)
    else:
        filename = '%s-%s-m%s-%s-%s.py' % (
            dt_type, tag, mode[0], mode[1], label)
    
    file_ = os.path.join(attr.datpath, dt_type, label, 'src', filename)

    verbose = opts.verbose
    if opts.test:
        verbose = 1
    f = UserFile()
    f.append(content) 
    f.output(file_, verbose=verbose)
    os.chmod(file_, 0755)
    return filename


def print_paras(paras):

    sys.stdout.write( '  title1  = %s\n'     %paras[0])
    sys.stdout.write( '  title2  = %s\n'     %paras[1])
    sys.stdout.write( '  evtfile = %s\n'     %paras[2])
    sys.stdout.write( '  epsfile = %s\n'     %paras[3])
    sys.stdout.write( '  outfile = %s\n'     %paras[4])
    sys.stdout.write( '  mc      = %s\n'     %paras[5])
    sys.stdout.write( '  num_fcn = %s\n'     %paras[6])
    sys.stdout.write( '  xi_side = %s\n'     %paras[7])
    sys.stdout.write( '  p_side  = %s\n'     %paras[8])
    sys.stdout.write( '  Sigma   = %s\n'     %paras[9])
    sys.stdout.write( '  Sa      = %s\n'     %paras[10])
    sys.stdout.write( '  Sb      = %s\n'     %paras[11])
    sys.stdout.write( '  Fa      = %s\n'     %paras[12])
    sys.stdout.write( '  Fb      = %s\n'     %paras[13])
    sys.stdout.write( '  int_d   = %s\n'     %paras[14])
    sys.stdout.write( '  optstr  = %s\n'     %paras[15])
    sys.stdout.write( '  Gamma   = %s\n'     %paras[16])
    sys.stdout.write( '  floatwidth = %s\n'  %paras[17])
    sys.stdout.write( '  R       = %s\n'     %paras[18])
    sys.stdout.write( '  Mres    = %s\n'     %paras[19]) 
    tools.print_sep()

    sys.stdout.write( '  N1      = %s\n'     %paras[20])
    sys.stdout.write( '  N2      = %s\n'     %paras[21])
    sys.stdout.write( '  Nbkgd1  = %s\n'     %paras[22])
    sys.stdout.write( '  Nbkgd2  = %s\n'     %paras[23])
    sys.stdout.write( '  md      = %s\n'     %paras[24])
    sys.stdout.write( '  p       = %s\n'     %paras[25])
    sys.stdout.write( '  sigmap1 = %s\n'     %paras[26])
    sys.stdout.write( '  xi      = %s\n'     %paras[27])   
    tools.print_sep()

    sys.stdout.write( '  Min     = %s\n'     %paras[28])
    sys.stdout.write( '  options = %s\n'     %paras[29])
    sys.stdout.write( '  MINUIT  = %s\n'     %paras[30]) 

    
def load_roofit_lib(dt_type, label=None):
    libbase  =  os.path.join(attr.base, 'lib')
    libcorename = 'libRooFitCore_3_0.so'
    libmodelsname = 'libRooFitModels_3_0.so'

    if dt_type == 'signal' or dt_type == 'generic':
        libmodelsname = 'libRooFitModels_3_0_12.so'

    if label == '281ipbv0':
        libmodelsname = 'libRooFitModels_3_0.so'
        
    libRooFitCore = os.path.join(libbase, 'RooFitCore', libcorename)
    libRooFitModels = os.path.join(libbase, 'RooFitModels', libmodelsname)
    libs = ["libHtml.so", "libMinuit.so", libRooFitCore, libRooFitModels] 
    for li in libs:
        sys.stdout.write('Loading %s ...\n' %li)
        if ROOT.gSystem.Load(li) < 0:
            raise NameError(li)
            

def double_all_d0s(dt_type, mode, label, test=False):
    tag = 'double'
    prefix = 'dir_'+label

    if label == '818ipbv12.1':
         label = '818ipbv12'
    evtprefix = get_evtprefix(dt_type, label)

    mode1 = 0
    mode2 = 0

    title1 = attr.modes[mode1]['uname']
    title2 = attr.modes[mode2]['unamebar']

    code1 = attr.interfacecodes[mode1]
    code2 = attr.interfacecodes[mode2]
    
    Gamma, Mres, R, mc = get_common_parameters(dt_type, label)

    Sigma1, F1a, F1b, S1a, S1b = get_resolution_paras(mode1, label)
    Sigma2, F2a, F2b, S2a, S2b = get_resolution_paras(mode2, label)

    opt, N, Nbkgd1, Nbkgd2, Nbkgd3, NbkgdFlat = get_double_paras(label)

    epsfile =  tools.set_file('eps', dt_type, mode, tag,
                              prefix=prefix, extbase=attr.figpath)
    fitpath = attr.fitpath 
    outfile =  tools.set_file('txt', dt_type, mode, tag,
                              prefix=prefix, extbase=fitpath)
    evtpath = attr.evtpath
    evtfile =  tools.set_file('evt', dt_type, mode, tag, prefix=evtprefix,
                              forceCombine=0, extbase=evtpath)

    
    if not os.access(evtfile, os.F_OK):
        forceCombine = 'all_d0s'  
        evtfile =  tools.set_file('evt', dt_type, mode, tag, prefix=evtprefix,
                                  forceCombine=forceCombine, extbase=evtpath)
    tools.print_sep()

    par_str = '("%s", %f, %f, %f, %f, %f, "%s", %f, %f, %f, \
    %f, %f, "%s", "%s", "%s", %d, "%s", "%s", "%s", %f,\
    %f, %f,  %f, %f, %f, %f, %f)'

    par_tuple = (code1, Sigma1, F1a, F1b, S1a, S1b,
                 code2, Sigma2, F2a, F2b, S2a, S2b,
                 evtfile, epsfile, outfile, mc, opt, title1, title2,
                 Gamma, Mres, R, N, Nbkgd1, Nbkgd2, Nbkgd3, NbkgdFlat)
    
    par = par_str % par_tuple
        
    print_paras_double(par_tuple)

    load_roofit_lib(dt_type, label)

    sourcename = 'lineshapefit2d.C'
    if prefix == 'dir_818ipbv12.1':
         sourcename = 'lineshapefit2d_1.C'

    #if interact:
    source = os.path.join(attr.srcfitpath, sourcename)
        
    tools.print_sep()
    sys.stdout.write('       ROOT macro: %s \n' % source)
    tools.print_sep()
    if test:
        return

    ROOT.gROOT.Macro( source + par)
    
    sys.stdout.write('Save output in %s\n'  % outfile)
    tools.eps2png(epsfile)
    tools.eps2pdf(epsfile)


def double_all_dps(dt_type, mode, label, test=False):
    tag = 'double'
    prefix = 'dir_'+label
    evtprefix = get_evtprefix(dt_type, label)

    if label == '818ipbv12.1':
         label = '818ipbv12'

    mode1 = 200
    mode2 = 200

    title1 = attr.modes[mode1]['uname']
    title2 = attr.modes[mode2]['unamebar']

    code1 = attr.interfacecodes[mode1]
    code2 = attr.interfacecodes[mode2]
    
    Gamma, Mres, R, mc = get_common_parameters(dt_type, label)

    Sigma1, F1a, F1b, S1a, S1b = get_resolution_paras(mode1, label)
    Sigma2, F2a, F2b, S2a, S2b = get_resolution_paras(mode2, label)

    opt, N, Nbkgd1, Nbkgd2, Nbkgd3, NbkgdFlat = get_double_paras(label)

    epsfile =  tools.set_file('eps', dt_type, mode, tag,
                              prefix=prefix, extbase=attr.figpath)
    fitpath = attr.fitpath 
    outfile =  tools.set_file('txt', dt_type, mode, tag,
                              prefix=prefix, extbase=fitpath)
    evtpath = attr.evtpath
    evtfile =  tools.set_file('evt', dt_type, mode, tag, prefix=evtprefix,
                              forceCombine=0, extbase=evtpath)

    
    if not os.access(evtfile, os.F_OK):
        forceCombine = 'all_dps'  
        evtfile =  tools.set_file('evt', dt_type, mode, tag, prefix=evtprefix,
                                  forceCombine=forceCombine, extbase=evtpath)
    tools.print_sep()

    par_str = '("%s", %f, %f, %f, %f, %f, "%s", %f, %f, %f, \
    %f, %f, "%s", "%s", "%s", %d, "%s", "%s", "%s", %f,\
    %f, %f,  %f, %f, %f, %f, %f)'

    par_tuple = (code1, Sigma1, F1a, F1b, S1a, S1b,
                 code2, Sigma2, F2a, F2b, S2a, S2b,
                 evtfile, epsfile, outfile, mc, opt, title1, title2,
                 Gamma, Mres, R, N, Nbkgd1, Nbkgd2, Nbkgd3, NbkgdFlat)
    
    par = par_str % par_tuple
        
    print_paras_double(par_tuple)

    load_roofit_lib(dt_type, label)

    sourcename = 'lineshapefit2d.C'
    if prefix == 'dir_818ipbv12.1':
         sourcename = 'lineshapefit2d_1.C'
    #if interact:
    source = os.path.join(attr.srcfitpath, sourcename)
        
    tools.print_sep()
    sys.stdout.write('       ROOT macro: %s \n' % source)
    tools.print_sep()
    if test:
        return

    ROOT.gROOT.Macro( source + par)
    
    sys.stdout.write('Save output in %s\n'  % outfile)
    tools.eps2png(epsfile)
    tools.eps2pdf(epsfile)


def double_tag_mode(dt_type, mode, label, interact=False, test=False):
    mode = get_modekey(mode)
    tag = 'double'
    prefix = 'dir_'+label
    evtprefix = get_evtprefix(dt_type, label)

    mode1 = mode[0]
    mode2 = mode[1]

    title1 = attr.modes[mode1]['uname']
    title2 = attr.modes[mode2]['unamebar']

    code1 = attr.interfacecodes[mode1]
    code2 = attr.interfacecodes[mode2]
    
    forceCombine = None # Different from single tag case

    Gamma, Mres, R, mc = get_common_parameters(dt_type, label)

    Sigma1, F1a, F1b, S1a, S1b = get_resolution_paras(mode1, label)
    Sigma2, F2a, F2b, S2a, S2b = get_resolution_paras(mode2, label)

    opt, N, Nbkgd1, Nbkgd2, Nbkgd3, NbkgdFlat = get_double_paras(label)
    
    epsfile =  tools.set_file('eps', dt_type, mode, tag,
                              prefix=prefix, extbase=attr.figpath)
    fitpath = attr.fitpath 
    outfile =  tools.set_file('txt', dt_type, mode, tag,
                              prefix=prefix, extbase=fitpath)
    evtpath = attr.evtpath
    evtfile =  tools.set_file('evt', dt_type, mode, tag, prefix=evtprefix,
                              forceCombine=forceCombine, extbase=evtpath)
    if not os.access(evtfile, os.F_OK):
        if '818ipb' in evtprefix:
            evtfile_281ipb = evtfile.replace('818ipb', '281ipb')
            evtfile_537ipb = evtfile.replace('818ipb', '537ipb')
            combine_files(evtfile_281ipb, evtfile_537ipb, evtfile)
        else:
            raise ValueError(evtfile)

    tools.print_sep()

    par_str = '("%s", %f, %f, %f, %f, %f, "%s", %f, %f, %f, \
    %f, %f, "%s", "%s", "%s", %d, "%s", "%s", "%s", %f,\
    %f, %f,  %f, %f, %f, %f, %f)'

    par_tuple = (code1, Sigma1, F1a, F1b, S1a, S1b,
                 code2, Sigma2, F2a, F2b, S2a, S2b,
                 evtfile, epsfile, outfile, mc, opt, title1, title2,
                 Gamma, Mres, R, N, Nbkgd1, Nbkgd2, Nbkgd3, NbkgdFlat)
    
    par = par_str % par_tuple
        
    print_paras_double(par_tuple)

    load_roofit_lib(dt_type, label)

    sourcename = 'lineshapefit2d.C'
    #if interact:
    source = os.path.join(attr.srcfitpath, sourcename)
        
    tools.print_sep()
    sys.stdout.write('       ROOT macro: %s \n' % source)
    tools.print_sep()
    if test:
        return

    ROOT.gROOT.Macro( source + par)
    
    sys.stdout.write('Save output in %s\n'  % outfile)
    tools.eps2png(epsfile)
    tools.eps2pdf(epsfile)

     
def print_paras_double(paras):

    sys.stdout.write( '  code1   = %s\n'     %paras[0])
    sys.stdout.write( '  Sigma1  = %s\n'     %paras[1])
    sys.stdout.write( '  F1a     = %s\n'     %paras[2])
    sys.stdout.write( '  F1b     = %s\n'     %paras[3])
    sys.stdout.write( '  S1a     = %s\n'     %paras[4])
    sys.stdout.write( '  S1b     = %s\n'     %paras[5])
    sys.stdout.write( '  code2   = %s\n'     %paras[6])
    sys.stdout.write( '  Sigma2  = %s\n'     %paras[7])
    sys.stdout.write( '  F2a     = %s\n'     %paras[8])
    sys.stdout.write( '  F2b     = %s\n'     %paras[9])
    sys.stdout.write( '  S2a     = %s\n'     %paras[10])
    sys.stdout.write( '  S2b     = %s\n'     %paras[11])
    sys.stdout.write( '  evtfile = %s\n'     %paras[12])
    sys.stdout.write( '  epsfile = %s\n'     %paras[13])
    sys.stdout.write( '  outfile = %s\n'     %paras[14])
    sys.stdout.write( '  mc      = %s\n'     %paras[15])
    sys.stdout.write( '  opt     = %s\n'     %paras[16])
    sys.stdout.write( '  title1  = %s\n'     %paras[17])
    sys.stdout.write( '  title2  = %s\n'     %paras[18])
    sys.stdout.write( '  Gamma   = %s\n'     %paras[19])
    sys.stdout.write( '  Mres    = %s\n'     %paras[20])
    sys.stdout.write( '  R       = %s\n'     %paras[21])
    sys.stdout.write( '  N       = %s\n'     %paras[22])
    sys.stdout.write( '  Nbkgd1  = %s\n'     %paras[23])
    sys.stdout.write( '  Nbkgd2  = %s\n'     %paras[24])
    sys.stdout.write( '  Nbkgd3  = %s\n'     %paras[25])
    sys.stdout.write( '  NbkgdFlad = %s\n'   %paras[26])

def get_double_paras(label):
    opt = ''
    N = 4000.0
    Nbkgd1 = 1.0
    Nbkgd2 = 1.0
    Nbkgd3 = 1.0
    NbkgdFlat = 1.0
    if 'resolution' in label:
        opt += 'fm'

    if '/p/0.5' in label:
        opt += 'p'
    return opt, N, Nbkgd1, Nbkgd2, Nbkgd3, NbkgdFlat


def get_evtprefix(dt_type, label):
    if '/widede' in label or '/nofsr' in label or '/desideband' in label \
           or '/single_candidate' in label or '/multiple_candidate' in label \
           or '/kssideband' in label or '/trig' in label or '/phipi' in label \
           or '/k0star' in label or '/phsp' in label or '/kstar1410' in label:
        
        evtprefix = 'dir_' + label

        if '/fix_sigmap1' in label:
            evtprefix = evtprefix.replace('/fix_sigmap1', '')
        if '/fix_n1n2' in label:
            evtprefix = evtprefix.replace('/fix_n1n2', '')

    elif label == '281ipbv12' and dt_type == 'data':
        evtprefix = 'dir_281ipbv7'

    elif label == '537ipbv12' and dt_type == 'data':
        evtprefix = 'dir_537ipbv7'

    elif dt_type == 'data' and '818ipbv12' in label:
        evtprefix = 'dir_818ipbv7'

    elif dt_type == 'data' and '818ipbv13' in label:
        evtprefix = 'dir_818ipbv7'

    else:
        evtprefix = 'dir_'+label.split('/')[0]

    return evtprefix 


def get_argus_paras_single(label, dt_type, tag, mode):
    if 'argus' in label:
        prefix = 'dir_' + label.replace('argus', 'desideband')

    argus_para_base = attr.fitpath
    tabfile =  tools.set_file('txt', dt_type, mode, tag,
                              prefix=prefix,
                              extbase=argus_para_base)

    sys.stdout.write('Loading ARGUS parameters from %s ...\n' %tabfile)    
    tab     = DHadTable(tabfile)
    xi      = float(tab.cell_get('xi', 'Value'))
    p       = float(tab.cell_get('p', 'Value'))
                  
    return xi, p

