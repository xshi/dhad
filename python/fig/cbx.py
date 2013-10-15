"""
Module for plotting figures on CBX

"""

import os
import sys
import attr
import cbx
from tools import set_file, check_and_copy


__author__ = "Xin Shi <xs32@cornell.edu>"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2005-2011 Xin Shi"
__license__ = "GPL"
__revision__ = "$Revision$"


def main(opts, args):
    figname = args[0]
    label = args[1]
    prefix = 'dir_%s' %label
    function = getattr(cbx, figname)
    return function(opts, figname, prefix)


def continuum_background(opts, figname, prefix):
    srcfigname = 'generic_cont_background'
    srcpdffile = set_file(extbase=attr.rfigpath, comname=srcfigname,
                          ext='pdf', prefix=prefix)
    pdffile = set_file(extbase=attr.cbxfigpath, comname=figname, ext='pdf')
    check_and_copy(srcpdffile, pdffile, verbose=1)
    

def copy_remote_files(srcfignames, prefix):
    for srcfigname in srcfignames:
        srcpdffile = set_file(extbase=attr.rfigpath, comname=srcfigname,
                              ext='pdf', prefix=prefix)
        pdffile = set_file(extbase=attr.cbxfigpath, comname=srcfigname,
                           ext='pdf')
        check_and_copy(srcpdffile, pdffile, verbose=1)


def copy_remote_cbx_figs(srcfignames, prefix=''):
    for srcfigname in srcfignames:
        srcpdffile = set_file(extbase=attr.rfigpath, comname=srcfigname,
                              ext='pdf', prefix=prefix)
        pdffile = set_file(extbase=attr.cbxfigpath, comname=srcfigname,
                           ext='pdf', prefix=prefix)
        check_and_copy(srcpdffile, pdffile, verbose=1)


def crossfeeds_one(opts, figname, prefix):
    srcfignames = ['signal_Single_D0_to_Kpi_fakes_Single_D0B_to_Kpi',
                   'signal_Single_D0B_to_Kpi_fakes_Single_D0_to_Kpi']
    prefix = os.path.join(prefix, 'crossfeeds')
    copy_remote_files(srcfignames, prefix)



def double_tag_all(opts, figname, prefix):
    srcfignames = []
    for modename in attr.double_mode_list:
        for datatype in ['signal', 'data', 'generic']:
            srcfignames.append('%s_%s' %(datatype, modename))
    copy_remote_files(srcfignames, prefix)
 

def generic_background(opts, figname, prefix):
    srcfigname = 'generic_ddbar_background'
    srcpdffile = set_file(extbase=attr.rfigpath, comname=srcfigname,
                          ext='pdf', prefix=prefix)
    pdffile = set_file(extbase=attr.cbxfigpath, comname=figname, ext='pdf')
    check_and_copy(srcpdffile, pdffile, verbose=1)


def pi0_momentum(opts, figname, prefix):
    srcfignames = ['var_pi0_momentum_data_Single_D0_to_Kpipi0_818ipbv7',
                   'var_pi0_momentum_data_Single_Dp_to_Kpipipi0_818ipbv7',
                   'var_pi0_momentum_data_Single_Dp_to_Kspipi0_818ipbv7']
    prefix = ''
    copy_remote_files(srcfignames, prefix)

  
def radret_background(opts, figname, prefix):
    srcfigname = 'generic_radret_background'
    srcpdffile = set_file(extbase=attr.rfigpath, comname=srcfigname,
                          ext='pdf', prefix=prefix)
    pdffile = set_file(extbase=attr.cbxfigpath, comname=figname, ext='pdf')
    check_and_copy(srcpdffile, pdffile, verbose=1)


def single_tag_all(opts, figname, prefix):
    srcfignames = []
    for modename in attr.diag_single_mode_list:
        for datatype in ['signal', 'data']:#, 'generic']:
            srcfignames.append('%s_%s' %(datatype, modename))
    copy_remote_files(srcfignames, prefix)
                               

def tautau_background(opts, figname, prefix):
    srcfigname = 'generic_tau_background'
    srcpdffile = set_file(extbase=attr.rfigpath, comname=srcfigname,
                          ext='pdf', prefix=prefix)
    pdffile = set_file(extbase=attr.cbxfigpath, comname=figname, ext='pdf')
    check_and_copy(srcpdffile, pdffile, verbose=1)


def trkmtm(opts, figname, prefix):
    srcfignames = []
    prefix += '/trkmtm'
    for mode in attr.modes:
        if mode in [0, 202]:
            continue
        
        sname = attr.modes[mode]['sname'].lower()
        srcfignames.append('%s_effmomenta_plain' % sname)
        srcfignames.append('%s_effmomenta' % sname)
        srcfignames.append('%s_momenta' % sname)
        srcfignames.append('%s_momentacor' % sname)
        
    copy_remote_cbx_figs(srcfignames, prefix)


def kkpidalitz(opts, figname, prefix):
    srcfignames = []
    mode = 205
    srcfignames.append('kkmass2_signal_data_Single_Dp_to_KKpi')
    srcfignames.append('kpimass1_signal_data_Single_Dp_to_KKpi')
    copy_remote_cbx_figs(srcfignames, prefix)
    
    
