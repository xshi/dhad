"""
Module for Branching Fractions Fitting 

"""

import os
import sys
import tools
import attr

from brf import datayields, sigeffs, syserr, files, staterr, genericyields

__author__ = "Xin Shi <xs32@cornell.edu>"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2005-2011 Xin Shi"
__license__ = "GPL"
__revision__ = "$Revision$"


def main(opts, args):
    verbose = opts.verbose
    
    paras = parse_parameters(opts, args)

    prefix = paras[0]
    prefix_data = paras[1]
    prefix_signal = paras[2]
    opt_sys_err = paras[3]
    fit1 = paras[4]
    fit2 = paras[5]


    if '/generic' in prefix:
        if prefix == 'dir_281ipbv0.0/generic' or \
               prefix == 'dir_281ipbv0.2/generic' :
            staterr.generic_fit_staterrors(fit1, prefix, verbose=verbose)
            return
        
        elif prefix == 'dir_281ipbv0.1/generic':
            prefix_generic = 'dir_281ipbv0.1'
            prefix_signal = 'dir_281ipbv0.1'

        elif '281ipbv12' in prefix:
            prefix_generic = 'dir_281ipbv12'
            prefix_signal = 'dir_281ipbv12'

        elif '818ipbv12' in prefix:
            prefix_generic = 'dir_818ipbv12'
            prefix_signal = 'dir_818ipbv12'

        else:
            raise NameError(prefix)

        genericyields.statonly_generic_yields(
            prefix, prefix_generic, verbose=verbose)  
        files.get_external_bkg_files_generic(prefix)
        files.get_background_files(prefix)
        sigeffs.signal_single_efficiencies(opts, prefix, prefix_signal,
                                           verbose=verbose)
        sigeffs.signal_double_efficiencies(prefix, prefix_signal,
                                           verbose=verbose) 
        syserr.get_statonly_sys_err_generic(prefix)
        files.get_other_files_generic(prefix)
        staterr.generic_fit_staterrors(fit1, prefix, verbose=verbose)
        return

        
    datayields.data_yields(prefix, prefix_data, opt_sys_err, verbose=verbose)
    datayields.statonly_data_yields(prefix, prefix_data, verbose=verbose)  
    sigeffs.signal_single_efficiencies(opts, prefix, prefix_signal, verbose=verbose)
    sigeffs.signal_double_efficiencies(prefix, prefix_signal, verbose=verbose) 
    syserr.get_statonly_sys_err(prefix)
    files.get_other_files(prefix) 
    files.get_data_statonly_crosssectionsdef(prefix) 
    files.get_background_files(prefix)
    files.get_external_bkg_files(prefix)
    if opts.test:
        return
    
    staterr.data_fit_staterrors(fit1, prefix, verbose=verbose)
    files.get_data_crosssectionsdef(prefix) 
    syserr.get_sys_err(prefix, opt_sys_err, verbose=verbose) 
    syserr.bf_stat_sys(fit2, prefix)
    
    
def parse_parameters(opts, args):
    if len(args) > 1:
        raise NameError(args)

    paras = []
    label = args[0]

    prefix = 'dir_' + label

    input_prefix = prefix
    if '.' in prefix:
        input_prefix = prefix.split('.')[0]
    
    prefix_data = input_prefix
    prefix_signal = input_prefix
    
    opt_sys_err = ''
    
    if '/nofsr' in label:
        prefix_data = prefix.split('/')[0]

    if '/gamma/' in label:
        prefix_signal = prefix.split('/')[0]

    fit1 = True
    fit2 = True
    
    if opts.test:
        fit1 = False
        fit2 = False
        
    paras.append(prefix)     
    paras.append(prefix_data) 
    paras.append(prefix_signal) 
    paras.append(opt_sys_err) 
    paras.append(fit1) 
    paras.append(fit2) 

    return paras

