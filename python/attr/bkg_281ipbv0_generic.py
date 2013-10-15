"""
Providing Attributes of Backgrounds for BF fitter

"""

__author__ = "Xin Shi <xs32@cornell.edu>"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2006-2011 Xin Shi"
__license__ = "GNU GPL"

#efficiencies and uncertainties for signal
efficiencies_single = {
    '0': .662,
    '1': .356,
    '3': .469,
    '200': .552,
    '201': .283,
    '202': .454,
    '203': .244,
    '204': .318,
    '205': .470 }

efficiencies_single_uc = {
    '0': .003,
    '1': .001,
    '3': .002,
    '200': .002,
    '201': .002,
    '202': .004,
    '203': .002,
    '204': .002,
    '205': .004 }

#efficiencies and uncertainties for background [generic]
bkg_efficiencies_single = {
    'kpi': .663,
    'kpipi0': .356,
    'k3pi': .470,
    'kkspi': 0.128,
    'kkspibar': 0.128,
    #'k3pigam': 0.00415,
    '3pi': 1,
    '3pipi0': 1,
    '5pi': 1,
    'kskspi': 0.013}
#'ks3pigam': 0.00445 }

bkg_efficiencies_single_uc = {
    'kpi': .005,
    'kpipi0': .012,
    'k3pi': .010,
    'kkspi': .004,
    'kkspibar': .004,
    #    'k3pigam': 0.0007,
    '3pi': 0,
    '3pipi0': 0,
    '5pi': 0,
    'kskspi': .001}
# 'ks3pigam': 0.0008 }

#BF for signal modes [ in generic MC ]
pdg_bf = {
    '0': 0.0383,    #0.0391,
    '1': 0.139,     #0.1494,
    '3': 0.07867,   #0.0829,
    '200': 0.09,    #0.0952,
    '201': 0.06812, #0.0604,
    '202': 0.01445, #0.0155,
    '203': 0.05425, #0.0717,
    '204': 0.03582, #0.0320,
    '205': 0.01493  #0.0097
    }

#BF for background modes [generic MC]
bkg_pdg_bf = {
    'kpi': 1.5e-4,    #1.43e-4,
    'kpipi0': 5e-4,   #3.29e-4,
    'k3pi': 0,        #2.49e-4,
    'kkspi': 1.43e-3, #3.4e-3,
    'kkspibar': 7.33e-4, #2.6e-3,
    #'k3pigam': 0.00381,
    '3pi': 477, #81,
    '3pipi0': 3381, #188,
    '5pi': 1866, #117,
    'kskspi': 3.763e-3} #, 5.3e-3,
#'ks3pigam':  0.00025 }


bkg_pdg_bf_uc = {
    'kpi': 0,  #0.4e-4,
    'kpipi0': 0, #0.30e-4,
    'k3pi': 0, #0.21e-4,
    'kkspi': 0, #0.5e-3,
    'kkspibar': 0, #0.5e-3,
    #'k3pigam': 1e-4,
    '3pi': 0, #21.7,
    '3pipi0': 0, # 55.7,
    '5pi': 0, #79.4,
    'kskspi': 0} #2.3e-3,
#    'ks3pigam': 1e-4 }

## bkg_bf_corfac = { 'kpi': 1.0, 'kpipi0': 17240./19985., 'k3pi': 18350./19985.,
##                   'kkspi': 19966./19985., 'kkspibar': 18313./19985.,
##                   '3pi': 1.0, '3pipi0': 1.0, '5pi': 1.0,
##                   'kskspi': 1.0 }

dcsd_pdg_bf = { '0': bkg_pdg_bf['kpi'],
                '1': bkg_pdg_bf['kpipi0'],
                '3': bkg_pdg_bf['k3pi'] }

dcsd_efficiencies_single = { '0': bkg_efficiencies_single['kpi'],
                             '1': bkg_efficiencies_single['kpipi0'],
                             '3': bkg_efficiencies_single['k3pi'] }

# The following gives D0 -> KS K+ pi-
scsd_pdg_bf = { '3': bkg_pdg_bf['kkspibar'] }
scsd_efficiencies_single = { '3': bkg_efficiencies_single['kkspibar'] }

total_d0d0b = 7067128
total_dpdm = 5300525
total_ddbar = total_d0d0b+total_dpdm

fake_mode_list = { 'kpi': '0', 'kpipi0': '1',  'kkspi': '3', 'kkspibar': '3',
##                   'k3pigam': '3',
                   '3pi': '202', '5pi': '204', 'kskspi': '204',
                   '3pipi0': '203', 'k3pi': '3',
##                   'ks3pigam': '204'
                   }
fake_mode_order = [ 'kpi', 'kpipi0', 'k3pi', 'kkspi', 'kkspibar',
##                    'k3pigam',
                    'd0generic',
                    '3pi', '3pipi0', '5pi', 'kskspi',
##                    'ks3pigam',
                    'dpgeneric' ]

single_tag_order = [ '0', '1', '3', '200', '201', '202', '203', '204', '205' ]




