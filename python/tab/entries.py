"""
Script to list evt entries 

"""

import os
import sys
import attr
import entries
import tools
from tools import DHadTable, makeDDecaySubTree, mcDmodeFixRad
from attr import modes
from attr import PossibleDoubleTags as possible_double_tags
from attr.pdg import *


__author__ = "Xin Shi <xs32@cornell.edu>"
__revision__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2010 Xin Shi"
__license__ = "GNU GPL"


def main(opts, args):
    function = getattr(entries, args[0])
    return function(opts, args[1:])

def evt(opts, args):
    tabname = 'entries_evt_' + '_'.join(args).replace('/', '_')

    if args[0] == 'log':
        return evt_log(args[1:])
    
    if args[0] not in ['data'] :
	raise NameError(args)

    dt_type = args[0]
    tag = args[1]
    label = args[2]

    evtpath = attr.evtpath()
    if '/' in label:
        ver = label.split('/')[0]
        label = label.split('/')[1]
        evtpath = attr.evtpath(ver)
        
    prefix = 'dir_' + label

    tab = DHadTable()
    tab.row_append(['Mode', 'fname', 'fnamebar', 'combined', 'sum(theory)'])

    for mode in attr.modes:
        evtfile1 = tools.set_file('evt', dt_type, mode, tag, sign=-1,
                                  prefix=prefix, extbase=evtpath)
        evtfile2 = tools.set_file('evt', dt_type, mode, tag, sign=1,
                                  prefix=prefix, extbase=evtpath)
        evtfile_combined = tools.set_file('evt', dt_type, mode, tag,
                                          prefix=prefix, extbase=evtpath)
        entries1 = tools.count_lines(evtfile1)
        entries2 = tools.count_lines(evtfile2)

        sumup = entries1 + entries2
        
        entries_combined = tools.count_lines(evtfile_combined)
        row = [mode, entries1, entries2, entries_combined, sumup]
        
        tab.row_append(map(str, row))

    tab.output(tabname)

    
def evt_log(args):
    print args
    if args[0] not in ['data'] :
	raise NameError(args)

    dt_type = args[0]
    tag = args[1]
    label = args[2]

    evtpath = attr.evtpath()
    if '/' in label:
        ver = label.split('/')[0]
        label = label.split('/')[1]
        evtpath = attr.evtpath(ver)
        
    prefix = 'dir_' + label
    evttab = 'entries_evt' + '_'.join(args).replace('/', '_') + '.tab'

    tab = DHadTable()
    tab.column_append_from_tab_file('Mode', evttab)
    tab.output()
    sys.exit()


def ddbars(opts, args):
    tabname = 'entries_ddbars_' + '_'.join(args).replace('/', '_')
    test = False # opts.test
    
    datatype = args[0]
    label = args[1]

    rootfile = tools.get_rootfile(datatype, label=label, test=test)

    print rootfile
    sys.exit()
    pt = tools.add_rootfile(rootfile)    

    print pt
    nd0d0b = 0
    ndpdm = 0
    ntotal = 0
    dmodecount = {}; dbmodecount = {}
    dtmodecount = {}

    for i in modes:
        dmodecount[i] = 0; dbmodecount[i] = 0

    for pair in possible_double_tags:
        dtmodecount[pair] = 0

    for pte in pt:
        if pte.entry % 100000 == 0: print pte.entry
        realdtag = None
        realdbtag = None
        ntotal += 1
        if pte.mcpdgid[3] == pdgid_Dz:
            nd0d0b += 1
        elif pte.mcpdgid[3] == pdgid_Dp:
            ndpdm += 1
        else:
            print 'HEEELP!'
        dtree = makeDDecaySubTree(pte,1)
        dbtree = makeDDecaySubTree(pte,-1)
        d = dtree[0]
        db = dbtree[0]
        mcdmode = d.mcDmode()
        mcdbmode = db.mcDmode()
        if ((mcDmodeFixRad(mcdmode) == modes[3]['mcdmode']) and
            mcdmode != mcDmodeFixRad(mcdmode)):
            for node in d.interestingDescendants():
                if node.pdgid == pdgid_gamma:
                    gnode = node
                    break
            if (gnode.parent.pdgid != pdgid_Dz and
                abs(gnode.parent.pdgid) != 20213 and
                gnode.parent.pdgid != pdgid_rhoz and
                abs(gnode.parent.pdgid) != 313 and
                abs(gnode.parent.pdgid) != 10323):
                print 'xxxxxxxxxxxxxxxxxx'
                print pte.run, pte.event
                for node in dtree:
                    print node
                pass

##         print 'HELP', mcdmode, pte.mcdmode
##         print mcdmodetostring(mcdmode), mcdmodetostring(pte.mcdmode)
##         print d
##         for node in d.interestingDescendants():
##             print node
        for j in modes:
            if mcDmodeFixRad(mcdmode) == modes[j]['mcdmode']:
                if j in (202, 203, 204):
                    nodes_of_interest = d.interestingDescendants()
                    for node in nodes_of_interest:
                        if node.pdgid == pdgid_KS:
                            dmodecount[j] += 1
                            realdtag = j
                            break
                else:
                    dmodecount[j] += 1
                    realdtag = j
                if j == 204:
                    daughter_dump(pte, 1)
                if (False and j in (202, 203, 204) and
                    mcdmodetostring(mcdmode) != 'K0 pi+ ' and
                    len(d.daughters) != 3):
                    tree = makeDecayTree(pte)
                    for node in tree:
                        if node.pdgid == pdgid_Dz:
                            nodes_of_interest = node.interestingDescendants()
                            break
                    print '--------------'
                    print mcdmode, mcdbmode, pte.mcdmode, pte.mcdbmode
                    print mcdmodetostring(mcdmode)
                    for node in tree:
                        print node
            if mcDmodeFixRad(mcdbmode) == modes[j]['mcdbmode']:
                if j in (202, 203, 204):
                    nodes_of_interest = db.interestingDescendants()
                    for node in nodes_of_interest:
                        if node.pdgid == pdgid_KS:
                            dbmodecount[j] += 1
                            realdbtag = j
                            break
                else:
                    dbmodecount[j] += 1
                    realdbtag = j
        if realdtag != None and realdbtag != None:
            dtmodecount[(realdtag,realdbtag)] += 1
        
    print 'N(all):', ntotal
    print 'N(D0D0B):', nd0d0b
    print 'N(D+D-):', ndpdm
    if nd0d0b > 0:
        print 'Ratio:', float(ndpdm)/nd0d0b
    for j in dmodecount:
        print modes[j]['fname'], dmodecount[j],
        if j < 200 and nd0d0b > 0:
            print float(dmodecount[j])/nd0d0b
        elif ndpdm > 0:
            print float(dmodecount[j])/ndpdm
        else:
            print
        print modes[j]['fnamebar'], dbmodecount[j],
        if j < 200 and nd0d0b > 0:
            print float(dbmodecount[j])/nd0d0b
        elif ndpdm > 0:
            print float(dbmodecount[j])/ndpdm
        else:
            print

    for pair in possible_double_tags:
        print "%s/%s %d" % (modes[pair[0]]['fname'], modes[pair[1]]['fnamebar'],
                            dtmodecount[pair])

    sys.exit()

def daughter_dump(pte, dsign):
    d = makeDDecaySubTree(pte, dsign)[0]
#    print pte.run, pte.event, 
    rv = makedict(map(lambda x: particle_data.findId(x.pdgid).name, d.daughters))
    mcdmode = d.mcDmode()
    ng2 = mcDmodeGetRad(mcdmode)
    if ng2 == 0:
        return
    ng = rv.get('gamma', 0)
    if ng > 0 and ng == mcDmodeGetRad(mcdmode):
        return
    if rv not in ignore[204]:
        print rv, mcdmodetostring(mcdmode), mcDmodeGetRad(mcdmode)


def makedict(desc):
    rv = {}
    for i in desc:
        rv[i] = rv.get(i,0) + 1
    return rv

def mcDmodeGetRad(mcdmode):
    rp1 = 10000000
    rp2 = 1000000
    return ((mcdmode % rp1) - (mcdmode % rp2)) / rp2
