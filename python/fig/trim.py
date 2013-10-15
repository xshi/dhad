"""
Module for trimming figures 

"""

import os
import sys
import attr
from yld import parse_args
from tools import set_file, eps2pdf, set_root_style, parse_opts_set
import ROOT 
from ROOT import TCanvas, TFile
from fit import load_roofit_lib


__author__ = "Xin Shi <xs32@cornell.edu>"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2005-2010 Xin Shi"
__license__ = "GPL"
__revision__ = "$Revision$"


def main(opts, args):
    parsed = parse_args(args)
    datatype = parsed[0]
    tag = parsed[1]
    modes = parsed[2]
    label = parsed[3]

    for mode in modes:
        sys.stdout.write('Processing mode %s ...' %mode)
        prefix = 'dir_%s' % label

        if mode == 'double_all_d0s':
            comname = '%s_%s' %(datatype, 'Double_all_D0s')
        elif mode == 'double_all_dps':
            comname = '%s_%s' %(datatype, 'Double_all_Dps')
        else:
            comname = '%s_%s' %(datatype, mode)
        finname = set_file('root', comname=comname,
                           prefix=prefix, extbase=attr.figpath)

        foutname = finname.replace('.root', '_trim.eps')
        
        comname1 = '%s_%s' %(datatype, mode.split('__')[0])
        #comname2 = '%s_%s_%s' %(datatype, tag, mode.split('__')[1])
        
        foutname1 = foutname.replace(comname, comname1)
        #foutname2 = foutname.replace(comname, comname2)
        #load_roofit_lib(datatype, label)
        fin = TFile.Open(finname, 'READ')

        if tag == 'single':
            canvas_name = 'canvas'
        else:
            canvas_name = 'c'

        canvas = fin.Get(canvas_name)
    
        pad1 = canvas.GetPrimitive(canvas_name+'_1')
        if mode == 'double_all_d0s' or mode == 'double_all_dps':
            pad1 = trim_pad2(pad1, opts)
        else:
            pad1 = trim_pad(pad1, opts)
        pad1.Draw()
        pad1.SaveAs(foutname1)
        eps2pdf(foutname1)


def trim_pad(pad, opts):

    TitleOffset = parse_opts_set(opts.set, 'SetTitleOffset')
    if TitleOffset == None:
        TitleOffset = 1.35 

    objs = pad.GetListOfPrimitives()
    for obj in objs:
        if isinstance(obj, ROOT.TFrame):
            obj.SetFillColor(0)

        if isinstance(obj, ROOT.RooPlot):
            yax = obj.GetYaxis()
            yax.SetTitleOffset(TitleOffset)
            obj.SetXTitle('#font[72]{M}_{BC} (GeV/#font[72]{c}^{2})')
            obj.SetYTitle('Events / (1 MeV/#font[72]{c}^{2})')
            obj.SetMarkerSize(0.5)

        if isinstance(obj, ROOT.TPaveText):
            obj.SetBorderSize(0)
            obj.SetFillColor(0)

        if isinstance(obj, ROOT.RooCurve):
            if obj.GetLineColor() in [ROOT.kGreen, ROOT.kMagenta]:
                objs.remove(obj)
            else:
                obj.SetLineWidth(2)

    pad.SetFillColor(0)

    pad.SetRightMargin(0.05)

    LeftMargin = parse_opts_set(opts.set, 'SetLeftMargin')
    if LeftMargin == None:
        LeftMargin = 0.15

    pad.SetLeftMargin(LeftMargin)        

    Logy = parse_opts_set(opts.set, 'SetLogy')
    if Logy != None:
        pad.SetLogy(Logy)
    
    return pad


def trim_pad2(pad, opts):
    objs = pad.GetListOfPrimitives()
    for obj in objs:
        if isinstance(obj, ROOT.TFrame):
            obj.SetFillColor(0)

        if isinstance(obj, ROOT.RooPlot):
            yax = obj.GetYaxis()
            yax.SetTitleOffset(2.0)
            obj.SetXTitle('M_{BC} (GeV/c^{2})')
            obj.SetYTitle('Events / (1 MeV/c^{2})')
            obj.SetMarkerSize(0.5)

        if isinstance(obj, ROOT.TPaveText):
            obj.SetBorderSize(0)
            obj.SetFillColor(0)

        if isinstance(obj, ROOT.RooCurve):
            if obj.GetLineColor() in [ROOT.kGreen, ROOT.kMagenta]:
                objs.remove(obj)
            elif obj.GetLineColor() in [ROOT.kBlue]:
                obj.SetLineStyle(ROOT.kDashed)
                obj.SetLineWidth(1)
            else:
                obj.SetLineWidth(1)


    pad.SetFillColor(0)
    pad.SetRightMargin(0.05)
    pad.SetLeftMargin(0.2)        
    pad.SetLogy(0)

    return pad











