"""
Module for Branching Fractions Fitting 

"""

import os 
import tools
import attr
import math
from tools import DHadTable
import sys 
from attr.modes import modes


__author__ = "Xin Shi <xs32@cornell.edu>"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2005-2011 Xin Shi"
__license__ = "GPL"
__revision__ = "$Revision$"


def data_yields(prefix, prefix_data, opt_sys_err='', verbose=0):
    outfilename = 'data_yields_for_werner'
    outfile  = tools.set_file(
        extbase = attr.brfpath, prefix = prefix, 
        comname = outfilename)

    label = prefix.replace('dir_', '')
    fo, bakfile = tools.backup_output(outfile)

    data_yields_single(fo, prefix_data, label=label, verbose=verbose)
    data_yields_double(fo, prefix_data, opt=opt_sys_err, label=label,
                       verbose=verbose)

    tools.check_output(fo, outfile, bakfile)


def data_yields_single(fo, prefix, opt='', label='', verbose=0):
    sys_err, sys_err_by_mode = attr.sys_err(label)

    dt_type = 'd'
    tag     = 's'

    #sys_err_by_mode = attr.sys_err_by_mode(label)

    for mode in modes:
        if opt == 'statonly':
            syerrmul = 0
        else:
            syerrmul = sys_err_by_mode[mode]['ST Background modeling']
            if mode ==0:
                lepton_veto = sys_err_by_mode[mode]['Lepton veto']
                syerrmul = math.sqrt(syerrmul**2+ lepton_veto**2)

        input_file = tools.set_file('txt', dt_type, mode, tag,
                                    prefix=prefix, extbase=attr.fitpath)
        tab    = DHadTable(input_file)
        N1     = tab.cell_get(1, 'Value')
        N1_err = tab.cell_get(1, 'Error')
        N1_err_sys = str(float(N1)*syerrmul)

        N2     = tab.cell_get(2, 'Value')
        N2_err = tab.cell_get(2, 'Error')
        N2_err_sys = str(float(N2)*syerrmul)

        fo.write('%s\n%s\n%s\n' % (N1, N1_err, N1_err_sys))
        fo.write('%s\n%s\n%s\n' % (N2, N2_err, N2_err_sys))

        if verbose > 1:
            print '%s +/- %s +/- %s'  % (N1, N1_err, N1_err_sys)
            print '%s +/- %s +/- %s'  % (N2, N2_err, N2_err_sys)
    if verbose >0:
        print 'single tag data yield finished.'


       
def data_yields_double(fo, prefix, opt='', label='', verbose=0):
    dt_type = 'd'
    tag     = 'd'
    mode_pair_list = attr.PossibleDoubleTags
    n = 0 

    for mode_pair in mode_pair_list:
        i = mode_pair[0]
        j = mode_pair[1]
        txtfile = tools.set_file('txt', dt_type, mode_pair, tag, 
                                 prefix  = prefix, extbase=attr.fitpath)
        tab    = DHadTable(txtfile)
        N      = tab.cell_get(1, 'Value')
        N_err  = tab.cell_get(1, 'Error')

        if 'DCSD_0' in opt :
            dcsd_sys = 0
            
        if opt == 'statonly':
            syerrmul = 0

        else:
            syerrmul = 0
            if i in (0, 1, 3):
                dcsd_sys, dcsd_cor = get_dcsd_sys(label, i, j)
                syerrmul += dcsd_sys**2
                if dcsd_cor != None:
                    sys.stdout.write(
                        'Correcting mode (%s %s) with %s +/- %s ...\n' %(
                        i,j,dcsd_cor, dcsd_sys))
                    N = str(float(N)*dcsd_cor)

            syerrmul = syerrmul**.5

        N_err_sys = str(float(N)*syerrmul)
        fo.write('%s\n%s\n%s\n' % (N, N_err, N_err_sys))
        n += 1
        if verbose > 1:
            print '%s +/- %s +/- %s'  % (N, N_err, N_err_sys)

    if verbose >0:
        print 'Total double tag data yield lines ... %s' %n


def statonly_data_yields(prefix, prefix_data, verbose=0):
    outfilename = 'statonly_data_yields_for_werner'

    label = prefix.replace('dir_', '')
    outfile = tools.set_file(extbase=attr.brfpath, prefix=prefix, 
                             comname=outfilename)

    fo, bakfile = tools.backup_output(outfile)

    data_yields_single(fo, prefix_data, opt='statonly', label=label, verbose=verbose)
    data_yields_double(fo, prefix_data, opt='statonly', label=label, verbose=verbose)

    tools.check_output(fo, outfile, bakfile)


def get_dcsd_sys(label, i, j):
    if label in ['281ipbv12.0']:
        sys_err = attr.sys_err(label)
        dcsd_sys = float(sys_err['Double DCSD interference(Neutral DT)'])
        dcsd_cor = None
    elif label in ['818ipbv12.0', '818ipbv12.1', '818ipbv12.2', '818ipbv12.3',
                   '818ipbv12.4', 'v13.1', 'v13.2']:
        tabdir = '818ipbv7'
        tabfile = os.path.join(attr.cbxtabpath, tabdir,
                               'dcsd_correction.txt')
        tab = DHadTable(tabfile)
        modename = '%s %s' %(modes[i]['fname'], modes[j]['fnamebar'])
        dcsd_val_err = tab.cell_get(modename, 'Yield correction factor')
        dcsd_cor = float(dcsd_val_err.split('+/-')[0])
        dcsd_sys = float(dcsd_val_err.split('+/-')[1])
    else:
        raise NameError(label)

    return dcsd_sys, dcsd_cor 
