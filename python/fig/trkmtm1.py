"""
Module for plotting track momentum second stage

"""

import os
import sys
import attr
import tools 
from tools import get_modekey, set_file, DHadTable, parse_args

from sel.trkmtm import get_selfile
from ROOT import TFile, TCanvas, kTRUE, kFALSE
import shelve


__author__ = "Xin Shi <xs32@cornell.edu>"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2005-2011 Xin Shi"
__license__ = "GPL"
__revision__ = "$Revision$"


def main(opts, args):
    tools.set_root_style(stat=1, grid=0)

    parsed = parse_args(args)
    datatype = parsed[0]
    tag = parsed[1]
    modes = parsed[2]
    label = parsed[3]

    figpath = os.path.join(attr.figpath, label, 'trkmtm')

    for mode in modes:
        modekey = tools.get_modekey(mode)
        sname = attr.modes[modekey]['sname'].lower()

        if sname == 'kpipi0':
            draw_momenta_kpipi0(datatype, mode, label, test=opts.test)
        elif sname == 'k3pi':
            draw_momenta_k3pi(datatype, mode, label, test=opts.test)
        elif sname == 'kpipi':
            draw_momenta_kpipi(datatype, mode, label, test=opts.test)
        elif sname == 'kpipipi0':
            draw_momenta_kpipipi0(datatype, mode, label, test=opts.test)
        elif sname == 'kspipi0':
            draw_momenta_kspipi0(datatype, mode, label, test=opts.test)
        elif sname == 'ks3pi':
            draw_momenta_ks3pi(datatype, mode, label, test=opts.test)
        elif sname == 'kkpi':
            draw_momenta_kkpi(figpath, datatype, mode, label, test=opts.test)

        else:
            raise NameError(sname)

def draw_momenta_kpipi0(datatype, mode, label, test):
    modekey = tools.get_modekey(mode)
    sname = attr.modes[modekey]['sname'].lower()
    figname = '%s_momenta' % sname
    figpath = os.path.join(attr.figpath, label, 'trkmtm')
    epsfile = set_file(extbase=figpath, comname=figname, ext='eps')

    h_mbc = {}; kpi1 = {} ; pipih = {}; 
    kpiz = {}; kpipih = {}; 
    h_pk = {}; h_ppi1 = {}; h_ppiz = {}
    h_pk_c = {}; h_ppi1_c = {}; h_ppiz_c = {}
    h_pk_sb = {}; h_ppi1_sb = {}; h_ppiz_sb = {}
    h_pk_sb_c = {}; h_ppi1_sb_c = {}; h_ppiz_sb_c = {}
    h_angk = {}; h_angpi1 = {}; h_angpiz = {}

    for datatype in datatype.split('/'):
        selfile = get_selfile(datatype, mode, label, test=test)
        selfile = selfile.replace('/trkmtm/', '/trkmtm2/')

        f = TFile(selfile)
        if datatype == 'signal' or datatype == 'generic':
            tp = 'mc'
        if datatype == 'data':
            tp = 'data'
            
        h_mbc[tp]= f.Get('h_mbc_'+tp)

        kpi1[tp]= f.Get('kpi1_'+tp)
        pipih[tp]= f.Get('pipih_'+tp)
        kpiz[tp]= f.Get('kpiz_'+tp)
        kpipih[tp]= f.Get('kpipih_'+tp)
    
        h_pk[tp]= f.Get('h_pk_'+tp)
        h_ppi1[tp]= f.Get('h_ppi1_'+tp)
        h_ppiz[tp]= f.Get('h_ppiz_'+tp)
        
        h_pk_c[tp]= f.Get('h_pk_c_'+tp)
        h_ppi1_c[tp]= f.Get('h_ppi1_c_'+tp)
        h_ppiz_c[tp]= f.Get('h_ppiz_c_'+tp)
   
        h_pk_sb[tp]= f.Get('h_pk_sb_'+tp)
        h_ppi1_sb[tp]= f.Get('h_ppi1_sb_'+tp)
        h_ppiz_sb[tp]= f.Get('h_ppiz_sb_'+tp)

        h_pk_sb_c[tp]= f.Get('h_pk_sb_c_'+tp)
        h_ppi1_sb_c[tp]= f.Get('h_ppi1_sb_c_'+tp)
        h_ppiz_sb_c[tp]= f.Get('h_ppiz_sb_c_'+tp)

        h_angk[tp]= f.Get('h_angk_'+tp)
        h_angpi1[tp]= f.Get('h_angpi1_'+tp)
        h_angpiz[tp]= f.Get('h_angpiz_'+tp)

        f.Clear()

    ratio = h_pk['data'].Integral()/h_pk['mc'].Integral()

    c1 = TCanvas('c1', 'canvas', 900, 900)
    c1.Divide(2,2)
    c1.cd(1)
    h_pk['data'].Draw('PE')
    h_pk['mc'].Scale(ratio)
    h_pk['mc'].Draw('SAME')
    c1.cd(2)
    h_ppi1['data'].Draw('PE')
    h_ppi1['mc'].Scale(ratio)
    h_ppi1['mc'].Draw('SAME')
    c1.cd(3)
    c1.cd(4)
    h_ppiz['data'].Draw('PE')
    h_ppiz['mc'].Scale(ratio)
    h_ppiz['mc'].Draw('SAME')

    c1.Print(epsfile)
    tools.eps2pdf(epsfile)

    tab = DHadTable()
    tab.row_append(['Name', 'Data/MC'])
                   
    c1.Clear()
    c1.Divide(2,2)
    c1.cd(1)
    h_pk_c['data'].Draw('PE')
    lratio = h_pk_c['data'].Integral()/h_pk_c['mc'].Integral()
    #print 'k:', lratio/ratio

    tab.row_append(['K', lratio/ratio])
    
    h_pk_c['mc'].Scale(lratio)
    h_pk_c['mc'].Draw('SAME')
    c1.cd(2)
    h_ppi1_c['data'].Draw('PE')
    lratio = h_ppi1_c['data'].Integral()/h_ppi1_c['mc'].Integral()
    #print 'pi1:', lratio/ratio

    tab.row_append(['pi1', lratio/ratio])

    h_ppi1_c['mc'].Scale(lratio)
    h_ppi1_c['mc'].Draw('SAME')
    c1.cd(3)
    c1.cd(4)
    h_ppiz_c['data'].Draw('PE')
    lratio = h_ppiz_c['data'].Integral()/h_ppiz_c['mc'].Integral()
    #print 'piz:', lratio/ratio

    tab.row_append(['piz', lratio/ratio])

    h_ppiz_c['mc'].Scale(lratio)
    h_ppiz_c['mc'].Draw('SAME')

    tab.column_trim('Data/MC', rnd='.0001')

    figname = '%s_momentacor' % sname
    epsfile = set_file(extbase=figpath, comname=figname, ext='eps')
    c1.Print(epsfile)
    tools.eps2pdf(epsfile)

    tabname = '%s_syst' % sname
    tab.output(tabname, label=label, export_html=False)

    
def read_hists(datatype, mode, label, test):
    
    h_mbc = {}; kpi1 = {} ; pipih = {}; 
    kpiz = {}; kpipih = {}; 
    h_pk = {}; h_ppi1 = {}; h_ppiz = {}
    h_pk_c = {}; h_ppi1_c = {}; h_ppiz_c = {}
    h_pk_sb = {}; h_ppi1_sb = {}; h_ppiz_sb = {}
    h_pk_sb_c = {}; h_ppi1_sb_c = {}; h_ppiz_sb_c = {}
    h_angk = {}; h_angpi1 = {}; h_angpiz = {}


def fit_mbc():
    from tools import normalizedRooFitIntegral, RooFitIntegral
    from ROOT import RooRealVar, RooDataSet, RooArgList, RooArgSet, \
         RooGaussian, RooArgusBG, RooCBShape, RooAddPdf, RooPolynomial, \
         RooDataHist, RooFit, kTRUE, kFALSE

    signal_margins = [1.86, 1.87]
    sb_margins = [1.84, 1.85]

    # Right here we compute background yield
    mbc = RooRealVar('mbc', 'mbc', 1.83, 1.89, 'GeV')
    arg_cutoff = RooRealVar('arg_cutoff', 'Argus cutoff', 1.8869, 1.885, 1.888, 'GeV')
    arg_slope = RooRealVar('arg_slope', 'Argus slope', -13, -100, -1)
    mbc_d0 = RooRealVar('mbc_d0', 'D0 Mbc', 1.8647, 'GeV')
    mbc_dp = RooRealVar('mbc_dp', 'D+ Mbc', 1.8694, 'GeV')
    mbc_float = RooRealVar('mbc_float', 'Floating D mass', 1.869, 1.855, 1.875, 'GeV')
    sigma = RooRealVar('sigma', 'D width', 0.00145, 0.0001, 0.0025, 'GeV')
    sigma2 = RooRealVar('sigma2', 'CB width', 0.00145, 0.0001, 0.005,
                        'GeV')
    alpha = RooRealVar('alpha', 'CB shape cutoff', -1.515, -2., 2)
    n = RooRealVar('n', 'CB tail parameter', 6, 0, 20)
    gauss_d0 = RooGaussian('gauss_d0', 'D0 gaussian', mbc, mbc_d0, sigma2)
    gauss_dp = RooGaussian('gauss_dp', 'D+ gaussian', mbc, mbc_dp, sigma2)
    gauss_float = RooGaussian('gauss_float', 'Floating gaussian',
                                                    mbc, mbc_float, sigma2)
    cb_d0 = RooCBShape('cb_d0', 'D0 Crystal Barrel', mbc,
                   mbc_d0, sigma, alpha, n)
    cb_dp = RooCBShape('cb_dp', 'D+ Crystal Barrel', mbc,
                       mbc_dp, sigma, alpha, n)
    cb_float = RooCBShape('cb_float', 'Floating Crystal Barrel', mbc,
                          mbc_float, sigma, alpha, n)
    argus = RooArgusBG('argus', 'Argus BG', mbc, arg_cutoff, arg_slope)
    yld = RooRealVar('yield', 'D yield', 25700, 0, 100000)
    yld2 = RooRealVar('yield2', '2nd yield', 100, 0, 2000)
    bkg = RooRealVar('bkg', 'Background', 1300, 0, 40000)
    a = RooRealVar('a', 'Norm', 1)
    poly = RooPolynomial('poly', 'poly PDF', mbc, RooArgList(a), 0)
    sumpdf_d0 = RooAddPdf('sumpdf_d0', 'D0 sum pdf',
                          RooArgList(cb_d0, argus),
                          RooArgList(yld, bkg))
    sumpdf_dp = RooAddPdf('sumpdf_dp', 'Dp sum pdf',
                          RooArgList(cb_dp, argus),
                          RooArgList(yld, bkg))
    sumpdf_float = RooAddPdf('sumpdf_float', 'Generic D sum pdf',
                             RooArgList(cb_float, argus),
                             RooArgList(yld, bkg))

    width_modes = { '0': 0.00150, '1': 0.001831, '3': 0.001426, '200': 0.001387,
                    '202': 0.001407 }

    n_modes = { '0': 2.68, '1': 4.06, '3': 4.34, '200': 4.05, '202': 5.26 }
    alpha_modes = { '0': -1.6145, '1': -1.4562, '3': -1.5834, '200': -1.6538,
                    '202': -1.5598 }


    pdf = sumpdf_float


    sigma.setVal(width_modes['1']) # sigma.setConstant()


    n.setVal(n_modes['1']) #n.setConstant()

    alpha.setVal(alpha_modes['1']) #alpha.setConstant()
    #sigma.setConstant()
    #arg_cutoff.setVal(1.8865); #arg_cutoff.setConstant()

    c1.Divide(1,2)
    c1.cd(1)
    dset = RooDataHist('dsetmc', 'title', RooArgList(mbc), h_mbc['mc'])

    #pdf.fitTo(dset, 'eq')
    Extended = RooFit.Extended(kTRUE) # e
    Verbose = RooFit.Verbose(kFALSE) #q

    pdf.fitTo(dset, Extended, Verbose)

    # xframe = mbc.frame()
    # dset.plotOn(xframe)
    # pdf.plotOn(xframe)
    # pdf.paramOn(xframe,dset)
    # xframe.SetTitle('Fake type 1, MC')
    # xframe.Draw()
    c1.cd(2)
    dset = RooDataHist('dsetdata', 'title', RooArgList(mbc), h_mbc['data'])
    #pdf.fitTo(dset, 'eq')
    pdf.fitTo(dset, Extended, Verbose)
    # xframe = mbc.frame()
    # dset.plotOn(xframe)
    # pdf.plotOn(xframe)
    # pdf.paramOn(xframe,dset)
    # xframe.SetTitle('Fake type 1, data')
    # xframe.Draw()
    sb_scale = (normalizedRooFitIntegral(argus, mbc, signal_margins[0],
                                         signal_margins[1])/
                normalizedRooFitIntegral(argus, mbc, sb_margins[0], sb_margins[1]))


def draw_momenta_k3pi(datatype, mode, label, test):
    modekey = tools.get_modekey(mode)
    sname = attr.modes[modekey]['sname'].lower()
    figname = '%s_momenta' % sname
    figpath = os.path.join(attr.figpath, label, 'trkmtm')
    epsfile = set_file(extbase=figpath, comname=figname, ext='eps')
    tab = DHadTable()
    tab.row_append(['Name', 'Data/MC'])
                   
    # --------------------------------------------------
    h_pk = {}; h_ppi1 = {}; h_ppi2 = {}; h_ppim = {}
    h_pk_c = {}; h_ppi1_c = {}; h_ppi2_c = {}; h_ppim_c = {}

    for datatype in datatype.split('/'):
        selfile = get_selfile(datatype, mode, label, test=test)
        selfile = selfile.replace('/trkmtm/', '/trkmtm2/')

        f = TFile(selfile)
        if datatype == 'signal' or datatype == 'generic':
            tp = 'mc'
        if datatype == 'data':
            tp = 'data'

        h_pk[tp]= f.Get('h_pk'+tp)
        h_ppi1[tp]= f.Get('h_ppi1'+tp)
        h_ppi2[tp]= f.Get('h_ppi2'+tp)
        h_ppim[tp]= f.Get('h_ppim'+tp)
        
        h_pk_c[tp]= f.Get('h_pk_c'+tp)
        h_ppi1_c[tp]= f.Get('h_ppi1_c'+tp)
        h_ppi2_c[tp]= f.Get('h_ppi2_c'+tp)
        h_ppim_c[tp]= f.Get('h_ppim_c'+tp)

        f.Clear()

    ratio = h_pk['data'].Integral()/h_pk['mc'].Integral()

    c1 = TCanvas('c1', 'canvas', 900, 900)
    c1.Divide(2,2)
    c1.cd(1)
    h_pk['data'].Draw('PE')
    h_pk['mc'].Scale(ratio)
    h_pk['mc'].Draw('SAME')
    c1.cd(2)
    h_ppi1['data'].Draw('PE')
    h_ppi1['mc'].Scale(ratio)
    h_ppi1['mc'].Draw('SAME')
    c1.cd(3)
    h_ppi2['data'].Draw('PE')
    h_ppi2['mc'].Scale(ratio)
    h_ppi2['mc'].Draw('SAME')
    c1.cd(4)
    h_ppim['data'].Draw('PE')
    h_ppim['mc'].Scale(ratio)
    h_ppim['mc'].Draw('SAME')

    c1.Print(epsfile)
    tools.eps2pdf(epsfile)

    # --------------------------------------------------

    c1.Clear()
    c1.Divide(2,2)

    c1.cd(1)
    h_pk_c['data'].Draw('PE')
    lratio = h_pk_c['data'].Integral()/h_pk_c['mc'].Integral()
    #print 'k:', lratio/ratio
    tab.row_append(['K', lratio/ratio])

    h_pk_c['mc'].Scale(lratio)
    h_pk_c['mc'].Draw('SAME')
    c1.cd(2)
    h_ppi1_c['data'].Draw('PE')
    lratio = h_ppi1_c['data'].Integral()/h_ppi1_c['mc'].Integral()
    #print 'pi1:', lratio/ratio
    tab.row_append(['pi1', lratio/ratio])

    h_ppi1_c['mc'].Scale(lratio)
    h_ppi1_c['mc'].Draw('SAME')
    c1.cd(3)
    h_ppi2_c['data'].Draw('PE')
    lratio = h_ppi2_c['data'].Integral()/h_ppi2_c['mc'].Integral()
    #print 'pi2:', lratio/ratio
    tab.row_append(['pi2', lratio/ratio])

    h_ppi2_c['mc'].Scale(lratio)
    h_ppi2_c['mc'].Draw('SAME')
    c1.cd(4)
    h_ppim_c['data'].Draw('PE')
    lratio = h_ppim_c['data'].Integral()/h_ppim_c['mc'].Integral()
    #print 'pim:', lratio/ratio
    tab.row_append(['pim', lratio/ratio])
    
    h_ppim_c['mc'].Scale(lratio)
    h_ppim_c['mc'].Draw('SAME')

    tab.column_trim('Data/MC', rnd='.0001')

    figname = '%s_momentacor' % sname
    epsfile = set_file(extbase=figpath, comname=figname, ext='eps')
    c1.Print(epsfile)
    tools.eps2pdf(epsfile)

    tabname = '%s_syst' % sname
    tab.output(tabname, label=label, export_html=False)


def draw_momenta_kpipi(datatype, mode, label, test):
    modekey = tools.get_modekey(mode)
    sname = attr.modes[modekey]['sname'].lower()
    figname = '%s_momenta' % sname
    figpath = os.path.join(attr.figpath, label, 'trkmtm')
    epsfile = set_file(extbase=figpath, comname=figname, ext='eps')
    tab = DHadTable()
    tab.row_append(['Name', 'Data/MC'])
                   
    # --------------------------------------------------
    h_pk = {}; h_ppi1 = {}; h_ppi2 = {}
    h_pk_c = {}; h_ppi1_c = {}; h_ppi2_c = {}

    for datatype in datatype.split('/'):
        selfile = get_selfile(datatype, mode, label, test=test)
        selfile = selfile.replace('/trkmtm/', '/trkmtm2/')

        f = TFile(selfile)
        if datatype == 'signal' or datatype == 'generic':
            tp = 'mc'
        if datatype == 'data':
            tp = 'data'

        h_pk[tp]= f.Get('h_pk'+tp)
        h_ppi1[tp]= f.Get('h_ppi1'+tp)
        h_ppi2[tp]= f.Get('h_ppi2'+tp)

        h_pk_c[tp]= f.Get('h_pk_c'+tp)
        h_ppi1_c[tp]= f.Get('h_ppi1_c'+tp)
        h_ppi2_c[tp]= f.Get('h_ppi2_c'+tp)

        f.Clear()

    ratio = h_pk['data'].Integral()/h_pk['mc'].Integral()

    c1 = TCanvas('c1', 'canvas', 900, 900)
    c1.Divide(2,2)
    c1.cd(1)
    h_pk['data'].Draw('PE')
    h_pk['mc'].Scale(ratio)
    h_pk['mc'].Draw('SAME')
    c1.cd(2)
    h_ppi1['data'].Draw('PE')
    h_ppi1['mc'].Scale(ratio)
    h_ppi1['mc'].Draw('SAME')
    c1.cd(3)
    h_ppi2['data'].Draw('PE')
    h_ppi2['mc'].Scale(ratio)
    h_ppi2['mc'].Draw('SAME')

    c1.Print(epsfile)
    tools.eps2pdf(epsfile)

    # --------------------------------------------------
    c1.Clear()
    c1.Divide(2,2)
    c1.cd(1)
    h_pk_c['data'].Draw('PE')
    lratio = h_pk_c['data'].Integral()/h_pk_c['mc'].Integral()
    #print 'k:', lratio/ratio
    tab.row_append(['K', lratio/ratio])
    h_pk_c['mc'].Scale(lratio)
    h_pk_c['mc'].Draw('SAME')
    c1.cd(2)
    h_ppi1_c['data'].Draw('PE')
    lratio = h_ppi1_c['data'].Integral()/h_ppi1_c['mc'].Integral()
    #print 'pi1:', lratio/ratio
    tab.row_append(['pi1', lratio/ratio])
    h_ppi1_c['mc'].Scale(lratio)
    h_ppi1_c['mc'].Draw('SAME')
    c1.cd(3)
    h_ppi2_c['data'].Draw('PE')
    lratio = h_ppi2_c['data'].Integral()/h_ppi2_c['mc'].Integral()
    #print 'pi2:', lratio/ratio
    tab.row_append(['pi2', lratio/ratio])
    h_ppi2_c['mc'].Scale(lratio)
    h_ppi2_c['mc'].Draw('SAME')
    c1.cd(4)

    tab.column_trim('Data/MC', rnd='.0001')

    figname = '%s_momentacor' % sname
    epsfile = set_file(extbase=figpath, comname=figname, ext='eps')
    c1.Print(epsfile)
    tools.eps2pdf(epsfile)

    tabname = '%s_syst' % sname
    tab.output(tabname, label=label, export_html=False)


def draw_momenta_kpipipi0(datatype, mode, label, test):
    modekey = tools.get_modekey(mode)
    sname = attr.modes[modekey]['sname'].lower()
    figname = '%s_momenta' % sname
    figpath = os.path.join(attr.figpath, label, 'trkmtm')
    epsfile = set_file(extbase=figpath, comname=figname, ext='eps')
    tab = DHadTable()
    tab.row_append(['Name', 'Data/MC'])
                   
    # --------------------------------------------------
    h_pk = {}; h_ppi1 = {}; h_ppi2 = {}; h_ppiz = {}
    h_pk_c = {}; h_ppi1_c = {}; h_ppi2_c = {}; h_ppiz_c = {}

    for datatype in datatype.split('/'):
        selfile = get_selfile(datatype, mode, label, test=test)
        selfile = selfile.replace('/trkmtm/', '/trkmtm2/')

        f = TFile(selfile)
        if datatype == 'signal' or datatype == 'generic':
            tp = 'mc'
        if datatype == 'data':
            tp = 'data'

        h_pk[tp]= f.Get('h_pk'+tp)
        h_ppi1[tp]= f.Get('h_ppi1'+tp)
        h_ppi2[tp]= f.Get('h_ppi2'+tp)
        h_ppiz[tp]= f.Get('h_ppiz'+tp)

        h_pk_c[tp]= f.Get('h_pk_c'+tp)
        h_ppi1_c[tp]= f.Get('h_ppi1_c'+tp)
        h_ppi2_c[tp]= f.Get('h_ppi2_c'+tp)
        h_ppiz_c[tp]= f.Get('h_ppiz_c'+tp)

        f.Clear()

    ratio = h_pk['data'].Integral()/h_pk['mc'].Integral()

    c1 = TCanvas('c1', 'canvas', 900, 900)
    c1.Divide(2,2)
    c1.cd(1)
    h_pk['data'].Draw('PE')
    h_pk['mc'].Scale(ratio)
    h_pk['mc'].Draw('SAME')
    c1.cd(2)
    h_ppi1['data'].Draw('PE')
    h_ppi1['mc'].Scale(ratio)
    h_ppi1['mc'].Draw('SAME')
    c1.cd(3)
    h_ppi2['data'].Draw('PE')
    h_ppi2['mc'].Scale(ratio)
    h_ppi2['mc'].Draw('SAME')
    c1.cd(4)
    h_ppiz['data'].Draw('PE')
    h_ppiz['mc'].Scale(ratio)
    h_ppiz['mc'].Draw('SAME')

    c1.Print(epsfile)
    tools.eps2pdf(epsfile)

    # --------------------------------------------------
    c1.Clear()
    c1.Divide(2,2)

    c1.cd(1)
    h_pk_c['data'].Draw('PE')
    lratio = h_pk_c['data'].Integral()/h_pk_c['mc'].Integral()
    #print 'k:', lratio/ratio
    tab.row_append(['K', lratio/ratio])

    h_pk_c['mc'].Scale(ratio)
    h_pk_c['mc'].Draw('SAME')
    c1.cd(2)
    h_ppi1_c['data'].Draw('PE')
    lratio = h_ppi1_c['data'].Integral()/h_ppi1_c['mc'].Integral()
    #print 'pi1:', lratio/ratio
    tab.row_append(['pi1', lratio/ratio])

    h_ppi1_c['mc'].Scale(ratio)
    h_ppi1_c['mc'].Draw('SAME')
    c1.cd(3)
    h_ppi2_c['data'].Draw('PE')
    lratio = h_ppi2_c['data'].Integral()/h_ppi2_c['mc'].Integral()
    #print 'pi2:', lratio/ratio
    tab.row_append(['pi2', lratio/ratio])

    h_ppi2_c['mc'].Scale(ratio)
    h_ppi2_c['mc'].Draw('SAME')
    c1.cd(4)
    h_ppiz_c['data'].Draw('PE')
    lratio = h_ppiz_c['data'].Integral()/h_ppiz_c['mc'].Integral()
    #print 'piz:', lratio/ratio
    tab.row_append(['piz', lratio/ratio])

    h_ppiz_c['mc'].Scale(ratio)
    h_ppiz_c['mc'].Draw('SAME')

    tab.column_trim('Data/MC', rnd='.0001')

    figname = '%s_momentacor' % sname
    epsfile = set_file(extbase=figpath, comname=figname, ext='eps')
    c1.Print(epsfile)
    tools.eps2pdf(epsfile)

    tabname = '%s_syst' % sname
    tab.output(tabname, label=label, export_html=False)

    
def draw_momenta_kspipi0(datatype, mode, label, test):
    modekey = tools.get_modekey(mode)
    sname = attr.modes[modekey]['sname'].lower()
    figname = '%s_momenta' % sname
    figpath = os.path.join(attr.figpath, label, 'trkmtm')
    epsfile = set_file(extbase=figpath, comname=figname, ext='eps')
    tab = DHadTable()
    tab.row_append(['Name', 'Data/MC'])
                   
    # --------------------------------------------------
    h_pks = {}; h_ppi1 = {}; h_ppiz = {}
    h_pks_c = {}; h_ppi1_c = {}; h_ppiz_c = {}

    for datatype in datatype.split('/'):
        selfile = get_selfile(datatype, mode, label, test=test)
        selfile = selfile.replace('/trkmtm/', '/trkmtm2/')

        f = TFile(selfile)
        if datatype == 'signal' or datatype == 'generic':
            tp = 'mc'
        if datatype == 'data':
            tp = 'data'

        h_pks[tp]= f.Get('h_pks'+tp)
        h_ppi1[tp]= f.Get('h_ppi1'+tp)
        h_ppiz[tp]= f.Get('h_ppiz'+tp)

        h_pks_c[tp]= f.Get('h_pks_c'+tp)
        h_ppi1_c[tp]= f.Get('h_ppi1_c'+tp)
        h_ppiz_c[tp]= f.Get('h_ppiz_c'+tp)

        f.Clear()

    ratio = h_pks['data'].Integral()/h_pks['mc'].Integral()

    c1 = TCanvas('c1', 'canvas', 900, 900)
    c1.Divide(2,2)
    c1.cd(1)
    h_pks['data'].Draw('PE')
    h_pks['mc'].Scale(ratio)
    h_pks['mc'].Draw('SAME')
    c1.cd(2)
    h_ppi1['data'].Draw('PE')
    h_ppi1['mc'].Scale(ratio)
    h_ppi1['mc'].Draw('SAME')
    c1.cd(3)
    c1.cd(4)
    h_ppiz['data'].Draw('PE')
    h_ppiz['mc'].Scale(ratio)
    h_ppiz['mc'].Draw('SAME')

    c1.Print(epsfile)
    tools.eps2pdf(epsfile)

    # --------------------------------------------------
    c1.Clear()
    c1.Divide(2,2)
    c1.cd(1)
    h_pks_c['data'].Draw('PE')
    lratio = h_pks_c['data'].Integral()/h_pks_c['mc'].Integral()
    #print 'k:', lratio/ratio
    tab.row_append(['K', lratio/ratio])

    h_pks_c['mc'].Scale(lratio)
    h_pks_c['mc'].Draw('SAME')
    c1.cd(2)
    h_ppi1_c['data'].Draw('PE')
    lratio = h_ppi1_c['data'].Integral()/h_ppi1_c['mc'].Integral()
    #print 'pi1:', lratio/ratio
    tab.row_append(['pi1', lratio/ratio])

    h_ppi1_c['mc'].Scale(lratio)
    h_ppi1_c['mc'].Draw('SAME')
    c1.cd(3)
    c1.cd(4)
    h_ppiz_c['data'].Draw('PE')
    lratio = h_ppiz_c['data'].Integral()/h_ppiz_c['mc'].Integral()
    #print 'piz:', lratio/ratio
    tab.row_append(['piz', lratio/ratio])
    
    h_ppiz_c['mc'].Scale(lratio)
    h_ppiz_c['mc'].Draw('SAME')

    tab.column_trim('Data/MC', rnd='.0001')

    figname = '%s_momentacor' % sname
    epsfile = set_file(extbase=figpath, comname=figname, ext='eps')
    c1.Print(epsfile)
    tools.eps2pdf(epsfile)

    tabname = '%s_syst' % sname
    tab.output(tabname, label=label, export_html=False)
       

def draw_momenta_ks3pi(datatype, mode, label, test):
    modekey = tools.get_modekey(mode)
    sname = attr.modes[modekey]['sname'].lower()
    figname = '%s_momenta' % sname
    figpath = os.path.join(attr.figpath, label, 'trkmtm')
    epsfile = set_file(extbase=figpath, comname=figname, ext='eps')
    tab = DHadTable()
    tab.row_append(['Name', 'Data/MC'])
                   
    # --------------------------------------------------
    h_pks = {}; h_ppi1 = {}; h_ppi2 = {}; h_ppim = {}
    h_pks_c = {}; h_ppi1_c = {}; h_ppi2_c = {}; h_ppim_c = {}

    for datatype in datatype.split('/'):
        selfile = get_selfile(datatype, mode, label, test=test)
        selfile = selfile.replace('/trkmtm/', '/trkmtm2/')

        f = TFile(selfile)
        if datatype == 'signal' or datatype == 'generic':
            tp = 'mc'
        if datatype == 'data':
            tp = 'data'

        h_pks[tp]= f.Get('h_pks'+tp)
        h_ppi1[tp]= f.Get('h_ppi1'+tp)
        h_ppi2[tp]= f.Get('h_ppi2'+tp)
        h_ppim[tp]= f.Get('h_ppim'+tp)

        h_pks_c[tp]= f.Get('h_pk_c'+tp)
        h_ppi1_c[tp]= f.Get('h_ppi1_c'+tp)
        h_ppi2_c[tp]= f.Get('h_ppi2_c'+tp)
        h_ppim_c[tp]= f.Get('h_ppim_c'+tp)

        f.Clear()

    ratio = h_pks['data'].Integral()/h_pks['mc'].Integral()

    c1 = TCanvas('c1', 'canvas', 900, 900)
    c1.Divide(2,2)
    c1.cd(1)
    h_pks['data'].Draw('PE')
    h_pks['mc'].Scale(ratio)
    h_pks['mc'].Draw('SAME')
    c1.cd(2)
    h_ppi1['data'].Draw('PE')
    h_ppi1['mc'].Scale(ratio)
    h_ppi1['mc'].Draw('SAME')
    c1.cd(3)
    h_ppi2['data'].Draw('PE')
    h_ppi2['mc'].Scale(ratio)
    h_ppi2['mc'].Draw('SAME')
    c1.cd(4)
    h_ppim['data'].Draw('PE')
    h_ppim['mc'].Scale(ratio)
    h_ppim['mc'].Draw('SAME')

    c1.Print(epsfile)
    tools.eps2pdf(epsfile)

    # --------------------------------------------------
    c1.Clear()
    c1.Divide(2,2)

    c1.cd(1)
    h_pks_c['data'].Draw('PE')
    lratio = h_pks_c['data'].Integral()/h_pks_c['mc'].Integral()
    #print 'k:', lratio/ratio
    tab.row_append(['K', lratio/ratio])

    h_pks_c['mc'].Scale(lratio)
    h_pks_c['mc'].Draw('SAME,HIST')
    c1.cd(2)
    h_ppi1_c['data'].Draw('PE')
    lratio = h_ppi1_c['data'].Integral()/h_ppi1_c['mc'].Integral()
    #print 'pi1:', lratio/ratio
    tab.row_append(['pi1', lratio/ratio])

    h_ppi1_c['mc'].Scale(lratio)
    h_ppi1_c['mc'].Draw('SAME,HIST')
    c1.cd(3)
    h_ppi2_c['data'].Draw('PE')
    lratio = h_ppi2_c['data'].Integral()/h_ppi2_c['mc'].Integral()
    #print 'pi2:', lratio/ratio
    tab.row_append(['pi2', lratio/ratio])

    h_ppi2_c['mc'].Scale(lratio)
    h_ppi2_c['mc'].Draw('SAME,HIST')
    c1.cd(4)
    h_ppim_c['data'].Draw('PE')
    lratio = h_ppim_c['data'].Integral()/h_ppim_c['mc'].Integral()
    #print 'pim:', lratio/ratio
    tab.row_append(['pim', lratio/ratio])

    h_ppim_c['mc'].Scale(lratio)
    h_ppim_c['mc'].Draw('SAME,HIST')
    
    tab.column_trim('Data/MC', rnd='.0001')

    figname = '%s_momentacor' % sname
    epsfile = set_file(extbase=figpath, comname=figname, ext='eps')
    c1.Print(epsfile)
    tools.eps2pdf(epsfile)

    tabname = '%s_syst' % sname
    tab.output(tabname, label=label, export_html=False)


def draw_momenta_kkpi(figpath, datatype, mode, label, test):
    modekey = tools.get_modekey(mode)
    sname = attr.modes[modekey]['sname'].lower()
    figname = '%s_momenta' % sname

    epsfile = set_file(extbase=figpath, comname=figname, ext='eps')

    #tab = DHadTable()
    #tab.row_append(['Name', 'Data/MC'])
                   
    # --------------------------------------------------
    h_pkm = {}; h_pkp = {}; h_ppi = {}
    h_pkm_c = {}; h_pkp_c = {}; h_ppi_c = {}

    for datatype in [datatype]:
        selfile = get_selfile(datatype, mode, label, test=test)
        selfile = selfile.replace('/trkmtm/', '/trkmtm2/')

        f = TFile(selfile)
        if datatype == 'signal': # or datatype == 'generic':
            tp = 'mc'
        #if datatype == 'data':
        #    tp = 'data'

        h_pkm[tp]= f.Get('h_pk'+tp)
        h_pkp[tp]= f.Get('h_ppi1'+tp)
        h_ppi[tp]= f.Get('h_ppiz'+tp)

        h_pkm_c[tp]= f.Get('h_pk_c'+tp)
        h_pkp_c[tp]= f.Get('h_ppi1_c'+tp)
        h_ppi_c[tp]= f.Get('h_ppiz_c'+tp)

        f.Clear()

    #ratio = h_pkm['data'].Integral()/h_pkm['mc'].Integral()

    c1 = TCanvas('c1', 'canvas', 900, 900)
    c1.Divide(2,2)
    c1.cd(1)
    h_pkm['mc'].Draw()
    #h_pkm['data'].Draw('PE')
    #h_pkm['mc'].Scale(ratio)
    #h_pkm['mc'].Draw('SAME')
    c1.cd(2)
    h_pkp['mc'].Draw()
    #h_pkp['data'].Draw('PE')
    #h_pkp['mc'].Scale(ratio)
    #h_pkp['mc'].Draw('SAME')
    c1.cd(3)
    c1.cd(4)
    h_ppi['mc'].Draw()
    #h_ppi['data'].Draw('PE')
    #h_ppi['mc'].Scale(ratio)
    #h_ppi['mc'].Draw('SAME')

    c1.Print(epsfile)
    tools.eps2pdf(epsfile)

    # # --------------------------------------------------
    # c1.Clear()
    # c1.Divide(2,2)

    # c1.cd(1)
    # h_pkm_c['data'].Draw('PE')
    # lratio = h_pkm_c['data'].Integral()/h_pkm_c['mc'].Integral()
    # #print 'km:', lratio/ratio
    # tab.row_append(['Km', lratio/ratio])

    # h_pkm_c['mc'].Scale(lratio)
    # h_pkm_c['mc'].Draw('SAME')


    # c1.cd(2)
    # h_pkp_c['data'].Draw('PE')
    # lratio = h_pkp_c['data'].Integral()/h_pkp_c['mc'].Integral()
    # #print 'kp:', lratio/ratio
    # tab.row_append(['Kp', lratio/ratio])

    # h_pkp_c['mc'].Scale(lratio)
    # h_pkp_c['mc'].Draw('SAME')

    # c1.cd(3)
    # c1.cd(4)
    # h_ppi_c['data'].Draw('PE')
    # lratio = h_ppi_c['data'].Integral()/h_ppi_c['mc'].Integral()
    # #print 'pi:', lratio/ratio
    # tab.row_append(['pi', lratio/ratio])

    # h_ppi_c['mc'].Scale(lratio)
    # h_ppi_c['mc'].Draw('SAME')

    # tab.column_trim('Data/MC', rnd='.0001')

    # figname = '%s_momentacor' % sname
    # epsfile = set_file(extbase=figpath, comname=figname, ext='eps')
    # c1.Print(epsfile)
    # tools.eps2pdf(epsfile)

    # tabname = '%s_syst' % sname
    # tab.output(tabname, label=label, export_html=False)
    
