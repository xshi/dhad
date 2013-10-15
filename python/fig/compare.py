"""
Module for Comparing Figures 

"""

import os
import sys
import tools
import attr

from tools.filetools import UserFile
from tools import DHadTable, get_modekey, parse_opts_set, \
     canvas_output, set_root_style
     
from yld import parse_args
from array import array
import operator
from ROOT import TGraphAsymmErrors, TCanvas, TPad, TGraph, TLegend, kRed, kBlue
import compare 
import simplejson as json 

__author__ = "Xin Shi <xs32@cornell.edu>"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2005-2011 Xin Shi"
__license__ = "GPL"
__revision__ = "$Revision$"


def main(opts, args):
    set_root_style()
    figname = '_'.join(args[:-1]).replace('/', '_')
    figname = figname.replace(',', '_')

    function = getattr(compare, args[0])
    return function(opts, args[1:], figname)


def kkmass0_old(opts, args):
    parsed = parse_args(args)
    datatype  = parsed[0]
    tag       = parsed[1]
    modes     = parsed[2]
    label     = parsed[3]

    mode = modes[0]
    modekey = tools.get_modekey(mode)

    binbase = parse_opts_set(opts.set, 'binbase')
    binwidth =  parse_opts_set(opts.set, 'binwidth')
    numbins = parse_opts_set(opts.set, 'numbins')

    figname = 'kkmass0_'+'_'.join(args[:-1]).replace('/', '_')
    figname = figname.replace(',', '_')+'.eps'
    epsfile = os.path.join(attr.figpath, label, figname)
    
    fullrangedata = {}
    init_dict(fullrangedata)

    fullrangemc = {}
    init_dict(fullrangemc)

    evtpath = os.path.join(attr.datpath, 'sel', label, 'kkmass')
    evtfiledata = tools.set_file('evt', 'data', modekey, tag,  prefix='',
                                 forceCombine=1, extbase=evtpath)
    
    evtfilemc = tools.set_file('evt', 'signal', modekey, tag,  prefix='',
                               forceCombine=1, extbase=evtpath)
    for i in xrange(numbins):
        lowmass = binbase+i*binwidth
        highmass = binbase+(i+1)*binwidth
        
        parse_evtfile(evtfiledata, lowmass, highmass, fullrangedata)
        parse_evtfile(evtfilemc, lowmass, highmass, fullrangemc)

    scaledict(fullrangedata, 1/sumdict(fullrangedata))
    
    scaledict(fullrangemc, 1/sumdict(fullrangemc))

    gdata = TGraph(len(fullrangedata['x']),
                   getarray('x', fullrangedata),
                   getarray('y', fullrangedata))

    gmc = TGraph(len(fullrangemc['x']),
                 getarray('x', fullrangemc),
                 getarray('y', fullrangemc))

    c1 = TCanvas('c','kk',600,600)
    c1.SetLeftMargin(0.15)
    c1.SetRightMargin(0.05)
    c1.SetBottomMargin(0.15)
    c1.SetTopMargin(0.05)
    #hr = c1.DrawFrame(0.95, 0.0, 1.95, 0.12)
    hr = c1.DrawFrame(0.9, 0.0, 1.8, 0.1)
    hr.GetYaxis().SetTitle('Yield (arbitrary units)')
    hr.GetXaxis().SetTitle('M(K^{-} K^{+}) (GeV/#font[72]{c}^{2})')
    hr.GetYaxis().SetTitleOffset(1.4)
    hr.GetYaxis().SetTitleSize(0.05)
    hr.GetXaxis().SetTitleOffset(1.3)
    hr.GetXaxis().SetTitleSize(0.05)
    gmc.SetMarkerStyle(21)
    gmc.SetMarkerColor(kRed)
    gmc.SetMarkerSize(0.6)
    gmc.SetLineColor(kRed)
    gmc.Draw("PL")
    gdata.SetMarkerStyle(20)
    gdata.SetMarkerColor(kBlue)
    gdata.SetMarkerSize(0.6)
    gdata.Draw("P")
    leg = TLegend(0.6, 0.75, 0.95, 0.95)
    leg.AddEntry(gdata, 'Data', 'pl')
    leg.AddEntry(gmc, 'MC', 'pl')
    leg.Draw()
    c1.Print(epsfile)
    eps2pdf(epsfile)


def kkmass(opts, args):
    parsed = parse_args(args)
    datatype  = parsed[0]
    tag       = parsed[1]
    modes     = parsed[2]
    label     = parsed[3]

    mode = modes[0]
    modekey = tools.get_modekey(mode)

    binbase = parse_opts_set(opts.set, 'binbase')
    binwidth =  parse_opts_set(opts.set, 'binwidth')
    numbins = parse_opts_set(opts.set, 'numbins')

    fullrangedata = {}
    init_dict(fullrangedata)

    fullrangemc = {}
    init_dict(fullrangemc)
    
    for i in xrange(numbins):
        lowmass = binbase+i*binwidth
        highmass = binbase+(i+1)*binwidth

        prefix = 'dir_%s/kkmass/%s_%s' % (label, lowmass, highmass)
        
        datafile = tools.set_file('txt', 'data', modekey, tag,
                                  prefix=prefix, extbase=attr.fitpath)

        mcfile = tools.set_file('txt', 'signal', modekey, tag,
                                prefix=prefix, extbase=attr.fitpath)

        if os.access(datafile, os.F_OK) and os.access(mcfile, os.F_OK):
            parsefile(datafile, lowmass, highmass, fullrangedata)
            parsefile(mcfile, lowmass, highmass, fullrangemc)


    scaledict(fullrangedata, 1/sumdict(fullrangedata))
    scaledict(fullrangemc, 1/sumdict(fullrangemc))


    gdata = TGraphAsymmErrors(len(fullrangedata['x']),
                              getarray('x', fullrangedata),
                              getarray('y', fullrangedata),
                              getarray('exl', fullrangedata),
                              getarray('exh', fullrangedata),
                              getarray('eyl', fullrangedata),
                              getarray('eyh', fullrangedata))

    gmc = TGraph(len(fullrangemc['x']),
                 getarray('x', fullrangemc),
                 getarray('y', fullrangemc))

    c1 = TCanvas('c','kk',600,600)
    c1.SetLeftMargin(0.15)
    c1.SetRightMargin(0.05)
    c1.SetBottomMargin(0.15)
    c1.SetTopMargin(0.05)
    #hr = c1.DrawFrame(0.95, 0.0, 1.95, 0.12)
    hr = c1.DrawFrame(0.9, 0.0, 1.8, 0.1)
    hr.GetYaxis().SetTitle('Yield (arbitrary units)')
    hr.GetXaxis().SetTitle('M(K^{-} K^{+}) (GeV/#font[72]{c}^{2})')
    hr.GetYaxis().SetTitleOffset(1.4)
    hr.GetYaxis().SetTitleSize(0.05)
    hr.GetXaxis().SetTitleOffset(1.3)
    hr.GetXaxis().SetTitleSize(0.05)
    gmc.SetMarkerStyle(21); gmc.SetMarkerColor(kRed); gmc.SetMarkerSize(0.6)
    gmc.SetLineColor(kRed)
    gmc.Draw("PL")
    gdata.SetMarkerStyle(20); gdata.SetMarkerColor(kBlue); gdata.SetMarkerSize(0.6)
    gdata.Draw("P")
    leg = TLegend(0.6, 0.75, 0.95, 0.95)
    leg.AddEntry(gdata, 'Data', 'pl')
    leg.AddEntry(gmc, 'MC', 'pl')
    leg.Draw()
    c1.Print('comparison.eps')
    eps2pdf('comparison.eps')


def kkmass2(opts, args):
    parsed = parse_args(args)
    datatype  = parsed[0]
    tag       = parsed[1]
    modes     = parsed[2]
    label     = parsed[3]

    mode = modes[0]
    modekey = tools.get_modekey(mode)

    binbase = parse_opts_set(opts.set, 'binbase')
    binwidth =  parse_opts_set(opts.set, 'binwidth')
    numbins = parse_opts_set(opts.set, 'numbins')

    fullrangedata = {}
    init_dict(fullrangedata)

    fullrangemc = {}
    init_dict(fullrangemc)

    evtpath = os.path.join(attr.datpath, 'sel', label, 'kkmass')
    evtfilemc = tools.set_file('evt', 'signal', modekey, tag,  prefix='',
                               forceCombine=1, extbase=evtpath)

    for i in xrange(numbins):
        lowmass = binbase+i*binwidth
        highmass = binbase+(i+1)*binwidth

        prefix = 'dir_%s/kkmass/%s_%s' % (label, lowmass, highmass)
        
        datafile = tools.set_file('txt', 'data', modekey, tag,
                                  prefix=prefix, extbase=attr.fitpath)

        #mcfile = tools.set_file('txt', 'signal', modekey, tag,
        #                        prefix=prefix, extbase=attr.fitpath)

        if os.access(datafile, os.F_OK): # and os.access(mcfile, os.F_OK):
            parsefile(datafile, lowmass, highmass, fullrangedata)
            parse_evtfile(evtfilemc, lowmass, highmass, fullrangemc)
            
        else:
            sys.stdout.write('Skipped %s %s ...\n' % (lowmass, highmass))


    scaledict(fullrangedata, 1/sumdict(fullrangedata))
    
    scaledict(fullrangemc, 1/sumdict(fullrangemc))

    gdata = TGraphAsymmErrors(len(fullrangedata['x']),
                              getarray('x', fullrangedata),
                              getarray('y', fullrangedata),
                              getarray('exl', fullrangedata),
                              getarray('exh', fullrangedata),
                              getarray('eyl', fullrangedata),
                              getarray('eyh', fullrangedata))

    gmc = TGraph(len(fullrangemc['x']),
                 getarray('x', fullrangemc),
                 getarray('y', fullrangemc))

    c1 = TCanvas('c','kk',600,600)
    c1.SetLeftMargin(0.15)
    c1.SetRightMargin(0.05)
    c1.SetBottomMargin(0.15)
    c1.SetTopMargin(0.05)
    #hr = c1.DrawFrame(0.95, 0.0, 1.95, 0.12)
    hr = c1.DrawFrame(0.9, 0.0, 1.8, 0.1)
    hr.GetYaxis().SetTitle('Yield (arbitrary units)')
    hr.GetXaxis().SetTitle('M(K^{-} K^{+}) (GeV/#font[72]{c}^{2})')
    hr.GetYaxis().SetTitleOffset(1.4)
    hr.GetYaxis().SetTitleSize(0.05)
    hr.GetXaxis().SetTitleOffset(1.3)
    hr.GetXaxis().SetTitleSize(0.05)
    gmc.SetMarkerStyle(21); gmc.SetMarkerColor(kRed); gmc.SetMarkerSize(0.6)
    gmc.SetLineColor(kRed)
    gmc.Draw("PL")
    gdata.SetMarkerStyle(20); gdata.SetMarkerColor(kBlue); gdata.SetMarkerSize(0.6)
    gdata.Draw("P")
    leg = TLegend(0.6, 0.75, 0.95, 0.95)
    leg.AddEntry(gdata, 'Data', 'pl')
    leg.AddEntry(gmc, 'MC', 'pl')
    leg.Draw()
    c1.Print('comparison.eps')
    eps2pdf('comparison.eps')


def init_dict(indict):
    indict['x'] = []
    indict['exl'] = []
    indict['exh'] = []
    indict['y'] = []
    indict['eyl'] = []
    indict['eyh'] = []


def parsefile(f, lowmass, highmass, indict):
    x0 = lowmass
    x1 = highmass
    xc = (x0 + x1)/2.

    tab     = DHadTable(f)
    N1      = float(tab.cell_get('N1', 'Value'))
    N2      = float(tab.cell_get('N2', 'Value'))

    if N1 > 1000 or N2 > 1000 :
        return

    indict['x'].append(xc)
    indict['exl'].append(xc-x0)
    indict['exh'].append(x1-xc)

    N = N1 + N2
    
    err_low_N1 = float(tab.cell_get('N1', 'Low'))
    err_low_N2 = float(tab.cell_get('N2', 'Low'))

    err_low = (err_low_N1**2 + err_low_N2**2)**.5

    err_high_N1 = float(tab.cell_get('N1', 'High'))
    err_high_N2 = float(tab.cell_get('N2', 'High'))
    err_high = (err_high_N1**2 + err_high_N2**2)**.5

    yc = float(N)
    yl = float(err_low)
    yh = float(err_high)

    indict['y'].append(yc)
    indict['eyl'].append(yl)
    indict['eyh'].append(yh)


def sumdict(indict):
    return reduce(operator.add, [y for y in indict['y'] if y > -30])

def scaledict(indict, scale):
    for l in ('y', 'eyl', 'eyh'):
        for i in xrange(len(indict[l])):
            indict[l][i] *= scale

def getarray(code, indict):
    return array('d', indict[code])


def parse_evtfile(f, lowmass, highmass, indict):
    f = open(f, 'r')
    
    total = 0
    selected = 0 
    for line in f:
        total += 1
        kkmass = float(line.split()[2])
        if kkmass > lowmass and kkmass < highmass:
            selected += 1 
    f.close()
    sys.stdout.write('Range %s - %s : selected %s out of %s \n' %(
        lowmass, highmass, selected, total))

    x0 = lowmass
    x1 = highmass
    xc = (x0 + x1)/2.

    indict['x'].append(xc)
    indict['exl'].append(xc-x0)
    indict['exh'].append(x1-xc)

    N = float(selected)

    indict['y'].append(N)

    
def kpimass0(opts, args, figname):
    parsed = parse_args(args)
    datatype  = parsed[0]
    tag       = parsed[1]
    modes     = parsed[2]
    label     = parsed[3]

    mode = modes[0]
    modekey = tools.get_modekey(mode)

    binbase = parse_opts_set(opts.set, 'binbase')
    binwidth =  parse_opts_set(opts.set, 'binwidth')
    numbins = parse_opts_set(opts.set, 'numbins')

    dbfile = os.path.join(attr.figpath, label, figname+'.db')

    fullrangedata, fullrangemc = get_fullrange_data_mc(
        opts, dbfile, label, 'kpimass',  modekey, tag, binbase, binwidth, numbins)

    scaledict(fullrangedata, 1/sumdict(fullrangedata))
    
    scaledict(fullrangemc, 1/sumdict(fullrangemc))

    gdata = TGraph(len(fullrangedata['x']),
                   getarray('x', fullrangedata),
                   getarray('y', fullrangedata))

    gmc = TGraph(len(fullrangemc['x']),
                 getarray('x', fullrangemc),
                 getarray('y', fullrangemc))

    c1 = TCanvas('c','kpi', 600, 600)
    c1.SetLeftMargin(0.15)
    c1.SetRightMargin(0.05)
    c1.SetBottomMargin(0.15)
    c1.SetTopMargin(0.05)
    hr = c1.DrawFrame(0.5, 0.0, 1.5, 0.04)
    hr.GetYaxis().SetTitle('Yield (arbitrary units)')
    hr.GetXaxis().SetTitle('M(K^{-} #pi^{+}) (GeV/#font[72]{c}^{2})')
    hr.GetYaxis().SetTitleOffset(1.4)
    hr.GetYaxis().SetTitleSize(0.05)
    hr.GetXaxis().SetTitleOffset(1.3)
    hr.GetXaxis().SetTitleSize(0.05)
    gmc.SetMarkerStyle(21)
    gmc.SetMarkerColor(kRed)
    gmc.SetMarkerSize(0.6)
    gmc.SetLineColor(kRed)
    gmc.Draw("PL")
    gdata.SetMarkerStyle(20)
    gdata.SetMarkerColor(kBlue)
    gdata.SetMarkerSize(0.6)
    gdata.Draw("P")
    leg = TLegend(0.6, 0.75, 0.95, 0.95)
    leg.AddEntry(gdata, 'Data', 'pl')
    leg.AddEntry(gmc, 'MC', 'pl')
    leg.Draw()
    canvas_output(c1, figname, label, opts.test)

    
def get_fullrange_data_mc(opts, dbfile, label, evtdir, modekey, tag,
                          binbase, binwidth, numbins):
    dbmode = parse_opts_set(opts.set, 'dbmode')
    if os.access(dbfile, os.F_OK) and dbmode == None:
        db = open(dbfile)
        fullrangedata, fullrangemc  = json.load(db)
        return fullrangedata, fullrangemc

    if dbmode == None:
        dbmode = 'w'
        
    db = open(dbfile, dbmode)

    fullrangedata = {}
    init_dict(fullrangedata)

    fullrangemc = {}
    init_dict(fullrangemc)

    evtpath = os.path.join(attr.datpath, 'sel', label, evtdir)
    evtfiledata = tools.set_file('evt', 'data', modekey, tag,  prefix='',
                             forceCombine=1, extbase=evtpath)

    evtfilemc = tools.set_file('evt', 'signal', modekey, tag,  prefix='',
                               forceCombine=1, extbase=evtpath)
    
    for i in xrange(numbins):
        lowmass = binbase+i*binwidth
        highmass = binbase+(i+1)*binwidth
        
        parse_evtfile(evtfiledata, lowmass, highmass, fullrangedata)
        parse_evtfile(evtfilemc, lowmass, highmass, fullrangemc)


    json.dump((fullrangedata,fullrangemc), db)
    db.close()

    sys.stdout.write('Save db as: %s \n' % dbfile)

    return fullrangedata, fullrangemc



def kpimass1(opts, args, figname):
    parsed = parse_args(args)
    datatype  = parsed[0]
    tag       = parsed[1]
    modes     = parsed[2]
    label     = parsed[3]

    mode = modes[0]
    modekey = tools.get_modekey(mode)

    binbase = parse_opts_set(opts.set, 'binbase')
    binwidth =  parse_opts_set(opts.set, 'binwidth')
    numbins = parse_opts_set(opts.set, 'numbins')
    nohtml = parse_opts_set(opts.set, 'nohtml')

    if nohtml == None:
        outputhtml = True
    else:
        outputhtml = False

    dbfile = os.path.join(attr.figpath, label, figname+'.db')

    alldata, fullrangemc = get_fullrange_data_mc(
        opts, dbfile, label, 'kpimass',  modekey, tag, binbase, binwidth, numbins)

    fullrangedata = {}
    init_dict(fullrangedata)

    evtpath = os.path.join(attr.datpath, 'sel', label, 'kpimass')
    evtfilemc = tools.set_file('evt', 'signal', modekey, tag,  prefix='',
                               forceCombine=1, extbase=evtpath)

    for i in xrange(numbins):
        lowmass = binbase+i*binwidth
        highmass = binbase+(i+1)*binwidth
        prefix = 'dir_%s/kpimass/%s_%s' % (label, lowmass, highmass)
        datafile = tools.set_file('txt', 'data', modekey, tag,
                                  prefix=prefix, extbase=attr.fitpath)

        if os.access(datafile, os.F_OK):
            parsefile(datafile, lowmass, highmass, fullrangedata)
            
        else:
            sys.stdout.write('Skipped %s %s ...\n' % (lowmass, highmass))

    scaledict(fullrangedata, 1/sumdict(fullrangedata))
    
    scaledict(fullrangemc, 1/sumdict(fullrangemc))

    gdata = TGraphAsymmErrors(len(fullrangedata['x']),
                              getarray('x', fullrangedata),
                              getarray('y', fullrangedata),
                              getarray('exl', fullrangedata),
                              getarray('exh', fullrangedata),
                              getarray('eyl', fullrangedata),
                              getarray('eyh', fullrangedata))

    gmc = TGraph(len(fullrangemc['x']),
                 getarray('x', fullrangemc),
                 getarray('y', fullrangemc))

    c1 = TCanvas('c','kpi', 600, 600)
    c1.SetLeftMargin(0.15)
    c1.SetRightMargin(0.05)
    c1.SetBottomMargin(0.15)
    c1.SetTopMargin(0.05)
    hr = c1.DrawFrame(0.5, 0.0, 1.5, 0.04)
    hr.GetYaxis().SetTitle('Yield (arbitrary units)')
    hr.GetXaxis().SetTitle('M(K^{-} #pi^{+}) (GeV/#font[72]{c}^{2})')
    hr.GetYaxis().SetTitleOffset(1.4)
    hr.GetYaxis().SetTitleSize(0.05)
    hr.GetXaxis().SetTitleOffset(1.3)
    hr.GetXaxis().SetTitleSize(0.05)
    gmc.SetMarkerStyle(21); gmc.SetMarkerColor(kRed); gmc.SetMarkerSize(0.6)
    gmc.SetLineColor(kRed)
    gmc.Draw("PL")
    gdata.SetMarkerStyle(20); gdata.SetMarkerColor(kBlue); gdata.SetMarkerSize(0.6)
    gdata.Draw("P")
    leg = TLegend(0.6, 0.75, 0.92, 0.92)
    leg.AddEntry(gdata, 'Data', 'pl')
    leg.AddEntry(gmc, 'MC', 'pl')
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
    leg.Draw()
    canvas_output(c1, figname, label, opts.test, outputhtml=outputhtml)


# ------------------
# Redo kkmass
# ------------------

def kkmass0(opts, args, figname):
    parsed = parse_args(args)
    datatype  = parsed[0]
    tag       = parsed[1]
    modes     = parsed[2]
    label     = parsed[3]

    mode = modes[0]
    modekey = tools.get_modekey(mode)

    binbase = parse_opts_set(opts.set, 'binbase')
    binwidth =  parse_opts_set(opts.set, 'binwidth')
    numbins = parse_opts_set(opts.set, 'numbins')
    nohtml = parse_opts_set(opts.set, 'nohtml')

    if nohtml == None:
        outputhtml = True
    else:
        outputhtml = False

    dbfile = os.path.join(attr.figpath, label, figname+'.db')

    fullrangedata, fullrangemc = get_fullrange_data_mc(
        opts, dbfile, label, 'kkmass', modekey, tag, binbase, binwidth, numbins)

    scaledict(fullrangedata, 1/sumdict(fullrangedata))
    
    scaledict(fullrangemc, 1/sumdict(fullrangemc))

    gdata = TGraph(len(fullrangedata['x']),
                   getarray('x', fullrangedata),
                   getarray('y', fullrangedata))

    gmc = TGraph(len(fullrangemc['x']),
                 getarray('x', fullrangemc),
                 getarray('y', fullrangemc))

    c1 = TCanvas('c','kk', 600, 600)
    c1.SetLeftMargin(0.15)
    c1.SetRightMargin(0.05)
    c1.SetBottomMargin(0.15)
    c1.SetTopMargin(0.05)
    hr = c1.DrawFrame(0.9, 0.0, 1.8, 0.1)
    hr.GetYaxis().SetTitle('Yield (arbitrary units)')
    hr.GetXaxis().SetTitle('M(K^{-} #pi^{+}) (GeV/#font[72]{c}^{2})')
    hr.GetYaxis().SetTitleOffset(1.4)
    hr.GetYaxis().SetTitleSize(0.05)
    hr.GetXaxis().SetTitleOffset(1.3)
    hr.GetXaxis().SetTitleSize(0.05)
    gmc.SetMarkerStyle(21)
    gmc.SetMarkerColor(kRed)
    gmc.SetMarkerSize(0.6)
    gmc.SetLineColor(kRed)
    gmc.Draw("PL")
    gdata.SetMarkerStyle(20)
    gdata.SetMarkerColor(kBlue)
    gdata.SetMarkerSize(0.6)
    gdata.Draw("P")
    leg = TLegend(0.6, 0.75, 0.95, 0.95)
    leg.AddEntry(gdata, 'Data', 'pl')
    leg.AddEntry(gmc, 'MC', 'pl')
    leg.Draw()
    canvas_output(c1, figname, label, opts.test,outputhtml=outputhtml)


def kkmass1(opts, args, figname):
    parsed = parse_args(args)
    datatype  = parsed[0]
    tag       = parsed[1]
    modes     = parsed[2]
    label     = parsed[3]

    mode = modes[0]
    modekey = tools.get_modekey(mode)

    binbase = parse_opts_set(opts.set, 'binbase')
    binwidth =  parse_opts_set(opts.set, 'binwidth')
    numbins = parse_opts_set(opts.set, 'numbins')
    nohtml = parse_opts_set(opts.set, 'nohtml')

    if nohtml == None:
        outputhtml = True
    else:
        outputhtml = False

    dbfile = os.path.join(attr.figpath, label, figname+'.db')

    alldata, fullrangemc = get_fullrange_data_mc(
        opts, dbfile, label, 'kkmass', modekey, tag, binbase, binwidth, numbins)

    fullrangedata = {}
    init_dict(fullrangedata)

    evtpath = os.path.join(attr.datpath, 'sel', label, 'kkmass')
    evtfilemc = tools.set_file('evt', 'signal', modekey, tag,  prefix='',
                               forceCombine=1, extbase=evtpath)

    for i in xrange(numbins):
        lowmass = binbase+i*binwidth
        highmass = binbase+(i+1)*binwidth
        prefix = 'dir_%s/kkmass/%s_%s' % (label, lowmass, highmass)
        datafile = tools.set_file('txt', 'data', modekey, tag,
                                  prefix=prefix, extbase=attr.fitpath)

        if os.access(datafile, os.F_OK):
            parsefile(datafile, lowmass, highmass, fullrangedata)
            
        else:
            sys.stdout.write('Skipped %s %s ...\n' % (lowmass, highmass))

    scaledict(fullrangedata, 1/sumdict(fullrangedata))
    
    scaledict(fullrangemc, 1/sumdict(fullrangemc))

    gdata = TGraphAsymmErrors(len(fullrangedata['x']),
                              getarray('x', fullrangedata),
                              getarray('y', fullrangedata),
                              getarray('exl', fullrangedata),
                              getarray('exh', fullrangedata),
                              getarray('eyl', fullrangedata),
                              getarray('eyh', fullrangedata))

    gmc = TGraph(len(fullrangemc['x']),
                 getarray('x', fullrangemc),
                 getarray('y', fullrangemc))

    c1 = TCanvas('c','kk', 600, 600)
    c1.SetLeftMargin(0.15)
    c1.SetRightMargin(0.05)
    c1.SetBottomMargin(0.15)
    c1.SetTopMargin(0.05)
    #hr = c1.DrawFrame(0.5, 0.0, 1.5, 0.04)
    hr = c1.DrawFrame(0.9, 0.0, 1.8, 0.1)
    hr.GetYaxis().SetTitle('Yield (arbitrary units)')
    hr.GetXaxis().SetTitle('M(K^{-} #pi^{+}) (GeV/#font[72]{c}^{2})')
    hr.GetYaxis().SetTitleOffset(1.4)
    hr.GetYaxis().SetTitleSize(0.05)
    hr.GetXaxis().SetTitleOffset(1.3)
    hr.GetXaxis().SetTitleSize(0.05)
    gmc.SetMarkerStyle(21); gmc.SetMarkerColor(kRed); gmc.SetMarkerSize(0.6)
    gmc.SetLineColor(kRed)
    gmc.Draw("PL")
    gdata.SetMarkerStyle(20); gdata.SetMarkerColor(kBlue); gdata.SetMarkerSize(0.6)
    gdata.Draw("P")
    leg = TLegend(0.6, 0.75, 0.92, 0.92)
    leg.AddEntry(gdata, 'Data', 'pl')
    leg.AddEntry(gmc, 'MC', 'pl')
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
    leg.Draw()
    canvas_output(c1, figname, label, opts.test, outputhtml=outputhtml)

