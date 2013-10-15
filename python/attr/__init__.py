"""
Providing Attributes in the D-Hadronic analysis scripts. 

"""

import os
import sys
from modes import modes, bkgmodes 
from math import sqrt  
from dhad import __version__ as version

__author__ = "Xin Shi <xs32@cornell.edu>"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2006-2011 Xin Shi"
__license__ = "GNU GPL"

#versions = ['6.09', '7.03', '7.05', '7.06', '9.03', '10.1']

#analysis = '10.1' use Label to identify analysis
#src = '11.4'


cleog = "20080624_MCGEN"
pass2 = "20071023_MCP2_A"
dskim = "20060224_FULL_A_3"
ntuple = "20080228_FULL"
fitter ='/home/xs32/work/CLEO/analysis/DHad/lib/HDBFitter/HDBFitter20070611'

datasets_281 = ['data31', 'data32', 'data33', 'data34', 'data35', 'data36',
                'data37']

base = os.environ['dhad']
rbase = os.environ['rdhad']

datpath = os.path.join(base,  'dat')
figpath = os.path.join(base,  'fig')
rfigpath = os.path.join(rbase,  'fig')
logpath = os.path.join(base,  'log')
tabpath = os.path.join(base,  'tab')

brfpath = os.path.join(base,  'dat', 'brf')
fitpath = os.path.join(base,  'dat', 'fit')
evtpath = os.path.join(base,  'dat', 'evt')
bkgpath = os.path.join(base,  'dat', 'bkg')

yldlogpath = os.path.join(base,  'log', 'yld')
sellogpath = os.path.join(base,  'log', 'sel')

orgsetup = os.path.join(base, 'web/setup.el')

#src = sys.argv[0].split('dhad-')[-1]
# based on srcpath
genpath = os.path.join(base, 'src', version, 'gen')
#if not os.access(genpath, os.F_OK) :
#    os.makedirs(genpath)

srcfitpath = os.path.join(base, 'src', version, 'fit')
srcselpath = os.path.join(base, 'src', version, 'sel')
srcprocpath = os.path.join(base, 'src', version, 'proc')
srcbrfpath = os.path.join(base, 'src', version, 'brf')
srcmnfpath = os.path.join(base, 'src', version, 'mnf')


# for CBX Path
cbxpath = os.path.join(base, 'doc/cbx818')
rcbxpath = os.path.join(rbase, 'doc/cbx818')
cbxtabpath = os.path.join(cbxpath, 'tab')
cbxfigpath = os.path.join(cbxpath, 'fig')
rcbxfigpath = os.path.join(rcbxpath, 'fig')
fitbase = os.path.join(base,  'dat', 'fit')
evtlogbase = os.path.join(base,  'log', 'evt')


TypeNames = {'s': 'signal', 'g': 'generic', 'd': 'data' }
TagNames = { 's': 'Single', 'd': 'Double' }


tab_web_header = '#+SETUPFILE: ../../web/tab.org\n'
tab_web_footer = ': '+ sys.argv[0].split('/')[-1] +' '+' '.join(sys.argv[1:])

fig_web_header = '#+SETUPFILE: ../../web/fig.org\n'
fig_web_footer = tab_web_footer

mode_line_dict = {0 :1,  1:2, 3:3, 200:4, 201:5, 202:6, 203:7, 204:8, 205:9 }

PossibleDoubleTags = [(akey, bkey) for akey in modes for bkey in modes \
                        if (akey < 200 and bkey < 200) or \
                        (akey >= 200 and bkey >= 200)]

DoubleTags_DZ = [(akey, bkey) for akey in modes for bkey in modes \
                        if (akey < 200 and bkey < 200) ]

DoubleTags_DP = [(akey, bkey) for akey in modes for bkey in modes \
                        if (akey >= 200 and bkey >= 200) ]

DiagDoubleTags = [(akey, bkey) for (akey, bkey) in PossibleDoubleTags\
                  if (akey == bkey)]

NonDiagDoubleTags = [(akey, bkey) for (akey, bkey) in PossibleDoubleTags\
                     if (akey != bkey)]


interfacecodes = {0: 'kpi', 1: 'kpipi0', 3: 'kpipipi',
                  200: 'kpipi',  201: 'kpipipi0', 202: 'kspi',
                  203: 'kspipi0', 204: 'kspipipi', 205: 'kkpi' }


veto_fakes_string_list = ['D0_to_Kpipi0 fakes Dp_to_Kpipi:',
                          'D0_to_Kpipi0 fakes Dp_to_Kspipi0:',
                          'D0B_to_Kpipipi fakes Dm_to_Kpipipi0:',
                          'Dp_to_Kpipi fakes D0B_to_Kpipipi:']  

used_crossfeeds = ['D0_to_Kpi fakes D0B_to_Kpi:', 'D0B_to_Kpi fakes D0_to_Kpi:']


simulation_parts = ['tracks',
                    'charged pions',
                    'charged kaons',
                    'electrons',
                    'showers',
                    'K0S',
                    'pi0',
                    'eta']

fit_paras = [  'ND0D0Bar' ,
               'BrD2KPi'     ,
               'BrD2KPiPi0'  ,
               'BrD2KPiPiPi' ,
               'ND+D-'       ,
               'BrD2KPiPi'   ,
               'BrD2KPiPiPi0',
               'BrD2KsPi'    ,
               'BrD2KsPiPi0' ,
               'BrD2KsPiPiPi',
               'BrD2KKPi'    ,
               ]

PDG2004_NBF = ['--',
               '0.0380 +/- 0.0009',
               '0.130 +/- 0.008',
               '0.0746 +/- 0.0031',
               '--',
               '0.092 +/- 0.006',
               '0.065 +/- 0.011',
               '0.014 +/- 0.001',
               '0.049 +/- 0.015',
               '0.036 +/- 0.005',
               '0.0089 +/- 0.0008'          
               ]


PDG2004_BF_Ratio = ['3.42 +/- 0.22',
                    '1.96 +/- 0.08',
                    '0.70 +/- 0.12',
                    '0.153 +/- 0.003',
                    '0.527 +/- 0.167',
                    '0.385 +/- 0.050',
                    '0.097 +/- 0.006'
                    ]

PDG2009_NBF = ['--',
               '0.0391 +/- 0.0005',
               '0.140 +/- 0.005',
               '0.0814 +/- 0.0020',
               '--',
               '0.0929 +/- 0.0025',
               '0.0604 +/- 0.0022',
               '0.0146 +/- 0.0004',
               '0.068 +/- 0.004',
               '0.0304 +/- 0.0011',
               '0.0097 +/- 0.0003'          
               ]

PDG2010_NBF = ['--',
               '0.0389 +/- 0.0005',
               '0.139 +/- 0.005',
               '0.0809 +/- 0.0021',
               '--',
               '0.094 +/- 0.004',
               '0.0608 +/- 0.0029',
               '0.0149 +/- 0.0004',
               '0.0690 +/- 0.0032',
               '0.0310 +/- 0.0011',
               '0.0098 +/- 0.0004'          
               ]


Generic281v0_NBF = ['9797000',
                    '0.0383',
                    '0.139',
                    '0.07867',
                    '7346000',
                    '0.09',
                    '0.06812',
                    '0.01445',
                    '0.05425',
                    '0.03582',
                    '0.01493'          
                    ]

Generic281_NBF = ['20065001',
                  '0.0382',
                  '0.1350',
                  '0.0770',
                  '15932489',
                  '0.0951',
                  '0.0599',
                  '0.0147',
                  '0.0700',
                  '0.0310',
                  '0.0100'          
                  ]


Generic818_NBF = ['58389155',
                  '0.0382',
                  '0.1350',
                  '0.0770',
                  '46363545',
                  '0.0951',
                  '0.0599',
                  '0.0147',
                  '0.0700',
                  '0.0310',
                  '0.0100'          
                  ]

NBF_dict ={
    'ND0D0Bar'    : '$N_{D^0\\bar D^0}$',
    'BrD2KPi'     : '${\cal B}(\Dzkpi)$',
    'BrD2KPiPi0'  : '${\cal B}(\Dzkpipiz)$',
    'BrD2KPiPiPi' : '${\cal B}(\Dzkpipipi)$',
    'ND+D-'       : '$N_{D^+D^-}$',
    'BrD2KPiPi'   : '${\cal B}(\Dpkpipi)$',
    'BrD2KPiPiPi0': '${\cal B}(\Dpkpipipiz)$',
    'BrD2KsPi'    : '${\cal B}(\Dpkspi)$ ',
    'BrD2KsPiPi0' : '${\cal B}(\Dpkspipiz)$',
    'BrD2KsPiPiPi': '${\cal B}(\Dpkspipipi)$',
    'BrD2KKPi'    : '${\cal B}(\Dpkkpi)$'
    }

BF_Ratio_dict ={
    'BrD2KPiPi0 / BrD2KPi': '${{\calB}(\Dzkpipiz)}/{{\calB}(\Km\pip)}$',
    'BrD2KPiPiPi / BrD2KPi': '${{\calB}(\Dzkpipipi)}/{{\calB}(\Km\pip)}$',
    'BrD2KPiPiPi0 / BrD2KPiPi': '${{\calB}(\Dpkpipipiz)}/{{\calB}(\Km\pip\pip)}$',
    'BrD2KsPi / BrD2KPiPi': '${{\calB}(\Dpkspi)}/{{\calB}(\Km\pip\pip)}$',
    'BrD2KsPiPi0 / BrD2KPiPi': '${{\calB}(\Dpkspipiz)}/{{\calB}(\Km\pip\pip)}$',
    'BrD2KsPiPiPi / BrD2KPiPi': '${{\calB}(\Dpkspipipi)}/{{\calB}(\Km\pip\pip)}$',
    'BrD2KKPi / BrD2KPiPi': '${{\calB}(\Dpkkpi)}/{{\calB}(\Km\pip\pip)}$'
    }

NBF_BF_Ratio_dict = NBF_dict
NBF_BF_Ratio_dict.update(BF_Ratio_dict)

cross_sections_dict = {
    'sigma(D0D0bar)': 'sigma( e^+e^-\\to D^0\\bar D^0 )',
    'sigma(D+D-)': 'sigma( e^+e^-\\to D^+ D^- )',
    'sigma(DDbar)': 'sigma( e^+e^-\\to D\\bar D )',
    'chg/neu': 'sigma( e^+e^-\\to D^+ D^- ) / sigma( e^+e^-\\to D^0\\bar D^0 )'
    }


weblinks = {
    'generic_mc-ddbar-dskim_20xlumi_data43': 'http://www.lepp.cornell.edu/~dskim/private/dskimMon/20060224_FULL_3/dskim_data43DDTE20lumi16hr11min51sec_Jun_9_2007/individual.html',
    'generic_mc-ddbar-dskim_20xlumi_data44': 'http://www.lepp.cornell.edu/~dskim/private/dskimMon/20060224_FULL_3/dskim_data44DDTE20lumi16hr12min33sec_Sep_17_2007/individual.html',
    'generic_mc-ddbar-dskim_20xlumi_data45': 'http://www.lepp.cornell.edu/~dskim/private/dskimMon/20060224_FULL_A_3/dskim_data45DDTE20lumi10hr43min25sec_Feb_11_2008/individual.html',
    'generic_mc-ddbar-dskim_20xlumi_data46': 'http://www.lepp.cornell.edu/~dskim/private/dskimMon/20060224_FULL_A_3/dskim_data46DDTE20lumi14hr36min42sec_Feb_15_2008/individual.html'
    }

gen_core_content = {
    'cleog': '''
c3rel $CGRELEASE
if [ ! -e $TOPDIR/cleog$CGSUFFIX ] ; then mkdir $TOPDIR/cleog$CGSUFFIX ; fi
#export NUMEVT=10
export NUMEVT=`cat $SCRIPTDIR/tag_numbers/$STRING`
export RUNNUMBER=`nl -s " " $SCRIPTDIR/runlist | grep " $SGE_TASK_ID " | awk '{ print $2 }'`
export OUTDIR=$TOPDIR/cleog$CGSUFFIX
suez -f genmc.tcl
''',
    'pass2':  '''
c3rel $P2RELEASE
if [ ! -e $TOPDIR/pass2$SUFFIX ] ; then mkdir $TOPDIR/pass2$SUFFIX ; fi
export INDIR=$TOPDIR/cleog$CGSUFFIX
export OUTDIR=$TOPDIR/pass2$SUFFIX
ls $C3_INFO/data/runinfo.runinfo > /dev/null
suez -f mcp2.tcl
''',
    'dskim': '''
c3rel $DSKIMRELEASE
if [ ! -e $TOPDIR/dskim$SUFFIX ] ; then mkdir $TOPDIR/dskim$SUFFIX ; fi
export INDIR=$TOPDIR/pass2$SUFFIX
export OUTDIR=$TOPDIR/dskim$SUFFIX
ls $C3_INFO/data/runinfo.runinfo > /dev/null
suez -f dskim.tcl
'''
    }

lumi_scale_factors = { #from CBX05-10 Table V
    'data31': 0.926,
    'data32': 0.925,
    'data33': 0.929,
    'data35': 0.937,
    'data36': 0.958,
    'data37': 0.981,
    'data43': 1,
    'data44': 1,
    'data45': 1,
    'data46': 1
    }



multiplicity_weight_ntr = {
    'init': {0: 1/1.15,
             1: 1/1.071,
             2: 1/0.955,
             3: 1/0.955,
             4: 1/1.04,
             5: 1/0.991,
             6: 1/2.64,
             7: 1/10.3 },
    'inc': { 0: 1/1.3,
             1: 1/1.15,
             2: 1/1.0,
             3: 1/0.85,
             4: 1/0.85,
             5: 1/0.7,
             6: 1/0.4,
             7: 1/0.2 },
    'dec': { 0: 1/0.7,
             1: 1/0.85,
             2: 1/1.0,
             3: 1/1.15,
             4: 1/1.15,
             5: 1/1.30,
             6: 1/5.0,
             7: 1/10.0 }
    }


multiplicity_weight_npi0 = {
    'init': { 0: 1.0,
              1: 1.0,
              2: 1.0,
              3: 1.0,
              4: 1.0,
              5: 1.0 },
    'inc': { 0: 1/1.3,
             1: 1/1.15,
             2: 1/1.0,
             3: 1/0.85,
             4: 1/0.7,
             5: 1/0.4 },
    'dec':  { 0: 1/0.7,
              1: 1/0.85,
              2: 1/1.0,
              3: 1/1.15,
              4: 1/1.30,
              5: 1/5.0 }
}

## CORRESPONDS TO GENERIC MC
width_modes = { '0': 0.00126, '1': 0.00160, '3': 0.00131, '200': 0.00128,
                '201': 0.00144, '202': 0.00127, '203': 0.00148,
                '204': 0.00128, '205': 0.00129 }
n_modes = { '0': 3.73, '1': 6.09, '3': 4.23, '200': 5.99, '201': 5.0,
            '202': 5.03, '202': 5.0, '203': 5.0, '204': 5.0, '205': 5.0 }
alpha_modes = { '0': -1.54, '1': -1.39, '3': -1.65, '200': -1.52, '201': -1.5,
                '202': -1.55, '203': -1.5, '204': -1.5, '205': -1.5 }

#--------------------------------------------------
# Constructed Attrs
#--------------------------------------------------


single_mode_list = [] 
single_mode_list_p = [] 
single_mode_list_m = []
single_mode_list_ks = []
single_mode_list_ks_p = []
single_org_dict ={}
single_tex_dict ={}

for k, v in modes.items():
    single_mode_list.append('Single_' + v['fname'])
    single_mode_list.append('Single_' + v['fnamebar'])

    single_mode_list_p.append('Single_' + v['fname'])
    single_mode_list_m.append('Single_' + v['fnamebar'])

    single_org_dict[v['fname']]= v['orgname']
    single_org_dict[v['fnamebar']]= v['orgnamebar']

    single_tex_dict[v['fname']]= v['lname']
    single_tex_dict[v['fnamebar']]= v['lnamebar']

    if k in [202, 203, 204]:
        single_mode_list_ks.append('Single_' + v['fname'])
        single_mode_list_ks.append('Single_' + v['fnamebar'])
        single_mode_list_ks_p.append('Single_' + v['fname'])


double_tex_dict ={}
for i, j in PossibleDoubleTags:
    fname    = modes[i]['fname']
    fnamebar = modes[j]['fnamebar']
    key = fname + ' ' + fnamebar

    hname    = modes[i]['lname']
    hnamebar = modes[j]['lnamebar']
    value    = hname + ' ' + hnamebar 
    double_tex_dict[key] = value

diag_double_mode_list = []
diag_single_mode_list = [] 
diag_single_mode_list_ks = []

for tag in DiagDoubleTags:
    pmode = tag[0]
    mmode = tag[1]
    modename = 'Double_'+modes[pmode]['fname']+'__'+modes[mmode]['fnamebar']
    diag_double_mode_list.append(modename)
    modename = 'Single_'+modes[pmode]['fname']+'__'+modes[mmode]['fnamebar']
    diag_single_mode_list.append(modename)
    if pmode in [202, 203, 204]:
        diag_single_mode_list_ks.append(modename)

 

double_mode_list = []
clean_double_mode_list = [] 
for tag in PossibleDoubleTags:
    pmode = tag[0]
    mmode = tag[1]
    modename = 'Double_'+modes[pmode]['fname']+'__'+modes[mmode]['fnamebar']
    double_mode_list.append(modename)
    if pmode in [0, 200] or mmode in [0, 200]:
        clean_double_mode_list.append(modename)

double_d0_mode_list = []
for tag in DoubleTags_DZ:
    pmode = tag[0]
    mmode = tag[1]
    modename = 'Double_'+modes[pmode]['fname']+'__'+modes[mmode]['fnamebar']
    double_d0_mode_list.append(modename)

double_dp_mode_list = []
for tag in DoubleTags_DP:
    pmode = tag[0]
    mmode = tag[1]
    modename = 'Double_'+modes[pmode]['fname']+'__'+modes[mmode]['fnamebar']
    double_dp_mode_list.append(modename)

     
nondiag_double_mode_list = [] 
for tag in NonDiagDoubleTags:
    pmode = tag[0]
    mmode = tag[1]
    modename = 'Double_'+modes[pmode]['fname']+'__'+modes[mmode]['fnamebar']
    nondiag_double_mode_list.append(modename)

clean_double_mode_list = [] 
for tag in PossibleDoubleTags:
    pmode = tag[0]
    mmode = tag[1]
    if pmode in [0, 200] or mmode in [0, 200]:
        modename = 'Double_'+modes[pmode]['fname']+'__'+modes[mmode]['fnamebar']
        clean_double_mode_list.append(modename)


#----------------------------------------------------------
#  Constants for Cuts
#----------------------------------------------------------
etamunu = (1, -1, -1, -1)

# Ds min mode number
DS_STARTS_FROM = 400

# pi0 shower energy minimum
pi0semin = 0.03 

# delta E sideband
def desideband(mode, side):
    decutl = modes[mode]['decutl']
    decuth = modes[mode]['decuth']
    de_half_width = (decuth - decutl)/2.

    desideband_low_l = decutl - de_half_width
    desideband_low_h = decutl

    desideband_high_l = decuth
    desideband_high_h = decuth + de_half_width

    # if mode == 200:
    #     offset = 0.01
    #     desideband_low_l =  desideband_low_l - offset
    #     desideband_low_h =  desideband_low_h - offset

    #     desideband_high_l = desideband_high_l + offset
    #     desideband_high_h = desideband_high_h + offset

    if side == 'low':
        alt_deltae = { 'decutl': desideband_low_l,
                       'decuth': desideband_low_h}
    elif side == 'high':
        alt_deltae = { 'decutl': desideband_high_l,
                       'decuth': desideband_high_h}
    else:
        raise NameError(side)
    
    return alt_deltae




#--------------------------------------------------
# Functions
#--------------------------------------------------



def get_tag_numbers(mode):
    if 'Single_' in mode:
        name = mode.replace('Single_', '')
        mode_key = mode_name_to_key(name)
        if mode_key != None:
            tag_number = modes[mode_key]['tag_num_s']
        else:
            tag_number = bkgmodes[name]['tag_num_s']
            
    elif 'Double_' in mode:
        tag_number = 2000
    else:
        raise NameError

    return tag_number


def get_generated_numbers(tag, jobs=30, mode=None):
    numbers  =  []
    if tag == 'double': 
        for i, j in PossibleDoubleTags:
            tag_number = 2000
            count = tag_number*jobs
            numbers.append(count)
        if mode != None:
            numbers = [count, count]
            
    if tag == 'single':
        mode_sign_list  = [(i,j) for i in modes for j in (1, -1)]
        if mode != None:
            if isinstance(mode, str):
                mode_list = map(int, mode.split(','))
            elif isinstance(mode, int):
                mode_list = [mode]
            else:
                raise TypeError(mode)
            mode_sign_list = [(i,j) for i in mode_list for j in (1, -1)]

        for mode, sign in mode_sign_list:
            tag_number = modes[mode]['tag_num_s']
            count = tag_number*jobs
            numbers.append(count)

    return numbers



def mode_name_to_key(name):
    for k, v in modes.items():
        if v['fname'] == name or v['fnamebar'] == name:
            return k

def get_dataset_by_run(run):
    if (200978 <= run and run <= 202101):
        dataset = 'data31'        
    elif (202126 <= run and run <= 203089):
        dataset = 'data32'        
    elif (203104 <= run and run <= 203634):
        dataset = 'data33'        
    elif (203912 <= run and run <= 204348):
        dataset = 'data34'        
    elif (204862 <= run and run <= 206185):
        dataset = 'data35'        
    elif (206359 <= run and run <= 208063):
        dataset = 'data36'        
    elif (208067 <= run and run <= 209967):
        dataset = 'data37'        
    else:
        raise ValueError(run)
    return dataset 

def get_runs_range(datasetname):
    if 'data31' in datasetname:
        low, high = 200978, 202101
    elif 'data32' in datasetname:
        low, high = 202126, 203089
    elif 'data33' in datasetname:
        low, high = 203104, 203634
    elif 'data35' in datasetname:
        low, high = 204862, 206185
    elif 'data36' in datasetname:
        low, high = 206359, 208063
    elif 'data37' in datasetname:
        low, high = 208067, 209967

    elif 'data43' in datasetname:
        low, high = 220898, 223271
    elif 'data44' in datasetname:
        low, high = 223279, 226042
    elif 'data45' in datasetname:
        low, high = 226429, 228271
    elif 'data46' in datasetname:
        low, high = 228285, 230130
    else:
        raise NameError(datasetname)
    return low, high


def get_dataset_numbers(label):
    numbers_281 = ['31', '32_1', '32_2', '33', '35', '36', '37_1', '37_2']
    numbers_537 = ['43_1', '43_2', '44_1', '44_2', '44_3', '45_1', '45_2',
		   '46_1', '46_2']

    if label == '281ipb':
	numbers = numbers_281
    elif label == '537ipb':
	numbers = numbers_537
    elif label == '818ipb':
	numbers = numbers_281 + numbers_537
    else:
        raise NameError(label)
    return numbers


def get_dcsd_correction():
    from uncertainties import ufloat, umath

    corr = []
    dz_modes = [(i,j) for i in [0,1,3] for j in [0,1,3]]
    for i,j in dz_modes:
        r_i_val = modes[i]['amplitude ratio']
        r_j_val = modes[j]['amplitude ratio']

        r_i_err = modes[i]['amplitude ratio err']
        r_j_err = modes[j]['amplitude ratio err']

        r_i = ufloat((r_i_val, r_i_err))
        r_j = ufloat((r_j_val, r_j_err))

        delta_i_val = modes[i]['phase']
        delta_j_val = modes[j]['phase']

        delta_i_err = modes[i]['phase err']
        delta_j_err = modes[j]['phase err']

        delta_i = ufloat((delta_i_val, delta_i_err))
        delta_j = ufloat((delta_j_val, delta_j_err))

        R_i_val = modes[i]['coherence factor']
        R_j_val = modes[j]['coherence factor']

        R_i_err = modes[i]['coherence factor err']
        R_j_err = modes[j]['coherence factor err']

        R_i = ufloat((R_i_val, R_i_err))
        R_j = ufloat((R_i_val, R_i_err))

        correction = 1 - 2*r_i*r_j*umath.cos(
            delta_i + delta_j ) + r_i**2 * r_j**2
        yield_factor = 1/correction
        corr.append(str(yield_factor))

    return corr


def get_pi0_eff_correction(p_avg):
    # CBX 2008-029 (\pi0 Finding Efficiencies)
    # Table 11
    a0_val = 0.939
    a0_err = 0.022
    a1_val = 0.001
    a1_err = 0.021
    rho = -0.947

    # Equation 8, 9
    ratio_val = a1_val*p_avg + a0_val
    ratio_err = sqrt(a1_err**2*p_avg**2 + a0_err**2
                     + 2*rho*a0_err*a1_err*p_avg)

    ratio = '%s +/- %s' %(ratio_val, ratio_err)
    return ratio

    
def sys_err(label):
    sys_err = None
    sys_err_by_mode = None
    
    if label == '281ipbv0.1/generic':
        from attr.syserr_281ipbv0_generic import sys_err
    elif label == '281ipbv0/generic':
        from attr.syserr_281ipbv0_generic import sys_err
    elif label == '281ipbv12.0':
        from attr.syserr_281ipbv0 import sys_err, sys_err_by_mode
    elif label == '818ipbv12.0':
        from attr.syserr_818ipbv10 import sys_err, sys_err_by_mode
    elif label == '281ipbv12.0/generic' or label == '281ipbv12.1/generic' \
             or label == '281ipbv12.2/generic': 
        from attr.syserr_818ipbv7_generic import sys_err
    elif label == '818ipbv12.0/generic' or label == '818ipbv12.2/generic':
        from attr.syserr_818ipbv7_generic import sys_err
    elif label == '818ipbv12.1':
        from attr.syserr_818ipbv12 import sys_err, sys_err_by_mode
    elif label == '818ipbv12.2' or label == '818ipbv12.3':
        from attr.syserr_818ipbv12_2 import sys_err, sys_err_by_mode
    elif label == '818ipbv12.2' or label == '818ipbv12.3':
        from attr.syserr_818ipbv12_2 import sys_err, sys_err_by_mode
    elif label == '818ipbv12.4' :
        from attr.syserr_818ipbv12_4 import sys_err, sys_err_by_mode
    else:
        raise NameError(label)
    return sys_err, sys_err_by_mode


def import_bkg(label):
    if label == '281ipbv0.1/generic': 
        from attr import bkg_281ipbv0_generic as bkg
    elif label == '281ipbv0/generic': 
        from attr import bkg_281ipbv0_generic as bkg
    elif label == '281ipbv12.0': 
        from attr import bkg_281ipbv0 as bkg
    elif label == '281ipbv12.0/generic' or label == '281ipbv12.1/generic'\
             or label == '281ipbv12.2/generic': 
        from attr import bkg_281ipbv12_generic as bkg
    elif label == '818ipbv12.0': 
        from attr import bkg_818ipbv11 as bkg
    elif label == '818ipbv12.0/generic' or label == '818ipbv12.2/generic': 
        from attr import bkg_818ipbv7_generic as bkg
    elif label == '818ipbv12.1' or label == '818ipbv12.2' \
            or label == '818ipbv12.3' or label == '818ipbv12.4': 
        from attr import bkg_818ipbv12 as bkg
    else:
        raise NameError(label)
    return bkg 


brs_pdg2004 =[
    'exec addPdg 1 0.0380 0.0009 \n' ,
    'exec addPdg 2 0.130 0.008   \n' ,
    'exec addPdg 3 0.0746 0.0031 \n' ,
    'exec addPdg 4 0.092 0.006   \n' ,
    'exec addPdg 5 0.065 0.011   \n' ,
    'exec addPdg 6 0.0141 0.0010 \n' ,
    'exec addPdg 7 0.0485 0.015  \n' ,
    'exec addPdg 8 0.0355 0.005  \n' ,
    'exec addPdg 9 0.0089 0.0008 \n' 
    ]
    

brs_pdg2010 = [
    'exec addPdg 1 0.0389 0.0005 \n' ,
    'exec addPdg 2 0.139 0.005   \n' ,
    'exec addPdg 3 0.0809 0.0021 \n' ,
    'exec addPdg 4 0.094 0.004   \n' ,
    'exec addPdg 5 0.0608 0.0029 \n' ,
    'exec addPdg 6 0.0149 0.0004 \n' ,
    'exec addPdg 7 0.0690 0.0032 \n' ,
    'exec addPdg 8 0.0310 0.0011 \n' ,
    'exec addPdg 9 0.0098 0.0004 \n' 
    ]


trk_pid_effs_281 = {
    'K tracking': {
        'Data': {
            '+': ['.9175 +/- .0065', '.8700 +/- .0069', '.8645 +/- .0086', 
                  '.9116 +/- .0152', '.8515 +/- .0181', '.8526 +/- .0087'], 
            '-': ['.8989 +/- .0068', '.8516 +/- .0069', '.8396 +/- .0087',
                  '.9229 +/- .0150', '.8309 +/- .0163', '.8493 +/- .0085']},
        
        'MC': {
            '+': ['.9114 +/- .0020', '.8719 +/- .0021', '.8435 +/- .0029',
                  '.9122 +/- .0041', '.8761 +/- .0046', '.8500 +/- .0023'],
            '-': ['.9074 +/- .0020', '.8712 +/- .0021', '.8418 +/- .0029',
                  '.9122 +/- .0042', '.8648 +/- .0046', '.8417 +/- .0023']}
        }, 

    'K PID': {
        'Data': {
            '+': ['.9574 +/- .0020'],
            '-': ['.9517 +/- .0020']},
        'MC': {
            '+': ['.9664 +/- .0006'],
            '-': ['.9640 +/- .0006']}
        },

    'pi tracking': {
        'Data': {
            '+': ['.9941 +/- .0080', '.9654 +/- .0039'],
            '-': ['.9808 +/- .0084', '.9716 +/- .0038']},
        'MC': {
            '+': ['.9776 +/- .0027', '.9697 +/- .0013'],
            '-': ['.9723 +/- .0027', '.9731 +/- .0013']}
        }, 

    'pi PID': {
        'Data': {
            '+': ['.9824 +/- .0005'],
            '-': ['.9846 +/- .0005']},
        'MC': {
            '+': ['.9891 +/- .0002'],
            '-': ['.9887 +/- .0002']}
        }
    }

trk_pid_effs_818 = {
    'K tracking': {
        'Data': {
            '+': ['.9097 +/- .0038', '.8568 +/- .0057', '.8481 +/- .0039'], 
            '-': ['.8989 +/- .0039', '.8568 +/- .0057', '.8412 +/- .0038']},
        
        'MC': {
            '+': ['.9067 +/- .0008', '.8723 +/- .0013', '.8429 +/- .0008'],
            '-': ['.9045 +/- .0008', '.8693 +/- .0013', '.8364 +/- .0008']}
        }, 

    'K PID': {
        'Data': {
            '+': ['.9574 +/- .0020'],
            '-': ['.9517 +/- .0020']},
        'MC': {
            '+': ['.9664 +/- .0006'],
            '-': ['.9640 +/- .0006']}
        },

    'pi tracking': {
        'Data': {
            '+': ['.9810 +/- .0047', '.9735 +/- .0017'],
            '-': ['.9749 +/- .0048', '.9727 +/- .0017']},
        'MC': {
            '+': ['.9786 +/- .0011', '.9715 +/- .0004'],
            '-': ['.9772 +/- .0011', '.9709 +/- .0004']}
        }, 

    'pi PID': {
        'Data': {
            '+': ['.9824 +/- .0005'],
            '-': ['.9846 +/- .0005']},
        'MC': {
            '+': ['.9891 +/- .0002'],
            '-': ['.9887 +/- .0002']}
        }
    }




def get_cp_asymmetry(name, label):
    from uncertainties import ufloat

    def avg(a, sa, b, sb):
        avg = (a/sa**2 + b/sb**2)/(1/sa**2 + 1/sb**2)
        savg = 1/sqrt(1/sa**2 + 1/sb**2)
        return avg, savg

    def calc_weighted_avg(l):
        neum = 0 
        denom = 0 
        for uval in l:
            val = uval.nominal_value
            err = uval.std_dev()
            neum += val/err**2
            denom += 1/err**2
        avg = neum/denom
        avg_err = 1/sqrt(denom)
        return ufloat((avg, avg_err))

    def calc_chdiff(pm):
        epu = str_to_ufloat(pm[0])
        emu = str_to_ufloat(pm[1])
        uval = epu/emu -1
        return uval
     
    def str_to_ufloat(s):
        val = float(s.split('+/-')[0])
        err = float(s.split('+/-')[1])
        ufl = ufloat((val, err))
        return ufl

    def calc_asy(pm):
        epu = str_to_ufloat(pm[0])
        emu = str_to_ufloat(pm[1])
        uval = (epu - emu)/(epu + emu)
        return uval

    def asy(valpair):
        ps = valpair['+']
        ms = valpair['-']
        pms = zip(ps, ms)
        asys = map(calc_asy, pms)
        avg_asy = calc_weighted_avg(asys)
        return avg_asy

    def calc_syst(uval):
        val = uval.nominal_value
        err = uval.std_dev()
        syst = sqrt(val**2 + err**2)
        return syst
    
    if '281ipb' in label:
        effs = trk_pid_effs_281
    elif '818ipb' in label:
        effs = trk_pid_effs_818
    else:
        raise NameError(label)

    asy_dt = asy(effs[name]['Data'])
    asy_mc = asy(effs[name]['MC'])
    dt_mc_diff = asy_dt - asy_mc
    syst = calc_syst(dt_mc_diff)
    
    row = map(str, [name, asy_dt, asy_mc, dt_mc_diff, syst])
    return row
