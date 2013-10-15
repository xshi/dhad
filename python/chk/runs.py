"""
Check Runs

"""

import sys
import ROOT
from array import array
from tools.filetools import HTMLFile
from attr import weblinks

__author__ = "Xin Shi <xs32@cornell.edu>"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2010 Xin Shi"
__license__ = "GPL"
__revision__ = "$Revision$"


def main(opts, args):
    sys.stdout.write('dhad.check.runs...\n')
    sys.stdout.flush()

    if args[0] == 'html':
        return chk_runs_html(opts, args[1:])

    rootfiles = args
    obj = "dnt"
    for rootfile in rootfiles:
        ch = ROOT.TChain(obj)
        ch.Add(rootfile)
        
        run = array('i', [0])
        ch.SetBranchAddress("run", run)
        
        ch.GetEntry(0)
        run_min = run[0]
    
        ch.GetEntry(ch.GetEntries()-1)
        run_max = run[0]

        delta = run_max - run_min 
        sys.stdout.write('| %s | %s | %s | %s | \n' %(
            rootfile, run_min, run_max, delta))
        ch.Delete()

def chk_runs_html(opts, args):
    linkname = args[0]
    weblink = weblinks[linkname]
    f = HTMLFile(weblink)
    runs = []

    for url in f.urls:
        run = url.split('/')[-1].replace('.html', '')
        try:
            run = int(run)
            runs.append(run)
        except ValueError:
            continue

    sys.stdout.write('start run: %s, end run: %s, #runs: %s\n'
                     %(min(runs), max(runs), len(runs)))
