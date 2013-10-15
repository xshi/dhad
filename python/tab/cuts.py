"""
Script to make selection cuts table

"""
import os
import sys
import attr
import yld
import cuts
from tools.filetools import UserFile
from sets import Set
from tools import add_rootfile, get_modekey_sign
from tools.cuts import chooseD

__author__ = "Xin Shi <xs32@cornell.edu>"
__revision__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2010 Xin Shi"
__license__ = "GNU GPL"


def main(opts, args):
    global _opts, _debug, _set, _tabname
    _opts = opts
    _debug = opts.debug
    _set = opts.set
    _tabname = 'cuts_' + '_'.join(args).replace('/', '_')
    function = getattr(cuts, args[0])
    return function(args[1:])

def events(args):

    parsed = yld.parse_args(args)
    datatype = parsed[0]
    tag = parsed[1]
    modes = parsed[2]
    label = parsed[3]

    if _set and 'events' in _set:
        unique_evt_label = _set.split('=')[1]

    for mode in modes:
        events = get_events_list(
            datatype, mode, unique_evt_label, debug=_debug)
        if _debug:
            sys.stdout.write('\ndebug: total events %s\n' %len(events))
        pt = chain_rootfile(datatype, mode, label)
        mode_key, sign = get_modekey_sign(mode)
        nselected = 0 
        ntotal = len(events)
        for pte in pt:
            if found_this_event(events, pte.run, pte.event):
                d = chooseD(mode_key, pte, sign, opt = label)
                if d != None:
                    if _debug:
                        sys.stdout.write('\ndebug: selected %s %s \n'
                                         % (pte.run, pte.event))
                    nselected += 1

        sys.stdout.write(' selected %s out of %s.\n' % (nselected, ntotal))
        sys.exit()

        evtname = datatype + '_' + mode + '.evt'
        unique_A, unique_B = get_unique_list(evtname, label_A, label_B)


        
        for evt in unique_B:
            evt = evt.strip().split(' ')
            run = int(evt[0])
            event = int(evt[1])
            print run, event
            for pte in pt_A:
                if pte.run == run and pte.event == event:
                    print pte.ecm
            sys.exit()
            
        sys.exit()
        events_A, unique_file_A = get_events_set(datpath, evtname, label_A)
        events_B, unique_file_B = get_events_set(datpath, evtname, label_B)
        events_inter = events_A & events_B
        unique_A = events_A - events_inter
        unique_B = events_B - events_inter
        sys.stdout.write('Writing the unique events for mode %s ...' %mode)
        output_set_to_file(unique_A, unique_file_A)
        output_set_to_file(unique_B, unique_file_B)
        sys.stdout.write(' done.\n')


def chain_rootfile(datatype, mode, label):
    datpath = attr.datpath
    if datatype == 'signal':
        rootname = mode + '.root'
    elif datatype == 'data':
        rootname = '*.root'
    else:
        raise NameError(datatype)
    
    rootfile = os.path.join(datpath, datatype, label, rootname)
    if _debug:
        sys.stdout.write('\ndebug: rootfile %s \n' %rootfile)
    pt = add_rootfile(rootfile, debug=_debug)
    return pt

def get_events_list(datatype, mode, label, debug=False):
    unique_evt_label = label   
    unique_evtname = '%s_%s_unqiue_%s.evt' %(
        datatype, mode, unique_evt_label)
    unique_evtpath = os.path.join(
        attr.datpath, 'evt', unique_evt_label, 'events')
    unique_evtfile = os.path.join(unique_evtpath, unique_evtname)
    if debug:
        sys.stdout.write('\ndebug: unique_file %s\n' % unique_evtfile)

    f = UserFile(unique_evtfile)
    return f.data
    
def found_this_event(events, run, evt):
    this_event = '%s %s\n' %(run, evt)
    if this_event in events:
        if _debug:
            sys.stdout.write('\ndebug: found %s %s\n' %(run, evt))
        return True
    else:
        return False


    
