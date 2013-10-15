"""
Module for making tables from Backgrounds 

"""

import os
import sys
import tools
import attr
import yld
from attr.modes import modes as dmodes
from attr.modes import mcdmode_to_dmodename, mcdbmode_to_dmodename
from tools import DHadTable, get_orgname_from_fname

__author__ = "Xin Shi <xs32@cornell.edu>"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2005-2010 Xin Shi"
__license__ = "GPL"
__revision__ = "$Revision$"


def main(opts, args):

    if args[0] == 'names':
        return bkg_names(opts, args[1:])
    
    tabname = 'bkg_' + '_'.join(args).replace('/', '_')
    debug = opts.debug
    test = opts.test

    parsed = yld.parse_args(args)
    datatype  = parsed[0]
    tag       = parsed[1]
    modes     = parsed[2]
    label     = parsed[3]

    if args[0] == 'generic':
        return bkg_generic_ddbar(tabname, datatype,
                                 tag, modes, label, test, debug)
    elif args[0] == 'generic/cont':
        return bkg_generic_cont(tabname, datatype,
                                tag, modes, label, test, debug)
    elif args[0] == 'generic/ddbar':
        return bkg_generic_ddbar(tabname, datatype,
                                tag, modes, label, test, debug)

    tab = DHadTable()
    row = ['Mode', 'Number of DDbar Backgrounds',
           'Number of Continuum Backgrounds']
    tab.row_append(row)
    for mode in modes:
        modename = mode.replace('Single_', '')
        ddbarnum = get_bkg_total('generic/ddbar', mode, label, debug)
        contnum = get_bkg_total('generic/cont', mode, label, debug)
        row = [modename, ddbarnum, contnum]
        tab.row_append(row)

    tab.column_trim('Number of DDbar Backgrounds', rnd='1')
    tab.column_trim('Number of Continuum Backgrounds', rnd='1')
    tab.output(tabname, test=test)



def get_bkg_total(datatype, mode, label, debug):
    prefix = 'dir_'+label
    bkgname = '%s_%s.txt' %(datatype, mode)
    bkgname = bkgname.replace('/', '_')
    bkgfile = tools.set_file(
        extbase=attr.bkgpath(), prefix=prefix, comname=bkgname)
    if debug:
        sys.stdout.write('\ndebug: bkgfile %s\n' %bkgfile)
    tab = DHadTable(bkgfile)
    col = tab.column_get('Number')
    total = sum(col[1:])

    if 'ddbar' in datatype:
        factor = 20
    if 'cont' in datatype:
        factor = 5

    total = total/float(factor)
    return total
        

def bkg_ddbar_single_mode(datatype, mode, label, ranges, debug):
    prefix = 'dir_'+label
    bkgname = '%s_%s.txt' %(datatype, mode)
    bkgname = bkgname.replace('/', '_')
    bkgfile = tools.set_file(
        extbase=attr.bkgpath(), prefix=prefix, comname=bkgname)

    if debug:
        sys.stdout.write('\ndebug: bkgfile %s\n' %bkgfile)
    modename = mode.replace('Single_', '')
    bkgtable = get_bkg_tab_link(datatype, mode, label)
    result = [modename, bkgtable]
    tab = DHadTable(bkgfile)
    result.extend(tab.column_analyze('Number', ranges))
    return result


def bkg_generic_ddbar(tabname, datatype, tag, modes, label, test, debug):
    ranges = ['>0', '>50', '>100', '>200', '>500',
                  '>1000', '>2000', '>3000']

    tab = DHadTable()
    row = ['Mode', 'Backgrounds']
    row.extend(ranges)
    tab.row_append(row)

    for mode in modes:
        new_row = bkg_ddbar_single_mode(datatype, mode, label, ranges, debug)
        tab.row_append(new_row)

    tab.output(tabname, test=test)

    
def bkg_cont_single_mode(datatype, mode, label, debug):
    prefix = 'dir_'+label
    bkgname = '%s_%s.txt' %(datatype, mode)
    bkgname = bkgname.replace('/', '_')
    bkgfile = tools.set_file(
        extbase=attr.bkgpath(), prefix=prefix, comname=bkgname)
    if debug:
        sys.stdout.write('\ndebug: bkgfile %s\n' %bkgfile)
    modename = mode.replace('Single_', '')
    result = [modename]
    tab = DHadTable(bkgfile)
    result.extend(tab.column_get('Number')[1:])
    return result


def bkg_names(opts, args):
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

    bkgmodes = 20
    if set_ != None and 'bkgmodes' in set_:
        bkgmodes = int(set_.split('=')[1])

    for mode in modes:
        tabname = 'bkg_names_%s_%s_%s'  %(
            datatype, mode, label)
        if prefix != None:
            tabname = 'bkg_names_%s_%s_%s_%s' %(
                prefix, datatype, mode, label)
        tabname = tabname.replace('/', '_')

        tab = DHadTable()
        modename = get_orgname_from_fname(mode)
        bkg_names, bkg_numbers = bkg_names_single_mode(
            datatype, mode, label, limit, bkgmodes, debug_, prefix)
        tab.column_append(bkg_names, title='Backgrounds for %s' %modename)
        tab.column_append(bkg_numbers, title='Number of Events')
        tab.sort_by_column('Number of Events', reverse=True)

        orgfooter = ': '+sys.argv[0].split('/')[-1]+\
                    ' tab backgrounds names %s %s %s ' %(
            datatype, mode, label)
        if prefix != None:
            orgfooter = ': '+sys.argv[0].split('/')[-1]+\
                        ' tab backgrounds names %s %s %s %s ' %(
                prefix, datatype, mode, label)
        
        tab.output(tabname, orgfooter=orgfooter, test=test_)


def bkg_names_single_mode(datatype, mode, label, limit, bkgmodes,
                          debug, prefix=None):
    bkgname = '%s_%s.txt' %(datatype, mode)
    if prefix !=None:
        bkgname = '%s_%s_%s.txt' %(prefix, datatype, mode)
        
    bkgname = bkgname.replace('/', '_')
    bkgfile = tools.set_file(
        extbase=attr.bkgpath(), prefix='dir_'+label, comname=bkgname)
    if debug:
        sys.stdout.write('\ndebug: bkgfile %s\n' %bkgfile)

    tab = DHadTable(bkgfile, evalcell=True)
    tab.sort_by_column('Number', reverse=True)

    if limit != None:
        mcddbars = tab.column_get('Mode', 'Number'+limit)[1:]

    if bkgmodes != None:
        mcddbars = tab.column_get('Mode')[1:bkgmodes+1]

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
        bkgtable = get_bkg_tab_link(datatype, mode, label)
        line = [modename, bkgtable]
        tab.row_append(line)
    tab.output(tabname, test=test)


def get_bkg_tab_link(datatype, mode, label):
    tab_name = 'bkg_names_%s_%s_%s' %(datatype, mode, label)
    tab_name = tab_name.replace('/', '_')
    tablink = '[[./%s.org][table]]' % tab_name
    return tablink


def bkg_generic_cont(tabname, datatype, tag, modes,
                     label, test, debug):
    tab = DHadTable()
    row = ['Mode', 'Continuum Backgrounds']
    tab.row_append(row)
    for mode in modes:
        new_row = bkg_cont_single_mode(datatype, mode, label, debug)
        tab.row_append(new_row)

    tab.output(tabname, test=test)
