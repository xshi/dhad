"""
Module for Sidebands Study

"""

import os
import sys
import ROOT
import attr
import tools

from yld import parse_args
from fit import create_bash_file, load_roofit_lib
from tools.filetools import UserFile
from tools import set_file, DHadTable


__author__ = "Xin Shi <xs32@cornell.edu>"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2005-2011 Xin Shi"
__license__ = "GPL"
__revision__ = "$Revision$"


def main(opts, args):
    parsed = parse_args(args)
    datatype  = parsed[0]
    tag       = parsed[1]
    modes     = parsed[2]
    label     = parsed[3]

    debug = opts.debug
    test = opts.test
    
    for mode in modes:
        if opts.set and opts.set == 'interact':
            fit_sidebands_single_mode(datatype, mode, label, test)
        else:
            submit_batch_job(datatype, mode, label, opts)


def fit_sidebands_single_mode(datatype, mode, label, test):
    load_roofit_lib(datatype, label)

    dt_type=datatype.replace('/', '_')
    modekey = tools.get_modekey(mode)
    
    comname = '%s_%s' %(dt_type, mode)
    input_label = label

    sdbpath = os.path.join(attr.evtpath, input_label)
    sdbfile = set_file(extbase=sdbpath, comname=comname, ext='evt')

    has_charge_conjugate = False
    if '__' in mode:
        has_charge_conjugate = True
    
    if not os.access(sdbfile, os.F_OK):
        if has_charge_conjugate:
            sdbfile = set_file(extbase=sdbpath, dt_type=dt_type,
                               tag='s', mode=modekey, 
                               comname=comname, ext='evt', forceCombine=1)
        else:
            raise ValueError(sdbfile)
        
    epspath = os.path.join(attr.figpath, label)    
    epsfile = set_file(extbase=epspath, comname=comname, ext='eps')

    txtpath = os.path.join(attr.fitpath, label)    
    txtfile = set_file(extbase=txtpath, comname=comname, ext='txt')

    if test:
        epsfile = epsfile + '.test'
        txtfile = txtfile + '.test'

    ROOT.gROOT.SetBatch(1)
    ROOT.gROOT.SetStyle('Plain')

    mbc = ROOT.RooRealVar('mbc', 'Beam constrained mass', 1.83, 1.89, 'GeV')
    mbc_aset = ROOT.RooArgSet(mbc)

    ebeam = ROOT.RooRealVar('ebeam', 'Ebeam', 1.8815, 1.892, 'GeV')

    dflav = ROOT.RooCategory('dflav','D0 flavor')

    dflav.defineType('dflav',1)
    dflav.defineType('dbarflav',-1)

    dataset_args = ROOT.RooArgList(mbc, ebeam, dflav)

    dataset = ROOT.RooDataSet.read(sdbfile, dataset_args)

    arg_cutoff = ebeam
    arg_slope = ROOT.RooRealVar('arg_slope', 'Argus slope', -10, -100, -1)
    arg_power = ROOT.RooRealVar('arg_power', 'Argus power', 0.5, 0.1, 1.5)
    
    yld = ROOT.RooRealVar('yield', 'D yield', 100, 0, 200000)
    bkg = ROOT.RooRealVar('bkg', 'Background', 100, 0, 1000000)

    sigma = ROOT.RooRealVar('sigma', 'D width', 0.0001, 0.005, 'GeV')

    pars = [arg_slope, arg_power, bkg, sigma, yld]
    
    mbc_d0 = ROOT.RooRealVar('mbc_d0', 'D0 Mbc', 1.8647, 'GeV')
    mbc_dp = ROOT.RooRealVar('mbc_dp', 'D+ Mbc', 1.8694, 'GeV')
    
    gauss_d0 = ROOT.RooGaussian('gauss_d0', 'D0 gaussian', mbc, mbc_d0, sigma)
    gauss_dp = ROOT.RooGaussian('gauss_dp', 'D+ gaussian', mbc, mbc_dp, sigma)

    argus = ROOT.RooArgusBG('argus', 'Argus BG', mbc, arg_cutoff, arg_slope,
                            arg_power)
    sumpdf_d0 = ROOT.RooAddPdf('sumpdf_d0', 'D0 sum pdf',
                          ROOT.RooArgList(gauss_d0, argus),
                          ROOT.RooArgList(yld, bkg))
    sumpdf_dp = ROOT.RooAddPdf('sumpdf_dp', 'Dp sum pdf',
                               ROOT.RooArgList(gauss_dp, argus),
                               ROOT.RooArgList(yld, bkg))


    Extended = ROOT.RooFit.Extended(ROOT.kTRUE)  # e
    Save = ROOT.RooFit.Save(ROOT.kTRUE)          # r
    Hesse = ROOT.RooFit.Hesse(ROOT.kFALSE)       # no h
    Verbose = ROOT.RooFit.Verbose(ROOT.kFALSE)   # no q 

    if 'D0' in mode:
        pdf = sumpdf_d0
    else:
        pdf = sumpdf_dp


    if has_charge_conjugate:
        yld_bar = ROOT.RooRealVar('yield_bar', 'Dbar yield', 100, 0, 200000)
        bkg_bar = ROOT.RooRealVar('bkg_bar', 'Background Bar', 100, 0, 1000000)
        pars.extend([yld_bar, bkg_bar])

        mbc_d0bar = ROOT.RooRealVar('mbc_d0bar', 'D0Bar Mbc', 1.8647, 'GeV')
        mbc_dm = ROOT.RooRealVar('mbc_dm', 'D- Mbc', 1.8694, 'GeV')
        
        gauss_d0bar = ROOT.RooGaussian('gauss_d0bar', 'D0bar gaussian',
                                       mbc, mbc_d0bar, sigma)
        gauss_dm = ROOT.RooGaussian('gauss_dm', 'D- gaussian',
                                    mbc, mbc_dm, sigma)
        
        sumpdf_d0bar = ROOT.RooAddPdf('sumpdf_d0bar', 'D0bar sum pdf',
                                      ROOT.RooArgList(gauss_d0bar, argus),
                                      ROOT.RooArgList(yld_bar, bkg_bar))
        sumpdf_dm = ROOT.RooAddPdf('sumpdf_dm', 'Dm sum pdf',
                                   ROOT.RooArgList(gauss_dm, argus),
                                   ROOT.RooArgList(yld_bar, bkg_bar))

        pdf = ROOT.RooSimultaneous('totalPdf', 'totalPdf', dflav)

        if 'D0' in mode:
            pdf.addPdf(sumpdf_d0, 'dflav')
            pdf.addPdf(sumpdf_d0bar, 'dbarflav')
        else:
            pdf.addPdf(sumpdf_dp, 'dflav')
            pdf.addPdf(sumpdf_dm, 'dbarflav')
            

    if 'nogaus' in label:
        yld.setVal(1)
        yld.setConstant(ROOT.kTRUE)
        pars.remove(yld)

    if 'floatsigma' not in label:
        datatype = 'data'
        tag = 'single'

        if '818ipb' in label:
            prefix = 'dir_818ipbv12'
            frame_max = 1500 #bkg_generic_ddbar_818_max[mode]
        else:
            raise NameError(label)


        tabfile = set_file('txt', datatype, modekey, tag,
                           prefix=prefix,
                           extbase=attr.fitpath)

        sys.stdout.write('Using width from %s \n' %tabfile)
        tab = DHadTable(tabfile)
        sigmap1 = float(tab.cell_get('sigmap1', 'Value'))
        sigma.setVal(sigmap1)
        sigma.setConstant(ROOT.kTRUE)
        pars.remove(sigma)
        
    #res = pdf.fitTo(dataset, Extended, Save, Verbose)
    res = pdf.fitTo(dataset, 'emr') #Migrad only, no MINOS
    res.Print('v')


    if not has_charge_conjugate:
        canvas = ROOT.TCanvas('canvas', 'canvas1', 600, 600)
        canvas.SetFixedAspectRatio(0)
        
        xframe = mbc.frame()
        
        xframe.SetMaximum(frame_max)
        xframe.SetMarkerSize(0.3)
        dataset.plotOn(xframe)
        pdf.plotOn(xframe)
        nfitParam = len(pars)
        chisq_ndof = xframe.chiSquare(nfitParam)
        
        nbin = xframe.GetNbinsX()
        ndof = nbin - nfitParam
        chisq = chisq_ndof * ndof
    
        chisqbox = ROOT.TPaveText(0.1, 0.1, 0.4, 0.15, 'BRNDC')
        chisqbox.SetFillColor(0)
        chisqbox.SetBorderSize(1)
        chisqbox.AddText('#chi^{2}/ndof = %.2f/%d =  %.2f' %
                         (chisq, ndof, chisq_ndof))
        xframe.addObject(chisqbox)

        pdf.paramOn(xframe, dataset)        

        xframe.SetTitle('Sidebands of %s' % mode)
        xframe.GetYaxis().SetTitleSize(0.03) 
        xframe.GetYaxis().SetLabelSize(0.03) 
        xframe.GetYaxis().SetTitleOffset(1.8)
        xframe.GetXaxis().SetTitleSize(0.03) 
        xframe.GetXaxis().SetLabelSize(0.03) 
        xframe.GetXaxis().SetTitleOffset(1.2)
        xframe.Draw()
    else:
        canvas = ROOT.TCanvas('canvas','mbc', 1200, 400);
        canvas.Divide(3,1)
        title1 = attr.modes[modekey]['uname']
        title2 = attr.modes[modekey]['unamebar']
        
        canvas_1 = canvas.GetListOfPrimitives().FindObject('canvas_1')
        canvas_2 = canvas.GetListOfPrimitives().FindObject('canvas_2')
        canvas_1.SetLogy() 
        canvas_2.SetLogy()
        
        ebeam.setBins(900)

        canvas.cd(1)
        mbcFrame=mbc.frame()
        mbcFrame=mbc.frame(60)
        dflav.setLabel('dflav')
        ebeam_aset = ROOT.RooArgSet(ebeam, dflav)
        ebeamdata = ROOT.RooDataHist("ebeamdata", "ebeamdata", 
                                     ebeam_aset, dataset)

        Cut = ROOT.RooFit.Cut("dflav==dflav::dflav")

        LineColor = ROOT.RooFit.LineColor(ROOT.kRed)
        LineWidth = ROOT.RooFit.LineWidth(1)
        #Slice = ROOT.RooFit.Slice(dflav, 'dflav')
        Slice = ROOT.RooFit.Slice(dflav)

        ProjWData = ROOT.RooFit.ProjWData(ebeam_aset, ebeamdata)
        
        dataset.plotOn(mbcFrame, Cut)
        mbcFrame.getAttMarker().SetMarkerSize(0.6)
        mbcFrame.Draw()


        pdf.plotOn(mbcFrame, LineColor, LineWidth, Slice, ProjWData)

        nfitParam = len(pars) - 2
        chisq_ndof = mbcFrame.chiSquare(nfitParam)
        
        nbin = mbcFrame.GetNbinsX()
        ndof = nbin - nfitParam
        chisq = chisq_ndof * ndof
    
        chisqbox = ROOT.TPaveText(0.1, 0.1, 0.55, 0.2, 'BRNDC')
        chisqbox.SetFillColor(0)
        chisqbox.SetBorderSize(1)
        chisqbox.AddText('#chi^{2}/ndof = %.2f/%d =  %.2f' %
                         (chisq, ndof, chisq_ndof))

        mbcFrame.addObject(chisqbox)

        mbcFrame.SetTitle(title1)
        mbcFrame.Draw()

        canvas.cd(2)
        mbcFrame = mbc.frame()
        mbcFrame=mbc.frame(60)
        dflav.setLabel('dbarflav')

        ebeam_aset = ROOT.RooArgSet(ebeam, dflav)
        ebeamdata = ROOT.RooDataHist("ebeamdata", "ebeamdata", 
                                     ebeam_aset, dataset)

        Cut = ROOT.RooFit.Cut("dflav==dflav::dbarflav")

        LineColor = ROOT.RooFit.LineColor(ROOT.kRed)
        LineWidth = ROOT.RooFit.LineWidth(1)
        #Slice = ROOT.RooFit.Slice(dflav, 'dbarflav')
        Slice = ROOT.RooFit.Slice(dflav)

        ProjWData = ROOT.RooFit.ProjWData(ebeam_aset, ebeamdata)
        
        dataset.plotOn(mbcFrame, Cut)
        mbcFrame.getAttMarker().SetMarkerSize(0.6)
        mbcFrame.Draw()


        pdf.plotOn(mbcFrame, LineColor, LineWidth, Slice, ProjWData)

        nfitParam = len(pars) - 2
        chisq_ndof = mbcFrame.chiSquare(nfitParam)
        
        nbin = mbcFrame.GetNbinsX()
        ndof = nbin - nfitParam
        chisq = chisq_ndof * ndof
    
        chisqbox = ROOT.TPaveText(0.1, 0.1, 0.55, 0.2, 'BRNDC')
        chisqbox.SetFillColor(0)
        chisqbox.SetBorderSize(1)
        chisqbox.AddText('#chi^{2}/ndof = %.2f/%d =  %.2f' %
                         (chisq, ndof, chisq_ndof))

        mbcFrame.addObject(chisqbox)

        mbcFrame.SetTitle(title2)
        mbcFrame.Draw()


        canvas.cd(3)
        mbcFrame = mbc.frame()
        
        paramWin1 = pdf.paramOn(mbcFrame,dataset,
                                "",2,"NELU",0.1,0.9,0.9)
        mbcFrame.GetXaxis().SetLabelSize(0) 
        mbcFrame.GetXaxis().SetTickLength(0) 
        mbcFrame.GetXaxis().SetLabelSize(0) 
        mbcFrame.GetXaxis().SetTitle("") 
        mbcFrame.GetXaxis().CenterTitle() 
        
        mbcFrame.GetYaxis().SetLabelSize(0) 
        mbcFrame.GetYaxis().SetTitleSize(0.03) 
        mbcFrame.GetYaxis().SetTickLength(0) 
        
        paramWin1.getAttText().SetTextSize(0.06) 
        
        mbcFrame.Draw() 
        mbcFrame.SetTitle("Fit Parameters") 
        mbcFrame.Draw() 
 

    canvas.Print(epsfile)
    tools.save_fit_result(pars, txtfile)

    if not test:
        tools.eps2png(epsfile)
        tools.eps2pdf(epsfile)


def submit_batch_job(datatype, mode, label, opts):
    script = create_python_script(opts, datatype, mode, label)
    
    dt =  datatype.replace('/', '-')
    mode_sign = tools.get_modekey_sign(mode)
    ms = tools.pair_to_str(mode_sign)

    bash_file_name = 'fit-sidebands-%s-%s.sh' % (dt, ms)
    #bash_file = create_bash_file(script, bash_file_name, 'setpyroot l')
    bash_file = create_bash_file(opts, label, datatype, script, bash_file_name)

    logname = '%s_%s.txt' %(datatype.replace('/', '_'), mode)
    logfile = tools.set_file(extbase=attr.logpath, prefix='dir_'+label,
                             comname=logname)
    qjobname = 'sdb%s' % ms

    tools.qsub_jobs(logfile, qjobname, bash_file, opts.test)
    

def create_python_script(opts, dt_type, mode, label):
    content =  '''#!/usr/bin/env python

from fit import sidebands

sidebands.fit_sidebands_single_mode("%s", "%s", "%s", %s)

'''% (dt_type, mode, label, opts.test)

    mode_sign = tools.get_modekey_sign(mode)

    ms = tools.pair_to_str(mode_sign)

    filename = 'sidebands-%s-%s-%s.py' % (dt_type, ms, label)

    filename = filename.replace('/', '-')
    
    file_ = os.path.join(attr.datpath, dt_type, label, 'src', filename)
    
    verbose = opts.verbose
    if opts.test:
        verbose = 1

    f = UserFile()
    f.append(content) 
    f.output(file_, verbose=verbose)
    os.chmod(file_, 0755)
    return filename

