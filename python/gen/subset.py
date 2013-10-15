"""
Subset MC Generation 

"""

import sys
from tools import parse_args, get_rootfile, add_rootfile, makeDDecaySubTree,\
     mcDmodeFixRad, mcstringtodmode, get_modekey_sign
from ROOT import TFile
from attr.pdg import *


__author__ = "Xin Shi <xs32@cornell.edu>"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2011 Xin Shi"
__license__ = "GPL"
__revision__ = "$Revision$"


def main(opts, args):
    sys.stdout.write('dhad.gen.subset ... ')
    sys.stdout.flush()
    
    parsed = parse_args(args)
    datatype  = parsed[0]
    tag       = parsed[1]
    modes     = parsed[2]
    label     = parsed[3]
    mode = modes[0]
    modekey, sign = get_modekey_sign(mode)

    input_label = label.split('/')[0]
    children = label.split('/')[1]
        
    infile = get_rootfile(datatype, mode, input_label)
    outfile = get_rootfile(datatype, mode, label, opt='Create')

    if opts.test:
        outfile += '.test'
        sys.stdout.write('Input rootfile: %s \n' % infile)
        sys.stdout.write('Output rootfile: %s \n' % outfile)
    
    pt = add_rootfile(infile)
    nselected, ntotal = copy_events(pt, outfile, sign, children, opts.test)
    sys.stdout.write(' selected %s out of %s.\n' % (nselected, ntotal))
    sys.stdout.flush()

    
def copy_events(pt, newfile, sign, children, test=False):
    pt.SetBranchStatus('*', 1)
    f = TFile(newfile, 'RECREATE')
    newtree = pt.CloneTree(0)
    pt.SetBranchStatus('*', 1)
    ntotal = 0 
    nselected = 0 
    for pte in pt:
        ntotal += 1
        if test and ntotal > 1000:
            break 
        if selection(pte, sign, children):
            newtree.Fill()
            nselected += 1
            
    f.Write()
    f.Close()
    return nselected, ntotal

    
def selection(pte, sign, children):
    result = False
    
    if children == 'phipi':
        if sign == 1:
            daughters = set([pdgid_phi, pdgid_pip])
        else:
            daughters = set([pdgid_phi, pdgid_pim])

    elif children == 'k0star':
        if sign == 1:
            daughters = set([pdgid_K0bstar, pdgid_Kp])
        else:
            daughters = set([pdgid_K0star, pdgid_Km])

    elif children == 'kstar1410':
        if sign == 1:
            daughters = set([pdgid_K0bstar0, pdgid_Kp])

        else:
            daughters = set([pdgid_K0star0, pdgid_Km])
            
    elif children == 'phsp':
        if sign == 1:
            daughters =  set([pdgid_Kp, pdgid_Km, pdgid_pip])
        else:
            daughters =  set([pdgid_Kp, pdgid_Km, pdgid_pim])
            
    else:
        raise NameError(children)
    
    d = makeDDecaySubTree(pte, sign)[0]
    decay_daus = set([dau.pdgid for dau in d.daughters])

    #if decay_daus == daughters:
        # for i in range(pte.nmcpart):
        #     pid = pte.mcpdgid[i]
        #     pname = particle_data.findId(pid)
        #     print '%s: %s' % (i, pname) 

        # phi = makeDDecaySubTree(pte, sign)[1]
        # phi_daus = set([dau.pdgid for dau in phi.daughters])
        # kk = set([pdgid_Kp, pdgid_Km])
        # kkg = set([pdgid_Kp, pdgid_Km, pdgid_gammaFSR])
        # if phi_daus != kk and phi_daus != kkg: 
        #     print phi, phi_daus
        #     sys.exit()

    #if children == 'phsp':
    #     print daughters
    #     sys.exit()
    #result = (decay_daus in  daughters)
    #else:
    #     print daughters
    #     sys.exit()
    #result = (decay_daus == daughters)
    result = (decay_daus == daughters)
    return result
