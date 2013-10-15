"""
Tools for fitting

"""

import os
import sys
from tools import save_fit_result, set_root_style


__author__ = "Xin Shi <xs32@cornell.edu>"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2011 Xin Shi"
__license__ = "GNU GPL"


def mbc_single_3s(evtfile, mc, setMres, setGamma, setR, sp1, sp2, sp3, fa,
                  fb, setmd, setp, setxi, setN1, setN2, setNbkgd1, setNbkgd2,
                  title1, title2, epsfile, txtfile, ymin=0.5,
                  cuts=None, err_type='SYMM', test=False):

    from ROOT import (gROOT, RooRealVar, RooCategory, RooArgSet, RooDataSet,
                      RooFit, RooGaussian, RooArgList, RooAddPdf, RooSimultaneous,
                      RooArgusBG, RooFormulaVar, RooDLineShape, RooAbsData,
                      RooDataHist, TCanvas, kRed, kBlue, kGreen, kMagenta,
                      TPaveText)
    set_root_style(stat=1, grid=0)
    
    # // sp1 = sigma of signal
    # // sp2 = ratio of sigmas betwwen sigma2 sigma 1
    # // sp3 = ratio of sigmas betwwen sigma3 sigma 2
    # // fa, fb, - fractions
    # // xi_side - slope of argus
    # // p_side - power of argus

    # mc = 1  Monte Carlo Model: EvtGenModels/Class/EvtVPHOtoVISR.cc
    # mc = 3  Data Model: with BES 2007 paper (BES2006 lineshape hepex/0612056) 

    mbc = RooRealVar('mbc', 'Beam constrained mass', 1.83, 1.89, 'GeV')
    ebeam = RooRealVar('ebeam', 'Ebeam', 1.8815, 1.892, 'GeV')

    dflav = RooCategory('dflav','D flavor')
    dflav.defineType('dflav', 1)
    dflav.defineType('dbarflav', -1)

    if cuts != None:
        if 'kkmass' in cuts:
            kkmass = RooRealVar('kkmass', 'KK invariant mass', 0.97, 1.90, 'GeV')
            ras = RooArgSet(mbc, ebeam, kkmass, dflav)
            dataset = RooDataSet.read(evtfile, ras)
        elif 'kpimass' in cuts:
            kpimass = RooRealVar('kpimass', 'Kpi invariant mass', 0.6, 1.4, 'GeV')
            ras = RooArgSet(mbc, ebeam, kpimass, dflav)
            dataset = RooDataSet.read(evtfile, ras)
        else:
            raise NameError(cuts)

        sys.stdout.write('Using cuts: %s...' %cuts)
        dataset = dataset.reduce(cuts)
        sys.stdout.write(' selected %s events.\n' % dataset.numEntries())
    else:
        ras = RooArgSet(mbc, ebeam, dflav)
        dataset = RooDataSet.read(evtfile, ras)

    res = RooRealVar("datares", "datares", mc)
    mres = RooRealVar("mres","mres", setMres)
    gamma = RooRealVar('gamma', 'gamma', setGamma)

    r = RooRealVar('r', 'r', setR)
    sigmaE = RooRealVar("sigmaE","sigmaE", 0.0021)

    sigmap1 = RooRealVar("sigmap1","sigmap1", sp1, 0.002, 0.040)

    scalep2 = RooRealVar("scalep2","scalep2",2.00,1.500,5.500)
    scalep3 = RooRealVar("scalep3","scalep3",5.00,3.00,10.000)
   
    scalep2.setVal(sp2)
    scalep2.setConstant(1)
    scalep3.setVal(sp3)
    scalep3.setConstant(1)

    as12 = RooArgList(sigmap1,scalep2)
    sigmap2 = RooFormulaVar("sigmap2","sigma2","sigmap1*scalep2", as12)

    as123 = RooArgList(sigmap1,scalep2,scalep3)
    sigmap3 = RooFormulaVar("sigmap3","sigma3","sigmap1*scalep2*scalep3",
                            as123)
    
    md = RooRealVar("md","md", setmd,1.863,1.875)

    f2 = RooRealVar("f2","f2", fa)
    f3 = RooRealVar("f3","f3", fb)
    al23 = RooArgList(f2,f3)
    f1 = RooFormulaVar("f1","f1","1.0-f2-f3", al23)

    # Construct signal shape

    fcn1_1 = RooDLineShape("DLineshape1_1","DLineShape1_1",4,mbc,ebeam,
                           mres,gamma,r,sigmaE,sigmap1,md,res)
    fcn1_2 = RooDLineShape("DLineshape1_2","DLineShape1_2",4,mbc,ebeam,
                           mres,gamma,r,sigmaE,sigmap2,md,res)
    fcn1_3 = RooDLineShape("DLineshape1_3","DLineShape1_3",4,mbc,ebeam,
                           mres,gamma,r,sigmaE,sigmap3,md,res)

    fcn2_1 = RooDLineShape("DLineshape2_1","DLineShape2_1",4,mbc,ebeam,
                           mres,gamma,r,sigmaE,sigmap1,md,res)
    fcn2_2 = RooDLineShape("DLineshape2_2","DLineShape2_2",4,mbc,ebeam,
                           mres,gamma,r,sigmaE,sigmap2,md,res)
    fcn2_3 = RooDLineShape("DLineshape2_3","DLineShape2_3",4,mbc,ebeam,
                           mres,gamma,r,sigmaE,sigmap3,md,res)


    alf1_123 = RooArgList(fcn1_1,fcn1_2,fcn1_3)
    af12 = RooArgList(f1,f2) 
    signal1_3 = RooAddPdf("signal1_3","signal1_3", alf1_123, af12)

    alf2_123 = RooArgList(fcn2_1,fcn2_2,fcn2_3)
    
    signal2_3 = RooAddPdf("signal2_3","signal2_3", alf2_123, af12)

    p = RooRealVar("p","p", setp, 0.1, 1.5)
    xi= RooRealVar("xi","xi",setxi,-100.0,-0.1)

    Bkgd1 = RooArgusBG("argus1","argus1",mbc,ebeam,xi,p)
    Bkgd2 = RooArgusBG("argus2","argus2",mbc,ebeam,xi,p)

    shapes1 = RooArgList(signal1_3)
    shapes1.add(signal1_3)
    shapes1.add(Bkgd1)    

    shapes2 = RooArgList(signal2_3)
    shapes2.add(signal2_3)
    shapes2.add(Bkgd2)

    N1 = RooRealVar("N1","N1",setN1,0.0,200000000.0)
    N2 = RooRealVar("N2","N2",setN2,0.0,200000000.0)

    Nbkgd1 = RooRealVar("Nbkgd1","Nbkgd1",setNbkgd1, 0.0, 200000000.0)
    Nbkgd2 = RooRealVar("Nbkgd2","Nbkgd2",setNbkgd2, 0.0, 200000000.0)

    yields1 = RooArgList(N1)
    yields1.add(N1)
    yields1.add(Nbkgd1)

    yields2 = RooArgList(N2)
    yields2.add(N2)
    yields2.add(Nbkgd2)

    
    totalPdf1 = RooAddPdf("totalPdf1","totalPdf1", shapes1,yields1)
    totalPdf2 = RooAddPdf("totalPdf2","totalPdf2", shapes2,yields2)

    totalPdf = RooSimultaneous("totalPdf","totalPdf",dflav)
    totalPdf.addPdf(totalPdf1,"dflav")
    totalPdf.addPdf(totalPdf2,"dbarflav")

    # Check fitTo options at:
    # http://root.cern.ch/root/html512/RooAbsPdf.html#RooAbsPdf:fitTo
    #
    # Available fit options:
    #  "m" = MIGRAD only, i.e. no MINOS
    #  "s" = estimate step size with HESSE before starting MIGRAD
    #  "h" = run HESSE after MIGRAD
    #  "e" = Perform extended MLL fit
    #  "0" = Run MIGRAD with strategy MINUIT 0
    #  (no correlation matrix calculation at end)
    #   Does not apply to HESSE or MINOS, if run afterwards.

    #  "q" = Switch off verbose mode
    #  "l" = Save log file with parameter values at each MINUIT step
    #  "v" = Show changed parameters at each MINUIT step
    #  "t" = Time fit
    #  "r" = Save fit output in RooFitResult object 
    # Available optimizer options
    #  "c" = Cache and precalculate components of PDF that exclusively
    #  depend on constant parameters
    #  "2" = Do NLL calculation in multi-processor mode on 2 processors
    #  "3" = Do NLL calculation in multi-processor mode on 3 processors
    #  "4" = Do NLL calculation in multi-processor mode on 4 processors

    MINUIT = 'ermh4'

    if err_type == 'ASYM':
        MINUIT = 'erh4'
        
    if test:
        sys.stdout.write('Will save epsfile as: %s \n' %epsfile)
        sys.stdout.write('Will save txtfile as: %s \n' %txtfile)
        return
    
    if dataset.numEntries() == 0:
        N1.setVal(0)
        N2.setVal(0)
    else:
        # Start Fitting
        fitres = totalPdf.fitTo(dataset, MINUIT)
        fitres.Print('v')

    # Save plots
    canvas = TCanvas('canvas','mbc', 1200, 400);
    canvas.Divide(3,1)

    canvas_1 = canvas.GetListOfPrimitives().FindObject('canvas_1')
    canvas_2 = canvas.GetListOfPrimitives().FindObject('canvas_2')
    canvas_1.SetLogy(1) 
    canvas_2.SetLogy(1)

    LineColorRed = RooFit.LineColor(kRed)
    LineColorBlue = RooFit.LineColor(kBlue)
    LineWidth = RooFit.LineWidth(1) #0.6)

    # Plot the D 
    canvas.cd(1)
    mbcFrame=mbc.frame()
    mbcFrame=mbc.frame(60)

    dflav.setLabel('dflav')
    ebas = RooArgSet(ebeam, dflav)
    ebeamdata = RooDataHist("ebeamdata", "ebeamdata", ebas, dataset)
    
    dataset.plotOn(mbcFrame, RooFit.Cut("dflav==dflav::dflav"))
    mbcFrame.getAttMarker().SetMarkerSize(0.6)
    mbcFrame.Draw()

    Slice = RooFit.Slice(dflav)
    ProjWData = RooFit.ProjWData(ebas, ebeamdata)
    
    totalPdf.plotOn(mbcFrame, LineColorRed, LineWidth, Slice, ProjWData)
    chisq1 = mbcFrame.chiSquare()*mbcFrame.GetNbinsX()
    mbcFrame.Draw()

    as_bkg1 = RooArgSet(Bkgd1)
    cp_bkg1 = RooFit.Components(as_bkg1)

    totalPdf.plotOn(mbcFrame, cp_bkg1, Slice, LineColorBlue, LineWidth, ProjWData)

    mbcFrame.SetTitle(title1)
    mbcFrame.SetMinimum(ymin)

    mbcFrame.Draw()

    # Plot the D bar
    canvas.cd(2)
    mbcFrame=mbc.frame()
    mbcFrame=mbc.frame(60)

    dflav.setLabel('dbarflav')
    ebas = RooArgSet(ebeam, dflav)
    ebeamdata = RooDataHist("ebeamdata", "ebeamdata", ebas, dataset)
    
    dataset.plotOn(mbcFrame, RooFit.Cut("dflav==dflav::dbarflav"))
    mbcFrame.getAttMarker().SetMarkerSize(0.6)
    mbcFrame.Draw()

    Slice = RooFit.Slice(dflav)
    ProjWData = RooFit.ProjWData(ebas, ebeamdata)
    
    totalPdf.plotOn(mbcFrame, LineColorRed, LineWidth, Slice, ProjWData)
    chisq2 = mbcFrame.chiSquare()*mbcFrame.GetNbinsX()
    mbcFrame.Draw()

    as_bkg2 = RooArgSet(Bkgd2)
    cp_bkg2 = RooFit.Components(as_bkg2)

    totalPdf.plotOn(mbcFrame, cp_bkg2, Slice, LineColorBlue, LineWidth, ProjWData)

    mbcFrame.SetTitle(title2)
    mbcFrame.SetMinimum(ymin)

    mbcFrame.Draw()

    # Plot Statistics Box
    canvas.cd(3)
    mbcFrame = mbc.frame()

    paramWin1 = totalPdf.paramOn(mbcFrame,dataset, "",2,"NELU",0.1,0.9,0.9)

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
    ATextBox = TPaveText(.1, .1, .8, .2,"BRNDC") 

    tempString = "#chi^{2}_{1} = %.1f, #chi^{2}_{2} = %.1f" % (chisq1,chisq2)  
    ATextBox.AddText(tempString) 
    ATextBox.SetFillColor(0)
    ATextBox.SetBorderSize(1)

    mbcFrame.addObject(ATextBox) 
    mbcFrame.Draw() 
    canvas.Print(epsfile)
    rootfile = epsfile.replace('.eps', '.root')
    canvas.Print(rootfile)

    # Save fitting parameters
    pars = [N1, N2, Nbkgd1, Nbkgd2, md, p, sigmap1, xi]
    save_fit_result(pars, txtfile, err_type=err_type, verbose=1)


def mbc_gau_che(evtfile, mc, setMres, setGamma, setR, sp1, sp2, sp3, fa,
                fb, setmd, setp, setxi, setN1, setN2, setNbkgd1, setNbkgd2,
                title1, title2, epsfile, txtfile, ymin=0.5,
                cuts=None, err_type='SYMM', test=False):
    
    from ROOT import (gROOT, RooRealVar, RooCategory, RooArgSet, RooDataSet,
                      RooFit, RooGaussian, RooArgList, RooAddPdf, RooSimultaneous,
                      RooArgusBG, RooFormulaVar, RooChebychev, RooAbsData,
                      RooDataHist, TCanvas, kRed, kBlue, kGreen, kMagenta,
                      TPaveText)
    set_root_style(stat=1, grid=0)

    mbc = RooRealVar('mbc', 'Beam constrained mass', 1.83, 1.89, 'GeV')
    ebeam = RooRealVar('ebeam','Ebeam', 1.8815, 1.892, 'GeV')

    dflav = RooCategory('dflav','D0 flavor')
    dflav.defineType('dflav',1)
    dflav.defineType('dbarflav',-1)

    if cuts != None:
        if 'kkmass' in cuts:
            kkmass = RooRealVar('kkmass', 'KK invariant mass', 0.97, 1.90, 'GeV')
            ras = RooArgSet(mbc, ebeam, kkmass, dflav)
            dataset = RooDataSet.read(evtfile, ras)
        elif 'kpimass' in cuts:
            kpimass = RooRealVar('kpimass', 'Kpi invariant mass', 0.6, 1.4, 'GeV')
            ras = RooArgSet(mbc, ebeam, kpimass, dflav)
            dataset = RooDataSet.read(evtfile, ras)
        else:
            raise NameError(cuts)

        sys.stdout.write('Using cuts: %s...' %cuts)
        dataset = dataset.reduce(cuts)
        sys.stdout.write(' selected %s events.\n' % dataset.numEntries())
    else:
        ras = RooArgSet(mbc, ebeam, dflav)
        dataset = RooDataSet.read(evtfile, ras)

    #sigma = RooRealVar('sigma', 'D width', 0.0001, 0.005, 'GeV')
    sigma = RooRealVar('sigma', 'D width', 0.00468, 'GeV')
    mbc_dp = RooRealVar('mbc_dp', 'D+ Mass', 1.86962, 'GeV')
    sigpdf = RooGaussian('gauss_dp', 'D+ gaussian', mbc, mbc_dp, sigma)
    
    #arg_cutoff = RooRealVar('arg_cutoff', 'Argus cutoff', 1.88, 1.89, 'GeV')
    #arg_slope = RooRealVar('arg_slope', 'Argus slope', -10, -100, -1)
    #bkgpdf = RooArgusBG('argus', 'Argus BG', mbc, arg_cutoff, arg_slope)

    con0 = RooRealVar('c0', 'constant', -1, 1)
    con1 = RooRealVar('c1', 'linear', -10, 10)
    con2 = RooRealVar('c2', 'quadratic', 1)

    bkgpdf = RooChebychev('bkgpdf', 'Background',
                          mbc, RooArgList(con1, con2))

    yld = RooRealVar('yld', 'D yield', 100, 0, 2000)
    bkg = RooRealVar('bkg', 'Background', 100, 0, 1000)

    sumpdf = RooAddPdf('sumpdf', 'Sum pdf', RooArgList(sigpdf, bkgpdf),
                       RooArgList(yld, bkg))

    yldbar = RooRealVar('yldbar', 'Dbar yield', 100, 0, 2000)
    bkgbar = RooRealVar('bkgbar', 'Background', 100, 0, 1000)

    sumpdfbar = RooAddPdf('sumpdfbar', 'Sum pdf', RooArgList(sigpdf, bkgpdf),
                          RooArgList(yldbar, bkgbar))

    totalpdf = RooSimultaneous('rs', 'Simultaneous PDF', dflav)
    totalpdf.addPdf(sumpdf, 'dflav')
    totalpdf.addPdf(sumpdfbar, 'dbarflav')

    MINUIT = 'ermh4'

    if err_type == 'ASYM':
        MINUIT = 'erh4'
        
    if test:
        sys.stdout.write('Will save epsfile as: %s \n' %epsfile)
        sys.stdout.write('Will save txtfile as: %s \n' %txtfile)
        return
    
    if dataset.numEntries() == 0:
        yld.setVal(0)
        yldbar.setVal(0)
    else:
        # Start Fitting
        fitres = totalpdf.fitTo(dataset, MINUIT)
        fitres.Print('v')

    # Save plots
    canvas = TCanvas('canvas','mbc', 400, 400);
    xframe=mbc.frame(50)
    ProjWData = RooFit.ProjWData(dataset)
    RooAbsData.plotOn(dataset, xframe)
    totalpdf.plotOn(xframe, ProjWData)
    totalpdf.paramOn(xframe)
    xframe.Draw()
    canvas.Print(epsfile)

    # Save fitting parameters
    pars = [bkg, bkgbar, con1, yld, yldbar]
    save_fit_result(pars, txtfile, err_type=err_type, verbose=1)


def mbc_dline_che(evtfile, mc, setMres, setGamma, setR, sp1, sp2, sp3, fa,
                  fb, setmd, setp, setxi, setN1, setN2, setNbkgd1, setNbkgd2,
                  title1, title2, epsfile, txtfile, ymin=0.5,
                  cuts=None, err_type='SYMM', test=False):
    
    from ROOT import (gROOT, RooRealVar, RooCategory, RooArgSet, RooDataSet,
                      RooFit, RooGaussian, RooArgList, RooAddPdf, RooSimultaneous,
                      RooArgusBG, RooFormulaVar, RooChebychev, RooAbsData,
                      RooDataHist, TCanvas, kRed, kBlue, kGreen, kMagenta,
                      TPaveText, RooDLineShape)
    set_root_style(stat=1, grid=0)

    mbc = RooRealVar('mbc', 'Beam constrained mass', 1.83, 1.89, 'GeV')
    ebeam = RooRealVar('ebeam','Ebeam', 1.8815, 1.892, 'GeV')

    dflav = RooCategory('dflav','D0 flavor')
    dflav.defineType('dflav',1)
    dflav.defineType('dbarflav',-1)

    if cuts != None:
        if 'kkmass' in cuts:
            kkmass = RooRealVar('kkmass', 'KK invariant mass', 0.97, 1.90, 'GeV')
            ras = RooArgSet(mbc, ebeam, kkmass, dflav)
            dataset = RooDataSet.read(evtfile, ras)
        else:
            raise NameError(cuts)

        sys.stdout.write('Using cuts: %s...' %cuts)
        dataset = dataset.reduce(cuts)
        sys.stdout.write(' selected %s events.\n' % dataset.numEntries())
    else:
        ras = RooArgSet(mbc, ebeam, dflav)
        dataset = RooDataSet.read(evtfile, ras)

    res = RooRealVar("datares", "datares", mc)
    mres = RooRealVar("mres","mres", setMres)
    gamma = RooRealVar('gamma', 'gamma', setGamma)

    r = RooRealVar('r', 'r', setR)
    sigmaE = RooRealVar("sigmaE","sigmaE", 0.0021)

    sigmap1 = RooRealVar("sigmap1","sigmap1", sp1, 0.002, 0.040)

    scalep2 = RooRealVar("scalep2","scalep2",2.00,1.500,5.500)
    scalep3 = RooRealVar("scalep3","scalep3",5.00,3.00,10.000)
   
    scalep2.setVal(sp2)
    scalep2.setConstant(1)
    scalep3.setVal(sp3)
    scalep3.setConstant(1)

    as12 = RooArgList(sigmap1,scalep2)
    sigmap2 = RooFormulaVar("sigmap2","sigma2","sigmap1*scalep2", as12)

    as123 = RooArgList(sigmap1,scalep2,scalep3)
    sigmap3 = RooFormulaVar("sigmap3","sigma3","sigmap1*scalep2*scalep3",
                            as123)
    
    md = RooRealVar("md","md", setmd,1.863,1.875)

    f2 = RooRealVar("f2","f2", fa)
    f3 = RooRealVar("f3","f3", fb)
    al23 = RooArgList(f2,f3)
    f1 = RooFormulaVar("f1","f1","1.0-f2-f3", al23)

    # Construct signal shape

    fcn1_1 = RooDLineShape("DLineshape1_1","DLineShape1_1",4,mbc,ebeam,
                           mres,gamma,r,sigmaE,sigmap1,md,res)
    fcn1_2 = RooDLineShape("DLineshape1_2","DLineShape1_2",4,mbc,ebeam,
                           mres,gamma,r,sigmaE,sigmap2,md,res)
    fcn1_3 = RooDLineShape("DLineshape1_3","DLineShape1_3",4,mbc,ebeam,
                           mres,gamma,r,sigmaE,sigmap3,md,res)

    fcn2_1 = RooDLineShape("DLineshape2_1","DLineShape2_1",4,mbc,ebeam,
                           mres,gamma,r,sigmaE,sigmap1,md,res)
    fcn2_2 = RooDLineShape("DLineshape2_2","DLineShape2_2",4,mbc,ebeam,
                           mres,gamma,r,sigmaE,sigmap2,md,res)
    fcn2_3 = RooDLineShape("DLineshape2_3","DLineShape2_3",4,mbc,ebeam,
                           mres,gamma,r,sigmaE,sigmap3,md,res)


    alf1_123 = RooArgList(fcn1_1,fcn1_2,fcn1_3)
    af12 = RooArgList(f1,f2) 
    sigpdf = RooAddPdf("signal1_3","signal1_3", alf1_123, af12)

    alf2_123 = RooArgList(fcn2_1,fcn2_2,fcn2_3)
    
    sigbarpdf = RooAddPdf("signal2_3","signal2_3", alf2_123, af12)

    con0 = RooRealVar('c0', 'constant', -1, 1)
    con1 = RooRealVar('c1', 'linear', -10, 10)
    con2 = RooRealVar('c2', 'quadratic', 1)

    bkgpdf = RooChebychev('bkgpdf', 'Background', mbc, RooArgList(con1, con2))
    
    bkgbarpdf = RooChebychev('bkgbarpdf', 'Background',
                             mbc, RooArgList(con1, con2))

    yld = RooRealVar('yld', 'D yield', 100, 0, 2000)
    bkg = RooRealVar('bkg', 'Background', 100, 0, 1000)

    sumpdf = RooAddPdf('sumpdf', 'Sum pdf', RooArgList(sigpdf, bkgpdf),
                       RooArgList(yld, bkg))
    yldbar = RooRealVar('yldbar', 'Dbar yield', 100, 0, 2000)
    bkgbar = RooRealVar('bkgbar', 'Background', 100, 0, 1000)

    sumpdfbar = RooAddPdf('sumpdfbar', 'Sum pdf', RooArgList(sigbarpdf, bkgbarpdf),
                          RooArgList(yldbar, bkgbar))

    totalpdf = RooSimultaneous('rs', 'Simultaneous PDF', dflav)
    totalpdf.addPdf(sumpdf, 'dflav')
    totalpdf.addPdf(sumpdfbar, 'dbarflav')

    MINUIT = 'ermh4'

    if err_type == 'ASYM':
        MINUIT = 'erh4'
        
    if test:
        sys.stdout.write('Will save epsfile as: %s \n' %epsfile)
        sys.stdout.write('Will save txtfile as: %s \n' %txtfile)
        return
    
    if dataset.numEntries() == 0:
        yld.setVal(0)
        yldbar.setVal(0)
    else:
        # Start Fitting
        fitres = totalpdf.fitTo(dataset, MINUIT)
        fitres.Print('v')

    # Save plots
    canvas = TCanvas('canvas','mbc', 400, 400);
    xframe=mbc.frame(50)
    ProjWData = RooFit.ProjWData(dataset)
    RooAbsData.plotOn(dataset, xframe)
    totalpdf.plotOn(xframe, ProjWData)
    totalpdf.paramOn(xframe)
    xframe.Draw()
    canvas.Print(epsfile)

    # Save fitting parameters
    pars = [bkg, bkgbar, con1, md, sigmap1, yld, yldbar]
    save_fit_result(pars, txtfile, err_type=err_type, verbose=1)


