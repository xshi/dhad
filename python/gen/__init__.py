"""
Module for Generate MC for DHadronic Analysis

"""

import attr


__author__ = "Xin Shi <xs32@cornell.edu>"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2005-2011 Xin Shi"
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
    elif args[0] == 'signal':
	import signal
	signal.main(opts, args[1:])
    elif args[0] == 'subset':
	import subset
	subset.main(opts, args[1:])
    else:
	raise NameError(args)

def parse_for_modes_tasks(args):

    if args[0] == 'single':
        modes = attr.single_mode_list
    elif args[0] == 'double':
        modes = attr.double_mode_list
    elif args[0] == 'diagdouble':
        modes = attr.diag_double_mode_list
    elif args[0] == 'nondiagdouble':
        modes = attr.nondiag_double_mode_list
    elif args[0].startswith('Single'):
        modes = [args[0]]
    elif args[0].startswith('Double'):
        modes = [args[0]]
    else:
        raise NameError(args)

    label = args[1]
    if '281ipb' in label:
        tasks = range(1, 11)
    elif '537ipb' in label:
        tasks = range(11, 31)
    elif '818ipb' in label:
        tasks = range(1, 31)
    else:
        raise NameError(label)

    if len(args) > 2:
        if args[2] == 'task':
            task_id = args[3]
            if '-' in task_id:
                task_begin = int(task_id.split('-')[0])
                task_end  = int(task_id.split('-')[1])+1
                tasks = range (task_begin, task_end)
            else:
                tasks = map(int, task_id.split(','))

        else:
            raise NameError(args)

    return modes, label, tasks

    
        
