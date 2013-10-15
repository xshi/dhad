"""
Script to diff table

"""
import os
import sys

import attr

import yld
import diff

from tools.filetools import UserFile
from sets import Set

__author__ = "Xin Shi <xs32@cornell.edu>"
__revision__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2010 Xin Shi"
__license__ = "GNU GPL"


def main(opts, args):
    global _opts, _tabname
    _opts = opts
    _tabname = 'diff_' + '_'.join(args).replace('/', '_')
    function = getattr(diff, args[0])
    return function(args[1:])

def events(args):
    parsed = yld.parse_args(args)
    datatype  = parsed[0]
    tag       = parsed[1]
    modes     = parsed[2]
    label_A   = parsed[3]
    label_B  = args[3]

    datpath = attr.datpath
    for mode in modes:
        modename = mode.replace('Single_', '')
        evtname = datatype + '_' + mode + '.evt'
        events_A, unique_file_A = get_events_set(datpath, evtname, label_A)
        events_B, unique_file_B = get_events_set(datpath, evtname, label_B)
        events_inter = events_A & events_B
        unique_A = events_A - events_inter
        unique_B = events_B - events_inter
        sys.stdout.write('Writing the unique events for mode %s ...' %mode)
        output_set_to_file(unique_A, unique_file_A)
        output_set_to_file(unique_B, unique_file_B)
        sys.stdout.write(' done.\n')

def get_events_set(datpath, evtname, label):
    evtpath = os.path.join(datpath, 'evt', label, 'events')
    evtfile = os.path.join(evtpath, evtname)
    f = UserFile(evtfile)
    events = Set(f.data)
    unique_file = evtfile.replace('.evt', '_unqiue_%s.evt' %label)
    return events, unique_file

def output_set_to_file(set_, file_):
    f = UserFile()
    f.data = sorted(list(set_))
    f.output(file_)
    

    
