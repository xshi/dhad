"""
Script to list parameters

"""

import os
import sys

import attr
import para
import tools
from tools import DHadTable


__author__ = "Xin Shi <xs32@cornell.edu>"
__revision__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2010-2011 Xin Shi"
__license__ = "GNU GPL"


def main(opts, args):
    #global _opts, _tabname
    #_opts = opts
    #_tabname = 'para_' + '_'.join(args).replace('/', '_')

    label = args[-1]
    tabname = '%s/para_%s' %(label, '_'.join(args[:-1]))

    function = getattr(para, args[0])
    return function(opts, tabname, args[1:])

def argus(opts, tabname, args):
    if args[0] == 'slope':
        rowname_A = 'xi'
        rowname_B = 'xi'
        rowname_C = 'xi'

    if args[0] == 'power':
        rowname_A = 'p'
        rowname_B = 'p'
        rowname_C = 'p'
    
    label = args[1]
    
    if args[2] != 'desidebands':
        raise NameError(args)

    namestyle = 'fname'
    rnd = '0.01'
    tag = 's'
    extbase = attr.fitbase
    ext = 'txt'
    dt_type = 'data'

    label_A = label
    prefix_A = 'dir_%s' % label_A

    label_B = 'desideband_low'
    prefix_B = 'dir_%s/%s' % (label, label_B)

    label_C = 'desideband_high'
    prefix_C = 'dir_%s/%s' % (label, label_C)

    tab = DHadTable()
    tab.column_append_from_dict('Mode', namestyle)
    tab.column_append_from_files(label_A, rowname_A, extbase, prefix_A,
                                 dt_type, tag, ext, rnd=rnd)
    tab.column_append_from_files(label_B, rowname_B, extbase, prefix_B,
                                 dt_type, tag, ext, rnd=rnd)
    tab.column_append_from_files(label_C, rowname_C, extbase, prefix_C,
                                 dt_type, tag, ext, rnd=rnd)
    tab.output(tabname)



def md(opts, tabname, args):
    para = 'md'
    namestyle = 'fname'
    rnd = '0.0000001'
    tag = 's'
    
    if opts.set:
        for li in opts.set.split(';'):
            name = li.split('=')[0]
            value = li.split('=')[1]
            sys.stdout.write('Set %s = %s \n' % (name, value))
            if name == 'label':
                label = value
                
    if args[0] == '281ipb':
        tab_A_name = args[1]
        tab_B_name = args[2]
        tab_C_name = args[3]

        if label:
            labels = label.split(',')
            tab_A_name = labels[0]
            tab_B_name = labels[1]
            tab_C_name = labels[2]
            
        tab = DHadTable()
        tab.column_append_from_dict('Mode', namestyle)
        tab.column_append_from_fit_files(tab_A_name, args[1], para, tag, rnd)
        tab.column_append_from_fit_files(tab_B_name, args[2], para, tag, rnd)
        tab.column_append_from_fit_files(tab_C_name, args[3], para, tag, rnd)

        tab.output(_tabname)
    else:
        raise ValueError(args)


def momentum(opts, tabname, args):
    if args[0] != 'resolution': 
        raise NameError(args)

    label = args[1] 
    dt_type = 'signal'
    tag = 'double'
    #ver = opts.analysis
    fitbase = attr.fitpath

    prefix = 'dir_%s/resolution' % label

    # Mode | sigma(MeV) | fa | fb | sa | sb | [sigmaE (MeV)]
    tab = DHadTable()
    tab.column_append_from_dict('Mode', 'fname')     
    tab.column_append_from_files(
        'sigma (MeV)', 'sigmacommon1', fitbase, prefix, 
        dt_type, tag,  'txt', rnd='.01', factor=1000)

    tab.column_append_from_files('fa', 'f1a',  fitbase, prefix, 
                                 dt_type, tag,  'txt', rnd='.001')
    tab.column_append_from_files('fb', 'f1b', fitbase, prefix, 
                                 dt_type, tag,  'txt', rnd='.0001')
    tab.column_append_from_files('sa', 's1a',  fitbase, prefix, 
                                 dt_type, tag,  'txt', rnd='.01')
    tab.column_append_from_files('sb', 's1b',  fitbase, prefix, 
                                 dt_type, tag,  'txt', rnd='.01')


    tab.output(tabname, test=opts.test)
    
    
