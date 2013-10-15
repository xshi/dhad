"""
Script for Branching Fraction related tables

"""

import os
import sys

import attr
import brf
import tools
from tools import DHadTable
from tools.filetools import UserFile
from attr.modes import modes


__author__ = "Xin Shi <xs32@cornell.edu>"
__revision__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2010-2011 Xin Shi"
__license__ = "GNU GPL"


def main(opts, args):
    function = getattr(brf, args[0])
    return function(opts, args[1:])


def yields_and_efficiencies(opts, args):
    label = args[0]
    prefix = 'dir_'+label
    
    yldfile = tools.set_file(extbase=attr.brfpath, prefix=prefix, 
                             comname='yields_and_efficiencies')
    
    f = UserFile()

    single_modes = [(pair, sign) for pair in modes for sign in [-1, 1]]

    input_label = label
    if '.' in label:
        input_label = label.split('.')[0]
        
    prefix='dir_'+input_label+'/crossfeeds'

    dt_type = 'signal'
    for x in single_modes:
        if x[1] == 1:
            uname = modes[x[0]]['uname']
            fname = modes[x[0]]['fname']
        else:
            uname = modes[x[0]]['unamebar']
            fname = modes[x[0]]['fnamebar']

        txtname = '%s_Single_%s_fakes_Single_%s.txt' % (dt_type, fname, fname)
        txtfile  = tools.set_file(extbase=attr.fitpath, prefix=prefix, comname=txtname)

        tab = DHadTable(txtfile)

        entries = tab.cell_get('entries', 'Value')
        entries = tab.cell_trim(entries, rnd='1')

        yld = tab.cell_get('yield', 'Value')
        yld = tab.cell_trim(yld, rnd='.000001')
        
        ratio = tab.cell_get('ratio', 'Value')
        ratio = tab.cell_trim(ratio, rnd='.000001')

        f.data.append('%s: %s %s %s\n' % (fname, entries, yld, ratio))
        
    for x, y  in [(x, y) for x in single_modes for y in single_modes if x!=y]:
        if x[1] == 1:
            uname = modes[x[0]]['uname']
            fname = modes[x[0]]['fname']
        else:
            uname = modes[x[0]]['unamebar']
            fname = modes[x[0]]['fnamebar']
        if y[1] == 1:
            unameb = modes[y[0]]['uname']
            fnameb = modes[y[0]]['fname']
        else:
            unameb = modes[y[0]]['unamebar']
            fnameb = modes[y[0]]['fnamebar']

        txtname = '%s_Single_%s_fakes_Single_%s.txt' % (dt_type, fname, fnameb)
        txtfile  = tools.set_file(extbase=attr.fitpath, prefix=prefix, comname=txtname)

        tab = DHadTable(txtfile)

        entries = tab.cell_get('entries', 'Value')
        entries = tab.cell_trim(entries, rnd='1')

        yld = tab.cell_get('yld', 'Value')
        ylderr = tab.cell_get('yld', 'Error')
        
        try:
            float(yld)/float(ylderr)
        except:
            sys.stdout.write('The original ylderr is %s, set to 1.0e10.\n' % ylderr)
            ylderr = 1.0e10
            
        yldsigma = str(float(yld)/float(ylderr))
        yldsigma = tab.cell_trim(yldsigma, rnd='.000001')
        
        yld = tab.cell_trim(yld, rnd='.000001')

        ratio = str(float(yld)/float(entries))
        ratio = tab.cell_trim(ratio, rnd='.000001')

        ratioerr = str(float(ylderr)/float(entries))
        ratioerr = tab.cell_trim(ratioerr, rnd='.000001')

        f.data.append('%s fakes %s: %s %s %s %s %s\n' % (
            fname, fnameb, yldsigma, entries, yld, ratio, ratioerr))
       
    f.output(yldfile, verbose=1)
    return yldfile
