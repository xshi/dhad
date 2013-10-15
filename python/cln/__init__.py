"""
Module for D-Hadronic: Cleans

"""

import os
import sys
import attr
import gen


__author__ = "Xin Shi <xs32@cornell.edu>"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2005-2011 Xin Shi"
__license__ = "GPL"
__revision__ = "$Revision$"


def main(opts, args):
    
    if args[0] == 'cleog':
        sys.stdout.write('Cleaning CLEOG files ... ')
        sys.stdout.flush()
        clean_cleog(args[1:])
    else:
	raise NameError(args)


def clean_cleog(args):
    modes, label, tasks = gen.parse_for_modes_tasks(args)
    filepath = os.path.join(
        attr.base, 'dat/signal', label, 'cleog_'+attr.cleog)

    files = []
    for mode in modes:
        for task_id in tasks:
            filename = 'cleog_%s_%s.pds' % (mode, task_id)
            file_ = os.path.join(filepath, filename)
            if os.access(file_, os.F_OK):
                files.append(os.path.join(filepath, filename))
            
    for file_ in files:
        os.remove(file_)

    sys.stdout.write(' %s cleaned.\n' %len(files))
