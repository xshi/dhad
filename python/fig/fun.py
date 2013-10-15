"""
Module for plotting functions 

"""

import os
import sys
import fun
import tools
from ROOT import TF1, TCanvas
from tools import canvas_output, parse_opts_set

__author__ = "Xin Shi <xs32@cornell.edu>"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2005-2010 Xin Shi"
__license__ = "GPL"
__revision__ = "$Revision$"


def main(opts, args):
    tools.set_root_style()
    figname = 'fun_'+'_'.join(args).replace('/', '_')
    function = getattr(fun, args[0])
    return function(opts, args[1:], figname)


def argus(opts, args, figname):
    '''
    ARGUS funcion:

    a(m; m0, xi, p) = A*m*(1- m^2/m0^2)^p * exp(xi*(1-m^2/m0^2))

    '''
    canvas = TCanvas("aCanvas", "Canvas", 600, 600)

    m0 = parse_opts_set(opts.set, 'm0')
    xi = parse_opts_set(opts.set, 'xi')
    p = parse_opts_set(opts.set, 'p')

    fun = 'x*TMath::Power((1-x**2/[0]**2),[2])*exp([1]*(1-x**2/[0]**2))'

    f1 = TF1('argus', fun, 1.83, 1.86)
    f1.SetParName(0, 'Resonance mass')
    f1.SetParName(1, 'Slope parameter')
    f1.SetParName(2, 'Power')

    f1.SetParameter(0, m0)
    f1.SetParameter(1, xi)
    f1.SetParameter(2, p)
    f1.Draw()
    canvas_output(canvas, figname, opts.test)
