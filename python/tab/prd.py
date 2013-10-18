"""
Script for Thesis related tables

"""

import os
import sys
import attr
import ths
import tools
import cbx

from tools import PRDTable, parse_result
from attr.modes import modes
from attr import cbxtabpath, fitbase, get_dcsd_correction, \
     get_pi0_eff_correction
from tools.filetools import BrfFile, PDLFile
from brf import yields_and_efficiencies


__author__ = "Xin Shi <xs32@cornell.edu>"
__revision__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2011 Xin Shi"
__license__ = "GNU GPL"


def main(opts, args):
    tabname = args[0]
    label = args[1]
    function = getattr(ths, tabname)
    return function(opts, tabname, label)


def fitResultsData(opts, tabname, label):
    bffilename = 'bf_stat_sys'
    bffile = tools.set_file(
        extbase=attr.brfpath, prefix='dir_'+label, comname=bffilename)
    tab = PRDTable()
    tab.column_append(parse_result(bffile, 'paras'), 'Parameters')
    tab.column_append(parse_result(bffile, 'value'), 'value')
    tab.column_append(parse_result(bffile, 'stat'),  'stat')
    tab.column_append(parse_result(bffile, 'syst'),  'syst')
    tab.column_append_by_divide('Stat.(%)', 'stat', 'value',
                                rnd='.1', factor=100)
    tab.column_append_by_divide('Syst.(%)', 'syst', 'value',
                                rnd='.1', factor=100)
    tab.columns_join3('Fitted value', 'value', 'stat',  'syst')
    tab.column_trim('Fitted value', row=['ND0D0Bar', 'ND+D-'],
                    rnd='.001', factor=0.000001, opt='(cell)x10E6')
    tab.column_trim('Fitted value', rnd='.001', factor=100,
                    except_row = ['ND0D0Bar', 'ND+D-'], opt='(cell)%')
    texhead = r'''Parameter & Fitted value & \multicolumn{2}{c}{Fractional error}\\[-0.6ex] & & Stat.(\%) & Syst.(\%)'''
    tab.output(tabname, texhead, trans_dict=attr.NBF_dict)


def fitResultsRatiosData(opts, tabname, label):
    bffilename = 'bf_stat_sys'
    bffile = tools.set_file(
        extbase=attr.brfpath, prefix='dir_'+label, comname=bffilename)
    tab = PRDTable()
    tab.column_append(parse_result(bffile, 'para_bf_ratio'),
                      'Parameters')
    tab.column_append(parse_result(bffile, 'value_bf_ratio'), 'value')
    tab.column_append(parse_result(bffile, 'stat_bf_ratio'), 'stat')
    tab.column_append(parse_result(bffile, 'syst_bf_ratio'), 'syst')
    tab.column_append_by_divide('Stat.(%)', 'stat', 'value',
                                rnd='.1', factor=100)
    tab.column_append_by_divide('Syst.(%)', 'syst', 'value',
                                rnd='.1', factor=100)
    tab.columns_join3('Fitted value','value','stat','syst', rnd='.001')
    texhead = r'''Parameter & Fitted value & \multicolumn{2}{c}{Fractional error}\\[-0.6ex] & & Stat.(\%) & Syst.(\%)'''
    tab.output(tabname, texhead, trans_dict=attr.BF_Ratio_dict)

