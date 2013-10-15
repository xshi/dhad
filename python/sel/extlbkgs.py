"""
Module to select External Backgounds events

"""

import os
import sys
import tools
import attr
import sel
from tools.cuts import chooseD, passDE
from tools import mcstringtodmode, makeDDecaySubTree, mcDmodeFixRad

__author__ = "Xin Shi <xs32@cornell.edu>"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2005-2011 Xin Shi"
__license__ = "GPL"
__revision__ = "$Revision$"


def main(opts, args):
    label = args[0]
    test = opts.test 
    sys.stdout.write('dhad.sel.extlbkgs ...')
    sys.stdout.flush()

    datpath = attr.datpath
    datatype = 'generic'
    rootfile = tools.get_rootfile(datatype, label=label, test=test)
    pt = tools.add_rootfile(rootfile)

    bkg_mcdmodes = { 'kpi' : mcstringtodmode('K+ pi-'),
                     'kpipi0' : mcstringtodmode('K+ pi- pi0'),
                     'k3pi' : mcstringtodmode('K+ pi- pi+ pi-'),
                     'kkspi' : mcstringtodmode('K- K0 pi+'),
                     'kkspibar' : mcstringtodmode('K+ K0 pi-'),
                     '3pi' : mcstringtodmode('pi+ pi- pi+'),
                     '3pipi0' : mcstringtodmode('pi+ pi- pi+ pi0'),
                     '5pi' : mcstringtodmode('pi+ pi- pi+ pi- pi+'),
                     'kskspi' : mcstringtodmode('K0 K0 pi+')
                     }

    bkg_mcdmodes_rev = {}
    counts = {}
    files = {}
    selpath = os.path.join(attr.datpath, 'sel', label, 'extlbkgs')
    
    for i in bkg_mcdmodes:
        bkg_mcdmodes_rev[bkg_mcdmodes[i]] = i
        counts[i] = 0
        selname = 'singtag_bkg_%s.evt' % i 
        if test:
            selname += '.test'

        selfile = tools.check_and_join(selpath, selname)

        files[i] = open(selfile, 'w')

    # First number is the sign of the D we should look at for the fake signal;
    # second number is the mode.
    bkg_dmodes = { 'kpi' : (-1, 0), 'kpipi0' : (-1, 1), 'k3pi' : (-1, 3),
                   'kkspi' : (1, 3),
                   'kkspibar' : (-1, 3), '3pi' : (1, 202), '3pipi0' : (1, 203),
                   '5pi' : (1, 204), 'kskspi' : (1, 204) }

    ensure_other_side_is_not = { 'kpi' : (mcstringtodmode('K+ pi-'),),
                                 'kpipi0' : (mcstringtodmode('K+ pi- pi0'),),
                                 'k3pi' : (mcstringtodmode('K+ pi- pi+ pi-'),
                                           mcstringtodmode('K+ K0 pi-')),
                                 'kkspi' : (mcstringtodmode('K- K0 pi+'),
                                            mcstringtodmode('K- pi+ pi- pi+')),
                                 'kkspibar' : (mcstringtodmode('K+ K0 pi-'),
                                               mcstringtodmode('K+ pi- pi- pi+')),
                                 '3pi' : (),
                                 '3pipi0' : (),
                                 '5pi' : (),
                                 'kskspi' : ()
                                 }


    ntotal = 0
    nselected = 0
    for pte in pt:
        ntotal += 1
        if test and ntotal > 1000:
            break

        mcd = makeDDecaySubTree(pte, 1)
        mcdb = makeDDecaySubTree(pte, -1)
        mcdmode = mcDmodeFixRad(mcd[0].mcDmode())
        mcdbmode = mcDmodeFixRad(mcdb[0].mcDmode())
        if (mcdmode in bkg_mcdmodes_rev):
            mcdmode_string = bkg_mcdmodes_rev[mcdmode]
            if mcdbmode not in ensure_other_side_is_not[mcdmode_string]:
                counts[mcdmode_string] += 1
                choice = chooseD(bkg_dmodes[mcdmode_string][1], pte,
                                 bkg_dmodes[mcdmode_string][0])
                if choice != None and passDE(choice, pte):
                    nselected += 1
                    files[mcdmode_string].write('%g\n' % pte.dmbc[choice])
                    
    sys.stdout.write(' selected %s out of %s.\n' % (nselected, ntotal))
    sys.stdout.write('Number of mcdmode: %s. \n' % counts)
    sys.stdout.flush()
