"""
Module for  D-Hadronic Checks

"""
import attr 


__author__ = "Xin Shi <xs32@cornell.edu>"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2005-2010 Xin Shi"
__license__ = "GPL"
__revision__ = "$Revision$"


def main(opts, args):
    
    if args[0] == 'cleog':
	import cleog
	cleog.main(opts, args[1:])
    elif args[0] == 'pass2':
	import pass2
	pass2.main(opts, args[1:])
    elif args[0] == 'dskim':
	import dskim
	dskim.main(opts, args[1:])
    elif args[0] == 'ntuple':
	import ntuple
	ntuple.main(opts, args[1:])
    elif args[0] == 'runs':
	import runs
	runs.main(opts, args[1:])
    else:
	raise NameError(args)


def parse_for_channel_names(args):
    
    channel_names =[]
    if args[0] == 'single':
        channel_names = attr.single_mode_list
    elif args[0] == 'double':
        channel_names = attr.double_mode_list
    elif args[0] == 'diagdouble':
        channel_names = attr.diag_double_mode_list
    elif args[0] == 'nondiagdouble':
        channel_names = attr.nondiag_double_mode_list
    else:
        channel_names.append(args[0])

    arg = None
    if len(args) > 1:
        arg = args[1:]

    return channel_names, arg
        
