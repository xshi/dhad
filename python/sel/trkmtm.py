"""
Module to select track momentum

"""

import os
import sys
import tools
import attr
import sel
from attr import modes
from attr.pdg import *
from tools.filetools import UserFile 
from yld import parse_args, create_bash_file
from tools import makeDDecaySubTree, mcDmodeFixRad, pmag, cosangle, \
     invmasssq
from ROOT import TFile, TH1F, TH2F
from tools.ttree import histBox
from tools.cuts import chooseD
import shelve


__author__ = "Xin Shi <xs32@cornell.edu>"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2005-2011 Xin Shi"
__license__ = "GPL"
__revision__ = "$Revision$"


def main(opts, args):
    parsed = parse_args(args)
    datatype  = parsed[0]
    tag       = parsed[1]
    modes     = parsed[2]
    label     = parsed[3]

    for mode in modes:
        if opts.set and opts.set == 'interact':
            if tag == 'single':
                single_tag_mode(datatype, mode, label, opts.test)
            else:
                raise ValueError(tag)
            continue

        script, logfile, qjobname = create_script_logfile_jobname(
            opts, datatype, tag, mode, label)

        bash_file = create_bash_file(opts, datatype, label,
                                     script, 'trkmtm.sh', 'sel')
        tools.qsub_jobs(logfile, qjobname, bash_file, opts.test)


def single_tag_mode(datatype, mode, label, test=False):
    sys.stdout.write('dhad.sel.trkmtm: Processing Mode %s...' % mode)
    sys.stdout.flush()

    datpath = attr.datpath
    rootfile = tools.get_rootfile(datatype, mode, label)

    pt = tools.add_rootfile(rootfile)

    selfile = get_selfile(datatype, mode, label, test=test)
    nselected, ntotal = output_trkmtm(pt, mode, selfile, label, test)
    
    sys.stdout.write(' selected %s out of %s.\n' % (nselected, ntotal))
    sys.stdout.write('Saved as %s \n' %selfile)
    sys.stdout.flush()


def output_trkmtm(pt, mode, selfile, label, test=False):
    modekey, signs = tools.get_modekey_sign(mode)
    sname = attr.modes[modekey]['sname'].lower()

    if sname == 'kpipi0':
        nselected, ntotal = output_trkmtm_kpipi0(
            pt, mode, selfile, label, test)
    elif sname == 'k3pi':
        nselected, ntotal = output_trkmtm_k3pi(
            pt, mode, selfile, label, test)
    elif sname == 'kpipi':
        nselected, ntotal = output_trkmtm_kpipi(
            pt, mode, selfile, label, test)
    elif sname == 'kpipipi0':
        nselected, ntotal = output_trkmtm_kpipipi0(
            pt, mode, selfile, label, test)
    elif sname == 'kspipi0':
        nselected, ntotal = output_trkmtm_kspipi0(
            pt, mode, selfile, label, test)
    elif sname == 'ks3pi':
        nselected, ntotal = output_trkmtm_ks3pi(
            pt, mode, selfile, label, test)
    elif sname == 'kkpi':
        nselected, ntotal = output_trkmtm_kkpi(
            pt, mode, selfile, label, test)
    else:
        raise NameError(sname)

    return nselected, ntotal


def output_trkmtm_kpipi0(pt, mode, selfile, label, test=False):
    nselected = 0 
    ntotal = 0 
    modekey, signs = tools.get_modekey_sign(mode)

    if signs != None: # single tag
        if not isinstance(signs, list):
            signs = [signs] 

    real_k_pmag = 0 ; real_p1_pmag = 0 ;  real_pz_pmag = 0

    mbc = {}; kpi1 = {} ; kpi2 = {}; pipih = {}; pipil = {}; pipipi = {}
    kpiz = {}; kpipih = {}; kpipil = {}
    h_pk = {}; h_ppi1 = {}; h_ppiz = {}
    h_angk = {}; h_angpi1 = {}; h_angpi2 = {}; h_angpiz = {}

    f = TFile(selfile, 'recreate')

    efffile = selfile.replace('.root', '.db')
    effs = shelve.open(efffile)

    h_k_dp = TH1F('h_k_dp', 'K delta p', 100, -0.05, 0.05)
    h_p1_dp = TH1F('h_p1_dp', 'pi1 delta p', 100, -0.05, 0.05)
    h_pz_dp = TH1F('h_pz_dp', 'pi^{0} delta p', 100, -0.05, 0.05)
    
    for type in ('mc', 'mctruth'):
        mbc[type] = TH1F('mbc_' + type, 'mbc', 100, 1.83, 1.89)
        h_pk[type] = TH1F('h_pk_' + type, 'K^{-} momentum', 20, 0, 1)
        h_ppi1[type] = TH1F('h_ppi1_' + type, '#pi^{+} momentum', 20, 0, 1)
        h_ppiz[type] = TH1F('h_ppiz_' + type, '#pi^{0} momentum', 20, 0, 1)

    args = (11, 0, 1.1, 8, 0, 1.0, 8, 0, 1.0)
    boxes_num = histBox(*args)
    boxes_denom = histBox(*args)

    for pte in pt:
        if test and nselected > 10:
            break

        ntotal += 1
        for sign in signs:

            loctree = makeDDecaySubTree(pte, sign)
   
            if sign == 1 and mcDmodeFixRad(
                loctree[0].mcDmode()) != modes[1]['mcdmode']:
                continue
            if sign == -1 and mcDmodeFixRad(
                loctree[0].mcDmode()) != modes[1]['mcdbmode']:
                continue
            # do MC truth stuff first
            mc_k = None
            mc_pi1 = None
            mc_piz = None
            reald = loctree[0]
            nodes_of_interest = reald.interestingDescendants()

            for node in nodes_of_interest:
                if node.pdgid == sign*pdgid_Km:
                    mc_k = node
                elif node.pdgid == sign*pdgid_pip:
                    if not mc_pi1:
                        mc_pi1 = node
                    else:
                        print 'ERROR'
                elif node.pdgid == pdgid_piz:
                    mc_piz = node
            if not mc_k or not mc_pi1 or not mc_piz:
                print 'ERROR2', mc_k, mc_pi1, mc_piz
            else:
                pass

            k = mc_k.index ; pip1 = mc_pi1.index ; 
            piz = mc_piz.index
            pk = (pte.mce[k], pte.mcpx[k], pte.mcpy[k], pte.mcpz[k])
            ppip1 = (pte.mce[pip1], pte.mcpx[pip1], pte.mcpy[pip1],
                     pte.mcpz[pip1])
            ppiz = (pte.mce[piz], pte.mcpx[piz], pte.mcpy[piz], pte.mcpz[piz])
            real_k_pmag = pmag(pk) ; real_pz_pmag = pmag(ppiz)

            h_pk['mctruth'].Fill(real_k_pmag)
            h_ppiz['mctruth'].Fill(real_pz_pmag)
            mag_ppi1 = pmag(ppip1)
            h_ppi1['mctruth'].Fill(mag_ppi1)
            real_p1_pmag = mag_ppi1

            boxes_denom.fill(real_k_pmag, real_p1_pmag, real_pz_pmag)

            choice = chooseD(modekey, pte, sign)
            if choice != None : #and passDE(choice, pte): included in chooseD
                nselected += 1
                mbc['mc'].Fill(pte.dmbc[choice])
                if not 1.86 < pte.dmbc[choice] < 1.87:
                    continue
                k = pte.ddau1[choice]; pip1 = pte.ddau2[choice];
                piz = pte.ddau3[choice]
                pk = (pte.trke[k], pte.trkpx[k], pte.trkpy[k],
                      pte.trkpz[k])
                ppip1 = (pte.trpie[pip1], pte.trpipx[pip1], pte.trpipy[pip1],
                         pte.trpipz[pip1])
                ppiz = (pte.pi0e[piz], pte.pi0px[piz], pte.pi0py[piz],
                        pte.pi0pz[piz])
                h_k_dp.Fill(pmag(pk)-real_k_pmag)
                h_pz_dp.Fill(pmag(ppiz)-real_pz_pmag)
                h_pk['mc'].Fill(pmag(pk))
                h_ppiz['mc'].Fill(pmag(ppiz))
                mag_ppi1 = pmag(ppip1);
                h_ppi1['mc'].Fill(mag_ppi1)
                h_p1_dp.Fill(mag_ppi1 - real_p1_pmag)

                boxes_num.fill(pmag(pk), mag_ppi1, pmag(ppiz))

    effs['boxes_num'] = boxes_num
    effs['boxes_denom'] = boxes_denom 
    effs.close()
    f.Write()
    f.Close()
    pt.Delete()

    return nselected, ntotal


def output_trkmtm_k3pi(pt, mode, selfile, label, test=False):
    nselected = 0 
    ntotal = 0 
    modekey, signs = tools.get_modekey_sign(mode)

    if signs != None: # single tag
        if not isinstance(signs, list):
            signs = [signs] 

    f = TFile(selfile, 'recreate')

    efffile = selfile.replace('.root', '.db')
    effs = shelve.open(efffile)

    real_k_pmag = 0 ; real_p1_pmag = 0 ; real_p2_pmag = 0; real_pz_pmag = 0

    mbc = {}; kpi1 = {} ; kpi2 = {}; pipih = {}; pipil = {}; pipipi = {}
    kpim = {}; kpipih = {}; kpipil = {}
    h_pk = {}; h_ppi1 = {}; h_ppi2 = {}; h_ppim = {}
    h_angk = {}; h_angpi1 = {}; h_angpi2 = {}; h_angpim = {}

    h_k_dp = TH1F('h_k_dp', 'K delta p', 100, -0.05, 0.05)
    h_p1_dp = TH1F('h_p1_dp', 'pi1 delta p', 100, -0.05, 0.05)
    h_p2_dp = TH1F('h_p2_dp', 'pi2 delta p', 100, -0.05, 0.05)
    h_pm_dp = TH1F('h_pm_dp', 'pi- delta p', 100, -0.05, 0.05)
    
    for tp in ('mc', 'mctruth'):
        mbc[tp] = TH1F('mbc_' + tp, 'mbc', 100, 1.83, 1.89)
        h_pk[tp] = TH1F('h_pk_' + tp, 'K^{-} momentum', 20, 0, 1)
        h_ppi1[tp] = TH1F('h_ppi1_' + tp, '#pi^{+}_{1} momentum', 20, 0, 1)
        h_ppi2[tp] = TH1F('h_ppi2_' + tp, '#pi^{+}_{2} momentum', 20, 0, 1)
        h_ppim[tp] = TH1F('h_ppim_' + tp, '#pi^{-} momentum', 20, 0, 1)

    args_p = (12, 0.1, 0.95, 4, 0.05, 0.9, 8, 0.05, 0.75, 4, 0.05, 0.9)
    args_a = (6, 0, 1, 6, 0, 1, 6, 0, 1, 6, 0, 1)
    boxes_num_p = histBox(*args_p)
    boxes_denom_p = histBox(*args_p)
    boxes_num_a = histBox(*args_a)
    boxes_denom_a = histBox(*args_a)

    for pte in pt:
        if test and nselected > 10:
            break

        ntotal += 1
        for sign in signs:
            loctree = makeDDecaySubTree(pte, sign)
            if sign == 1 and mcDmodeFixRad(
                loctree[0].mcDmode()) != modes[3]['mcdmode']:
                continue
            if sign == -1 and mcDmodeFixRad(
                loctree[0].mcDmode()) != modes[3]['mcdbmode']:
                continue
            # do MC truth stuff first
            mc_k = None
            mc_pi1 = None
            mc_pi2 = None
            mc_pim = None
            reald = loctree[0]
            nodes_of_interest = reald.interestingDescendants()

            for node in nodes_of_interest:
                if node.pdgid == sign*pdgid_Km:
                    mc_k = node
                elif node.pdgid == sign*pdgid_pip:
                    if not mc_pi1:
                        mc_pi1 = node
                    else:
                        if mc_pi2:
                            print 'ERROR'
                            print len(nodes_of_interest)
                            print mc_pi1
                            print mc_pi2
                            print node
                            print ' ---- '
                            for nnode in nodes_of_interest:
                                print nnode
                                print '-'
                            print '================='
                        mc_pi2 = node
                elif node.pdgid == pdgid_pim:
                    mc_pim = node

            if not mc_k or not mc_pi1 or not mc_pi2 or not mc_pim:
                print 'ERROR2', mc_k, mc_pi1, mc_pi2, mc_pim
            else:
                pass

            k = mc_k.index ; pip1 = mc_pi1.index ; pip2 = mc_pi2.index
            pim = mc_pim.index
            pk = (pte.mce[k], pte.mcpx[k], pte.mcpy[k],
                  pte.mcpz[k])
            ppip1 = (pte.mce[pip1], pte.mcpx[pip1], pte.mcpy[pip1],
                     pte.mcpz[pip1])
            ppip2 = (pte.mce[pip2], pte.mcpx[pip2], pte.mcpy[pip2],
                     pte.mcpz[pip2])
            ppim = (pte.mce[pim], pte.mcpx[pim], pte.mcpy[pim],
                    pte.mcpz[pim])
            real_k_pmag = pmag(pk) ; real_pm_pmag = pmag(ppim)
            zhat = (0,1,0,0)
            ang_k = abs(cosangle(pk,zhat))
            ang_pim = abs(cosangle(ppim,zhat))
            h_pk['mctruth'].Fill(real_k_pmag)
            h_ppim['mctruth'].Fill(real_pm_pmag)
            mag_ppi1 = pmag(ppip1); mag_ppi2 = pmag(ppip2)
            if max(mag_ppi1, mag_ppi2) == mag_ppi1:
                h_ppi1['mctruth'].Fill(mag_ppi1)
                h_ppi2['mctruth'].Fill(mag_ppi2)
                real_p1_pmag = mag_ppi1 ; real_p2_pmag = mag_ppi2
                ang_pi1 = abs(cosangle(ppip1,zhat));
                ang_pi2 = abs(cosangle(ppip2,zhat))
            else:
                h_ppi1['mctruth'].Fill(mag_ppi2)
                h_ppi2['mctruth'].Fill(mag_ppi1)
                real_p1_pmag = mag_ppi2 ; real_p2_pmag = mag_ppi1
                ang_pi1 = abs(cosangle(ppip2,zhat));
                ang_pi2 = abs(cosangle(ppip1,zhat))


            boxes_denom_p.fill(real_k_pmag, real_p1_pmag, real_p2_pmag,
                               real_pm_pmag)
            boxes_denom_a.fill(ang_k, ang_pi1, ang_pi2, ang_pim)

            choice = chooseD(3, pte, sign)

            if choice != None: # and passDE(choice, pte):
                nselected += 1
                mbc['mc'].Fill(pte.dmbc[choice])
                if not 1.86 < pte.dmbc[choice] < 1.87:
                    continue
                k = pte.ddau1[choice]; pip1 = pte.ddau2[choice];
                pip2 = pte.ddau3[choice]; pim = pte.ddau4[choice]
                pk = (pte.trke[k], pte.trkpx[k], pte.trkpy[k],
                  pte.trkpz[k])
                ppip1 = (pte.trpie[pip1], pte.trpipx[pip1], pte.trpipy[pip1],
                         pte.trpipz[pip1])
                ppip2 = (pte.trpie[pip2], pte.trpipx[pip2], pte.trpipy[pip2],
                         pte.trpipz[pip2])
                ppim = (pte.trpie[pim], pte.trpipx[pim], pte.trpipy[pim],
                        pte.trpipz[pim])
                h_k_dp.Fill(pmag(pk)-real_k_pmag)
                h_pm_dp.Fill(pmag(ppim)-real_pm_pmag)
                h_pk['mc'].Fill(pmag(pk))
                h_ppim['mc'].Fill(pmag(ppim))
                ang_k = abs(pte.trcosth[k]); ang_pim = abs(pte.trcosth[pim])
                mag_ppi1 = pmag(ppip1); mag_ppi2 = pmag(ppip2)
                if max(mag_ppi1, mag_ppi2) == mag_ppi1:
                    h_ppi1['mc'].Fill(mag_ppi1)
                    h_ppi2['mc'].Fill(mag_ppi2)
                    h_p1_dp.Fill(mag_ppi1 - real_p1_pmag)
                    h_p2_dp.Fill(mag_ppi2 - real_p2_pmag)
                    ang_pi1 = abs(pte.trcosth[pip1])
                    ang_pi2 = abs(pte.trcosth[pip2])
                else:
                    h_ppi1['mc'].Fill(mag_ppi2)
                    h_ppi2['mc'].Fill(mag_ppi1)
                    h_p1_dp.Fill(mag_ppi2 - real_p1_pmag)
                    h_p2_dp.Fill(mag_ppi1 - real_p2_pmag)
                    ang_pi1 = abs(pte.trcosth[pip2])
                    ang_pi2 = abs(pte.trcosth[pip1])
                boxes_num_p.fill(pmag(pk), min(mag_ppi2, mag_ppi1),
                                 max(mag_ppi2, mag_ppi1),
                                 pmag(ppim))
                boxes_num_a.fill(ang_k, ang_pi1, ang_pi2, ang_pim)

    effs['boxes_num_p'] = boxes_num_p
    effs['boxes_denom_p'] = boxes_denom_p
    effs['boxes_num_a'] = boxes_num_a
    effs['boxes_denom_a'] = boxes_denom_a
    effs.close()
    f.Write()
    f.Close()
    pt.Delete()

    return nselected, ntotal


def output_trkmtm_kpipi(pt, mode, selfile, label, test=False):
    nselected = 0 
    ntotal = 0 
    modekey, signs = tools.get_modekey_sign(mode)

    if signs != None: # single tag
        if not isinstance(signs, list):
            signs = [signs] 

    real_k_pmag = 0 ; real_p1_pmag = 0 ;  real_p2_pmag = 0

    mbc = {}; kpi1 = {} ; kpi2 = {}; pipih = {}; pipil = {}; pipipi = {}
    kpim = {}; kpipih = {}; kpipil = {}
    h_pk = {}; h_ppi1 = {}; h_ppi2 = {}; h_ppim = {}
    h_angk = {}; h_angpi1 = {}; h_angpi2 = {}; h_angpim = {}

    f = TFile(selfile, 'recreate')

    efffile = selfile.replace('.root', '.db')
    effs = shelve.open(efffile)

    h_k_dp = TH1F('h_k_dp', 'K^{-} delta p', 100, -0.05, 0.05)
    h_p1_dp = TH1F('h_p1_dp', '#pi^{+}_{1} delta p', 100, -0.05, 0.05)
    h_p2_dp = TH1F('h_p2_dp', '#pi^{+}_{2} delta p', 100, -0.05, 0.05)

    for type in ('mc', 'mctruth'):
        mbc[type] = TH1F('mbc_' + type, 'mbc', 100, 1.83, 1.89)
        h_pk[type] = TH1F('h_pk_' + type, 'K^{-} momentum', 20, 0, 1)
        h_ppi1[type] = TH1F('h_ppi1_' + type, '#pi^{+}_{1} momentum', 20, 0, 1)
        h_ppi2[type] = TH1F('h_ppi2_' + type, '#pi^{+}_{2} momentum', 20, 0, 1)

    args_p = (12, 0.1, 0.95, 4, 0.05, 0.9, 8, 0.05, 0.75)
    args_a = (6, 0, 1, 6, 0, 1, 6, 0, 1)
    boxes_num_p = histBox(*args_p)
    boxes_denom_p = histBox(*args_p)
    boxes_num_a = histBox(*args_a)
    boxes_denom_a = histBox(*args_a)

    for pte in pt:
        if test and nselected > 10:
            break

        ntotal += 1
        for sign in signs:
            loctree = makeDDecaySubTree(pte, sign)
            if sign == 1 and mcDmodeFixRad(
                loctree[0].mcDmode()) != modes[200]['mcdmode']:
                continue
            if sign == -1 and mcDmodeFixRad(
                loctree[0].mcDmode()) != modes[200]['mcdbmode']:
                continue
            # do MC truth stuff first
            mc_k = None; mc_pi1 = None; mc_pi2 = None
            reald = loctree[0]
            nodes_of_interest = reald.interestingDescendants()

            for node in nodes_of_interest:
                if node.pdgid == sign*pdgid_Km:
                    mc_k = node
                elif node.pdgid == sign*pdgid_pip:
                    if not mc_pi1:
                        mc_pi1 = node
                    else:
                        if mc_pi2:
                            print 'ERROR'
                            print len(nodes_of_interest)
                            print mc_pi1
                            print mc_pi2
                            print node
                            print ' ---- '
                            for nnode in nodes_of_interest:
                                print nnode
                                print '-'
                            print '================='
                        mc_pi2 = node
            if not mc_k or not mc_pi1 or not mc_pi2:
                print 'ERROR2', mc_k, mc_pi1, mc_pi2
            else:
                pass
            k = mc_k.index ; pip1 = mc_pi1.index ; pip2 = mc_pi2.index
            pk = (pte.mce[k], pte.mcpx[k], pte.mcpy[k],
                  pte.mcpz[k])
            ppip1 = (pte.mce[pip1], pte.mcpx[pip1], pte.mcpy[pip1],
                     pte.mcpz[pip1])
            ppip2 = (pte.mce[pip2], pte.mcpx[pip2], pte.mcpy[pip2],
                     pte.mcpz[pip2])
            real_k_pmag = pmag(pk)
            zhat = (0,1,0,0)
            ang_k = abs(cosangle(pk,zhat))
            h_pk['mctruth'].Fill(real_k_pmag)
            mag_ppi1 = pmag(ppip1); mag_ppi2 = pmag(ppip2)
            if max(mag_ppi1, mag_ppi2) == mag_ppi1:
                h_ppi1['mctruth'].Fill(mag_ppi1)
                h_ppi2['mctruth'].Fill(mag_ppi2)
                real_p1_pmag = mag_ppi1 ; real_p2_pmag = mag_ppi2
                ang_pi1 = abs(cosangle(ppip1,zhat));
                ang_pi2 = abs(cosangle(ppip2,zhat))
            else:
                h_ppi1['mctruth'].Fill(mag_ppi2)
                h_ppi2['mctruth'].Fill(mag_ppi1)
                real_p1_pmag = mag_ppi2 ; real_p2_pmag = mag_ppi1
                ang_pi1 = abs(cosangle(ppip2,zhat));
                ang_pi2 = abs(cosangle(ppip1,zhat))
                
            boxes_denom_p.fill(real_k_pmag, real_p1_pmag, real_p2_pmag)
            boxes_denom_a.fill(ang_k, ang_pi1, ang_pi2)
        
            choice = chooseD(200, pte, sign)
            if choice != None : #and passDE(choice, pte): included in chooseD
                nselected += 1
                mbc['mc'].Fill(pte.dmbc[choice])
                if not 1.865 < pte.dmbc[choice] < 1.875:
                    continue
                k = pte.ddau1[choice]; pip1 = pte.ddau2[choice];
                pip2 = pte.ddau3[choice]
                pk = (pte.trke[k], pte.trkpx[k], pte.trkpy[k],
                      pte.trkpz[k])
                ppip1 = (pte.trpie[pip1], pte.trpipx[pip1], pte.trpipy[pip1],
                         pte.trpipz[pip1])
                ppip2 = (pte.trpie[pip2], pte.trpipx[pip2], pte.trpipy[pip2],
                         pte.trpipz[pip2])
                h_k_dp.Fill(pmag(pk)-real_k_pmag)
                h_pk['mc'].Fill(pmag(pk))
                ang_k = abs(pte.trcosth[k])
                mag_ppi1 = pmag(ppip1); mag_ppi2 = pmag(ppip2)
                if max(mag_ppi1, mag_ppi2) == mag_ppi1:
                    h_ppi1['mc'].Fill(mag_ppi1)
                    h_ppi2['mc'].Fill(mag_ppi2)
                    h_p1_dp.Fill(mag_ppi1 - real_p1_pmag)
                    h_p2_dp.Fill(mag_ppi2 - real_p2_pmag)
                    ang_pi1 = abs(pte.trcosth[pip1])
                    ang_pi2 = abs(pte.trcosth[pip2])
                else:
                    h_ppi1['mc'].Fill(mag_ppi2)
                    h_ppi2['mc'].Fill(mag_ppi1)
                    h_p1_dp.Fill(mag_ppi2 - real_p1_pmag)
                    h_p2_dp.Fill(mag_ppi1 - real_p2_pmag)
                    ang_pi1 = abs(pte.trcosth[pip2])
                    ang_pi2 = abs(pte.trcosth[pip1])
                boxes_num_p.fill(pmag(pk), min(mag_ppi2, mag_ppi1),
                                 max(mag_ppi2, mag_ppi1))
                
                boxes_num_a.fill(ang_k, ang_pi1, ang_pi2)

    effs['boxes_num_p'] = boxes_num_p
    effs['boxes_denom_p'] = boxes_denom_p
    effs['boxes_num_a'] = boxes_num_a
    effs['boxes_denom_a'] = boxes_denom_a
    effs.close()
    f.Write()
    f.Close()
    pt.Delete()

    return nselected, ntotal


def output_trkmtm_kpipipi0(pt, mode, selfile, label, test=False):
    nselected = 0 
    ntotal = 0 
    modekey, signs = tools.get_modekey_sign(mode)

    f = TFile(selfile, 'recreate')
    efffile = selfile.replace('.root', '.db')
    effs = shelve.open(efffile)

    if signs != None: # single tag
        if not isinstance(signs, list):
            signs = [signs] 

    real_k_pmag = 0 ; real_p1_pmag = 0 ; real_p2_pmag = 0 ; real_pz_pmag = 0
    mbc = {}; kpi1 = {} ; kpi2 = {}; pipih = {}; pipil = {}; pipipi = {}
    kpim = {}; kpipih = {}; kpipil = {}
    h_pk = {}; h_ppi1 = {}; h_ppi2 = {}; h_ppiz = {}
    h_angk = {}; h_angpi1 = {}; h_angpi2 = {}; h_angpiz = {}

    h_k_dp = TH1F('h_k_dp', 'K^{-} delta p', 100, -0.05, 0.05)
    h_p1_dp = TH1F('h_p1_dp', 'pi1 delta p', 100, -0.05, 0.05)
    h_p2_dp = TH1F('h_p2_dp', 'pi2 delta p', 100, -0.05, 0.05)
    h_pz_dp = TH1F('h_pm_dp', 'pi^{0} delta p', 100, -0.05, 0.05)

    for type in ('mc', 'mctruth'):
        mbc[type] = TH1F('mbc_' + type, 'mbc', 100, 1.83, 1.89)
        h_pk[type] = TH1F('h_pk_' + type, 'K^{-} momentum', 20, 0, 1)
        h_ppi1[type] = TH1F('h_ppi1_' + type, '#pi^{+}_{1} momentum', 20, 0, 1)
        h_ppi2[type] = TH1F('h_ppi2_' + type, '#pi^{+}_{2} momentum', 20, 0, 1)
        h_ppiz[type] = TH1F('h_ppim_' + type, '#pi^{0} momentum', 20, 0, 1)
    
    args_p = (12, 0.1, 0.95, 4, 0.05, 0.9, 8, 0.05, 0.75, 4, 0.05, 0.9)
    args_a = (6, 0, 1, 6, 0, 1, 6, 0, 1, 6, 0, 1)
    boxes_num_p = histBox(*args_p)
    boxes_denom_p = histBox(*args_p)
    boxes_num_a = histBox(*args_a)
    boxes_denom_a = histBox(*args_a)

    for pte in pt:
        if test and nselected > 10:
            break

        ntotal += 1
        for sign in signs:
            loctree = makeDDecaySubTree(pte, sign)

            if sign == 1 and mcDmodeFixRad(
                loctree[0].mcDmode()) != modes[201]['mcdmode']:
                continue
            if sign == -1 and mcDmodeFixRad(
                loctree[0].mcDmode()) != modes[201]['mcdbmode']:
                continue
            mc_k = None; mc_pi1 = None; mc_pi2 = None; mc_piz = None
            reald = loctree[0]
            nodes_of_interest = reald.interestingDescendants()
            for node in nodes_of_interest:
                if node.pdgid == sign*pdgid_Km:
                    mc_k = node
                elif node.pdgid == sign*pdgid_pip:
                    if not mc_pi1:
                        mc_pi1 = node
                    else:
                        if mc_pi2:
                            print 'ERROR'
                            print len(nodes_of_interest)
                            print mc_pi1
                            print mc_pi2
                            print node
                            print ' ---- '
                            for nnode in nodes_of_interest:
                                print nnode
                                print '-'
                            print '================='
                        mc_pi2 = node
                elif node.pdgid == sign*pdgid_piz:
                    mc_piz = node
        
            if not mc_k or not mc_pi1 or not mc_pi2 or not mc_piz:
                print 'ERROR2', mc_ks, mc_pi1, mc_pi2, mc_pim
            else:
                pass
            k = mc_k.index ; pip1 = mc_pi1.index ; pip2 = mc_pi2.index
            piz = mc_piz.index
            pk = (pte.mce[k], pte.mcpx[k], pte.mcpy[k],
                  pte.mcpz[k])
            ppip1 = (pte.mce[pip1], pte.mcpx[pip1], pte.mcpy[pip1],
                     pte.mcpz[pip1])
            ppip2 = (pte.mce[pip2], pte.mcpx[pip2], pte.mcpy[pip2],
                     pte.mcpz[pip2])
            ppiz = (pte.mce[piz], pte.mcpx[piz], pte.mcpy[piz],
                    pte.mcpz[piz])
            real_k_pmag = pmag(pk) ; real_pz_pmag = pmag(ppiz)
            zhat = (0,1,0,0)
            ang_k = abs(cosangle(pk,zhat))
            ang_piz = abs(cosangle(ppiz,zhat))
            h_pk['mctruth'].Fill(real_k_pmag)
            h_ppiz['mctruth'].Fill(real_pz_pmag)
            mag_ppi1 = pmag(ppip1); mag_ppi2 = pmag(ppip2)
            if max(mag_ppi1, mag_ppi2) == mag_ppi1:
                h_ppi1['mctruth'].Fill(mag_ppi1)
                h_ppi2['mctruth'].Fill(mag_ppi2)
                real_p1_pmag = mag_ppi1 ; real_p2_pmag = mag_ppi2
                ang_pi1 = abs(cosangle(ppip1,zhat));
                ang_pi2 = abs(cosangle(ppip2,zhat))
            else:
                h_ppi1['mctruth'].Fill(mag_ppi2)
                h_ppi2['mctruth'].Fill(mag_ppi1)
                real_p1_pmag = mag_ppi2 ; real_p2_pmag = mag_ppi1
                ang_pi1 = abs(cosangle(ppip2,zhat));
                ang_pi2 = abs(cosangle(ppip1,zhat))

            boxes_denom_p.fill(real_k_pmag, real_p1_pmag, real_p2_pmag,
                               real_pz_pmag)
            boxes_denom_a.fill(ang_k, ang_pi1, ang_pi2, ang_piz)
            
            choice = chooseD(201, pte, sign)
            if choice != None : #and passDE(choice, pte): included in chooseD
                nselected += 1
                
                mbc['mc'].Fill(pte.dmbc[choice])
                if not 1.86 < pte.dmbc[choice] < 1.87:
                    continue
                k = pte.ddau1[choice]; pip1 = pte.ddau2[choice];
                pip2 = pte.ddau3[choice]; piz = pte.ddau4[choice]
                pk = (pte.trke[k], pte.trkpx[k], pte.trkpy[k],
                      pte.trkpz[k])
                ppip1 = (pte.trpie[pip1], pte.trpipx[pip1], pte.trpipy[pip1],
                         pte.trpipz[pip1])
                ppip2 = (pte.trpie[pip2], pte.trpipx[pip2], pte.trpipy[pip2],
                         pte.trpipz[pip2])
                ppiz = (pte.pi0e[piz], pte.pi0px[piz], pte.pi0py[piz],
                        pte.pi0pz[piz])
                h_k_dp.Fill(pmag(pk)-real_k_pmag)
                h_pz_dp.Fill(pmag(ppiz)-real_pz_pmag)
                h_pk['mc'].Fill(pmag(pk))
                h_ppiz['mc'].Fill(pmag(ppiz))
                ang_k = abs(pte.trcosth[k]); ang_pim = abs(ang_piz)
                mag_ppi1 = pmag(ppip1); mag_ppi2 = pmag(ppip2)
                
                if max(mag_ppi1, mag_ppi2) == mag_ppi1:
                    h_ppi1['mc'].Fill(mag_ppi1)
                    h_ppi2['mc'].Fill(mag_ppi2)
                    h_p1_dp.Fill(mag_ppi1 - real_p1_pmag)
                    h_p2_dp.Fill(mag_ppi2 - real_p2_pmag)
                    ang_pi1 = abs(pte.trcosth[pip1])
                    ang_pi2 = abs(pte.trcosth[pip2])
                else:
                    h_ppi1['mc'].Fill(mag_ppi2)
                    h_ppi2['mc'].Fill(mag_ppi1)
                    h_p1_dp.Fill(mag_ppi2 - real_p1_pmag)
                    h_p2_dp.Fill(mag_ppi1 - real_p2_pmag)
                    ang_pi1 = abs(pte.trcosth[pip2])
                    ang_pi2 = abs(pte.trcosth[pip1])
                boxes_num_p.fill(pmag(pk), min(mag_ppi2, mag_ppi1),
                                 max(mag_ppi2, mag_ppi1),
                                 pmag(ppiz))
                
                boxes_num_a.fill(ang_k, ang_pi1, ang_pi2, ang_piz)

    effs['boxes_num_p'] = boxes_num_p
    effs['boxes_denom_p'] = boxes_denom_p
    effs['boxes_num_a'] = boxes_num_a
    effs['boxes_denom_a'] = boxes_denom_a
    effs.close()
    f.Write()
    f.Close()
    pt.Delete()

    return nselected, ntotal
                

def output_trkmtm_kspipi0(pt, mode, selfile, label, test=False):
    nselected = 0 
    ntotal = 0 
    modekey, signs = tools.get_modekey_sign(mode)

    f = TFile(selfile, 'recreate')
    efffile = selfile.replace('.root', '.db')
    effs = shelve.open(efffile)

    if signs != None: # single tag
        if not isinstance(signs, list):
            signs = [signs] 

    mbc = {}; kpi1 = {} ; kpi2 = {}; pipih = {}; pipil = {}; pipipi = {}
    kpiz = {}; kpipih = {}; kpipil = {}
    h_pks = {}; h_ppi1 = {}; h_ppiz = {}
    h_angks = {}; h_angpi1 = {}; h_angpi2 = {}; h_angpiz = {}
    real_ks_pmag = 0 ; real_p1_pmag = 0 ;  real_pz_pmag = 0

    h_ks_dp = TH1F('h_ks_dp', 'K_{S} delta p', 100, -0.05, 0.05)
    h_p1_dp = TH1F('h_p1_dp', '#pi^{+} delta p', 100, -0.05, 0.05)
    h_pz_dp = TH1F('h_pz_dp', '#pi^{0} delta p', 100, -0.05, 0.05)
    
    h_dalitz = TH2F('h_dalitz', 'K_{S} #pi^{+} #pi^{0} Dalitz plot',
                    100, 0, 2, 100, 0, 3)
    for type in ('mc', 'mctruth'):
        mbc[type] = TH1F('mbc_' + type, 'mbc', 100, 1.83, 1.89)
        h_pks[type] = TH1F('h_pks_' + type, 'K_{S} momentum', 20, 0, 1)
        h_ppi1[type] = TH1F('h_ppi1_' + type, '#pi^{+} momentum', 20, 0, 1)
        h_ppiz[type] = TH1F('h_ppiz_' + type, '#pi^{0} momentum', 20, 0, 1)

    args = (11, 0, 1.1, 8, 0, 1.0, 8, 0, 1.0)
    boxes_num = histBox(*args)
    boxes_denom = histBox(*args)
    for pte in pt:
        if test and nselected > 10:
            break
        ntotal += 1
        for sign in signs:
            loctree = makeDDecaySubTree(pte, sign)
            if sign == 1 and mcDmodeFixRad(
                loctree[0].mcDmode()) != modes[203]['mcdmode']:
                continue
            if sign == -1 and mcDmodeFixRad(
                loctree[0].mcDmode()) != modes[203]['mcdbmode']:
                continue
            mc_ks = None; mc_pi1 = None; mc_piz = None
            reald = loctree[0]
            nodes_of_interest = reald.interestingDescendants()

            for node in nodes_of_interest:
                if node.pdgid == pdgid_KS or node.pdgid == pdgid_KL:
                    mc_ks = node
                elif node.pdgid == sign*pdgid_pip:
                    if not mc_pi1:
                        mc_pi1 = node
                    else:
                        print 'ERROR'
                elif node.pdgid == pdgid_piz:
                    mc_piz = node

            if mc_ks and mc_ks.pdgid == pdgid_KL:
                continue
            if not mc_ks or not mc_pi1 or not mc_piz:
                print 'ERROR2', mc_ks, mc_pi1, mc_piz
                for node in nodes_of_interest:
                    print node
            else:
                pass

            ks = mc_ks.index ; pip1 = mc_pi1.index ; 
            piz = mc_piz.index
            pks = (pte.mce[ks], pte.mcpx[ks], pte.mcpy[ks],
                  pte.mcpz[ks])
            ppip1 = (pte.mce[pip1], pte.mcpx[pip1], pte.mcpy[pip1],
                     pte.mcpz[pip1])
            ppiz = (pte.mce[piz], pte.mcpx[piz], pte.mcpy[piz],
                    pte.mcpz[piz])
            real_ks_pmag = pmag(pks) ; real_pz_pmag = pmag(ppiz)
            if pmag(ppiz) >0:
                # print 'K0+piz give', invmass(pks, ppiz)
                # print 'piz+pip give', invmass(ppiz, ppip1)
                h_dalitz.Fill(invmasssq(ppiz, ppip1),
                              invmasssq(pks, ppiz))
            h_pks['mctruth'].Fill(real_ks_pmag)
            h_ppiz['mctruth'].Fill(real_pz_pmag)
            mag_ppi1 = pmag(ppip1)
            h_ppi1['mctruth'].Fill(mag_ppi1)
            real_p1_pmag = mag_ppi1

            boxes_denom.fill(real_ks_pmag, real_p1_pmag,
                             real_pz_pmag)
            
            choice = chooseD(203, pte, sign)
            if choice != None: # and passDE(choice, pte):
                nselected += 1
                mbc['mc'].Fill(pte.dmbc[choice])
                if not 1.86 < pte.dmbc[choice] < 1.87:
                    continue
                ks = pte.ddau1[choice]; pip1 = pte.ddau2[choice];
                piz = pte.ddau3[choice]
                pks = (pte.kse[ks], pte.kspx[ks], pte.kspy[ks],
                      pte.kspz[ks])
                ppip1 = (pte.trpie[pip1], pte.trpipx[pip1], pte.trpipy[pip1],
                         pte.trpipz[pip1])
                ppiz = (pte.pi0e[piz], pte.pi0px[piz], pte.pi0py[piz],
                        pte.pi0pz[piz])
                h_ks_dp.Fill(pmag(pks)-real_ks_pmag)
                h_pz_dp.Fill(pmag(ppiz)-real_pz_pmag)
                h_pks['mc'].Fill(pmag(pks))
                h_ppiz['mc'].Fill(pmag(ppiz))
                mag_ppi1 = pmag(ppip1);
                h_ppi1['mc'].Fill(mag_ppi1)
                h_p1_dp.Fill(mag_ppi1 - real_p1_pmag)

                boxes_num.fill(pmag(pks), mag_ppi1, pmag(ppiz))

    effs['boxes_num'] = boxes_num
    effs['boxes_denom'] = boxes_denom 
    effs.close()
    f.Write()
    f.Close()
    pt.Delete()

    return nselected, ntotal

                
def output_trkmtm_ks3pi(pt, mode, selfile, label, test=False):
    nselected = 0 
    ntotal = 0

    modekey, signs = tools.get_modekey_sign(mode)

    f = TFile(selfile, 'recreate')
    efffile = selfile.replace('.root', '.db')
    effs = shelve.open(efffile)

    if signs != None: # single tag
        if not isinstance(signs, list):
            signs = [signs] 

    mbc = {}; kpi1 = {} ; kpi2 = {}; pipih = {}; pipil = {}; pipipi = {}
    kpim = {}; kpipih = {}; kpipil = {}
    h_pks = {}; h_ppi1 = {}; h_ppi2 = {}; h_ppim = {}
    h_angks = {}; h_angpi1 = {}; h_angpi2 = {}; h_angpim = {}
    real_ks_pmag = 0 ; real_p1_pmag = 0 ; real_p2_pmag = 0 ; real_pm_pmag = 0

    h_ks_dp = TH1F('h_ks_dp', 'K_{S} delta p', 100, -0.05, 0.05)
    h_p1_dp = TH1F('h_p1_dp', 'pi1 delta p', 100, -0.05, 0.05)
    h_p2_dp = TH1F('h_p2_dp', 'pi2 delta p', 100, -0.05, 0.05)
    h_pm_dp = TH1F('h_pm_dp', 'pi- delta p', 100, -0.05, 0.05)

    for type in ('mc', 'mctruth'):
        mbc[type] = TH1F('mbc_' + type, 'mbc', 100, 1.83, 1.89)
        h_pks[type] = TH1F('h_pk_' + type, 'K_{S} momentum', 20, 0, 1)
        h_ppi1[type] = TH1F('h_ppi1_' + type, '#pi^{+}_{1} momentum', 20, 0, 1)
        h_ppi2[type] = TH1F('h_ppi2_' + type, '#pi^{+}_{2} momentum', 20, 0, 1)
        h_ppim[type] = TH1F('h_ppim_' + type, '#pi^{-} momentum', 20, 0, 1)

    args_p = (12, 0.1, 0.95, 4, 0.05, 0.9, 8, 0.05, 0.75, 4, 0.05, 0.9)
    args_a = (6, 0, 1, 6, 0, 1, 6, 0, 1, 6, 0, 1)
    boxes_num_p = histBox(*args_p)
    boxes_denom_p = histBox(*args_p)
    boxes_num_a = histBox(*args_a)
    boxes_denom_a = histBox(*args_a)

    for pte in pt:
        if test and nselected > 10:
            break

        ntotal += 1
        for sign in signs:
            loctree = makeDDecaySubTree(pte, sign)
            if sign == 1 and mcDmodeFixRad(
                loctree[0].mcDmode()) != modes[204]['mcdmode']:
                continue
            if sign == -1 and mcDmodeFixRad(
                loctree[0].mcDmode()) != modes[204]['mcdbmode']:
                continue
            mc_ks = None; mc_pi1 = None; mc_pi2 = None; mc_pim = None; mc_kl = None
            reald = loctree[0]

            nodes_of_interest = reald.interestingDescendants()
            for node in nodes_of_interest:
                if node.pdgid == sign*pdgid_KS:
                    mc_ks = node
                elif node.pdgid == sign*pdgid_KL:
                    mc_kl = node
                elif node.pdgid == sign*pdgid_pip:
                    if not mc_pi1:
                        mc_pi1 = node
                    else:
                        if mc_pi2:
                            print 'ERROR'
                            print len(nodes_of_interest)
                            print mc_pi1
                            print mc_pi2
                            print node
                            print ' ---- '
                            for nnode in nodes_of_interest:
                                print nnode
                                print '-'
                            print '================='
                        mc_pi2 = node
                elif node.pdgid == sign*pdgid_pim:
                    mc_pim = node

            if not mc_ks or not mc_pi1 or not mc_pi2 or not mc_pim:
                if mc_kl:
                    continue
                else:
                    print 'ERROR2', mc_ks, mc_pi1, mc_pi2, mc_pim
            else:
                pass
            
            ks = mc_ks.index ; pip1 = mc_pi1.index ; pip2 = mc_pi2.index
            pim = mc_pim.index
            pks = (pte.mce[ks], pte.mcpx[ks], pte.mcpy[ks],
                   pte.mcpz[ks])
            ppip1 = (pte.mce[pip1], pte.mcpx[pip1], pte.mcpy[pip1],
                     pte.mcpz[pip1])
            ppip2 = (pte.mce[pip2], pte.mcpx[pip2], pte.mcpy[pip2],
                     pte.mcpz[pip2])
            ppim = (pte.mce[pim], pte.mcpx[pim], pte.mcpy[pim],
                    pte.mcpz[pim])
            real_ks_pmag = pmag(pks) ; real_pm_pmag = pmag(ppim)
            zhat = (0,1,0,0)
            ang_ks = abs(cosangle(pks,zhat))
            ang_pim = abs(cosangle(ppim,zhat))
            h_pks['mctruth'].Fill(real_ks_pmag)
            h_ppim['mctruth'].Fill(real_pm_pmag)
            mag_ppi1 = pmag(ppip1); mag_ppi2 = pmag(ppip2)
            if max(mag_ppi1, mag_ppi2) == mag_ppi1:
                h_ppi1['mctruth'].Fill(mag_ppi1)
                h_ppi2['mctruth'].Fill(mag_ppi2)
                real_p1_pmag = mag_ppi1 ; real_p2_pmag = mag_ppi2
                ang_pi1 = abs(cosangle(ppip1,zhat));
                ang_pi2 = abs(cosangle(ppip2,zhat))
            else:
                h_ppi1['mctruth'].Fill(mag_ppi2)
                h_ppi2['mctruth'].Fill(mag_ppi1)
                real_p1_pmag = mag_ppi2 ; real_p2_pmag = mag_ppi1
                ang_pi1 = abs(cosangle(ppip2,zhat));
                ang_pi2 = abs(cosangle(ppip1,zhat))

            boxes_denom_p.fill(real_ks_pmag, real_p1_pmag, real_p2_pmag,
                               real_pm_pmag)
            boxes_denom_a.fill(ang_ks, ang_pi1, ang_pi2, ang_pim)
            
            choice = chooseD(204, pte, sign)
            if choice != None: # and passDE(choice, pte):
                nselected += 1
                mbc['mc'].Fill(pte.dmbc[choice])
                if not 1.865 < pte.dmbc[choice] < 1.875:
                    continue
                ks = pte.ddau1[choice]; pip1 = pte.ddau2[choice];
                pip2 = pte.ddau3[choice]; pim = pte.ddau4[choice]
                pks = (pte.kse[ks], pte.kspx[ks], pte.kspy[ks],
                       pte.kspz[ks])
                ppip1 = (pte.trpie[pip1], pte.trpipx[pip1], pte.trpipy[pip1],
                         pte.trpipz[pip1])
                ppip2 = (pte.trpie[pip2], pte.trpipx[pip2], pte.trpipy[pip2],
                         pte.trpipz[pip2])
                ppim = (pte.trpie[pim], pte.trpipx[pim], pte.trpipy[pim],
                        pte.trpipz[pim])
                h_ks_dp.Fill(pmag(pks)-real_ks_pmag)
                h_pm_dp.Fill(pmag(ppim)-real_pm_pmag)
                h_pks['mc'].Fill(pmag(pks))
                h_ppim['mc'].Fill(pmag(ppim))
                try:
                    ang_ks = abs(pte.trcosth[ks])
                    ang_pim = abs(pte.trcosth[pim])
                except IndexError:
                    pass
                
                mag_ppi1 = pmag(ppip1); mag_ppi2 = pmag(ppip2)
                if max(mag_ppi1, mag_ppi2) == mag_ppi1:
                    h_ppi1['mc'].Fill(mag_ppi1)
                    h_ppi2['mc'].Fill(mag_ppi2)
                    h_p1_dp.Fill(mag_ppi1 - real_p1_pmag)
                    h_p2_dp.Fill(mag_ppi2 - real_p2_pmag)
                    ang_pi1 = abs(pte.trcosth[pip1])
                    ang_pi2 = abs(pte.trcosth[pip2])
                else:
                    h_ppi1['mc'].Fill(mag_ppi2)
                    h_ppi2['mc'].Fill(mag_ppi1)
                    h_p1_dp.Fill(mag_ppi2 - real_p1_pmag)
                    h_p2_dp.Fill(mag_ppi1 - real_p2_pmag)
                    ang_pi1 = abs(pte.trcosth[pip2])
                    ang_pi2 = abs(pte.trcosth[pip1])
                boxes_num_p.fill(pmag(pks), min(mag_ppi2, mag_ppi1),
                                 max(mag_ppi2, mag_ppi1),
                                 pmag(ppim))
                boxes_num_a.fill(ang_ks, ang_pi1, ang_pi2, ang_pim)

    effs['boxes_num_p'] = boxes_num_p
    effs['boxes_denom_p'] = boxes_denom_p
    effs['boxes_num_a'] = boxes_num_a
    effs['boxes_denom_a'] = boxes_denom_a
    effs.close()
    f.Write()
    f.Close()
    pt.Delete()

    return nselected, ntotal

def output_trkmtm_kkpi(pt, mode, selfile, label, test=False):
    nselected = 0 
    ntotal = 0

    modekey, signs = tools.get_modekey_sign(mode)

    f = TFile(selfile, 'recreate')
    efffile = selfile.replace('.root', '.db')
    effs = shelve.open(efffile)

    if signs != None: # single tag
        if not isinstance(signs, list):
            signs = [signs] 

    mbc = {}; kpi1 = {} ; kpi2 = {}; pipih = {}; pipil = {}; pipipi = {}
    kpiz = {}; kpipih = {}; kpipil = {}
    h_pkp = {}; h_pkm = {}; h_ppi = {}
    h_angkp = {}; h_angkm = {}; h_angpi = {};

    real_kp_pmag = 0 ; real_km_pmag = 0 ;  real_pi_pmag = 0

    h_kp_dp = TH1F('h_kp_dp', 'K^{+} delta p', 100, -0.05, 0.05)
    h_km_dp = TH1F('h_km_dp', 'K^{-} delta p', 100, -0.05, 0.05)
    h_pi_dp = TH1F('h_pi_dp', '#pi^{+} delta p', 100, -0.05, 0.05)
    
    for type in ('mc', 'mctruth'):
        mbc[type] = TH1F('mbc_' + type, 'mbc', 100, 1.83, 1.89)
        h_pkp[type] = TH1F('h_pkp_' + type, 'K^{+} momentum', 20, 0, 1)
        h_pkm[type] = TH1F('h_pkm_' + type, 'K^{-} momentum', 20, 0, 1)
        h_ppi[type] = TH1F('h_ppi_' + type, '#pi^{+} momentum', 20, 0, 1)

    args = (11, 0, 1.1, 8, 0, 1.0, 8, 0, 1.0)
    boxes_num = histBox(*args)
    boxes_denom = histBox(*args)

    for pte in pt:
        if test and nselected > 10:
            break

        ntotal += 1
        for sign in signs:
            loctree = makeDDecaySubTree(pte, sign)
            if sign == 1 and mcDmodeFixRad(
                loctree[0].mcDmode()) != modes[205]['mcdmode']:
                continue
            if sign == -1 and mcDmodeFixRad(
                loctree[0].mcDmode()) != modes[205]['mcdbmode']:
                continue
            mc_kp = None; mc_km = None; mc_pi = None
            reald = loctree[0]
            nodes_of_interest = reald.interestingDescendants()
            for node in nodes_of_interest:
                if node.pdgid == sign*pdgid_Kp:
                    mc_kp = node
                elif node.pdgid == sign*pdgid_Km:
                    mc_km = node
                elif node.pdgid == sign*pdgid_pip:
                    mc_pi = node

            if not mc_kp or not mc_km or not mc_pi:
                print 'ERROR2', mc_kp, mc_km, mc_pi
            else:
                pass

            kp = mc_kp.index ; km = mc_km.index ; 
            pi = mc_pi.index
            pkp = (pte.mce[kp], pte.mcpx[kp], pte.mcpy[kp],
                   pte.mcpz[kp])
            pkm = (pte.mce[km], pte.mcpx[km], pte.mcpy[km],
                   pte.mcpz[km])
            ppi = (pte.mce[pi], pte.mcpx[pi], pte.mcpy[pi],
                   pte.mcpz[pi])
            real_kp_pmag = pmag(pkp) ; real_km_pmag = pmag(pkm)
            real_pi_pmag = pmag(ppi)
            h_pkp['mctruth'].Fill(real_kp_pmag)
            h_pkm['mctruth'].Fill(real_km_pmag)
            h_ppi['mctruth'].Fill(real_pi_pmag)

            boxes_denom.fill(real_kp_pmag, real_km_pmag,
                             real_pi_pmag)

            choice = chooseD(205, pte, sign)
            if choice != None: # and passDE(choice, pte):
                nselected += 1
                mbc['mc'].Fill(pte.dmbc[choice])
                if not 1.865 < pte.dmbc[choice] < 1.875:
                    continue
                km = pte.ddau1[choice]; kp = pte.ddau2[choice];
                pi = pte.ddau3[choice]
                pkp = (pte.trke[kp], pte.trkpx[kp], pte.trkpy[kp],
                       pte.trkpz[kp])
                pkm = (pte.trke[km], pte.trkpx[km], pte.trkpy[km],
                       pte.trkpz[km])
                ppi = (pte.trpie[pi], pte.trpipx[pi], pte.trpipy[pi],
                       pte.trpipz[pi])
                h_kp_dp.Fill(pmag(pkp)-real_kp_pmag)
                h_km_dp.Fill(pmag(pkm)-real_km_pmag)
                h_pi_dp.Fill(pmag(ppi) - real_pi_pmag)
                h_pkm['mc'].Fill(pmag(pkm))
                h_pkp['mc'].Fill(pmag(pkp))
                h_ppi['mc'].Fill(pmag(ppi))

                boxes_num.fill(pmag(pkp), pmag(pkm), pmag(ppi))

    effs['boxes_num'] = boxes_num
    effs['boxes_denom'] = boxes_denom 
    effs.close()
    f.Write()
    f.Close()
    pt.Delete()

    return nselected, ntotal




def create_script_logfile_jobname(opts, datatype, tag, mode, label):
    logname = '%s_%s.log' %(datatype, mode)
    logpath = os.path.join(attr.sellogpath, label, 'trkmtm')
    logfile = tools.set_file(extbase=logpath, comname=logname)

    content =  '''#!/usr/bin/env python

from sel import trkmtm

trkmtm.single_tag_mode("%s", "%s", "%s", test=%s)

'''% (datatype, mode, label, opts.test)

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

    file_ = os.path.join(attr.datpath, datatype, label, 'src', 'sel', filename)

    verbose = opts.verbose
    if opts.test:
        verbose = 1
    f = UserFile()
    f.data.append(content) 
    f.output(file_, verbose=verbose)
    os.chmod(file_, 0755)

    return filename, logfile, qjobname


def get_selfile(datatype, mode, label, test=False):
    selname = '%s_%s.root' %(datatype, mode)
    if test:
        selname += '.test'
        
    selpath = os.path.join(attr.datpath, 'sel', label, 'trkmtm')
    selfile = tools.check_and_join(selpath, selname)
    return selfile


