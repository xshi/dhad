"""
Module to select multplicity spectrum

"""

import os
import sys
import tools
import attr
import sel
from attr import modes
from yld import parse_args, create_bash_file
from ROOT import TTree, TFile, gROOT, TChain, TH1F, TH2F
from tools import makeDDecaySubTree, create_bash_file_pyline
from attr.pdg import *
from tools.cuts import chooseD, passDE, countDcand
import shelve
from tools.filetools import UserFile 
from fit import load_roofit_lib


__author__ = "Xin Shi <xs32@cornell.edu>"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2005-2011 Xin Shi"
__license__ = "GPL"
__revision__ = "$Revision$"


def main(opts, args):
    reweight = args[0]
    
    parsed = parse_args(args[1:])
    datatype  = parsed[0]
    tag       = parsed[1]
    modes     = parsed[2]
    label     = parsed[3]

    for mode in modes:
        if opts.set and opts.set == 'interact':
            if tag == 'single':
                single_tag_mode(reweight, datatype, mode, label, opts.test)
            else:
                raise ValueError(tag)
        else:
            submit_batch_job(reweight, datatype, tag, mode, label, opts)

        # script, logfile, qjobname = create_script_logfile_jobname(
        #     reweight, datatype, tag, mode, label, opts.test)
        # bash_file = create_bash_file(script, 'multspec.sh', 'sel')
        # tools.qsub_jobs(logfile, qjobname, bash_file, opts.test)



def create_script_logfile_jobname(reweight, datatype, tag, mode, label, test):
    logname = '%s_%s.log' %(datatype, mode)
    logpath = os.path.join(attr.sellogpath, label, 'multspec')
    logfile = tools.set_file(extbase=logpath, comname=logname)

    content =  '''#!/usr/bin/env python

from sel import multspec

multspec.single_tag_mode("%s", "%s", "%s", "%s", test=%s)

'''% (reweight, datatype, mode, label, test)

    mode, sign = tools.get_modekey_sign(mode)

    if tag == 'single':
        if sign == [-1, 1]:
            filename = 'sel-%s-%s-m%s-%s.py' % (datatype, tag, mode, label)
            qjobname = 'sel%s' % mode 
        else:
            if sign == 1:
                sign = 'p'
            else: 
                sign = 'm'
            filename = 'sel-%s-%s-m%s-%s-%s.py' % (datatype, tag, mode, sign, label)
            qjobname = 'sel%s,%s' % (mode, sign)
            
    else:
        filename = 'sel-%s-%s-m%s-%s-%s.py' % (datatype, tag, mode[0], mode[1], label)
        qjobname = 'sel%s,%s' % (mode[0], mode[1])

    file_ = os.path.join(attr.base, 'src', attr.src, 'sel', filename)

    f = UserFile()
    f.data.append(content) 
    f.output(file_)
    os.chmod(file_, 0755)

    return filename, logfile, qjobname


def single_tag_mode(reweight, datatype, mode, label, test=False):
    sys.stdout.write('dhad.sel.multspec: Processing Mode %s...' % mode)
    sys.stdout.flush()

    datpath = attr.datpath
    rootfile = tools.get_rootfile(datatype, mode, label)

    pt = tools.add_rootfile(rootfile)

    selname = '%s_%s.root' %(datatype, mode)
    if test:
        selname += '.test'
        
    selpath = os.path.join(attr.datpath, 'sel', label, 'multspec', reweight)
    selfile = tools.check_and_join(selpath, selname)

    nselected, ntotal = output_multspec(reweight, pt, mode, selfile,
                                        label, test)
    
    sys.stdout.write(' selected %s out of %s.\n' % (nselected, ntotal))
    sys.stdout.write('Saved as %s \n' %selfile)
    sys.stdout.flush()


def track_passes_quality(index, pte):
    rv = True
    rv &= (0.050 <= pte.trpip[index] <= 2.0)
    rv &= abs(pte.trd0[index]) <= 0.005
    rv &= abs(pte.trz0[index]) <= 0.050
    rv &= abs(pte.trchi2[index]) <= 100000
    rv &= pte.trhitf[index] != 1e3000000 and pte.trhitf[index] >= 0.5
    rv &= abs(pte.trcosth[index]) <= 0.93
    return rv


def getindex(rawind, dict):
    length = len(dict)
    if rawind < 0:
        rv = 0
    elif rawind >= length:
        rv = length - 1
        while rv % 2 != rawind % 2:
            rv -= 1
    else:
        rv = rawind
    return rv


def getpi0index(rawind, dict):
    length = len(dict)
    if rawind < 0:
        rv = 0
    elif rawind >= length:
        rv = length -1
    else:
        rv = rawind
    return rv


def output_multspec(reweight, pt, mode, selfile, label, test=False):
    mode, signs = tools.get_modekey_sign(mode)
    f = TFile(selfile, 'recreate')

    load_roofit_lib('signal', label)
    
    from ROOT import RooRealVar, RooDataSet, RooArgList, RooArgSet, \
         RooGaussian, RooArgusBG, RooCBShape, RooAddPdf, RooPolynomial, \
         gSystem, TCanvas

    efffile = selfile.replace('.root', '.db')
    effs = shelve.open(efffile)

    mbc = RooRealVar('mbc', 'Beam constrained mass', 1.83, 1.89, 'GeV')
    weight2 = RooRealVar('weight2', 'weight', 1)
    weight3 = RooRealVar('weight3', 'weight', 1)
    mbc_aset = RooArgSet(mbc)

    ntrack_d0 = TH1F('ntrack_d0', 'Number of other side tracks for D^{0} #rightarrow K#pi', 10, 0, 9)
    ntrack_dp = TH1F('ntrack_dp', 'Number of other side tracks for D^{+} #rightarrow K#pi#pi', 10, 0, 9)
    
    unweight_sum = 0
    reweight_ntr_sum = 0; reweight_npi0_sum = 0
    reweight_ntr_mcand_cnt = 0; reweight_npi0_mcand_cnt = 0
    unweight_dmbc = TH1F('unweight_dmbc', 'm_{BC}, direct MC', 100, 1.83, 1.89)
    reweight_ntr_dmbc = TH1F('reweight_ntr_dmbc', 'm_{BC}, track reweighted MC',
                             100, 1.83, 1.89)
    reweight_npi0_dmbc = TH1F('reweight_npi0_dmbc', 'm_{BC}, #pi^{0} reweighted MC',
                              100, 1.83, 1.89)
    
    chgpart = (pdgid_pip, pdgid_pim, pdgid_Kp, pdgid_Km, pdgid_mup, pdgid_mum,
               pdgid_ep, pdgid_em)
    neupart = (pdgid_KL, pdgid_piz, pdgid_gamma)
    intpart = chgpart + neupart

    ntr_denoms = {}; gen_dmbc_ntr = {}; npi0_denoms = {}; gen_dmbc_npi0 = {}
    for i in range(7+1):
        ntr_denoms[i] = 0
        gen_dmbc_ntr[i] = TH1F('gen_dmbc_ntr_'+`i`, 'm_{BC} for '+`i`+' tracks',
                               100, 1.83, 1.89)
    for i in range(5+1):
        npi0_denoms[i] = 0
        gen_dmbc_npi0[i] = TH1F('gen_dmbc_npi0_'+`i`, 'm_{BC} for '+`i`+' #pi^{0}',
                                100, 1.83, 1.89)

    ntotal = 0
    nselected = 0

    for pte in pt:
        ntotal += 1
        if test and nselected > 10:
            break

        if test and ntotal > 1000:
            break
        
        if pte.ecm < 3.7:
            continue
        othsidetrk = 0; othsidepi0 = 0
        dtree = makeDDecaySubTree(pte, -1)
    
        ddesc = dtree[0].interestingDescendants(intpart, False, False)

        for i in ddesc:
            if i.pdgid in chgpart:
                othsidetrk += 1
            if (i.pdgid in chgpart and i.parent.pdgid == pdgid_KS and
                len(i.parent.daughters) == 1):
                # This absurd special case is due to GEANT's "K_S -> pi" decay
                othsidetrk += 1
            if i.pdgid == pdgid_piz:
                othsidepi0 += 1
            if (i.pdgid == pdgid_KS) and len(i.daughters) != 2:
                print i

        if mode >= 200:
            mod2 = 1
        else:
            mod2 = 0

        if (othsidetrk % 2) != mod2:
            print '-----------------------------------', othsidetrk
            print chgpart
            # for node in makeDecayTree(pte):
            #  pass
            #  if len(node.daughters) == 0 and node.pdgid in chgpart:
            #  print node

        choice = chooseD(mode, pte, 1)

        if choice != None and not passDE(choice, pte):
            choice = None
            
        unweight_sum += 1
        
        index_tr = getindex(othsidetrk, ntr_denoms)
        ntr_denoms[index_tr] += 1
        index_pi0 = getpi0index(othsidepi0, npi0_denoms)
        npi0_denoms[index_pi0] += 1

        final_weight_vector_ntr = attr.multiplicity_weight_ntr[reweight]
        initial_weight_vector_ntr = attr.multiplicity_weight_ntr['init']

        final_weight_vector_npi0 = attr.multiplicity_weight_npi0[reweight]
        initial_weight_vector_npi0 = attr.multiplicity_weight_npi0['init']

        reweight_ntr_sum += (final_weight_vector_ntr[index_tr]/
                             initial_weight_vector_ntr[index_tr])
        reweight_npi0_sum += (final_weight_vector_npi0[index_pi0]/
                              initial_weight_vector_npi0[index_pi0])
        if choice != None:
            nselected += 1
            
            unweight_dmbc.Fill(pte.dmbc[choice])
            reweight_ntr_dmbc.Fill(pte.dmbc[choice],
                                    (final_weight_vector_ntr[index_tr]/
                                     initial_weight_vector_ntr[index_tr]))
            reweight_npi0_dmbc.Fill(pte.dmbc[choice],
                                    (final_weight_vector_npi0[index_pi0]/
                                     initial_weight_vector_npi0[index_pi0]))
            gen_dmbc_ntr[index_tr].Fill(pte.dmbc[choice])
            gen_dmbc_npi0[index_pi0].Fill(pte.dmbc[choice])
            mbc.setVal(pte.dmbc[choice])
            

    effs['npi0_denom'] = npi0_denoms
    effs['ntr_denom'] = ntr_denoms
    effs['unweight_sum'] = unweight_sum
    effs['reweight_ntr_sum'] = reweight_ntr_sum
    effs['reweight_npi0_sum'] = reweight_npi0_sum
    
    effs.close()
    #sys.stdout.write('Saved %s \n' %efffile)

    f.Write()
    f.Close()
    pt.Delete()

    return nselected, ntotal


def submit_batch_job(reweight, datatype, tag, mode, label, opts):
    mode_sign = tools.get_modekey_sign(mode)
    ms = tools.pair_to_str(mode_sign)
    pyline = 'from sel import multspec; multspec.%s_tag_mode("%s", "%s", "%s", "%s", test=%s)'% (tag, reweight, datatype, mode, label, opts.test)

    bash_file_name = 'multspec-%s.sh' % ms 
    bash_file = create_bash_file_pyline(opts, label, datatype, pyline,
                                        bash_file_name, subdir='sel')
    logname = '%s_%s.txt' %(datatype.replace('/', '_'), mode)
    logpath = os.path.join(attr.logpath, label, 'multspec')
    logfile = tools.set_file(extbase=logpath, comname=logname)
    qjobname = 'sel%s' % ms

    tools.qsub_jobs(logfile, qjobname, bash_file, opts.test)

