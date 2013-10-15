"""
Script for Web related tables

"""

import os
import sys
import attr
import web
import tools

from tools import DHadTable, parse_result
from attr.modes import modes
from attr import fitbase, get_generated_numbers

__author__ = "Xin Shi <xs32@cornell.edu>"
__revision__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2010-2011 Xin Shi"
__license__ = "GNU GPL"


def main(opts, args):
    tabname = args[0] #'_'.join(args).replace('/', '_')
    label = args[1]
    function = getattr(web, tabname)
    return function(opts, tabname, label)

    
def vary_argus_single(opts, tabname, label):
    tab = DHadTable()

    print tabname

    tabprefix0 = 'dir_818ipbv7/argus_low/fix_n1n2'
    tabprefix1 = 'dir_818ipbv7'
    tabprefix2 = 'dir_818ipbv7/argus_high/fix_n1n2'

    tab.column_append_from_dict('Mode', 'fname,fnamebar')
    titles = ['argus_low', 'std', 'argus_high']
    tab.column_append_from_files(titles[0], 'N1,N2', fitbase,
                                 tabprefix0, 'd', 's', 'txt')
    tab.column_append_from_files(titles[1], 'N1,N2', fitbase, tabprefix1,  
                                 'd', 's', 'txt')
    tab.column_append_from_files(titles[2], 'N1,N2', fitbase,
                                 tabprefix2, 'd', 's', 'txt')

    std = titles[1]
    colA = titles[0]
    colB = titles[2]
    headA = 'diff(%s)' %colA
    headB = 'diff(%s)' %colB
    headC = 'max-diff(%)'
    tab.column_append_by_diff_pct(headA, colA, std)
    tab.column_append_by_diff_pct(headB, colB, std)
    tab.column_append_by_max(headC, headA, headB)
    #tab.columns_delete([headA, headB])
    tab.columns_trim(titles, rnd='1.')

    tab.output()#tabname, texhead, outputtxt=True)


def fitResultsMC(opts, tabname, label):
    bffilename = 'bf_stat'
    bffile = tools.set_file(
        extbase=attr.brfpath, prefix='dir_'+label, comname=bffilename)

    if '281ipbv0' in label and '/generic' in label:
        generated = attr.Generic281v0_NBF
        power = '10E6'
        factor = 0.000001

    elif '281ipbv12' in label and '/generic' in label:
        generated = attr.Generic281_NBF
        power = '10E7'
        factor = 0.0000001

    elif '818ipbv12' in label and '/generic' in label:
        generated = attr.Generic818_NBF
        power = '10E7'
        factor = 0.0000001

    else:
        raise NameError(label)
    

    tab = DHadTable()
    tab.column_append(parse_result(bffile, 'paras'), 'Parameters')
    tab.column_append(parse_result(bffile, 'value_err'), 'Fitted Value')

    tab.column_append(generated, 'Generated Value')
    tab.column_append_by_diff_sigma('Difference', 'Fitted Value',
                                    'Generated Value')
    tab.column_trim('Fitted Value', row=['ND0D0Bar', 'ND+D-'],
                    rnd='.001', factor=factor, opt='(cell)x%s' %power)
    tab.column_trim('Fitted Value', rnd='.00001',
                    except_row=['ND0D0Bar', 'ND+D-'])
    tab.column_append(parse_result(bffile, 'err_frac'),
                      'Frac. Err', rnd='.1', opt='(cell%)')
    tab.columns_join('Fitted Value','Fitted Value','Frac. Err', str=' ')

    tab.column_trim('Generated Value', row=['ND0D0Bar', 'ND+D-'],
                    rnd='.001', factor=factor, opt='cellx%s'%power)
    tab.output(tabname, label=label)


def eff_kkpi_comp(opts, tabname, label):
    tab = DHadTable()
    tabprefix = 'dir_'+label
    mode = 205 

    tab.column_append_from_dict('Mode', 'fname,fnamebar', mode=mode)
    tab.column_append([20000, 20000], 'Generated')
    tab.column_append_from_files('Yield', 'N1,N2', fitbase, tabprefix, 
                                 's', 's' ,'txt', rnd='1.', mode=mode)
    tab.column_append_by_divide('Eff(%)','Yield','Generated',  
                                'Efcy', '.01', 100) 
    tab.columns_delete(['Generated', 'Yield'])

    def get_eff(subdir):
        logname = 'signal_Single_%s.txt' % modes[mode]['fname']
        logpath = os.path.join(attr.logpath, label, subdir, 'yld')
        logfile = tools.set_file(extbase=logpath, comname=logname)
        for line in file(logfile):
            if 'selected' in line:
                total = int(line.split()[-1].replace('.', ''))
                break
        t = DHadTable()
        t.column_append([total, total], 'Generated')
        t.column_append_from_files('Yield', 'N1,N2', fitbase, '%s/%s' %(
            tabprefix, subdir), 's', 's' ,'txt', rnd='1.', mode=mode)
        t.column_append_by_divide('%s(%%)' % subdir, 'Yield','Generated',  
                                  'Efcy', '.01', 100)
        return t.column_get('%s(%%)' % subdir)

    for subdir in ['phipi', 'k0star', 'phsp']:
        tab.column_append(get_eff(subdir))
        #head_diff =  subdir
        #col = '%s(%%)' % subdir
        #std = 'Eff(%)'
        #tab.column_append_by_diff_pct(head_diff, col, std)

    tab.output(tabname, label=label)
