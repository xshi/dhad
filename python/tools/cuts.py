"""
Module for Selection Cuts

Partly borrowed from Peter Onyisi. 

"""
import sys 
import attr
from math import sqrt
from attr import trigger
from attr import etamunu, DS_STARTS_FROM, pi0semin
modes = attr.modes


def checkVetoes(mode, pte, index, opt='', sign=None):
    if 'trig' in opt:
        if 'trig2' in opt:
            if not pte.l1trig2 & trigger.kTwoTrack:
                return False
        else:    
            if (not pte.l1trig & trigger.kElTrack) and (
                not pte.l1trig2 & trigger.kTwoTrack):
                return False
    
    if 'costh' in opt :
        daughter_defs = modes[mode]['daughter_defs']
        for daughter in daughter_defs:
            dauind = pte.__getattr__('ddau%d' % daughter)[index]
            if daughter_defs[daughter] in ('K-', 'K+', 'pi-', 'pi+'):
                if abs(pte.trcosth[dauind]) > 0.9:
                    return False
            elif daughter_defs[daughter] == 'KS':
                if (abs(pte.trcosth[pte.ksdau1[dauind]]) > 0.9 or
                    abs(pte.trcosth[pte.ksdau2[dauind]]) > 0.9):
                    return False

    if 'nosig' in opt :
        # mcdmode code: gamma, pi0, pi+, pi-, K0, K+, K-

        mcdmode  = modes[mode]['mcdmode']
        mcdbmode = modes[mode]['mcdbmode']

        evt_mcdmode = remove_gamma(pte.mcdmode)
        evt_mcdbmode = remove_gamma(pte.mcdbmode)

        if evt_mcdmode == mcdmode or evt_mcdbmode == mcdbmode:
            return False
        if evt_mcdmode == mcdbmode or evt_mcdbmode == mcdmode :
            return False

        # Consider the positive part for now.
        if sign == -1:
            raise ValueError(sign)
        
        if mode == 3:
            if evt_mcdbmode == 10101 or evt_mcdmode == 10101: 
                return False
        if mode == 202:
            if evt_mcdmode == 21000 or evt_mcdmode == 10001:
                return False
        if mode == 203:
            if evt_mcdmode == 121000:
                return False
        if mode == 204:
            if evt_mcdmode == 32000 or mcdmode == 10200:
                return False

    if 'noxfeed' in opt:
        evt_mcdmode = remove_gamma(pte.mcdmode)
        evt_mcdbmode = remove_gamma(pte.mcdbmode)
        
        for mode_key in modes:
            mcdmode  = modes[mode_key]['mcdmode']
            mcdbmode = modes[mode_key]['mcdbmode']
            if evt_mcdmode == mcdmode or evt_mcdbmode == mcdbmode:
                return False
            if evt_mcdmode == mcdbmode or evt_mcdbmode == mcdmode:
                return False

    if 'nofsr' in opt:
        mcdmode  = modes[mode]['mcdmode']
        mcdbmode = modes[mode]['mcdbmode']
        if (sign == 1 and pte.mcdmode != mcdmode) or \
               (sign == -1 and pte.mcdbmode != mcdbmode):
            return False

    if 'trhitf' in opt:
        trhitf_0 = eval(opt.split('trhitf/')[1])

        for trk_daughter in modes[mode]['trdau']:
            ddaughter_index = pte.__getattr__('ddau%d'%(trk_daughter+1))[index]
            trhitf_1 = pte.trhitf[ddaughter_index]
            
            if trhitf_1 < trhitf_0:
                return False

    # Use +- 12 MeV ( 3-sigma) for Kshort mass cut to match the DSkim v1
    # Must do this before the Cabibbo suppressed cuts, otherwise IndexError. 
    if mode in [202, 203, 204]:
        ksindex = pte.ddau1[index]
        ksmass = pte.ksmass[ksindex]
        ksmax = 0.4977 + 0.012 # 0.5097  
        ksmin = 0.4977 - 0.012 # 0.4857
        
        if 'kssideband' in opt:
            if '_srs' in opt: # 6.5 sigma 
                if not (0.4717 < ksmass < 0.482 or 0.5134 < ksmass < 0.5237):
                    return False
            else: 
                if not (0.47 < ksmass < 0.482 or 0.5134 < ksmass < 0.5254):
                    return False
        else:
            if ksmin > ksmass or ksmass > ksmax:
                return False
        
    if mode == 0:
        if pte.ntrack == 2 and pte.lepveto[index] >= -1:
            return False

    elif mode == 1: # K pi pi0 
        pi0index = pte.ddau3[index]
        # only need to check softer photon
        # se : Shower Energy
        if pte.se[int(pte.pi0dau2[pi0index])] < pi0semin:
            return False

    elif mode == 201: # K pi pi pi0 
        pi0index = pte.ddau4[index]

    elif mode == 203: # Ks pi pi0 
        pi0index = pte.ddau3[index]
	
    elif mode == 204:
        #D+ -> KS0 pi pi pi, has backgrounds from Cabibbo suppressed
        #modes with two KS0.
        
        pions = [pte.ddau2[index], pte.ddau3[index],
                 pte.ddau4[index]]
        fourvecs = []
        for index in pions:
            fourvecs.append([pte.trpie[index], pte.trpipx[index],
                             pte.trpipy[index], pte.trpipz[index]])
        imass1 = invmass(fourvecs[0], fourvecs[2])
        imass2 = invmass(fourvecs[1], fourvecs[2])
        ksfound = False
        if 0.491 < imass1 < 0.504 or \
           0.491 < imass2 < 0.504 :
            return False

    # Check the type1 pi0 in modes Kpipi0, Kpipipi0, Kspipi0
    if mode in [1, 201, 203] and '281ipbv0' not in opt:
	if pte.pi0istype1[pi0index] != 1:
	    return False 

	    
    return True



def chooseD(mode, pte, sign, checkVetoes=checkVetoes,
            alt_deltae=None, opt=''):

    choices = {}
    if mode < DS_STARTS_FROM:

        if pte.ecm < 3.7:
            return None
            
        for i in range(pte.ndcand):
            if pte.dmode[i] == mode and pte.dcsign[i]==sign:

                if checkVetoes(mode, pte, i, opt, sign):
                    if 'noDEcut' in opt or passDE(i, pte, alt_deltae):
                        choices[abs(pte.ddeltae[i])] = i
                            
    else:
        for i in range(pte.ndcand):
            if pte.dmode[i] == mode and pte.dcsign[i]==sign:
                if checkVetoes(mode, pte, i) and passMBC(i, pte, 'loose'):
                    choices[abs(pte.dmbc[i]-MBC_FOR_DSDSSTAR)] = i
    DEs = choices.keys()
    if DEs:
        return choices[min(DEs)]
    else:
        return None


def chooseDD(dmode, dbmode, pte, checkVetoes=checkVetoes, opt=''):
    choices = {}
    for i in range(pte.nddcand):
        d = pte.d[i]; dbar = pte.dbar[i]
        if pte.dmode[d] == dmode and pte.dmode[dbar] == dbmode:
            if 'nofsr' in opt:
                mcdmode  = modes[dmode]['mcdmode']
                mcdbmode = modes[dbmode]['mcdbmode']
                if pte.mcdmode != mcdmode or pte.mcdbmode != mcdbmode:
                    continue

            if not checkVetoes(dmode, pte, d, opt) or \
               not checkVetoes(dbmode, pte, dbar, opt):
                continue
            if dmode >= DS_STARTS_FROM:
                if not ((passMBC(d, pte, 'loose') and \
                         passMBC(dbar, pte, 'tight'))
                        or (passMBC(d, pte, 'tight') and \
                            passMBC(dbar, pte, 'loose'))):
                    continue
                choices[abs(pte.dmraw[d]+pte.dmraw[dbar]
                            -2*modes[dmode]['mass'])] = i
            else:
                if not passDE(d, pte):
                    continue
                if not passDE(dbar, pte):
                    continue
                choices[abs(pte.dmbc[d]+pte.dmbc[dbar]
                            -2*modes[dmode]['mass'])] = i
    DEs = choices.keys()
    if DEs:
        return choices[min(DEs)]
    else:
        return None



def invmass(*p4s):
    return sqrt(invmasssq(*p4s))

def invmasssq(*p4s):
    total = map(sum, zip(*p4s))
    return sum(map(lambda x: x[0]*x[0]*x[1], zip(total, etamunu)))


def passDE(choice, pte, alt_deltae=None):
    if alt_deltae != None:
        return alt_deltae['decutl'] < pte.ddeltae[choice] < alt_deltae['decuth']
    else:
        mode = pte.dmode[choice]
        return modes[mode]['decutl'] < pte.ddeltae[choice] < modes[mode]['decuth']


def get_mBC(mode, pte, d, opt=''):

    if  'calc' in opt :
        if mode == 1:
            p1_index = pte.ddau1[d]
            p1e = pte.trke[p1_index]
            p1x = pte.trkpx[p1_index]
            p1y = pte.trkpy[p1_index]
            p1z = pte.trkpz[p1_index]
            p1 = lab.Momentum(p1e, p1x, p1y, p1z)

            p2_index = pte.ddau2[d]
            p2e = pte.trpie[p2_index]
            p2x = pte.trpipx[p2_index]
            p2y = pte.trpipy[p2_index]
            p2z = pte.trpipz[p2_index]
            p2  = lab.Momentum(p2e, p2x, p2y, p2z)
                        
            p3_index = pte.ddau3[d]
            p3e = pte.pi0e[p3_index]
            p3x = pte.pi0px[p3_index]
            p3y = pte.pi0py[p3_index]
            p3z = pte.pi0pz[p3_index]
            p3  = lab.Momentum(p3e, p3x, p3y, p3z)

            if 'pi0' in opt:
                factor = float(opt.split('pi0/')[1])
                p3x = p3x * factor
                p3y = p3y * factor
                p3z = p3z * factor
                p3e = sqrt(p3.mass**2 + p3x**2 + p3y**2 + p3z**2)
                p3  = lab.Momentum(p3e, p3x, p3y, p3z)

            pd = p1+p2+p3

        else:
            raise ValueError('Mode not implemented.')

        ppsi = lab.Momentum(pte.ecm,pte.pxcm,pte.pycm,pte.pzcm)
        psiframe =  ppsi.rest_frame
        pde, pdx,pdy, pdz = psiframe.coordinatesOf(pd)
        ebm = ppsi.mass/2.0

        mbc = sqrt(ebm**2 - pdx**2 - pdy**2 - pdz**2)

        if 'diff' in opt:
            diff = (mbc - pte.dmbc[d])*100./pte.dmbc[d]
            return diff
    else:
        mbc = pte.dmbc[d]
    
    return mbc


def get_decimal_at_position(integer, position):
    integer = int(integer)
    val = (integer % 10**(position+1)) - (integer % 10**position)
    return val / 10**position

def set_decimal_at_position(integer, position, new_val):
    new_str = []
    pos     = 0
    length = len(str(integer))
    for i in str(integer):
        pos+= 1
        if length-pos == position: 
            new_str.append(str(new_val))
        else:
            new_str.append(i)
    new_integer = int(''.join(new_str))
    return new_integer

def remove_gamma(evt_mcdmode):
    gamma_num = get_decimal_at_position(evt_mcdmode, 6)
    if gamma_num != 0:
        evt_mcdmode = set_decimal_at_position(evt_mcdmode, 6, 0)
    return evt_mcdmode


def countDcand(mode, pte, sign):
    rv = 0
    for i in range(pte.ndcand):
        if (pte.dmode[i] == mode and pte.dcsign[i]==sign and
            checkVetoes(mode, pte, i) and passDE(i, pte)):
            rv += 1
    return rv

