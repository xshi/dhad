"""
Script for Slide related tables

"""

import os
import sys
import attr
import sld
import tools

from tools import DHadCBXTable, parse_result


__author__ = "Xin Shi <xs32@cornell.edu>"
__revision__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2010 Xin Shi"
__license__ = "GNU GPL"


def main(opts, args):
    tabname = '_'.join(args)
    function = getattr(sld, args[0])
    return function(opts, tabname, args[1:])


def brf_data_results(opts, tabname, args):
    label_A = args[0]
    label_B = args[1]
    tabbase = os.path.join(attr.base, 'doc', args[2], 'tab')
    
    labels = []
    labels.append(label_A)
    labels.append(label_B)

    bffilename = 'bf_stat_sys'
    tab = DHadCBXTable()
    paras = False
    for label in labels:
        if '281ipb' in label:
            factor =  0.000001
        elif '537ipb' in label:
            factor =  0.000001*281/537
        elif '818ipb' in label:
            factor =  0.000001*281/818
        else:
            raise NameError(label)

        if '818ipb' in label_A and '818ipb' in label_B:
            factor = 0.000001
            
        bffile = os.path.join(attr.brfpath(), label, bffilename)
        if not paras:
            tab.column_append(tools.parse_result(bffile, 'paras'),
                              'Parameters')
            paras = True
        tab.column_append(tools.parse_result(bffile, 'value'), 'value')
        tab.column_append(tools.parse_result(bffile, 'stat'),  'stat')
        tab.column_append(tools.parse_result(bffile, 'syst'),  'syst')
        tab.columns_join3('Fitted Value', 'value', 'stat',  'syst')
        tab.column_trim('Fitted Value', row=['ND0D0Bar', 'ND+D-'],
                        rnd='.001', factor=factor, opt='(cell)x1E6')
        tab.column_trim('Fitted Value', rnd='.0001',
                        except_row=['ND0D0Bar', 'ND+D-'])
        tab.column_append(tools.parse_result(bffile, 'err_frac'),
                          'Frac. Err', rnd='.1', opt='(cell%)')
        tab.columns_join(label, 'Fitted Value','Frac. Err', str=' ')
    tab.column_append_by_diff_sigma('Difference', label_B,label_A)
    tab.output(tabname, tabbase=tabbase, trans_dict=attr.NBF_dict)
