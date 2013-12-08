"""
Module for D-Hadronic: Link files 

"""

import os
import sys
import attr


__author__ = "Xin Shi <xs32@cornell.edu>"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2005-2013 Xin Shi"
__license__ = "GPL"
__revision__ = "$Revision$"


def main(opts, args):
    if args[0] == 'fit':
        return fit(args[1:]) 
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

def ln_files(srcdir, dstdir, pattern=None):
    fs = []
    for root, dirs, files in os.walk(srcdir):
        fs.extend(files)
        break
    
    if pattern is None:
        src_fs = fs
    else:
        src_fs = [f for f in fs if pattern in f]
        
    n_lnk = 0 
    cwd = os.getcwd()
    os.chdir(dstdir)
    for f in src_fs:
        src = os.path.join(srcdir, f)
        try:
            os.symlink(src, f)
            n_lnk += 1

        except OSError:
            pass 

    os.chdir(cwd)
    sys.stdout.write('Linked %s files. \n' %n_lnk)

