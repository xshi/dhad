"""
Module for plotting selected events

"""

import os
import sys
import attr
import tools
import ROOT 
import evt
from yld import parse_args
from tools import add_rootfile, get_rootfile, parse_opts_set
from tools import canvas_output, get_modekey_sign, get_modekey
from tools.filetools import UserFile

from sel.var import get_evtfile 
from sel.kkmass import get_evtfile as get_evtfile_kkmass


__author__ = "Xin Shi <xs32@cornell.edu>"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2005-2011 Xin Shi"
__license__ = "GPL"
__revision__ = "$Revision$"


def main(opts, args):
    tools.set_root_style()
    figname = 'evt_'+'_'.join(args).replace('/', '_')
    function = getattr(evt, args[0])
    return function(opts, args[1:], figname)


def kkmass(opts, args, figname):
    var = 'kkmass'
    parsed = parse_args(args)
    datatype = parsed[0]
    tag = parsed[1]
    modes = parsed[2]
    label = parsed[3]

    if len(modes) > 1:
        raise ValueError(modes, 'Only handle one mode at this time!')

    mode = modes[0]

    if ',' in datatype:
        datatypes = datatype.split(',')
    else:
        datatypes = [datatype]

    hist_list = []
    nBins = 100
    Xmin = 0.9
    Xmax = 1.8

    labels = [label, label]
    hist_names = ['Signal MC', 'Data']

    modekey, sign = get_modekey_sign(mode)
    modename = attr.modes[modekey]['uname']
    hist_title = 'KK mass in %s' %modename
    for datatype, hist_name in zip(datatypes, hist_names):
        hist = ROOT.TH1D(hist_name, hist_title, nBins, Xmin, Xmax)
        evtfile = get_evtfile_kkmass(datatype, mode, label, var, test=opts.test)
        f = open(evtfile, 'r')

        for line in f:
            kkmass = float(line.split()[2])
            hist.Fill(kkmass)

        hist_list.append(hist)

    xtitle = 'M(K^{+}K^{-}) (GeV/c^{2})'

    legend = ROOT.TLegend(0.66, 0.8, 0.9, 0.9)
    canvas = tools.draw_hist(hist_list, xtitle, legend, reverse=True)

    canvas_output(canvas, figname, label, opts.test)
    hist.Delete()


def kpimass(opts, args, figname):
    var = 'kpimass'
    parsed = parse_args(args)
    datatype = parsed[0]
    tag = parsed[1]
    modes = parsed[2]
    label = parsed[3]

    if len(modes) > 1:
        raise ValueError(modes, 'Only handle one mode at this time!')

    mode = modes[0]

    if ',' in datatype:
        datatypes = datatype.split(',')
    else:
        datatypes = [datatype]

    hist_list = []
    nBins = 100
    Xmin = 0.5
    Xmax = 1.5

    labels = [label, label]
    hist_names = ['Signal MC', 'Data']

    modekey, sign = get_modekey_sign(mode)
    modename = attr.modes[modekey]['uname']
    hist_title = 'K^{-} #pi^{+} mass in %s' %modename
    for datatype, hist_name in zip(datatypes, hist_names):
        hist = ROOT.TH1D(hist_name, hist_title, nBins, Xmin, Xmax)
        evtfile = get_evtfile_kkmass(datatype, mode, label, var, test=opts.test)
        f = open(evtfile, 'r')

        for line in f:
            kpimass = float(line.split()[2])
            hist.Fill(kpimass)

        hist_list.append(hist)

    xtitle = 'M(K^{+}#pi^{-}) (GeV/c^{2})'

    legend = ROOT.TLegend(0.1, 0.8, 0.3, 0.9)
    canvas = tools.draw_hist(hist_list, xtitle, legend, reverse=True)

    canvas_output(canvas, figname, label, opts.test, outputhtml=False)
    hist.Delete()

    
def mass_kk(opts, args, figname):
    var = 'mass_kk'
    parsed = parse_args(args)
    datatype = parsed[0]
    tag = parsed[1]
    modes = parsed[2]
    label = parsed[3]

    if len(modes) > 1:
        raise ValueError(modes, 'Only handle one mode at this time!')

    mode = modes[0]

    if ',' in datatype:
        datatypes = datatype.split(',')
    else:
        datatypes = [datatype]

    hist_list = []
    nBins = 100
    Xmin = 0
    Xmax = 2

    labels = [label, label]
    hist_names = ['Signal MC', 'Data']
    
    modekey, sign = get_modekey_sign(mode)
    modename = attr.modes[modekey]['uname']
    hist_title = 'KK mass in %s' %modename
    for datatype, hist_name in zip(datatypes, hist_names):
        hist = ROOT.TH1D(hist_name, hist_title, nBins, Xmin, Xmax)
        evtfile = get_evtfile(datatype, mode, label, var, test=opts.test)
    
        f = open(evtfile, 'r')
        
        for line in f:
            kkmass = float(line)
            hist.Fill(kkmass)

        hist_list.append(hist)


    xtitle = 'M(K^{+}K^{-}) (GeV/c^{2})'

    legend = ROOT.TLegend(0.66, 0.8, 0.9, 0.9)
    canvas = tools.draw_hist(hist_list, xtitle, legend)

    canvas_output(canvas, figname, label, opts.test)
    hist.Delete()
