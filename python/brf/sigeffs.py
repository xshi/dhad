"""
Module for Branching Fractions Fitting 

"""

import os
import sys
import attr
import tools
import math 
from attr.modes import modes
from tools import DHadTable
from tab.brf import yields_and_efficiencies

__author__ = "Xin Shi <xs32@cornell.edu>"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2005-2011 Xin Shi"
__license__ = "GPL"
__revision__ = "$Revision$"



def signal_single_efficiencies(opts, prefix, prefix_signal, verbose=0):
    effmatrix = []
    errmatrix = []
    mode_sign_list  = [(i,j) for i in modes for j in (1, -1)]
    dt_type = 's'
    tag     = 's'

    label = prefix.replace('dir_', '')
    
    prefix_yld = prefix
    if ('/nofsr' in prefix) or ('/widede' in prefix) or (
        '/gamma/' in prefix) or ('/p/0.5' in prefix):
        prefix_yld = prefix_yld.split('/')[0]

    if '281ipbv0' in label:
        yldfile = os.path.join(attr.datpath, 'brf', '281ipbv0',
                               'yields_and_efficiencies')
    else:
        yldfile = yields_and_efficiencies(opts, [label])

    for i in mode_sign_list:
        mode = i[0]
        sign = i[1]
        effline = []
        errline = []
        tot_gen  = get_generated_numbers_single(i, prefix_signal)
        for j in  mode_sign_list:
            if i == j: 
                eff  = get_diag_eff(prefix_signal, dt_type,
                                    tag, mode, sign, tot_gen)
                err  = get_diag_err(prefix_signal, dt_type,
                                    tag, mode, sign, tot_gen, eff)
            else:      
                eff  = get_off_diag_eff(i, j, yldfile, verbose)
                err  = get_off_diag_err(i, j, yldfile, verbose)

            effline.append(eff)
            errline.append(err)

        effmatrix.append(effline)
        errmatrix.append(errline)

    eff_file_name = 'signal_single_efficiencies_for_werner'
    err_file_name = 'signal_single_efficiencies_errors_for_werner'

    eff_file  = tools.set_file(
        extbase=attr.brfpath, prefix=prefix, 
        comname=eff_file_name)

    err_file  = tools.set_file(
        extbase=attr.brfpath, prefix=prefix, 
        comname=err_file_name)

    output_matrix(effmatrix, eff_file)
    output_matrix(errmatrix, err_file)

def get_generated_numbers_single(i, prefix=''):
    if '281ipb' in prefix:
        mult_fact = 10
    elif '537ipb' in prefix:
        mult_fact = 20
    elif '818ipb' in prefix:
        mult_fact = 30
    else:
        raise NameError(prefix)
    
    mode = i[0]
    sign = i[1]
    tag_number = modes[mode]['tag_num_s']
    count = tag_number*mult_fact

    if 'noFSR' in prefix:
        mode = i[0]
        sign = i[1]
        logfile =  tools.set_file('log', 's',  mode, 's', sign, prefix,
                                      extbase=evtlogbase)
        tab = DHadTable(logfile)
        FSR = tab.cell_get('FSR', 'Value')
        count = count - int(FSR)
        
    return count

def getfnamestr(pair):
    if pair[1] == 1:
        return modes[pair[0]]['fname']
    else:
        return modes[pair[0]]['fnamebar']

def get_diag_eff(prefix, dt_type, tag, mode, sign, tot_gen):
    txtfile =  tools.set_file('txt', dt_type, mode, tag, prefix=prefix,
                              extbase=attr.fitpath)
    if sign == 1:
        name = 'N1'
    else:
        name = 'N2'
    yld  = float(DHadTable(txtfile).cell_get(name, 'Value'))

    if '281ipbv0.1' in prefix and mode == 0:
        tot_gen = tot_gen/2.

    eff  = yld/tot_gen
    return eff


def get_diag_err(prefix, dt_type, tag, mode, sign, tot_gen, eff):
    txtfile =  tools.set_file('txt', dt_type, mode, tag, prefix=prefix,
                              extbase=attr.fitpath)
    if sign == 1:
        name = 'N1'
    else:
        name = 'N2'
    yld_err  = float(DHadTable(txtfile).cell_get(name, 'Error'))

    if '281ipbv0.1' in prefix and mode == 0:
        tot_gen = tot_gen/2.

    err      = yld_err/tot_gen*math.sqrt(1-eff)
    return err

def get_off_diag_eff(i, j, yldfile, verbose = 0):
    eff = 0
    cfeed = open(yldfile, 'r')
    cfeedlines = cfeed.readlines()
    fname_i = tools.get_fname(i)
    fname_j = tools.get_fname(j)
    idstring = '%s fakes %s:' % (fname_i, fname_j)
    for st in cfeedlines:
        if idstring in st:
            use_this_value = False
            a   = float(st.split()[-2]) 
            b   = float(st.split()[3])  # signal MC yield/error on yield

            if a > 0 and abs(1-b) > 3 and idstring in attr.used_crossfeeds:
                eff = a
                sys.stdout.write('crossfeed is using %s  %s\n' % (idstring, a))

    return eff

def get_off_diag_err(i, j, yldfile, verbose = 0):
    err = 0
    cfeed = open(yldfile, 'r')
    cfeedlines = cfeed.readlines()
    fname_i = tools.get_fname(i)
    fname_j = tools.get_fname(j)
    idstring = '%s fakes %s:' % (fname_i, fname_j)
    for st in cfeedlines:
        if idstring in st:
            use_this_value = False
            a   = float(st.split()[-2]) 
            b   = float(st.split()[3])  # signal MC yield/error on yield
            c   = float(st.split()[-1]) # efficiency error

            if a > 0 and abs(1-b) > 3 and idstring in attr.used_crossfeeds:
                err = c*math.sqrt(1-a)
                if verbose > 0:
                    print 'err: crossfeed is using %s' % idstring

    return err

def output_matrix(matrix, outfile):

    fo, bakfile = tools.backup_output(outfile)

    for i in xrange(len(matrix[0])):
        for j in xrange(len(matrix)):
            fo.write('%s\n' % matrix[j][i])

    tools.check_output(fo, outfile, bakfile)
 


def signal_double_efficiencies(prefix, prefix_signal, verbose=0):
    effmatrix = []
    errmatrix = []
    dt_type = 's'
    tag     = 'd'

    mode_pair_list = attr.PossibleDoubleTags
    for i in mode_pair_list:
        txtfile = tools.set_file('txt', dt_type, i, tag, 
                                 prefix=prefix_signal,
                                 extbase=attr.fitpath)

        N      = float(DHadTable(txtfile).cell_get(1, 'Value'))
        N_err  = float(DHadTable(txtfile).cell_get(1, 'Error'))

        tot_gen  = get_generated_numbers_double(i, prefix_signal)

        effline = []
        errline = []

        for j in  mode_pair_list:
            if i == j:
                if '281ipbv0.1' in prefix and i == (1, 1):
                    tot_gen = tot_gen*(0.257402179684/0.140119760479)
                
                eff  = N/tot_gen
                err  = N_err/tot_gen*math.sqrt(1-eff)
            else:
                eff = 0
                err = 0

            effline.append(eff)
            errline.append(err)

        effmatrix.append(effline)
        errmatrix.append(errline)
                
    eff_file_name = 'signal_double_efficiencies_for_werner'
    err_file_name = 'signal_double_efficiencies_errors_for_werner'

    eff_file  = tools.set_file(
        extbase   = attr.brfpath, prefix  = prefix, 
        comname   = eff_file_name)

    err_file  = tools.set_file(
        extbase   = attr.brfpath, prefix  = prefix, 
        comname   = err_file_name)

    output_matrix(effmatrix, eff_file)
    output_matrix(errmatrix, err_file)
                

def get_generated_numbers_double(pair, prefix=''):
    if '281ipb' in prefix:
        mult_fact = 10
    elif '537ipb' in prefix:
        mult_fact = 20
    elif '818ipb' in prefix:
        mult_fact = 30
    else:
        raise NameError(prefix)

    i = pair[0]
    j = pair[1]

    #genpath = attr.genpath
    #print genpath
    #sys.exit()
    #if attr.analysis == '10.1' and '281ipbv0' in prefix :
    #    genpath = '/nfs/cor/user/ponyisi/cleog/scripts-summerconf/'

    tag_number = 2000
    count = tag_number * mult_fact

    if 'noFSR' in prefix:
        logfile =  tools.set_file('log', 's',  pair, 'd', prefix=prefix,
                                  extbase=evtlogbase)
        tab =DHadTable(logfile)
        FSR = tab.cell_get('FSR', 'Value')
        count = count - int(FSR)

    return count

