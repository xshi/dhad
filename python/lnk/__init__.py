"""
Module for D-Hadronic: Link files 

"""

import os
import sys
import attr
from tools import ln_files


__author__ = "Xin Shi <xs32@cornell.edu>"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2005-2013 Xin Shi"
__license__ = "GPL"
__revision__ = "$Revision$"


def main(opts, args):
    if args[0] == 'fit':
        return fit(args[1:]) 
    elif args[0] == 'fit/crossfeeds':
        return fit_crossfeeds(args[1:]) 
    else:
	raise NameError(args)


def fit(args):
    label = args[0] 
    if label == 'v13':
        src_label = '818ipbv12'
    else:
        raise NameError(args)
        
    srcdir = os.path.join(attr.fitpath, src_label)
    dstdir = os.path.join(attr.fitpath, label)

    ln_files(srcdir, dstdir, '.txt')


def fit_crossfeeds(args):
    label = args[0] 
    subdir = 'crossfeeds'

    if label == 'v13':
        src_label = '818ipbv12'
    else:
        raise NameError(args)
        
    srcdir = os.path.join(attr.fitpath, src_label, subdir)
    dstdir = os.path.join(attr.fitpath, label    , subdir)

    ln_files(srcdir, dstdir, '.txt')


