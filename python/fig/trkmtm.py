"""
Module for plotting track momentum

"""

import os
import sys
import attr
import tools 
from yld import parse_args
from tools import canvas_output, get_modekey, set_file
from sel.trkmtm import get_selfile
from ROOT import TFile, TCanvas
import shelve


__author__ = "Xin Shi <xs32@cornell.edu>"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2005-2011 Xin Shi"
__license__ = "GPL"
__revision__ = "$Revision$"


def main(opts, args):
    tools.set_root_style(stat=1, grid=0, PadTopMargin=0.1,
                         PadLeftMargin = 0.15)

    parsed = parse_args(args)
    datatype = parsed[0]
    tag = parsed[1]
    modes = parsed[2]
    label = parsed[3]

    if tag != 'single':
        # only deal with single tag
        raise NameError(tag)

    figpath = os.path.join(attr.figpath, label, 'trkmtm')
    
    for mode in modes:
        modekey = tools.get_modekey(mode)
        selfile = get_selfile(datatype, mode, label, test=opts.test)

        efffile = selfile.replace('.root', '.db')

        sname = attr.modes[modekey]['sname'].lower()
        f = TFile(selfile)

        effs = shelve.open(efffile)

        if sname == 'kpipi0':
            h_pk = {}; h_ppi1 = {}; h_ppiz = {}
            for tp in ('mc', 'mctruth'):
                h_pk[tp] = f.Get('h_pk_' + tp)
                h_ppi1[tp] = f.Get('h_ppi1_' + tp)
                h_ppiz[tp] = f.Get('h_ppiz_' + tp)
            draw_effmomenta_kpipi0(figpath, effs, sname, h_pk, h_ppi1, h_ppiz)
        elif sname == 'k3pi':
            h_pk = {}; h_ppi1 = {}; h_ppi2 = {}; h_ppim = {}
            for tp in ('mc', 'mctruth'):
                h_pk[tp] = f.Get('h_pk_' + tp)
                h_ppi1[tp] = f.Get('h_ppi1_' + tp)
                h_ppi2[tp] = f.Get('h_ppi2_' + tp)
                h_ppim[tp] = f.Get('h_ppim_' + tp)
            draw_effmomenta_k3pi(figpath, effs, sname, h_pk, h_ppi1, h_ppi2, h_ppim)
        elif sname == 'kpipi':
            h_pk = {}; h_ppi1 = {}; h_ppi2 = {}
            for tp in ('mc', 'mctruth'):
                h_pk[tp] = f.Get('h_pk_' + tp)
                h_ppi1[tp] = f.Get('h_ppi1_' + tp)
                h_ppi2[tp] = f.Get('h_ppi2_' + tp)
            draw_effmomenta_kpipi(figpath, effs, sname, h_pk, h_ppi1, h_ppi2)
        elif sname == 'kpipipi0':
            h_pk = {}; h_ppi1 = {}; h_ppi2 = {}; h_ppiz = {}
            for tp in ('mc', 'mctruth'):
                h_pk[tp] = f.Get('h_pk_' + tp)
                h_ppi1[tp] = f.Get('h_ppi1_' + tp)
                h_ppi2[tp] = f.Get('h_ppi2_' + tp)
                h_ppiz[tp] = f.Get('h_ppim_' + tp)
            draw_effmomenta_kpipipi0(figpath, effs, sname, h_pk, h_ppi1, h_ppi2, h_ppiz)
        elif sname == 'kspipi0':
            h_pks = {}; h_ppi1 = {}; h_ppiz = {}
            for tp in ('mc', 'mctruth'):
                h_pks[tp] = f.Get('h_pks_' + tp)
                h_ppi1[tp] = f.Get('h_ppi1_' + tp)
                h_ppiz[tp] = f.Get('h_ppiz_' + tp)
            draw_effmomenta_kspipi0(figpath, effs, sname, h_pks, h_ppi1, h_ppiz)
        elif sname == 'ks3pi':
            h_pks = {}; h_ppi1 = {}; h_ppi2 = {}; h_ppim = {}
            for tp in ('mc', 'mctruth'):
                h_pks[tp] = f.Get('h_pk_' + tp)
                h_ppi1[tp] = f.Get('h_ppi1_' + tp)
                h_ppi2[tp] = f.Get('h_ppi2_' + tp)
                h_ppim[tp] = f.Get('h_ppim_' + tp)
            draw_effmomenta_ks3pi(figpath, effs, sname, h_pks, h_ppi1, h_ppi2, h_ppim)
        elif sname == 'kkpi':
            h_pkm = {}; h_pkp = {}; h_ppi = {}
            for tp in ('mc', 'mctruth'):
                h_pkm[tp] = f.Get('h_pkm_' + tp)
                h_pkp[tp] = f.Get('h_pkp_' + tp)
                h_ppi[tp] = f.Get('h_ppi_' + tp)
            draw_effmomenta_kkpi(figpath, effs, sname, h_pkp, h_pkm, h_ppi)

        else:
            raise NameError(sname)

def draw_effmomenta_kpipi0(figpath, effs, sname, h_pk, h_ppi1, h_ppiz):
    figname = '%s_effmomenta_plain' % sname
    epsfile = set_file(extbase=figpath, comname=figname, ext='eps')

    ratio = 1 
    c1 = TCanvas('c1', 'canvas', 900, 850)
    c1.Divide(2,2)
    c1.cd(1)
    #kpi1['mc'].Sumw2();
    h_pk['mctruth'].Draw('PE')
    h_pk['mc'].Scale(ratio)
    h_pk['mc'].Draw('SAME')
    c1.cd(2)
    h_ppi1['mctruth'].Draw('PE')
    h_ppi1['mc'].Scale(ratio)
    h_ppi1['mc'].Draw('SAME')
    c1.cd(3)
    c1.cd(4)
    h_ppiz['mctruth'].Draw('PE')
    h_ppiz['mc'].Scale(ratio)
    h_ppiz['mc'].Draw('SAME')

    c1.Print(epsfile)
    c1.Clear()
    tools.eps2pdf(epsfile)

    # -------------------------------------
    figname = '%s_effmomenta' % sname
    epsfile = set_file(extbase=figpath, comname=figname, ext='eps')

    for type in ('mc', 'mctruth'):
        h_pk[type].Sumw2()
        h_ppi1[type].Sumw2()
        h_ppiz[type].Sumw2()

    loceffs = {}
    c1 = TCanvas('c1', 'canvas', 900, 850)
    c1.Divide(2,2)
    c1.cd(1)
     
    clone = h_pk['mctruth'].Clone()
    clone.Divide(h_pk['mc'], h_pk['mctruth'], 1, 1, 'B')
    clone.SetTitle('Efficiency as a function of K^{-} momentum')
    clone.Draw('PE')
    #clone.Print('all')
    for i in range(1, 1+clone.GetNbinsX()):
        loceffs[clone.GetBinCenter(i)] = clone.GetBinContent(i)
    effs['k']=loceffs

    c1.cd(2)
    clone = h_ppi1['mctruth'].Clone()
    clone.Divide(h_ppi1['mc'], h_ppi1['mctruth'], 1, 1, 'B')
    clone.SetTitle('Efficiency as a function of #pi^{+} momentum')
    clone.Draw('PE')
    loceffs.clear()
    for i in range(1, 1+clone.GetNbinsX()):
        loceffs[clone.GetBinCenter(i)] = clone.GetBinContent(i)
    effs['pi1']=loceffs

    c1.cd(3)

    c1.cd(4)
    clone = h_ppiz['mctruth'].Clone()
    clone.Divide(h_ppiz['mc'], h_ppiz['mctruth'], 1, 1, 'B')
    clone.SetTitle('Efficiency as a function of #pi^{0} momentum')
    clone.Draw('PE')
    loceffs.clear()

    for i in range(1, 1+clone.GetNbinsX()):
        loceffs[clone.GetBinCenter(i)] = clone.GetBinContent(i)
    effs['piz']=loceffs

    boxes_num = effs['boxes_num']
    boxes_denom = effs['boxes_denom']

    effs['total'] = boxes_num/boxes_denom
    effs.close() 
    c1.Print(epsfile)
    c1.Clear()
    tools.eps2pdf(epsfile)
    

def draw_effmomenta_k3pi(figpath, effs, sname, h_pk, h_ppi1, h_ppi2, h_ppim):
    figname = '%s_effmomenta_plain' % sname
    epsfile = set_file(extbase=figpath, comname=figname, ext='eps')

    ratio = 1 
    c1 = TCanvas('c1', 'canvas', 900, 850)
    c1.Divide(2,2)
    c1.cd(1)
    #kpi1['mc'].Sumw2();
    h_pk['mctruth'].Draw('PE')
    h_pk['mc'].Scale(ratio)
    h_pk['mc'].Draw('SAME')
    c1.cd(2)
    h_ppi1['mctruth'].Draw('PE')
    h_ppi1['mc'].Scale(ratio)
    h_ppi1['mc'].Draw('SAME')
    c1.cd(3)
    h_ppi2['mctruth'].Draw('PE')
    h_ppi2['mc'].Scale(ratio)
    h_ppi2['mc'].Draw('SAME')
    c1.cd(4)
    h_ppim['mctruth'].Draw('PE')
    h_ppim['mc'].Scale(ratio)
    h_ppim['mc'].Draw('SAME')

    c1.Print(epsfile)
    c1.Clear()
    tools.eps2pdf(epsfile)
    
    # -------------------------------------
    figname = '%s_effmomenta' % sname
    epsfile = set_file(extbase=figpath, comname=figname, ext='eps')

    for type in ('mc', 'mctruth'):
        h_pk[type].Sumw2()
        h_ppi1[type].Sumw2()
        h_ppi2[type].Sumw2()
        h_ppim[type].Sumw2()

    loceffs = {}
    c1 = TCanvas('c1', 'canvas', 900, 850)
    c1.Divide(2,2)
    c1.cd(1)
     
    clone = h_pk['mctruth'].Clone()
    clone.Divide(h_pk['mc'], h_pk['mctruth'], 1, 1, 'B')
    clone.SetTitle('Efficiency as a function of K^{-} momentum')
    clone.Draw('PE')
    #clone.Print('all')
    for i in range(1, 1+clone.GetNbinsX()):
        loceffs[clone.GetBinCenter(i)] = clone.GetBinContent(i)
    effs['k']=loceffs

    c1.cd(2)
    clone = h_ppi1['mctruth'].Clone()
    clone.Divide(h_ppi1['mc'], h_ppi1['mctruth'], 1, 1, 'B')
    clone.SetTitle('Efficiency as a function of #pi^{+}_{1} momentum')
    clone.Draw('PE')
    loceffs.clear()
    for i in range(1, 1+clone.GetNbinsX()):
        loceffs[clone.GetBinCenter(i)] = clone.GetBinContent(i)
    effs['pi1']=loceffs

    c1.cd(3)
    clone = h_ppi2['mctruth'].Clone()
    clone.Divide(h_ppi2['mc'], h_ppi2['mctruth'], 1, 1, 'B')
    clone.SetTitle('Efficiency as a function of #pi^{+}_{2} momentum')
    clone.Draw('PE')
    loceffs.clear()
    for i in range(1, 1+clone.GetNbinsX()):
        loceffs[clone.GetBinCenter(i)] = clone.GetBinContent(i)
    effs['pi2']=loceffs

    c1.cd(4)
    clone = h_ppim['mctruth'].Clone()
    clone.Divide(h_ppim['mc'], h_ppim['mctruth'], 1, 1, 'B')
    clone.SetTitle('Efficiency as a function of #pi^{-} momentum')
    clone.Draw('PE')
    loceffs.clear()
    for i in range(1, 1+clone.GetNbinsX()):
        loceffs[clone.GetBinCenter(i)] = clone.GetBinContent(i)
    effs['pim']=loceffs


    boxes_num_p = effs['boxes_num_p']
    boxes_denom_p = effs['boxes_denom_p']
    boxes_num_a = effs['boxes_num_a']
    boxes_denom_a = effs['boxes_denom_a']

    effs['total_p'] = boxes_num_p/boxes_denom_p
    effs['total_a'] = boxes_num_a/boxes_denom_a

    effs.close() 
    c1.Print(epsfile)
    c1.Clear()
    tools.eps2pdf(epsfile)
    

def draw_effmomenta_kpipi(figpath, effs, sname, h_pk, h_ppi1, h_ppi2):
    figname = '%s_effmomenta_plain' % sname
    epsfile = set_file(extbase=figpath, comname=figname, ext='eps')

    ratio = 1 
    c1 = TCanvas('c1', 'canvas', 900, 850)
    c1.Divide(2,2)
    c1.cd(1)
    h_pk['mctruth'].Draw('PE')
    h_pk['mc'].Scale(ratio)
    h_pk['mc'].Draw('SAME')
    c1.cd(2)
    h_ppi1['mctruth'].Draw('PE')
    h_ppi1['mc'].Scale(ratio)
    h_ppi1['mc'].Draw('SAME')
    c1.cd(3)
    h_ppi2['mctruth'].Draw('PE')
    h_ppi2['mc'].Scale(ratio)
    h_ppi2['mc'].Draw('SAME')
    c1.cd(4)
    
    c1.Print(epsfile)
    c1.Clear()
    tools.eps2pdf(epsfile)

    # -------------------------------------
    figname = '%s_effmomenta' % sname
    epsfile = set_file(extbase=figpath, comname=figname, ext='eps')

    for type in ('mc', 'mctruth'):
        h_pk[type].Sumw2()
        h_ppi1[type].Sumw2()
        h_ppi2[type].Sumw2()

    loceffs = {}
    c1 = TCanvas('c1', 'canvas', 900, 850)
    c1.Divide(2,2)
    c1.cd(1)

    clone = h_pk['mctruth'].Clone()
    clone.Divide(h_pk['mc'], h_pk['mctruth'], 1, 1, 'B')
    clone.SetTitle('Efficiency as a function of K^{-} momentum')
    clone.Draw('PE')
    #clone.Print('all')
    for i in range(1, 1+clone.GetNbinsX()):
        loceffs[clone.GetBinCenter(i)] = clone.GetBinContent(i)
    effs['k']=loceffs

    c1.cd(2)
    clone = h_ppi1['mctruth'].Clone()
    clone.Divide(h_ppi1['mc'], h_ppi1['mctruth'], 1, 1, 'B')
    clone.SetTitle('Efficiency as a function of #pi^{+}_{1} momentum')
    clone.Draw('PE')
    loceffs.clear()
    for i in range(1, 1+clone.GetNbinsX()):
        loceffs[clone.GetBinCenter(i)] = clone.GetBinContent(i)
    effs['pi1']=loceffs

    c1.cd(3)
    clone = h_ppi2['mctruth'].Clone()
    clone.Divide(h_ppi2['mc'], h_ppi2['mctruth'], 1, 1, 'B')
    clone.SetTitle('Efficiency as a function of #pi^{+}_{2} momentum')
    clone.Draw('PE')
    loceffs.clear()
    for i in range(1, 1+clone.GetNbinsX()):
        loceffs[clone.GetBinCenter(i)] = clone.GetBinContent(i)
    effs['pi2']=loceffs
    
    c1.cd(4)
    
    boxes_num_p = effs['boxes_num_p']
    boxes_denom_p = effs['boxes_denom_p']
    boxes_num_a = effs['boxes_num_a']
    boxes_denom_a = effs['boxes_denom_a']

    effs['total_p'] = boxes_num_p/boxes_denom_p
    effs['total_a'] = boxes_num_a/boxes_denom_a
    effs.close() 
    c1.Print(epsfile)
    c1.Clear()
    tools.eps2pdf(epsfile)
    
def draw_effmomenta_kpipipi0(figpath, effs, sname, h_pk, h_ppi1, h_ppi2, h_ppiz):
    figname = '%s_effmomenta_plain' % sname
    epsfile = set_file(extbase=figpath, comname=figname, ext='eps')

    ratio = 1 
    c1 = TCanvas('c1', 'canvas', 900, 850)
    c1.Divide(2,2)

    c1.cd(1)

    h_pk['mctruth'].Draw('PE')
    h_pk['mc'].Scale(ratio)
    h_pk['mc'].Draw('SAME')
    c1.cd(2)
    h_ppi1['mctruth'].Draw('PE')
    h_ppi1['mc'].Scale(ratio)
    h_ppi1['mc'].Draw('SAME')
    c1.cd(3)
    h_ppi2['mctruth'].Draw('PE')
    h_ppi2['mc'].Scale(ratio)
    h_ppi2['mc'].Draw('SAME')
    c1.cd(4)
    h_ppiz['mctruth'].Draw('PE')
    h_ppiz['mc'].Scale(ratio)
    h_ppiz['mc'].Draw('SAME')

    c1.Print(epsfile)
    c1.Clear()
    tools.eps2pdf(epsfile)
    
    # -------------------------------------
    figname = '%s_effmomenta' % sname
    epsfile = set_file(extbase=figpath, comname=figname, ext='eps')

    for type in ('mc', 'mctruth'):
        h_pk[type].Sumw2()
        h_ppi1[type].Sumw2()
        h_ppi2[type].Sumw2()
        h_ppiz[type].Sumw2()

    loceffs = {}
    c1.Clear()
    c1.Divide(2,2)
    c1.cd(1)
    clone = h_pk['mctruth'].Clone()
    clone.Divide(h_pk['mc'], h_pk['mctruth'], 1, 1, 'B')
    clone.SetTitle('Efficiency as a function of K^{-} momentum')
    clone.Draw('PE')
    #clone.Print('all')
    for i in range(1, 1+clone.GetNbinsX()):
        loceffs[clone.GetBinCenter(i)] = clone.GetBinContent(i)
    effs['k']=loceffs

    c1.cd(2)
    clone = h_ppi1['mctruth'].Clone()
    clone.Divide(h_ppi1['mc'], h_ppi1['mctruth'], 1, 1, 'B')
    clone.SetTitle('Efficiency as a function of #pi^{+}_{1} momentum')
    clone.Draw('PE')
    loceffs.clear()
    for i in range(1, 1+clone.GetNbinsX()):
        loceffs[clone.GetBinCenter(i)] = clone.GetBinContent(i)
    effs['pi1']=loceffs
    
    c1.cd(3)
    clone = h_ppi2['mctruth'].Clone()
    clone.Divide(h_ppi2['mc'], h_ppi2['mctruth'], 1, 1, 'B')
    clone.SetTitle('Efficiency as a function of #pi^{+}_{2} momentum')
    clone.Draw('PE')
    loceffs.clear()
    for i in range(1, 1+clone.GetNbinsX()):
        loceffs[clone.GetBinCenter(i)] = clone.GetBinContent(i)
    effs['pi2']=loceffs

    c1.cd(4)
    clone = h_ppiz['mctruth'].Clone()
    clone.Divide(h_ppiz['mc'], h_ppiz['mctruth'], 1, 1, 'B')
    clone.SetTitle('Efficiency as a function of #pi^{-} momentum')
    clone.Draw('PE')
    loceffs.clear()
    for i in range(1, 1+clone.GetNbinsX()):
        loceffs[clone.GetBinCenter(i)] = clone.GetBinContent(i)
    effs['piz']=loceffs

    boxes_num_p = effs['boxes_num_p']
    boxes_denom_p = effs['boxes_denom_p']
    boxes_num_a = effs['boxes_num_a']
    boxes_denom_a = effs['boxes_denom_a']

    effs['total_p'] = boxes_num_p/boxes_denom_p
    effs['total_a'] = boxes_num_a/boxes_denom_a

    effs.close() 
    c1.Print(epsfile)
    c1.Clear()
    tools.eps2pdf(epsfile)

    
def draw_effmomenta_kspipi0(figpath, effs, sname, h_pks, h_ppi1, h_ppiz):
    figname = '%s_effmomenta_plain' % sname
    epsfile = set_file(extbase=figpath, comname=figname, ext='eps')

    ratio = 1 
    c1 = TCanvas('c1', 'canvas', 900, 850)
    c1.Divide(2,2)

    c1.cd(1)

    h_pks['mctruth'].Draw('PE')
    h_pks['mc'].Scale(ratio)
    h_pks['mc'].Draw('SAME')
    c1.cd(2)
    h_ppi1['mctruth'].Draw('PE')
    h_ppi1['mc'].Scale(ratio)
    h_ppi1['mc'].Draw('SAME')
    c1.cd(3)
    c1.cd(4)
    h_ppiz['mctruth'].Draw('PE')
    h_ppiz['mc'].Scale(ratio)
    h_ppiz['mc'].Draw('SAME')

    c1.Print(epsfile)
    c1.Clear()
    tools.eps2pdf(epsfile)
    
    # -------------------------------------
    figname = '%s_effmomenta' % sname
    epsfile = set_file(extbase=figpath, comname=figname, ext='eps')

    for type in ('mc', 'mctruth'):
        h_pks[type].Sumw2()
        h_ppi1[type].Sumw2()
        h_ppiz[type].Sumw2()

    loceffs = {}
    c1.Clear()
    c1.Divide(2,2)
    c1.cd(1)
    clone = h_pks['mctruth'].Clone()
    clone.Divide(h_pks['mc'], h_pks['mctruth'], 1, 1, 'B')
    clone.SetTitle('Efficiency as a function of K_{S} momentum')
    clone.Draw('PE')
    #clone.Print('all')
    for i in range(1, 1+clone.GetNbinsX()):
        loceffs[clone.GetBinCenter(i)] = clone.GetBinContent(i)
    effs['ks']=loceffs

    c1.cd(2)
    clone = h_ppi1['mctruth'].Clone()
    clone.Divide(h_ppi1['mc'], h_ppi1['mctruth'], 1, 1, 'B')
    clone.SetTitle('Efficiency as a function of #pi^{+} momentum')
    clone.Draw('PE')
    loceffs.clear()
    for i in range(1, 1+clone.GetNbinsX()):
        loceffs[clone.GetBinCenter(i)] = clone.GetBinContent(i)
    effs['pi1']=loceffs

    c1.cd(3)
    
    c1.cd(4)
    clone = h_ppiz['mctruth'].Clone()
    clone.Divide(h_ppiz['mc'], h_ppiz['mctruth'], 1, 1, 'B')
    clone.SetTitle('Efficiency as a function of #pi^{0} momentum')
    clone.Draw('PE')
    loceffs.clear()
    for i in range(1, 1+clone.GetNbinsX()):
        loceffs[clone.GetBinCenter(i)] = clone.GetBinContent(i)
    effs['piz']=loceffs

    boxes_num = effs['boxes_num']
    boxes_denom = effs['boxes_denom']

    effs['total'] = boxes_num/boxes_denom
    effs.close() 
    c1.Print(epsfile)
    c1.Clear()
    tools.eps2pdf(epsfile)


def draw_effmomenta_ks3pi(figpath, effs, sname, h_pks, h_ppi1, h_ppi2, h_ppim):
    figname = '%s_effmomenta_plain' % sname
    epsfile = set_file(extbase=figpath, comname=figname, ext='eps')

    ratio = 1 
    c1 = TCanvas('c1', 'canvas', 900, 850)
    c1.Divide(2,2)

    c1.cd(1)

    h_pks['mctruth'].Draw('PE')
    h_pks['mc'].Scale(ratio)
    h_pks['mc'].Draw('SAME')
    c1.cd(2)
    h_ppi1['mctruth'].Draw('PE')
    h_ppi1['mc'].Scale(ratio)
    h_ppi1['mc'].Draw('SAME')
    c1.cd(3)
    h_ppi2['mctruth'].Draw('PE')
    h_ppi2['mc'].Scale(ratio)
    h_ppi2['mc'].Draw('SAME')
    c1.cd(4)
    h_ppim['mctruth'].Draw('PE')
    h_ppim['mc'].Scale(ratio)
    h_ppim['mc'].Draw('SAME')

    c1.Print(epsfile)
    c1.Clear()
    tools.eps2pdf(epsfile)

    # -------------------------------------
    figname = '%s_effmomenta' % sname
    epsfile = set_file(extbase=figpath, comname=figname, ext='eps')

    for type in ('mc', 'mctruth'):
        h_pks[type].Sumw2()
        h_ppi1[type].Sumw2()
        h_ppi2[type].Sumw2()
        h_ppim[type].Sumw2()

    loceffs = {}
    c1.Clear()
    c1.Divide(2,2)
    c1.cd(1)
    clone = h_pks['mctruth'].Clone()
    clone.SetTitle('Efficiency as a function of K_{S} momentum')
    clone.Divide(h_pks['mc'], h_pks['mctruth'], 1, 1, 'B')
    clone.Draw('PE')
    #clone.Print('all')
    for i in range(1, 1+clone.GetNbinsX()):
        loceffs[clone.GetBinCenter(i)] = clone.GetBinContent(i)
    effs['ks']=loceffs

    c1.cd(2)
    clone = h_ppi1['mctruth'].Clone()
    clone.SetTitle('Efficiency as a function of #pi^{+}_{1} momentum')
    clone.Divide(h_ppi1['mc'], h_ppi1['mctruth'], 1, 1, 'B')
    clone.Draw('PE')
    loceffs.clear()
    for i in range(1, 1+clone.GetNbinsX()):
        loceffs[clone.GetBinCenter(i)] = clone.GetBinContent(i)
    effs['pi1']=loceffs

    c1.cd(3)
    clone = h_ppi2['mctruth'].Clone()
    clone.SetTitle('Efficiency as a function of #pi^{+}_{2} momentum')
    clone.Divide(h_ppi2['mc'], h_ppi2['mctruth'], 1, 1, 'B')
    clone.Draw('PE')
    loceffs.clear()
    for i in range(1, 1+clone.GetNbinsX()):
        loceffs[clone.GetBinCenter(i)] = clone.GetBinContent(i)
    effs['pi2']=loceffs

    c1.cd(4)
    clone = h_ppim['mctruth'].Clone()
    clone.SetTitle('Efficiency as a function of #pi^{-} momentum')
    clone.Divide(h_ppim['mc'], h_ppim['mctruth'], 1, 1, 'B')
    clone.Draw('PE')
    loceffs.clear()
    for i in range(1, 1+clone.GetNbinsX()):
        loceffs[clone.GetBinCenter(i)] = clone.GetBinContent(i)
    effs['pim']=loceffs

    boxes_num_p = effs['boxes_num_p']
    boxes_denom_p = effs['boxes_denom_p']
    boxes_num_a = effs['boxes_num_a']
    boxes_denom_a = effs['boxes_denom_a']

    effs['total_p'] = boxes_num_p/boxes_denom_p
    effs['total_a'] = boxes_num_a/boxes_denom_a

    effs.close() 
    c1.Print(epsfile)
    c1.Clear()
    tools.eps2pdf(epsfile)


def draw_effmomenta_kkpi(figpath, effs, sname, h_pkp, h_pkm, h_ppi):
    figname = '%s_effmomenta_plain' % sname
    epsfile = set_file(extbase=figpath, comname=figname, ext='eps')

    ratio = 1 
    c1 = TCanvas('c1', 'canvas', 900, 850)
    c1.Divide(2,2)

    c1.cd(1)

    h_pkm['mctruth'].Draw('PE')
    h_pkm['mc'].Scale(ratio)
    h_pkm['mc'].Draw('SAME')
    c1.cd(2)
    h_pkp['mctruth'].Draw('PE')
    h_pkp['mc'].Scale(ratio)
    h_pkp['mc'].Draw('SAME')
    c1.cd(3)
    c1.cd(4)
    h_ppi['mctruth'].Draw('PE')
    h_ppi['mc'].Scale(ratio)
    h_ppi['mc'].Draw('SAME')

    c1.Print(epsfile)
    c1.Clear()
    tools.eps2pdf(epsfile)
    
    # -------------------------------------
    figname = '%s_effmomenta' % sname
    epsfile = set_file(extbase=figpath, comname=figname, ext='eps')

    for type in ('mc', 'mctruth'):
        h_pkm[type].Sumw2()
        h_pkp[type].Sumw2()
        h_ppi[type].Sumw2()

    loceffs = {}
    c1.Clear()
    c1.Divide(2,2)
    c1.cd(1)
    clone = h_pkm['mctruth'].Clone()
    clone.Divide(h_pkm['mc'], h_pkm['mctruth'], 1, 1, 'B')
    clone.SetTitle('Efficiency as a function of K^{-} momentum')
    clone.Draw('PE')
    #clone.Print('all')
    for i in range(1, 1+clone.GetNbinsX()):
        loceffs[clone.GetBinCenter(i)] = clone.GetBinContent(i)
    effs['km']=loceffs

    c1.cd(2)
    clone = h_pkp['mctruth'].Clone()
    clone.Divide(h_pkp['mc'], h_pkp['mctruth'], 1, 1, 'B')
    clone.SetTitle('Efficiency as a function of K^{+} momentum')
    clone.Draw('PE')
    loceffs.clear()
    for i in range(1, 1+clone.GetNbinsX()):
        loceffs[clone.GetBinCenter(i)] = clone.GetBinContent(i)
    effs['kp']=loceffs

    c1.cd(3)
    
    c1.cd(4)
    clone = h_ppi['mctruth'].Clone()
    clone.Divide(h_ppi['mc'], h_ppi['mctruth'], 1, 1, 'B')
    clone.SetTitle('Efficiency as a function of #pi^{+} momentum')
    clone.Draw('PE')
    loceffs.clear()
    for i in range(1, 1+clone.GetNbinsX()):
        loceffs[clone.GetBinCenter(i)] = clone.GetBinContent(i)
    effs['pi']=loceffs

    boxes_num = effs['boxes_num']
    boxes_denom = effs['boxes_denom']

    effs['total'] = boxes_num/boxes_denom
    effs.close() 
    c1.Print(epsfile)
    c1.Clear()
    tools.eps2pdf(epsfile)


