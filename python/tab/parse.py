"""
Script to parse contents

"""
import os
import sys
import attr
import yld
import parse
import tools
from attr import get_dataset_by_run
from tools import EventsFile, DHadTable 
from sets import Set
from tools.filetools import UserFile
from tools.decparser import interactive


__author__ = "Xin Shi <xs32@cornell.edu>"
__revision__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2010-2011 Xin Shi"
__license__ = "GNU GPL"



def main(opts, args):
    #global _debug, _set, _tabname, _test
    #_debug = opts.debug
    #_set = opts.set
    #_test = opts.test 
    #_tabname = 'parse_' + '_'.join(args).replace('/', '_')
    function = getattr(parse, args[0])
    return function(opts, args[1:])

def dec(opts, args):
    release = args[0]
    action = args[1]
    parent = args[2]
    children = args[4:]

    decfile = '/nfs/cleo3/Offline/rel/%s/data/DECAY.DEC' % release

    i = interactive()
    i.do_readfile(decfile)

    if action == 'explain':
        i.explain(parent, children)
    elif action == 'details':
        i.details(parent, children)
    else:
        raise NameError(action)


def events(args):
    parsed = yld.parse_args(args)
    datatype = parsed[0]
    tag = parsed[1]
    modes = parsed[2]
    label = parsed[3]

    unique_evt_label = label 
    if _set and 'events' in _set:
        unique_evt_label = _set.split('=')[1]

    tab = DHadTable()

    row = ['Mode']
    row.extend(attr.datasets_281)
    tab.row_append(row)

    for mode in modes:
        modename = mode.replace('Single_', '')
        evtfile = get_unique_evtfile(
            datatype, mode, unique_evt_label, debug=_debug)
        f = EventsFile(evtfile)
        row = map(str, f.datasets_sorted)
        row.insert(0, modename)
        tab.row_append(row)

    tab.output(_tabname)


def get_unique_evtfile(datatype, mode, label, debug=False):
    unique_evt_label = label   
    unique_evtname = '%s_%s_unqiue_%s.evt' %(
        datatype, mode, unique_evt_label)
    unique_evtpath = os.path.join(
        attr.datpath, 'evt', unique_evt_label, 'events')
    unique_evtfile = os.path.join(unique_evtpath, unique_evtname)
    if debug:
        sys.stdout.write('\ndebug: unique_file %s\n' % unique_evtfile)
    return unique_evtfile

def runs(args):
    parsed = yld.parse_args(args)
    datatype = parsed[0]
    tag = parsed[1]
    modes = parsed[2]
    label = parsed[3]

    unique_evt_label = label 

    datatype = 'data'
    run_event_set = Set([])
    for mode in attr.single_mode_list:
        evtname = '%s_%s_unqiue_%s.evt' %(datatype, mode, label)
        evtpath = os.path.join(attr.datpath, 'evt', label, 'events')
        unique_file = os.path.join(evtpath, evtname)
        f = UserFile(unique_file)
        events = Set(f.data)
        run_event_set.update(events)


    fe = EventsFile()
    fe.data = list(run_event_set)
    fe.parse()

    tab = DHadTable()
    row = ['Dataset', 'Run', 'Number of Events']
    tab.row_append(row)
    for run, num in sorted(fe.runs.iteritems()):
        dataset = get_dataset_by_run(run)
        row = [dataset, run, num]
        tab.row_append(map(str, row))

    if _test:
        tab.output()
        sys.stdout.write('\ntest: Will write to %s\n' %_tabname)
    else:
        tab.output(_tabname)


    
def output_headerfiles(label):
    headernames = ['Double_D0D0B_header', 'Double_DpDm_header',
                   'Single_D0_header', 'Single_D0B_header',
                   'Single_Dp_header', 'Single_Dm_header']
    outpath = os.path.join(attr.datpath, 'signal', label,
                           'src', 'tag_fragments')
    for hname in headernames:
        headerfile = tools.check_and_join(outpath, hname)
        f = UserFile()
        if 'D0D0B' in hname:
            alias_line = '#\nAlias myD0 D0\n#\n#\nAlias myanti-D0 anti-D0\n#\n'
            psi_decay_line = '1.000    myD0  myanti-D0         VSS;\n'

        if 'DpDm' in hname:
            alias_line = '#\nAlias myD+ D+\n#\n#\nAlias myD- D-\n#\n'
            psi_decay_line = '1.000    myD+  myD-         VSS;\n'

        elif 'Single_D0_' in hname:
            alias_line = '#\nAlias myD0 D0\n#\n'
            psi_decay_line = '1.000    myD0  anti-D0         VSS;\n'

        elif 'Single_D0B_' in hname:
            alias_line = '#\nAlias myanti-D0 anti-D0\n#\n'
            psi_decay_line = '1.000    D0  myanti-D0         VSS;\n'

        elif 'Single_Dp_' in hname:
            alias_line = '#\nAlias myD+ D+\n#\n'
            psi_decay_line = '1.000    myD+  D-         VSS;\n'

        elif 'Single_Dm_' in hname:
            alias_line = '#\nAlias myD- D-\n#\n'
            psi_decay_line = '1.000    D+  myD-         VSS;\n'

        f.append(alias_line)
        f.append('Decay vpho\n1.000   psi(3770)  gamma    VPHOTOVISR ;\nEnddecay\n#\nDecay psi(3770)\n')
        f.append(psi_decay_line)
        f.append('Enddecay\n#')
        f.output(headerfile, verbose=1)


def tag_fragments(opts, args):
    label = args[0]
    if label in ['281ipbv12', '537ipbv12', '818ipbv12']:
        release = '20080624_MCGEN'
    else:
        raise NameError(label)
    sys.stdout.write('Using release %s...\n' %release)

    output_headerfiles(label)

    decfile = '/nfs/cleo3/Offline/rel/%s/data/DECAY.DEC' % release
    i = interactive()
    i.do_readfile(decfile)

    modes = attr.modes
    for mode in modes:
        for fname, decname in [('fname','decname'),
                               ('fnamebar','decnamebar')]:
            decay = modes[mode][decname]
            parent = decay.split()[0]
            children = decay.split()[2:]
            outname = modes[mode][fname]
            outpath = os.path.join(attr.datpath, 'signal', label,
                                   'src', 'tag_fragments')
            outfile = tools.check_and_join(outpath, outname)
            i.details(parent, children, outfile)

