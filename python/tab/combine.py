"""
Script to combine comparison table

"""

import os
import sys

import attr
import combine
from tools import DHadTable


__author__ = "Xin Shi <xs32@cornell.edu>"
__revision__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2010 Xin Shi"
__license__ = "GNU GPL"


def main(opts, args):

    global _opts, _tabname

    _opts = opts
    _tabname = 'combine_' + '_'.join(args).replace('/', '_')

    function = getattr(combine, args[0])
    return function(args[1:])



def compare_yields_data_signal_divide_537ipb(args):
    
    sys.stdout.write('dhad.table: Creating %s ...\n' % _tabname)
    tabpath1 = os.path.join(
        attr.base, '7.06', 'tab')
    tabfile1 = os.path.join(
        tabpath1, 'compare_yields_data_divide_281ipb_537ipb.txt')
    tabfile2 = os.path.join(
        attr.tabpath, 'compare_yields_signal_divide_537ipb_9.03_regular12.txt')
    
    tab  = DHadTable()
    tab.column_append_from_tab_file('Mode', tabfile1, 'Mode')
    tab.column_append_from_tab_file('Data', tabfile1, '537ipb/281ipb')
    tab.column_append_from_tab_file('Signal', tabfile2, '537ipb/281ipb')
    tab.column_append_by_diff_sigma_pct('diff(%)', 'Signal', 'Data')
    tab.output(_tabname)
   
def signal_line_shape_syst(args):
    '''
    --------------------------------------------------
       Signal line shape systematics
    --------------------------------------------------
    '''
    tab_name = 'signal_line_shape_syst'

    tabbase = os.path.join(attr.base, '7.06', 'tab')
    
    tab = DHadTable()
    tab.column_append_from_dict('Mode', 'fname,fnamebar')
    tab_file_A = os.path.join(
        tabbase, 'yields_M_3.7713_regular_M_3.7723_data_Single.txt')

    name_A  = 'Mass(+/-0.5 MeV)%'
    column = 'max-diff(%)'
    tab.column_append_from_tab_file(name_A, tab_file_A, column)

    tab_file_B = os.path.join(
        tabbase, 'yields_Gamma_0.0261_regular_Gamma_0.0311_data_Single.txt')
    name_B  = 'Gamma(+/-2.5 MeV)%'
    tab.column_append_from_tab_file(name_B, tab_file_B, column)


    tab_file_C = os.path.join(
        tabbase, 'yields_R_8.3_regular_R_16.3_data_Single.txt')
    name_C  = 'R(+/- 4)%'
    tab.column_append_from_tab_file(name_C, tab_file_C, column)

    name_D = 'Total(%)'
    tab.column_append_by_add_quadrature3(name_D, name_A,
                                        name_B, name_C, rnd='.01')

    tab.rows_join_by_max(name_D)
    
    tab.output(tab_name)


def fsr_syst(args):
    '''
    --------------------
       FSR systematics
    --------------------
    '''
    tab_name = 'FSR_syst'

    tabbase = os.path.join(attr.base, '7.06', 'tab')
    
    tab = DHadTable()
    tab.column_append_from_dict('Mode', 'fname,fnamebar')
    tab_file = os.path.join(tabbase, 'noFSR_single_signal_eff.txt')
    columnA    = 'Efficiency without FSR(%)'
    tab.column_append_from_tab_file(columnA, tab_file)
    columnB     = 'Efficiency with FSR(%)'
    tab.column_append_from_tab_file(columnB, tab_file)
    tab.column_append_by_diff('diff(%)', columnA, columnB, factor=100)
    tab.column_append_by_times_number('diff X 30%', 'diff(%)', '0.3',
                                      rnd='.01')
    tab.rows_join_by_max('diff X 30%')
    tab.output(tab_name)
