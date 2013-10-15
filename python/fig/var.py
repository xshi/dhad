"""
Module for plotting variables

"""

import os
import sys
import attr
import var
import ROOT
import tools 
from yld import parse_args
from tools import add_rootfile, get_rootfile, parse_opts_set, \
     canvas_output, get_modekey_sign, get_modekey, draw_hist
from tools.cuts import chooseD, invmass
from tools.filetools import UserFile
from math import sqrt
from sel.var import get_evtfile


__author__ = "Xin Shi <xs32@cornell.edu>"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2005-2011 Xin Shi"
__license__ = "GPL"
__revision__ = "$Revision$"


def main(opts, args):
    tools.set_root_style()
    figname = 'var_'+'_'.join(args).replace('/', '_')
    function = getattr(var, args[0])
    return function(opts, args[1:], figname)


def deltae(opts, args, figname):
    parsed = parse_args(args)
    datatype = parsed[0]
    tag = parsed[1]
    modes = parsed[2]
    label = parsed[3]

    alt_deltae = {'decutl': -1, 'decuth': 1}

    canvas = ROOT.TCanvas("aCanvas", "Canvas", 1000, 1000)
    canvas.Divide(3,3)

    deltae_hist = {}
    
    hist = ROOT.TH1F('deltae', 'DeltaE', 100, -0.1, 0.1) 
    pad = 1
    for mode in modes:
        frametitle = tools.get_mode_root_name(mode)
        canvas.cd(pad)
        pad += 1
        
        modekey, sign = get_modekey_sign(mode)
        deltae_hist[modekey] = ROOT.TH1F('deltae-%s' % modekey,
                                         frametitle, 100, -0.1, 0.1) 

        rootfile = get_rootfile(datatype, mode, label)
        pt = add_rootfile(rootfile, debug=opts.debug)

        for pte in pt:
            d =chooseD(modekey, pte, sign, alt_deltae=alt_deltae)
            if d != None:
                deltae_hist[modekey].Fill(pte.ddeltae[d])
        deltae_hist[modekey].Draw()
    canvas_output(canvas, figname, opts.test)


def ksmass(opts, args, figname):
    parsed = parse_args(args)
    datatype = parsed[0]
    tag = parsed[1]
    modes = parsed[2]
    label = parsed[3]

    var = 'ksmass'
    varname = 'K_{S} mass'
    unit = 'GeV'
    nBins = 100
    Xmin = 0.45
    Xmax = 0.55

    if len(modes) > 1:
        raise ValueError(modes, 'Only handle one mode at this time!')

    mode = modes[0]
    modekey, sign = get_modekey_sign(mode)
    
    modename = attr.modes[modekey]['uname']
    histname = '%s in %s' %(varname, modename)
    rootfile = get_rootfile(datatype, mode, label)
    pt = add_rootfile(rootfile, debug=opts.debug)
    canvas  =  ROOT.TCanvas("aCanvas", "Canvas", 600, 600)
    hist = ROOT.TH1F(var, histname, nBins, Xmin, Xmax)

    ntotal = 0
    nselected = 0
    def alt_checkVetoes(mode, pte, index, opt='', sign=None):
        return True

    if modekey not in (202, 203, 204):
        raise ValueError(modekey)
    
    for pte in pt:
        ntotal += 1
        if opts.test and ntotal >1000:
            break
        
        d =chooseD(modekey, pte, sign, checkVetoes=alt_checkVetoes)
        if d != None:
            nselected += 1
            ksmass = pte.ksmass[pte.ddau1[d]]
            hist.Fill(ksmass)

    hist.Draw()
    canvas_output(canvas, figname, opts.test)
    hist.Delete()
    sys.stdout.write(' selected %s out of %s.\n' % (nselected, ntotal))


def ksrad(opts, args, figname):
    parsed = parse_args(args)
    datatype = parsed[0]
    tag = parsed[1]
    modes = parsed[2]
    label = parsed[3]

    if len(modes) > 1:
        raise ValueError(modes, 'Only handle one mode at this time!')

    labels = [label]
    if ',' in label:
        labels = label.split(',')

    figname = shorten_figname(figname)
    mode = modes[0]
    modekey, sign = get_modekey_sign(mode)
    modename = attr.modes[modekey]['uname']
    frametitle = modename

    if modekey not in (202, 203, 204):
        raise ValueError(modekey)
    
    hnames = parse_opts_set(opts.set, 'legend')
    if hnames:
        hist_names = hnames.split(',')
    else:
        hist_names = labels

    nBins = 100
    Xmin = 0
    Xmax = .5
    xtitle = 'K_{S} vertex radius' 
    legend = ROOT.TLegend(0.75, 0.8, 0.95, 0.9)
   
    hist_list = []
    for label, hist_name in zip(labels, hist_names):
        hist_title = frametitle
        hist = ROOT.TH1D(hist_name, hist_title, nBins, Xmin, Xmax)
        rootfile = get_rootfile(datatype, mode, label)
        pt = add_rootfile(rootfile, debug=opts.debug)

        ntotal = 0
        nselected = 0 
        for pte in pt:
            ntotal += 1
            if opts.test and ntotal >100000:
                break

            d =chooseD(modekey, pte, sign, opt=label)
            if d != None:
                nks = pte.ddau1[d]
                ksrad = pte.ksrad[nks]
                hist.Fill(ksrad)
                nselected += 1
        sys.stdout.write('%s: Selected %s out of %s. \n' %(
            label,nselected, ntotal))
        hist_list.append(hist)

    canvas = draw_hist(hist_list, xtitle, legend)

    canvas_output(canvas, figname, opts.test)
    hist.Delete()


def mass(opts, args, figname):
    if args[0] == 'pi0':
        mass_pi0(opts, args[1:], figname)
    elif args[0] == 'kk':
        mass_kk(opts, args[1:], figname)
    else:
        raise NameError(args)
    
def mass_kk(opts, args, figname):
    parsed = parse_args(args)
    datatype = parsed[0]
    tag = parsed[1]
    modes = parsed[2]
    label = parsed[3]

    if len(modes) > 1:
        raise ValueError(modes, 'Only handle one mode at this time!')

    mode = modes[0]
    modekey, sign = get_modekey_sign(mode)
    modename = attr.modes[modekey]['uname']
    rootfile = get_rootfile(datatype, mode, label)

    pt = add_rootfile(rootfile, debug=opts.debug)
    canvas  =  ROOT.TCanvas("aCanvas", "Canvas", 600, 600)
    hist = ROOT.TH1F('kkmass', 'KK mass in %s' %modename, 100, 0, 2)
    hist.SetXTitle('M(K^{+}K^{-}) (GeV/c^{2})')
    num = 0
    for pte in pt:
        if opts.test and num >10000:
            break

        d =chooseD(modekey, pte, sign)
        if modekey != 205:
            raise NameError(modekey)
        
        if d != None:
            num += 1
            kaons = [pte.ddau1[d], pte.ddau2[d]]

            fourvecs = []
            for index in kaons:
                fourvecs.append([pte.trke[index], pte.trkpy[index],
                                 pte.trkpy[index], pte.trkpz[index]])

            kkmass = invmass(fourvecs[0], fourvecs[1])
            hist.Fill(kkmass)

    hist.Draw()
    canvas_output(canvas, figname, label, opts.test, outputroot=True)
    hist.Delete()


def mass_pi0(opts, args, figname):
    parsed = parse_args(args)
    datatype = parsed[0]
    tag = parsed[1]
    modes = parsed[2]
    label = parsed[3]

    if len(modes) > 1:
        raise ValueError(modes, 'Only handle one mode at this time!')

    mode = modes[0]
    modekey, sign = get_modekey_sign(mode)
    modename = attr.modes[modekey]['uname']
    rootfile = get_rootfile(datatype, mode, label)
    print rootfile, label
    sys.exit()
    pt = add_rootfile(rootfile, debug=opts.debug)
    canvas  =  ROOT.TCanvas("aCanvas", "Canvas")
    hist = ROOT.TH1F('pi0mass', '#pi^{0} mass in %s' %modename, 100, 0.1, 0.2) 
    num = 0
    for pte in pt:
        if opts.test and num >1000:
            break

        d =chooseD(modekey, pte, sign)
        if d != None:
            num += 1
            if modekey == 1 or modekey == 203:
                npi0 = pte.ddau3[d]
            if modekey == 201:
                npi0 = pte.ddau4[d]

            pi0mass = pte.pi0mass[npi0]
            hist.Fill(pi0mass)

    hist.Draw()
    canvas_output(canvas, figname, opts.test)
    hist.Delete()


def mbc(opts, args, figname):
    parsed = parse_args(args)
    datatype = parsed[0]
    tag = parsed[1]
    modes = parsed[2]
    label = parsed[3]

    if len(modes) > 1:
        raise ValueError(modes)

    labels = [label]
    if ',' in label:
        labels = label.split(',')

    figname = shorten_figname(figname)
    mode = modes[0]
    modekey, sign = get_modekey_sign(mode)
    modename = attr.modes[modekey]['uname']
    frametitle = modename

    hnames = parse_opts_set(opts.set, 'legend')
    if hnames:
        hist_names = hnames.split(',')
    else:
        hist_names = labels

    nBins = 100
    Xmin = 1.83
    Xmax = 1.89
    
    hist_list = []
    for label, hist_name in zip(labels, hist_names):
        hist_title = frametitle
        hist = ROOT.TH1D(hist_name, hist_title, nBins, Xmin, Xmax)
        rootfile = get_rootfile(datatype, mode, label)
        pt = add_rootfile(rootfile, debug=opts.debug)

        ntotal = 0
        nselected = 0 
        for pte in pt:
            ntotal += 1
            d =chooseD(modekey, pte, sign, opt=label)
            if d != None:
                hist.Fill(pte.dmbc[d])
                nselected += 1
        sys.stdout.write('Selected %s out of %s. \n' %(nselected, ntotal))
        hist_list.append(hist)

    xtitle = 'mBC (GeV)' 
    legend = ROOT.TLegend(0.66, 0.8, 0.9, 0.9)
    canvas = draw_hist(hist_list, xtitle, legend)

    Logy = parse_opts_set(opts.set, 'SetLogy')
    if Logy != None:
        canvas.SetLogy(Logy)

    canvas_output(canvas, figname, opts.test)
    hist.Delete()

    

def momentum(opts, args, figname):
    if args[0] == 'D0':
        momentum_D(opts, args[1:], figname)
    elif args[0] == 'K':
        momentum_K(opts, args[1:], figname)
    elif args[0] == 'pi':
        momentum_pi(opts, args[1:], figname)
    elif args[0] == 'pi_KS':
        momentum_pi_KS(opts, args[1:], figname)
    elif args[0] == 'pim_KS':
        momentum_pim_KS(opts, args[1:], figname)
    elif args[0] == 'pi0':
        momentum_pi0(opts, args[1:], figname)
    else:
        raise NameError(args)
    

def momentum_D(opts, args, figname):
    parsed = parse_args(args)
    datatype = parsed[0]
    tag = parsed[1]
    modes = parsed[2]
    label = parsed[3]

    if len(modes) > 1:
        raise ValueError(modes, 'Only handle one mode at this time!')

    mode = modes[0]
    modekey, sign = get_modekey_sign(mode)
    modename = attr.modes[modekey]['uname']
    rootfile = get_rootfile(datatype, mode, label)
    pt = add_rootfile(rootfile, debug=opts.debug)
    canvas  =  ROOT.TCanvas("aCanvas", "Canvas")
    hist = ROOT.TH1F('D0', 'D^{0} momentum in %s' %modename, 100, 0, 1) 
    num = 0
    for pte in pt:
        if opts.test and num >1000:
            break

        d =chooseD(modekey, pte, sign)
        if d != None:
            num += 1
            dpx = pte.dpx[d]
            dpy = pte.dpy[d]
            dpz = pte.dpz[d]
            dp = sqrt(dpx**2 + dpy**2 + dpz**2) 
            hist.Fill(dp)

    hist.Draw()
    canvas_output(canvas, figname, opts.test)
    hist.Delete()


def momentum_K(opts, args, figname):
    parsed = parse_args(args)
    datatype = parsed[0]
    tag = parsed[1]
    modes = parsed[2]
    label = parsed[3]

    if len(modes) > 1:
        raise ValueError(modes, 'Only handle one mode at this time!')

    mode = modes[0]
    modekey, sign = get_modekey_sign(mode)
    modename = attr.modes[modekey]['uname']
    rootfile = get_rootfile(datatype, mode, label)
    pt = add_rootfile(rootfile, debug=opts.debug)
    canvas  =  ROOT.TCanvas("aCanvas", "Canvas")

    pmax = 1
    if modekey == 0:
        pmax = 1.5 
    
    hist = ROOT.TH1F('K', 'K momentum in %s' %modename, 100, 0, pmax) 
    num = 0
    for pte in pt:
        if opts.test and num >1000:
            break

        d =chooseD(modekey, pte, sign)
        if d != None:
            num += 1
            nK = pte.ddau1[d]            

            Kpx = pte.trkpx[nK]
            Kpy = pte.trkpy[nK]
            Kpz = pte.trkpz[nK]
            Kp = sqrt(Kpx**2 + Kpy**2 + Kpz**2) 
            hist.Fill(Kp)

    hist.Draw()
    canvas_output(canvas, figname, opts.test)
    hist.Delete()

    
def momentum_pi(opts, args, figname):
    parsed = parse_args(args)
    datatype = parsed[0]
    tag = parsed[1]
    modes = parsed[2]
    label = parsed[3]

    if len(modes) > 1:
        raise ValueError(modes, 'Only handle one mode at this time!')

    mode = modes[0]
    modekey, sign = get_modekey_sign(mode)
    modename = attr.modes[modekey]['uname']
    rootfile = get_rootfile(datatype, mode, label)
    pt = add_rootfile(rootfile, debug=opts.debug)
    canvas  =  ROOT.TCanvas("aCanvas", "Canvas", 600, 600)
    hist = ROOT.TH1F('pip', '#pi momentum in %s' %modename, 100, 0, 1) 
    num = 0
    for pte in pt:
        if opts.test and num >1000:
            break

        d =chooseD(modekey, pte, sign)
        if d != None:
            num += 1
            npi = pte.ddau2[d]
            pipx = pte.trpipx[npi]
            pipy = pte.trpipy[npi]
            pipz = pte.trpipz[npi]
            pip = sqrt(pipx**2 + pipy**2 + pipz**2) 
            hist.Fill(pip)

    hist.Draw()
    canvas_output(canvas, figname, opts.test)
    hist.Delete()


def momentum_pi_KS(opts, args, figname):
    parsed = parse_args(args)
    datatype = parsed[0]
    tag = parsed[1]
    modes = parsed[2]
    label = parsed[3]

    if len(modes) > 1:
        raise ValueError(modes, 'Only handle one mode at this time!')

    labels = [label]
    if ',' in label:
        labels = label.split(',')

    figname = shorten_figname(figname)
    mode = modes[0]
    modekey, sign = get_modekey_sign(mode)
    modename = attr.modes[modekey]['uname']
    frametitle = modename

    if modekey not in (202, 203, 204):
        raise ValueError(modekey)
    
    hnames = parse_opts_set(opts.set, 'legend')
    if hnames:
        hist_names = hnames.split(',')
    else:
        hist_names = labels

    nBins = 100
    Xmin = 0
    Xmax = 1
    xtitle = '#pi^{+} (K_{S}) momentum (GeV)' 
    legend = ROOT.TLegend(0.75, 0.8, 0.95, 0.9)
   
    hist_list = []
    for label, hist_name in zip(labels, hist_names):
        hist_title = frametitle
        hist = ROOT.TH1D(hist_name, hist_title, nBins, Xmin, Xmax)
        rootfile = get_rootfile(datatype, mode, label)
        pt = add_rootfile(rootfile, debug=opts.debug)

        ntotal = 0
        nselected = 0 
        for pte in pt:
            ntotal += 1
            if opts.test and ntotal >80000:
                break

            d =chooseD(modekey, pte, sign, opt=label)
            if d != None:
                nks = pte.ddau1[d]
                npi = pte.ksdau1[nks]
                pipx = pte.trpipx[npi]
                pipy = pte.trpipy[npi]
                pipz = pte.trpipz[npi]
                pip = sqrt(pipx**2 + pipy**2 + pipz**2) 
                hist.Fill(pip)
                nselected += 1
        sys.stdout.write('%s: Selected %s out of %s. \n' %(
            label,nselected, ntotal))
        hist_list.append(hist)

    canvas = draw_hist(hist_list, xtitle, legend)

    canvas_output(canvas, figname, opts.test)
    hist.Delete()

def momentum_pim_KS(opts, args, figname):
    parsed = parse_args(args)
    datatype = parsed[0]
    tag = parsed[1]
    modes = parsed[2]
    label = parsed[3]

    if len(modes) > 1:
        raise ValueError(modes, 'Only handle one mode at this time!')

    labels = [label]
    if ',' in label:
        labels = label.split(',')

    figname = shorten_figname(figname)
    mode = modes[0]
    modekey, sign = get_modekey_sign(mode)
    modename = attr.modes[modekey]['uname']
    frametitle = modename

    if modekey not in (202, 203, 204):
        raise ValueError(modekey)
    
    hnames = parse_opts_set(opts.set, 'legend')
    if hnames:
        hist_names = hnames.split(',')
    else:
        hist_names = labels

    nBins = 100
    Xmin = 0
    Xmax = 1
    xtitle = '#pi^{-} (K_{S}) momentum (GeV)' 
    legend = ROOT.TLegend(0.75, 0.8, 0.95, 0.9)
   
    hist_list = []
    for label, hist_name in zip(labels, hist_names):
        hist_title = frametitle
        hist = ROOT.TH1D(hist_name, hist_title, nBins, Xmin, Xmax)
        rootfile = get_rootfile(datatype, mode, label)
        pt = add_rootfile(rootfile, debug=opts.debug)

        ntotal = 0
        nselected = 0 
        for pte in pt:
            ntotal += 1
            if opts.test and ntotal >80000:
                break

            d =chooseD(modekey, pte, sign, opt=label)
            if d != None:
                nks = pte.ddau1[d]
                npi = pte.ksdau2[nks]
                
                pipx = pte.trpipx[npi]
                pipy = pte.trpipy[npi]
                pipz = pte.trpipz[npi]
                pip = sqrt(pipx**2 + pipy**2 + pipz**2) 
                hist.Fill(pip)
                nselected += 1
        sys.stdout.write('%s: Selected %s out of %s. \n' %(
            label,nselected, ntotal))
        hist_list.append(hist)

    canvas = draw_hist(hist_list, xtitle, legend)

    canvas_output(canvas, figname, opts.test)
    hist.Delete()
   
def momentum_pi0(opts, args, figname):
    parsed = parse_args(args)
    datatype = parsed[0]
    tag = parsed[1]
    modes = parsed[2]
    label = parsed[3]


    if len(modes) > 1:
        raise ValueError(modes, 'Only handle one mode at this time!')

    mode = modes[0]
    modekey, sign = get_modekey_sign(mode)
    modename = attr.modes[modekey]['uname']

    rootfile = get_rootfile(datatype, mode, label)
    pt = add_rootfile(rootfile, debug=opts.debug)
    #canvas  =  ROOT.TCanvas("aCanvas", "Canvas", 900, 900)

    var = 'pi0p'
    title = modename
    unit = 'GeV'
    nBins = 100
    Xmin = 0.
    Xmax = 1.
    xtitle = '#pi^{0} momentum (GeV)'
    ytitle = 'Events / (%s %s)' % ((Xmax-Xmin)/nBins, unit)

    hist = ROOT.TH1F(var, title, nBins, Xmin, Xmax)

    num = 0
    for pte in pt:
        if opts.test and num >1000:
            break

        d =chooseD(modekey, pte, sign)
        if d != None:
            num += 1
            if modekey == 1 or modekey == 203:
                npi0 = pte.ddau3[d]
            if modekey == 201:
                npi0 = pte.ddau4[d]

            pi0px = pte.pi0px[npi0]
            pi0py = pte.pi0py[npi0]
            pi0pz = pte.pi0pz[npi0]
            pi0p = sqrt(pi0px**2 + pi0py**2 + pi0pz**2) 
            hist.Fill(pi0p)

    canvas = draw_hist(hist, xtitle, ytitle)
    canvas_output(canvas, figname, label, test=opts.test)


    
def pi0(opts, args, figname):
    if args[0] == 'momentum':
        momentum_pi0(opts, args[1:], figname)
    else:
        raise NameError(args)

def pi0mass(opts, args, figname):
    var = 'pi0mass'
    varname = '#pi^{0} mass'
    unit = 'GeV'
    nBins = 100
    Xmin = 0.115
    Xmax = 0.16

    parsed = parse_args(args)
    datatype  = parsed[0]
    tag       = parsed[1]
    modes     = parsed[2]
    label     = parsed[3]

    figname = shorten_figname(figname)
    mode = modes[0]

    modekey = get_modekey(mode)
    modename = attr.modes[modekey]['uname']
    frametitle = '#pi^{0} mass in %s' % modename

    labels = [label]
    if ',' in label:
        labels = label.split(',')

    hnames = parse_opts_set(opts.set, 'legend')
    if hnames:
        hist_names = hnames.split(',')
    else:
        hist_names = labels
        
    hist_list = []
    for label, hist_name in zip(labels, hist_names):
        hist_title = frametitle
        hist = ROOT.TH1D(hist_name, hist_title, nBins, Xmin, Xmax)
        evtfile = get_evtfile(datatype, mode, label, var, test=False)
        hist = tools.fill_hist_evtfile(hist, evtfile)
        hist_list.append(hist)

    xtitle = '%s (%s)' %(varname, unit)
    legend = ROOT.TLegend(0.66, 0.8, 0.9, 0.9)
    canvas = draw_hist(hist_list, xtitle, legend)
    canvas_output(canvas, figname, test=opts.test)
    

def se9o25(opts, args, figname):
    particle = args[0]
    datatype = args[1]
    mode = args[2]
    label = args[3]
    
    rootfile = get_rootfile(datatype, mode, label)
    pt = add_rootfile(rootfile, debug=opts.debug)

    for pte in pt:
        if opts.test and num >1000: break
        sys.exit()


def shorten_figname(figname):
    figname = figname.replace(',', '_')
    items = figname.split('_')
    items = tools.remove_duplicates_from_list(items)
    figname = '_'.join(items)
    return figname


def var_plot(realvar, evtfile, nBins, frametitle):
    dataset_args = ROOT.RooArgList(realvar)
    dataset = ROOT.RooDataSet.read(evtfile, dataset_args)
    Binning = ROOT.RooFit.Binning(nBins)
    frame = realvar.frame()
    dataset.plotOn(frame, Binning)
    frame.SetTitle(frametitle)
    frame.GetYaxis().SetTitleSize(0.03) 
    frame.GetYaxis().SetLabelSize(0.03) 
    frame.GetYaxis().SetTitleOffset(1.8)
    frame.GetXaxis().SetTitleSize(0.03) 
    frame.GetXaxis().SetLabelSize(0.03) 
    frame.GetXaxis().SetTitleOffset(1.2)
    frame.Draw()


