"""
Script to create luminosity table

"""

import os
import sys
import attr
import math
from tools.filetools import RunFile, CLEOGLOGFile
from tools import get_files_with_commonname


__author__ = "Xin Shi <xs32@cornell.edu>"
__revision__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2010 Xin Shi"
__license__ = "GNU GPL"


def main(opts, args):
    global _opts
    _opts = opts

    if args[0] == 'list':
	lumi_list(args[1:])
    elif args[0] == 'runs':
	lumi_runs(args[1:])
    elif args[0] == 'data':
	lumi_data(args[1:])
    else:
	raise NameError(args)
    
	
def lumi_list(args):
    listpath = '/home/pass1/cleo-c/Luminosities/runlists/'
    if args[0] == 'data43':
	datanames = ['data43']
    elif args[0] == 'data43-46':
	datanames = ['data43', 'data44', 'data45', 'data46']
    else:
	raise NameError(args)
    sys.stdout.write('| Data    | Lumi (/pb) |\n')
    sys.stdout.write('|---------+------------|\n')
    total_lumi = 0 
    for dataname in datanames:
	runlist = os.path.join(listpath, dataname + '.runlist')
	run = RunFile(runlist)
	lumi = run.get_total_lumi('/pb')
	total_lumi = total_lumi + lumi 
	sys.stdout.write('| %s  | %s |\n' % (dataname, lumi))

    sys.stdout.write('|---------+------------|\n')
    sys.stdout.write('| Total   | %s |\n' % total_lumi)
    
def lumi_runs(args):
    if _opts.set:
	for li in _opts.set.split(','):
            name = li.split('=')[0]
            value = li.split('=')[1]
            sys.stdout.write('dhad: set %s = %s \n' % (name, value))
            if name == 'perlumi':
                perlumi = eval(value)

    listpath = '/home/pass1/cleo-c/Luminosities/runlists/'
    if args[0] == 'data43-46':
	datanames = ['data43', 'data44', 'data45', 'data46']
    else:
	raise NameError(args)
    runs = {}
    for dataname in datanames:
	runlist = os.path.join(listpath, dataname + '.runlist')
	run = RunFile(runlist)
	runs.update(run.runs)

    runkeys = runs.keys()
    runkeys.sort()
    acc_lumi = 0
    nth = 0
    sys.stdout.write('| No.  | Run | PerLumi*No. | Acc lumi |\n')
    sys.stdout.write('|------+-----|-------------+----------|\n')
    for run in runkeys:
	acc_lumi = acc_lumi + runs[run]['lumi']
	if acc_lumi >= perlumi*nth:
	    sys.stdout.write('| %s | %s | %s | %s |\n' %(
		nth, run, perlumi*nth, acc_lumi))
	    nth += 1
	
def lumi_data(args):
    label = args[0]
    logpath = os.path.join(attr.base, 'dat', 'data', '10.1.7')
    numbers = attr.get_dataset_numbers(label)

    total = 0
    error = 0

    for num in numbers:
        logname = 'dtuple-data%s.txt' %num
        logfile = os.path.join(logpath, logname)
        dataset = 'data'+num.split('_')[0]
        factor = attr.lumi_scale_factors[dataset]
        parsed = CLEOGLOGFile(logfile)
        lumi_val = 0
        lumi_err = 0
        for ebeam, lumi in parsed.lumi['Ebeam'].items():
            ebeam = float(ebeam)
            if ebeam > 1880 and ebeam < 1892:
                lumi_val += eval(lumi[0])
                lumi_err = math.sqrt(lumi_err**2 + eval(lumi[1])**2
                                     + eval(lumi[2])**2)
        value = lumi_val * factor
        total += value
        error = math.sqrt(error**2 + lumi_err**2)

    lumi_val =  total*0.001
    lumi_err =  error*0.001

    sys.stdout.write('Luminosity for %s : (%.2f +- %.2f) /pb \n'
                     % (label, lumi_val, lumi_err))

