"""
Module for DHad Selection

"""

__author__ = "Xin Shi <xs32@cornell.edu>"
__revision__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2005-2011 Xin Shi"
__license__ = "GNU GPL"


def main(opts, args):
    if args[0] == 'diff':
	import diff
	diff.main(opts, args[1:])
    elif args[0] == 'trkmtm':
	import trkmtm
	trkmtm.main(opts, args[1:])
    elif args[0] == 'trkmtm2':
	import trkmtm2
	trkmtm2.main(opts, args[1:])
    elif args[0] == 'var':
	import var
	var.main(opts, args[1:])
    elif args[0] == 'multspec':
	import multspec
	multspec.main(opts, args[1:])
    elif args[0] == 'multcand':
	import multcand
	multcand.main(opts, args[1:])
    elif args[0] == 'kssideband':
	import kssideband
	kssideband.main(opts, args[1:])
    elif args[0] == 'extlbkgs':
	import extlbkgs
	extlbkgs.main(opts, args[1:])
    elif args[0] == 'kkmass':
	import kkmass
	kkmass.main(opts, args[1:])
    elif args[0] == 'kpimass':
	import kpimass
	kpimass.main(opts, args[1:])
    else:
	raise NameError(args)
    
