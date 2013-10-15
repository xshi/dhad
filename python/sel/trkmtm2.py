"""
Module to select track momentum second stage 

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
from tools import makeDDecaySubTree, mcDmodeFixRad
from tools import pmag, cosangle, invmass, invmasssq, fourvecadd 
from ROOT import TFile, TH1F, TH2F
from tools.cuts import chooseD
import shelve
import shutil


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
                                     script, 'trkmtm2.sh', 'sel')
        tools.qsub_jobs(logfile, qjobname, bash_file, opts.test)


def single_tag_mode(datatype, mode, label, test=False):
    sys.stdout.write('dhad.sel.trkmtm2: Processing Mode %s...' % mode)
    sys.stdout.flush()
    datpath = attr.datpath
    rootfile = tools.get_rootfile(datatype, mode, label)
    if test:
        sys.stdout.write('rootfile: %s \n' %rootfile)

    pt = tools.add_rootfile(rootfile)
    selfile = get_selfile(datatype, mode, label, test=test)
    nselected, ntotal = output_trkmtm2(pt, datatype, mode, selfile, label, test)
    sys.stdout.write(' selected %s out of %s.\n' % (nselected, ntotal))
    sys.stdout.write('Saved as %s \n' %selfile)
    sys.stdout.flush()


def output_trkmtm2(pt, datatype, mode, selfile, label, test=False):
    modekey = tools.get_modekey(mode)
    sname = attr.modes[modekey]['sname'].lower()
    if sname == 'kpipi0':
        nselected, ntotal = output_trkmtm2_kpipi0(
            pt, datatype, mode, selfile, label, test)
    elif sname == 'k3pi':
        nselected, ntotal = output_trkmtm2_k3pi(
            pt, datatype, mode, selfile, label, test)
    elif sname == 'kpipi':
        nselected, ntotal = output_trkmtm2_kpipi(
            pt, datatype, mode, selfile, label, test)
    elif sname == 'kpipipi0':
        nselected, ntotal = output_trkmtm2_kpipipi0(
            pt, datatype, mode, selfile, label, test)
    elif sname == 'kspipi0':
        nselected, ntotal = output_trkmtm2_kspipi0(
            pt, datatype, mode, selfile, label, test)
    elif sname == 'ks3pi':
        nselected, ntotal = output_trkmtm2_ks3pi(
            pt, datatype, mode, selfile, label, test)
    elif sname == 'kkpi':
        nselected, ntotal = output_trkmtm2_kkpi(
            pt, datatype, mode, selfile, label, test)
    else:
        raise NameError(sname)

    return nselected, ntotal


def output_trkmtm2_kpipi0(pt, datatype, mode, selfile, label, test=False):
    nselected = 0 
    ntotal = 0 
    modekey = tools.get_modekey(mode)

    efffile = selfile.replace('.root', '.db')
    efffile = efffile.replace('/trkmtm2/', '/trkmtm/')

    tp = 'mc'
    if datatype == 'data':
        tp = 'data'
        efffile = efffile.replace('/data_', '/signal_')
    if datatype == 'generic':
        efffile = efffile.replace('/generic_', '/signal_')

    f = TFile(selfile, 'recreate')
    effs = shelve.open(efffile, flag='r')

    effskeys = {}
    for dt in [x for x in effs if isinstance(effs[x], dict)]:
        keys = effs[dt].keys()
        keys.sort()
        effskeys[dt] = keys
        
    fuller = effs['total']

    h_mbc = TH1F('h_mbc_'+tp, 'mbc', 100, 1.83, 1.89)

    kpi1 = TH1F('kpi1_'+tp, '(K^{-} #pi^{+})', 100, 0.5, 1.5)
    pipih = TH1F('pipih_'+tp, '(#pi^{+} #pi^{0})', 100, 0.2, 1.2)
    kpiz = TH1F('kpiz_'+tp, 'K^{-} #pi^{0}', 100, 0.4, 1.6)
    kpipih = TH1F('kpipih_'+tp, 'K^{-} (#pi^{+} #pi^{0})',
                        100, 0.6, 1.8)
    
    h_pk = TH1F('h_pk_'+tp, 'K^{-} momentum', 100, 0, 1.1)
    h_ppi1 = TH1F('h_ppi1_'+tp, '#pi^{+} momentum', 100, 0, 1)
    h_ppiz = TH1F('h_ppiz_'+tp, '#pi^{0} momentum', 100, 0, 1)

    h_pk_c = TH1F('h_pk_c_'+tp, 'K^{-} momentum, corrected', 100, 0, 1.1)
    h_ppi1_c = TH1F('h_ppi1_c_'+tp, '#pi^{+} momentum, corrected', 100, 0, 1)
    h_ppiz_c = TH1F('h_ppiz_c_'+tp, '#pi^{0} momentum, corrected', 100, 0, 1)
   
    h_pk_sb = TH1F('h_pk_sb_'+tp, 'K^{-} momentum', 100, 0, 1.1)
    h_ppi1_sb = TH1F('h_ppi1_sb_'+tp, '#pi^{+} momentum', 100, 0, 1)
    h_ppiz_sb = TH1F('h_ppiz_sb_'+tp, '#pi^{0} momentum', 100, 0, 1)

    h_pk_sb_c = TH1F('h_pk_sb_c_'+tp, 'K^{-} momentum, corrected', 100, 0, 1.1)
    h_ppi1_sb_c = TH1F('h_ppi1_sb_c_'+tp, '#pi^{+} momentum, corrected', 100, 0, 1)
    h_ppiz_sb_c = TH1F('h_ppiz_sb_c_'+tp, '#pi^{0} momentum, corrected', 100, 0, 1)

    h_angk = TH1F('h_angk_'+tp, 'K^{-} cos #theta', 25, -1, 1)
    h_angpi1 = TH1F('h_angpi1_'+tp, '#pi^{+} cos #theta', 25, -1, 1)
    h_angpiz = TH1F('h_angpiz_'+tp, '#pi^{0} cos #theta', 25, -1, 1)

    signal_margins = [1.86, 1.87]
    sb_margins = [1.84, 1.85]

    for pte in pt:
        ntotal += 1
        if test and nselected > 10:
            break

        for sign in (1,): # only for one 
            choice = chooseD(1, pte, sign)
            if choice != None :# and passDE(choice, pte) and pte.ecm > 3.7:
                nselected += 1
                h_mbc.Fill(pte.dmbc[choice])
##                if not 1.86 < pte.dmbc[choice] < 1.87:
                is_sideband = 0
                if signal_margins[0] < pte.dmbc[choice] < signal_margins[1]:
                    is_sideband = 0
                elif sb_margins[0] < pte.dmbc[choice] < sb_margins[1]:
                    is_sideband = 1
                else:
                    continue
                k = pte.ddau1[choice]; pip1 = pte.ddau2[choice];
                piz = pte.ddau3[choice]
                pk = (pte.trke[k], pte.trkpx[k], pte.trkpy[k],
                      pte.trkpz[k])
                ppip1 = (pte.trpie[pip1], pte.trpipx[pip1], pte.trpipy[pip1],
                         pte.trpipz[pip1])
                ppiz = (pte.pi0e[piz], pte.pi0px[piz], pte.pi0py[piz],
                        pte.pi0pz[piz])
                mag_pk = pmag(pk) ; mag_ppiz = pmag(ppiz)
                mag_ppi1 = pmag(ppip1)
                if is_sideband:
                    h_pk_sb.Fill(mag_pk)
                    h_ppiz_sb.Fill(mag_ppiz)
                    h_ppi1_sb.Fill(mag_ppi1)
                    h_ppi1_sb_c.Fill(
                        mag_ppi1, 1/getEfficiency_kpipi0(
                            mag_ppi1, 'pi1', tp, effs, effskeys))

                    
                    if getEfficiency_kpipi0(mag_pk, 'k', tp, effs, effskeys) == 0:
                        h_pk_sb_c.Fill(mag_pk, 1/0.3)
                    else:
                        h_pk_sb_c.Fill(mag_pk, 1/getEfficiency_kpipi0(
                            mag_pk, 'k', tp, effs, effskeys))
                    h_ppiz_sb_c.Fill(mag_ppiz, 1/getEfficiency_kpipi0(
                        mag_ppiz, 'piz', tp, effs, effskeys))
                else:
                    h_pk.Fill(mag_pk)
                    h_ppiz.Fill(mag_ppiz)
                    h_angk.Fill(pte.trcosth[k])
                    h_angpiz.Fill(cosangle(ppiz,(0,0,0,1)))
                    h_ppi1.Fill(mag_ppi1)
                    h_angpi1.Fill(pte.trcosth[pip1])
                    efficiency = fuller.lookup(mag_pk, mag_ppi1, mag_ppiz)

                    h_ppi1_c.Fill(mag_ppi1, 1/getEfficiency_kpipi0(
                        mag_ppi1, 'pi1', tp, effs, effskeys))
                    h_pk_c.Fill(mag_pk, 1/getEfficiency_kpipi0(
                        mag_pk, 'k', tp, effs, effskeys))
                    h_ppiz_c.Fill(mag_ppiz, 1/getEfficiency_kpipi0(
                        mag_ppiz, 'piz', tp, effs, effskeys))
                    pipi1 = invmass(ppiz, ppip1)

                    pipih.Fill(pipi1)
                    kpi1.Fill(invmass(pk, ppip1))
                    kpiz.Fill(invmass(pk, ppiz))
                    kpizsum = fourvecadd(pk, ppiz)
                    kpipih.Fill(invmass(kpizsum, ppip1))

    f.Write()
    f.Close()
    pt.Delete()

    return nselected, ntotal


def output_trkmtm2_k3pi(pt, datatype, mode, selfile, label, test=False):
    nselected = 0 
    ntotal = 0 
    modekey = tools.get_modekey(mode)
    efffile = get_efffile(selfile, datatype, test)
    tp = 'mc'
    if datatype == 'data':
        tp = 'data'

    f = TFile(selfile, 'recreate')
    effs = shelve.open(efffile, flag='r')
    effskeys = {}
    for dt in [x for x in effs if isinstance(effs[x], dict)]:
        keys = effs[dt].keys()
        keys.sort()
        effskeys[dt] = keys

    zhat = (0,1,0,0)
    fuller_p = effs['total_p']
    fuller_a = effs['total_a']
    def getEfficiency(mom, mode, type):
        correction = 1.0
        bincenters = effskeys[mode]
        upper = None
        for i in range(len(bincenters)):
            if mom < bincenters[i]:
                upper = i
                break
        if upper == None:
            rv = effs[mode][len(bincenters)-1]
        elif upper == 0:
            rv = effs[mode][0]
        else:
            rv = ((mom-bincenters[upper-1])*effs[mode][bincenters[upper]]+
                  (bincenters[upper]-mom)*effs[mode][bincenters[upper-1]])/ \
                  (bincenters[upper]-bincenters[upper-1])*correction
        if rv < 0.03:
            print 'lo', mom
            rv = 0.4
        return rv

    mbc = TH1F('mbc'+tp, 'mbc', 100, 1.83, 1.89)
    kpi1 = TH1F('kpi1'+tp, '(K^{-} #pi^{+})_{1}', 100, 0.5, 1.5)
    kpi2 = TH1F('kpi2'+tp, '(K^{-} #pi^{+})_{2}', 100, 0.5, 1.5)
    pipih = TH1F('pipih'+tp, '(#pi^{+} #pi^{-})_{high}', 100, 0.2, 1.2)
    pipil = TH1F('pipll'+tp, '(#pi^{+} #pi^{-})_{low}', 100, 0.2, 1.2)
    pipipi = TH1F('pipipi'+tp, '#pi^{+} #pi^{+} #pi^{-}', 100, 0.4, 1.6)
    kpim = TH1F('kpim'+tp, 'K^{-} #pi^{-}', 100, 0.4, 1.6)
    kpipih = TH1F('kpipih'+tp, 'K^{-} (#pi^{+} #pi^{-})_{high}',
                        100, 0.6, 1.8)
    kpipil = TH1F('kpipil'+tp, 'K^{-} (#pi^{+} #pi^{-})_{low}',
                        100, 0.6, 1.8)
    
    h_pk = TH1F('h_pk'+tp, 'K^{-} momentum', 100, 0, 1)
    h_ppi1 = TH1F('h_ppi1'+tp, '#pi^{+}_{1} momentum', 100, 0, 1)
    h_ppi2 = TH1F('h_ppi2'+tp, '#pi^{+}_{2} momentum', 100, 0, 1)
    h_ppim = TH1F('h_ppim'+tp, '#pi^{-} momentum', 100, 0, 1)

    h_pk_c = TH1F('h_pk_c'+tp, 'K^{-} momentum, corrected', 100, 0, 1)
    h_ppi1_c = TH1F('h_ppi1_c'+tp, '#pi^{+}_{1} momentum, corrected', 100, 0, 1)
    h_ppi2_c = TH1F('h_ppi2_c'+tp, '#pi^{+}_{2} momentum, corrected', 100, 0, 1)
    h_ppim_c = TH1F('h_ppim_c'+tp, '#pi^{-} momentum, corrected', 100, 0, 1)
   
    h_angk = TH1F('h_angk'+tp, 'K^{-} cos #theta', 25, -1, 1)
    h_angpi1 = TH1F('h_angpi1'+tp, '#pi^{+}_{1} cos #theta', 25, -1, 1)
    h_angpi2 = TH1F('h_angpi2'+tp, '#pi^{+}_{2} cos #theta', 25, -1, 1)
    h_angpim = TH1F('h_angpim'+tp, '#pi^{-} cos #theta', 25, -1, 1)

    eff_cut = 0.00

    for pte in pt:
        ntotal += 1
        if test and nselected > 10:
            break

        for sign in (1,):
            choice = chooseD(3, pte, sign)
            if choice != None :# and passDE(choice, pte) and pte.ecm > 3.7:
                nselected += 1
                mbc.Fill(pte.dmbc[choice])
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
                mag_pk = pmag(pk) ; mag_ppim = pmag(ppim)
                mag_ppi1 = pmag(ppip1); mag_ppi2 = pmag(ppip2)

                h_pk.Fill(mag_pk)
                h_ppim.Fill(mag_ppim)
                h_angk.Fill(pte.trcosth[k])
                h_angpim.Fill(pte.trcosth[pim])
                ang_k = abs(cosangle(pk,zhat))
                ang_pim = abs(cosangle(ppim,zhat))
                if max(mag_ppi1, mag_ppi2) == mag_ppi1:
                    h_ppi1.Fill(mag_ppi1)
                    h_angpi1.Fill(pte.trcosth[pip1])
                    h_ppi2.Fill(mag_ppi2)
                    h_angpi2.Fill(pte.trcosth[pip2])
                    ang_pi1 = abs(cosangle(ppip1,zhat));
                    ang_pi2 = abs(cosangle(ppip2,zhat))
                    efficiency_p = fuller_p.lookup(mag_pk, mag_ppi1, mag_ppi2,
                                                   mag_ppim)
                    efficiency = fuller_a.lookup(ang_k, ang_pi1, ang_pi2,
                                               ang_pim)
                    h_ppi1_c.Fill(mag_ppi1, 1/getEfficiency(mag_ppi1, 'pi1', type))
                    h_ppi2_c.Fill(mag_ppi2, 1/getEfficiency(mag_ppi2, 'pi2', type))
                    if efficiency > eff_cut:
                        pass

                else:
                    h_ppi1.Fill(mag_ppi2)
                    h_angpi1.Fill(pte.trcosth[pip2])
                    h_ppi2.Fill(mag_ppi1)
                    h_angpi2.Fill(pte.trcosth[pip1])
                    ang_pi1 = abs(cosangle(ppip2,zhat));
                    ang_pi2 = abs(cosangle(ppip1,zhat))
                    efficiency_p = fuller_p.lookup(mag_pk, mag_ppi2, mag_ppi1,
                                                   mag_ppim)
                    efficiency = fuller_a.lookup(ang_k, ang_pi1, ang_pi2,
                                               ang_pim)
                    h_ppi1_c.Fill(mag_ppi1, 1/getEfficiency(mag_ppi2, 'pi1', type))
                    h_ppi2_c.Fill(mag_ppi2, 1/getEfficiency(mag_ppi1, 'pi2', type))
                    if efficiency > eff_cut:
                        pass

                h_pk_c.Fill(mag_pk, 1/getEfficiency(mag_pk, 'k', type))
                h_ppim_c.Fill(mag_ppim, 1/getEfficiency(mag_ppim, 'pim', type))

                pipi1 = invmass(ppim, ppip1); pipi2 = invmass(ppim, ppip2)
                maxpipi = max(pipi1, pipi2);
                if maxpipi == pipi1:
                    pipih.Fill(pipi1)
                    pipil.Fill(pipi2)
                    kpi1.Fill(invmass(pk, ppip2))
                    kpi2.Fill(invmass(pk, ppip1))
                    pipipi.Fill(invmass(ppim, fourvecadd(ppip1, ppip2)))
                    kpim.Fill(invmass(pk, ppim))
                    kpimsum = fourvecadd(pk, ppim)
                    kpipih.Fill(invmass(kpimsum, ppip1))
                    kpipil.Fill(invmass(kpimsum, ppip2))
                else:
                    pipih.Fill(pipi2)
                    pipil.Fill(pipi1)
                    kpi1.Fill(invmass(pk, ppip1))
                    kpi2.Fill(invmass(pk, ppip2))
                    pipipi.Fill(invmass(ppim, fourvecadd(ppip1, ppip2)))
                    kpim.Fill(invmass(pk, ppim))
                    kpimsum = fourvecadd(pk, ppim)
                    kpipih.Fill(invmass(kpimsum, ppip2))
                    kpipil.Fill(invmass(kpimsum, ppip1))


    f.Write()
    f.Close()
    pt.Delete()

    return nselected, ntotal


def create_script_logfile_jobname(opts, datatype, tag, mode, label):
    logname = '%s_%s.log' %(datatype, mode)
    logpath = os.path.join(attr.sellogpath, label, 'trkmtm2')
    logfile = tools.set_file(extbase=logpath, comname=logname)

    content =  '''#!/usr/bin/env python

from sel import trkmtm2

trkmtm2.single_tag_mode("%s", "%s", "%s", test=%s)

'''% (datatype, mode, label, opts.test)

    mode, sign = tools.get_modekey_sign(mode)

    if tag == 'single':
        if sign == [-1, 1]:
            filename = 'sel-%s-%s-m%s-%s.py' % (
                datatype, tag, mode, label)
            qjobname = 'sel%s' % mode
        else:
            if sign == 1:
                sign = 'p'
            else: 
                sign = 'm'
            filename = 'sel-%s-%s-m%s-%s-%s.py' % (
                datatype, tag, mode, sign, label)
            qjobname = 'sel%s,%s' % (mode, sign)
    else:
        filename = 'sel-%s-%s-m%s-%s-%s.py' % (
            datatype, tag, mode[0], mode[1], label)
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
        
    selpath = os.path.join(attr.datpath, 'sel', label, 'trkmtm2')
    selfile = tools.check_and_join(selpath, selname)
    return selfile


def getEfficiency_kpipi0(mom, mode, type, effs, effskeys):
##    if type == 'data':
    if False:
        correction = 1.01
        if mom < 0.1:
            correction = 1.046
        elif 0.1 < mom < 0.13:
            correction = 1.018
        elif 0.13 < mom < 0.16:
            correction = 1.017
        elif 0.16 < mom < 0.3:
            correction = 1.013
    else:
        correction = 1.0
    bincenters = effskeys[mode]
    upper = None
    for i in range(len(bincenters)):
        if mom < bincenters[i]:
            upper = i
            break
    if upper == None:
        if len(bincenters)-1 not in effs[mode]:
            rv = 0.3
        else:
            rv = effs[mode][len(bincenters)-1]
    elif upper == 0:
        rv = 0.3
    else:
        rv = ((mom-bincenters[upper-1])*effs[mode][bincenters[upper]]+
                (bincenters[upper]-mom)*effs[mode][bincenters[upper-1]])/ \
                (bincenters[upper]-bincenters[upper-1])*correction
    if rv < 0.03:
        rv = 0.3
    return rv


def get_efffile(selfile, datatype, test=False):
    efffile = selfile.replace('.root', '.db')
    efffile = efffile.replace('/trkmtm2/', '/trkmtm/')
    if datatype == 'data':
        efffile = efffile.replace('/data_', '/signal_')
    if datatype == 'generic':
        efffile = efffile.replace('/generic_', '/signal_')

    if test:
        efffile_src = efffile.replace('.test', '')
        shutil.copy(efffile_src, efffile)

    return efffile


def output_trkmtm2_kpipi(pt, datatype, mode, selfile, label, test=False):
    nselected = 0 
    ntotal = 0 
    modekey = tools.get_modekey(mode)
    efffile = get_efffile(selfile, datatype, test)
    tp = 'mc'
    if datatype == 'data':
        tp = 'data'

    f = TFile(selfile, 'recreate')
    effs = shelve.open(efffile, flag='r')
    effskeys = {}
    for dt in [x for x in effs if isinstance(effs[x], dict)]:
        keys = effs[dt].keys()
        keys.sort()
        effskeys[dt] = keys

    def getEfficiency(mom, mode, type):
        correction = 1.0
        bincenters = effskeys[mode]
        upper = None
        for i in range(len(bincenters)):
            if mom < bincenters[i]:
                upper = i
                break
        if upper == None:
            if len(bincenters)-1 not in effs[mode]:
                rv = 0.5
            else:
                rv = effs[mode][len(bincenters)-1]
        elif upper == 0:
            rv = effs[mode][0]
        else:
            rv = ((mom-bincenters[upper-1])*effs[mode][bincenters[upper]]+
                  (bincenters[upper]-mom)*effs[mode][bincenters[upper-1]])/ \
                  (bincenters[upper]-bincenters[upper-1])*correction
        if rv < 0.03:
            print 'lo', mom
            rv = 0.5
        return rv

    zhat = (0,1,0,0)

    fuller_p = effs['total_p']
    fuller_a = effs['total_a']

    mbc = TH1F('mbc'+tp, 'mbc', 100, 1.83, 1.89)
    kpi1 = TH1F('kpi1'+tp, '(K^{-} #pi^{+})_{1}', 100, 0.5, 1.5)
    kpi2 = TH1F('kpi2'+tp, '(K^{-} #pi^{+})_{2}', 100, 0.5, 1.5)
    pipih = TH1F('pipih'+tp, '(#pi^{+} #pi^{-})_{high}', 100, 0.2, 1.2)
    pipil = TH1F('pipll'+tp, '(#pi^{+} #pi^{-})_{low}', 100, 0.2, 1.2)
    pipipi = TH1F('pipipi'+tp, '#pi^{+} #pi^{+} #pi^{-}', 100, 0.4, 1.6)
    kpim = TH1F('kpim'+tp, 'K^{-} #pi^{-}', 100, 0.4, 1.6)
    kpipih = TH1F('kpipih'+tp, 'K^{-} (#pi^{+} #pi^{-})_{high}',
                        100, 0.6, 1.8)
    kpipil = TH1F('kpipil'+tp, 'K^{-} (#pi^{+} #pi^{-})_{low}',
                        100, 0.6, 1.8)
    
    h_pk = TH1F('h_pk'+tp, 'K^{-} momentum', 100, 0, 1)
    h_ppi1 = TH1F('h_ppi1'+tp, '#pi^{+}_{1} momentum', 100, 0, 1)
    h_ppi2 = TH1F('h_ppi2'+tp, '#pi^{+}_{2} momentum', 100, 0, 1)
    h_ppim = TH1F('h_ppim'+tp, '#pi^{-} momentum', 100, 0, 1)

    h_pk_c = TH1F('h_pk_c'+tp, 'K^{-} momentum, corrected', 100, 0, 1)
    h_ppi1_c = TH1F('h_ppi1_c'+tp, '#pi^{+}_{1} momentum, corrected', 100, 0, 1)
    h_ppi2_c = TH1F('h_ppi2_c'+tp, '#pi^{+}_{2} momentum, corrected', 100, 0, 1)
    h_ppim_c = TH1F('h_ppim_c'+tp, '#pi^{-} momentum, corrected', 100, 0, 1)
   
    h_angk = TH1F('h_angk'+tp, 'K^{-} cos #theta', 25, -1, 1)
    h_angpi1 = TH1F('h_angpi1'+tp, '#pi^{+}_{1} cos #theta', 25, -1, 1)
    h_angpi2 = TH1F('h_angpi2'+tp, '#pi^{+}_{2} cos #theta', 25, -1, 1)
    h_angpim = TH1F('h_angpim'+tp, '#pi^{-} cos #theta', 25, -1, 1)

    eff_cut = 0.00

    for pte in pt:
        ntotal += 1
        if test and nselected > 10:
            break

        for sign in (1,):
            choice = chooseD(200, pte, sign)
            if choice != None :# and passDE(choice, pte) and pte.ecm > 3.7:
                mbc.Fill(pte.dmbc[choice])
                if not 1.865 < pte.dmbc[choice] < 1.875:
                    continue
                nselected += 1
                
                k = pte.ddau1[choice]; pip1 = pte.ddau2[choice];
                pip2 = pte.ddau3[choice]
                pk = (pte.trke[k], pte.trkpx[k], pte.trkpy[k],
                      pte.trkpz[k])
                ppip1 = (pte.trpie[pip1], pte.trpipx[pip1], pte.trpipy[pip1],
                         pte.trpipz[pip1])
                ppip2 = (pte.trpie[pip2], pte.trpipx[pip2], pte.trpipy[pip2],
                         pte.trpipz[pip2])
                mag_pk = pmag(pk)
                mag_ppi1 = pmag(ppip1); mag_ppi2 = pmag(ppip2)

                h_pk.Fill(mag_pk)
                h_angk.Fill(pte.trcosth[k])
                ang_k = abs(cosangle(pk,zhat))
                if max(mag_ppi1, mag_ppi2) == mag_ppi1:
                    h_ppi1.Fill(mag_ppi1)
                    h_angpi1.Fill(pte.trcosth[pip1])
                    h_ppi2.Fill(mag_ppi2)
                    h_angpi2.Fill(pte.trcosth[pip2])
                    ang_pi1 = abs(cosangle(ppip1,zhat));
                    ang_pi2 = abs(cosangle(ppip2,zhat))
                    efficiency_p = fuller_p.lookup(mag_pk, mag_ppi1, mag_ppi2)
                    efficiency = fuller_a.lookup(ang_k, ang_pi1, ang_pi2)
                    if getEfficiency(mag_ppi1, 'pi1', type) == 0:
                        h_ppi1_c.Fill(mag_ppi1, 1/0.5)
                    else:
                        h_ppi1_c.Fill(mag_ppi1, 1/getEfficiency(mag_ppi1, 'pi1', type))
                    h_ppi2_c.Fill(mag_ppi2, 1/getEfficiency(mag_ppi2, 'pi2', type))
                    if efficiency > eff_cut:
                        pass
                else:
                    h_ppi1.Fill(mag_ppi2)
                    h_angpi1.Fill(pte.trcosth[pip2])
                    h_ppi2.Fill(mag_ppi1)
                    h_angpi2.Fill(pte.trcosth[pip1])
                    ang_pi1 = abs(cosangle(ppip2,zhat));
                    ang_pi2 = abs(cosangle(ppip1,zhat))
                    efficiency_p = fuller_p.lookup(mag_pk, mag_ppi2, mag_ppi1)
                    efficiency = fuller_a.lookup(ang_k, ang_pi1, ang_pi2)
                    if getEfficiency(mag_ppi2, 'pi1', type) == 0:
                        h_ppi1_c.Fill(mag_ppi2, 1/0.5)
                    else:
                        h_ppi1_c.Fill(mag_ppi2, 1/getEfficiency(mag_ppi2, 'pi1', type))             
                    h_ppi2_c.Fill(mag_ppi1, 1/getEfficiency(mag_ppi1, 'pi2', type))
                    if efficiency > eff_cut:
                        pass

                h_pk_c.Fill(mag_pk, 1/getEfficiency(mag_pk, 'k', type))

    f.Write()
    f.Close()
    pt.Delete()

    return nselected, ntotal


    
def output_trkmtm2_kpipipi0(pt, datatype, mode, selfile, label, test=False):
    nselected = 0 
    ntotal = 0 
    modekey = tools.get_modekey(mode)
    efffile = get_efffile(selfile, datatype, test)
    tp = 'mc'
    if datatype == 'data':
        tp = 'data'

    f = TFile(selfile, 'recreate')
    effs = shelve.open(efffile, flag='r')
    effskeys = {}
    for dt in [x for x in effs if isinstance(effs[x], dict)]:
        keys = effs[dt].keys()
        keys.sort()
        effskeys[dt] = keys

    zhat = (0,1,0,0)
    
    fuller_p = effs['total_p']
    fuller_a = effs['total_a']

    def getEfficiency(mom, mode, type):
        correction = 1.0
        bincenters = effskeys[mode]
        upper = None
        for i in range(len(bincenters)):
            if mom < bincenters[i]:
                upper = i
                break
        if upper == None:
            rv = effs[mode][len(bincenters)-1]
        elif upper == 0:
            rv = 1e6
        else:
            rv = ((mom-bincenters[upper-1])*effs[mode][bincenters[upper]]+
                  (bincenters[upper]-mom)*effs[mode][bincenters[upper-1]])/ \
                  (bincenters[upper]-bincenters[upper-1])*correction
        if rv < 0.03:
            print 'lo', mom
            rv = 0.25
        return rv

    mbc = TH1F('mbc'+tp, 'mbc', 100, 1.83, 1.89)
    kpi1 = TH1F('kpi1'+tp, '(K^{-} #pi^{+})_{1}', 100, 0.5, 1.5)
    kpi2 = TH1F('kpi2'+tp, '(K^{-} #pi^{+})_{2}', 100, 0.5, 1.5)
    pipih = TH1F('pipih'+tp, '(#pi^{+} #pi^{-})_{high}', 100, 0.2, 1.2)
    pipil = TH1F('pipll'+tp, '(#pi^{+} #pi^{-})_{low}', 100, 0.2, 1.2)
    pipipi = TH1F('pipipi'+tp, '#pi^{+} #pi^{+} #pi^{-}', 100, 0.4, 1.6)
    kpiz = TH1F('kpiz'+tp, 'K^{-} #pi^{-}', 100, 0.4, 1.6)
    kpipih = TH1F('kpipih'+tp, 'K^{-} (#pi^{+} #pi^{-})_{high}',
                        100, 0.6, 1.8)
    kpipil = TH1F('kpipil'+tp, 'K^{-} (#pi^{+} #pi^{-})_{low}',
                        100, 0.6, 1.8)

    h_pk = TH1F('h_pk'+tp, 'K^{-} momentum', 50, 0, 1)
    h_ppi1 = TH1F('h_ppi1'+tp, '#pi^{+}_{1} momentum', 50, 0, 1)
    h_ppi2 = TH1F('h_ppi2'+tp, '#pi^{+}_{2} momentum', 50, 0, 1)
    h_ppiz = TH1F('h_ppiz'+tp, '#pi^{-} momentum', 50, 0, 1)

    h_pk_c = TH1F('h_pk_c'+tp, 'K^{-} momentum, corrected', 50, 0, 1)
    h_ppi1_c = TH1F('h_ppi1_c'+tp, '#pi^{+}_{1} momentum, corrected', 50, 0, 1)
    h_ppi2_c = TH1F('h_ppi2_c'+tp, '#pi^{+}_{2} momentum, corrected', 50, 0, 1)
    h_ppiz_c = TH1F('h_ppiz_c'+tp, '#pi^{-} momentum, corrected', 50, 0, 1)
   
    h_angk = TH1F('h_angk'+tp, 'K^{-} cos #theta', 25, -1, 1)
    h_angpi1 = TH1F('h_angpi1'+tp, '#pi^{+}_{1} cos #theta', 25, -1, 1)
    h_angpi2 = TH1F('h_angpi2'+tp, '#pi^{+}_{2} cos #theta', 25, -1, 1)
    h_angpiz = TH1F('h_angpiz'+tp, '#pi^{-} cos #theta', 25, -1, 1)
    corrections = TH2F('corrections'+tp,
                             'K_{S} momentum 1/correction',
                             100, 0, 1, 100, 0, 1)

    eff_cut = 0.00

    for pte in pt:
        ntotal += 1
        if test and nselected > 10:
            break

        for sign in (1,):
            choice = chooseD(201, pte, sign)
            if choice != None :# and passDE(choice, pte) and pte.ecm > 3.7:
                mbc.Fill(pte.dmbc[choice])
                if not 1.865 < pte.dmbc[choice] < 1.87:
                    continue
                nselected += 1
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
                mag_pk = pmag(pk) ; mag_ppiz = pmag(ppiz)
                mag_ppi1 = pmag(ppip1); mag_ppi2 = pmag(ppip2)
                h_pk.Fill(mag_pk)
                h_ppiz.Fill(mag_ppiz)
                ang_k = abs(cosangle(pk,zhat))
                ang_piz = abs(cosangle(ppiz,zhat))
                h_angk.Fill(ang_k)
                h_angpiz.Fill(ang_piz)
                if max(mag_ppi1, mag_ppi2) == mag_ppi1:
                    h_ppi1.Fill(mag_ppi1)
                    h_angpi1.Fill(pte.trcosth[pip1])
                    h_ppi2.Fill(mag_ppi2)
                    h_angpi2.Fill(pte.trcosth[pip2])
                    ang_pi1 = abs(cosangle(ppip1,zhat));
                    ang_pi2 = abs(cosangle(ppip2,zhat))
                    efficiency_p = fuller_p.lookup(mag_pk, mag_ppi1, mag_ppi2,
                                                   mag_ppiz)
                    efficiency = efficiency_p
                    h_ppi1_c.Fill(mag_ppi1, 1/getEfficiency(mag_ppi1, 'pi1', type))
                    h_ppi2_c.Fill(mag_ppi2, 1/getEfficiency(mag_ppi2, 'pi2', type))
                    corrections.Fill(mag_ppi1, getEfficiency(mag_ppi1, 'pi1', type))
                    if efficiency >= eff_cut:
                        pass
                    else:
                        print efficiency
                else:
                    h_ppi1.Fill(mag_ppi2)
                    h_angpi1.Fill(pte.trcosth[pip2])
                    h_ppi2.Fill(mag_ppi1)
                    h_angpi2.Fill(pte.trcosth[pip1])
                    ang_pi1 = abs(cosangle(ppip2,zhat));
                    ang_pi2 = abs(cosangle(ppip1,zhat))
                    efficiency_p = fuller_p.lookup(mag_pk, mag_ppi2, mag_ppi1,
                                                   mag_ppiz)
                    efficiency_a = fuller_a.lookup(ang_k, ang_pi1, ang_pi2,
                                               ang_piz)
                    efficiency = efficiency_p
                    h_ppi1_c.Fill(mag_ppi2, 1/getEfficiency(mag_ppi2, 'pi1', type))
                    h_ppi2_c.Fill(mag_ppi1, 1/getEfficiency(mag_ppi1, 'pi2', type))
                    if efficiency > eff_cut:
                        pass
                h_pk_c.Fill(mag_pk, 1/getEfficiency(mag_pk, 'k', type))
                h_ppiz_c.Fill(mag_ppiz, 1/getEfficiency(mag_ppiz, 'piz', type))

                pipi1 = invmass(ppiz, ppip1); pipi2 = invmass(ppiz, ppip2)
                maxpipi = max(pipi1, pipi2);
                if maxpipi == pipi1:
                    pipih.Fill(pipi1)
                    pipil.Fill(pipi2)
                    kpi1.Fill(invmass(pk, ppip2))
                    kpi2.Fill(invmass(pk, ppip1))
                    pipipi.Fill(invmass(ppiz, fourvecadd(ppip1, ppip2)))
                    kpiz.Fill(invmass(pk, ppiz))
                    kpizsum = fourvecadd(pk, ppiz)
                    kpipih.Fill(invmass(kpizsum, ppip1))
                    kpipil.Fill(invmass(kpizsum, ppip2))
                else:
                    pipih.Fill(pipi2)
                    pipil.Fill(pipi1)
                    kpi1.Fill(invmass(pk, ppip1))
                    kpi2.Fill(invmass(pk, ppip2))
                    pipipi.Fill(invmass(ppiz, fourvecadd(ppip1, ppip2)))
                    kpiz.Fill(invmass(pk, ppiz))
                    kpizsum = fourvecadd(pk, ppiz)
                    kpipih.Fill(invmass(kpizsum, ppip2))
                    kpipil.Fill(invmass(kpizsum, ppip1))

    f.Write()
    f.Close()
    pt.Delete()

    return nselected, ntotal

                
 
def output_trkmtm2_kspipi0(pt, datatype, mode, selfile, label, test=False):
    nselected = 0 
    ntotal = 0 
    modekey = tools.get_modekey(mode)
    efffile = get_efffile(selfile, datatype, test)
    tp = 'mc'
    if datatype == 'data':
        tp = 'data'

    f = TFile(selfile, 'recreate')
    effs = shelve.open(efffile, flag='r')
    effskeys = {}
    for dt in [x for x in effs if isinstance(effs[x], dict)]:
        keys = effs[dt].keys()
        keys.sort()
        effskeys[dt] = keys

    fuller = effs['total']

    def getEfficiency(mom, mode, type):
        correction = 1.0
        bincenters = effskeys[mode]
        upper = None
        for i in range(len(bincenters)):
            if mom < bincenters[i]:
                upper = i
                break
        if upper == None:
            if len(bincenters)-1 not in effs[mode]:
                rv = 0.3
            else:
                rv = effs[mode][len(bincenters)-1]
        elif upper == 0:
            rv = 0.3
        else:
            rv = ((mom-bincenters[upper-1])*effs[mode][bincenters[upper]]+
                  (bincenters[upper]-mom)*effs[mode][bincenters[upper-1]])/ \
                  (bincenters[upper]-bincenters[upper-1])*correction
        if rv < 0.03:
            print 'lo', mom
            rv = 0.3
        return rv


    h_mbc = TH1F('h_mbc'+tp, 'mbc', 100, 1.83, 1.89)
    kpi1 = TH1F('kpi1'+tp, '(K_{S} #pi^{+})', 200, 0., 3)
    pipih = TH1F('pipih'+tp, '(#pi^{+} #pi^{0})', 200, 0., 3)
    kpiz = TH1F('kpiz'+tp, 'K_{S} #pi^{0}', 200, 0., 3)
    kpipih = TH1F('kpipih'+tp, 'K^{-} (#pi^{+} #pi^{0})',
                        100, 0.6, 1.8)
    
    h_pks = TH1F('h_pks'+tp, 'K_{S} momentum', 100, 0, 1.1)
    h_ppi1 = TH1F('h_ppi1'+tp, '#pi^{+} momentum', 100, 0, 1)
    h_ppiz = TH1F('h_ppiz'+tp, '#pi^{0} momentum', 100, 0, 1)

    h_pks_c = TH1F('h_pks_c'+tp, 'K_{S} momentum, corrected', 100, 0, 1.1)
    h_ppi1_c = TH1F('h_ppi1_c'+tp, '#pi^{+} momentum, corrected', 100, 0, 1)
    h_ppiz_c = TH1F('h_ppiz_c'+tp, '#pi^{0} momentum, corrected', 100, 0, 1)
   
    h_pks_sb = TH1F('h_pks_sb'+tp, 'K_{S} momentum, sideband', 100, 0, 1.1)
    h_ppi1_sb = TH1F('h_ppi1_sb'+tp, '#pi^{+} momentum, sideband', 100, 0, 1)
    h_ppiz_sb = TH1F('h_ppiz_sb'+tp, '#pi^{0} momentum, sideband', 100, 0, 1)

    h_pks_sb_c = TH1F('h_pks_sb_c'+tp, 'K_{S} momentum, sideband, corrected', 100, 0, 1.1)
    h_ppi1_sb_c = TH1F('h_ppi1_sb_c'+tp, '#pi^{+} momentum, sideband, corrected', 100, 0, 1)
    h_ppiz_sb_c = TH1F('h_ppiz_sb_c'+tp, '#pi^{0} momentum, sideband, corrected', 100, 0, 1)

    h_angks = TH1F('h_angk'+tp, 'K_{S} cos #theta', 25, -1, 1)
    h_angpi1 = TH1F('h_angpi1'+tp, '#pi^{+} cos #theta', 25, -1, 1)
    h_angpiz = TH1F('h_angpiz'+tp, '#pi^{0} cos #theta', 25, -1, 1)

    h_dalitz = TH2F('h_dalitz'+tp, 'Dalitz for '+tp,
                          100, 0, 2, 100, 0, 3)

    signal_margins = [1.865, 1.875]
    sb_margins = [1.845, 1.855]

    for pte in pt:
        ntotal += 1
        if test and nselected > 10:
            break

        for sign in (1,):
            choice = chooseD(203, pte, sign)
            if choice != None :# and passDE(choice, pte) and pte.ecm > 3.7:
                h_mbc.Fill(pte.dmbc[choice])
                if not 1.865 < pte.dmbc[choice] < 1.87:
                    continue
                nselected += 1
                is_sideband = 0
                if signal_margins[0] < pte.dmbc[choice] < signal_margins[1]:
                    is_sideband = 0
                elif sb_margins[0] < pte.dmbc[choice] < sb_margins[1]:
                    is_sideband = 1
                else:
                    continue
                ks = pte.ddau1[choice]; pip1 = pte.ddau2[choice];
                piz = pte.ddau3[choice]
                pks = (pte.kse[ks], pte.kspx[ks], pte.kspy[ks],
                      pte.kspz[ks])
                ppip1 = (pte.trpie[pip1], pte.trpipx[pip1], pte.trpipy[pip1],
                         pte.trpipz[pip1])
                ppiz = (pte.pi0e[piz], pte.pi0px[piz], pte.pi0py[piz],
                        pte.pi0pz[piz])
                mag_pks = pmag(pks) ; mag_ppiz = pmag(ppiz)
                mag_ppi1 = pmag(ppip1)
                if is_sideband:
                    h_pks_sb.Fill(mag_pks)
                    h_ppiz_sb.Fill(mag_ppiz)
                    h_ppi1_sb.Fill(mag_ppi1)
                    h_ppi1_sb_c.Fill(mag_ppi1, 1/getEfficiency(mag_ppi1, 'pi1', type))
                    if getEfficiency(mag_pks, 'ks', type) == 0:
                        h_pks_sb_c.Fill(mag_pks, 1/0.3)
                    else:
                        h_pks_sb_c.Fill(mag_pks, 1/getEfficiency(mag_pks, 'ks', type))
                    h_ppiz_sb_c.Fill(mag_ppiz, 1/getEfficiency(mag_ppiz, 'piz', type))
                else:
                    h_dalitz.Fill(invmasssq(ppiz, ppip1),
                                        invmasssq(pks, ppiz))
                    h_pks.Fill(mag_pks)
                    h_ppiz.Fill(mag_ppiz)
                    try: 
                        h_angks.Fill(pte.trcosth[ks])
                    except IndexError:
                        pass
                    
                    h_angpiz.Fill(cosangle(ppiz,(0,0,0,1)))
                    h_ppi1.Fill(mag_ppi1)
                    h_angpi1.Fill(pte.trcosth[pip1])
                    efficiency = fuller.lookup(mag_pks, mag_ppi1, mag_ppiz)
                    h_ppi1_c.Fill(mag_ppi1, 1/getEfficiency(mag_ppi1, 'pi1', type))
                    h_pks_c.Fill(mag_pks, 1/getEfficiency(mag_pks, 'ks', type))
                    h_ppiz_c.Fill(mag_ppiz, 1/getEfficiency(mag_ppiz, 'piz', type))
                    pipi1 = invmass(ppiz, ppip1)
                    pipih.Fill(pipi1**2)
                    kpi1.Fill(invmasssq(pks, ppip1))
                    kpiz.Fill(invmasssq(pks, ppiz))
                    kpizsum = fourvecadd(pks, ppiz)
                    kpipih.Fill(invmass(kpizsum, ppip1))

    f.Write()
    f.Close()
    pt.Delete()

    return nselected, ntotal


def output_trkmtm2_ks3pi(pt, datatype, mode, selfile, label, test=False):
    nselected = 0 
    ntotal = 0 
    modekey = tools.get_modekey(mode)
    efffile = get_efffile(selfile, datatype, test)
    tp = 'mc'
    if datatype == 'data':
        tp = 'data'

    f = TFile(selfile, 'recreate')
    effs = shelve.open(efffile, flag='r')
    effskeys = {}
    for dt in [x for x in effs if isinstance(effs[x], dict)]:
        keys = effs[dt].keys()
        keys.sort()
        effskeys[dt] = keys

    zhat = (0,1,0,0)

    fuller_p = effs['total_p']
    fuller_a = effs['total_a']

    def getEfficiency(mom, mode, type):
        correction = 1.0
        bincenters = effskeys[mode]
        upper = None
        for i in range(len(bincenters)):
            if mom < bincenters[i]:
                upper = i
                break
        if upper == None:
            if len(bincenters)-1 not in effs[mode]:
                rv = 0.2
            else:
                if effs[mode][len(bincenters)-1] == 0:
                    rv = 0.2
                else:
                    rv = effs[mode][len(bincenters)-1]
        elif upper == 0:
            rv = 0.2
        else:
            rv = ((mom-bincenters[upper-1])*effs[mode][bincenters[upper]]+
                  (bincenters[upper]-mom)*effs[mode][bincenters[upper-1]])/ \
                  (bincenters[upper]-bincenters[upper-1])*correction
        if rv < 0.03:
            print 'lo', mom
            rv = 0.2
        return rv

    mbc = TH1F('mbc'+tp, 'mbc', 100, 1.83, 1.89)
    kpi1 = TH1F('kpi1'+tp, '(K^{-} #pi^{+})_{1}', 100, 0.5, 1.5)
    kpi2 = TH1F('kpi2'+tp, '(K^{-} #pi^{+})_{2}', 100, 0.5, 1.5)
    pipih = TH1F('pipih'+tp, '(#pi^{+} #pi^{-})_{high}', 100, 0.2, 1.2)
    pipil = TH1F('pipll'+tp, '(#pi^{+} #pi^{-})_{low}', 100, 0.2, 1.2)
    pipipi = TH1F('pipipi'+tp, '#pi^{+} #pi^{+} #pi^{-}', 100, 0.4, 1.6)
    kpim = TH1F('kpim'+tp, 'K^{-} #pi^{-}', 100, 0.4, 1.6)
    kpipih = TH1F('kpipih'+tp, 'K^{-} (#pi^{+} #pi^{-})_{high}',
                        100, 0.6, 1.8)
    kpipil = TH1F('kpipil'+tp, 'K^{-} (#pi^{+} #pi^{-})_{low}',
                        100, 0.6, 1.8)
    h_ppii = TH1F('ppi2'+tp, 'Index 2 momentum', 100, 0.0, 1)

    h_pks = TH1F('h_pks'+tp, 'K_{S} momentum', 50, 0, 1)
    h_ppi1 = TH1F('h_ppi1'+tp, '#pi^{+}_{1} momentum', 50, 0, 1)
    h_ppi2 = TH1F('h_ppi2'+tp, '#pi^{+}_{2} momentum', 50, 0, 1)
    h_ppim = TH1F('h_ppim'+tp, '#pi^{-} momentum', 50, 0, 1)

    h_pks_c = TH1F('h_pk_c'+tp, 'K_{S} momentum, corrected', 50, 0, 1)
    h_ppi1_c = TH1F('h_ppi1_c'+tp, '#pi^{+}_{1} momentum, corrected', 50, 0, 1)
    h_ppi2_c = TH1F('h_ppi2_c'+tp, '#pi^{+}_{2} momentum, corrected', 50, 0, 1)
    h_ppim_c = TH1F('h_ppim_c'+tp, '#pi^{-} momentum, corrected', 50, 0, 1)
    h_ppi1_c2 = TH1F('h_ppi1_c2'+tp, '#pi^{+}_{1} momentum, corrected in loop', 50, 0, 1)
   
    h_angks = TH1F('h_angks'+tp, 'K_{S} cos #theta', 25, -1, 1)
    h_angpi1 = TH1F('h_angpi1'+tp, '#pi^{+}_{1} cos #theta', 25, -1, 1)
    h_angpi2 = TH1F('h_angpi2'+tp, '#pi^{+}_{2} cos #theta', 25, -1, 1)
    h_angpim = TH1F('h_angpim'+tp, '#pi^{-} cos #theta', 25, -1, 1)
    corrections = TH2F('corrections'+tp,
                             'K_{S} momentum 1/correction',
                             100, 0, 1, 100, 0, 1)
    eff_cut = 0.00
    for pte in pt:
        ntotal += 1
        if test and nselected > 10:
            break

        for sign in (1,):
            choice = chooseD(204, pte, sign)
            if choice != None :# and passDE(choice, pte) and pte.ecm > 3.7:
                mbc.Fill(pte.dmbc[choice])
                if not 1.865 < pte.dmbc[choice] < 1.875:
                    continue
                nselected += 1
                ks = pte.ddau1[choice]; pip1 = pte.ddau2[choice];
                pip2 = pte.ddau3[choice]; pim = pte.ddau4[choice]
                pks = (pte.kse[ks], pte.kspx[ks], pte.kspy[ks],
                      pte.kspz[ks])
                ppip1 = (pte.trpie[pip1], pte.trpipx[pip1], pte.trpipy[pip1],
                         pte.trpipz[pip1])
                h_ppii.Fill(pmag(ppip1))
                ppip2 = (pte.trpie[pip2], pte.trpipx[pip2], pte.trpipy[pip2],
                         pte.trpipz[pip2])
                ppim = (pte.trpie[pim], pte.trpipx[pim], pte.trpipy[pim],
                        pte.trpipz[pim])
                mag_pks = pmag(pks) ; mag_ppim = pmag(ppim)
                mag_ppi1 = pmag(ppip1); mag_ppi2 = pmag(ppip2)
                h_pks.Fill(mag_pks)
                h_ppim.Fill(mag_ppim)
                ang_ks = abs(cosangle(pks,zhat))
                ang_pim = abs(cosangle(ppim,zhat))
                h_angks.Fill(ang_ks)
                h_angpim.Fill(ang_pim)
                if max(mag_ppi1, mag_ppi2) == mag_ppi1:
                    h_ppi1.Fill(mag_ppi1)
                    h_angpi1.Fill(pte.trcosth[pip1])
                    h_ppi2.Fill(mag_ppi2)
                    h_angpi2.Fill(pte.trcosth[pip2])
                    ang_pi1 = abs(cosangle(ppip1,zhat));
                    ang_pi2 = abs(cosangle(ppip2,zhat))
                    efficiency_p = fuller_p.lookup(mag_pks, mag_ppi1, mag_ppi2,
                                                   mag_ppim)
                    efficiency = efficiency_p
                    h_ppi1_c.Fill(mag_ppi1, 1/getEfficiency(mag_ppi1, 'pi1', type))
                    h_ppi2_c.Fill(mag_ppi2, 1/getEfficiency(mag_ppi2, 'pi2', type))
                    if efficiency >= eff_cut:
                        pass
                
                    else:
                        print efficiency
                else:
                    h_ppi1.Fill(mag_ppi2)
                    h_angpi1.Fill(pte.trcosth[pip2])
                    h_ppi2.Fill(mag_ppi1)
                    h_angpi2.Fill(pte.trcosth[pip1])
                    ang_pi1 = abs(cosangle(ppip2,zhat));
                    ang_pi2 = abs(cosangle(ppip1,zhat))
                    efficiency_p = fuller_p.lookup(mag_pks, mag_ppi2, mag_ppi1,
                                                   mag_ppim)
                    efficiency_a = fuller_a.lookup(ang_ks, ang_pi1, ang_pi2,
                                               ang_pim)
                    efficiency = efficiency_p
                    h_ppi1_c.Fill(mag_ppi2, 1/getEfficiency(mag_ppi2, 'pi1', type))
                    if getEfficiency(mag_ppi1, 'pi2', type) > 0:
                        h_ppi2_c.Fill(mag_ppi1, 1/getEfficiency(mag_ppi1, 'pi2', type))
                        
                    if efficiency > eff_cut:
                        pass
                h_pks_c.Fill(mag_pks, 1/getEfficiency(mag_pks, 'ks', type))
                h_ppim_c.Fill(mag_ppim, 1/getEfficiency(mag_ppim, 'pim', type))
                pipi1 = invmass(ppim, ppip1); pipi2 = invmass(ppim, ppip2)
                maxpipi = max(pipi1, pipi2);
                if maxpipi == pipi1:
                    pipih.Fill(pipi1)
                    pipil.Fill(pipi2)
                    kpi1.Fill(invmass(pks, ppip2))
                    kpi2.Fill(invmass(pks, ppip1))
                    pipipi.Fill(invmass(ppim, fourvecadd(ppip1, ppip2)))
                    kpim.Fill(invmass(pks, ppim))
                    kpimsum = fourvecadd(pks, ppim)
                    kpipih.Fill(invmass(kpimsum, ppip1))
                    kpipil.Fill(invmass(kpimsum, ppip2))
                else:
                    pipih.Fill(pipi2)
                    pipil.Fill(pipi1)
                    kpi1.Fill(invmass(pks, ppip1))
                    kpi2.Fill(invmass(pks, ppip2))
                    pipipi.Fill(invmass(ppim, fourvecadd(ppip1, ppip2)))
                    kpim.Fill(invmass(pks, ppim))
                    kpimsum = fourvecadd(pks, ppim)
                    kpipih.Fill(invmass(kpimsum, ppip2))
                    kpipil.Fill(invmass(kpimsum, ppip1))

    f.Write()
    f.Close()
    pt.Delete()

    return nselected, ntotal


def output_trkmtm2_kkpi(pt, datatype, mode, selfile, label, test=False):
    nselected = 0 
    ntotal = 0 
    modekey = tools.get_modekey(mode)
    efffile = get_efffile(selfile, datatype, test)
    tp = 'mc'
    if datatype == 'data':
        tp = 'data'

    f = TFile(selfile, 'recreate')
    effs = shelve.open(efffile, flag='r')
    effskeys = {}
    for dt in [x for x in effs if isinstance(effs[x], dict)]:
        keys = effs[dt].keys()
        keys.sort()
        effskeys[dt] = keys

    fuller = effs['total']

    def getEfficiency(mom, mode, type):
        correction = 1.0
        bincenters = effskeys[mode]
        upper = None
        for i in range(len(bincenters)):
            if mom < bincenters[i]:
                upper = i
                break
        if upper == None:
            if len(bincenters)-1 not in effs[mode]:
                rv = 0.3
            else:
                rv = effs[mode][len(bincenters)-1]
        elif upper == 0:
            rv = 0.3
        else:
            rv = ((mom-bincenters[upper-1])*effs[mode][bincenters[upper]]+
                  (bincenters[upper]-mom)*effs[mode][bincenters[upper-1]])/ \
                  (bincenters[upper]-bincenters[upper-1])*correction
        if rv < 0.03:
            print 'lo', mom
            rv = 0.3
        return rv

    h_mbc = TH1F('h_mbc'+tp, 'mbc', 100, 1.83, 1.89)
    kpi1 = TH1F('kpi1'+tp, '(K^{-} K^{+})', 100, 0.5, 1.5)
    pipih = TH1F('pipih'+tp, '(K^{+} #pi^{+})', 100, 0.2, 1.2)
    kpiz = TH1F('kpiz'+tp, 'K^{-} K^{+}', 100, 0.4, 1.6)
    kpipih = TH1F('kpipih'+tp, 'K^{-} (K^{+} #pi^{+})',
                        100, 0.6, 1.8)
    
    h_pkm = TH1F('h_pk'+tp, 'K^{-} momentum', 100, 0, 1.1)
    h_pkp = TH1F('h_ppi1'+tp, 'K^{+} momentum', 100, 0, 1)
    h_ppi = TH1F('h_ppiz'+tp, '#pi^{+} momentum', 100, 0, 1)

    h_pkm_c = TH1F('h_pk_c'+tp, 'K^{-} momentum, corrected', 100, 0, 1.1)
    h_pkp_c = TH1F('h_ppi1_c'+tp, 'K^{+} momentum, corrected', 100, 0, 1)
    h_ppi_c = TH1F('h_ppiz_c'+tp, '#pi^{+} momentum, corrected', 100, 0, 1)
   
    h_pkm_sb = TH1F('h_pk_sb'+tp, 'K^{-} momentum', 100, 0, 1.1)
    h_pkp_sb = TH1F('h_ppi1_sb'+tp, 'K^{+} momentum', 100, 0, 1)
    h_ppi_sb = TH1F('h_ppiz_sb'+tp, '#pi^{+} momentum', 100, 0, 1)

    h_pkm_sb_c = TH1F('h_pk_sb_c'+tp, 'K^{-} momentum, corrected', 100, 0, 1.1)
    h_pkp_sb_c = TH1F('h_ppi1_sb_c'+tp, 'K^{+} momentum, corrected', 100, 0, 1)
    h_ppi_sb_c = TH1F('h_ppiz_sb_c'+tp, '#pi^{+} momentum, corrected', 100, 0, 1)

    h_angkm = TH1F('h_angk'+tp, 'K^{-} cos #theta', 25, -1, 1)
    h_angkp = TH1F('h_angpi1'+tp, 'K^{+} cos #theta', 25, -1, 1)
    h_angpi = TH1F('h_angpiz'+tp, '#pi^{+} cos #theta', 25, -1, 1)

    signal_margins = [1.865, 1.875]
    sb_margins = [1.845, 1.855]

    for pte in pt:
        ntotal += 1
        if test and nselected > 10:
            break

        for sign in (1,):
            choice = chooseD(205, pte, sign)
            if choice != None :# and passDE(choice, pte) and pte.ecm > 3.7:
                h_mbc.Fill(pte.dmbc[choice])
                if not 1.865 < pte.dmbc[choice] < 1.87:
                    continue
                nselected += 1
                is_sideband = 0
                if signal_margins[0] < pte.dmbc[choice] < signal_margins[1]:
                    is_sideband = 0
                elif sb_margins[0] < pte.dmbc[choice] < sb_margins[1]:
                    is_sideband = 1
                else:
                    continue
                km = pte.ddau1[choice]; kp = pte.ddau2[choice];
                pi = pte.ddau3[choice]
                pkm = (pte.trke[km], pte.trkpx[km], pte.trkpy[km],
                       pte.trkpz[km])
                pkp = (pte.trke[kp], pte.trkpx[kp], pte.trkpy[kp],
                       pte.trkpz[kp])
                ppi = (pte.trpie[pi], pte.trpipx[pi], pte.trpipy[pi],
                       pte.trpipz[pi])
                mag_pkm = pmag(pkm) ; mag_pkp = pmag(pkp)
                mag_ppi = pmag(ppi)
                if is_sideband:
                    h_pkm_sb.Fill(mag_pkm)
                    h_ppi_sb.Fill(mag_ppi)
                    h_pkp_sb.Fill(mag_pkp)
                    h_pkp_sb_c.Fill(mag_pkp, 1/getEfficiency(mag_pkp, 'kp', type))
                    if getEfficiency(mag_pkm, 'km', type) == 0:
                        h_pkm_sb_c.Fill(mag_pkm, 1/0.3)
                    else:
                        h_pkm_sb_c.Fill(mag_pkm, 1/getEfficiency(mag_pkm, 'km', type))
                    if getEfficiency(mag_ppi, 'pi', type) == 0:
                        h_ppi_sb_c.Fill(mag_ppi, 1/0.3)
                    else:
                        h_ppi_sb_c.Fill(mag_ppi, 1/getEfficiency(mag_ppi, 'pi', type))                    
                else:
                    h_pkm.Fill(mag_pkm)
                    h_ppi.Fill(mag_ppi)
                    h_angkm.Fill(pte.trcosth[km])
                    h_angpi.Fill(cosangle(ppi,(0,0,0,1)))
                    h_pkp.Fill(mag_pkp)
                    h_angkp.Fill(pte.trcosth[kp])
                    efficiency = fuller.lookup(mag_pkm, mag_pkp, mag_ppi)

                    h_pkp_c.Fill(mag_pkp, 1/getEfficiency(mag_pkp, 'kp', type))

                    h_pkm_c.Fill(mag_pkm, 1/getEfficiency(mag_pkm, 'km', type))
                    h_ppi_c.Fill(mag_ppi, 1/getEfficiency(mag_ppi, 'pi', type))

                    pipi1 = invmass(ppi, pkp)

                    pipih.Fill(pipi1)
                    kpi1.Fill(invmass(pkm, pkp))
                    kpiz.Fill(invmass(pkm, pkp))
                    kpizsum = fourvecadd(pkm, ppi)
                    kpipih.Fill(invmass(kpizsum, pkp))

    f.Write()
    f.Close()
    pt.Delete()

    return nselected, ntotal

