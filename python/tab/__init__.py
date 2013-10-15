"""
Module for DHad Table

"""


__author__ = "Xin Shi <xs32@cornell.edu>"
__revision__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2010 Xin Shi"
__license__ = "GNU GPL"


def main(opts, args):
    if args[0] == 'lumi':
	import lumi
	lumi.main(opts, args[1:])
    elif args[0] == 'compare':
	import compare
	compare.main(opts, args[1:])
    elif args[0] == 'combine':
	import combine
	combine.main(opts, args[1:])
    elif args[0] == 'divide':
	import divide
	divide.main(opts, args[1:])
    elif args[0] == 'para':
	import para
	para.main(opts, args[1:])
    elif args[0] == 'entries':
	import entries
	entries.main(opts, args[1:])
    elif args[0] == 'brf':
	import brf
	brf.main(opts, args[1:])
    elif args[0] == 'diff':
	import diff
	diff.main(opts, args[1:])
    elif args[0] == 'cuts':
	import cuts
	cuts.main(opts, args[1:])
    elif args[0] == 'parse':
	import parse
	parse.main(opts, args[1:])
    elif args[0] == 'backgrounds':
	import backgrounds
	backgrounds.main(opts, args[1:])
    elif args[0] == 'cbx':
	import cbx
	cbx.main(opts, args[1:])
    elif args[0] == 'sld':
	import sld
	sld.main(opts, args[1:])
    elif args[0] == 'web':
	import web
	web.main(opts, args[1:])
    elif args[0] == 'mctruth':
	import mctruth
	mctruth.main(opts, args[1:])
    elif args[0] == 'ths':
	import ths
	ths.main(opts, args[1:])
    elif args[0] == 'prd':
	import prd
	prd.main(opts, args[1:])
    else:
	raise NameError(args)
    
