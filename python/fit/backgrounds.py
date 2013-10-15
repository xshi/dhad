"""
Module for Backgrounds Study

"""

import os
import sys
import time
import ROOT
import attr
import tools

from yld import parse_args
from fit import create_bash_file
from tools.filetools import UserFile
from attr.modes import bkg_generic_ddbar_281_max
from attr.modes import bkg_generic_ddbar_537_max
from attr.modes import bkg_generic_ddbar_818_max
from attr.modes import bkg_generic_ddbar_818_max_noxfeed
from tools import set_file, DHadTable, get_mode_root_name


__author__ = "Xin Shi <xs32@cornell.edu>"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2005-2010 Xin Shi"
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

    if 'allinone' in opts.set:
        if  'interact' in opts.set:
            fit_backgrounds_single(datatype, modes, label, test)
        else:
            submit_batch_job_allinone(datatype, modes, label, test)
        return
    
    for mode in modes:
        if opts.set and opts.set == 'interact':
            fit_backgrounds_single_mode(datatype, mode, label, test)
        else:
            submit_batch_job(datatype, mode, label, test)


def fit_backgrounds_single_mode(datatype, mode, label, test):
    comname = '%s_%s' %(datatype.replace('/', '_'), mode)
    input_label = label
    if 'nogaus' in label:
        input_label = label.split('/')[0]

    bkgpath = os.path.join(attr.bkgpath(), input_label)
    bkgfile = set_file(extbase=bkgpath, comname=comname, ext='evt')
    if not os.access(bkgfile, os.F_OK):
        input_prefix = 'dir_%s' % input_label
        bkgfile = set_file(extbase=attr.bkgpath(),
                           dt_type=datatype.replace('/', '_'),
                           tag='s', mode=mode, prefix=input_prefix,
                           comname=comname, ext='evt', forceCombine=1)

    epspath = os.path.join(attr.figpath, label)    
    epsfile = set_file(extbase=epspath, comname=comname, ext='eps')

    txtpath = os.path.join(attr.fitpath(), label)    
    txtfile = set_file(extbase=txtpath, comname=comname, ext='txt')

    if test:
        epsfile = epsfile + '.test'
        txtfile = txtfile + '.test'

    ROOT.gROOT.SetBatch(1)
    ROOT.gROOT.SetStyle('Plain')
    
    mbc = ROOT.RooRealVar('mbc', 'Beam constrained mass', 1.83, 1.89, 'GeV')
    mbc_aset = ROOT.RooArgSet(mbc)

    ebeam = ROOT.RooRealVar('ebeam','Ebeam',1.8815,1.892,'GeV')

    dflav = ROOT.RooCategory('dflav','D0 flavor')
    dflav.defineType('dflav',1)
    dflav.defineType('dbarflav',-1)

    dataset_args = ROOT.RooArgList(mbc, ebeam, dflav)

    dataset = ROOT.RooDataSet.read(bkgfile, dataset_args)


    arg_cutoff = ROOT.RooRealVar('arg_cutoff', 'Argus cutoff', 1.88, 1.89, 'GeV')
    arg_slope = ROOT.RooRealVar('arg_slope', 'Argus slope', -10, -100, -1)
    yld = ROOT.RooRealVar('yield', 'D yield', 100, 0, 200000)
    bkg = ROOT.RooRealVar('bkg', 'Background', 100, 0, 1000000)

    sigma = ROOT.RooRealVar('sigma', 'D width', 0.0001, 0.005, 'GeV')
    
    pars = [arg_cutoff, arg_slope, bkg, sigma, yld]

    mbc_d0 = ROOT.RooRealVar('mbc_d0', 'D0 Mbc', 1.8647, 'GeV')
    mbc_dp = ROOT.RooRealVar('mbc_dp', 'D+ Mbc', 1.8694, 'GeV')
    
    gauss_d0 = ROOT.RooGaussian('gauss_d0', 'D0 gaussian', mbc, mbc_d0, sigma)
    gauss_dp = ROOT.RooGaussian('gauss_dp', 'D+ gaussian', mbc, mbc_dp, sigma)

    argus = ROOT.RooArgusBG('argus', 'Argus BG', mbc, arg_cutoff, arg_slope)
    sumpdf_d0 = ROOT.RooAddPdf('sumpdf_d0', 'D0 sum pdf',
                          ROOT.RooArgList(gauss_d0, argus),
                          ROOT.RooArgList(yld, bkg))
    sumpdf_dp = ROOT.RooAddPdf('sumpdf_dp', 'Dp sum pdf',
                               ROOT.RooArgList(gauss_dp, argus),
                               ROOT.RooArgList(yld, bkg))

    Extended = ROOT.RooFit.Extended(ROOT.kTRUE)
    Save = ROOT.RooFit.Save(ROOT.kTRUE)
    Hesse = ROOT.RooFit.Hesse(ROOT.kFALSE)
    Verbose = ROOT.RooFit.Verbose(ROOT.kFALSE)

    if 'D0' in mode:
        pdf = sumpdf_d0
    else:
        pdf = sumpdf_dp


    if 'nogaus' in label:
        yld.setVal(1)
        yld.setConstant(ROOT.kTRUE)
        pars.remove(yld)

    if 'floatsigma' not in label:
        datatype = 'data'
        tag = 'single'

        if '281ipb' in label:
            prefix = 'dir_281ipbv7'
            frame_max = bkg_generic_ddbar_281_max[mode]
        elif '537ipb' in label:
            prefix = 'dir_537ipbv7'
            frame_max = bkg_generic_ddbar_537_max[mode]
        elif '818ipb' in label:
            prefix = 'dir_818ipbv7'
            frame_max = bkg_generic_ddbar_818_max[mode]
            if 'noxfeed' in label:
                frame_max = bkg_generic_ddbar_818_max_noxfeed[mode]

        else:
            raise NameError(label)
        
        tabfile = set_file('txt', datatype, mode, tag,
                           prefix=prefix,
                           extbase=attr.fitpath())

        sys.stdout.write('Using width from %s \n' %tabfile)
        tab = DHadTable(tabfile)
        sigmap1 = float(tab.cell_get('sigmap1', 'Value'))
        sigma.setVal(sigmap1)
        sigma.setConstant(ROOT.kTRUE)
        pars.remove(sigma)
        
    res = pdf.fitTo(dataset, Extended, Save, Verbose)
    res.Print('v')
    c1 = ROOT.TCanvas('c1', 'canvas1', 600, 600)
    c1.SetFixedAspectRatio(0)

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
    chisqbox.AddText('#chi^{2}/ndof = %.3f/%d =  %.3f' %
                     (chisq, ndof, chisq_ndof))
    xframe.addObject(chisqbox)

    pdf.paramOn(xframe, dataset)        

    xframe.SetTitle('Generic faking %s' % mode)
    xframe.Draw()

    c1.Print(epsfile)
    tools.save_fit_result(pars, txtfile)

    if not test:
        tools.eps2png(epsfile)
        tools.eps2pdf(epsfile)


def submit_batch_job(datatype, mode, label, test):
    script = create_python_script(datatype, mode, label, test)
    
    dt =  datatype.replace('/', '-')
    mode_sign = tools.get_modekey_sign(mode)
    ms = tools.pair_to_str(mode_sign)

    bash_file_name = 'fit-backgrounds-%s-%s.sh' % (dt, ms)
    bash_file = create_bash_file(script, bash_file_name, 'setpyroot l')


    logname = '%s_%s.txt' %(datatype.replace('/', '_'), mode)
    logfile = tools.set_file(extbase=attr.logpath,
                             prefix='dir_'+label+'/backgrounds',
                             comname=logname)

    qjobname = 'bkg%s' % ms

    tools.qsub_jobs(logfile, qjobname, bash_file, test)
    

def create_python_script(dt_type, mode, label, test):
    content =  '''#!/usr/bin/env python

from fit import backgrounds

backgrounds.fit_backgrounds_single_mode("%s", "%s", "%s", %s)

'''% (dt_type, mode, label, test)

    mode_sign = tools.get_modekey_sign(mode)

    ms = tools.pair_to_str(mode_sign)

    filename = 'backgrounds-%s-%s-%s.py' % (dt_type, ms, label)

    filename = filename.replace('/', '-')
    
    file_ = os.path.join(attr.srcfitpath, filename)
    
    f = UserFile()
    f.append(content) 
    f.output(file_)
    os.chmod(file_, 0755)
    return filename


def fit_backgrounds_single(datatype, modes, label, test):
    epsname = '%s_background' %(datatype.replace('/', '_'))
    epspath = os.path.join(attr.figpath, label)    
    epsfile = set_file(extbase=epspath, comname=epsname, ext='eps')

    if test:
        epsfile = epsfile + '.test'

    input_label = label

    ROOT.gROOT.SetBatch(1)
    ROOT.gROOT.SetStyle('Plain')
    
    mbc = ROOT.RooRealVar('mbc', 'Beam constrained mass', 1.83, 1.89, 'GeV')
    mbc_aset = ROOT.RooArgSet(mbc)

    ebeam = ROOT.RooRealVar('ebeam','Ebeam',1.8815,1.892,'GeV')

    dflav = ROOT.RooCategory('dflav','D0 flavor')
    dflav.defineType('dflav',1)
    dflav.defineType('dbarflav',-1)

    dataset_args = ROOT.RooArgList(mbc, ebeam, dflav)

    arg_cutoff = ROOT.RooRealVar('arg_cutoff', 'Argus cutoff', 1.88, 1.89, 'GeV')
    arg_slope = ROOT.RooRealVar('arg_slope', 'Argus slope', -10, -100, -1)
    yld = ROOT.RooRealVar('yield', 'D yield', 100, 0, 200000)
    bkg = ROOT.RooRealVar('bkg', 'Background', 100, 0, 1000000)

    sigma = ROOT.RooRealVar('sigma', 'D width', 0.0001, 0.005, 'GeV')
    

    mbc_d0 = ROOT.RooRealVar('mbc_d0', 'D0 Mbc', 1.8647, 'GeV')
    mbc_dp = ROOT.RooRealVar('mbc_dp', 'D+ Mbc', 1.8694, 'GeV')
    
    gauss_d0 = ROOT.RooGaussian('gauss_d0', 'D0 gaussian', mbc, mbc_d0, sigma)
    gauss_dp = ROOT.RooGaussian('gauss_dp', 'D+ gaussian', mbc, mbc_dp, sigma)

    argus = ROOT.RooArgusBG('argus', 'Argus BG', mbc, arg_cutoff, arg_slope)
    sumpdf_d0 = ROOT.RooAddPdf('sumpdf_d0', 'D0 sum pdf',
                          ROOT.RooArgList(gauss_d0, argus),
                          ROOT.RooArgList(yld, bkg))
    sumpdf_dp = ROOT.RooAddPdf('sumpdf_dp', 'Dp sum pdf',
                               ROOT.RooArgList(gauss_dp, argus),
                               ROOT.RooArgList(yld, bkg))

    Extended = ROOT.RooFit.Extended(ROOT.kTRUE)
    Save = ROOT.RooFit.Save(ROOT.kTRUE)
    Hesse = ROOT.RooFit.Hesse(ROOT.kFALSE)
    Verbose = ROOT.RooFit.Verbose(ROOT.kFALSE)

    if '281ipb' in label:
        prefix = 'dir_281ipbv7'
    elif '537ipb' in label:
        prefix = 'dir_537ipbv7'
    elif '818ipb' in label:
        prefix = 'dir_818ipbv7'
    else:
        raise NameError(label)

    c1 = ROOT.TCanvas('c1', 'canvas1', 800, 1000)
    #c1.SetFixedAspectRatio(0)
    c1.Divide(3,3)
    pad = 1
    for mode in modes:
        mode_root_name = get_mode_root_name(mode)
        if datatype == 'generic/ddbar':
            frametitle = 'Generic faking %s' % mode_root_name
        elif datatype == 'generic/cont':
            frametitle = 'Continuum production faking %s' % mode_root_name
        elif datatype == 'generic/tau':
            frametitle = '#tau #tau production faking %s' % mode_root_name
        elif datatype == 'generic/radret':
            frametitle = 'Radiative return faking %s' % mode_root_name
        else:
            raise NameError(datatype)
    
        c1.cd(pad)
        pad += 1
        comname = '%s_%s' %(datatype.replace('/', '_'), mode)
        bkgpath = os.path.join(attr.bkgpath(), input_label)
        bkgfile = set_file(extbase=bkgpath, comname=comname, ext='evt')
        if not os.access(bkgfile, os.F_OK):
            input_prefix = 'dir_%s' % input_label
            bkgfile = set_file(extbase=attr.bkgpath(),
                               dt_type=datatype.replace('/', '_'),
                               tag='s', mode=mode, prefix=input_prefix,
                               comname=comname, ext='evt', forceCombine=1)

        dataset = ROOT.RooDataSet.read(bkgfile, dataset_args)

        if 'D0' in mode:
            pdf = sumpdf_d0
        else:
            pdf = sumpdf_dp

        if 'floatsigma' not in label:
            tab_datatype = 'data'
            tag = 'single'
        
        tabfile = set_file('txt', tab_datatype, mode, tag,
                           prefix=prefix,
                           extbase=attr.fitpath())

        sys.stdout.write('Using width from %s \n' %tabfile)
        tab = DHadTable(tabfile)
        sigmap1 = float(tab.cell_get('sigmap1', 'Value'))
        sigma.setVal(sigmap1)
        sigma.setConstant(ROOT.kTRUE)
        
        res = pdf.fitTo(dataset, Extended, Save, Verbose)
        res.Print('v')

        xframe = mbc.frame()
        xframe.SetMarkerSize(0.3)
        if '818ipb' in label and 'noxfeed' in label:
            frame_max = bkg_generic_ddbar_818_max_noxfeed[mode]
            xframe.SetMaximum(frame_max)

        dataset.plotOn(xframe)
        pdf.plotOn(xframe)

        pdf.paramOn(xframe, dataset)        

        xframe.SetTitle(frametitle)
        xframe.Draw()

    c1.Print(epsfile)

    if not test:
        tools.eps2png(epsfile)
        tools.eps2pdf(epsfile)

        
def submit_batch_job_allinone(datatype, modes, label, test):
    script = create_python_script_allinone(datatype, modes, label, test)
    dt =  datatype.replace('/', '-')
    bash_file_name = 'fit-backgrounds-%s-allinone.sh' % dt 
    bash_file = create_bash_file(script, bash_file_name, 'setpyroot l')

    logname = '%s_allinone.txt' % datatype.replace('/', '_')
    logfile = tools.set_file(extbase=attr.logpath,
                             prefix='dir_'+label+'/backgrounds',
                             comname=logname)
    qn = datatype.split('/')[-1]
    qjobname = 'bkg%s' % qn
    tools.qsub_jobs(logfile, qjobname, bash_file, test)
    

def create_python_script_allinone(dt_type, modes, label, test):
    content =  '''#!/usr/bin/env python

from fit import backgrounds

backgrounds.fit_backgrounds_single("%s", %s, "%s", %s)

'''% (dt_type, modes, label, test)
    filename = 'backgrounds-%s-allinone-%s.py' % (dt_type, label)
    filename = filename.replace('/', '-')
    file_ = os.path.join(attr.srcfitpath, filename)
    f = UserFile()
    f.append(content) 
    f.output(file_)
    os.chmod(file_, 0755)
    return filename

