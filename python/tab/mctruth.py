"""
Module for making tables from MC Truth info

"""

import os
import sys
import tools
import attr
import yld
from attr.modes import modes as dmodes
from attr.modes import mcdmode_to_dmodename, mcdbmode_to_dmodename
from tools import DHadTable, get_orgname_from_fname
from sel.var import get_evtfile

__author__ = "Xin Shi <xs32@cornell.edu>"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2005-2011 Xin Shi"
__license__ = "GPL"
__revision__ = "$Revision$"


def main(opts, args):

    if args[0] == 'names':
        return mctruth_names(opts, args[1:])
    
    tabname = 'mctruth_' + '_'.join(args).replace('/', '_')
    debug = opts.debug
    test = opts.test

    parsed = yld.parse_args(args)
    datatype  = parsed[0]
    tag       = parsed[1]
    modes     = parsed[2]
    label     = parsed[3]

    if args[0] == 'generic':
        return mctruth_generic_ddbar(tabname, datatype,
                                tag, modes, label, test, debug)
    else:
        raise NameError(args)
    

def mctruth_ddbar_single_mode(datatype, mode, label, ranges, test):
    var = 'mctruth'
    mctruthfile = get_evtfile(datatype, mode, label, var)

    if test:
        sys.stdout.write('\ntest: mctruthfile %s\n' % mctruthfile)

    modename = mode.replace('Single_', '')
    mctruthtable = get_mctruth_tab_link(datatype, mode, label)
    result = [modename, mctruthtable]
    tab = DHadTable(mctruthfile)
    result.extend(tab.column_analyze('Number', ranges))
    return result


def mctruth_generic_ddbar(tabname, datatype, tag, modes, label, test, debug):
    ranges = ['>0', '>50', '>100', '>200', '>500',
                  '>1000', '>2000', '>3000']

    tab = DHadTable()
    row = ['Mode', 'MC Truth']
    row.extend(ranges)
    tab.row_append(row)

    for mode in modes:
        new_row = mctruth_ddbar_single_mode(datatype, mode, label, ranges, test)
        tab.row_append(new_row)

    tab.output(tabname, test=test)

    
def mctruth_names(opts, args):
    debug_ = opts.debug
    test_ = opts.test
    set_ = opts.set

    prefix = None
    if args[0] == 'peak':
        prefix = 'peak'
        args = args[1:]
    
    parsed = yld.parse_args(args)
    datatype  = parsed[0]
    tag       = parsed[1]
    modes     = parsed[2]
    label     = parsed[3]

    limit = None
    if set_ != None and 'min' in set_:
        min_ = set_.split('=')[1]
        limit = '>%s' %min_

    mctruthmodes = 50
    if set_ != None and 'mctruthmodes' in set_:
        mctruthmodes = int(set_.split('=')[1])

    for mode in modes:
        tabname = 'mctruth_names_%s_%s_%s'  %(
            datatype, mode, label)
        if prefix != None:
            tabname = 'mctruth_names_%s_%s_%s_%s' %(
                prefix, datatype, mode, label)
        tabname = tabname.replace('/', '_')

        tab = DHadTable()
        modename = get_orgname_from_fname(mode)
        mctruth_names, mctruth_numbers = mctruth_names_single_mode(
            datatype, mode, label, limit, mctruthmodes, debug_, prefix)

        tab.column_append(mctruth_names, title='MC Truth for %s' %modename)
        tab.column_append(mctruth_numbers, title='Number of Events')
        tab.sort_by_column('Number of Events', reverse=True)

        orgfooter = ': '+sys.argv[0].split('/')[-1]+\
                    ' tab mctruth names %s %s %s ' %(
            datatype, mode, label)
        if prefix != None:
            orgfooter = ': '+sys.argv[0].split('/')[-1]+\
                        ' tab mctruth names %s %s %s %s ' %(
                prefix, datatype, mode, label)
        
        tab.output(tabname, orgfooter=orgfooter, test=test_)


def mctruth_names_single_mode(datatype, mode, label, limit, mctruthmodes,
                          debug, prefix=None):
    var = 'mctruth'
    mctruthfile = get_evtfile(datatype, mode, label, var)

    if debug:
        sys.stdout.write('\ndebug: mctruthfile %s\n' %mctruthfile)

    tab = DHadTable(mctruthfile, evalcell=True)
    tab.sort_by_column('Number', reverse=True)

    if limit != None:
        mcddbars = tab.column_get('Mode', 'Number'+limit)[1:]

    if mctruthmodes != None:
        mcddbars = tab.column_get('Mode')[1:mctruthmodes+1]

    numbers = tab.column_get('Number')[1:len(mcddbars)+1]

    mcddbarmodenames = mcddbars_to_modenames(mcddbars)

    return mcddbarmodenames, numbers 


def mcddbars_to_modenames(mcddbars):
    modenames = []
    for mcddbar in mcddbars:
        mcdmode = mcddbar[0]
        mcdbmode = mcddbar[1]
        dmodename = mcdmode_to_dmodename(mcdmode)
        dbmodename = mcdbmode_to_dmodename(mcdbmode)
        modenames.append('%s, %s' %(dmodename, dbmodename))
    return modenames


def make_overview_table(tabname, datatype, modes, label, test=False):
    tab = DHadTable()
    tab.row_append(['Mode', 'Backgrounds'])
    for mode in modes:
        modename = mode.replace('Single_', '')
        mctruthtable = get_mctruth_tab_link(datatype, mode, label)
        line = [modename, mctruthtable]
        tab.row_append(line)
    tab.output(tabname, test=test)


def get_mctruth_tab_link(datatype, mode, label):
    tab_name = 'mctruth_names_%s_%s_%s' %(datatype, mode, label)
    tab_name = tab_name.replace('/', '_')
    tablink = '[[./%s.org][table]]' % tab_name
    return tablink


