from math import sqrt, radians

modes = { 0:
          {'sname'     : 'Kpi',
           'cname'     : 'D0AndD0B_to_Kpi' ,
           'buname'    : 'D0->K pi',
           'uname'     : 'D^{0}#rightarrowK^{-} #pi^{+}',
           'unamebar'  : '#bar{D}^{0}#rightarrowK^{+} #pi^{-}',
           'fname'     : 'D0_to_Kpi',
           'fnamebar'  : 'D0B_to_Kpi',
           'hname'     : 'D<sup>0</sup> &rarr K<sup>-</sup> &pi<sup>+</sup>',
           'hnamebar'  : '<span style="text-decoration:overline">D</span> <sup>0</sup>&rarr K<sup>+</sup> &pi<sup>-</sup> ',
           'lname'     : '$\Dzkpi$',
           'lnamebar'  : '$\Dzbarkpi$',
           'orgname'   : 'D^{0}\\to K^{- }\pi^{+ }',
           'orgnamebar': '-D- ^{0}\\to K^{+ }\pi^{- }',
           'decname'   : 'D0 to K- pi+',
           'decnamebar': 'anti-D0 to K+ pi-',
           'tag_num_s' : 6274,
           'mass'      : 1.8647,
           'mcdmode'   : 10001,
           'mcdbmode'  : 1010,
           'decutl'    : -0.0294,
           'decuth'    : 0.0294,
           'mbccut'    : 0.005,
           'trdau'     : (0, 1),
           'amplitude ratio' : sqrt(0.3308e-2), #2010.11.17 update sqrt(0.3317e-2),
           'amplitude ratio err' : sqrt(0.0080e-2), #2010.11.17 sqrt(0.0081e-2), 
           'phase'     : radians(21.3), # 26.6),
           'phase err' : radians(11.1), # 12.1),
           'coherence factor' : 1,
           'coherence factor err' : 0, 
           'daughter_defs'  : { 1: 'K-', 2: 'pi+' }
           },
          1:
          {'sname'     : 'Kpipi0',
           'cname'     : 'D0AndD0B_to_Kpipi0',
           'buname'    : 'D0->K pi pi0',
           'uname'     : 'D^{0}#rightarrowK^{-} #pi^{+} #pi^{0}',
           'unamebar'  : '#bar{D}^{0}#rightarrowK^{+} #pi^{-} #pi^{0}',
           'fname'     : 'D0_to_Kpipi0',
           'fnamebar'  : 'D0B_to_Kpipi0',
           'hname'     : 'D<sup>0</sup> &rarr K<sup>-</sup> &pi<sup>+</sup> &pi<sup>0</sup>',
           'hnamebar'  : '<span style="text-decoration:overline">D</span> <sup>0</sup>&rarr K<sup>+</sup> &pi<sup>-</sup> &pi<sup>0</sup>',
           'lname'     : '$\Dzkpipiz$',
           'lnamebar'  : '$\Dzbarkpipiz$',
           'orgname'   : 'D^{0}\\to K^{- }\pi^{+ }\pi^{0}',
           'orgnamebar': '-D- ^{0}\\to K^{+ }\pi^{- }\pi^{0}',
           'decname'   : 'D0 to K- pi+ pi0',
           'decnamebar': 'anti-D0 to K+ pi- pi0',
           'tag_num_s' : 19735,
           'mass'      : 1.8647,
           'mcdmode'   : 110001,
           'mcdbmode'  : 101010,
           'decutl'    : -0.0583,
           'decuth'    : 0.0350,
           'mbccut'    : 0.005,
           'trdau'     : (0, 1),
           'amplitude ratio' : sqrt(2.20e-3), # PDG2010
           'amplitude ratio err' : sqrt(0.10e-3), # PDG2010 
           'phase'     : radians(227-180),  # arXiv:0903.4853
           'phase err' : radians(17),
           'coherence factor' : 0.84, #  arXiv:0903.4853
           'coherence factor err' : 0.07,
           'average pi0 momentum': 0.478,
           'daughter_defs'  : { 1: 'K-', 2: 'pi+' , 3: 'pi0'}
           },
          3:           
          {'sname'     : 'K3pi',
           'cname'     : 'D0AndD0B_to_Kpipipi',
           'buname'    : 'D0->K 3pi', 
           'uname'     : 'D^{0}#rightarrowK^{-} #pi^{+} #pi^{+} #pi^{-}',
           'unamebar'  : '#bar{D}^{0}#rightarrowK^{+} #pi^{-} #pi^{-} #pi^{+}',
           'fname'     : 'D0_to_Kpipipi',
           'fnamebar'  : 'D0B_to_Kpipipi',
           'hname'     : 'D<sup>0</sup> &rarr K<sup>-</sup> &pi<sup>+</sup> &pi<sup>-</sup> &pi<sup>+</sup>',
           'hnamebar'  : '<span style="text-decoration:overline">D</span> <sup>0</sup>&rarr K<sup>+</sup> &pi<sup>-</sup> &pi<sup>+</sup> &pi<sup>-</sup>',
           'lname'     : '$\Dzkpipipi$',
           'lnamebar'  : '$\Dzbarkpipipi$',
           'orgname'   : 'D^{0}\\to K^{- }\pi^{+ }\pi^{- }\pi^{+ }',
           'orgnamebar': '-D- ^{0}\\to K^{+ }\pi^{- }\pi^{+ }\pi^{- }',
           'decname'   : 'D0 to K- pi+ pi- pi+',
           'decnamebar': 'anti-D0 to K+ pi- pi+ pi-',
           'tag_num_s' : 9948,
           'mass'      : 1.8647,
           'mcdmode'   : 21001,
           'mcdbmode'  : 12010,
           'decutl'    : -0.0200,
           'decuth'    : 0.0200,
           'mbccut'    : 0.005,
           'trdau'     : (0, 1, 2, 3),
           'amplitude ratio' : sqrt(3.24e-3), # PDG2010 
           'amplitude ratio err' : sqrt(0.25e-3),
           'phase'     : radians(114-180), # arXiv:0903.4853
           'phase err'     : radians(26),
           'coherence factor' : 0.33, #  arXiv:0903.4853
           'coherence factor err' : 0.23,
           'daughter_defs'  : { 1: 'K-', 2: 'pi+' , 3: 'pi+', 4: 'pi-'}
           },
          200:         
          {'sname'     : 'Kpipi',
           'cname'     : 'DpAndDm_to_Kpipi',
           'buname'    : 'D+->K pi pi',
           'uname'     : 'D^{+}#rightarrowK^{-} #pi^{+} #pi^{+}',
           'unamebar'  : 'D^{-}#rightarrowK^{+} #pi^{-} #pi^{-}',
           'fname'     : 'Dp_to_Kpipi',
           'fnamebar'  : 'Dm_to_Kpipi',
           'hname'     : 'D<sup>+</sup> &rarr K<sup>-</sup> &pi<sup>+</sup> &pi<sup>+</sup>',
           'hnamebar'  : 'D<sup>-</sup> &rarr K<sup>+</sup> &pi<sup>-</sup> &pi<sup>-</sup>',
           'lname'     : '$\Dpkpipi$',
           'lnamebar'  : '$\Dmkpipi$',
           'orgname'   : 'D^{+ }\\to K^{- }\pi^{+ }\pi^{+ }',
           'orgnamebar': 'D^{- }\\to K^{+ }\pi^{- }\pi^{- }',
           'decname'   : 'D+ to K- pi+ pi+',
           'decnamebar': 'D- to K+ pi- pi-',
           'tag_num_s' : 7998,
           'mass'      : 1.8694,
           'mcdmode'   : 20001,
           'mcdbmode'  : 2010,
           'decutl'    : -0.0218,
           'decuth'    : 0.0218,
           'mbccut'    : 0.005,
           'trdau'     : (0, 1, 2),
           'daughter_defs'  : { 1: 'K-', 2: 'pi+' , 3: 'pi+'}
           },
          201:         
          {'sname'     : 'Kpipipi0',
           'cname'     : 'DpAndDm_to_Kpipipi0',
           'buname'    : 'D+->K pi pi pi0',
           'uname'     : 'D^{+}#rightarrowK^{-} #pi^{+} #pi^{+} #pi^{0}',
           'unamebar'  : 'D^{-}#rightarrowK^{+} #pi^{-} #pi^{-} #pi^{0}',
           'fname'     : 'Dp_to_Kpipipi0',
           'fnamebar'  : 'Dm_to_Kpipipi0',
           'hname'     : 'D<sup>+</sup> &rarr K<sup>-</sup> &pi<sup>+</sup> &pi<sup>+</sup> &pi<sup>0</sup>',
           'hnamebar'  : 'D<sup>-</sup> &rarr K<sup>+</sup> &pi<sup>-</sup> &pi<sup>-</sup> &pi<sup>0</sup>',
           'lname'     : '$\Dpkpipipiz$',
           'lnamebar'  : '$\Dmkpipipiz$',
           'orgname'   : 'D^{+ }\\to K^{- }\pi^{+ }\pi^{+ }\pi^{0}',
           'orgnamebar': 'D^{- }\\to K^{+ }\pi^{- }\pi^{- }\pi^{0}',
           'decname'   : 'D+ to K- pi+ pi+ pi0',
           'decnamebar': 'D- to K+ pi- pi- pi0',
           'tag_num_s' : 7338,
           'mass'      : 1.8694,
           'mcdmode'   : 120001,
           'mcdbmode'  : 102010,
           'decutl'    : -0.0518,
           'decuth'    : 0.0401,
           'mbccut'    : 0.005,
           'trdau'     : (0, 1, 2),
           'average pi0 momentum': 0.339, 
           'daughter_defs'  : { 1: 'K-', 2: 'pi+' , 3: 'pi+', 4: 'pi0'}
           },
          202:         
          {'sname'     : 'Kspi',
           'cname'     : 'DpAndDm_to_Kspi',
           'buname'    : 'D+->Ks pi', 
           'uname'     : 'D^{+}#rightarrowK_{S} #pi^{+}',
           'unamebar'  : 'D^{-}#rightarrowK_{S} #pi^{-}',
           'fname'     : 'Dp_to_Kspi',
           'fnamebar'  : 'Dm_to_Kspi',
           'hname'     : 'D<sup>+</sup> &rarr K<sub>S</sub><sup>0</sup> &pi<sup>+</sup>',
           'hnamebar'  : 'D<sup>-</sup> &rarr  K<sub>S</sub><sup>0</sup>&pi<sup>-</sup>',
           'lname'     : '$\Dpkspi$',
           'lnamebar'  : '$\Dmkspi$',
           'orgname'   : 'D^{+ }\\to K^{0}_{S}\pi^{+ }',
           'orgnamebar': 'D^{- }\\to K^{0}_{S}\pi^{- }',
           'decname'   : 'D+ to K_S0 pi+',
           'decnamebar': 'D- to K_S0 pi-',
           'tag_num_s' : 8000,
           'mass'      : 1.8694,
           'mcdmode'   : 10100,
           'mcdbmode'  : 1100,
           'decutl'    : -0.0265,
           'decuth'    : 0.0265,
           'mbccut'    : 0.005,
           'trdau'     : (1, ),
           'bkg_multipions' : 'Dp_to_pipipi',
           'daughter_defs'  : { 1: 'KS', 2: 'pi+'}
           },
          203:         
          {'sname'     : 'Kspipi0',
           'cname'     : 'DpAndDm_to_Kspipi0',
           'buname'    : 'D+->Ks pi pi0', 
           'uname'     : 'D^{+}#rightarrowK_{S} #pi^{+} #pi^{0}',
           'unamebar'  : 'D^{-}#rightarrowK_{S} #pi^{-} #pi^{0}',
           'fname'     : 'Dp_to_Kspipi0', 
           'fnamebar'  : 'Dm_to_Kspipi0',
           'hname'     : 'D<sup>+</sup> &rarr K<sub>S</sub><sup>0</sup> &pi<sup>+</sup> &pi<sup>0</sup>',
           'hnamebar'  : 'D<sup>-</sup> &rarr  K<sub>S</sub><sup>0</sup>&pi<sup>-</sup> &pi<sup>0</sup>',
           'lname'     : '$\Dpkspipiz$',
           'lnamebar'  : '$\Dmkspipiz$',
           'orgname'   : 'D^{+ }\\to K^{0}_{S}\pi^{+ }\pi^{0}',
           'orgnamebar': 'D^{- }\\to K^{0}_{S}\pi^{- }\pi^{0}',
           'decname'   : 'D+ to K_S0 pi+ pi0',
           'decnamebar': 'D- to K_S0 pi- pi0',
           'tag_num_s' : 5716,
           'mass'      : 1.8694,
           'mcdmode'   : 110100, 
           'mcdbmode'  : 101100,
           'decutl'    : -0.0455,
           'decuth'    : 0.0423,
           'mbccut'    : 0.005,
           'trdau'     : (1, ),
           'average pi0 momentum': 0.498, 
           'bkg_multipions' : 'Dp_to_pipipipi0',
           'daughter_defs'  : { 1: 'KS', 2: 'pi+' , 3: 'pi0'}
           },
          204:         
          {'sname'     : 'Ks3pi',
           'cname'     : 'DpAndDm_to_Kspipipi',
           'buname'    : 'D+->Ks pi pi pi', 
           'uname'     : 'D^{+}#rightarrowK_{S} #pi^{+} #pi^{+} #pi^{-}',
           'unamebar'  : 'D^{-}#rightarrowK_{S} #pi^{-} #pi^{-} #pi^{+}',
           'fname'     : 'Dp_to_Kspipipi',
           'fnamebar'  : 'Dm_to_Kspipipi',
           'hname'     : 'D<sup>+</sup> &rarr K<sub>S</sub><sup>0</sup> &pi<sup>+</sup> &pi<sup>+</sup> &pi<sup>-</sup>',
           'hnamebar'  : 'D<sup>-</sup> &rarr  K<sub>S</sub><sup>0</sup>&pi<sup>-</sup> &pi<sup>-</sup> &pi<sup>+</sup>',
           'lname'     : '$\Dpkspipipi$',
           'lnamebar'  : '$\Dmkspipipi$',
           'orgname'   : 'D^{+ }\\to K^{0}_{S}\pi^{+ }\pi^{+ }\pi^{- }',
           'orgnamebar': 'D^{- }\\to K^{0}_{S}\pi^{- }\pi^{- }\pi^{+ }',
           'decname'   : 'D+ to K_S0 pi+ pi+ pi-',
           'decnamebar': 'D- to K_S0 pi- pi- pi+',
           'tag_num_s' : 3931,
           'mass'      : 1.8694,
           'mcdmode'   : 21100,
           'mcdbmode'  : 12100,
           'decutl'    : -0.0265,
           'decuth'    : 0.0265,
           'mbccut'    : 0.005,
           'trdau'     : (1, 2, 3),
           'bkg_multipions' : 'Dp_to_pipipipipi',
           'daughter_defs'  : { 1: 'KS', 2: 'pi+' , 3: 'pi+', 4: 'pi-'}
           },
          205:         
          {'sname'     : 'KKpi',
           'cname'     : 'DpAndDm_to_KKpi',
           'buname'    : 'D+->K K pi',
           'uname'     : 'D^{+}#rightarrowK^{-} K^{+} #pi^{+}',
           'unamebar'  : 'D^{-}#rightarrowK^{+} K^{-} #pi^{-}',
           'fname'     : 'Dp_to_KKpi', 
           'fnamebar'  : 'Dm_to_KKpi',
           'hname'     : 'D<sup>+</sup> &rarr K<sup>+</sup> K<sup>-</sup> &pi<sup>+</sup>',
           'hnamebar'  : 'D<sup>-</sup> &rarr K<sup>-</sup> K<sup>+</sup> &pi<sup>-</sup>',
           'lname'     : '$\Dpkkpi$',
           'lnamebar'  : '$\Dmkkpi$',
           'orgname'   : 'D^{+ }\\to K^{+ }K^{- }\pi^{+ }',
           'orgnamebar': 'D^{- }\\to K^{- }K^{+ }\pi^{- }',
           'decname'   : 'D+ to K+ K- pi+',
           'decnamebar': 'D- to K- K+ pi-',
           'tag_num_s' : 2000,
           'mass'      : 1.8694,
           'mcdmode'   : 10011,
           'mcdbmode'  : 1011,
           'decutl'    : -0.0218,
           'decuth'    : 0.0218,
           'mbccut'    : 0.005,
           'trdau'     : (1, 2, 3),
           'daughter_defs'  : { 1: 'K-', 2: 'K+' , 3: 'pi+'}
           }

          }


bkgmodes = {
    'Dp_to_pipipi':
    {'tag_num_s': 2000}
    }


Dz_modes = [ 'Kpi', 'Kpipi0', 'Kpipipi' ]

Dpm_modes = [ 'Kpipi', 'Kpipipi0', 'Kspi', 'Kspipi0', 'Kspipipi', 'KKpi' ]

dmode_dict = { 1: 'K-', 10: 'K+', 100: 'K0', 1000: 'pi-', 10000: 'pi+',
               100000: 'pi0', 1000000: 'gamma', 10000000: 'l',
               100000000: "eta(')", 1000000000: 'X'}

dmode_revdict = {}
for e in dmode_dict:
    dmode_revdict[dmode_dict[e]] = e
            
## CORRESPONDS TO GENERIC MC
width_modes = { '0': 0.00126, '1': 0.00160, '3': 0.00131, '200': 0.00128,
                '201': 0.00144, '202': 0.00127, '203': 0.00148,
                '204': 0.00128, '205': 0.00129 }

bkg_generic_ddbar_281_max = {
    'Single_D0_to_Kpi': 50, 
    'Single_D0_to_Kpipi0': 2200,
    'Single_D0_to_Kpipipi': 2000,
    'Single_Dp_to_Kpipi': 1200,
    'Single_Dp_to_Kpipipi0': 8000,
    'Single_Dp_to_Kspi': 120,
    'Single_Dp_to_Kspipi0': 3200,
    'Single_Dp_to_Kspipipi': 3800,
    'Single_Dp_to_KKpi': 1200
    }

bkg_generic_ddbar_537_max = {
    'Single_D0_to_Kpi': 50, 
    'Single_D0_to_Kpipi0': 5200,
    'Single_D0_to_Kpipipi': 4000,
    'Single_Dp_to_Kpipi': 2200,
    'Single_Dp_to_Kpipipi0': 12000,
    'Single_Dp_to_Kspi': 180,
    'Single_Dp_to_Kspipi0': 6000,
    'Single_Dp_to_Kspipipi': 6800,
    'Single_Dp_to_KKpi': 2200
    }


bkg_generic_ddbar_818_max = {
    'Single_D0_to_Kpi': 100, 
    'Single_D0_to_Kpipi0': 8000,
    'Single_D0_to_Kpipipi': 6000,
    'Single_Dp_to_Kpipi': 3200,
    'Single_Dp_to_Kpipipi0': 18000,
    'Single_Dp_to_Kspi': 240,
    'Single_Dp_to_Kspipi0': 9000,
    'Single_Dp_to_Kspipipi': 11000,
    'Single_Dp_to_KKpi': 3200
    }

bkg_generic_ddbar_818_max_noxfeed = {
    'Single_D0_to_Kpi': 60, 
    'Single_D0_to_Kpipi0': 4000,
    'Single_D0_to_Kpipipi': 4000,
    'Single_Dp_to_Kpipi': 1200,
    'Single_Dp_to_Kpipipi0': 10000,
    'Single_Dp_to_Kspi': 120,
    'Single_Dp_to_Kspipi0': 5000,
    'Single_Dp_to_Kspipipi': 6000,
    'Single_Dp_to_KKpi': 1500
    }

def mcdmodetostring(mcdmode):
    str = `mcdmode`
    retstrs = []
    for i in range(len(str)-1, -1, -1):
        for j in range(int(str[i])):
            retstrs.append(dmode_dict[10**(len(str)-1-i)] + ' ')
    return ''.join(retstrs)


def mcdmode_to_dmodename(mcdmode):
    children = mcdmodetostring(mcdmode)
    dcharge = total_charge(children)
    if dcharge == 0:
        dmodename = 'D0 to '+children
    elif dcharge == 1:
        dmodename = 'Dp to '+children
    elif dcharge == 'Unknown':
        dmodename = 'D to '+children
    else:
        raise NameError(dcharge)
    return dmodename

def mcdbmode_to_dmodename(mcdbmode):
    children = mcdmodetostring(mcdbmode)
    dbcharge = total_charge(children)
    if dbcharge == 0:
        dbmodename = 'D0B to '+children
    elif dbcharge == -1:
        dbmodename = 'Dm to '+children
    elif dbcharge == 'Unknown':
        dbmodename = 'Dbar to '+children
    else:
        raise NameError(dbcharge)
    return dbmodename

def set_modes_attr(opt=''):
    for mode in modes:
        if 'widede' in opt :
            modes[mode]['decutl'] *= 2
            modes[mode]['decuth'] *= 2
        
        if 'posde'  in opt :
            modes[mode]['decutl'] =0
        
        if 'negde'  in opt :
            modes[mode]['decuth'] =0
    
        if 'desidebandl' in opt :
            if mode ==1 or mode == 201:
                modes[mode]['decuth'] = - 0.060  
            else:
                modes[mode]['decutl'] = -0.100
                modes[mode]['decuth'] = -0.050

        if 'desidebandh' in opt : 
            modes[mode]['decutl'] = 0.050
            modes[mode]['decuth'] = 0.100

def total_charge(children):
    children = [child for child in children.split(' ') if child != '']
    total_charge = 0 
    for child in children:
        charge = child[-1]
        if charge == '+':
            total_charge += 1
        elif charge == '-':
            total_charge += -1
        elif charge == '0':
            total_charge += 0
        else:
            total_charge = 'Unknown'

    return total_charge
        
